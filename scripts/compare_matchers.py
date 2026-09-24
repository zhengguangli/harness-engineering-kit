#!/usr/bin/env python3
"""
Matcher comparison experiment — fixed substrings vs character n-gram TF-IDF.

Answers the question "would a different matching mechanism discriminate better?"
using only the stdlib (no numpy/sklearn/jieba). Chinese needs no word
segmentation when matching on character n-grams.

Result (2026-09-24, n=46 positive cases):

    method                        positive acc   negative rejection
    fixed substrings (current)    89.1% (41/46)  4/5
    TF-IDF over routing fields    34.8% (16/46)  4/5
    TF-IDF over full SKILL.md     95.7% (44/46)  0/5

McNemar exact test on the paired comparison: p = 0.375 — the 89.1% vs 95.7%
difference is NOT statistically significant at n=46. And TF-IDF over full text
loses all negative rejection because cosine similarity is never zero, so
expressing "no skill applies" requires a threshold — and picking that threshold
on 51 cases would be overfitting.

Conclusion recorded here so it is not re-derived: with the current data volume,
neither mechanism is demonstrably better. The prerequisite is a larger labelled
set (roughly 150 cases for a +/-5% interval), not a better matcher.

Usage:
    python3 scripts/compare_matchers.py
"""

import json, math, re, sys, os, collections

ROOT = os.getcwd()
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import run_trigger_regression as rtr

SKILLS = sorted(rtr.SKILL_KW)

def ngrams(text, n=(2, 3)):
    text = re.sub(r"\s+", "", text)
    out = []
    for k in n:
        out += [text[i:i+k] for i in range(len(text)-k+1)]
    return out

def skill_doc(skill, mode):
    p = os.path.join(ROOT, "skills", skill, "SKILL.md")
    txt = open(p, encoding="utf-8").read()
    if mode == "full":
        body = txt
    else:  # routing-relevant fields only
        fm = {}
        lines = txt.splitlines()
        if lines and lines[0].strip() == "---":
            for l in lines[1:]:
                if l.strip() == "---": break
                m = re.match(r"^(\w[\w-]*)\s*:\s*(.*)", l.strip())
                if m: fm[m.group(1)] = m.group(2)
        body = " ".join(fm.get(k, "") for k in ("description", "when_to_use"))
    return body

def build(mode):
    docs = {s: ngrams(skill_doc(s, mode)) for s in SKILLS}
    df = collections.Counter()
    for s, terms in docs.items():
        for t in set(terms): df[t] += 1
    N = len(docs)
    idf = {t: math.log((N+1)/(c+1)) + 1 for t, c in df.items()}
    vecs = {}
    for s, terms in docs.items():
        tf = collections.Counter(terms)
        v = {t: (1+math.log(c)) * idf.get(t, 0) for t, c in tf.items()}
        norm = math.sqrt(sum(x*x for x in v.values())) or 1.0
        vecs[s] = {t: x/norm for t, x in v.items()}
    return vecs

def rank(vecs, text):
    q_terms = ngrams(text)
    tf = collections.Counter(q_terms)
    q = {t: 1+math.log(c) for t, c in tf.items()}
    norm = math.sqrt(sum(x*x for x in q.values())) or 1.0
    q = {t: x/norm for t, x in q.items()}
    # cosine: dot product of normalised vectors, but IDF-weight the query too
    scores = {}
    for s, v in vecs.items():
        scores[s] = sum(w * v.get(t, 0.0) for t, w in q.items())
    return sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))


cases = json.load(open(os.path.join(ROOT, "tests/triggers/cases.json"), encoding="utf-8"))
pos = [c for c in cases if c["expected_primary_skill"] != "none"]
neg = [c for c in cases if c["expected_primary_skill"] == "none"]


def _tiebreak(skill):
    """Deterministic tie-break: reverse-lexicographic, matching the repo's
    regression script so the two tools agree on ordering."""
    return [-ord(ch) for ch in skill]


def top_substring(text):
    sc = {s: rtr.match_count(s, text) for s in SKILLS}
    best = max(sc.items(), key=lambda kv: (kv[1], _tiebreak(kv[0])))
    return best[0] if best[1] > 0 else None


def top_tfidf(vecs, text):
    tf = collections.Counter(ngrams(text))
    q = {t: 1 + math.log(c) for t, c in tf.items()}
    nrm = math.sqrt(sum(x * x for x in q.values())) or 1.0
    q = {t: x / nrm for t, x in q.items()}
    sc = {s: sum(w * v.get(t, 0.0) for t, w in q.items()) for s, v in vecs.items()}
    best = max(sc.items(), key=lambda kv: (kv[1], _tiebreak(kv[0])))
    return best[0] if best[1] > 0 else None


def report():
    print("统一口径：全 13 skill 排序取 top1\n")
    b = sum(1 for c in pos if top_substring(c["input"]) == c["expected_primary_skill"])
    bn = sum(1 for c in neg if top_substring(c["input"]) is None)
    print(f"{'固定子串（现状）':<26} 正样本 {b}/{len(pos)} = {b/len(pos):5.1%}   "
          f"负样本 {bn}/{len(neg)}")
    for mode, label in [("routing", "TF-IDF 路由字段"), ("full", "TF-IDF 全文")]:
        vecs = build(mode)
        ok = sum(1 for c in pos if top_tfidf(vecs, c["input"]) == c["expected_primary_skill"])
        ng = sum(1 for c in neg if top_tfidf(vecs, c["input"]) is None)
        print(f"{label:<26} 正样本 {ok}/{len(pos)} = {ok/len(pos):5.1%}   "
              f"负样本 {ng}/{len(neg)}")

    # McNemar exact test on the paired comparison
    only_sub = only_tfidf = 0
    for c in pos:
        exp = c["expected_primary_skill"]
        s_ok = top_substring(c["input"]) == exp
        t_ok = top_tfidf(build("full"), c["input"]) == exp
        if s_ok and not t_ok:
            only_sub += 1
        elif t_ok and not s_ok:
            only_tfidf += 1
    print(f"\nMcNemar 配对比较: 仅子串对={only_sub}  仅 TF-IDF 对={only_tfidf}")
    if only_sub + only_tfidf > 0:
        n, k = only_sub + only_tfidf, min(only_sub, only_tfidf)
        p = sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n * 2
        print(f"精确二项检验 p = {min(p, 1.0):.3f}  → "
              f"{'差异不显著' if min(p,1.0) > 0.05 else '差异显著'}")


if __name__ == "__main__":
    report()
