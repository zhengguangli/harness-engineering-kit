#!/bin/bash
# 技能质量自动化检查脚本

SKILLS_DIR="./skills"
REPORT_FILE="docs/quality-reports/round1-automated-check.md"

# 创建报告目录
mkdir -p docs/quality-reports

# 开始报告
echo "# 第一轮自动化检查报告" > "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "检查时间: $(date)" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# 获取所有skills
SKILLS=($(ls -d "$SKILLS_DIR"/harness-* 2>/dev/null | xargs -n 1 basename))

echo "## 检查概览" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "- 总skills数: ${#SKILLS[@]}" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# 检查每个skill
for skill in "${SKILLS[@]}"; do
    echo "## $skill" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    
    SKILL_FILE="$SKILLS_DIR/$skill/SKILL.md"
    
    # 检查文件存在性
    if [ -f "$SKILL_FILE" ]; then
        echo "### 文件结构" >> "$REPORT_FILE"
        echo "- [x] SKILL.md 文件存在" >> "$REPORT_FILE"
        
        # 检查frontmatter
        echo "### Frontmatter检查" >> "$REPORT_FILE"
        
        if grep -q "^name:" "$SKILL_FILE"; then
            echo "- [x] name 字段存在" >> "$REPORT_FILE"
        else
            echo "- [ ] name 字段缺失" >> "$REPORT_FILE"
        fi
        
        if grep -q "^description:" "$SKILL_FILE"; then
            echo "- [x] description 字段存在" >> "$REPORT_FILE"
            # 检查description长度
            desc_line=$(grep "^description:" "$SKILL_FILE")
            desc_content=$(echo "$desc_line" | sed 's/^description: *//')
            if [ ${#desc_content} -ge 20 ]; then
                echo "- [x] description 长度 ≥ 20 字符" >> "$REPORT_FILE"
            else
                echo "- [ ] description 长度 < 20 字符" >> "$REPORT_FILE"
            fi
        else
            echo "- [ ] description 字段缺失" >> "$REPORT_FILE"
        fi
        
        if grep -q "^when_to_use:" "$SKILL_FILE"; then
            echo "- [x] when_to_use 字段存在" >> "$REPORT_FILE"
        else
            echo "- [ ] when_to_use 字段缺失" >> "$REPORT_FILE"
        fi
        
        if grep -q "^compatibility:" "$SKILL_FILE"; then
            echo "- [x] compatibility 字段存在" >> "$REPORT_FILE"
        else
            echo "- [ ] compatibility 字段缺失" >> "$REPORT_FILE"
        fi
        
        # 检查标准章节
        echo "### 章节结构检查" >> "$REPORT_FILE"
        
        if grep -q "^## 核心原则" "$SKILL_FILE"; then
            echo "- [x] 核心原则章节存在" >> "$REPORT_FILE"
        else
            echo "- [ ] 核心原则章节缺失" >> "$REPORT_FILE"
        fi
        
        if grep -q "^## 何时使用" "$SKILL_FILE"; then
            echo "- [x] 何时使用章节存在" >> "$REPORT_FILE"
        else
            echo "- [ ] 何时使用章节缺失" >> "$REPORT_FILE"
        fi
        
        if grep -q "^## 何时不该用" "$SKILL_FILE"; then
            echo "- [x] 何时不该用章节存在" >> "$REPORT_FILE"
        else
            echo "- [ ] 何时不该用章节缺失" >> "$REPORT_FILE"
        fi
        
        if grep -q "^## 方法论" "$SKILL_FILE"; then
            echo "- [x] 方法论章节存在" >> "$REPORT_FILE"
        else
            echo "- [ ] 方法论章节缺失" >> "$REPORT_FILE"
        fi
        
        if grep -q "^## 关键要点" "$SKILL_FILE"; then
            echo "- [x] 关键要点章节存在" >> "$REPORT_FILE"
        else
            echo "- [ ] 关键要点章节缺失" >> "$REPORT_FILE"
        fi
        
        if grep -q "^## 常见陷阱" "$SKILL_FILE"; then
            echo "- [x] 常见陷阱章节存在" >> "$REPORT_FILE"
        else
            echo "- [ ] 常见陷阱章节缺失" >> "$REPORT_FILE"
        fi
        
        if grep -q "^## Agent 提示词" "$SKILL_FILE"; then
            echo "- [x] Agent 提示词章节存在" >> "$REPORT_FILE"
        else
            echo "- [ ] Agent 提示词章节缺失" >> "$REPORT_FILE"
        fi
        
        # 检查文件行数
        line_count=$(wc -l < "$SKILL_FILE")
        echo "### 文件统计" >> "$REPORT_FILE"
        echo "- 总行数: $line_count" >> "$REPORT_FILE"
        
    else
        echo "### 文件结构" >> "$REPORT_FILE"
        echo "- [ ] SKILL.md 文件不存在" >> "$REPORT_FILE"
    fi
    
    echo "" >> "$REPORT_FILE"
done

echo "自动化检查完成，报告已保存到 $REPORT_FILE"