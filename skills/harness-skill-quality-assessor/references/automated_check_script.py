#!/usr/bin/env python3
"""
Skills quality assessment — automated check script (v2.0 weighted scoring edition)

Usage: python3 automated_check_script.py [skill-name|all]

Output: JSON-formatted check results with weighted scores.

替代 automated-check-script.sh (536 lines → Python)
"""

import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone

# Path resolution
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, ".."))
ROOT_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, "../../.."))
SKILLS_DIR = os.environ.get("SKILLS_DIR", os.path.join(ROOT_DIR, "skills"))


def read_file(path):
    """Read file contents; returns empty string on error."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except (OSError, UnicodeDecodeError):
        return ""


def read_lines(path):
    """Read file as lines; returns [] on error."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.readlines()
    except (OSError, UnicodeDecodeError):
        return []


def read_frontmatter(file_path):
    """Parse YAML frontmatter (--- ... ---) into dict."""
    lines = read_lines(file_path)
    if not lines or lines[0].strip() != "---":
        return {}
    result = {}
    for line in lines[1:]:
        stripped = line.strip()
        if stripped == "---":
            break
        m = re.match(r"^(\w[\w-]*?)\s*:\s*(.*)", stripped)
        if m:
            result[m.group(1)] = m.group(2).strip()
    return result


def get_encoding(file_path):
    """Detect file encoding using `file` command (cross-platform)."""
    import subprocess
    try:
        result = subprocess.run(
            ["file", "-b", "--mime-encoding", file_path],
            capture_output=True, text=True, timeout=5
        )
        enc = result.stdout.strip()
        return enc if enc else "unknown"
    except Exception:
        return "unknown"


# --- Weighted scoring checker ---

class WeightedSkillChecker:
    """
    Weighted scoring checker with severity levels.
    CRITICAL=5, HIGH=3, MEDIUM=2, LOW=1, WARN=0 penalty.
    """

    WEIGHT_MAP = {"CRITICAL": 5, "HIGH": 3, "MEDIUM": 2, "LOW": 1, "WARN": 0}

    def __init__(self, skill_name=""):
        self.skill_name = skill_name
        self.total = 0
        self.passed = 0
        self.failed = 0
        self.warning_count = 0
        self.penalty_score = 0  # weighted penalty sum
        self.issues = []
        self.warning_items = []

    def check_pass(self, check_name=""):
        self.total += 1
        self.passed += 1
        self.penalty_score += 1

    def check_fail(self, check_name, severity="HIGH", detail=""):
        self.total += 1
        self.failed += 1
        penalty = self.WEIGHT_MAP.get(severity, 1)
        self.penalty_score = max(0, self.penalty_score - penalty)
        self.issues.append({"check": check_name, "severity": severity, "detail": detail})

    def check_warn(self, check_name, detail=""):
        self.total += 1
        self.warning_count += 1
        self.warning_items.append({"check": check_name, "detail": detail})

    @property
    def weighted_score(self):
        """Map penalty_score to 0-10 scale."""
        if self.total == 0:
            return 0.0
        score = round(self.penalty_score * 10 / self.total, 2)
        return max(0.0, min(10.0, score))

    @property
    def grade(self):
        ws = self.weighted_score
        if ws >= 9.5:
            return "A+"
        elif ws >= 9.0:
            return "A"
        elif ws >= 8.5:
            return "B+"
        elif ws >= 8.0:
            return "B"
        elif ws >= 7.0:
            return "C"
        elif ws >= 6.0:
            return "D"
        else:
            return "F"

    def to_dict(self):
        return {
            "skill_name": self.skill_name,
            "auto_check_score": self.weighted_score,
            "weighted_score": self.weighted_score,
            "grade": self.grade,
            "scoring_model": "weighted (CRITICAL=5, HIGH=3, MEDIUM=2, LOW=1, WARN=0)",
            "stats": {
                "total_checks": self.total,
                "passed": self.passed,
                "failed": self.failed,
                "warnings": self.warning_count,
                "penalty_score": self.penalty_score,
            },
            "issues": self.issues,
            "warnings": self.warning_items,
        }


# --- Check helper functions ---

def check_file_exists(c, file_path):
    if os.path.isfile(file_path):
        c.check_pass("file-exists")
        return True
    else:
        c.check_fail("File exists", "CRITICAL", f"SKILL.md does not exist: {file_path}")
        return False


def check_file_readable(c, file_path):
    if os.access(file_path, os.R_OK):
        c.check_pass("file-readable")
    else:
        c.check_fail("File readable", "CRITICAL", "File is not readable")


def check_file_encoding(c, file_path):
    enc = get_encoding(file_path)
    if enc in ("utf-8", "ascii", "us-ascii"):
        c.check_pass("file-encoding")
    else:
        c.check_warn("File encoding", f"Encoding is {enc}, UTF-8 recommended")


def check_fm_field(c, file_path, field, required=True):
    fm = read_frontmatter(file_path)
    if field in fm:
        c.check_pass(f"frontmatter-{field}")
    else:
        if required:
            c.check_fail(f"frontmatter-{field}", "HIGH", f"Missing required field: {field}")
        else:
            c.check_warn(f"frontmatter-{field}", f"Missing optional field: {field}")


def check_fm_description_length(c, file_path):
    fm = read_frontmatter(file_path)
    desc = fm.get("description", "")
    if len(desc) >= 20:
        c.check_pass("frontmatter-description-length")
    else:
        c.check_fail("frontmatter-description-length", "HIGH",
                     f"Description length {len(desc)} < 20")


def check_fm_no_version(c, file_path):
    fm = read_frontmatter(file_path)
    if "version" in fm:
        c.check_fail("frontmatter-no-version", "MEDIUM",
                     "Contains deprecated version field")
    else:
        c.check_pass("frontmatter-no-version")


def check_fm_metadata(c, file_path):
    fm = read_frontmatter(file_path)
    if "metadata" in fm:
        c.check_pass("frontmatter-metadata")
    else:
        c.check_warn("frontmatter-metadata", "Missing metadata field (recommended)")


def check_fm_context(c, file_path):
    fm = read_frontmatter(file_path)
    ctx = fm.get("context", "")
    if ctx:
        c.check_pass("frontmatter-context")
        if ctx not in ("fork", "merge", "edit"):
            c.check_warn("frontmatter-context-value",
                         f"Context value is '{ctx}', not a standard value (fork/merge/edit)")
    else:
        c.check_warn("frontmatter-context", "Missing context field (recommended)")


def check_fm_allowed_tools(c, file_path):
    fm = read_frontmatter(file_path)
    at = fm.get("allowed-tools", "")
    if at:
        c.check_pass("frontmatter-allowed-tools")
        if len(at) < 20:
            c.check_warn("frontmatter-allowed-tools-value",
                         f"allowed-tools declaration too short ({len(at)} chars), may be empty")
    else:
        c.check_warn("frontmatter-allowed-tools",
                     "Missing allowed-tools field (violates least privilege principle)")


def check_fm_allowed_tools_syntax(c, file_path):
    fm = read_frontmatter(file_path)
    at = fm.get("allowed-tools", "")
    if not at:
        c.check_warn("allowed-tools-syntax", "No allowed-tools content to validate")
        return
    # Validate format: Tool(cmd1 cmd2) Tool2(cmd3) ...
    if re.match(r"^[A-Za-z_]+\([^)]*\)(\s+[A-Za-z_]+\([^)]*\))*$", at):
        c.check_pass("allowed-tools-syntax")
    else:
        c.check_fail("allowed-tools-syntax", "MEDIUM",
                     f"allowed-tools format invalid (expected: Tool(cmd1 cmd2)): {at}")


def check_fm_agent_prompt_consistency(c, file_path):
    fm = read_frontmatter(file_path)
    contents = read_file(file_path)
    agent_name = fm.get("agent", "")
    prompt_section_match = re.search(r"^##\s+(?:Agent Prompt|Agent 提示词)", contents, re.MULTILINE)
    if agent_name and prompt_section_match:
        # Check if agent name appears in prompt section
        if re.search(rf"^\s*###\s+{re.escape(agent_name)}", contents, re.MULTILINE) or \
           agent_name.lower() in prompt_section_match.group():
            c.check_pass("agent-prompt-consistency")
        else:
            c.check_warn("agent-prompt-consistency",
                         f"Agent field value '{agent_name}' does not appear in/after Agent Prompt section")
    else:
        c.check_warn("agent-prompt-consistency",
                     "Cannot verify consistency (missing agent field or Agent Prompt section)")


def check_fm_metadata_category(c, file_path):
    contents = read_file(file_path)
    if re.search(r"category:", contents):
        c.check_pass("frontmatter-category")
    else:
        c.check_warn("frontmatter-category", "Missing metadata.category field")


def check_section(c, file_path, name, required=True):
    contents = read_file(file_path)
    if re.search(rf"^##\s+{re.escape(name)}", contents, re.MULTILINE):
        c.check_pass(f"section-{name}")
    else:
        if required:
            c.check_fail(f"section-{name}", "HIGH", f"Missing required section: {name}")
        else:
            c.check_warn(f"section-{name}", f"Missing optional section: {name}")


def check_hard_constraints_section(c, file_path):
    contents = read_file(file_path)
    m = re.search(r"^##\s+Hard\s*Constraints", contents, re.MULTILINE)
    if m:
        c.check_pass("section-hard-constraints")
        after = contents[m.end():]
        next_section = re.search(r"\n##\s+", after)
        section_body = after[:next_section.start()] if next_section else after
        count = len(re.findall(r"^\s*(?:\d+\.|[-*])", section_body, re.MULTILINE))
        if count >= 2:
            c.check_pass("hard-constraints-count")
        else:
            c.check_warn("hard-constraints-count", f"Hard constraints count {count} < 2")
    else:
        c.check_warn("section-hard-constraints",
                     "Missing Hard Constraints section (recommended)")


def check_agent_prompt(c, file_path):
    contents = read_file(file_path)
    if re.search(r"^##\s+(?:Agent Prompt|Agent 提示词)", contents, re.MULTILINE):
        c.check_pass("agent-prompt")
        subs = ["Skip Conditions", "Role Definition", "Core Capabilities",
                "Execution Flow", "Constraints", "Output Specification"]
        for s in subs:
            if re.search(rf"^\s*###\s+{re.escape(s)}", contents, re.MULTILINE):
                c.check_pass(f"agent-prompt-{s}")
            else:
                c.check_warn(f"agent-prompt-{s}",
                             f"Missing Agent Prompt subsection: {s}")
    else:
        c.check_fail("agent-prompt", "HIGH", "Missing required Agent Prompt section")


def check_last_updated_freshness(c, file_path):
    contents = read_file(file_path)
    m = re.search(r"Last updated[:\s]+(\d{4}-\d{2}-\d{2})", contents)
    if m:
        last_date_str = m.group(1)
        try:
            last_date = datetime.strptime(last_date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
            now = datetime.now(timezone.utc)
            diff_days = (now - last_date).days
            if diff_days <= 90:
                c.check_pass("content-freshness")
            else:
                c.check_fail("content-freshness", "LOW",
                             f"Last updated {diff_days} days ago, exceeds 90-day threshold")
        except ValueError:
            c.check_warn("content-last-updated", "Invalid date format in last updated")
    else:
        c.check_warn("content-last-updated", "Missing last updated date")


def check_content_examples(c, file_path):
    contents = read_file(file_path)
    count = len(re.findall(r"(?:example|use\s*case)", contents, re.IGNORECASE))
    if count >= 3:
        c.check_pass("content-examples")
    elif count >= 1:
        c.check_warn("content-examples",
                     f"Only {count} example references (recommend >=3)")
    else:
        c.check_fail("content-examples", "MEDIUM", "Missing usage examples")


def check_content_error_handling(c, file_path):
    contents = read_file(file_path)
    if re.search(r"error.handling|troubleshooting|FAQ|edge\s*case", contents, re.IGNORECASE):
        c.check_pass("content-error-handling")
    else:
        c.check_warn("content-error-handling", "Missing error handling guidance")


def check_content_best_practices(c, file_path):
    contents = read_file(file_path)
    if re.search(r"best.?practice", contents, re.IGNORECASE):
        c.check_pass("content-best-practices")
    else:
        c.check_warn("content-best-practices", "Missing best practices section")


def check_cross_skill_handoff(c, file_path):
    contents = read_file(file_path)
    count = len(re.findall(r"handoff|upstream|downstream|dependency", contents, re.IGNORECASE))
    if count >= 1:
        c.check_pass("cross-skill-handoff")
    else:
        c.check_warn("cross-skill-handoff", "No cross-skill handoff points mentioned")


def check_common_edge_cases(c, file_path):
    ref_file = os.path.join(os.path.dirname(file_path), "references", "common-edge-cases.md")
    if os.path.isfile(ref_file):
        c.check_pass("common-edge-cases")
    else:
        c.check_warn("common-edge-cases", "Missing references/common-edge-cases.md")


def check_automated_check_script(c, file_path):
    skill_dir = os.path.dirname(file_path)
    script_path = os.path.join(skill_dir, "references", "automated_check_script.py")
    if os.path.isfile(script_path):
        c.check_pass("automation-script")
        if os.access(script_path, os.X_OK):
            c.check_pass("automation-script-executable")
        else:
            c.check_warn("automation-script", "automated_check_script.py is not executable")
    else:
        c.check_warn("automation-script", "Missing references/automated_check_script.py")


def check_markdown_headings(c, file_path):
    contents = read_file(file_path)
    if re.search(r"^#\s+", contents, re.MULTILINE):
        c.check_pass("Markdown-H1")
    else:
        c.check_warn("Markdown-H1", "Missing H1 heading")


def check_markdown_code_blocks(c, file_path):
    contents = read_file(file_path)
    count = len(re.findall(r"^\s*```", contents, re.MULTILINE))
    if count % 2 == 0:
        c.check_pass("Markdown-code-blocks")
    else:
        c.check_fail("Markdown-code-blocks", "MEDIUM",
                     f"Code blocks not paired ({count} markers)")


def check_no_self_ref(c, file_path):
    fm = read_frontmatter(file_path)
    name = fm.get("name", "")
    if not name:
        c.check_warn("self-reference", "Cannot check self-reference (name field missing)")
        return
    contents = read_file(file_path)
    count = contents.count(name)
    if count <= 3:
        c.check_pass("self-reference")
    else:
        c.check_warn("self-reference", f"Possible self-reference ({count} times)")


def check_skill_refs(c, file_path):
    contents = read_file(file_path)
    refs = re.findall(r"harness-[a-z-]+", contents)
    unique_refs = sorted(set(r for r in refs if r != "harness-" and r != "harness-"))
    missing = 0
    for ref in unique_refs:
        ref_dir = os.path.join(SKILLS_DIR, ref)
        if not os.path.isdir(ref_dir):
            c.check_warn("skill-reference", f"Reference does not exist: {ref}")
            missing += 1
    if missing == 0:
        c.check_pass("skill-reference")


# --- Main assessment ---

def assess_skill(skill):
    """Assess a single skill, return results dict."""
    file_path = os.path.join(SKILLS_DIR, skill, "SKILL.md")
    c = WeightedSkillChecker(skill)

    # File structure check
    if not check_file_exists(c, file_path):
        return c.to_dict()
    check_file_readable(c, file_path)
    check_file_encoding(c, file_path)

    # Frontmatter deep check
    check_fm_field(c, file_path, "name")
    check_fm_field(c, file_path, "description")
    check_fm_field(c, file_path, "when_to_use")
    check_fm_field(c, file_path, "compatibility")
    check_fm_field(c, file_path, "context", required=False)
    check_fm_field(c, file_path, "agent", required=False)
    check_fm_no_version(c, file_path)
    check_fm_metadata(c, file_path)
    check_fm_context(c, file_path)
    check_fm_allowed_tools(c, file_path)
    check_fm_metadata_category(c, file_path)
    check_fm_description_length(c, file_path)
    check_fm_allowed_tools_syntax(c, file_path)
    check_fm_agent_prompt_consistency(c, file_path)

    # Section structure check
    for s in ["Core Principles", "When to Use", "When Not to Use",
              "Methodology", "Key Points", "Common Pitfalls", "Edge Case Handling"]:
        check_section(c, file_path, s)
    check_hard_constraints_section(c, file_path)
    check_agent_prompt(c, file_path)

    # Markdown format check
    check_markdown_headings(c, file_path)
    check_markdown_code_blocks(c, file_path)

    # Content depth check
    check_content_examples(c, file_path)
    check_content_error_handling(c, file_path)
    check_content_best_practices(c, file_path)
    check_last_updated_freshness(c, file_path)

    # Cross-skill check
    check_cross_skill_handoff(c, file_path)
    check_common_edge_cases(c, file_path)
    check_automated_check_script(c, file_path)

    # Reference check
    check_no_self_ref(c, file_path)
    check_skill_refs(c, file_path)

    return c.to_dict()


def assess_all():
    """Assess all skills and produce cross-skill summary."""
    skills = []
    for entry in sorted(os.listdir(SKILLS_DIR)):
        d = os.path.join(SKILLS_DIR, entry)
        if os.path.isdir(d) and os.path.isfile(os.path.join(d, "SKILL.md")):
            skills.append(entry)

    results = []
    total_score = 0.0
    count = 0
    for skill in skills:
        result = assess_skill(skill)
        results.append(result)
        total_score += result.get("weighted_score", 0)
        count += 1

    avg_score = round(total_score / count, 2) if count > 0 else 0

    # Cross-skill uniformity check
    required_sections = ["Core Principles", "When to Use", "Methodology", "Key Points"]
    missing_map = []
    for skill in skills:
        contents = read_file(os.path.join(SKILLS_DIR, skill, "SKILL.md"))
        for sec in required_sections:
            if not re.search(rf"^##\s+{re.escape(sec)}", contents, re.MULTILINE):
                missing_map.append(f"[{skill}:{sec}]")

    cross_skill_issues = []
    if missing_map:
        cross_skill_issues.append({
            "check": "cross-skill-uniformity",
            "severity": "WARN",
            "detail": f"Skills missing required sections:{' '.join(missing_map)}"
        })

    # Bidirectional reference check
    bidir_issues = []
    for skill in skills:
        contents = read_file(os.path.join(SKILLS_DIR, skill, "SKILL.md"))
        refs = set(re.findall(r"harness-[a-z-]+", contents))
        for ref in refs:
            if ref in ("harness-", "") or ref == skill:
                continue
            ref_contents = read_file(os.path.join(SKILLS_DIR, ref, "SKILL.md"))
            if ref_contents and skill not in ref_contents:
                bidir_issues.append(f"[{skill}→{ref}]")

    if bidir_issues:
        cross_skill_issues.append({
            "check": "bidirectional-refs",
            "severity": "WARN",
            "detail": f"Missing back-references:{' '.join(bidir_issues)}"
        })

    output = {
        "evaluation_date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "total_skills": len(results),
        "average_score": avg_score,
        "scoring_model": "weighted (CRITICAL=5, HIGH=3, MEDIUM=2, LOW=1, WARN=0)",
        "results": results,
        "cross_skill_checks": {
            "total_cross_skill_checks": 2,
            "cross_skill_issues": len(cross_skill_issues),
        },
        "cross_skill_issues": cross_skill_issues,
    }

    return output


# --- Entry point ---

def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "all"
    if target == "all":
        output = assess_all()
    else:
        target_path = os.path.join(SKILLS_DIR, target)
        if not os.path.isdir(target_path):
            print(json.dumps({"error": f"Skill not found: {target}"}), file=sys.stderr)
            sys.exit(1)
        output = assess_skill(target)

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
