#!/bin/bash
# Automated check script for harness-observability-and-browser
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
for ref_file in "browser-verification-cycle.md" "observability-tools-guide.md" "verification-checklist-template.md" "capability-gap-report-template.md"; do
  ((++TOTAL_EXTRA))
  if [ -f "$SKILL_DIR/references/$ref_file" ]; then
    ((++PASSED_EXTRA))
  else
    echo "  [FAIL] Missing reference: $ref_file"
  fi
done

# Check browser automation config section
((++TOTAL_EXTRA))
if grep -qE "浏览器自动化配置参考" "$SKILL_DIR/SKILL.md"; then
  ((++PASSED_EXTRA))
else
  echo "  [FAIL] Missing 浏览器自动化配置参考 section"
fi

# Check that two types of feedback sensors are mentioned
((++TOTAL_EXTRA))
if grep -qE "两类反馈传感器" "$SKILL_DIR/SKILL.md"; then
  ((++PASSED_EXTRA))
else
  echo "  [FAIL] Missing 两类反馈传感器 section"
fi

# Check for Playwright/Puppeteer mentions
((++TOTAL_EXTRA))
if grep -qE "Playwright|Puppeteer" "$SKILL_DIR/SKILL.md"; then
  ((++PASSED_EXTRA))
else
  echo "  [FAIL] Missing browser automation tool names (Playwright/Puppeteer)"
fi

# Check verification example criteria present
((++TOTAL_EXTRA))
if grep -qE "验收标准示例" "$SKILL_DIR/SKILL.md"; then
  ((++PASSED_EXTRA))
else
  echo "  [FAIL] Missing 验收标准示例 section"
fi

echo "---"
echo "Extra checks: $PASSED_EXTRA/$TOTAL_EXTRA passed"
