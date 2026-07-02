# 12 Skills 审计建议清单（2026-07-02）

- 来源：12 个并发 subagent 五维评估
- 基线：triggers-check 12 OK / keyword-consistency 12 OK / triggers-regression PASS=30 WARN=0 FAIL=0 / prompts-sync-check pass=12 warn=0 fail=0
- 总建议数：**49 条**
- 严重程度分布：CRITICAL 4 / HIGH 4 / MEDIUM 21 / LOW 20

---

## CRITICAL（4 条，必须先处理）

### 1. harness-authoring — 教与硬约束相反的规则

- 位置：`skills/harness-authoring/SKILL.md:92-95`
- 当前：教 "`agents/<name>.md` 是 canonical 版本，修改 agent prompt 时只改 `agents/<name>.md`"
- 改为：教 "`SKILL.md` 的 `## Agent 提示词` section 是 Claude Code 平台的 canonical 版本"，"Codex 平台保留 `agents/openai.yaml`，其 `system_prompt` 必须与 `## Agent 提示词` 逐字一致"，"不再使用 `agents/<name>.md`"
- 理由：违反 AGENTS.md L12 硬约束；harness-authoring 是 11 个 skill 的母版，错误规则会污染 skill-scaffolder 生成
- effort: small

### 2. harness-commit-gate — allowed-tools 漏声明

- 位置：`skills/harness-commit-gate/SKILL.md:6`
- 当前：`allowed-tools: Bash(git *) Bash(npm *) Bash(bun *) Bash(cargo *)`
- 改为：追加 `Bash(vitest *) Bash(tsc *) Bash(bunx *) Bash(make *) Bash(just *)`
- 理由：方法论 L40-43 提到 vitest / tsc / bunx tsc，L53 提到 Makefile/Justfile，但 allowed-tools 未声明。沙箱会拒绝这些命令，验证流程被阻塞
- effort: trivial

### 3. harness-architecture-boundaries — description 措辞与执行模型矛盾

- 位置：`skills/harness-architecture-boundaries/SKILL.md:3`
- 当前："通过自定义 lint 规则和结构化测试机械化强制约束"
- 改为："通过 boundary-auditor agent 内联 Grep/Bash 检查机械化强制约束"
- 理由：L17/69/111 明确说"不需要预先配置独立 lint 工具链"，description 暗示存在独立工具链会误导
- effort: trivial

### 4. harness-exec-plans / observability-and-browser / golden-principles — 死链到 `agents/<name>.md`（3 处）

- `skills/harness-exec-plans/SKILL.md:87` — `agents/plan-architect.md` 死链
- `skills/harness-observability-and-browser/SKILL.md:97` — `agents/qa-verifier.md` 死链
- `skills/harness-golden-principles/SKILL.md:72` — `agents/entropy-collector.md` 死链
- 改为：删除行，或改为 `agents/openai.yaml`（Codex 平台副本）
- 理由：`completed/skills-prompt-polish-2026-07-02.md` Phase A.1-A.3 声称清理 3 处，但实际漏了这 3 处——计划与现状漂移
- effort: trivial × 3

---

## HIGH（4 条）

### 5. harness-bootstrap — description 提"CI 模板"但正文无内容

- 位置：`skills/harness-bootstrap/SKILL.md:3`
- 改为：从 description 删除"CI 模板"，或方法论补 CI 模板生成章节
- 理由：承诺/能力不一致
- effort: trivial

### 6. harness-authoring — L88 .md 指代模糊

- 位置：`skills/harness-authoring/SKILL.md:88`
- 改为：明确指向 `SKILL.md` 的 `## Agent 提示词` section
- 理由：会让人误以为存在独立的 `agents/<name>.md`
- effort: trivial

### 7. harness-commit-gate — Agent 提示词缺推送判定步骤

- 位置：`skills/harness-commit-gate/SKILL.md:117-118`
- 改为：在第 7 步后插入"处理推送"步骤，按"并推送/不推送/未提及"三档
- 理由：方法论 L72 已固定三档处理，Agent 段缺失导致子 agent 实际执行无推送判定
- effort: small

### 8. harness-golden-principles — L72 死链（见 CRITICAL #4，HIGH 不重复）

---

## MEDIUM（21 条，选要）

汇总分类（不展开原文，给定位+建议方向）：

| Skill | 位置 | 维度 | 摘要 |
|---|---|---|---|
| architecture-boundaries | L3 | trigger_precision | 触发词仅 2 个，建议扩到 5 个含"ARCHITECTURE.md 落地" |
| architecture-boundaries | L3 | description_clarity | 补"数据边界"三柱之一 |
| bootstrap | L3 | description_clarity | "一键"→"快速"，与多步骤流程一致 |
| bootstrap | L80-82 | internal_consistency | .gitignore 硬编码 JS 假设，改为按项目栈判断 |
| bootstrap | L96 | internal_consistency | 自检步骤与 Agent 段输出口径不一致 |
| commit-gate | L118 | internal_consistency | "变更文件数、行数"vs"变更摘要"两处口径漂移 |
| commit-gate | L93-126 | agent_prompt_quality | 缺"## 跳过条件"section 镜像 SKILL.md"何时不该用" |
| exec-plans | L91 | agent_prompt_quality | h3 + h2 层级断点，5 个 h2 子节悬挂在 h3 后 |
| observability-and-browser | L82-93 | internal_consistency | SKILL.md Agent 段比 openai.yaml short 30%+，需逐字对齐 |
| orchestration | L57-65 | internal_consistency | 交接点表与 references/routing-decision-tree.md 不等价 |
| orchestration | L110-113 | internal_consistency | Agent 段约束未复述 SKILL.md 硬约束"Workflow 1 不得跳过 project-intake" |
| project-intake | L119-149 | internal_consistency | h3 内嵌 5 个 h2 子节，破坏层级；建议降为 h4 |
| project-intake | L3 | internal_consistency | description 5 维度名与正文"分析五维度"不对应 |
| prompt-optimizer | L64 | internal_consistency | 五维评估表只覆盖 5 项，漏"变量字典""输出 schema" |
| prompt-optimizer | L133 | agent_prompt_quality | 填充顺序只点名 4 区块，漏 3 区块与主文档不对齐 |
| repo-map | L171-176 | internal_consistency | 输出规范与约束 4 条中 3 条重复，缺"报告结构/严重程度"格式 |
| repo-map | L154 | internal_consistency | 无条件验证 openai.yaml 在纯 opencode 项目里误报 |
| repo-map | L151 | agent_prompt_quality | "对应 agent 定义文件"措辞与硬约束矛盾（应指"内联 section"） |
| verification-loop | L122 | agent_prompt_quality | 缺卡住检测时机与诊断文件引用 |
| verification-loop | L117 | agent_prompt_quality | 完成定义描述抽象，缺 exec-plan schema 校验 |
| verification-loop | L129 | agent_prompt_quality | "立即停止"缺可执行路径（指向 stuck-loop-diagnostics.md） |

---

## LOW（20 条）

主要为：标点风格漂移（中英混用）、次级文案重复、措辞与 references/ 子文件不一致、与 openai.yaml 内容字节差异 ≤ 30%。详细见 subagent 原始输出，存档于本目录 `recommendations-raw.json`（待生成）。

---

## 立即可执行（Trivial effort）

17 条 trivial 建议可单 commit 落地，无需跨文件协调：

- architecture-boundaries: L3 × 3（CRITICAL #3 + 触发词扩展 + description_clarity 补"数据边界"）
- authoring: L84（自检清单补 agent 提示词位置）、L139（全角→半角标点）
- bootstrap: L3（"一键"→"快速"）、L22（when_to_use 删"run harness"）、L96（自检加文件清单）
- commit-gate: L6（allowed-tools 追加）、L118（口径统一）
- exec-plans: L87（删死链）
- golden-principles: L72（删死链）、L80（"只读执行"加粗）
- observability-and-browser: L97（删死链）
- orchestration: L16-19（与 when_to_use 对齐）
- project-intake: L3（维度名对齐）、L151-154（输出去重）、L134（fallback 标注）
- prompt-optimizer: L3（删触发场景段）、L96（补 3-7 步下限）、L120（加"## 何时不适用"）
- repo-map: L76（展开跨段引用）、L151（措辞改内联 section）、L154（加平台判定）、L171-176（输出规范改格式）
