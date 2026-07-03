#!/bin/bash
# Automated check script for harness-golden-principles
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
for ref_file in "quality-score-template.md" "pr-guidelines.md" "principle-prioritization.md" "rule-formulation-checklist.md"; do
  ((++TOTAL_EXTRA))
  if [ -f "$SKILL_DIR/references/$ref_file" ]; then
    ((++PASSED_EXTRA))
  else
    echo "  [FAIL] Missing reference: $ref_file"
  fi
done

# Check SKILL.md Core Principles section contains "Deviation lifetime"
((++TOTAL_EXTRA))
if grep -qE "^##\s+Core Principles" "$SKILL_DIR/SKILL.md"; then
  if sed -n '/^## Core Principles/,/^## /p' "$SKILL_DIR/SKILL.md" | grep -q "Deviation lifetime"; then
    ((++PASSED_EXTRA))
  else
    echo "  [FAIL] Core Principles section missing 'Deviation lifetime'"
  fi
else
  echo "  [FAIL] Missing Core Principles section"
fi

# Check Sweep Rhythm section in SKILL.md
((++TOTAL_EXTRA))
if grep -qE "Sweep Rhythm" "$SKILL_DIR/SKILL.md"; then
  ((++PASSED_EXTRA))
else
  echo "  [FAIL] Missing Sweep Rhythm section"
fi

# Check Golden Principles vs Architecture Boundaries comparison table
((++TOTAL_EXTRA))
if grep -qE "Golden Principles vs Architecture Boundaries" "$SKILL_DIR/SKILL.md"; then
  ((++PASSED_EXTRA))
else
  echo "  [FAIL] Missing Golden Principles vs Architecture Boundaries comparison table"
fi

echo "---"
echo "Extra checks: $PASSED_EXTRA/$TOTAL_EXTRA passed"
