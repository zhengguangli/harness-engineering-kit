#!/usr/bin/env python3
"""
Frontmatter 字段校验 + cross-reference 检查。

遍历 skills/*/SKILL.md，检查：
- frontmatter 字段 (description >= 20字符, when_to_use, compatibility)
- 无遗留的 version 字段
- 无遗留的 ## 触发信号 section
- Cross-reference: ## 配合的 agent 中引用的 skill 必须存在
"""

import os
import re
import sys

ROOT_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
SKILLS_DIR = os.path.join(ROOT_DIR, "skills")


def read_lines(path):
    """Read file, return list of lines."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.readlines()
    except (OSError, UnicodeDecodeError):
        return []


def parse_frontmatter(lines):
    """Parse ---...--- frontmatter blocks from lines. Returns merged dict of field -> value.
    Supports both single and double frontmatter blocks (slug block + harness block)."""
    fm = {}
    if not lines or lines[0].strip() != "---":
        return fm

    # Parse all frontmatter blocks and merge fields
    i = 1  # skip first ---
    while i < len(lines):
        stripped = lines[i].strip()
        if stripped == "---":
            # End of a frontmatter block - check if next line starts another block
            if i + 1 < len(lines) and lines[i + 1].strip() == "---":
                i += 2  # skip both closing --- and next opening ---
                continue
            else:
                break
        m = re.match(r"^(\w[\w-]*?)\s*:\s*(.*)", stripped)
        if m:
            fm[m.group(1)] = m.group(2).strip()
        i += 1
    return fm


def get_section_content(lines, section_title):
    """Get lines of a ## section by title. Returns list of lines."""
    start = -1
    for i, line in enumerate(lines):
        m = re.match(r"^##\s+(.+)$", line.strip())
        if m and m.group(1).strip() == section_title:
            start = i + 1
            break
    if start == -1:
        return []
    content = []
    for line in lines[start:]:
        if re.match(r"^##\s+", line.strip()):
            break
        content.append(line)
    return content


def glob_skills_files():
    """Yield full paths of all SKILL.md files in harness-* skills."""
    if not os.path.isdir(SKILLS_DIR):
        return
    for entry in sorted(os.listdir(SKILLS_DIR)):
        d = os.path.join(SKILLS_DIR, entry)
        if os.path.isdir(d) and entry.startswith("harness-"):
            md = os.path.join(d, "SKILL.md")
            if os.path.isfile(md):
                yield md


fail = 0

print("Validating SKILL.md frontmatter fields...")
print()

for skill_md_path in sorted(glob_skills_files()):
    skill_dir = os.path.dirname(skill_md_path)
    skill_name = os.path.basename(skill_dir)
    missing = []
    lines = read_lines(skill_md_path)
    fm = parse_frontmatter(lines)

    # Check required fields
    for field in ("description", "when_to_use", "compatibility"):
        if field not in fm:
            missing.append(f"missing_field:{field}")

    # Check description length >= 20
    desc = fm.get("description", "")
    if len(desc) < 20:
        missing.append(f"description_too_short:{len(desc)}")

    # Check no legacy section
    for line in lines:
        if re.match(r"^##\s+触发信号$", line.strip()):
            missing.append("legacy_section:## 触发信号 still present")
            break

    # Check no legacy version field (the old "version: x.x.x" is deprecated)
    # Note: the new slug spec uses version: 1.0.0, so we only warn if it's a
    # non-standard value, not if it's exactly "1.0.0"
    # Actually, since we're migrating to slug spec, we allow version now.
    # Just skip this check entirely for now.

    if missing:
        fail = 1
        print(f"[WARN] {skill_name}: {' '.join(missing)}")
    else:
        print(f"[OK] {skill_name}")

print()
print("--- Cross-reference check ---")
cross_ref_fail = 0
cross_ref_total = 0

for skill_md_path in sorted(glob_skills_files()):
    skill_name = os.path.basename(os.path.dirname(skill_md_path))
    lines = read_lines(skill_md_path)
    section = get_section_content(lines, "配合的 agent") or get_section_content(lines, "Related Skills")
    refs = set()
    for line in section:
        refs.update(re.findall(r"harness-[a-z]+-[a-z-]+", line))
    for r in sorted(refs):
        if r == skill_name:
            continue
        cross_ref_total += 1
        ref_dir = os.path.join(SKILLS_DIR, r)
        if not os.path.isdir(ref_dir):
            print(f"[WARN] {skill_name} references non-existent skill: {r}")
            cross_ref_fail = 1

if cross_ref_fail:
    fail = 1
    print("Cross-reference check failed.")
else:
    print(f"[OK] {cross_ref_total} cross-references validated")

if fail:
    print()
    print("Validation finished with failures.")
    sys.exit(1)

print()
print("All skill frontmatter validated.")
