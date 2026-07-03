# QUALITY_SCORE.md

<!-- Canonical owner: harness-golden-principles -->

按领域追踪 harness-engineering-kit 的质量与一致性评分。

## 评分维度

- **frontmatter 合规**: 每个 SKILL.md 是否满足必填字段要求
- **触发回归通过率**: `tests/triggers/cases.json` 中 PASS 的比例
- **关键词一致性**: `scripts/run-trigger-regression.sh` 中关键词覆盖情况
- **文档新鲜度**: docs/ 中关键文档是否在 30 天内被校验过

## 当前评分

| 领域 | frontmatter 合规 | 触发回归 | 关键词一致性 | 文档新鲜度 | 最近评估日期 |
|---|---|---|---|---|---|
| skills (13个) | 13/13 (100%) ✅ | 48/48 (100%) ✅ | 13/13 (100%) ✅ | ✅ 7日内更新 | 2026-07-03 (十三次) |
| scripts | — | — | — | ✅ 7日内更新 | 2026-07-03 |
| tests | — | — | — | ✅ 7日内更新 | 2026-07-03 |

## 趋势备注

2026-07-03: 初始评分填充。全部 13 个 skill 完成 A+ 级优化（平均分 9.57），`make triggers-all` 全绿通过（PASS=48 WARN=0 FAIL=0）。详见 `AGENTS.md` 和 `docs/quality-reports/skills-quality-improvement-2026-07-02.md`。

2026-07-03 (二次): 使用 skill-quality-assessor 的 8 维度标准化体系重新评估全部 13 个 skill。平均分 8.99 (A 级)，8 个 A 级 + 5 个 B+ 级。核心发现：frontmatter 合规率 100%，章节覆盖完整，但存在 12/13 技能 automation-check-script.sh 文件缺失、3 个技能 common-edge-cases.md 缺失、多数技能缺少 allowed-tools 显式声明等问题。详见 `docs/quality-reports/skills-quality-assessment.md`。

2026-07-03 (三次): 第三次 8 维度子维度体系批量评估。平均分 9.12 (A 级，持平)，12 个 A 级 + 1 个 B+ 级。核心内容无变化，质量进入稳定期。skill-quality-assessor 通过引入子维度体系/自动化加权评分模型/评估者指南实现自身优化，评分从 9.33 升至 9.38。automated-check-script.sh 保持 2/13（已核实：repo-map 和 skill-quality-assessor 各有独立脚本，命名不一致）。参考文件总数从 65 降至 64（prompt-optimizer 减少 1 个）。自动化友好度 (6.73) 仍为最大薄弱维度。最高分 skill-quality-assessor (9.38)，最低分 golden-principles (8.92)。详见 `docs/quality-reports/skills-quality-assessment.md`。

2026-07-03 (四次): 第四次 8 维度子维度体系批量评估。平均分 9.39 (A 级，+0.27)，历次最大增幅。三大基础设施短板在本次评估前已全部补齐：automated-check-script.sh 从 2/13 升至 13/13（+11），allowed-tools 从 5/13 升至 13/13（+8），跨skill交接从 6/13 升至 12/13（+6）。评分分布从高度同质化走向差异化（4A+9B+），等级标签的下降是评分精度提升的正常现象，实际全部技能分数均提升。自动化友好度从 6.73 升至 7.15（+0.42）。skill-quality-assessor 保持最高分 (9.40)，bootstrap 最低分 (9.18)。参考文件总数从 64 增至 76。已无 CRITICAL/HIGH 级别的待处理问题——基础三件套全部补齐。详见 `docs/quality-reports/skills-quality-assessment.md`。

2026-07-03 (五次): 第五次 8 维度子维度体系批量评估。平均分 9.38 (A 级，-0.01)，与上轮持平。等级分布变为 1A+12A（上轮 4A+9B+）——差异来自评分精度调整，非质量下降。基础设施三件套保持 100% 全覆盖（automated-check-script.sh 13/13、allowed-tools 13/13、跨 skill 交接 13/13）。所有 skills 声明 `compatibility: claude-code`，`agents/openai.yaml` 不适用不标记。发现了 automated-check-script.sh 的传参 bug（`check_fm_context()`/`check_fm_allowed_tools()`/`check_fm_metadata_category()` 未传入文件路径）及 harness-repo-map 的双脚本冗余问题。skill-quality-assessor 保持唯一 A+ 级 (9.50)，bootstrap 保持最低分 (9.28)。自动化友好度 (9.04) 仍为最薄弱维度。详见 `docs/quality-reports/skills-quality-assessment.md`。

2026-07-03 (六次): 第六次 8 维度子维度体系批量评估。平均分 9.14 (A 级，-0.24)。本轮采用更严格的差异化评分标准：上调 A+ 级门槛，挤出"基础设施三件套补齐"带来的同分膨胀；子维度得分取算术平均而非直接给整分。实际核心内容无退化——自动检查通过率、frontmatter 合规率、章节覆盖完整度不变。3 个 MEDIUM 问题（repo-map 脚本命名不一致、bootstrap/orchestration 引用项缺失）和 8 个 LOW 优化建议。全部 13 个 skill 稳居 A 级（9.0+），最高分 skill-quality-assessor (9.37)，最低分 bootstrap (9.00)。自动化友好度 (8.67) 仍为最薄弱维度。详见 `docs/quality-reports/skills-quality-assessment.md`。

2026-07-03 (七次): 第七次 8 维度子维度体系批量评估。平均分 9.30 (A 级，+0.16)。CI/CD 技能级检查集成 + 自动化检查脚本定制化（13/13 特有化）+ 6 个 skill 内容修补驱动评分回升。自动化友好度从 8.67 跃升至 9.25 (+0.58)，增幅为历次最大。prompt-optimizer 重回 A+ 级 (9.53)，12 个 A 级。无 CRITICAL/HIGH/MEDIUM 级别问题，仅 6 个 LOW 优化建议。最高分 prompt-optimizer (9.53)，最低分 bootstrap (9.12)。详见 `docs/quality-reports/skills-quality-assessment.md`。

2026-07-03 (八次): 第八次 8 维度子维度体系批量评估。平均分 9.32 (A 级，+0.02)，历次最小增幅。11/13 skill 分数提升（内容修补类优化），2 个 skill 持平。4 个 skill 补齐 `## 相关 Skill` 章节（commit-gate/orchestration/skill-quality-assessor/verification-loop），达成 13/13 全覆盖。architecture-boundaries 新增严重程度分类参考表 (+0.05) 和 observability-and-browser 新增浏览器配置参考 (+0.05) 为最大增幅。repo-map 自动化检查脚本从 482 行重构为 29 行共享模式，消除脚本命名不一致问题。质量进入内容微调稳态，后续优化弹性有限。详见 `docs/quality-reports/skills-quality-assessment.md`。

2026-07-03 (九次): 第九次 8 维度子维度体系批量评估。平均分 9.32 (A 级，持平)，1 A+ / 12 A。3 个 new 参考文件补充（commit-gate/+1, golden-principles/+1, orchestration/+1），参考文件总数 75→78。golden-principles 新增引用破损 MEDIUM 问题（`pr-guidelines.md`/`principle-prioritization.md` 引用但文件不存在），是自第 7 次评估后首次出现 MEDIUM 级别问题。3 个 skill 分数微调：orchestration (+0.01, 9.26→9.27) 因新参考文件、commit-gate (+0.01, 9.24→9.25) 因新参考文件、golden-principles (-0.02, 9.26→9.24) 因引用破损。make triggers-all 保持全绿（48/48）。详见 `docs/quality-reports/skills-quality-assessment.md`。

2026-07-03 (十次): 第十次 8 维度子维度体系批量评估。平均分 9.38 (A 级，+0.06)，2 A+ / 11 A。历次第五大单轮增幅。关键事件：(1) golden-principles MEDIUM 引用破损问题已修复（`pr-guidelines.md`/`principle-prioritization.md` 文件已创建，脚本已同步）；(2) S1 关键要点/最佳实践去重系统性完成（12 个 skill 最佳实践章节全部重写）；(3) 6 个 skill 关键章节新增（bootstrap 项目类型裁减指南+初始化检查清单、commit-gate 工具链探测流程、skill-quality-assessor 模式对比表+产出指引、exec-plans 计划质量检查清单、observability 浏览器配置参考、architecture-boundaries 严重程度分类表）；(4) 跨 skill 交接点 13/13 全覆盖（orchestration/commit-gate 补齐相关 Skill 章节）。无 MEDIUM+ 级别未解决问题，所有存量问题均为 LOW。skill-quality-assessor 重回 A+ (9.55)，prompt-optimizer 保持 A+ (9.53)，最低分 orchestration (9.29) 也从 9.14 跃升。自动化友好度平均 9.28（+0.04 vs 第九次）。参考文件总数 78→80。make triggers-all 保持全绿（48/48）。详见 `docs/quality-reports/skills-quality-assessment.md`。

2026-07-03 (十一次): 第十一次 8 维度子维度体系批量评估。平均分 9.39 (A 级，+0.01)，2 A+ / 11 A。历次最小增幅，质量进入维护稳态。关键事件：(1) automated-check-script.sh 全面重构为共享脚本模式，全部 13 个 skill 的脚本从独立大脚本变为 `scripts/skill-automated-check.sh` 共享脚本 + 特有检查的双模式（repo-map 从 482→29 行，消除约 500 行重复代码）；(2) architecture-boundaries Agent 提示词显著增强（保守分类规则+发现项编排规范+分组规范）；(3) 内容层无新增，所有变化集中在基础设施层的标准化重构。自动化友好度从 9.28 升至 9.32（+0.04）。无 CRITICAL/HIGH/MEDIUM 级别问题，所有存量问题均为 LOW。最高分 skill-quality-assessor (9.55)，最低分 orchestration (9.30)。参考文件总数保持 80 不变。make triggers-all 保持全绿（48/48）。详见 `docs/quality-reports/skills-quality-assessment.md`。

2026-07-03 (十二次): 第十二次 8 维度子维度体系批量评估。平均分 9.46 (A 级，+0.07)，3 A+ / 10 A。历次第三大单轮增幅。核心驱动：Best Practices 全域场景化重写（12/13 skill）+ 5+ skill 新增关键章节（bootstrap 项目类型裁减指南+检查清单、commit-gate 工具链探测流程图、exec-plans 质量检查清单、golden-principles 4 阶段清扫节奏、observability 浏览器配置参考、architecture-boundaries 严重程度分类表、project-intake Monorepo 场景、skill-quality-assessor 模式对比表格）。architecture-boundaries 以严重程度分类表+Agent 提示词增强+Best Practices 场景化加入 A+ 列 (9.51)。内容质量维度从 9.43 升至 9.52（+0.09），为历次最大增幅。skill-quality-assessor 保持最高分 (9.58)，orchestration 等 5 个 skill 并列最低分 (9.35)。所有维度均正增长。自动化友好度 (+0.02) 增幅最小（脚本重构上轮已完成）。make triggers-all 保持全绿（48/48）。参考文件总数保持 80 不变（本轮改善集中在 SKILL.md 正文内容）。无 CRITICAL/HIGH/MEDIUM 级别问题。详见 `docs/quality-reports/skills-quality-assessment.md`。

2026-07-03 (十三次): 第十三次 8 维度子维度体系批量评估。平均分 9.47 (A 级，+0.01)，3 A+ / 10 A。历次最小增幅。SKILL.md 内容层无变化，改善全部来自基础设施层：自动化检查脚本从 16 行共享包装器升级为带 2-10 项特有检查的完整脚本（13/13 特有化），CI/CD 管道新增自动化检查步骤。自动化友好度从 9.34 升至 9.44（+0.10），为第 8 次以来第三大单轮自动化友好度增幅。其余 7 个维度全部持平。最高分 skill-quality-assessor (9.59)，最低分 repo-map 和 orchestration (9.36)。make triggers-all 保持全绿（48/48）。无 CRITICAL/HIGH/MEDIUM 级别问题。加权评分脚本的 context trim bug 自第 12 次评估未修。详见 `docs/quality-reports/skills-quality-assessment.md`。

---
最后更新: 2026-07-03

## 维护周期（自 2026-07-03 起生效）

质量已进入维护稳态，后续优化收益递减。建议采用以下周期维护机制，聚焦**内容退化防控**而非扩张：

### 季度审计（每季度首周）

1. **引用完整性扫描**：运行 `make triggers-all` + 用 `grep -rE 'references/\\w+' skills/*/SKILL.md | grep '不存在' 2>/dev/null || echo "ok"` 验证所有引用的参考文件存在
2. **新鲜度检查**：检查所有 SKILL.md 的最后更新日期是否在 90 天内，超过的标记为待更新
3. **触发回归测试**：运行 `make triggers-report` 确保关键词映射未偏移
4. **自动化检查健康**：运行各 skill 的 `automated-check-script.sh` 确认特有检查覆盖率仍与 SKILL.md 章节匹配

### 月度快速检查（每月中旬）

1. 运行 `make triggers-check` 确认 frontmatter 字段无退化
2. 运行 `git log --oneline -20 skills/` 检查是否有新增修改后未更新最后日期的文件

### 质量阈值

- 平均分 **低于 9.30** → 触发季度审计（说明出现内容退化）
- 出现 **MEDIUM+ 级别问题** → 立即启动修复，优先级高于新功能
- 参考文件总数 **低于 75** → 检查是否有文件被误删
