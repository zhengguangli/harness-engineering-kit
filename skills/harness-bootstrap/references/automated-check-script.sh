#!/bin/bash
# Automated check script for harness-bootstrap
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
for ref_file in "agents-md-template.md" "agents-md-examples.md" "docs-skeleton-template.md" "docs-skeleton-by-stack.md" "gitignore-templates.md" "init-workflows.md"; do
  ((++TOTAL_EXTRA))
  if [ -f "$SKILL_DIR/references/$ref_file" ]; then
    ((++PASSED_EXTRA))
  else
    echo "  [FAIL] Missing reference: $ref_file"
  fi
done

# Check SKILL.md contains "最小可用" in 核心原则 section
((++TOTAL_EXTRA))
if grep -qE "^##\s+核心原则" "$SKILL_DIR/SKILL.md"; then
  if sed -n '/^## 核心原则/,/^## /p' "$SKILL_DIR/SKILL.md" | grep -q "最小可用"; then
    ((++PASSED_EXTRA))
  else
    echo "  [FAIL] 核心原则 section missing '最小可用'"
  fi
else
  echo "  [FAIL] Missing 核心原则 section"
fi

# Check 项目类型裁减指南 section exists (new content)
((++TOTAL_EXTRA))
if grep -qE "项目类型裁减指南" "$SKILL_DIR/SKILL.md"; then
  ((++PASSED_EXTRA))
else
  echo "  [FAIL] Missing 项目类型裁减指南 section"
fi

# Check 三层结构 section
((++TOTAL_EXTRA))
if grep -qE "三层结构" "$SKILL_DIR/SKILL.md"; then
  ((++PASSED_EXTRA))
else
  echo "  [FAIL] Missing 三层结构 section in methodology"
fi

# Check 初始化后检查清单
((++TOTAL_EXTRA))
if grep -qE "初始化后检查清单" "$SKILL_DIR/SKILL.md"; then
  ((++PASSED_EXTRA))
else
  echo "  [FAIL] Missing 初始化后检查清单 section"
fi

echo "---"
echo "Extra checks: $PASSED_EXTRA/$TOTAL_EXTRA passed"
