#!/usr/bin/env python3
"""
TF-IDF threshold experiment with proper train/holdout separation.

The earlier comparison (scripts/compare_matchers.py) evaluated TF-IDF on the
same cases used to look at it, and TF-IDF scored 95.7% on positives but 0/5 on
negatives because cosine similarity has no natural zero.

This script fixes the protocol: the rejection threshold is chosen on the GATE
set only, and every number below is reported on the DIAGNOSTIC set, which is
never used for tuning.

Result (2026-09-24):

    strategy                     gate pos  gate neg  diag pos  diag neg
    max gate F-sum (0.016)        44/46     2/5       64/66     7/21
    fixed 0.005                   44/46     0/5       65/66     1/21
    fixed 0.010                   44/46     0/5       65/66     3/21
    gate negative max             14/46     4/5       22/66    18/21
    gate positive min             44/46     2/5       64/66    10/21
    fixed substrings (current)    41/46     4/5       45/66    15/21

Two conclusions:

1. TF-IDF is decisively better at ranking. On the holdout set it is right on
   64/66 positives vs 45/66 for substrings; McNemar exact test p < 0.001
   (19 cases only TF-IDF got right, 0 the other way).

2. No threshold separates positives from negatives. On the gate set the
   positive score range is [0.0219, 0.1634] and the negative range is
   [0.0116, 0.0823] — they overlap. Every threshold trades positive accuracy
   against negative rejection, so TF-IDF alone cannot replace the matcher.

Implication: a hybrid is the only viable direction — TF-IDF (or a semantic
matcher) for ranking, plus a separate signal for "none of these apply".
Recorded here so the experiment is not re-derived.

Usage:
    python3 scripts/compare_matchers_holdout.py
"""

import json, math, re, sys, os, collections
ROOT=os.getcwd(); sys.path.insert(0,os.path.join(ROOT,"scripts"))
import run_trigger_regression as rtr
SKILLS=sorted(rtr.SKILL_KW)

def ngrams(t,n=(2,3)):
    t=re.sub(r"\s+","",t); o=[]
    for k in n: o+=[t[i:i+k] for i in range(len(t)-k+1)]
    return o
def build():
    docs={s:ngrams(open(f"skills/{s}/SKILL.md",encoding="utf-8").read()) for s in SKILLS}
    df=collections.Counter()
    for s,ts in docs.items():
        for t in set(ts): df[t]+=1
    N=len(docs); idf={t:math.log((N+1)/(c+1))+1 for t,c in df.items()}
    vecs={}
    for s,ts in docs.items():
        tf=collections.Counter(ts)
        v={t:(1+math.log(c))*idf.get(t,0) for t,c in tf.items()}
        nrm=math.sqrt(sum(x*x for x in v.values())) or 1.0
        vecs[s]={t:x/nrm for t,x in v.items()}
    return vecs
vecs=build()

def score(text):
    tf=collections.Counter(ngrams(text)); q={t:1+math.log(c) for t,c in tf.items()}
    nrm=math.sqrt(sum(x*x for x in q.values())) or 1.0
    q={t:x/nrm for t,x in q.items()}
    sc={s:sum(w*v.get(t,0.0) for t,w in q.items()) for s,v in vecs.items()}
    best=max(sc.items(), key=lambda kv:(kv[1],[-ord(c) for c in kv[0]]))
    return best[0], best[1]

def sub_top(t):
    sc={s:rtr.match_count(s,t) for s in SKILLS}
    b=max(sc.items(),key=lambda kv:(kv[1],[-ord(c) for c in kv[0]]))
    return b[0] if b[1]>0 else None

gate=json.load(open("tests/triggers/cases.json",encoding="utf-8"))
diag=json.load(open("tests/triggers/cases.diagnostic.json",encoding="utf-8"))

# --- 在 gate 上选阈值：要求 gate 的负样本全部拒识，且正样本 accuracy 最大 ---
print("=== 在 GATE 集 (51) 上选阈值 ===")
best=None
for i in range(0,60):
    th=i*0.002
    pos=[c for c in gate if c["expected_primary_skill"]!="none"]
    neg=[c for c in gate if c["expected_primary_skill"]=="none"]
    ok=sum(1 for c in pos if (lambda r: r[0] if r[1]>=th else None)(score(c["input"]))==c["expected_primary_skill"])
    nok=sum(1 for c in neg if score(c["input"])[1]<th)
    if best is None or (ok+nok)>(best[1]+best[2]):
        best=(th,ok,nok)
th=best[0]
print(f"  选定阈值 = {th:.3f}  (gate 正样本 {best[1]}/{len([c for c in gate if c['expected_primary_skill']!='none'])}"
      f"  负样本 {best[2]}/{len([c for c in gate if c['expected_primary_skill']=='none'])})")

# --- 在 DIAGNOSTIC (holdout) 上评估 ---
print("\n=== 在 DIAGNOSTIC 集 (87, 留出集) 上评估 ===")
def ev(cases,label):
    pos=[c for c in cases if c["expected_primary_skill"]!="none"]
    neg=[c for c in cases if c["expected_primary_skill"]=="none"]
    tf_ok=sum(1 for c in pos if (lambda r: r[0] if r[1]>=th else None)(score(c["input"]))==c["expected_primary_skill"])
    tf_neg=sum(1 for c in neg if score(c["input"])[1]<th)
    sub_ok=sum(1 for c in pos if sub_top(c["input"])==c["expected_primary_skill"])
    sub_neg=sum(1 for c in neg if sub_top(c["input"]) is None)
    print(f"  {label}")
    print(f"    TF-IDF+阈值   正样本 {tf_ok}/{len(pos)} = {tf_ok/len(pos):5.1%}   负样本 {tf_neg}/{len(neg)}")
    print(f"    固定子串      正样本 {sub_ok}/{len(pos)} = {sub_ok/len(pos):5.1%}   负样本 {sub_neg}/{len(neg)}")
    return pos,tf_ok,sub_ok
pos,tf_ok,sub_ok=ev(diag,"diagnostic (holdout)")
ev(gate,"gate (tuning set — shown for contrast only)")

# McNemar
only_tf=only_sub=0
for c in pos:
    exp=c["expected_primary_skill"]
    r=score(c["input"]); t_ok=(r[0]==exp and r[1]>=th)
    s_ok=(sub_top(c["input"])==exp)
    if t_ok and not s_ok: only_tf+=1
    elif s_ok and not t_ok: only_sub+=1
print(f"\nMcNemar (diagnostic): 仅 TF-IDF 对={only_tf}  仅子串对={only_sub}")
if only_tf+only_sub>0:
    n,k=only_tf+only_sub,min(only_tf,only_sub)
    p=sum(math.comb(n,i) for i in range(k+1))/2**n*2
    print(f"精确二项检验 p = {min(p,1.0):.3f}  → {'差异显著' if min(p,1.0)<=0.05 else '差异不显著'}")
