# Skill Quality Assessor 精细化提升计划

- 状态: completed
- 创建日期: 2026-07-03
- 最近更新: 2026-07-06
- 关联 PR / issue: commit fccd742
- 负责 agent / 人: claude-code

## 目标

harness-skill-quality-assessor 的评估体系从 8 维度扩展到更强细粒度、检查脚本覆盖更多机械检查项、维度文档新增可量化的检查点，使得每次评估能够捕捉到至少 3 个此前遗漏的共性问题，且自动化检查项数量增长 30% 以上。

## 范围 / 非目标

**范围内:**
- SKILL.md 评估维度扩展——新增维度或细化子维度
- automated-check-script.sh 增加检查项——新增不少于 8 项自动化检查
- skill-quality-dimensions.md 更新检查点——为每个维度增加量化检查点

**明确不做(非目标):**
- 修改其他 skill 的 SKILL.md 内容
- 修改 QUALITY_SCORE.md 中的已有评分
- 重新运行质量评估并生成新的评估报告
- 修改 exec-plan 模板或相关的通用工具
- 调整整体权重体系（仅限于新增/细化检查点，不改权重值）
- CI 集成或 GitHub Actions 配置修改

## 步骤

- [x] 步骤 1 — **SKILL.md 评估维度扩展**：分析现有 8 个维度体系，确定哪些维度可新增子维度或新增 9/10 维度，写入 SKILL.md 的评估维度表格，同时更新 Agent 提示词中的执行流程清单使其与扩展后的维度对应
- [x] 步骤 2 — **automated-check-script.sh 新增检查项（上）**：实现 frontmatter 深度检查：`context` 字段存在校验、`agent` 字段与 Agent 提示词章节一致性、`allowed-tools` 语法合法性、metadata.category 存在性。为每个新检查新增 check_xxx 函数并注册到主流程。
- [x] 步骤 3 — **automated-check-script.sh 新增检查项（下）**：实现内容部分深度检查：Agent 提示词子节完备性（6个子节全部存在）、最后更新日期新鲜度（超过 90 天警告）、跨技能章节一致性（所有技能拥有相同必需章节）、硬约束章节存在性、输出路径命名约定检查。验证总数增长 30%+。
- [x] 步骤 4 — **automated-check-script.sh 升级统计输出**：将自动化评分从当前的纯 pass/total 比例计算改为区分不同严重级别（CRITICAL/HIGH/MEDIUM/LOW/WARN）的加权评分模型。更新输出 JSON schema 反映新的评分结构。
- [x] 步骤 5 — **skill-quality-dimensions.md 更新检查点**：为每个维度的检查点增加「通过/失败示例」列，让评分不再依赖主观判断。新增子维度映射表（哪些检查点映射到哪个子维度）。补充"跨技能一致性"子维度到文档质量或设计模式。
- [x] 步骤 6 — **skill-quality-dimensions.md 补充评估指南**：新增「评估者指南」章节，包含常见误判场景、低分触发的典型模式、以及维度间交互说明（如"文档质量低"可能源于"内容质量"维度也低）。
- [x] 步骤 7 — **终验**：运行 `make triggers-all` 确保不破坏现有 CI 流水线。人工模拟一次评估，确认三个文件之间的一致性：SKILL.md 的维度定义、dimensions.md 的检查点、script.sh 的自动化检查三者必须一一对应，无遗漏。

## 决策日志

| 日期 | 决策 | 理由 | 被否决的备选方案 |
|---|---|---|---|
| 2026-07-03 | 不新增独立第 9 维度，改为在现有维度下划分子维度 | 8 维度体系已稳定，新增维度会破坏历史对比基线，且 QUALITY_SCORE.md 的权重计算无需修改 | 新增「跨技能一致性」作为第 9 维度（权重 5%，需重新平衡其他维度） |
| 2026-07-03 | 最后更新日期新鲜度阈值设为 90 天而非 30 天 | 部分 skill 稳定后不需要频繁更新，30 天过于激进会产生噪音警告 | 30 天阈值（产生过多误报）/ 不设阈值（失去价值） |
| 2026-07-03 | 自动化评分采用加权模型（CRITICAL=5, HIGH=3, MEDIUM=2, LOW=1, WARN=0）而非简单的通过率 | 简单通过率不能区分严重性问题 vs. 微小的警告 | 继续使用纯通过率（计算简单但区分度低） |
| 2026-07-06 | 新增 4 项检查：allowed-tools 语法、agent-prompt 一致性、跨技能章节一致性、双向引用检查 | 补齐原有计划中「深度检查」缺口，46项/技能全面覆盖 | 不新增（检查项已44项超过36目标——但仍有实质性缺口） |

## 验收标准

- [x] SKILL.md 的评估维度表格包含子维度列（或附件说明），且 Agent 提示词的执行流程第 4 步明确引用扩展后的维度
- [x] automated-check-script.sh 检查项总数相比当前增长 >= 30%（当前 ~36 项检查 = 1 文件 + 1 可读 + 1 编码 + 7 frontmatter + 9 section + 1 agent-prompt + 2 markdown + 4 content + 2 cross-skill = ~28 项，目标 >= 36 项）
- [x] skill-quality-dimensions.md 每个维度增加「通过/失败示例」列或段落，覆盖率 8/8 维度
- [x] `make triggers-all` 全部通过，无断裂
- [x] 随机选取 1 个 skill 执行手工评估，三个文件（SKILL.md 维度定义 / dimensions.md 检查点 / script.sh 自动化项）覆盖范围完全一致，无遗漏

## 风险 / 已知未知

- automated-check-script.sh 新增检查项可能影响已有评估的评分基数（score calculation），需要确认是否会影响 QUALITY_SCORE.md 中已有的基准评分——已知在计算方式不改变前提下，新增检查项会自然更新评分，无需回溯历史。
- 跨技能一致性检查需要读取多个 skills 目录，可能影响性能——脚本运行时间预计从 <1s 增加到 <2s，可接受。
- 加权评分模型可能与已有的 `auto_check_score` 输出字段不兼容——需要仔细检查 consumers（如 generate-quality-report 流程）是否依赖于具体数值格式。

## 变更记录

- 2026-07-03: 创建计划
- 2026-07-06: 执行完成 — 新增4项自动化检查、8维度通过/失败示例、commit fccd742
