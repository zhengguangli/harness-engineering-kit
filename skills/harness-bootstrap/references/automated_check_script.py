#!/usr/bin/env python3
"""Automated check script for harness-bootstrap"""
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
    ["claude-md-template.md", "claude-md-examples.md", "docs-skeleton-template.md",
     "docs-skeleton-by-stack.md", "gitignore-templates.md", "init-workflows.md"])

# Skill-specific content checks
content = read_file(os.path.join(SKILL_DIR, "SKILL.md"))
for pattern, label in [
    (r"^##\s+Core Principles", "Core Principles section"),
    (r"Project Type Tailoring Guide", "Project Type Tailoring Guide"),
    (r"Three-Layer Structure", "Three-Layer Structure"),
    (r"Post-Initialization Checklist", "Post-Initialization Checklist"),
    (r"\.gitignore", ".gitignore rules section"),
    (r"Write is for new files only", "Hard constraint: Write for new files only"),
]:
    total_extra += 1
    if has_text(content, pattern, re.IGNORECASE | re.MULTILINE):
        passed_extra += 1; checker.check_pass(label)
    else:
        print(f"  [FAIL] Missing {label}")

print_extra_summary(checker, passed_extra, total_extra)

sys.exit(checker.exit_code())
