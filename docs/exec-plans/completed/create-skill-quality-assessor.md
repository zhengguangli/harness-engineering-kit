# 创建skills质量评估skill

- 状态: completed
- 创建日期: 2026-07-02
- 最近更新: 2026-07-02
- 关联 PR / issue: 暂无
- 负责 agent / 人: opencode

## 目标

创建一个名为`harness-skill-quality-assessor`的skill，能够系统评估harness体系中所有skills的质量，提供可量化的评估报告和改进建议。

## 范围 / 非目标

**范围内:**
- 分析现有skills的结构和内容模式
- 参考harness-prompt-optimizer skill的设计模式
- 定义skills质量评估维度和评分标准
- 设计可执行的评估流程
- 生成完整的SKILL.md文件

**明确不做(非目标):**
- 不修改现有skills的内容
- 不创建自动化测试脚本
- 不设计UI界面
- 不处理skills之间的依赖关系

## 步骤

- [ ] 步骤 1 — 分析现有skills结构，识别共同模式和规范
- [ ] 步骤 2 — 深度分析harness-prompt-optimizer skill，提取设计模式
- [ ] 步骤 3 — 定义skills质量评估维度体系（5-7个维度）
- [ ] 步骤 4 — 设计评估流程和评分规则
- [ ] 步骤 5 — 创建SKILL.md模板和文档结构
- [ ] 步骤 6 — 编写评估示例和用例
- [ ] 步骤 7 — 验证生成的skill符合harness体系规范

## 决策日志

| 日期 | 决策 | 理由 | 被否决的备选方案 |
|---|---|---|---|
| 2026-07-02 | 使用harness-prompt-optimizer作为参考skill | 该skill结构完整，设计模式清晰，适合作为质量评估的参考 | 使用harness-authoring作为参考，但该skill更侧重于创建而非评估 |
| 2026-07-02 | 采用六区块prompt结构设计评估框架 | 符合harness体系的设计模式，便于agent理解和执行 | 使用传统评估框架，但可能不符合harness体系的设计理念 |

## 验收标准

- [ ] 生成的SKILL.md文件包含完整的frontmatter（name, description, when_to_use, compatibility等）
- [ ] 评估维度包含至少5个可量化的评估维度
- [ ] 每个评估维度有明确的评分标准（0-10分制）
- [ ] 评估流程包含自动化检查和人工评审两部分
- [ ] 生成的skill能够评估现有12个skills的质量
- [ ] 评估报告包含具体的问题列表和改进建议

## 风险 / 已知未知

- 评估维度的量化标准可能需要根据实际评估结果进行调整
- 不同skills的特殊性可能导致评估标准需要灵活处理
- 评估流程的自动化程度可能受限于现有工具支持

## 变更记录

- 2026-07-02: 创建计划