#!/usr/bin/env python3
"""
Task-set coverage audit.

For every task in tests/tasks/tasks.json, check that the owning skill's
SKILL.md actually specifies how to satisfy each acceptance criterion. This is
specification conformance testing: it finds skills whose instructions cannot
produce the outcome they promise.

It does NOT run the skill, so it cannot measure whether the skill works — only
whether the spec is complete enough to be testable at all.

Usage:
    python3 scripts/audit_task_coverage.py
"""
import json
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
TASKS = os.path.join(ROOT, "tests", "tasks", "tasks.json")
SKILLS_DIR = os.path.join(ROOT, "skills")

# Criterion keyword -> what the spec must mention for it to be actionable.
# Deliberately coarse: this catches "the spec never mentions this at all",
# not subtle wording problems.
REQUIRES = {
    "report title":            r"title|标题",
    "file path":               r"file path|路径",
    "line number":             r"line number|行号|line",
    "violated rule":           r"violated rule|Rule Violated|违反.*规则",
    "impact":                  r"impact|影响",
    "suggested fix":           r"suggested fix|fix suggestion|修复建议|建议",
    "grouped by severity":     r"severity|严重程度|CRITICAL",
    "no file is modified":     r"read-only|read only|不修改|never modify|strictly read",
    "i have fixed this":       r"I have fixed|已修复",
    "manifest":                r"manifest|清单",
    "structural architecture violations": r"structural.*boundary-auditor|boundary-auditor",
    "100 lines":               r"100|≤\s*100",
    "last updated":            r"last updated|最后更新",
    "project type":            r"project type|project scale|项目类型",
    "business code":           r"business code|业务代码",
    "72 characters":           r"72",
    "diff is reviewed":        r"diff|review",
    "tests/build":             r"test|build|lint",
    "commit is blocked":       r"block|abort|reject|拒绝",
    "template":                r"template|模板",
    "mechanically verifiable": r"mechanically verifiable|mechanically checkable|可机械|可自动",
    "one PR":                  r"one PR|单个 PR|single PR",
    "decision log":            r"decision log|决策日志",
    "implementation code":     r"implementation detail|implementation code|实现细节|pre-write|预先写",
    "risk level":              r"risk level|risk|风险",
    "before/after":            r"before|after|前后",
    "timestamp":               r"timestamp|时间戳",
    "URL":                     r"URL|url",
    "execution order":         r"execution order|执行顺序|顺序",
    "workflow":                r"workflow|工作流",
    "skipped":                 r"skip|跳过|省略",
    "5 dimensions":            r"5-dimension|dimension|维度",
    "fabricated":              r"fabricat|编造|猜测",
    "intermediate":            r"intermediate|中间.*输出|silent",
    "severity":                r"severity|严重程度",
    "repair suggestion":       r"repair|修复|建议",
    "pass/fail":               r"pass|fail|PASS|FAIL",
    "iteration log":           r"iteration|迭代",
    "stuck":                   r"stuck|卡住",
    "8-round":                 r"8|maximum iteration|最大迭代",
    "escalate":                r"escalat|升级|human|人工",
    "no report file is persisted":  r"not persisted|conversation only|conversation-only",
    "no standalone evidence file":  r"not as standalone|conversation",
    "no file is created":           r"no file is created|conversation output only|conversation only",
    "no project card file":         r"do not create a project card file|conversation-only",
    "findings ordered":             r"ordered by severity|HIGH.*MEDIUM.*LOW",
    "unrelated changes are not mixed": r"do not mix unrelated|independent.*suggestion|split into independent",
}


def skill_text(skill):
    return open(os.path.join(SKILLS_DIR, skill, "SKILL.md"), encoding="utf-8").read()


def main():
    tasks = json.load(open(TASKS, encoding="utf-8"))
    gaps = []
    checked = 0
    for t in tasks:
        skill = t["skill"]
        txt = skill_text(skill)
        for crit in t["acceptance_criteria"]:
            checked += 1
            matched = False
            for key, pat in REQUIRES.items():
                if key.lower() in crit.lower() and re.search(pat, txt, re.I):
                    matched = True
                    break
            # No fuzzy fallback. An earlier version accepted a criterion when
            # >=50% of its 4+ letter words appeared anywhere in SKILL.md; that
            # let "a quantum checksum of the diff must be computed before
            # commit" pass on the strength of 'diff'/'commit'/'before'. A
            # checker that accepts nonsense is worse than no checker.
            if not matched:
                gaps.append((t["id"], skill, crit))

    print("== task coverage audit ==")
    print()
    print(f"tasks: {len(tasks)}   acceptance criteria checked: {checked}   "
          f"unbacked: {len(gaps)}")
    if gaps:
        print()
        for tid, skill, crit in gaps:
            print(f"  [{tid}] {skill}")
            print(f"      criterion: {crit}")
            print(f"      -> SKILL.md does not specify how to satisfy this")
    return 1 if gaps else 0


if __name__ == "__main__":
    sys.exit(main())
