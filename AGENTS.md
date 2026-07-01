# AGENTS.md

这个文件是地图，不是百科全书。如果你在这里没找到答案，去下面对应的 `docs/` 文件里找——不要假设这个文件之外的信息不存在，只是它被放在了别处。DO NOT send optional commentary

## 这个仓库是什么

Harness Engineering Kit：一套通用、与具体项目无关的 skills + agents 套件，适用于 Claude Code、OpenCode 和 Codex。把 OpenAI 和 LangChain 两篇 harness engineering 文章的核心方法论，落地为可直接放进任意仓库的可执行工件。

## 硬约束（极少数，违反即阻塞合并）

- 每个 `SKILL.md` 的 frontmatter 必须包含 `description`（≥20 字符）、`when_to_use`、`compatibility` 字段，不含已废弃的 `version` 字段。
- 每个 skill 的 agent 提示词 canonical 版本在 `agents/<name>.md`，`references/` 里的同名文件只是存根，不允许出现两份不同内容。
- Skills 之间不允许循环依赖；依赖方向见 `docs/ARCHITECTURE.md`。

## 去哪里找更多

| 我想知道… | 去看这里 |
|---|---|
| 12 个 skill 的分层架构与依赖方向 | `docs/ARCHITECTURE.md` |
| agent-first 的核心运作信念 | `docs/design-docs/core-beliefs.md` |
| 设计决策索引 | `docs/design-docs/index.md` |
| 当前/已完成的执行计划 | `docs/exec-plans/active/`, `docs/exec-plans/completed/` |
| 已知但暂不处理的技术债 | `docs/exec-plans/tech-debt-tracker.md` |
| 产品功能规格 | `docs/product-specs/index.md` |
| 各领域的质量评分 | `docs/QUALITY_SCORE.md` |
| 详细的安装方式、触发速查表、回归用例维护规范 | `README.md` |

## 工作方式提示

- 复杂、可能跨多次会话的任务，先用 `harness-exec-plans` 技能落一份 exec-plan，不要直接动手。
- 改动完成后，跑自验证循环（`harness-verification-loop`）而不是一次性提交了事。
- 提交前跑 `make triggers-all` 确保 frontmatter 校验、关键词一致性、回归测试全部通过。
- 不确定某条规则是否仍然有效？去对应的 docs 文件查"最后校验日期"，过期的规则应该被标记而不是被信任。
- 要给这套体系添加新能力，参考 `harness-authoring` skill。

---
最后更新: 2026-07-01
