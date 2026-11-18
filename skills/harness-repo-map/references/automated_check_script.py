#!/usr/bin/env python3
"""Automated check script for harness-repo-map"""
import os, re, sys

# Shared checker library lives in the kit repo's scripts/lib/. Resolve it via an
# absolute path so the script works from any CWD, and degrade gracefully when the
# skill has been deployed standalone (e.g. ~/.claude/skills/<name>/) where the
# kit's scripts/ directory is not shipped -- there is nothing to check there.
_SHARED_LIB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../scripts")
if os.path.isdir(_SHARED_LIB):
    sys.path.insert(0, _SHARED_LIB)
    from lib.harness_check import (read_file, has_text,
                                    run_shared_checks, check_reference_files,
                                    check_skill_patterns, print_extra_summary)
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
    ["agents-md-map-template.md", "e2e-repo-map-example.md"])

# Skill-specific content checks
content = read_file(os.path.join(SKILL_DIR, "SKILL.md"))
p, t = check_skill_patterns(checker, content, [
    (r"table of contents|not an encyclopedia|progressive disclosure", "Core philosophy (map/encyclopedia)"),
    (r"broken.link", "Broken-link detection mention"),
    (r"freshness|last update|30 days", "Freshness check mention"),
    (r"AGENTS\.md\s*≤\s*100|AGENTS\.md.*100 lines", "AGENTS.md ≤ 100 line constraint"),
    (r"Strictly read-only", "Read-only audit constraint"),
])
passed_extra += p
total_extra += t

# TD-007 anti-regression: map template must not regress to CLAUDE.md
total_extra += 1
map_tpl = read_file(os.path.join(SKILL_DIR, "references", "agents-md-map-template.md"))
if has_text(map_tpl, r"CLAUDE\.md"):
    checker.check_fail("map-template-no-claude-md", "MEDIUM", "agents-md-map-template.md still mentions CLAUDE.md")
else:
    passed_extra += 1
    checker.check_pass("map-template-no-claude-md")

print_extra_summary(checker, passed_extra, total_extra)

sys.exit(checker.exit_code())
