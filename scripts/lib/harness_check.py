"""
Shared utility library for harness script checking.

Provides:
- Path constants (ROOT_DIR, SKILLS_DIR)
- SkillChecker class: pass/fail/warn counters with JSON output
- run_shared_checks(): replicating scripts/skill-automated-check.sh behavior
- Frontmatter parsing and section lookup helpers
"""

import json
import os
import re
import sys

# --- Path constants ---

ROOT_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), "../.."))
SKILLS_DIR = os.path.join(ROOT_DIR, "skills")


def resolve_skill_path(skill_name):
    """Return the path to a skill directory given its name."""
    return os.path.join(SKILLS_DIR, skill_name)


def read_skill_md(skill_name):
    """Return the full path to a skill's SKILL.md."""
    return os.path.join(SKILLS_DIR, skill_name, "SKILL.md")


def read_file(path):
    """Read a file and return its lines. Returns empty list on error."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().splitlines()
    except (OSError, UnicodeDecodeError):
        return []


def read_frontmatter(file_path):
    """
    Parse the YAML frontmatter (--- ... ---) of a SKILL.md.
    Returns a dict with key-value pairs (no nested YAML parsing).
    Returns {} if no frontmatter found.
    """
    lines = read_file(file_path)
    if not lines or lines[0].strip() != "---":
        return {}
    result = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        m = re.match(r"^(\w[\w-]*?)\s*:\s*(.*)", line)
        if m:
            result[m.group(1)] = m.group(2).strip()
    return result


def has_section(file_path, section_name):
    """Check if the file has a ##-level section matching section_name."""
    for line in read_file(file_path):
        m = re.match(r"^##\s+(.+)$", line)
        if m and section_name in m.group(1):
            return True
    return False


def has_text(file_path, pattern):
    """Check if the file contains text matching the regex pattern."""
    for line in read_file(file_path):
        if re.search(pattern, line, re.IGNORECASE):
            return True
    return False


def count_text(file_path, pattern):
    """Count lines matching a regex pattern (case-insensitive)."""
    count = 0
    for line in read_file(file_path):
        if re.search(pattern, line, re.IGNORECASE):
            count += 1
    return count


def skill_dirs():
    """Yield (skill_name, skill_dir_path) for all harness-* skills."""
    if not os.path.isdir(SKILLS_DIR):
        return
    for entry in sorted(os.listdir(SKILLS_DIR)):
        d = os.path.join(SKILLS_DIR, entry)
        if os.path.isdir(d) and entry.startswith("harness-"):
            yield entry, d


def skill_md_files():
    """Yield (skill_name, skill_md_path) for all skills with SKILL.md."""
    for name, _ in skill_dirs():
        md = os.path.join(SKILLS_DIR, name, "SKILL.md")
        if os.path.isfile(md):
            yield name, md


# --- SkillChecker class ---

class SkillChecker:
    """
    Check counter with pass/fail/warn tracking and JSON output.
    Mirrors the check_pass/check_fail/check_warn pattern from the bash scripts.
    """

    def __init__(self, skill_name=""):
        self.skill_name = skill_name
        self.total = 0
        self.passed = 0
        self.failed = 0
        self.warning_count = 0
        self.issues = []      # {"check", "severity", "detail"}
        self.warnings = []    # {"check", "detail"}

    def check_pass(self, check_name=""):
        self.total += 1
        self.passed += 1

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
        """Calculate 0-10 score from pass/total ratio."""
        if self.total == 0:
            return 0.0
        return round(self.passed * 10 / self.total, 2)

    def to_dict(self):
        return {
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

    def to_json(self):
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

    def print_json(self):
        print(self.to_json())


# --- Shared checks (replicating scripts/skill-automated-check.sh) ---

def run_shared_checks(skills_dir, skill_name):
    """
    Perform the shared checks that scripts/skill-automated-check.sh does.
    Returns a SkillChecker instance with all shared checks recorded.
    """
    checker = SkillChecker(skill_name)
    file_path = os.path.join(skills_dir, skill_name, "SKILL.md")

    # Check file exists
    if not os.path.isfile(file_path):
        checker.check_fail("file-exists", "CRITICAL", f"SKILL.md not found for {skill_name}")
        return checker
    checker.check_pass("file-exists")

    fm = read_frontmatter(file_path)

    # Check frontmatter fields
    for field in ("name", "description", "when_to_use", "compatibility"):
        if field in fm:
            checker.check_pass(f"fm-{field}")
        else:
            checker.check_fail(f"fm-{field}", "HIGH", f"Missing {field}")

    # Check key sections
    for section in ("Core Principles", "When to Use", "Methodology", "Key Points"):
        if has_section(file_path, section):
            checker.check_pass(f"section-{section}")
        else:
            checker.check_warn(f"section-{section}", f"Missing {section}")

    # Check Agent prompt section
    if has_text(file_path, r"^##\s+Agent\s+(Prompt|提示词)"):
        checker.check_pass("agent-prompt")
    else:
        checker.check_warn("agent-prompt", "Missing Agent 提示词 section")

    # Check Last updated
    if has_text(file_path, r"Last [Uu]pdated"):
        checker.check_pass("last-updated")
    else:
        checker.check_warn("last-updated", "Missing last updated date")

    # Check Edge Cases
    if has_text(file_path, r"Edge Case"):
        checker.check_pass("edge-cases")
    else:
        checker.check_warn("edge-cases", "No edge cases section")

    return checker


# --- Reference check helpers ---

def check_reference_files(checker, skill_dir, ref_files):
    """Check existence of reference files. Returns number passed."""
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
    """Print extra checks summary line (matching old script format)."""
    print("---")
    print(f"Extra checks: {passed_extra}/{total_extra} passed")


if __name__ == "__main__":
    # Quick self-test
    print("SkillChecker library loaded OK")
    print(f"ROOT_DIR = {ROOT_DIR}")
    c = SkillChecker("test")
    c.check_pass("test-pass")
    c.check_warn("test-warn", "just a test")
    print(c.to_json())
