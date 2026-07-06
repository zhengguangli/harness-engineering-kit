#!/usr/bin/env python3
"""Automated check script for harness-authoring"""
import json, os, re, sys

def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except (OSError, UnicodeDecodeError):
        return ""

def read_lines(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.readlines()
    except (OSError, UnicodeDecodeError):
        return []

def has_text(text, pattern, flags=0):
    return bool(re.search(pattern, text, flags))

class SkillChecker:
    def __init__(self, skill_name=""):
        self.skill_name = skill_name
        self.total = self.passed = self.failed = self.warning_count = 0
        self.issues = []
        self.warnings = []
    def check_pass(self, check_name=""):
        self.total += 1; self.passed += 1
    def check_fail(self, check_name, severity="HIGH", detail=""):
        self.total += 1; self.failed += 1
        self.issues.append({"check": check_name, "severity": severity, "detail": detail})
    def check_warn(self, check_name, detail=""):
        self.total += 1; self.warning_count += 1
        self.warnings.append({"check": check_name, "detail": detail})
    @property
    def score(self):
        return round(self.passed * 10 / self.total, 2) if self.total else 0.0
    def print_json(self):
        d = {"skill_name": self.skill_name, "auto_check_score": self.score,
             "stats": {"total": self.total, "passed": self.passed, "failed": self.failed, "warnings": self.warning_count},
             "issues": self.issues, "warnings": self.warnings}
        print(json.dumps(d, ensure_ascii=False, indent=2))

def run_shared_checks(skills_dir, skill_name):
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
            if s == "---": break
            m = re.match(r"^(\w[\w-]*?)\s*:\s*(.*)", s)
            if m: fm[m.group(1)] = m.group(2).strip()
    for field in ("name", "description", "when_to_use", "compatibility"):
        if field in fm: checker.check_pass(f"fm-{field}")
        else: checker.check_fail(f"fm-{field}", "HIGH", f"Missing {field}")
    for section in ("Core Principles", "When to Use", "Methodology", "Key Points"):
        if has_text(content, rf"^##\s+{re.escape(section)}", re.MULTILINE): checker.check_pass(f"section-{section}")
        else: checker.check_warn(f"section-{section}", f"Missing {section}")
    if has_text(content, r"^##\s+Agent\s+(Prompt|提示词)", re.MULTILINE): checker.check_pass("agent-prompt")
    else: checker.check_warn("agent-prompt", "Missing Agent 提示词 section")
    if has_text(content, r"Last [Uu]pdated"): checker.check_pass("last-updated")
    else: checker.check_warn("last-updated", "Missing last updated date")
    if has_text(content, r"Edge Case", re.IGNORECASE): checker.check_pass("edge-cases")
    else: checker.check_warn("edge-cases", "No edge cases section")
    return checker

def check_reference_files(checker, skill_dir, ref_files):
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

# Path resolution
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, ".."))
ROOT_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, "../../.."))
SKILLS_DIR = os.path.join(ROOT_DIR, "skills")
SKILL_NAME = os.path.basename(SKILL_DIR)

checker = run_shared_checks(SKILLS_DIR, SKILL_NAME)
checker.print_json()

passed_extra, total_extra = check_reference_files(checker, SKILL_DIR,
    ["scaffold-templates.md", "skill-design-patterns.md", "subagent-design-patterns.md",
     "context-budget-management-guide.md"])

# Skill-specific content checks
content = read_file(os.path.join(SKILL_DIR, "SKILL.md"))
for pattern, label in [
    (r"Context Budget Discipline", "Context Budget Discipline section"),
    (r"canonical", "canonical version convention"),
    (r"Skill.*Subagent", "Skill vs Subagent comparison table"),
    (r"Permission Discipline", "Permission Discipline principle"),
    (r"Combating Context Rot", "Combating Context Rot methodology section"),
    (r"Steps to Add", "Steps to Add New Capability checklist"),
]:
    total_extra += 1
    if has_text(content, pattern, re.IGNORECASE | re.MULTILINE):
        passed_extra += 1; checker.check_pass(label)
    else:
        print(f"  [FAIL] Missing {label}")

print_extra_summary(checker, passed_extra, total_extra)
