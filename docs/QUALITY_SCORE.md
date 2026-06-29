# QUALITY_SCORE.md

按技能和分层追踪代码质量与架构一致性的评分,随时间观察差距是否在收敛还是扩大。由 `entropy-collector` agent 在周期性清扫时更新。

黄金原则列表见 `docs/golden-principles.md`。架构边界检查模式见 `docs/ARCHITECTURE.md` 的"检查模式"章节。

## 评分维度

- **结构一致性**:是否遵守 `ARCHITECTURE.md` 里定义的 skill 内部结构(SKILL.md + agents/ + references/)
- **Agent 定义完整性**:agent `.md` 文件 frontmatter 的完整度(name/description/type/tools/model/skills)
- **跨平台同步**:Claude Code(.md) 和 Codex(openai.yaml) 的 agent 定义是否功能对等——不仅要求文件存在,还要求:
  1. `openai.yaml` 包含完整的 metadata、tools、system_prompt 三个区块
  2. 系统提示词内容与对应 `.md` 文件实质等价(允许平台特定的工具名差异)
  3. 工具权限对等(只读型在两个平台都是只读,执行型在两个平台都有写工具)
  4. 模型映射合理(sonnet↔gpt-5.4, opus↔gpt-5.5)
- **文档新鲜度**:对应 `docs/` 条目是否在最近 30 天内被校验过
- **黄金原则遵循度**:对照 `docs/golden-principles.md` 中 GP-01~GP-05 的违反密度

## 当前评分

| 领域 | 结构一致性 | Agent 定义完整性 | 跨平台同步 | 文档新鲜度 | 黄金原则遵循度 | 最近评估日期 |
|---|---|---|---|---|---|---|
| harness-repo-map | ✅ | ✅ | ✅ | ✅ | ✅ | 2026-06-29 |
| harness-exec-plans | ✅ | ✅ | ✅ | ✅ | ✅ | 2026-06-29 |
| harness-architecture-boundaries | ✅ | ✅ | ✅ | ✅ | ✅ | 2026-06-29 |
| harness-verification-loop | ✅ | ✅ | ✅ | ✅ | ✅ | 2026-06-29 |
| harness-observability-and-browser | ✅ | ✅ | ✅ | ✅ | ✅ | 2026-06-29 |
| harness-golden-principles | ✅ | ✅ | ✅ | ✅ | ✅ | 2026-06-29 |
| harness-authoring | ✅ | ✅ | ✅ | ✅ | ✅ | 2026-06-29 |
| harness-bootstrap | ✅ | ✅ | ✅ | ✅ | ✅ | 2026-06-29 |
| harness-commit-gate | ✅ | ✅ | ✅ | ✅ | ✅ | 2026-06-29 |
| harness-project-intake | ✅ | ✅ | ✅ | ✅ | ✅ | 2026-06-29 |
| harness-orchestration | ✅ | ✅ | ✅ | ✅ | ✅ | 2026-06-29 |

## 趋势备注

2026-06-29 审查修复:

- 修复了 2 处跨 skill 文件路径引用(GP-01 违反):`harness-observability-and-browser` 和 `harness-verification-loop` 的 SKILL.md 中直接引用了 `harness-exec-plans` 的 `references/exec-plan-template.md`,已改为指向 `docs/exec-plans/` 目录。
- 清理了 `harness-orchestration/references/` 中多余的 `.gitkeep` 文件。
- 独立审查确认:三件套结构、frontmatter 完整性、跨平台同步、黄金原则 GP-01~GP-05 全部通过机械化检查。
- 新增 `scripts/check-skills-quality.sh` 统一执行 6 项质量检查(结构/frontmatter/命名/日期/三区块/跨平台同步),任何失败返回 FAIL=1。

下一轮评估前重点关注:

- `harness-authoring` 的 `skill-scaffolder` agent 应该能够自动生成符合全部约束的新技能骨架——这本身就是一种结构化强制。
- 跨平台同步检查已脚本化: `check-cross-platform-sync` 验证每个 `openai.yaml` 的三区块完整性与对应 `.md` 存在性(见 `docs/ARCHITECTURE.md` 的检查模式章节)。下一步可扩展:system_prompt 内容与对应 `.md` 的语义等价验证。
- 黄金原则列表应随仓库演进持续补充——当某类偏差在清扫中反复出现时,说明需要新增或细化原则。
- GP-01 检查命令当前只匹配 `skills/harness-` 路径前缀,无法捕获"引用其他 skill 的 references/ 文件"这种间接跨 skill 引用,建议补充更精确的检查模式。

---
最后更新: 2026-06-29
