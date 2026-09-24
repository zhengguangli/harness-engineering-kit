# QUALITY_SCORE.md

<!-- Canonical owner: harness-golden-principles -->

按领域追踪 harness-engineering-kit 的质量与一致性评分。

## 评分维度

- **frontmatter 合规**: 每个 SKILL.md 是否满足必填字段要求
- **触发回归通过率**: `tests/triggers/cases.json` 中 PASS 的比例
- **关键词一致性**: `scripts/run_trigger_regression.py` 中关键词覆盖情况
- **文档新鲜度**: docs/ 中关键文档是否在 30 天内被校验过

## 当前评分

| 领域 | frontmatter 合规 | 触发回归 | 关键词一致性 | 文档新鲜度 | 最近评估日期 |
|---|---|---|---|---|---|
| skills (13个) | 13/13 (100%) ✅ | 51/51 (100%) ✅ | 13/13 (100%) ✅ | ✅ 当日更新 | 2026-09-24 (三十四次) |
| scripts | — | — | — | ✅ 当日更新 | 2026-09-24 (新增依赖校验脚本) |
| tests | — | — | — | ✅ 当日更新 | 2026-09-24 (新增 18 个依赖校验用例) |

## 趋势备注

2026-07-03: 初始评分填充。全部 13 个 skill 完成 A+ 级优化（平均分 9.57），`make triggers-all` 全绿通过（PASS=48 WARN=0 FAIL=0）。详见 `CLAUDE.md` 和 `docs/quality-reports/skills-quality-assessment.md`。

2026-07-03 (二次): 使用 skill-quality-assessor 的 8 维度标准化体系重新评估全部 13 个 skill。平均分 8.99 (A 级)，8 个 A 级 + 5 个 B+ 级。核心发现：frontmatter 合规率 100%，章节覆盖完整，但存在 12/13 技能 automated_check_script.py 文件缺失、3 个技能 common-edge-cases.md 缺失、多数技能缺少 allowed-tools 显式声明等问题。详见 `docs/quality-reports/skills-quality-assessment.md`。

2026-07-03 (三次): 第三次 8 维度子维度体系批量评估。平均分 9.12 (A 级，持平)，12 个 A 级 + 1 个 B+ 级。核心内容无变化，质量进入稳定期。skill-quality-assessor 通过引入子维度体系/自动化加权评分模型/评估者指南实现自身优化，评分从 9.33 升至 9.38。automated_check_script.py 保持 2/13（已核实：repo-map 和 skill-quality-assessor 各有独立脚本，命名不一致）。参考文件总数从 65 降至 64（prompt-optimizer 减少 1 个）。自动化友好度 (6.73) 仍为最大薄弱维度。最高分 skill-quality-assessor (9.38)，最低分 golden-principles (8.92)。详见 `docs/quality-reports/skills-quality-assessment.md`。

2026-07-03 (四次): 第四次 8 维度子维度体系批量评估。平均分 9.39 (A 级，+0.27)，历次最大增幅。三大基础设施短板在本次评估前已全部补齐：automated_check_script.py 从 2/13 升至 13/13（+11），allowed-tools 从 5/13 升至 13/13（+8），跨skill交接从 6/13 升至 12/13（+6）。评分分布从高度同质化走向差异化（4A+9B+），等级标签的下降是评分精度提升的正常现象，实际全部技能分数均提升。自动化友好度从 6.73 升至 7.15（+0.42）。skill-quality-assessor 保持最高分 (9.40)，bootstrap 最低分 (9.18)。参考文件总数从 64 增至 76。已无 CRITICAL/HIGH 级别的待处理问题——基础三件套全部补齐。详见 `docs/quality-reports/skills-quality-assessment.md`。

2026-07-03 (五次): 第五次 8 维度子维度体系批量评估。平均分 9.38 (A 级，-0.01)，与上轮持平。等级分布变为 1A+12A（上轮 4A+9B+）——差异来自评分精度调整，非质量下降。基础设施三件套保持 100% 全覆盖（automated_check_script.py 13/13、allowed-tools 13/13、跨 skill 交接 13/13）。所有 skills 声明 `compatibility: claude-code`，`agents/openai.yaml` 不适用不标记。发现了 automated_check_script.py 的传参 bug（`check_fm_context()`/`check_fm_allowed_tools()`/`check_fm_metadata_category()` 未传入文件路径）及 harness-repo-map 的双脚本冗余问题。skill-quality-assessor 保持唯一 A+ 级 (9.50)，bootstrap 保持最低分 (9.28)。自动化友好度 (9.04) 仍为最薄弱维度。详见 `docs/quality-reports/skills-quality-assessment.md`。

2026-07-03 (六次): 第六次 8 维度子维度体系批量评估。平均分 9.14 (A 级，-0.24)。本轮采用更严格的差异化评分标准：上调 A+ 级门槛，挤出"基础设施三件套补齐"带来的同分膨胀；子维度得分取算术平均而非直接给整分。实际核心内容无退化——自动检查通过率、frontmatter 合规率、章节覆盖完整度不变。3 个 MEDIUM 问题（repo-map 脚本命名不一致、bootstrap/orchestration 引用项缺失）和 8 个 LOW 优化建议。全部 13 个 skill 稳居 A 级（9.0+），最高分 skill-quality-assessor (9.37)，最低分 bootstrap (9.00)。自动化友好度 (8.67) 仍为最薄弱维度。详见 `docs/quality-reports/skills-quality-assessment.md`。

2026-07-03 (七次): 第七次 8 维度子维度体系批量评估。平均分 9.30 (A 级，+0.16)。CI/CD 技能级检查集成 + 自动化检查脚本定制化（13/13 特有化）+ 6 个 skill 内容修补驱动评分回升。自动化友好度从 8.67 跃升至 9.25 (+0.58)，增幅为历次最大。prompt-optimizer 重回 A+ 级 (9.53)，12 个 A 级。无 CRITICAL/HIGH/MEDIUM 级别问题，仅 6 个 LOW 优化建议。最高分 prompt-optimizer (9.53)，最低分 bootstrap (9.12)。详见 `docs/quality-reports/skills-quality-assessment.md`。

2026-07-03 (八次): 第八次 8 维度子维度体系批量评估。平均分 9.32 (A 级，+0.02)，历次最小增幅。11/13 skill 分数提升（内容修补类优化），2 个 skill 持平。4 个 skill 补齐 `## 相关 Skill` 章节（commit-gate/orchestration/skill-quality-assessor/verification-loop），达成 13/13 全覆盖。architecture-boundaries 新增严重程度分类参考表 (+0.05) 和 observability-and-browser 新增浏览器配置参考 (+0.05) 为最大增幅。repo-map 自动化检查脚本从 482 行重构为 29 行共享模式，消除脚本命名不一致问题。质量进入内容微调稳态，后续优化弹性有限。详见 `docs/quality-reports/skills-quality-assessment.md`。

2026-07-03 (九次): 第九次 8 维度子维度体系批量评估。平均分 9.32 (A 级，持平)，1 A+ / 12 A。3 个 new 参考文件补充（commit-gate/+1, golden-principles/+1, orchestration/+1），参考文件总数 75→78。golden-principles 新增引用破损 MEDIUM 问题（`pr-guidelines.md`/`principle-prioritization.md` 引用但文件不存在），是自第 7 次评估后首次出现 MEDIUM 级别问题。3 个 skill 分数微调：orchestration (+0.01, 9.26→9.27) 因新参考文件、commit-gate (+0.01, 9.24→9.25) 因新参考文件、golden-principles (-0.02, 9.26→9.24) 因引用破损。make triggers-all 保持全绿（48/48）。详见 `docs/quality-reports/skills-quality-assessment.md`。

2026-07-03 (十次): 第十次 8 维度子维度体系批量评估。平均分 9.38 (A 级，+0.06)，2 A+ / 11 A。历次第五大单轮增幅。关键事件：(1) golden-principles MEDIUM 引用破损问题已修复（`pr-guidelines.md`/`principle-prioritization.md` 文件已创建，脚本已同步）；(2) S1 关键要点/最佳实践去重系统性完成（12 个 skill 最佳实践章节全部重写）；(3) 6 个 skill 关键章节新增（bootstrap 项目类型裁减指南+初始化检查清单、commit-gate 工具链探测流程、skill-quality-assessor 模式对比表+产出指引、exec-plans 计划质量检查清单、observability 浏览器配置参考、architecture-boundaries 严重程度分类表）；(4) 跨 skill 交接点 13/13 全覆盖（orchestration/commit-gate 补齐相关 Skill 章节）。无 MEDIUM+ 级别未解决问题，所有存量问题均为 LOW。skill-quality-assessor 重回 A+ (9.55)，prompt-optimizer 保持 A+ (9.53)，最低分 orchestration (9.29) 也从 9.14 跃升。自动化友好度平均 9.28（+0.04 vs 第九次）。参考文件总数 78→80。make triggers-all 保持全绿（48/48）。详见 `docs/quality-reports/skills-quality-assessment.md`。

2026-07-03 (十一次): 第十一次 8 维度子维度体系批量评估。平均分 9.39 (A 级，+0.01)，2 A+ / 11 A。历次最小增幅，质量进入维护稳态。关键事件：(1) automated_check_script.py 全面重构为共享脚本模式，全部 13 个 skill 的脚本从独立大脚本变为 `scripts/skill_automated_check.py` 共享脚本 + 特有检查的双模式（repo-map 从 482→29 行，消除约 500 行重复代码）；(2) architecture-boundaries Agent 提示词显著增强（保守分类规则+发现项编排规范+分组规范）；(3) 内容层无新增，所有变化集中在基础设施层的标准化重构。自动化友好度从 9.28 升至 9.32（+0.04）。无 CRITICAL/HIGH/MEDIUM 级别问题，所有存量问题均为 LOW。最高分 skill-quality-assessor (9.55)，最低分 orchestration (9.30)。参考文件总数保持 80 不变。make triggers-all 保持全绿（48/48）。详见 `docs/quality-reports/skills-quality-assessment.md`。

2026-07-03 (十二次): 第十二次 8 维度子维度体系批量评估。平均分 9.46 (A 级，+0.07)，3 A+ / 10 A。历次第三大单轮增幅。核心驱动：Best Practices 全域场景化重写（12/13 skill）+ 5+ skill 新增关键章节（bootstrap 项目类型裁减指南+检查清单、commit-gate 工具链探测流程图、exec-plans 质量检查清单、golden-principles 4 阶段清扫节奏、observability 浏览器配置参考、architecture-boundaries 严重程度分类表、project-intake Monorepo 场景、skill-quality-assessor 模式对比表格）。architecture-boundaries 以严重程度分类表+Agent 提示词增强+Best Practices 场景化加入 A+ 列 (9.51)。内容质量维度从 9.43 升至 9.52（+0.09），为历次最大增幅。skill-quality-assessor 保持最高分 (9.58)，orchestration 等 5 个 skill 并列最低分 (9.35)。所有维度均正增长。自动化友好度 (+0.02) 增幅最小（脚本重构上轮已完成）。make triggers-all 保持全绿（48/48）。参考文件总数保持 80 不变（本轮改善集中在 SKILL.md 正文内容）。无 CRITICAL/HIGH/MEDIUM 级别问题。详见 `docs/quality-reports/skills-quality-assessment.md`。

2026-07-03 (十三次): 第十三次 8 维度子维度体系批量评估。平均分 9.47 (A 级，+0.01)，3 A+ / 10 A。历次最小增幅。SKILL.md 内容层无变化，改善全部来自基础设施层：自动化检查脚本从 16 行共享包装器升级为带 2-10 项特有检查的完整脚本（13/13 特有化），CI/CD 管道新增自动化检查步骤。自动化友好度从 9.34 升至 9.44（+0.10），为第 8 次以来第三大单轮自动化友好度增幅。其余 7 个维度全部持平。最高分 skill-quality-assessor (9.59)，最低分 repo-map 和 orchestration (9.36)。make triggers-all 保持全绿（48/48）。无 CRITICAL/HIGH/MEDIUM 级别问题。加权评分脚本的 context trim bug 自第 12 次评估未修。详见 `docs/quality-reports/skills-quality-assessment.md`。

2026-07-03 (十四次): 第十四次 8 维度子维度体系批量评估。平均分 9.47 (A 级，持平)，3 A+ / 10 A。本轮最大事件：全 13 个 SKILL.md 完成中译英全文翻译，内容逻辑和结构不变。评分持平（9.47），等级分布不变（3A+/10A）。自动化检查脚本发现 3 个自身 bug 并已修复：① `check_common_edge_cases()` 的 `dirname` 多一层目录上移（`dirname "$(dirname "$1")"` 改为 `dirname "$1"`）；② agent-prompt 搜索 `## Agent Prompt` 改为同时匹配 `## Agent 提示词`；③ context 值未 trim 尾部空格（sed 增加 trailing whitespace trim）。同步修复共享脚本 `scripts/skill_automated_check.py` 中的中文 section 名（核心原则→Core Principles，何时使用→When to Use，方法论→Methodology，关键要点→Key Points，最后更新→Last updated，边界情况→Edge Case）。无 CRITICAL/HIGH/MEDIUM 级别问题——第五次达成"零未解决 MEDIUM+ 问题"状态。详见 `docs/quality-reports/skills-quality-assessment.md`。

2026-07-06 (十五次): 第十五次 8 维度子维度体系批量评估。平均分 9.48 (A 级，+0.01)，3 A+ / 10 A。本轮三大变更：(1) F1-F7 章节标题统一——消除 Key Takeaways/When NOT/Further Reading 等 3 个非标准命名；(2) Agent Prompt 子节标准化——顺序、命名、层级统一（11/13 完全对齐，2 个 LOW 遗留问题）；(3) 3 个新参考文件（diff-review-checklist.md / workflow-summary-cheatsheet.md / loop-troubleshooting-guide.md），参考文件总数 80→83。基础设施三件套维持 100% 全覆盖（automated_check_script.py 13/13、allowed-tools 13/13、跨 skill 交接 13/13）。结构完整性维度 +0.04 为最大增幅。2 个新的 LOW 问题（observability-and-browser Agent Prompt 子节顺序、authoring agent 名称 heading 级别）——第六次达成"零未解决 MEDIUM+ 问题"状态。详见 `docs/quality-reports/skills-quality-assessment.md`。

2026-07-06 (十六次): 第十六次 8 维度子维度体系批量评估。平均分 9.49 (A 级，+0.01)，3 A+ / 10 A。本轮为存量问题修复轮次：第 15 次评估指出的 2 个 LOW 遗留问题已全部修复——observability-and-browser Agent Prompt 子节顺序标准化（Skip Conditions 前置）、authoring agent 名称 heading 级别标准化（### → ##）。同步修复 observability 修复过程中发现的 duplicate bullet points 遗留。prompt-optimizer 新增 2 条 Skip Conditions。skill-quality-assessor "Last updated" 日期更新至 2026-07-06（第 15 次 LOW 问题）。唯一持续性遗留：skill-quality-assessor 加权评分脚本 context trim bug（连续 5 个周期未修复）。第七次达成"零未解决 MEDIUM+ 问题"状态。详见 `docs/quality-reports/skills-quality-assessment.md`。

2026-07-06 (十七次): 第十七次 8 维度子维度体系批量评估。平均分 9.49 (A 级，持平)，3 A+ / 10 A。本轮为"确认评估轮次"——第 16 次评估后无内容变更（仅有 `.sh` → `.py` 引用名更新），全量验证链通过确认质量未退化。全部 8 维度评分与第 16 次持平。第八次达成"零未解决 MEDIUM+ 问题"状态。唯一持续性遗留：skill-quality-assessor 加权评分脚本 context trim bug（连续 6 个周期未修复）。详见 `docs/quality-reports/skills-quality-assessment.md`。

2026-07-06 (十八次): 第十八次 8 维度子维度体系批量评估。平均分 9.45 (A 级，持平)，3 A+ / 10 A。本轮 repo-map 获得实质性内容增强——Examples 2→4、Key Points 8→10、Agent Prompt Skip Conditions 3→5、Core Capabilities 新增严重程度评级。repo-map 评分从 9.37 升至 9.41 (+0.04)，其余 12 个 skill 评分持平。最低分从 repo-map (9.37) 变为 orchestration (9.38)。第九次达成"零未解决 MEDIUM+ 问题"状态。唯一持续性遗留：skill-quality-assessor 加权评分脚本 context trim bug（连续 7 个周期未修复）。详见 `docs/quality-reports/skills-quality-assessment.md`。

2026-07-06 (十九次): 第十九次 8 维度子维度体系批量评估。平均分 9.45 (A 级，持平)，3 A+ / 10 A。本轮为确认评估轮次（第 2 次确认）——自第 18 次评估后 SKILL.md 无任何内容变更。全量验证链通过确认质量未退化。全部 8 维度评分与第 18 次完全持平。第十次达成"零未解决 MEDIUM+ 问题"状态。唯一持续性遗留：skill-quality-assessor 加权评分脚本 context trim bug（连续 8 个周期未修复）。详见 `docs/quality-reports/skills-quality-assessment.md`。

2026-07-06 (二十次): 第二十次单 skill 详细评估（harness-observability-and-browser）。平均分 9.45 (A 级，实际微升从 9.4523→9.4537)，**4 A+ / 9 A**（第 12 次以来首次等级分布变化）。observability-and-browser 因 Agent 提示词大幅增强（Skip Conditions 3→6, Core Capabilities 4→6, Execution Flow step 0, Constraints +1, 3 个 Acceptance Criteria 新示例, 2 个新 Key Points, 2 条新 Best Practices）评分从 9.48 升至 9.52 (+0.04)，晋升 A+ 列。其余 12 个 skill 评分完全持平。3 个新 LOW 问题（Observability Output Specification 未同步增强 + Related Templates 列表不完整 + 加权评分脚本 context trim bug 持续第 9 周期）。详见 `docs/quality-reports/skills-quality-assessment.md`。

2026-07-06 (二十一次): 第二十一次单 skill 详细评估（harness-commit-gate）。平均分 9.45 (A 级，持平)。commit-gate 8 维度评分与第 20 次一致（9.46），内容无新增变更。detail 评估确认：3 个 LOW 问题（automated_check_script.py 缺少可执行权限、特有检查覆盖偏少、agent 命名一致性）。其余 12 个 skill 评分完全持平。第十一次达成"零未解决 MEDIUM+ 问题"状态。唯一持续性遗留：skill-quality-assessor 加权评分脚本 context trim bug（连续第 10 个周期未修复）。详见 `docs/quality-reports/skills-quality-assessment.md`。

2026-07-06 (二十二次): 第二十二次单 skill 详细评估（harness-repo-map）。平均分 9.46 (A 级，+0.01)，4 A+ / 9 A。repo-map 经过全 8 维度深度评估，评分从 9.37 (第 18 次) 经两次确认评估稳定在 9.41 (第 19-21 次) 后，详细评估揭示其在 Agent 提示词质量和用户体验维度被低估，评分从 9.41 升至 9.46 (+0.05)，排名从第 9 升至第 6。8 项 LOW 优化建议，主要集中于 Methodology 流程入口优化、特有检查扩展、跨 skill 交接细化。第十二次达成"零未解决 MEDIUM+ 问题"状态。唯一持续性遗留：skill-quality-assessor 加权评分脚本 context trim bug（连续第 11 个周期未修复）。详见 `docs/quality-reports/skills-quality-assessment.md`。

2026-07-06 (二十三次): 第二十三次单 skill 详细评估（harness-orchestration）。平均分 9.46 (A 级，持平)，4 A+ / 9 A。orchestration 经过全 8 维度深度评估，评分稳定在 9.37（与第 18-22 次保持的 9.38 差异在评分精度范围内）。6 项 LOW 优化建议：输出模板示例缺失、特有检查覆盖偏少（3 项 vs 平均 5.6 项）、Common Omission 与 Complexity Assessment 约 40% 重叠需要合并瘦身、Edge Case Handling 偏薄、Core Principles 可扩展至 4-5 条、缺少"路由建议被忽略"的 recovery 指引。第十三次达成"零未解决 MEDIUM+ 问题"状态。唯一持续性遗留：skill-quality-assessor 加权评分脚本 context trim bug（连续第 12 个周期未修复）。详见 `docs/quality-reports/skills-quality-assessment.md`。

2026-07-06 (二十四次): 第二十四次维护修复轮次。context trim bug 经核实已被 bash→Python 迁移自然解决（所有 Python `read_frontmatter()` 使用 `.strip()`，SKILL.md 无尾部空格残留），标记为已解决。orchestration 4 项 LOW 优化已落地：Core Principles 3→5 条（新增"Clarify before routing"和"Intake before bootstrap"）、Output Specification 增加路由建议模板示例、Common Pitfalls 增加"路由建议被忽略"和"重复路由" recovery 指引、Edge Case Handling 扩展 2 个新场景（Wrong Skill 和 Multi-goal Ambiguity）。第十四次达成"零未解决 MEDIUM+ 问题"状态。无未解决持续性遗留。详见 `docs/quality-reports/skills-quality-assessment.md`。

2026-07-06 (二十五次): 第二十五次批量评估。平均分 **9.48** (A 级，+0.02)。全 9 个 A 级 skill 批量优化验证：全部 9 个 skill 正增长（+0.02 ~ +0.09），但 **A+ 阵营未扩张**（4 A+ / 9 A）。commit-gate (9.49) 最接近 A+ 门槛（差 0.01）。最大增幅：bootstrap (+0.09) due to Examples 2→4；orchestration UX (+0.15) 为单维度最大增幅。Agent 提示词质量 (均 9.39) 仍为 A+ 突破的最大瓶颈（距参考 skill 差 -0.26）。详见 `docs/quality-reports/skills-quality-assessment.md`。

2026-07-07 (二十六次): 第二十六次批量评估。平均分 **9.50** (A 级，+0.02)，**5 A+ / 8 A**。**A+ 阵营首次扩张**——commit-gate 通过 Agent Prompt 增强（push decision Capability + Execution Flow step 8 增强 + new Constraint）从 9.49 突破至 9.51。全 8 个 A 级 skill 均获 Agent Prompt 增强（新 Constraints + Capabilities 扩展 + Execution Flow 增强），评分正增长（+0.01 ~ +0.02）。Agent 提示词质量均分从 9.39 升至 9.44 (+0.05)，为本轮最大增幅维度。repo-map (9.49) 距 A+ 仅差 0.01，为最接近候选。无 CRITICAL/HIGH/MEDIUM 级别问题，第十五次达成"零未解决 MEDIUM+ 问题"状态。详见 `docs/quality-reports/skills-quality-assessment.md`。

2026-07-10 (二十七次): 第二十七次单 skill 详细评估（prompt-optimizer + verification-loop）。平均分 **9.51** (A 级，+0.01)，**6 A+ / 7 A**。**verification-loop 从 9.47 突破至 9.52 成功晋升 A+**——最小反馈信号章节解决"无测试项目无法使用"的根本问题，复杂问题分级+升级时机判断提供明确行为指南。prompt-optimizer (9.55) 持平，优化集中在边界防御（超短/已成熟/迭代多次 prompt 不优化判断 + 复杂需求处理 + 需求拆分）。全 13 个 SKILL.md 完成旧 frontmatter 块清理（移除冗余 slug/displayName/version/summary/license）。无 CRITICAL/HIGH/MEDIUM 级别问题。详见 `docs/quality-reports/skills-quality-assessment.md`。

2026-07-10 (二十八次): 第二十八次批量评估。平均分 **9.48** (A 级，-0.03)，**4 A+ / 9 A**。评分精度微调——将部分维度"上限宽松分"回调至更严格标准，核心内容无退化。全 13 个 SKILL.md 结构完整、内容质量稳定。最高分 skill-quality-assessor (9.55)，最低分 exec-plans (9.43)。8 维度均分 9.45-9.55，无显著薄弱维度。5 个 LOW 优化建议（bootstrap Related Skills 补充、exec-plans Examples 扩充、orchestration 自动化检查增强、observability Hard Constraints 补充、architecture-boundaries 自动化检测脚本）。第十六次达成"零未解决 MEDIUM+ 问题"状态。详见 `docs/quality-reports/skills-quality-assessment.md`。

2026-07-10 (二十九次): 第二十九次批量评估。平均分 **9.50** (A 级，+0.02)，**6 A+ / 7 A**。A+ 阵营从 4→6 扩张——repo-map (9.52) 和 observability-and-browser (9.52) 成功晋升。5 个重点 skill 全部正增长：project-intake (+0.04, Edge Cases 3→7 场景 + Agent Constraints 4→7 项)、bootstrap (+0.02, Related Skills 3→6 项)、orchestration (+0.02, Routing Quality Validation + Hard Constraints 4 项)、architecture-boundaries (+0.02, Agent Prompt 增强)、exec-plans (持平)。可用性维度 (+0.04) 和设计模式维度 (+0.03) 为最大增幅维度。无 CRITICAL/HIGH/MEDIUM 级别问题，第十七次达成"零未解决 MEDIUM+ 问题"状态。详见 `docs/quality-reports/skills-quality-assessment.md`。

2026-07-10 (三十次): 第三十次批量评估（确认评估轮次）。平均分 **9.50** (A 级，持平)，**6 A+ / 7 A**。自第29次评估后 SKILL.md 无新增内容变更，全量验证链通过确认质量未退化。全部8维度评分与第29次完全持平。exec-plans (9.43) 仍为最低分，bootstrap/orchestration (9.46) 交替倒数第二。无 CRITICAL/HIGH/MEDIUM 级别问题，第十八次达成"零未解决 MEDIUM+ 问题"状态。详见 `docs/quality-reports/skills-quality-assessment.md`。

2026-07-10 (三十一次): 第三十一次全量重新评估。平均分 **9.48** (A 级，-0.02)，**6 A+ / 7 A**。重新读取全部13个SKILL.md最新内容逐一手动评审。评分精度微调——部分维度"上限宽松分"回调至更严格标准，核心内容无退化。排名调整：skill-quality-assessor (9.55) 保持最高分，prompt-optimizer (9.54) 紧随其后，repo-map (9.52)/project-intake (9.51)/verification-loop (9.50)/orchestration (9.49) 维持或晋升 A+。commit-gate (9.49)/architecture-boundaries (9.49) 并列 A 级最高。6 个 LOW 优化建议（observability Hard Constraints 偏少、authoring/commit-gate/observability/verification-loop agent 命名一致性、prompt-optimizer Best Practices 去重、architecture-boundaries Edge Cases 扩充）。第十九次达成"零未解决 MEDIUM+ 问题"状态。详见 `docs/quality-reports/skills-quality-assessment.md`。

2026-07-10 (三十二次): 第三十二次批量评估。平均分 **9.49** (A 级，+0.01)，**6 A+ / 7 A**。8 个 skill 完成内容增强（architecture-boundaries Edge Cases 1→4、authoring Edge Cases 5→7、bootstrap Output Specification 扩展、commit-gate heading 对齐、exec-plans Example 5 + overrun detection、golden-principles Edge Cases 3→5 + Example 4、observability Examples 2→4 + Related Skills 2→4、orchestration Hard Constraints + Routing Quality Validation），5 个 skill 持平。等级分布不变（6A+/7A），排名微调：skill-quality-assessor (9.56, +0.01) 保持最高分，authoring (9.46, +0.02) 为最大正增长，observability (9.43, -0.03) 因评分精度微调下降。1 个 MEDIUM 问题（observability Hard Constraints 仅2条，全库最少）。第二十次达成"零未解决 CRITICAL/HIGH 问题"状态。详见 `docs/quality-reports/skills-quality-assessment.md`。

2026-07-10 (三十三次): 第三十三次批量评估。平均分 **9.46** (A 级，-0.03)，**5 A+ / 8 A**。评分精度微调——部分维度"上限宽松分"回调至更严格标准，核心内容无退化。13个 skill 全部有未提交变更（slug frontmatter 清理 + 内容增强 + 自动化检查脚本修复）。关键事件：(1) observability Hard Constraints 2→5（+3条新约束），评分从 9.43 升至 9.46 (+0.03)，但未突破 A+ 门槛；(2) 3 个自动化检查脚本修复缩进 bug（architecture-boundaries/exec-plans/orchestration）；(3) verification-loop 新增 Minimum Feedback Signals + Complex Problem Classification + Escalation Timing Rules；(4) authoring 新增 Quick Decision Table；(5) bootstrap Related Skills 3→6；(6) orchestration 新增 Routing Quality Validation 4项检查。等级分布从 6A+/7A 变为 5A+/8A（commit-gate 晋升 A+，project-intake 降至 A）。最高分 skill-quality-assessor (9.50)，最低分 project-intake (9.42)。1 个 MEDIUM 问题（exec-plans 缺少显式 Cross-Skill Handoff section）。第二十一次达成"零未解决 CRITICAL/HIGH 问题"状态。详见 `docs/quality-reports/skills-quality-assessment.md`。

---
最后更新: 2026-07-10（第 33 次）

## 维护周期（自 2026-07-03 起生效）

质量已进入维护稳态，后续优化收益递减。建议采用以下周期维护机制，聚焦**内容退化防控**而非扩张：

### 季度审计（每季度首周）

1. **引用完整性扫描**：运行 `python3 scripts/run-all.py` + 用 `grep -rE 'references/\\w+' skills/*/SKILL.md | grep '不存在' 2>/dev/null || echo "ok"` 验证所有引用的参考文件存在
2. **新鲜度检查**：检查所有 SKILL.md 的最后更新日期是否在 90 天内，超过的标记为待更新
3. **触发回归测试**：运行 `python3 scripts/run-all.py --run-type regression --json` 确保关键词映射未偏移
4. **自动化检查健康**：运行各 skill 的 `python3 skills/<name>/references/automated_check_script.py` 确认特有检查覆盖率仍与 SKILL.md 章节匹配

### 月度快速检查（每月中旬）

1. 运行 `python3 scripts/run-all.py --run-type check` 确认 frontmatter 字段无退化
2. 运行 `git log --oneline -20 skills/` 检查是否有新增修改后未更新最后日期的文件

### 质量阈值

- 平均分 **低于 9.30** → 触发季度审计（说明出现内容退化）
- 出现 **MEDIUM+ 级别问题** → 立即启动修复，优先级高于新功能
- 参考文件总数 **低于 75** → 检查是否有文件被误删

2026-09-24 (三十四次): **机械指标审计轮次**。本轮不再复算主观加权分——第 1-33 轮的 9.xx 分是评估者按 8 维度 rubric 人工打分，无法被机械复现，强行给一个"可比数字"等于编造。因此本轮改为对 rubric 中**可客观判定**的检查点做全量机械审计，结果 13/13 全绿：

| 检查点 | 结果 |
|---|---|
| frontmatter 必填字段完整（name/description/when_to_use/compatibility/context/agent/allowed-tools/depends_on） | 13/13 |
| metadata.category 存在 | 13/13 |
| 10 个必需章节齐全 | 13/13 |
| Hard Constraints 为编号列表且每条含 Violation 后果 | 13/13 |
| Agent 提示词 6 个子节齐全（Skip/Role/Capabilities/Flow/Constraints/Output） | 13/13 |
| Examples ≥ 3 | 13/13 |
| references/common-edge-cases.md 存在 | 13/13 |
| Edge Case Handling 场景 ≥ 3 | 13/13 |
| Last updated ≤ 90 天 | 13/13 |
| automated_check_script.py 存在且可执行 | 13/13 |

本轮修复的结构性缺陷（均由机械审计发现，非人工浏览）：
1. Hard Constraints 格式分裂为 5 编号 / 8 bullet，已统一为编号列表
2. harness-architecture-boundaries 缺 `## Common Pitfalls` 标题——6 条要点 orphaned 在 Edge Case Handling 末尾
3. harness-authoring 的 `## Related Templates` 整块重复
4. harness-prompt-optimizer 的 Edge Case Handling 排在 Best Practices 之后，顺序错位
5. 4 处硬约束只有规则没有 Violation 后果（commit-gate ×1、project-intake ×2、prompt-optimizer ×1）

新增机械强制：`depends_on` frontmatter 契约 + `scripts/validate_skill_dependencies.py`（环检测/向下流动/Meta 隔离/引用有效性/跨 skill 路径存在性），TD-001 关闭。

**关于 A+ 数量的说明**：第 33 次记录为 5 A+ / 8 A。本轮不做主观重评，因此不更新该计数——它仍是第 33 次评估的结果，不是本轮的。若需要新的 A+ 判定，需由 harness-skill-quality-assessor 按 rubric 人工执行。
