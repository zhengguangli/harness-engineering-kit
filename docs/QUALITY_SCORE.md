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
| skills (13个) | 13/13 (100%) ✅ | 48/48 (100%) ✅ | 13/13 (100%) ✅ | ✅ 7日内更新 | 2026-07-03 (六次) |
| scripts | — | — | — | ✅ 7日内更新 | 2026-07-03 |
| tests | — | — | — | ✅ 7日内更新 | 2026-07-03 |

## 趋势备注

2026-07-03: 初始评分填充。全部 13 个 skill 完成 A+ 级优化（平均分 9.57），`make triggers-all` 全绿通过（PASS=48 WARN=0 FAIL=0）。详见 `AGENTS.md` 和 `docs/quality-reports/skills-quality-improvement-2026-07-02.md`。

2026-07-03 (二次): 使用 skill-quality-assessor 的 8 维度标准化体系重新评估全部 13 个 skill。平均分 8.99 (A 级)，8 个 A 级 + 5 个 B+ 级。核心发现：frontmatter 合规率 100%，章节覆盖完整，但存在 12/13 技能 automation-check-script.sh 文件缺失、3 个技能 common-edge-cases.md 缺失、多数技能缺少 allowed-tools 显式声明等问题。详见 `docs/quality-reports/skills-quality-assessment.md`。

2026-07-03 (三次): 第三次 8 维度子维度体系批量评估。平均分 9.12 (A 级，持平)，12 个 A 级 + 1 个 B+ 级。核心内容无变化，质量进入稳定期。skill-quality-assessor 通过引入子维度体系/自动化加权评分模型/评估者指南实现自身优化，评分从 9.33 升至 9.38。automated-check-script.sh 保持 2/13（已核实：repo-map 和 skill-quality-assessor 各有独立脚本，命名不一致）。参考文件总数从 65 降至 64（prompt-optimizer 减少 1 个）。自动化友好度 (6.73) 仍为最大薄弱维度。最高分 skill-quality-assessor (9.38)，最低分 golden-principles (8.92)。详见 `docs/quality-reports/skills-quality-assessment.md`。

2026-07-03 (四次): 第四次 8 维度子维度体系批量评估。平均分 9.39 (A 级，+0.27)，历次最大增幅。三大基础设施短板在本次评估前已全部补齐：automated-check-script.sh 从 2/13 升至 13/13（+11），allowed-tools 从 5/13 升至 13/13（+8），跨skill交接从 6/13 升至 12/13（+6）。评分分布从高度同质化走向差异化（4A+9B+），等级标签的下降是评分精度提升的正常现象，实际全部技能分数均提升。自动化友好度从 6.73 升至 7.15（+0.42）。skill-quality-assessor 保持最高分 (9.40)，bootstrap 最低分 (9.18)。参考文件总数从 64 增至 76。已无 CRITICAL/HIGH 级别的待处理问题——基础三件套全部补齐。详见 `docs/quality-reports/skills-quality-assessment.md`。

2026-07-03 (五次): 第五次 8 维度子维度体系批量评估。平均分 9.38 (A 级，-0.01)，与上轮持平。等级分布变为 1A+12A（上轮 4A+9B+）——差异来自评分精度调整，非质量下降。基础设施三件套保持 100% 全覆盖（automated-check-script.sh 13/13、allowed-tools 13/13、跨 skill 交接 13/13）。所有 skills 声明 `compatibility: claude-code`，`agents/openai.yaml` 不适用不标记。发现了 automated-check-script.sh 的传参 bug（`check_fm_context()`/`check_fm_allowed_tools()`/`check_fm_metadata_category()` 未传入文件路径）及 harness-repo-map 的双脚本冗余问题。skill-quality-assessor 保持唯一 A+ 级 (9.50)，bootstrap 保持最低分 (9.28)。自动化友好度 (9.04) 仍为最薄弱维度。详见 `docs/quality-reports/skills-quality-assessment.md`。

2026-07-03 (六次): 第六次 8 维度子维度体系批量评估。平均分 9.14 (A 级，-0.24)。本轮采用更严格的差异化评分标准：上调 A+ 级门槛，挤出"基础设施三件套补齐"带来的同分膨胀；子维度得分取算术平均而非直接给整分。实际核心内容无退化——自动检查通过率、frontmatter 合规率、章节覆盖完整度不变。3 个 MEDIUM 问题（repo-map 脚本命名不一致、bootstrap/orchestration 引用项缺失）和 8 个 LOW 优化建议。全部 13 个 skill 稳居 A 级（9.0+），最高分 skill-quality-assessor (9.37)，最低分 bootstrap (9.00)。自动化友好度 (8.67) 仍为最薄弱维度。详见 `docs/quality-reports/skills-quality-assessment.md`。

---
最后更新: 2026-07-03
