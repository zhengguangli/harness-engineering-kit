#!/bin/bash
# Automated check script for harness-commit-gate
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
for ref_file in "commit-message-guide.md" "ci-integration-guide.md"; do
  ((++TOTAL_EXTRA))
  if [ -f "$SKILL_DIR/references/$ref_file" ]; then
    ((++PASSED_EXTRA))
  else
    echo "  [FAIL] Missing reference: $ref_file"
  fi
done

# Check frontmatter has allowed-tools declared
((++TOTAL_EXTRA))
if grep -q "^allowed-tools:" "$SKILL_DIR/SKILL.md"; then
  ((++PASSED_EXTRA))
else
  echo "  [FAIL] Frontmatter missing allowed-tools field"
fi

# Check methodology mentions "three-layer check" section
((++TOTAL_EXTRA))
if grep -qE "Three Checks of the Quality Gate" "$SKILL_DIR/SKILL.md"; then
  ((++PASSED_EXTRA))
else
  echo "  [FAIL] Missing Three Checks of the Quality Gate section in methodology"
fi

# Check toolchain probe process
((++TOTAL_EXTRA))
if grep -qE "Toolchain Detection Flow|Check Strategy.*Based on Project Configuration" "$SKILL_DIR/SKILL.md"; then
  ((++PASSED_EXTRA))
else
  echo "  [FAIL] Missing Toolchain Detection Flow / Check Strategy section"
fi

# Check that "Diff Review" check is documented
((++TOTAL_EXTRA))
if grep -qE "Diff.*Review|diff.*review" "$SKILL_DIR/SKILL.md"; then
  ((++PASSED_EXTRA))
else
  echo "  [FAIL] Missing Diff Review check documentation"
fi

echo "---"
echo "Extra checks: $PASSED_EXTRA/$TOTAL_EXTRA passed"
