#!/bin/bash
# Automated check script for harness-orchestration
# Includes shared checks + skill-specific checks

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../../.." && pwd)"
SKILL_NAME="$(basename "$SKILL_DIR")"

# Run shared checks first
shared_result=$(bash "$ROOT_DIR/scripts/skill-automated-check.sh" "$ROOT_DIR/skills" "$SKILL_NAME")
echo "$shared_result"

# Skill-specific checks
TOTAL_EXTRA=0
PASSED_EXTRA=0

# Check mandatory reference files
for ref_file in "routing-decision-tree.md" "workflow-execution-examples.md"; do
  ((++TOTAL_EXTRA))
  if [ -f "$SKILL_DIR/references/$ref_file" ]; then
    ((++PASSED_EXTRA))
  else
    echo "  [FAIL] Missing reference: $ref_file"
  fi
done

# Check SKILL.md has Five Standard Workflows section
((++TOTAL_EXTRA))
if grep -qE "Five Standard Workflows" "$SKILL_DIR/SKILL.md"; then
  ((++PASSED_EXTRA))
else
  echo "  [FAIL] Missing Five Standard Workflows section"
fi

# Check SKILL.md has Cross-Skill Handoff Points or Related Skills section
((++TOTAL_EXTRA))
if grep -qE "^##\s+Cross-Skill Handoff Points|^##\s+Related Skills" "$SKILL_DIR/SKILL.md"; then
  ((++PASSED_EXTRA))
else
  echo "  [FAIL] Missing Cross-Skill Handoff Points or Related Skills section"
fi

# Check for Common Omission Scenarios section
((++TOTAL_EXTRA))
if grep -qE "Common Omission Scenarios" "$SKILL_DIR/SKILL.md"; then
  ((++PASSED_EXTRA))
else
  echo "  [FAIL] Missing Common Omission Scenarios section"
fi

echo "---"
echo "Extra checks: $PASSED_EXTRA/$TOTAL_EXTRA passed"
