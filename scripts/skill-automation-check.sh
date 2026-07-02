#!/bin/bash
# 通用 SKILL.md 自动化检查脚本
# Usage: ./scripts/skill-automation-check.sh <skill-name>
# Example: ./scripts/skill-automation-check.sh harness-commit-gate

SKILL_NAME="$1"
if [ -z "$SKILL_NAME" ]; then
  echo "Usage: $0 <skill-name>"
  exit 1
fi

SKILLS_DIR="./skills"
REPORT_FILE="docs/quality-reports/${SKILL_NAME}-check.md"
SKILL_FILE="$SKILLS_DIR/$SKILL_NAME/SKILL.md"

mkdir -p docs/quality-reports

report() { echo "$@" >> "$REPORT_FILE"; }

report "# ${SKILL_NAME} 自动化检查报告"
report ""
report "检查时间: $(date)"
report ""

if [ ! -f "$SKILL_FILE" ]; then
  report "## 错误"
  report "SKILL.md 文件不存在: $SKILL_FILE"
  echo "检查完成，报告已保存到 $REPORT_FILE"
  exit 1
fi

report "## 检查结果"
report ""

# Frontmatter
report "### Frontmatter检查"
for field in name description when_to_use compatibility; do
  if grep -q "^${field}:" "$SKILL_FILE"; then
    report "- [x] ${field} 字段存在"
  else
    report "- [ ] ${field} 字段缺失"
  fi
done

# Standard sections
report "### 章节结构检查"
for section in "核心原则" "何时使用" "方法论" "硬约束" "关键要点"; do
  if grep -q "^## ${section}" "$SKILL_FILE"; then
    report "- [x] ${section} 章节存在"
  else
    report "- [ ] ${section} 章节缺失"
  fi
done

# Agent prompt section
if grep -q "^## Agent 提示词" "$SKILL_FILE"; then
  report "- [x] Agent 提示词章节存在"
else
  report "- [ ] Agent 提示词章节缺失"
fi

# Optional sections
report "### 可选章节检查"
for section in "常见陷阱" "边界情况处理" "最佳实践" "跨skill交接点" "自动化检查" "相关模板"; do
  if grep -q "^## ${section}" "$SKILL_FILE"; then
    report "- [x] ${section} 章节存在"
  fi
done

# Example counts
example_count=$(grep -c "^### 示例\|^#### 示例\|^## 示例" "$SKILL_FILE" || echo "0")
report "### 示例统计"
report "- 示例数量: $example_count"

report ""
report "## 检查完成"

echo "检查完成，报告已保存到 $REPORT_FILE"
