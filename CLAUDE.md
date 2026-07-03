# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> 本仓库是 **Harness Engineering Kit** 自身，不是被初始化的目标项目。目标项目在你执行 `harness-bootstrap` 后各自生成自己的 AGENTS.md。

## Quick start

```bash
make triggers-all     # 完整验证流水线（frontmatter 校验 + 关键词回归 + agent prompt 存在性检查）
make triggers-check   # 仅 frontmatter 字段校验
make triggers-regression  # 仅触发关键词回归测试（48 个测试用例）
make prompts-sync-check   # 仅 agent prompt 存在性检查
```

## Navigation

**首先读 `AGENTS.md`。** 它是本仓库的入口地图，包含硬约束、路由表和工作方式提示。深入信息在 `docs/` 目录下，`AGENTS.md` 只做索引不做百科全书。

关键文档：
- `docs/ARCHITECTURE.md` — 13 个 skill 的分层架构与依赖方向
- `docs/design-docs/core-beliefs.md` — 10 条 agent-first 核心信念
- `skills/` — 13 个 skill，每个含方法论正文 + agent 提示词 + 模板

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

提交前必须运行 `make triggers-all`。当前全 13 个 skill 质量评分 9.66/10（A+ 级）。详细维度评分见 `docs/QUALITY_SCORE.md`。

## Skill 文件结构

```
skills/<name>/
├── SKILL.md           # 方法论正文 + frontmatter + ## Agent 提示词
├── agents/
│   └── openai.yaml    # Codex UI 元数据（与 SKILL.md 逐字同步）
└── references/         # 模板文件、边界情况指南
```

Agent 提示词 canonical 版本在 `SKILL.md` 的 `## Agent 提示词` section；`disable-model-invocation: true` 的 skill 必须通过 subagent 调用。

**frontmatter 是跨平台契约**：Claude Code 读 `description`/`when_to_use`/`context`/`allowed-tools`；Codex 读 `name`/`description`/`compatibility`/`metadata`。各平台忽略自己不识别的字段，不要用同一字段存放不同内容。

## Testing

测试文件在 `tests/triggers/cases.json`（48 个触发回归用例）。关键词映射在 `scripts/run-trigger-regression.sh` 的 `SKILL_KW` 数组。新增 skill 时必须同时更新关键词映射和测试用例。

## Development Workflow

修改 skill 后按此顺序操作：

1. 修改 `skills/<name>/SKILL.md`（同步更新 `agents/openai.yaml` 的 system_prompt）
2. 运行 `make triggers-all` 确保无断裂
3. 用 `harness-skill-quality-assessor` 评估修改质量
4. 提交前运行 `make triggers-all` — **这是硬约束，提交前必须通过**
5. 推送到 `developer` 分支（本仓库 PR 合并到 `main`）

## Post-push

推送后主动询问是否同步技能包到 `~/.agents/skills`：
```bash
rsync -av --delete skills/ ~/.agents/skills/
```
