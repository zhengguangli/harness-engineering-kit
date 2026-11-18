#!/usr/bin/env python3
"""Automated check script for harness-exec-plans"""
import os, re, sys

# Shared checker library lives in the kit repo's scripts/lib/. Resolve it via an
# absolute path so the script works from any CWD, and degrade gracefully when the
# skill has been deployed standalone (e.g. ~/.claude/skills/<name>/) where the
# kit's scripts/ directory is not shipped -- there is nothing to check there.
_SHARED_LIB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../scripts")
if os.path.isdir(_SHARED_LIB):
    sys.path.insert(0, _SHARED_LIB)
    from lib.harness_check import (read_file, run_shared_checks,
                                    check_reference_files, check_skill_patterns,
                                    print_extra_summary, count_hard_constraints)
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
    ["exec-plan-template.md", "tech-debt-tracker-template.md", "agent-handoff-protocol.md"])

# Skill-specific content checks
content = read_file(os.path.join(SKILL_DIR, "SKILL.md"))
p, t = check_skill_patterns(checker, content, [
    (r"Plan only, no.*code", "Plan only, no code constraint"),
    (r"mechanically verifiable", "Mechanically verifiable criteria"),
    (r"one PR|single PR", "One-PR step granularity"),
    (r"Decision log", "Decision log concept"),
    (r"Non-goals", "Non-goals requirement"),
    (r"overrun|50%|blocked", "Overrun / blocked protocol"),
], flags=re.IGNORECASE)
passed_extra += p
total_extra += t

constraint_count = count_hard_constraints(content)
total_extra += 1
if constraint_count >= 4:
    passed_extra += 1; checker.check_pass("hard-constraints-count")
else:
    checker.check_fail("hard-constraints-count", "MEDIUM", f"Hard Constraints count: {constraint_count} (expected ≥4)")

print_extra_summary(checker, passed_extra, total_extra)

sys.exit(checker.exit_code())
