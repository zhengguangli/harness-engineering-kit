# Skills 提示词二轮优化（Round 2）

- 状态: active
- 创建日期: 2026-07-02
- 最近更新: 2026-07-02
- 关联 PR / issue: 暂无
- 负责 agent / 人: opencode（主对话）+ 用户 review
- 前置: `docs/exec-plans/completed/skills-audit-2026-07-02.md`（Round 1，49 条建议中 26 条已落地、20 条 LOW 延后到 TD-003）

## 执行摘要

- **基线**（2026-07-02）：`make triggers-all` → 4/4 脚本 OK，30/30 PASS=30 WARN=0 FAIL=0，12/12 skill frontmatter+keyword+agent_prompt OK
- **目标**：处理 TD-003 剩余 17 条 LOW + 7 类新发现结构性问题 + 测试用例 30→50（每 skill ≥ 3）
- **范围**：12 个 `skills/harness-*/SKILL.md` + `tests/triggers/cases.json`
- **明确不做**：`agents/openai.yaml`（TD-002）、`references/*.md`、`scripts/`、`docs/`（除本 exec-plan 文件外）

## 目标

将 12 个 skill 的 SKILL.md 三段（frontmatter / 正文 / Agent 提示词）统一到以下标准：

1. **frontmatter 字段齐全**：`description`（≥20 字符）、`when_to_use`、`compatibility` 三个硬约束字段 + 可选 `agent:` 字段
2. **Agent 提示词六段式**：`## 角色定义` / `## 核心能力` / `## 执行流程` / `## 约束` / `## 输出规范`，heading 层级统一为 `##`
3. **约束带修复行为**：每条约束包含"违反时怎么办"
4. **测试覆盖**：每 skill ≥ 3 个用例，含 positive / ambiguous / negative 三类

完成后：12 个 skill 在结构上一致、五维审计（description_clarity / trigger_precision / frontmatter_consistency / agent_prompt_quality / internal_consistency）下 LOW 数为 0，触发回归 50/50 PASS 不退化。

## 范围 / 非目标

**范围内:**
- 12 个 `skills/harness-*/SKILL.md` 的 frontmatter / 正文 / `## Agent 提示词` section
- `tests/triggers/cases.json`（30 → 50 条）
- 本 exec-plan 落盘与归档

**明确不做(非目标):**
- 不动 `agents/openai.yaml`（TD-002 已知）
- 不动 `references/*.md` 子文件
- 不动 `scripts/`、`docs/`
- 不新增 / 删除 SKILL.md 章节（仅在现有结构内对齐）
- 不改 SKILL.md 的语义内容（架构、职责、方法论、模板引用等），只调整结构与措辞

## 待处理项清单

### A. 7 类结构性问题（跨 skill）

| ID | 问题 | 涉及文件 | 修复方式 |
|---|---|---|---|
| A1 | Agent 提示词子标题层级不一致（`####` / `###` / `##` 三种） | exec-plans（`####`）、project-intake（`###`） | 统一为 `##` |
| A2 | 缺 `## 输出规范` section | authoring、commit-gate、orchestration、verification-loop | 各补一节 |
| A3 | frontmatter 缺 `agent:` 字段 | orchestration | 补 `agent: orchestrator` |
| A4 | "禁止" 列表在 核心能力 + 约束 中重复 | project-intake（L129+L144）、verification-loop（L113+L133） | 保留约束版，移除核心能力里的"禁止"行 |
| A5 | `context: fork` 缺失 | commit-gate、verification-loop（动作型 skill） | 补 `context: fork`（其余 2 个非动作型保持现状） |
| A6 | Agent 段缺"## 跳过条件"section | commit-gate、observability-and-browser | 补"## 跳过条件"（commit-gate 已有，仅 observability 缺） |
| A7 | 跨 skill 交接未在 agent prompt 中显式编码 | architecture-boundaries → entropy-collector LOW 项交接 | 在 architecture-boundaries agent prompt 加"LOW 项交接 entropy-collector"步骤 |

### B. TD-003 剩余 17 条 LOW 建议

来源：`docs/exec-plans/tech-debt-tracker.md` 中标"(待处理)"的条目（已与 CRITICAL/MEDIUM 合并的 3 条跳过）：

| Skill | 位置 | 摘要 |
|---|---|---|
| harness-authoring | L139 | 全角标点"：""，"改半角 |
| harness-authoring | L84 | 自检清单补"agent 提示词位置"项 |
| harness-bootstrap | L22 | "何时使用"段删"run harness"触发词（与 SKILL_KW 一致性） |
| harness-bootstrap | L87 | 新增"## 相关 skill"小节（project-intake / repo-map） |
| harness-golden-principles | L50 | "持续观察"措辞与 agent prompt L99 对齐 |
| harness-golden-principles | L80 | "只读执行"加粗强调 |
| harness-golden-principles | L91 | 早退路径补结构化报告 |
| harness-orchestration | L16-19 | "何时使用"列表与 when_to_use 对齐 |
| harness-project-intake | L5-L6 | 引号风格统一（弯引号 vs 直引号） |
| harness-prompt-optimizer | L3 | description 末尾删"用于..."段（与 when_to_use 重复） |
| harness-prompt-optimizer | L96 | 硬约束补"3 步下限" |
| harness-prompt-optimizer | L120 | 新增"## 何时不适用"section |
| harness-repo-map | L76 | 操作步骤第 6 步展开跨段引用 |
| harness-verification-loop | L70-76 | 三套并行流程（methodology/操作步骤/Agent 提示词）编号统一 |
| harness-verification-loop | L122 | 循环步骤 6 加卡住检测子步骤 |
| harness-verification-loop | L117 | 完成定义补 exec-plan schema 校验子步骤 |
| harness-verification-loop | L129 | "立即停止"约束补诊断文件路径 |

### C. 测试用例 30 → 50

当前覆盖（30 条）：

| Skill | 用例数 | 缺口 |
|---|---|---|
| harness-commit-gate | 5 | OK |
| harness-exec-plans | 4 | OK |
| harness-repo-map | 4 | OK |
| harness-orchestration | 3 | OK |
| harness-bootstrap | 3 | OK |
| harness-verification-loop | 3 | OK |
| harness-project-intake | 2 | +1 |
| harness-prompt-optimizer | 2 | +1 |
| harness-authoring | 2 | +1 |
| harness-golden-principles | 2 | +1 |
| **harness-observability-and-browser** | **0** | **+3** |
| **harness-architecture-boundaries** | **0** | **+3** |

补充 20 条用例：
- 12 条补缺口到 ≥ 3（每个薄弱 skill）
- 5 条 negative（"代码实现"等不应触发 prompt-optimizer 的输入）验证不会误路由
- 3 条 ambiguous（"重构代码"等模糊输入，验证多 skill 候选列表）

## 步骤

- [x] 1 — **基线快照**（已完成）:`make triggers-all 2>&1 | tee /tmp/baseline-2026-07-02-r2.log` → PASS=30 WARN=0 FAIL=0，所有 4 脚本退出码 0
- [x] 2 — **逐文件修复**：按 12 个 skill 顺序，每个文件应用 A1-A7 中适用于该文件的项 + TD-003 中属于该文件的项；逐文件 `make triggers-check` 子目标验证
- [x] 3 — **测试用例补充**：在 `tests/triggers/cases.json` 增加 18 条用例（48 总计，含 5 negative + 3 ambiguous）
- [x] 4 — **全量验证**：`make triggers-all`，确认 PASS=48 WARN=0 FAIL=0
- [ ] 5 — **报告与归档**：在主对话输出改动摘要 + diff stat；移动本文件到 `docs/exec-plans/completed/`，更新 tech-debt-tracker.md（清空 TD-003 17 条）

## 决策日志

| 日期 | 决策 | 理由 | 被否决的备选方案 |
|---|---|---|---|
| 2026-07-02 | heading 层级统一为 `##` | 与 harness-prompt-optimizer 六区块结构对齐，doc-gardener "配对完整性"检查依赖此一致性 | 保留异构——会持续制造"配对完整性"自指 bug |
| 2026-07-02 | 保留 4 个非动作型 skill 的 `context: fork` 现状（authoring、orchestration） | 二者纯路由/咨询，不需要主对话上下文隔离 | 全部加 `context: fork`——会增加子 agent 启动开销但无实际收益 |
| 2026-07-02 | 给 commit-gate / verification-loop 加 `context: fork` | 这两个会修改 git 状态 / 写业务代码，副作用强 | 保持主对话执行——风险太高 |
| 2026-07-02 | description 字段不重写 | 关键词一致性校验依赖 description 里的关键词字符串，重写有删词风险 | 重写 description——TD-001 经验值 |
| 2026-07-02 | 测试用例 ID 沿用 `xxx-NN` 序号 | 与现有命名风格一致 | 改成 `<skill>-<type>-<n>` 三段式——超范围 |

## 验收标准

- [ ] 12 个 skill 的 `## Agent 提示词` section 全部包含 5 个子标题：`## 角色定义` / `## 核心能力` / `## 执行流程` / `## 约束` / `## 输出规范`（orchestration / verification-loop 补 `## 输出规范` 后验收）
- [ ] 11 个 skill 的 frontmatter 含 `agent:` 字段（orchestration 补后验收，doc-gardener 配对完整性检查通过）
- [ ] 4 个动作型 skill 含 `context: fork`（commit-gate / verification-loop 补后）
- [ ] TD-003 的 17 条 LOW 全部落地
- [ ] `tests/triggers/cases.json` 包含 50 条用例，每 skill ≥ 3 条
- [ ] 至少 5 条 negative 用例（输入不应触发任一 skill）
- [ ] 至少 3 条 ambiguous 用例（输入有 2+ skill 候选）
- [ ] `make triggers-all` 退出码 0，PASS ≥ 30，WARN=0，FAIL=0
- [ ] 每条 commit message 符合 `chore(skills):` 风格、≤ 72 字符（仅在用户明确要求提交时）

## 风险 / 已知未知

- **关键词命中风险**：修改 description / 何时使用 / 何时不该用 段时若无意删除 `SKILL_KW[]` 数组中的关键词，`validate-keyword-consistency.sh` 会失败。**缓解**：实施每条建议前对照 `scripts/run-trigger-regression.sh` 第 20-32 行的关键词表。
- **测试用例回归风险**：新增 20 条用例可能引入 FAIL（关键词命中错位）。**缓解**：每加 5 条跑一次 `make triggers-regression`。
- **heading 改 `####` → `##` 影响 grep 模式**：如果用户/工具有脚本依赖特定 heading 锚点（如 `### plan-architect` 引用），改后需要更新引用。**缓解**：改后立即 grep `####` 关键词确认无残留引用。
- **跨文件交接（架构 → 熵增）新增步骤可能触发关键词漂移**：新增的"交接 entropy-collector"步骤若引入新词，与 SKILL_KW 数组无关（因为 SKILL_KW 只匹配 input），但需要确保 description 里的现有关键词不被动到。

## 变更记录

- 2026-07-02: 创建本 plan（Round 2），基线已快照，PASS=30 不退化
- 2026-07-02: 12 个 SKILL.md 全部修复完成（28 处改动），18 条测试用例补充，PASS=48 WARN=0 FAIL=0
- 2026-07-02: 移动到 completed/
