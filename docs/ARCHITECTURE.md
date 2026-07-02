# ARCHITECTURE.md

<!-- Canonical owner: harness-architecture-boundaries -->

这个文件定义 harness-engineering-kit 的领域划分与依赖方向规则。

## 领域划分

| 领域 | 简述 | 对应路径 |
|---|---|---|
| skills | 12 个 skill（方法论 + agent 提示词 + 模板） | `skills/harness-*/` |
| scripts | 校验脚本（frontmatter、关键词一致性、回归） | `scripts/` |
| tests | 触发回归用例与报告 | `tests/` |
| ci | GitHub Actions 工作流与 PR 模板 | `.github/` |

## Skill 分层与依赖方向

```
Layer 0 信息采集    harness-project-intake
       ↓
Layer 1 骨架搭建    harness-bootstrap
       ↓
Layer 2 知识与约束  harness-repo-map, harness-architecture-boundaries,
                    harness-golden-principles, harness-prompt-optimizer
       ↓
Layer 3 计划驱动    harness-exec-plans
       ↓
Layer 4 执行验证    harness-verification-loop, harness-observability-and-browser
       ↓
Layer 5 提交门      harness-commit-gate

元层                harness-orchestration, harness-authoring
```

- 依赖只能向下流动：Layer N 的 skill 可引用 Layer <N 的产出，不可反向。
- 同层 skill 之间可以并行，不互相依赖。
- 元层 skill 可被任意层调用（orchestration 负责路由，authoring 负责扩展体系本身）。

## 每个 Skill 的内部结构

```
skills/<name>/
├── SKILL.md          # 方法论正文 + agent 提示词（含跨平台 frontmatter）
├── agents/
│   └── openai.yaml   # Codex UI 元数据
└── references/       # 模板文件
```

Agent 提示词已内联到 SKILL.md 的 `## Agent 提示词` section，不再使用独立的 `agents/<name>.md` 文件。

## 支撑基础设施的依赖方向

```
scripts/ → skills/    （脚本校验 skill 的 frontmatter 和关键词）
tests/   → skills/    （回归用例验证 skill 的触发逻辑）
.github/ → scripts/   （CI 调用校验脚本）
```

- scripts/ 只读取 skills/ 的内容，不修改。
- tests/ 的回归用例依赖 scripts/ 中定义的关键词映射。
- .github/workflows/ 调用 `make triggers-all` 触发完整校验链。

## 数据边界规则

- 每个 `SKILL.md` 的 frontmatter 是 skill 与平台之间的契约——平台只读自己认识的字段，忽略未知字段。
- Agent 提示词的 canonical 版本在 `SKILL.md` 的 `## Agent 提示词` section。

## 机械强制现状

| 规则 | 强制方式 | 状态 |
|---|---|---|
| frontmatter 必填字段 | `scripts/validate-skill-triggers.sh` | ✅ 已强制 |
| 关键词一致性 | `scripts/validate-keyword-consistency.sh` | ✅ 已强制 |
| 触发回归 | `scripts/run-trigger-regression.sh` | ✅ 已强制 |
| agent 提示词存在性 | `scripts/validate-agent-prompt-sync.sh` | ✅ 已强制 |
| skill 间无循环依赖 | 人工 review | ⚠️ 仅文档，未强制 |

---
最后更新: 2026-07-02
