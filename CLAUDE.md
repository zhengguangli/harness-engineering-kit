# CLAUDE.md

这个文件是地图，不是百科全书。如果你在这里没找到答案，去下面对应的 `docs/` 文件里找——不要假设这个文件之外的信息不存在，只是它被放在了别处。DO NOT send optional commentary.

> 本仓库是 **Harness Engineering Kit** 自身，不是被初始化的目标项目。目标项目在你执行 `harness-bootstrap` 后各自生成自己的 **CLAUDE.md**。
>
> Harness Engineering Kit：一套通用、与具体项目无关的 skills 套件，完美适配 Claude Code CLI。把 OpenAI 和 LangChain 两篇 harness engineering 文章的核心方法论，落地为可直接放进任意仓库的可执行工件。

## Quick start

```bash
make triggers-all     # 完整验证流水线（frontmatter 校验 + 关键词回归 + agent prompt 存在性检查）
make triggers-check   # 仅 frontmatter 字段校验
make triggers-regression  # 仅触发关键词回归测试（48 个测试用例）
make triggers-report  # 触发关键词回归 JSON 报告（含详细判定信息）
make prompts-sync-check   # 仅 agent prompt 存在性检查
```

## Navigation

关键文档：

| 我想知道… | 去看这里 |
|---|---|
| 13 个 skill 的分层架构与依赖方向 | `docs/ARCHITECTURE.md` |
| agent-first 的核心运作信念 | `docs/design-docs/core-beliefs.md` |
| 设计决策索引 | `docs/design-docs/index.md` |
| 当前执行计划 | `docs/exec-plans/active/` |
| 已知但暂不处理的技术债 | `docs/exec-plans/tech-debt-tracker.md` |
| 产品功能规格 | `docs/product-specs/index.md` |
| 各 skill 质量评分与趋势追踪 | `docs/QUALITY_SCORE.md` |
| 技能生成的报告（扫描/审计/评估） | `docs/quality-reports/` |
| 13 个 skill 的方法论正文 + agent 提示词 + 模板 | `skills/` |
| 详细的安装方式、触发速查表、回归用例维护规范 | `README.md` |

## 硬约束（违反即阻塞合并）

- 每个 `SKILL.md` 的 frontmatter 必须包含 `description`（>= 20 字符）、`when_to_use`、`compatibility` 字段，不含已废弃的 `version` 字段。
- 每个 skill 的 agent 提示词维护在 `SKILL.md` 的 `## Agent 提示词` section，不再使用独立的 `agents/<name>.md` 文件。
- Skills 之间不允许循环依赖；依赖方向见 `docs/ARCHITECTURE.md`。

## Architecture

```
Layer 0 信息采集    harness-project-intake
Layer 1 骨架搭建    harness-bootstrap
Layer 2 知识与约束  harness-repo-map, harness-architecture-boundaries,
                    harness-golden-principles, harness-prompt-optimizer
Layer 3 计划驱动    harness-exec-plans
Layer 4 执行验证    harness-verification-loop, harness-observability-and-browser
Layer 5 提交门      harness-commit-gate
元层                harness-orchestration, harness-authoring
```

依赖只能向下流动。同层可并行。元层可被任意层调用。

## Skill Invocation

所有 skill 均使用 `context: fork`，通过 subagent 独立执行。

- **3 个 `disable-model-invocation: true`**：`harness-bootstrap`、`harness-commit-gate`、`harness-verification-loop` — 不能直接用 Skill tool 调用，必须通过 `Agent` tool 或 Workflow 使用。
- **2 个 `allowed-tools` 受限**：`harness-commit-gate` 和 `harness-verification-loop` 分别将 Bash 限制为 `git`/`npm`/`bun`/`cargo`/`make`/`just` 子集。其余 skill 默认继承全部工具，不符合最小权限原则时应手动限制。
- Agent 提示词 canonical 版本在 `SKILL.md` 的 `## Agent 提示词` section，不再使用独立的 `agents/<name>.md` 文件。

## Quality gates

提交前必须运行 `make triggers-all`。当前全 13 个 skill 质量评分 9.12/10（A 级）。详细维度评分见 `docs/QUALITY_SCORE.md`。

## Skill 文件结构

```
skills/<name>/
├── SKILL.md           # 方法论正文 + frontmatter + ## Agent 提示词
└── references/         # 模板文件、边界情况指南
```

**frontmatter 字段说明**：`description`（做什么 + 什么时候用）、`when_to_use`（触发场景）、`context`（执行模式，如 `fork`）、`allowed-tools`（工具白名单）。各字段仅 Claude Code 读取。

## Testing

测试文件在 `tests/triggers/cases.json`（48 个触发回归用例）。关键词映射在 `scripts/run-trigger-regression.sh` 的 `SKILL_KW` 数组。新增 skill 时必须同时更新关键词映射和测试用例。

## Development Workflow

修改 skill 后按此顺序操作：

1. 修改 `skills/<name>/SKILL.md`
2. 运行 `make triggers-all` 确保无断裂
3. 用 `harness-skill-quality-assessor` 评估修改质量
4. 提交前运行 `make triggers-all` — **这是硬约束，提交前必须通过**
5. 推送到 `developer` 分支（本仓库 PR 合并到 `main`）

## 工作方式提示

- 复杂、可能跨多次会话的任务，先用 `harness-exec-plans` 技能落一份 exec-plan，不要直接动手。
- 改动完成后，跑自验证循环（`harness-verification-loop`）而不是一次性提交了事。
- 提交前跑 `make triggers-all` 确保 frontmatter 校验、关键词一致性、回归测试全部通过。
- 不确定某条规则是否仍然有效？去对应的 docs 文件查"最后校验日期"，过期的规则应该被标记而不是被信任。
- 要给这套体系添加新能力，参考 `harness-authoring` skill。
- **推送代码后**，主动询问用户是否同步技能包到 `~/.agents/skills`，获得允许后执行：

  ```bash
  rsync -av --delete skills/ ~/.agents/skills/
  ```

## CI Pipeline

```yaml
push → main:      make triggers-all
PR → main:        确保 source 为 developer 分支 + make triggers-all
```

详情见 `.github/workflows/skill-triggers.yml`。PR 必须从 `developer` 分支发起，不可直接从特性分支向 `main` 提 PR。

---

最后更新: 2026-07-03（CLAUDE.md 已合并至此文件，不再单独维护）
