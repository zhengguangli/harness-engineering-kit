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

# Check 严重程度分类参考 table exists
((++TOTAL_EXTRA))
if grep -qE "严重程度分类参考" "$SKILL_DIR/SKILL.md"; then
  ((++PASSED_EXTRA))
else
  echo "  [FAIL] Missing 严重程度分类参考 section"
fi

# Check hard constraints mention severity levels
((++TOTAL_EXTRA))
if grep -qE "CRITICAL|HIGH|MEDIUM|LOW" "$SKILL_DIR/SKILL.md"; then
  ((++PASSED_EXTRA))
else
  echo "  [FAIL] Hard constraints missing severity level references"
fi

# Check that 最佳实践 section exists and is not empty
((++TOTAL_EXTRA))
if grep -qE "^##\s+最佳实践" "$SKILL_DIR/SKILL.md"; then
  ((++PASSED_EXTRA))
else
  echo "  [FAIL] Missing 最佳实践 section"
fi

# Check 发现项编排规范 section
((++TOTAL_EXTRA))
if grep -qE "发现项编排规范" "$SKILL_DIR/SKILL.md"; then
  ((++PASSED_EXTRA))
else
  echo "  [FAIL] Missing 发现项编排规范 section"
fi

# Check 典型分层模型参考 section
((++TOTAL_EXTRA))
if grep -qE "典型分层模型参考" "$SKILL_DIR/SKILL.md"; then
  ((++PASSED_EXTRA))
else
  echo "  [FAIL] Missing 典型分层模型参考 section"
fi

echo "---"
echo "Extra checks: $PASSED_EXTRA/$TOTAL_EXTRA passed"
