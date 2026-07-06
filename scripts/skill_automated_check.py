#!/usr/bin/env python3
"""
Shared SKILL.md automated checker.

Usage: python3 scripts/skill_automated_check.py <skills_dir> <skill_name>

Outputs JSON with check results, matching the schema of skill-automated-check.sh.

替代 scripts/skill-automated-check.sh
"""

import json
import os
import re
import sys

# Add scripts/lib to path
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), ".")))


def read_lines(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.readlines()
    except (OSError, UnicodeDecodeError):
        return []


def parse_frontmatter(lines):
    fm = {}
    if not lines or lines[0].strip() != "---":
        return fm
    for line in lines[1:]:
        stripped = line.strip()
        if stripped == "---":
            break
        m = re.match(r"^(\w[\w-]*?)\s*:\s*(.*)", stripped)
        if m:
            fm[m.group(1)] = m.group(2).strip()
    return fm


def has_section(lines, section_name):
    for line in lines:
        m = re.match(r"^##\s+(.+)$", line.strip())
        if m and section_name in m.group(1):
            return True
    return False


def has_text(lines, pattern):
    for line in lines:
        if re.search(pattern, line, re.IGNORECASE):
            return True
    return False


class SimpleChecker:
    """Lightweight checker for shared use — no external dependencies."""

    def __init__(self, skill_name=""):
        self.skill_name = skill_name
        self.total = 0
        self.passed = 0
        self.failed = 0
        self.warnings = 0
        self.issues = []
        self.warning_items = []

    def check_pass(self, check_name=""):
        self.total += 1
        self.passed += 1

    def check_fail(self, check_name, severity="HIGH", detail=""):
        self.total += 1
        self.failed += 1
        self.issues.append({"check": check_name, "severity": severity, "detail": detail})

    def check_warn(self, check_name, detail=""):
        self.total += 1
        self.warnings += 1
        self.warning_items.append({"check": check_name, "detail": detail})

    def to_dict(self):
        score = round(self.passed * 10 / self.total, 2) if self.total > 0 else 0
        return {
            "skill_name": self.skill_name,
            "auto_check_score": score,
            "stats": {
                "total": self.total,
                "passed": self.passed,
                "failed": self.failed,
                "warnings": self.warnings,
            },
            "issues": self.issues,
            "warnings": self.warning_items,
        }


def main():
    if len(sys.argv) < 3:
        print(json.dumps({"error": "Usage: python3 skill_automated_check.py <skills_dir> <skill_name>"}))
        sys.exit(1)

    skills_dir = sys.argv[1]
    skill_name = sys.argv[2]
    file_path = os.path.join(skills_dir, skill_name, "SKILL.md")

    checker = SimpleChecker(skill_name)

    # Check file exists
    if not os.path.isfile(file_path):
        print(json.dumps({"error": f"SKILL.md not found for {skill_name}"}, ensure_ascii=False))
        sys.exit(1)
    checker.check_pass("file-exists")

    lines = read_lines(file_path)
    fm = parse_frontmatter(lines)

    # Check frontmatter fields
    for field in ("name", "description", "when_to_use", "compatibility"):
        if field in fm:
            checker.check_pass(f"fm-{field}")
        else:
            checker.check_fail(f"fm-{field}", "HIGH", f"Missing {field}")

    # Check key sections
    for section in ("Core Principles", "When to Use", "Methodology", "Key Points"):
        if has_section(lines, section):
            checker.check_pass(f"section-{section}")
        else:
            checker.check_warn(f"section-{section}", f"Missing {section}")

    # Check Agent prompt
    if has_text(lines, r"^##\s+Agent\s+(Prompt|提示词)"):
        checker.check_pass("agent-prompt")
    else:
        checker.check_warn("agent-prompt", "Missing Agent 提示词 section")

    # Check last updated
    if has_text(lines, r"Last [Uu]pdated"):
        checker.check_pass("last-updated")
    else:
        checker.check_warn("last-updated", "Missing last updated date")

    # Check edge cases
    if has_text(lines, r"Edge Case"):
        checker.check_pass("edge-cases")
    else:
        checker.check_warn("edge-cases", "No edge cases section")

    # Output JSON
    result = checker.to_dict()
    # Ensure issue/warning details use empty string not None
    for issue in result["issues"]:
        issue.setdefault("detail", "")
    for warn_item in result["warnings"]:
        warn_item.setdefault("detail", "")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
