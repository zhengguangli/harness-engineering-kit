#!/bin/bash
# Automated check script for harness-authoring
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
for ref_file in "scaffold-templates.md" "skill-design-patterns.md" "subagent-design-patterns.md" "context-budget-management-guide.md"; do
  ((++TOTAL_EXTRA))
  if [ -f "$SKILL_DIR/references/$ref_file" ]; then
    ((++PASSED_EXTRA))
  else
    echo "  [FAIL] Missing reference: $ref_file"
  fi
done

# Check context budget discipline mentioned in 方法论
((++TOTAL_EXTRA))
if grep -qE "上下文预算" "$SKILL_DIR/SKILL.md"; then
  ((++PASSED_EXTRA))
else
  echo "  [FAIL] 方法论 missing 上下文预算 discipline"
fi

# Check canonical 版本约定 section
((++TOTAL_EXTRA))
if grep -qE "canonical" "$SKILL_DIR/SKILL.md"; then
  ((++PASSED_EXTRA))
else
  echo "  [FAIL] Missing canonical version convention"
fi

# Check Skill vs Subagent comparison table present
((++TOTAL_EXTRA))
if grep -qE "^##\s+方法论" "$SKILL_DIR/SKILL.md" && grep -qE "Skill.*Subagent" "$SKILL_DIR/SKILL.md"; then
  ((++PASSED_EXTRA))
else
  echo "  [FAIL] Missing Skill vs Subagent comparison table"
fi

# Check minimal-tools-principle mentioned
((++TOTAL_EXTRA))
if grep -qE "最小权限" "$SKILL_DIR/SKILL.md"; then
  ((++PASSED_EXTRA))
else
  echo "  [FAIL] Missing 最小权限 principle"
fi

echo "---"
echo "Extra checks: $PASSED_EXTRA/$TOTAL_EXTRA passed"
