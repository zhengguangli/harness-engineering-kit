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

# Check SKILL.md contains "偏差存活时间" in 核心原则 section
((++TOTAL_EXTRA))
if grep -qE "^##\s+核心原则" "$SKILL_DIR/SKILL.md"; then
  if sed -n '/^## 核心原则/,/^## /p' "$SKILL_DIR/SKILL.md" | grep -q "偏差存活时间"; then
    ((++PASSED_EXTRA))
  else
    echo "  [FAIL] 核心原则 section missing '偏差存活时间'"
  fi
else
  echo "  [FAIL] Missing 核心原则 section"
fi

# Check 清扫节奏 section
((++TOTAL_EXTRA))
if grep -qE "清扫节奏" "$SKILL_DIR/SKILL.md"; then
  ((++PASSED_EXTRA))
else
  echo "  [FAIL] Missing 清扫节奏 section"
fi

# Check Golden Principles vs Architecture Boundaries comparison table
((++TOTAL_EXTRA))
if grep -qE "黄金原则 vs 架构边界" "$SKILL_DIR/SKILL.md"; then
  ((++PASSED_EXTRA))
else
  echo "  [FAIL] Missing 黄金原则 vs 架构边界 comparison table"
fi

echo "---"
echo "Extra checks: $PASSED_EXTRA/$TOTAL_EXTRA passed"
