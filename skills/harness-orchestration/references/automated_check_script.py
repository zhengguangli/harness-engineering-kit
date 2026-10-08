#!/usr/bin/env python3
"""Automated check script for harness-orchestration"""
import os, re, sys

# Shared checker library lives in the kit repo's scripts/lib/. Resolve it via an
# absolute path so the script works from any CWD, and degrade gracefully when the
# skill has been deployed standalone (e.g. ~/.claude/skills/<name>/) where the
# kit's scripts/ directory is not shipped -- there is nothing to check there.
_SHARED_LIB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../scripts")
if os.path.isdir(_SHARED_LIB):
    sys.path.insert(0, _SHARED_LIB)
    from lib.harness_check import (read_file, read_lines, has_text, SkillChecker,
                                    run_shared_checks, check_reference_files,
                                    print_extra_summary, count_hard_constraints,
                                    count_agent_constraints)
else:
    print("[SKIP] shared checker library not found at ../../../scripts -- this "
          "script only runs inside the harness-engineering-kit repository "
          "layout; a standalone-deployed skill copy has nothing to check.")
    sys.exit(0)

# Path resolution
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, ".."))
SKILLS_DIR = os.path.normpath(os.path.join(SKILL_DIR, ".."))
SKILL_NAME = os.path.basename(SKILL_DIR)

checker = run_shared_checks(SKILLS_DIR, SKILL_NAME)

checker.print_json()

passed_extra, total_extra = check_reference_files(checker, SKILL_DIR,
    ["routing-decision-tree.md", "workflow-execution-examples.md"])

# Skill-specific content checks
content = read_file(os.path.join(SKILL_DIR, "SKILL.md"))
for pattern, label in [
    (r"Five Standard Workflows", "Five Standard Workflows section"),
    (r"^##\s+Cross-Skill Handoff Points|^##\s+Related Skills", "Cross-Skill Handoff or Related Skills section"),
    (r"Omission Decision Guide", "Omission Decision Guide section"),
    (r"FAQ / Troubleshooting", "FAQ / Troubleshooting section"),
    (r"Intent Matching Table|User Intent Matching|Intent Matching", "Intent Matching Table section"),
    (r"^###\s+\d+\.\s+Three-Layer Routing", "Three-Layer Routing Framework section"),
    (r"Cross-workflow combination", "Cross-workflow combination handling"),
    (r"Read-only.*routing|read-only.*orchestrat", "Read-only routing advisor constraint"),
    (r"Routing Quality Validation", "Routing Quality Validation subsection"),
    (r"^##\s+Hard Constraints", "Hard Constraints section"),
]:
    total_extra += 1
    if has_text(content, pattern, re.IGNORECASE | re.MULTILINE):
        passed_extra += 1; checker.check_pass(label)
    else:
        print(f"  [FAIL] Missing {label}")

# Workflow completeness: all 5 workflows must be present
workflow_count = len(re.findall(r"###\s+Workflow\s+\d+", content))
total_extra += 1
if workflow_count >= 5:
    passed_extra += 1; checker.check_pass("workflow-completeness")
else:
    print(f"  [FAIL] Only {workflow_count}/5 workflows defined (expected ≥5)")

# Hard Constraints count: must have at least 4
constraint_count = count_hard_constraints(content)
total_extra += 1
if constraint_count >= 4:
    passed_extra += 1; checker.check_pass("hard-constraints-count")
else:
    print(f"  [FAIL] Hard Constraints count: {constraint_count} (expected ≥4)")

# Handoff table completeness: must have at least 4 rows
handoff_section = content[content.find("## Cross-Skill Handoff Points"):content.find("## Edge Case")] if "## Cross-Skill Handoff Points" in content else ""
handoff_rows = len(re.findall(r"^\|.*\|.*\|.*\|", handoff_section, re.MULTILINE))
total_extra += 1
if handoff_rows >= 4:
    passed_extra += 1; checker.check_pass("handoff-table-completeness")
else:
    print(f"  [FAIL] Handoff table rows: {handoff_rows} (expected ≥4)")

print_extra_summary(checker, passed_extra, total_extra)

sys.exit(checker.exit_code())
