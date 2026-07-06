#!/usr/bin/env python3
"""
Agent 提示词存在性校验：检查每个 skill 的 SKILL.md 中
是否包含 "## Agent 提示词" section。

替代 scripts/validate-agent-prompt-sync.sh
"""

import os
import sys
import re

ROOT_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
SKILLS_DIR = os.path.join(ROOT_DIR, "skills")

fail = 0
warn = 0
pass_count = 0
total = 0

print("== agent prompt presence check ==")
print()

for entry in sorted(os.listdir(SKILLS_DIR)):
    skill_dir = os.path.join(SKILLS_DIR, entry)
    if not os.path.isdir(skill_dir) or not entry.startswith("harness-"):
        continue
    total += 1
    skill_md = os.path.join(skill_dir, "SKILL.md")

    if not os.path.isfile(skill_md):
        print(f"[FAIL] {entry}: SKILL.md not found")
        fail += 1
        continue

    # Check for ## Agent 提示词 or ## Agent Prompt section
    found = False
    try:
        with open(skill_md, "r", encoding="utf-8") as f:
            for line in f:
                if re.match(r"^##\s+Agent\s+(Prompt|提示词)", line):
                    found = True
                    break
    except (OSError, UnicodeDecodeError):
        print(f"[FAIL] {entry}: Cannot read SKILL.md")
        fail += 1
        continue

    if found:
        print(f"[OK] {entry}: has '## Agent 提示词' section")
        pass_count += 1
    else:
        print(f"[WARN] {entry}: missing '## Agent 提示词' section")
        warn += 1

print()
print(f"summary: pass={pass_count}  warn={warn}  fail={fail}")

if fail > 0:
    print()
    print(f"Validation finished with {fail} failure(s).")
    sys.exit(1)

if warn > 0:
    print()
    print(f"Validation finished with {warn} warning(s).")
    print("  → 这些 skill 的 SKILL.md 中缺少 '## Agent 提示词' section，")
    print("    后续 PR 会逐个补充。当前不阻断 CI。")

print()
print("All agent prompt checks passed.")
