#!/usr/bin/env python3
"""Automated check script for harness-prompt-optimizer"""
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
    ["prompt-architecture-template.md", "optimization-examples.md",
     "variable-dictionary-design-guide.md", "six-block-design-notes.md"])
print_extra_summary(checker, passed_extra, total_extra)

sys.exit(checker.exit_code())
