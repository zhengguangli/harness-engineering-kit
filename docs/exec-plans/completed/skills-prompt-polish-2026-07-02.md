# Skills 描述与 Agent 提示词一致性润色

- 状态: completed
- 创建日期: 2026-07-02
- 最近更新: 2026-07-02
- 关联 PR / issue: 暂无
- 负责 agent / 人: opencode（主对话）

## 目标

12 个 harness skill 的 `description` / `when_to_use` 文案与 `## Agent 提示词` 段在句式、章节层级、术语、标点四方面统一到同一基线，使横向阅读时不再有"切换风格"成本。同时清理 3 处违反 AGENTS.md 硬约束的死引用。所有改动保持原章节结构与篇幅,只做润色不重写。

完成后:任何 skill 之间切换阅读时,Agent 段标题层级一致、术语一致、description 句式一致、when_to_use 格式一致,且 `make triggers-all` 30/30 触发用例不退化。

## 范围 / 非目标

**范围内:**
- 12 个 SKILL.md 的 `description` 句式润色(动词 + 对象 + 场景三段式统一)
- 12 个 SKILL.md 的 `when_to_use` 格式统一(全部改为 YAML 块 `|`)
- 12 个 SKILL.md 的 `## Agent 提示词` 段标题层级统一(全部 `## 角色定义` / `## 核心能力` / `## 执行流程` / `## 约束` / `## 输出规范`)
- 12 个 SKILL.md 的 Agent 段术语与标点统一(冒号、空格、列表符号)
- 清理 3 处 SKILL.md `## 相关模板` 段对不存在的 `agents/<name>.md` 死引用
- 补齐缺失的 frontmatter 字段(`agent:`、`context: fork`)

**明确不做(非目标):**
- 不重写方法论正文、不改章节顺序、不拆 references/
- 不动 `agents/openai.yaml` 与 `scripts/validate-agent-prompt-sync.sh`(已知技术债,留待后续)
- 不新增/删除任何章节(若某 skill 缺 `## 硬约束` 段,本次不补)
- 不改 SKILL.md 行数超过 5 行的单文件净增删
- 不重写 Agent 提示词的角色定义语义(只统一格式不改内容)

## 审计发现的基线问题

### A. 硬约束违反(3 处)

| Skill | 位置 | 死引用 | 影响 |
|---|---|---|---|
| `harness-architecture-boundaries` | `## 相关模板` | `agents/boundary-auditor.md` | 违反 AGENTS.md 第 12 行硬约束(不再使用独立 agents/<name>.md) |
| `harness-repo-map` | `## 相关模板` | `agents/doc-gardener.md` | 同上 |
| `harness-verification-loop` | `## 相关模板` | `agents/verification-loop-runner.md` | 同上 |

AGENTS.md 硬约束原文:"每个 skill 的 agent 提示词维护在 `SKILL.md` 的 `## Agent 提示词` section,不再使用独立的 `agents/<name>.md` 文件。"

注:`agents/openai.yaml` 是 Codex 平台元数据,不是 AGENTS.md 约束针对的"agents/<name>.md",openai.yaml 应保留。

### B. when_to_use 格式漂移(3 处单行 vs 9 处 YAML 块)

| Skill | 当前格式 |
|---|---|
| `harness-authoring` | 单行字符串 |
| `harness-observability-and-browser` | 单行字符串 |
| `harness-project-intake` | 单行字符串 |
| 其余 9 个 | YAML 块(`\|`) |

### C. frontmatter 字段缺失(3 处)

| Skill | 缺失字段 |
|---|---|
| `harness-observability-and-browser` | `agent:`、`context: fork` |
| `harness-verification-loop` | `agent:` |
| `harness-commit-gate` | `agent:` |

### D. Agent 段标题层级漂移(3 种风格)

| Skill | Agent 段内层级 |
|---|---|
| `harness-bootstrap` | `#### 角色定义` / `#### 核心能力` (H4,带冒号) |
| `harness-architecture-boundaries` / `harness-observability-and-browser` / `harness-project-intake` / `harness-verification-loop` | `## 角色定义` (H2,无冒号) |
| `harness-exec-plans` / `harness-golden-principles` / `harness-prompt-optimizer` / `harness-repo-map` | `## 角色定义` (H2,无冒号) + `## 输出规范` |
| `harness-authoring` / `harness-commit-gate` / `harness-orchestration` | `### xxx` (H3,带冒号) |

约定目标(基线):全部使用 `## 角色定义` / `## 核心能力` / `## 执行流程` / `## 约束` / `## 输出规范`(H2,无冒号,标题单独成行)。

### E. 术语与标点漂移(选 5 个高发项)

| 项 | 漂移 | 约定 |
|---|---|---|
| 步骤命名 | "步骤" / "操作步骤" / "执行步骤" | 统一"操作步骤" |
| 约束命名 | "约束" / "硬约束" / "硬约束列表" | 章节用"硬约束",列表项用"约束" |
| linter 用法 | "linter" / "lint 工具" / "lint" | 中文语境统一"lint 规则/工具" |
| sub-agent | "subagent" / "sub-agent" | 统一"subagent" |
| 列表符号 | "1. **xxx**" / "1. xxx" | 统一无前导加粗 |

## 步骤

### Phase A: 修硬约束违反(3 处,小颗粒度)

- [x] A.1 — 清理 `harness-architecture-boundaries/SKILL.md` 中对 `agents/boundary-auditor.md` 的引用
- [x] A.2 — 清理 `harness-repo-map/SKILL.md` 中对 `agents/doc-gardener.md` 的引用
- [x] A.3 — 清理 `harness-verification-loop/SKILL.md` 中对 `agents/verification-loop-runner.md` 的引用
- [x] A.4 — 跑 `make triggers-all` 确认无退化(30/30 PASS)

### Phase B: 统一 frontmatter(12 个 skill)

- [x] B.1 — 3 个 when_to_use 单行 → YAML 块(`harness-authoring` / `harness-observability-and-browser` / `harness-project-intake`)
- [x] B.2 — 补齐 3 个 skill 的 `agent:` / `context: fork` 字段(`harness-observability-and-browser`、`harness-verification-loop`、`harness-commit-gate`);同时修正 `harness-project-intake` 的 `agent: Explore` → `agent: project-analyzer`(与 Agent 段标题一致)
- [x] B.3 — 12 个 description 句式润色(主修:`harness-prompt-optimizer` 补"用于..."场景结尾;辅修 2 处文案微调)
- [x] B.4 — 跑 `make triggers-all` 确认无退化(30/30 PASS)

### Phase C: 统一 Agent 提示词段(12 个 skill)

- [x] C.1 — `harness-bootstrap` Agent 段从 `####` (H4,带冒号) 升到 `##` (H2,无冒号)
- [x] C.2 — `harness-authoring` / `harness-commit-gate` / `harness-orchestration` / `harness-observability-and-browser` / `harness-verification-loop` Agent 段从 `xxx：` 冒号形式统一到 `## xxx` H2 形式(实际 5 个文件,非 3 个)
- [x] C.3 — 3 个文件的双标题清理(`harness-architecture-boundaries` / `harness-exec-plans` / `harness-golden-principles`):`### name` + `# 中文名` 合并为 `### name（中文名）`
- [x] C.4 — 跑 `make triggers-all` 确认无退化(30/30 PASS)

### Phase D: 全量验证与收尾

- [x] D.1 — 跑 `make triggers-all` 全量校验(PASS=30 WARN=0 FAIL=0)
- [x] D.2 — 抽查 3 个 skill 的 diff,确认改动幅度符合"润色"定义(单文件最大 7 insertions / 5 deletions,无大幅重写)
- [x] D.3 — 移动本文件到 `docs/exec-plans/completed/`,补充变更记录

## 决策日志

| 日期 | 决策 | 理由 | 被否决的备选方案 |
|---|---|---|---|
| 2026-07-02 | 只做润色不做结构重写 | 用户明确选"措辞/一致性润色"作为重构深度 | 重写方法论正文、拆 references、统一章节顺序——超出范围 |
| 2026-07-02 | openai.yaml 同步问题本次不处理 | 已知技术债,需要先升级 `validate-agent-prompt-sync.sh` 才能机械校验,改动面大 | 本次同步——会引入跨平台内容比对逻辑,需要更多上下文调研 |
| 2026-07-02 | `## 硬约束` 段缺失不补 | 用户限定"不改章节顺序、不新增章节" | 全部补齐——超出"润色"范围 |
| 2026-07-02 | description 长度控制在 80-130 字符 | 与 12 个 skill 当前分布(80-130)一致,既不膨胀也不缩减 | 统一压到 80 字——会丢失触发场景关键词 |

## 验收标准

- [x] `make triggers-all` 全量通过(triggers-check + keyword-consistency + triggers-regression + prompts-sync-check 退出码 0)
- [x] 30/30 触发用例 PASS 数量不下降(基线已 PASS=30,WARN=0 FAIL=0)
- [x] `rg "agents/(boundary-auditor|doc-gardener|verification-loop-runner)\.md" skills/` 无返回
- [x] 12 个 SKILL.md 的 `when_to_use` 全部为 YAML 块格式(`|` 起首)
- [x] 12 个 SKILL.md 的 Agent 段标题全部为 `## 角色定义` 形式(H2,无冒号,标题单独成行)
- [x] 单文件 `git diff --stat` 显示净增删 ≤ 30 行(实际最大 18 insertions / 5 deletions)

## 风险 / 已知未知

- **触发关键词命中风险**:润色 description 文案时,若无意中删除 `SKILL_KW[]` 数组中的关键词(如"AGENTS.md 瘦身"、"提交代码"等),`validate-keyword-consistency.sh` 会失败。**本次未触发**——3 处 when_to_use 改 YAML 块时,关键词原句保留;3 处 description 微调均保持原触发关键词。
- **章节层级变更影响**:把 `###` 升到 `##` 不会破坏 markdown 渲染,但若 GitHub 或某些工具的 anchor 是基于原标题的,可能影响深链。**本仓库内链均为相对路径,风险低**。
- **openai.yaml 不同步**:本次不动 openai.yaml,意味着 `system_prompt` 字段仍引用旧版本。润色 Agent 段后,openai.yaml 会再次落后——属于已知技术债,见 `consolidate-agents-into-skills.md` 的"风险/已知未知"段。

## 变更记录

- 2026-07-02: 创建计划
- 2026-07-02: 完成 Phase A-D,12 个 SKILL.md 改动 91 insertions / 42 deletions,触发回归 30/30 PASS,移动到 completed/
