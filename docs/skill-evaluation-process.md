# Skills质量评估流程

## 评估流程概述

本流程定义了如何系统评估harness体系中skills的质量，包括自动化检查和人工评审两部分。

## 评估准备

### 1. 环境准备

**必需工具**：
- 文件系统访问权限
- Markdown解析器
- JSON处理能力

**评估数据**：
- 待评估的SKILL.md文件
- 参考skill（默认使用harness-prompt-optimizer）
- 评估维度体系（见`skill-quality-dimensions.md`）

### 2. 评估输入

**必需输入**：
- `skills_directory`: skills目录路径
- `target_skill`: 待评估的skill名称

**可选输入**：
- `reference_skill`: 参考skill名称（默认：harness-prompt-optimizer）
- `evaluation_mode`: 评估模式（详细/摘要/评分卡）
- `output_format`: 输出格式（JSON/Markdown/HTML）

## 自动化检查流程

### 步骤1：文件结构验证

**检查内容**：
1. 检查SKILL.md文件是否存在
2. 检查文件是否可读
3. 检查文件编码（UTF-8）

**检查命令**：
```bash
# 检查文件存在性
test -f skills/<skill-name>/SKILL.md && echo "文件存在" || echo "文件不存在"

# 检查文件可读性
test -r skills/<skill-name>/SKILL.md && echo "文件可读" || echo "文件不可读"

# 检查文件编码
file -I skills/<skill-name>/SKILL.md
```

**评分规则**：
- 文件存在且可读：+2分
- 文件编码正确（UTF-8）：+1分

### 步骤2：Frontmatter验证

**检查内容**：
1. frontmatter是否存在
2. 必需字段完整性
3. 字段格式正确性

**检查命令**：
```bash
# 提取frontmatter
sed -n '/^---$/,/^---$/p' skills/<skill-name>/SKILL.md

# 检查必需字段
grep -q "^name:" skills/<skill-name>/SKILL.md && echo "name字段存在" || echo "name字段缺失"
grep -q "^description:" skills/<skill-name>/SKILL.md && echo "description字段存在" || echo "description字段缺失"
grep -q "^when_to_use:" skills/<skill-name>/SKILL.md && echo "when_to_use字段存在" || echo "when_to_use字段缺失"
grep -q "^compatibility:" skills/<skill-name>/SKILL.md && echo "compatibility字段存在" || echo "compatibility字段缺失"
```

**评分规则**：
- frontmatter存在：+1分
- name字段存在且非空：+1分
- description字段存在且≥20字符：+1分
- when_to_use字段存在且非空：+1分
- compatibility字段存在且非空：+1分

### 步骤3：章节结构验证

**检查内容**：
1. 标准章节是否存在
2. 章节层级是否正确
3. 章节内容是否为空

**检查命令**：
```bash
# 检查标准章节
grep -q "^## 核心原则" skills/<skill-name>/SKILL.md && echo "核心原则章节存在" || echo "核心原则章节缺失"
grep -q "^## 何时使用" skills/<skill-name>/SKILL.md && echo "何时使用章节存在" || echo "何时使用章节缺失"
grep -q "^## 何时不该用" skills/<skill-name>/SKILL.md && echo "何时不该用章节存在" || echo "何时不该用章节缺失"
grep -q "^## 方法论" skills/<skill-name>/SKILL.md && echo "方法论章节存在" || echo "方法论章节缺失"
grep -q "^## 关键要点" skills/<skill-name>/SKILL.md && echo "关键要点章节存在" || echo "关键要点章节缺失"
grep -q "^## 常见陷阱" skills/<skill-name>/SKILL.md && echo "常见陷阱章节存在" || echo "常见陷阱章节缺失"
```

**评分规则**：
- 每个标准章节存在：+0.5分（最高3分）
- 章节层级正确：+1分
- 章节内容非空：+1分

### 步骤4：Markdown格式验证

**检查内容**：
1. 标题层级是否正确
2. 列表格式是否规范
3. 代码块格式是否正确
4. 链接格式是否正确

**检查命令**：
```bash
# 检查标题层级
grep -n "^#" skills/<skill-name>/SKILL.md | head -10

# 检查列表格式
grep -n "^- " skills/<skill-name>/SKILL.md | head -10

# 检查代码块
grep -n "^```" skills/<skill-name>/SKILL.md | head -10
```

**评分规则**：
- 标题层级正确：+1分
- 列表格式规范：+0.5分
- 代码块格式正确：+0.5分
- 链接格式正确：+0.5分

## 人工评审流程

### 评审1：内容质量评审

**评审标准**：
1. 核心原则清晰明确
2. 方法论步骤详细可执行
3. 示例和用例具体实用
4. 无歧义表述
5. 无冗余信息

**评审方法**：
1. 阅读核心原则章节
2. 评估方法论的可执行性
3. 检查示例的实用性
4. 识别歧义和冗余

**评分规则**：
- 优秀（9-10分）：内容清晰、完整、可直接执行
- 良好（7-8分）：内容基本清晰完整
- 一般（5-6分）：内容部分清晰，存在歧义
- 较差（3-4分）：内容模糊，难以执行
- 不合格（0-2分）：内容混乱，无法使用

### 评审2：可用性评审

**评审标准**：
1. 触发条件清晰明确
2. 执行流程明确
3. 输出格式规范
4. 使用示例具体

**评审方法**：
1. 评估"何时使用"场景的具体性
2. 评估"何时不该用"场景的清晰度
3. 评估执行流程的明确性
4. 评估输出格式的规范性

**评分规则**：
- 优秀（9-10分）：触发条件清晰，执行流程明确，输出格式规范
- 良好（7-8分）：基本可用，个别环节可优化
- 一般（5-6分）：可用但存在困惑点
- 较差（3-4分）：难以使用，需要大量猜测
- 不合格（0-2分）：几乎无法使用

### 评审3：设计模式评审

**评审标准**：
1. 遵循harness体系设计模式
2. 结构模块化清晰
3. 允许未来扩展
4. 与其他skills风格一致

**评审方法**：
1. 与参考skill对比设计模式
2. 评估结构的模块化程度
3. 评估可扩展性
4. 评估与其他skills的一致性

**评分规则**：
- 优秀（9-10分）：设计优秀，模块化清晰，可扩展，高度一致
- 良好（7-8分）：设计良好，基本符合体系设计模式
- 一般（5-6分）：设计一般，部分符合体系设计模式
- 较差（3-4分）：设计较差，与体系设计模式不一致
- 不合格（0-2分）：设计混乱，无模块化

### 评审4：文档质量评审

**评审标准**：
1. 示例丰富度
2. 说明清晰度
3. 错误处理指导
4. 故障排除建议

**评审方法**：
1. 统计示例数量
2. 评估说明清晰度
3. 检查错误处理指导
4. 检查故障排除建议

**评分规则**：
- 优秀（9-10分）：文档优秀，示例丰富，说明清晰，包含错误处理
- 良好（7-8分）：文档良好，基本够用
- 一般（5-6分）：文档一般，缺少部分示例或说明
- 较差（3-4分）：文档较差，难以理解
- 不合格（0-2分）：几乎无文档

### 评审5：Agent提示词质量评审

**评审标准**：
1. 角色定义清晰
2. 核心能力明确
3. 执行流程详细
4. 约束条件合理
5. 输出规范明确

**评审方法**：
1. 评估角色定义的清晰度
2. 评估核心能力的明确性
3. 评估执行流程的详细程度
4. 评估约束条件的合理性
5. 评估输出规范的明确性

**评分规则**：
- 优秀（9-10分）：Agent提示词优秀，角色清晰，流程明确，约束合理
- 良好（7-8分）：Agent提示词良好，基本可用
- 一般（5-6分）：Agent提示词一般，存在困惑点
- 较差（3-4分）：Agent提示词较差，难以执行
- 不合格（0-2分）：几乎无Agent提示词

## 评估报告生成

### 报告结构

```json
{
  "skill_name": "skill名称",
  "evaluation_date": "评估日期",
  "evaluator": "评估者",
  "evaluation_mode": "评估模式",
  "total_score": 8.5,
  "grade": "A",
  "dimensions": {
    "structure_completeness": {
      "score": 9.0,
      "weight": 0.20,
      "automated_score": 8.0,
      "manual_score": 10.0,
      "comments": "结构完整，符合规范"
    },
    "content_quality": {
      "score": 8.5,
      "weight": 0.25,
      "comments": "内容清晰，可执行性强"
    },
    "usability": {
      "score": 8.0,
      "weight": 0.20,
      "comments": "可用性良好，触发条件清晰"
    },
    "design_patterns": {
      "score": 9.0,
      "weight": 0.15,
      "comments": "设计优秀，模块化清晰"
    },
    "documentation_quality": {
      "score": 8.0,
      "weight": 0.10,
      "comments": "文档良好，示例足够"
    },
    "agent_prompt_quality": {
      "score": 8.5,
      "weight": 0.10,
      "comments": "Agent提示词质量良好"
    }
  },
  "automated_checks": {
    "file_structure": {
      "status": "PASS",
      "score": 3,
      "max_score": 3,
      "details": "文件存在，可读，编码正确"
    },
    "frontmatter": {
      "status": "PASS",
      "score": 5,
      "max_score": 5,
      "details": "所有必需字段存在且格式正确"
    },
    "section_structure": {
      "status": "PASS",
      "score": 4,
      "max_score": 5,
      "details": "缺少'常见陷阱'章节"
    },
    "markdown_format": {
      "status": "PASS",
      "score": 2.5,
      "max_score": 3,
      "details": "格式基本正确，个别链接格式可优化"
    }
  },
  "manual_review": {
    "content_quality": {
      "score": 8.5,
      "reviewer_comments": "内容清晰，可执行性强"
    },
    "usability": {
      "score": 8.0,
      "reviewer_comments": "可用性良好，触发条件清晰"
    },
    "design_patterns": {
      "score": 9.0,
      "reviewer_comments": "设计优秀，模块化清晰"
    },
    "documentation_quality": {
      "score": 8.0,
      "reviewer_comments": "文档良好，示例足够"
    },
    "agent_prompt_quality": {
      "score": 8.5,
      "reviewer_comments": "Agent提示词质量良好"
    }
  },
  "issues": [
    {
      "dimension": "章节结构",
      "severity": "LOW",
      "description": "缺少'常见陷阱'章节",
      "suggestion": "建议添加'常见陷阱'章节，列出常见问题和解决方案",
      "location": "SKILL.md",
      "automated": true
    },
    {
      "dimension": "内容质量",
      "severity": "LOW",
      "description": "个别表述可更清晰",
      "suggestion": "建议优化措辞，提高可读性",
      "location": "方法论章节",
      "automated": false
    }
  ],
  "recommendations": [
    "建议添加'常见陷阱'章节",
    "建议增加更多使用示例",
    "建议优化触发条件描述"
  ],
  "comparison_with_reference": {
    "reference_skill": "harness-prompt-optimizer",
    "strengths": ["结构更简洁", "触发条件更清晰"],
    "weaknesses": ["缺少示例", "文档不够详细"],
    "suggestions": ["参考prompt-optimizer的示例设计", "补充更多使用场景"]
  }
}
```

## 评估结果应用

### 1. 质量等级应用

**A级（9-10分）**：
- 可作为参考范例
- 可用于培训新skills
- 可在文档中推荐

**B级（7-8分）**：
- 符合标准，可正常使用
- 可进行小幅优化
- 可作为改进基础

**C级（5-6分）**：
- 需要改进
- 制定改进计划
- 定期重新评估

**D级（3-4分）**：
- 需要重大改进
- 暂停使用直到改进完成
- 提供具体改进指导

**F级（0-2分）**：
- 不合格，需要重写
- 从skills集合中移除
- 提供重写指导

### 2. 改进建议应用

**短期改进（1-2天）**：
- 修复明显问题
- 补充缺失内容
- 优化格式

**中期改进（1周）**：
- 重新设计部分内容
- 增加示例和用例
- 优化用户体验

**长期改进（1个月）**：
- 重新评估设计模式
- 考虑是否需要拆分或合并
- 评估是否需要新的skill

## 评估自动化

### 1. 自动化脚本

**检查脚本示例**：
```bash
#!/bin/bash
# skill-quality-check.sh

SKILL_DIR=$1
SKILL_NAME=$2

# 检查文件存在性
if [ ! -f "$SKILL_DIR/$SKILL_NAME/SKILL.md" ]; then
    echo "错误：SKILL.md文件不存在"
    exit 1
fi

# 检查frontmatter
echo "检查frontmatter..."
grep -q "^name:" "$SKILL_DIR/$SKILL_NAME/SKILL.md" && echo "✓ name字段存在" || echo "✗ name字段缺失"
grep -q "^description:" "$SKILL_DIR/$SKILL_NAME/SKILL.md" && echo "✓ description字段存在" || echo "✗ description字段缺失"
grep -q "^when_to_use:" "$SKILL_DIR/$SKILL_NAME/SKILL.md" && echo "✓ when_to_use字段存在" || echo "✗ when_to_use字段缺失"
grep -q "^compatibility:" "$SKILL_DIR/$SKILL_NAME/SKILL.md" && echo "✓ compatibility字段存在" || echo "✗ compatibility字段缺失"

# 检查章节结构
echo "检查章节结构..."
grep -q "^## 核心原则" "$SKILL_DIR/$SKILL_NAME/SKILL.md" && echo "✓ 核心原则章节存在" || echo "✗ 核心原则章节缺失"
grep -q "^## 何时使用" "$SKILL_DIR/$SKILL_NAME/SKILL.md" && echo "✓ 何时使用章节存在" || echo "✗ 何时使用章节缺失"
grep -q "^## 何时不该用" "$SKILL_DIR/$SKILL_NAME/SKILL.md" && echo "✓ 何时不该用章节存在" || echo "✗ 何时不该用章节缺失"
grep -q "^## 方法论" "$SKILL_DIR/$SKILL_NAME/SKILL.md" && echo "✓ 方法论章节存在" || echo "✗ 方法论章节缺失"
grep -q "^## 关键要点" "$SKILL_DIR/$SKILL_NAME/SKILL.md" && echo "✓ 关键要点章节存在" || echo "✗ 关键要点章节缺失"
grep -q "^## 常见陷阱" "$SKILL_DIR/$SKILL_NAME/SKILL.md" && echo "✓ 常见陷阱章节存在" || echo "✗ 常见陷阱章节缺失"

echo "检查完成"
```

### 2. 集成到CI/CD

**GitHub Actions示例**：
```yaml
name: Skill Quality Check

on:
  push:
    paths:
      - 'skills/**/SKILL.md'
  pull_request:
    paths:
      - 'skills/**/SKILL.md'

jobs:
  quality-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Check skill quality
        run: |
          for skill_dir in skills/*/; do
            skill_name=$(basename "$skill_dir")
            echo "检查 $skill_name..."
            bash scripts/skill-quality-check.sh skills "$skill_name"
          done
```

## 评估报告模板

### 详细报告模板

```markdown
# Skills质量评估报告

## 基本信息

- **评估日期**：2026-07-02
- **评估者**：opencode
- **评估模式**：详细评估
- **评估范围**：所有skills

## 评估结果概览

| 维度 | 得分 | 权重 | 加权得分 |
|------|------|------|----------|
| 结构完整性 | 8.5 | 20% | 1.7 |
| 内容质量 | 8.0 | 25% | 2.0 |
| 可用性 | 7.5 | 20% | 1.5 |
| 设计模式 | 9.0 | 15% | 1.35 |
| 文档质量 | 8.0 | 10% | 0.8 |
| Agent提示词质量 | 8.5 | 10% | 0.85 |
| **总分** | - | - | **8.2** |

## 等级分布

- A级（9-10分）：2个skills
- B级（7-8分）：8个skills
- C级（5-6分）：2个skills
- D级（3-4分）：0个skills
- F级（0-2分）：0个skills

## 详细评估结果

### harness-prompt-optimizer

**总分**：9.2分（A级）

**维度得分**：
- 结构完整性：9.5分
- 内容质量：9.0分
- 可用性：9.0分
- 设计模式：9.5分
- 文档质量：9.0分
- Agent提示词质量：9.0分

**优势**：
1. 结构完整，符合harness体系规范
2. 内容清晰，可执行性强
3. 设计优秀，模块化清晰
4. 示例丰富，文档详细

**改进建议**：
1. 可增加更多边界情况示例
2. 可优化触发条件描述

### harness-bootstrap

**总分**：8.5分（B级）

**维度得分**：
- 结构完整性：9.0分
- 内容质量：8.5分
- 可用性：8.0分
- 设计模式：8.5分
- 文档质量：8.0分
- Agent提示词质量：8.5分

**优势**：
1. 结构完整，符合规范
2. 内容清晰，步骤明确
3. 设计良好，模块化清晰

**改进建议**：
1. 可增加更多使用示例
2. 可优化错误处理指导
3. 可补充故障排除建议

## 总体建议

### 短期改进（1-2天）

1. 为所有skills添加"常见陷阱"章节
2. 补充缺失的使用示例
3. 优化触发条件描述

### 中期改进（1周）

1. 统一所有skills的文档风格
2. 增加错误处理和故障排除指导
3. 优化Agent提示词的清晰度

### 长期改进（1个月）

1. 考虑是否需要新的评估维度
2. 评估是否需要拆分或合并skills
3. 建立skills质量基准线

## 附录

### 评估维度权重说明

| 维度 | 权重 | 理由 |
|------|------|------|
| 结构完整性 | 20% | 基础要求，影响可用性 |
| 内容质量 | 25% | 核心价值，直接影响使用效果 |
| 可用性 | 20% | 用户体验，影响采用率 |
| 设计模式 | 15% | 长期维护，影响扩展性 |
| 文档质量 | 10% | 辅助价值，影响学习曲线 |
| Agent提示词质量 | 10% | 执行质量，影响自动化效果 |

### 评估工具清单

1. 文件系统检查工具
2. Markdown解析器
3. JSON处理库
4. 自动化测试脚本
5. CI/CD集成工具

---
最后更新: 2026-07-02
```

---
最后更新: 2026-07-02