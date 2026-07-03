#!/bin/bash
# Automated check script for harness-exec-plans
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
for ref_file in "exec-plan-template.md" "tech-debt-tracker-template.md" "agent-handoff-protocol.md"; do
  ((++TOTAL_EXTRA))
  if [ -f "$SKILL_DIR/references/$ref_file" ]; then
    ((++PASSED_EXTRA))
  else
    echo "  [FAIL] Missing reference: $ref_file"
  fi
done

# Check exec-plan file structure section
((++TOTAL_EXTRA))
if grep -qE "exec-plan 文件结构|exec-plan.*模板" "$SKILL_DIR/SKILL.md"; then
  ((++PASSED_EXTRA))
else
  echo "  [FAIL] Missing exec-plan file structure section"
fi

# Check 临时计划 vs 执行计划 comparison
((++TOTAL_EXTRA))
if grep -qE "临时计划|临时轻量计划" "$SKILL_DIR/SKILL.md"; then
  ((++PASSED_EXTRA))
else
  echo "  [FAIL] Missing 临时计划 vs 执行计划 comparison"
fi

# Check 并行协作约定 section
((++TOTAL_EXTRA))
if grep -qE "并行协作" "$SKILL_DIR/SKILL.md"; then
  ((++PASSED_EXTRA))
else
  echo "  [FAIL] Missing 并行协作约定 section"
fi

echo "---"
echo "Extra checks: $PASSED_EXTRA/$TOTAL_EXTRA passed"
