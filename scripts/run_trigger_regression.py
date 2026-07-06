#!/usr/bin/env python3
"""
Trigger keyword regression test.

Reads tests/triggers/cases.json, matches each input against keyword mappings,
and reports PASS/WARN/FAIL.

Usage:
    python3 scripts/run-all.py --run-type regression
    python3 scripts/run-all.py --run-type regression --json
"""

import json
import os
import sys

ROOT_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
CASES_FILE = os.path.join(ROOT_DIR, "tests/triggers/cases.json")
REPORT_FILE = os.path.join(ROOT_DIR, "tests/triggers/report.json")


# Keyword mappings (replicating SKILL_KW associative array from bash)
SKILL_KW = {
    "harness-architecture-boundaries": "分层架构 循环依赖 层间越界 lint 规则 依赖方向 架构腐化",
    "harness-authoring": "怎么写一个好的 SKILL.md 给 harness 添新能力 skill 还是 subagent 瘦身",
    "harness-bootstrap": "init harness 为这个项目初始化 harness CLAUDE.md docs/ 骨架 CI 模板",
    "harness-commit-gate": "提交代码 commit git commit 修复，提交代码 代码提交",
    "harness-exec-plans": "先做个计划 改动比较大 落盘 跨多个会话 跨多窗口 接力 上一轮试过什么",
    "harness-golden-principles": "周期性扫描 模式漂移 黄金原则 品味编码 重复模式",
    "harness-observability-and-browser": "复现 UI bug P99 截图 浏览器 验证",
    "harness-orchestration": "我该用哪些 skill 多 skill 协作 不确定先后顺序 不确定先做什么后做什么 路由",
    "harness-project-intake": "分析当前项目 项目概览 README 这个项目是做什么的 项目卡片",
    "harness-prompt-optimizer": "优化这个 prompt prompt 效果不好 system prompt",
    "harness-repo-map": "CLAUDE.md 瘦身 断链 过期 从零搭建 docs 渐进式披露",
    "harness-verification-loop": "可合并 自验证循环 测试失败 循环迭代 实现→自检→测试→评审→修复 迭代",
    "harness-skill-quality-assessor": "评估skill质量 skills质量审计 优化skills skill质量怎么样 检查skills规范",
}


def match_count(skill, text):
    """Count how many keywords from SKILL_KW[skill] appear in text."""
    kw = SKILL_KW.get(skill, "")
    if not kw:
        return 0
    count = 0
    for word in kw.split():
        if word in text:
            count += 1
    return count


def process_case(case, json_mode):
    """Process a single test case. Returns (result, reason, matched_candidates)."""
    case_id = case["id"]
    input_text = case["input"]
    primary = case["expected_primary_skill"]
    candidates = case.get("expected_candidates", [])

    primary_count = match_count(primary, input_text)
    best_skill = primary
    best_count = primary_count
    matched_candidates = []

    for c in candidates:
        c_count = match_count(c, input_text)
        if c_count > 0:
            matched_candidates.append(c)
            if c_count > best_count:
                best_count = c_count
                best_skill = c

    reason = ""
    if primary == "none":
        # Negative test case: passes if no candidates matched
        if not matched_candidates:
            result = "PASS"
            reason = "negative case: no skill matched as expected"
        else:
            result = "FAIL"
            reason = f"negative case: unexpected match on {' '.join(matched_candidates)}"
    elif primary_count > 0:
        if best_skill == primary:
            result = "PASS"
            reason = "primary matched with strongest signal"
        else:
            result = "WARN"
            reason = "primary matched but not strongest signal"
    else:
        result = "FAIL"
        reason = "primary not matched"

    print(f"[{result}] {case_id} -> {primary} ({reason})")

    return result, reason, " ".join(matched_candidates)


def main():
    json_mode = "--json" in sys.argv
    if json_mode:
        os.makedirs(os.path.dirname(REPORT_FILE), exist_ok=True)

    if not os.path.isfile(CASES_FILE):
        print(f"cases file not found: {CASES_FILE}")
        sys.exit(2)

    with open(CASES_FILE, "r", encoding="utf-8") as f:
        cases = json.load(f)

    pass_count = 0
    warn_count = 0
    fail_count = 0
    json_items = []

    for case in cases:
        result, reason, matched = process_case(case, json_mode)
        if result == "PASS":
            pass_count += 1
        elif result == "WARN":
            warn_count += 1
        else:
            fail_count += 1

        if json_mode:
            json_items.append({
                "id": case["id"],
                "input": case["input"],
                "primary": case["expected_primary_skill"],
                "result": result,
                "reason": reason,
                "matched_candidates": matched,
            })

    print(f"\nSummary: PASS={pass_count} WARN={warn_count} FAIL={fail_count}")

    if json_mode:
        with open(REPORT_FILE, "w", encoding="utf-8") as f:
            json.dump(json_items, f, ensure_ascii=False, indent=2)
        print(f"Report written to {REPORT_FILE}")

    if fail_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
