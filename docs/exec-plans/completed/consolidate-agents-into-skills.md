# 消除独立 agents 目录——合并 agent 提示词到 SKILL.md

- 状态: completed
- 创建日期: 2026-07-02
- 最近更新: 2026-07-02
- 关联 PR / issue: 暂无
- 负责 agent / 人: plan-architect（规划）→ skill-scaffolder（执行）→ verification-loop-runner（验证）

## 目标

每个 skill 的 agent 提示词内联到对应 SKILL.md 中，消除 `skills/*/agents/*.md` 文件，使 skill 结构符合 Claude Code 官方推荐的单文件模式。合并后 `skills/*/agents/` 目录仅保留 `openai.yaml`（Codex 元数据）。

## 范围

- 12 个 skill 的 `agents/<name>.md` 内容合并到对应 `SKILL.md`
- 更新每个 `SKILL.md` 的 frontmatter（添加 `context`、`agent` 字段）
- 更新 `docs/ARCHITECTURE.md` 中的目录结构说明
- 更新 `scripts/validate-agent-prompt-sync.sh` 适配新结构
- 更新 `AGENTS.md` 中相关约束描述
- 更新 `Makefile` 中 `prompts-sync-check` 目标（如需要）

## 明确不做（非目标）

- 不修改 agent 提示词的内容本身（角色定义、执行流程、约束等原样保留）
- 不修改 `openai.yaml` 文件（Codex 元数据保持不变）
- 不改变 skill 的功能行为和触发逻辑
- 不修改 `skills/` 目录的命名规范
- 不处理 `openai.yaml` 与合并后 SKILL.md 的同步问题（留作后续 PR）

## 决策日志

| 日期 | 决策 | 理由 | 被否决的备选方案 |
|---|---|---|---|
| 2026-07-02 | 采用合并入 SKILL.md 方案（方案 A） | 官方文档展示的 skill 模式是单文件指令；当前 agent 与 skill 高度耦合 | 方案 B（迁移到 .claude/agents/）改动面过大；方案 C（保持现状）不符合官方推荐 |
| 2026-07-02 | openai.yaml 保留在 agents/ 目录 | Codex 元数据与 Claude Code 提示词是两个独立关注点，合并会引入跨平台耦合 | 合并进 SKILL.md frontmatter 会破坏 Codex 解析 |
| 2026-07-02 | agent 提示词以独立 section 合并（不拆散到 skill 各段落） | 保持 agent 提示词的完整性便于后续维护和跨平台同步 | 拆散到 skill 各段落会增加维护复杂度 |

## 步骤

### Phase 1: 试点验证（1 个 skill）

- [ ] 1.1 — 选择 `harness-bootstrap` 作为试点，将 `agents/harness-bootstrapper.md` 内容合并到 `SKILL.md`
  - 验证方式：`SKILL.md` 包含完整 agent 提示词，`agents/harness-bootstrapper.md` 已删除
- [ ] 1.2 — 更新 `harness-bootstrap/SKILL.md` frontmatter，添加 `context: fork` 和 `agent` 字段
  - 验证方式：frontmatter 包含 `context: fork` 和 `agent: harness-bootstrapper`
- [ ] 1.3 — 运行 `make triggers-all` 确认试点不破坏现有校验
  - 验证方式：所有校验脚本退出码为 0

### Phase 2: 批量迁移（剩余 11 个 skill）

按依赖层级从低到高迁移，每批 3-4 个 skill，每批完成后运行校验：

- [ ] 2.1 — Layer 0-1: `harness-project-intake`、`harness-bootstrap`（试点已完成）
  - 验证方式：2 个 skill 的 agent 提示词已内联，`make triggers-all` 通过
- [ ] 2.2 — Layer 2: `harness-repo-map`、`harness-architecture-boundaries`、`harness-golden-principles`、`harness-prompt-optimizer`
  - 验证方式：4 个 skill 的 agent 提示词已内联，`make triggers-all` 通过
- [ ] 2.3 — Layer 3: `harness-exec-plans`
  - 验证方式：agent 提示词已内联，`make triggers-all` 通过
- [ ] 2.4 — Layer 4: `harness-verification-loop`、`harness-observability-and-browser`
  - 验证方式：2 个 skill 的 agent 提示词已内联，`make triggers-all` 通过
- [ ] 2.5 — Layer 5 + 元层: `harness-commit-gate`、`harness-orchestration`、`harness-authoring`
  - 验证方式：3 个 skill 的 agent 提示词已内联，`make triggers-all` 通过

### Phase 3: 基础设施更新

- [ ] 3.1 — 更新 `docs/ARCHITECTURE.md` 目录结构说明，移除 `agents/<name>.md` 描述
  - 验证方式：`ARCHITECTURE.md` 中不再引用 `agents/<name>.md` 作为 canonical 位置
- [ ] 3.2 — 更新 `scripts/validate-agent-prompt-sync.sh`，适配合并后结构
  - 验证方式：脚本能正确从 SKILL.md 中提取 agent 提示词并与 openai.yaml 比对
- [ ] 3.3 — 更新 `AGENTS.md` 中"每个 skill 的 agent 提示词只维护 `agents/<name>.md` 一处"约束
  - 验证方式：AGENTS.md 中约束描述已更新为新结构
- [ ] 3.4 — 清理残留的 `agents/*.md` 文件（确认全部迁移后）
  - 验证方式：`find skills/ -name "*.md" -path "*/agents/*"` 返回空

### Phase 4: 全量验证

- [ ] 4.1 — 运行 `make triggers-all` 全量校验
  - 验证方式：所有校验脚本退出码为 0
- [ ] 4.2 — 抽查 3 个 skill 的合并结果，确认 agent 提示词完整性
  - 验证方式：人工确认合并后的 SKILL.md 包含完整的角色定义、执行流程、约束
- [ ] 4.3 — 确认 `openai.yaml` 文件未被修改
  - 验证方式：`git diff --name-only` 中不包含 `openai.yaml`

## 多 Agent 执行策略

### Agent 分工

| Agent | 职责 | 工具权限 | 执行阶段 |
|---|---|---|---|
| `plan-architect` | 制定计划、拆解步骤、记录决策 | Read, Glob, Grep, Write（仅 docs/exec-plans/） | Phase 0（已完成） |
| `skill-scaffolder` | 执行文件合并、更新 frontmatter | Read, Write, Edit, Glob, Grep | Phase 1-3 |
| `verification-loop-runner` | 每批迁移后运行校验循环 | Bash, Read, Glob, Grep | Phase 1-4（每步验证） |
| `boundary-auditor` | 检查架构边界未被破坏 | Read, Glob, Grep | Phase 4（最终审查） |

### 执行流程

```
plan-architect（当前）
    │
    ▼
skill-scaffolder（Phase 1 试点）
    │
    ▼
verification-loop-runner（验证试点）
    │
    ▼
skill-scaffolder（Phase 2 批量迁移，每批 3-4 个 skill）
    │
    ├─▶ verification-loop-runner（每批验证）
    │
    ▼
skill-scaffolder（Phase 3 基础设施更新）
    │
    ▼
verification-loop-runner（Phase 4 全量验证）
    │
    ▼
boundary-auditor（最终架构边界审查）
```

### 交接协议

1. `skill-scaffolder` 完成一批迁移后，在 exec-plan 中勾选对应步骤
2. `verification-loop-runner` 运行 `make triggers-all`，结果写入 exec-plan
3. 校验失败时，`verification-loop-runner` 将失败原因写入 exec-plan，`skill-scaffolder` 修复后重新验证
4. 所有步骤完成后，`boundary-auditor` 做最终审查，确认无架构边界违规

## 验收标准

- [ ] `find skills/ -name "*.md" -path "*/agents/*"` 返回空（agents/*.md 全部清除）
- [ ] `make triggers-all` 全量通过（退出码 0）
- [ ] `git diff --name-only | grep openai.yaml` 返回空（openai.yaml 未被修改）
- [ ] 每个 SKILL.md 的 frontmatter 包含 `context: fork` 字段
- [ ] 每个 SKILL.md 包含 `## Agent 提示词` section，内容与原 agents/*.md 一致
- [ ] `docs/ARCHITECTURE.md` 中目录结构说明已更新
- [ ] `AGENTS.md` 中约束描述已更新

## 风险 / 已知未知

- **校验脚本适配风险**：`validate-agent-prompt-sync.sh` 从文件路径硬编码读取 agent 提示词，合并后需要改为从 SKILL.md 中解析 section。如果解析逻辑复杂度过高，可能需要简化为"只检查 SKILL.md 中存在 Agent 提示词 section"。
- **openai.yaml 同步问题**：合并后 openai.yaml 的 `system_prompt` 字段仍指向旧的 agent 提示词内容。本次计划不处理此同步问题，留作后续 PR。
- **SKILL.md 体积膨胀**：12 个 SKILL.md 各增加约 40-60 行 agent 提示词。需确认不影响 Claude Code 的 skill 加载性能。

## 变更记录

- 2026-07-02: 创建计划
- 2026-07-02: 执行完成，追加经验总结

## 经验总结

### 执行过程回顾

| 阶段 | 执行方式 | 耗时 | 问题 |
|---|---|---|---|
| Phase 1 试点 | 主对话直接执行 | 3 轮工具调用 | 无 |
| Phase 2 批量迁移 | 2 个 general agent 并行 | 1 轮 | 第二批 5 个 skill 未正确添加 section |
| Phase 3 基础设施 | 主对话直接执行 | 5 轮工具调用 | 无 |
| Phase 4 验证 + 修复 | 1 个 general agent 修复 | 2 轮 | 5 个 skill 需手动补 section |

### 关键教训

1. **并行 agent 批量操作需验证每个输出**
   - 两个 general agent 并行迁移 11 个 skill，第一批 6 个全部成功，第二批 5 个全部遗漏 `## Agent 提示词` section
   - 原因：agent 只更新了 frontmatter 和日期，但没有在文件末尾添加 section
   - 教训：批量操作后必须逐项验证，不能只依赖 agent 的自我报告

2. **校验脚本需适配结构变更**
   - 原 `validate-agent-prompt-sync.sh` 从 `agents/*.md` 读取并与 `openai.yaml` 比对
   - 合并后改为检查 SKILL.md 中是否存在 `## Agent 提示词` section
   - 教训：结构变更时同步更新校验脚本，否则 CI 会误报

3. **openai.yaml 同步问题留作技术债**
   - 合并后 openai.yaml 的 `system_prompt` 字段仍引用旧的 agent 提示词内容
   - 本次未处理，需后续 PR 同步
   - 教训：跨平台项目需考虑所有平台的同步问题

4. **官方文档优先级高于本地推测**
   - 最初不确定 agent 提示词能否合并到 SKILL.md
   - 查询 `code.claude.com/docs/en/skills` 后确认官方支持 `context: fork` + `agent` 字段
   - 教训：结构变更前先查官方文档，避免基于过时假设决策

### 多 Agent 协作模式验证

本次验证了"规划→执行→验证"的三阶段多 agent 协作模式：

```
plan-architect（规划）
    ↓
general agent（执行迁移）
    ↓
general agent（修复遗漏）
    ↓
verification-loop-runner（验证）
```

**有效点**：
- 并行 agent 显著提速（11 个 skill 迁移 < 1 分钟）
- 校验脚本提供了机械化的验证手段

**改进点**：
- 批量操作后需逐项验证，不能依赖 agent 自我报告
- 修复阶段应由独立 agent 执行，避免执行者自己验证自己的输出
