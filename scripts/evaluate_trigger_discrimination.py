#!/usr/bin/env python3
"""
Trigger discrimination evaluation — a measurement, not a score.

Reports, from tests/triggers/cases.json:
  - ranking accuracy (does the labelled primary skill rank first?)
  - negative rejection rate
  - confusion pairs (which skills get mistaken for which)
  - per-skill recall
  - Top1-Top2 margin distribution (how decisive matches are)
  - the concrete evidence for every failure
  - a 95% Wilson confidence interval

Deliberately does NOT emit a single composite "quality score". A weighted sum of
judgement calls is not a measurement; these numbers are all derived from
labelled data and are reproducible.

Known limitation: cases.json labels only ONE correct skill per case and has 5
negatives, so precision cannot be computed — only recall and ranking accuracy.
Widening the labelled set (positive AND negative labels per case) is the
prerequisite for a precision figure.

Usage:
    python3 scripts/evaluate_trigger_discrimination.py
"""

import json, sys, collections, os
ROOT = os.getcwd()
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import run_trigger_regression as rtr

CASES_FILE = os.path.join(ROOT, "tests", "triggers", "cases.json")
DIAG_FILE = os.path.join(ROOT, "tests", "triggers", "cases.diagnostic.json")
SKILLS = sorted(rtr.SKILL_KW)


def load_cases():
    """Gate cases (must stay green) + diagnostic cases (measurement only).

    The gate set guards against keyword-table drift. The diagnostic set is
    derived from each skill's documented when_to_use contract and exists to
    produce an honest accuracy figure — it is NOT a gate, because making it one
    would force keyword tuning against the measurement set.
    """
    gate = json.load(open(CASES_FILE, encoding="utf-8")) if os.path.isfile(CASES_FILE) else []
    diag = json.load(open(DIAG_FILE, encoding="utf-8")) if os.path.isfile(DIAG_FILE) else []
    for c in gate:
        c["_set"] = "gate"
    for c in diag:
        c["_set"] = "diagnostic"
    return gate + diag


cases = load_cases()

rows = []
for c in cases:
    primary = c["expected_primary_skill"]
    text = c["input"]
    scores = {s: rtr.match_count(s, text) for s in SKILLS}
    ranked = sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))
    top = ranked[0][0] if ranked[0][1] > 0 else None
    rows.append({"id": c["id"], "primary": primary, "top": top,
                 "scores": scores, "tags": c.get("tags", []), "set": c.get("_set", "?")})

# --- 1. ranking accuracy ---
pos = [r for r in rows if r["primary"] != "none"]
neg = [r for r in rows if r["primary"] == "none"]
pos_ok = sum(1 for r in pos if r["top"] == r["primary"])
neg_ok = sum(1 for r in neg if r["top"] is None)
print("=" * 68)
print(f"触发判别力评估（基于现有 {len(cases)} 个用例）")
print("=" * 68)
print(f"正样本 ranking accuracy : {pos_ok}/{len(pos)} = {pos_ok/len(pos):.1%}")
print(f"负样本 正确拒识         : {neg_ok}/{len(neg)} = {neg_ok/len(neg):.1%}")
print(f"总体                   : {pos_ok+neg_ok}/{len(rows)} = {(pos_ok+neg_ok)/len(rows):.1%}")

print("\n按集合拆分（gate=回归门控集，diagnostic=契约派生测量集）:")
for _lbl in ("gate", "diagnostic"):
    _sp = [r for r in pos if r["set"] == _lbl]
    _sn = [r for r in neg if r["set"] == _lbl]
    _ok = sum(1 for r in _sp if r["top"] == r["primary"])
    _nok = sum(1 for r in _sn if r["top"] is None)
    print(f"  {_lbl:<12} 正样本 {_ok}/{len(_sp)} = {_ok/len(_sp):5.1%}   负样本 {_nok}/{len(_sn)}")

# --- 2. confusion pairs ---
print("\n混淆对（期望 A，实际 top 是 B）:")
conf = collections.Counter()
for r in pos:
    if r["top"] != r["primary"]:
        conf[(r["primary"], r["top"])] += 1
if not conf:
    print("  无")
for (exp, act), n in conf.most_common():
    print(f"  {exp}  ←误→  {act}   ({n} 次)")

# --- 3. per-skill recall ---
print("\n每 skill 的 recall（该 skill 的用例中 top 命中的比例）:")
per = collections.defaultdict(lambda: [0, 0])
for r in pos:
    per[r["primary"]][1] += 1
    if r["top"] == r["primary"]:
        per[r["primary"]][0] += 1
for s in sorted(per, key=lambda x: per[x][0]/per[x][1]):
    ok, tot = per[s]
    flag = "  ← 低于均值" if ok/tot < pos_ok/len(pos) else ""
    print(f"  {s:<38} {ok}/{tot}{flag}")

# --- 4. margin: 判别力有多决定性 ---
margins = []
for r in pos:
    sc = sorted(r["scores"].values(), reverse=True)
    margins.append(sc[0] - (sc[1] if len(sc) > 1 else 0))
import statistics
print(f"\nTop1-Top2 分差: 均值 {statistics.mean(margins):.2f}  "
      f"中位数 {statistics.median(margins)}  最小 {min(margins)}  最大 {max(margins)}")
ties = sum(1 for m in margins if m == 0)
print(f"分差为 0（完全打平）的用例: {ties}/{len(pos)}")
print("→ 分差越小，说明 skill 边界越模糊；打平用例是边界不清的直接证据")

# --- 5. ambiguous 标签的实际含义 ---
amb = [r for r in rows if "ambiguous" in r["tags"]]
amb_ok = sum(1 for r in amb if r["top"] == r["primary"])
print(f"\n标为 ambiguous 的 {len(amb)} 个用例中，top 命中期望 primary 的: {amb_ok}")
print("→ 若命中率显著低于总体，说明『歧义』被用作掩盖触发失败的标签")

# --- 6b. 95% Wilson 置信区间 ---
import math
def wilson(k, n, z=1.96):
    if n == 0: return (0.0, 0.0)
    p = k / n
    d = 1 + z*z/n
    c = (p + z*z/(2*n)) / d
    h = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
    return (c-h, c+h)
lo, hi = wilson(pos_ok, len(pos))
print(f"\n正样本 95% Wilson 置信区间: [{lo:.1%}, {hi:.1%}]  (宽度 {(hi-lo):.1%})")
lo2, hi2 = wilson(pos_ok+neg_ok, len(rows))
print(f"总体   95% Wilson 置信区间: [{lo2:.1%}, {hi2:.1%}]  (宽度 {(hi2-lo2):.1%})")
print(f"参考: 要把宽度压到 ±5% 约需 151 个正样本（当前 {len(pos)}）")

# --- 7. 失败用例的具体证据 ---
print("\n" + "=" * 68)
print(f"全部 {len(rows)-(pos_ok+neg_ok)} 个失败用例的具体证据")
print("=" * 68)
for r in rows:
    if r["primary"] == "none":
        if r["top"] is not None:
            print(f"\n[{r['id']}] 负样本被误触发 → {r['top']}")
            print(f"  输入: {next(c['input'] for c in cases if c['id']==r['id'])}")
    elif r["top"] != r["primary"]:
        c = next(c for c in cases if c["id"] == r["id"])
        print(f"\n[{r['id']}] 期望 {r['primary']} → 实际 {r['top']}")
        print(f"  输入: {c['input']}")
        sc = sorted(r["scores"].items(), key=lambda kv: -kv[1])[:4]
        print(f"  得分: " + "  ".join(f"{s.split('harness-')[1]}={v}" for s, v in sc if v > 0))
        print(f"  标签: {c.get('tags')}")
