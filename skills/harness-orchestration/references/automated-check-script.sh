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

# Check SKILL.md has 五条标准工作流 section
((++TOTAL_EXTRA))
if grep -qE "五条标准工作流" "$SKILL_DIR/SKILL.md"; then
  ((++PASSED_EXTRA))
else
  echo "  [FAIL] Missing 五条标准工作流 section"
fi

# Check SKILL.md has 跨skill交接点 or 相关 Skill section
((++TOTAL_EXTRA))
if grep -qE "^##\s+跨skill交接点|^##\s+相关 Skill" "$SKILL_DIR/SKILL.md"; then
  ((++PASSED_EXTRA))
else
  echo "  [FAIL] Missing 跨skill交接点 or 相关 Skill section"
fi

# Check for 常见省略场景 section
((++TOTAL_EXTRA))
if grep -qE "常见省略场景" "$SKILL_DIR/SKILL.md"; then
  ((++PASSED_EXTRA))
else
  echo "  [FAIL] Missing 常见省略场景 section"
fi

echo "---"
echo "Extra checks: $PASSED_EXTRA/$TOTAL_EXTRA passed"
