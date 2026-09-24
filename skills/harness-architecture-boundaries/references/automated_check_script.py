#!/usr/bin/env python3
"""Automated check script for harness-architecture-boundaries"""
import os, re, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../scripts"))
from lib.harness_check import (read_file, read_lines, has_text, SkillChecker,
                                run_shared_checks, check_reference_files,
                                print_extra_summary, count_hard_constraints,
                                count_agent_constraints)

# Path resolution
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, ".."))
SKILLS_DIR = os.path.normpath(os.path.join(SKILL_DIR, ".."))
SKILL_NAME = os.path.basename(SKILL_DIR)

checker = run_shared_checks(SKILLS_DIR, SKILL_NAME)

checker.print_json()

passed_extra, total_extra = check_reference_files(checker, SKILL_DIR,
    ["architecture-template.md", "check-pattern-template.md", "e2e-architecture-audit-example.md"])

# Skill-specific content checks
content = read_file(os.path.join(SKILL_DIR, "SKILL.md"))
for pattern, label in [
    (r"Severity Classification Reference", "Severity Classification Reference section"),
    (r"CRITICAL|HIGH|MEDIUM|LOW", "severity level references"),
    (r"^##\s+Best Practices", "Best Practices section"),
    (r"Finding organization specification", "Finding Organization Specification section"),
    (r"Reference Layering Model", "Reference Layering Model section"),
    (r"Parse.*Don.*Validate|Parse, Don't Validate", "Parse Don't Validate pattern"),
    (r"cross-cutting.*chokepoint|single chokepoint|unified Providers", "Cross-cutting chokepoint pattern"),
    (r"Implementation variations", "Implementation variations across projects"),
]:
    total_extra += 1
    if has_text(content, pattern, re.IGNORECASE | re.MULTILINE):
        passed_extra += 1; checker.check_pass(label)
    else:
        print(f"  [FAIL] Missing {label}")

# Hard Constraints completeness: must have at least 5
constraint_section = content[content.find("## Hard Constraints"):content.find("## Key Points")] if "## Hard Constraints" in content else ""
constraint_count = len(re.findall(r"^\d+\.\s+\*\*", constraint_section, re.MULTILINE))
total_extra += 1
if constraint_count >= 5:
    passed_extra += 1; checker.check_pass("hard-constraints-count")
else:
    print(f"  [FAIL] Hard Constraints count: {constraint_count} (expected ≥5)")

# Layering model diagram: must contain the arrow chain
total_extra += 1
if has_text(content, r"Types\s*→\s*Config\s*→\s*Repo\s*→\s*Service"):
    passed_extra += 1; checker.check_pass("layering-model-diagram")
else:
    print(f"  [FAIL] Missing layering model arrow chain (Types → Config → Repo → Service)")

# Agent Prompt constraints count: must have at least 5
agent_constraint_count = count_agent_constraints(content)
total_extra += 1
if agent_constraint_count >= 5:
    passed_extra += 1; checker.check_pass("agent-constraints-count")
else:
    print(f"  [FAIL] Agent Prompt constraints: {agent_constraint_count} (expected ≥5)")

print_extra_summary(checker, passed_extra, total_extra)

sys.exit(checker.exit_code())
