#!/bin/bash
# Automated check script for harness-architecture-boundaries
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
for ref_file in "architecture-template.md" "check-pattern-template.md" "e2e-architecture-audit-example.md"; do
  ((++TOTAL_EXTRA))
  if [ -f "$SKILL_DIR/references/$ref_file" ]; then
    ((++PASSED_EXTRA))
  else
    echo "  [FAIL] Missing reference: $ref_file"
  fi
done

# Check that Severity Classification Reference section exists
((++TOTAL_EXTRA))
if grep -qE "Severity Classification Reference" "$SKILL_DIR/SKILL.md"; then
  ((++PASSED_EXTRA))
else
  echo "  [FAIL] Missing Severity Classification Reference section"
fi

# Check hard constraints mention severity levels
((++TOTAL_EXTRA))
if grep -qE "CRITICAL|HIGH|MEDIUM|LOW" "$SKILL_DIR/SKILL.md"; then
  ((++PASSED_EXTRA))
else
  echo "  [FAIL] Hard constraints missing severity level references"
fi

# Check that Best Practices section exists and is not empty
((++TOTAL_EXTRA))
if grep -qE "^##\s+Best Practices" "$SKILL_DIR/SKILL.md"; then
  ((++PASSED_EXTRA))
else
  echo "  [FAIL] Missing Best Practices section"
fi

# Check Finding Organization Specification section
((++TOTAL_EXTRA))
if grep -qE "Finding organization specification" "$SKILL_DIR/SKILL.md"; then
  ((++PASSED_EXTRA))
else
  echo "  [FAIL] Missing Finding Organization Specification section"
fi

# Check Reference Layering Model section
((++TOTAL_EXTRA))
if grep -qE "Reference Layering Model" "$SKILL_DIR/SKILL.md"; then
  ((++PASSED_EXTRA))
else
  echo "  [FAIL] Missing Reference Layering Model section"
fi

echo "---"
echo "Extra checks: $PASSED_EXTRA/$TOTAL_EXTRA passed"
