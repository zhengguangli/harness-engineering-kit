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
    ["exec-plan-template.md", "tech-debt-tracker-template.md", "agent-handoff-protocol.md"])

# Skill-specific content checks
content = read_file(os.path.join(SKILL_DIR, "SKILL.md"))
for pattern, label in [
    (r"exec-plan.*(?:File Structure|Template)", "exec-plan file structure/template section"),
    (r"Lightweight Plan", "Lightweight Plan concept"),
    (r"Parallel Collaboration", "Parallel Collaboration concept"),
    (r"Plan Quality Checklist", "Plan Quality Checklist section"),
    (r"Decision log", "Decision log concept"),
    (r"plan overrun|Plan overrun|scope re-assessment", "Plan overrun recovery mechanism"),
    (r"Directory.*Lifecycle|Directory & Lifecycle", "Directory lifecycle management"),
    (r"Cross-skill handoff|cross.*skill.*handoff", "Cross-skill handoff documentation"),
]:
    total_extra += 1
    if has_text(content, pattern, re.IGNORECASE):
        passed_extra += 1; checker.check_pass(label)
    else:
        print(f"  [FAIL] Missing {label}")

# Hard Constraints completeness: must have at least 3
constraint_count = count_hard_constraints(content)
total_extra += 1
if constraint_count >= 3:
    passed_extra += 1; checker.check_pass("hard-constraints-count")
else:
    print(f"  [FAIL] Hard Constraints count: {constraint_count} (expected ≥3)")

# Examples count: must have at least 4
example_count = len(re.findall(r"\*\*Example\s+\d+\*\*", content))
total_extra += 1
if example_count >= 4:
    passed_extra += 1; checker.check_pass("examples-count")
else:
    print(f"  [FAIL] Examples count: {example_count} (expected ≥4)")

# Agent Prompt constraints: must have at least 6
agent_constraint_count = count_agent_constraints(content)
total_extra += 1
if agent_constraint_count >= 6:
    passed_extra += 1; checker.check_pass("agent-constraints-count")
else:
    print(f"  [FAIL] Agent Prompt constraints: {agent_constraint_count} (expected ≥6)")

print_extra_summary(checker, passed_extra, total_extra)

sys.exit(checker.exit_code())
