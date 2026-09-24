"""
Shared checker library for skill-level automated checks.

This module is the single implementation behind every
`skills/*/references/automated_check_script.py`. Before it existed, all 13
scripts carried their own ~110-line copy of the boilerplate below; the copies
had already drifted (several counted Hard Constraints with a bullet-only regex
that broke once the sections were normalised to numbered lists).

Each skill's script now imports this module and contributes only its own
checks. Behaviour is identical to the old inline copies.

Usage from a skill script:

    import os, sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../scripts"))
    from lib.harness_check import (read_file, has_text, SkillChecker,
                                   run_shared_checks, check_reference_files,
                                   print_extra_summary)
"""

import json
import os
import re

# --- Path constants ---

ROOT_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), "../.."))
SKILLS_DIR = os.path.join(ROOT_DIR, "skills")


# --- File helpers (signatures match the former inline copies) ---

def read_file(path):
    """Read a file and return its full text. Returns '' on error."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except (OSError, UnicodeDecodeError):
        return ""


def read_lines(path):
    """Read a file as a list of lines. Returns [] on error."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.readlines()
    except (OSError, UnicodeDecodeError):
        return []


def has_text(text, pattern, flags=0):
    """True if `text` (a string, not a path) matches `pattern`."""
    return bool(re.search(pattern, text, flags))


# --- SkillChecker ---

class SkillChecker:
    """Pass/fail/warn counter with JSON output."""

    def __init__(self, skill_name=""):
        self.skill_name = skill_name
        self.total = self.passed = self.failed = self.warning_count = 0
        self.issues = []      # [{"check", "severity", "detail"}]
        self.warnings = []    # [{"check", "detail"}]
        self.passed_items = []

    def check_pass(self, check_name=""):
        self.total += 1
        self.passed += 1
        self.passed_items.append(check_name)

    def check_fail(self, check_name, severity="HIGH", detail=""):
        self.total += 1
        self.failed += 1
        self.issues.append({"check": check_name, "severity": severity, "detail": detail})

    def check_warn(self, check_name, detail=""):
        self.total += 1
        self.warning_count += 1
        self.warnings.append({"check": check_name, "detail": detail})

    @property
    def score(self):
        return round(self.passed * 10 / self.total, 2) if self.total else 0.0

    def print_json(self):
        d = {
            "skill_name": self.skill_name,
            "auto_check_score": self.score,
            "stats": {
                "total": self.total,
                "passed": self.passed,
                "failed": self.failed,
                "warnings": self.warning_count,
            },
            "issues": self.issues,
            "warnings": self.warnings,
        }
        print(json.dumps(d, ensure_ascii=False, indent=2))

    def exit_code(self):
        """Non-zero when any check failed, so CI can actually gate on it."""
        return 1 if self.failed else 0


# --- Shared checks (identical for every skill) ---

def run_shared_checks(skills_dir, skill_name):
    """Run the checks common to all skills. Returns a SkillChecker."""
    checker = SkillChecker(skill_name)
    file_path = os.path.join(skills_dir, skill_name, "SKILL.md")

    if not os.path.isfile(file_path):
        checker.check_fail("file-exists", "CRITICAL", f"SKILL.md not found for {skill_name}")
        return checker
    checker.check_pass("file-exists")

    content = read_file(file_path)
    fm = {}
    lines = read_lines(file_path)
    if lines and lines[0].strip() == "---":
        for line in lines[1:]:
            s = line.strip()
            if s == "---":
                break
            m = re.match(r"^(\w[\w-]*?)\s*:\s*(.*)", s)
            if m:
                fm[m.group(1)] = m.group(2).strip()

    for field in ("name", "description", "when_to_use", "compatibility"):
        if field in fm:
            checker.check_pass(f"fm-{field}")
        else:
            checker.check_fail(f"fm-{field}", "HIGH", f"Missing {field}")

    for section in ("Core Principles", "When to Use", "Methodology", "Key Points"):
        if has_text(content, rf"^##\s+{re.escape(section)}", re.MULTILINE):
            checker.check_pass(f"section-{section}")
        else:
            checker.check_warn(f"section-{section}", f"Missing {section}")

    if has_text(content, r"^##\s+Agent\s+(Prompt|提示词)", re.MULTILINE):
        checker.check_pass("agent-prompt")
    else:
        checker.check_warn("agent-prompt", "Missing Agent 提示词 section")

    if has_text(content, r"Last [Uu]pdated"):
        checker.check_pass("last-updated")
    else:
        checker.check_warn("last-updated", "Missing last updated date")

    if has_text(content, r"Edge Case", re.IGNORECASE):
        checker.check_pass("edge-cases")
    else:
        checker.check_warn("edge-cases", "No edge cases section")

    return checker


# --- Reference-file helpers ---

def check_reference_files(checker, skill_dir, ref_files):
    """Check that each listed reference file exists. Returns (passed, total)."""
    passed_extra = 0
    total_extra = 0
    for ref in ref_files:
        total_extra += 1
        path = os.path.join(skill_dir, "references", ref)
        if os.path.isfile(path):
            checker.check_pass(f"ref-{ref}")
            passed_extra += 1
        else:
            checker.check_fail(f"ref-{ref}", "HIGH", f"Missing reference: {ref}")
    return passed_extra, total_extra


def print_extra_summary(checker, passed_extra, total_extra):
    print("---")
    print(f"Extra checks: {passed_extra}/{total_extra} passed")


# --- Counting helpers used by skill-specific checks ---

def count_hard_constraints(content):
    """Count Hard Constraints entries.

    Accepts both the numbered form ('1. **Rule**: ...') and the legacy bullet
    form ('- **Rule**: ...'). Several skills' checks used a bullet-only regex
    and silently reported 0 after the sections were normalised to numbered
    lists.
    """
    m = re.search(r"^##\s+Hard Constraints\s*$(.*?)(?=^##\s|\Z)",
                  content, re.MULTILINE | re.DOTALL)
    if not m:
        return 0
    return len(re.findall(r"^\s*(?:\d+\.|-)\s+\*\*", m.group(1), re.MULTILINE))


def count_agent_constraints(content):
    """Count entries in the '### Constraints' sub-section of the agent prompt.

    The agent block is '## Agent 提示词' followed by a '## <agent-name> (<Role>)'
    heading at the SAME level, so the block cannot be bounded by '## ' alone.
    Locate the agent prompt, then find '### Constraints' after it.
    """
    m = re.search(r"^##\s+Agent\s+(?:Prompt|提示词)\s*$", content, re.MULTILINE)
    if not m:
        return 0
    tail = content[m.end():]
    c = re.search(r"^###\s+Constraints\s*$(.*?)(?=^###\s|^##\s|\Z)",
                  tail, re.MULTILINE | re.DOTALL)
    if not c:
        return 0
    return len(re.findall(r"^\s*(?:\d+\.|-)\s+\*\*", c.group(1), re.MULTILINE))
