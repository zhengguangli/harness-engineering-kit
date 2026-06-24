# Harness Engineering Kit for Claude Code

一套通用、与具体项目无关的 Claude Code **skills + subagents** 套件,把 OpenAI《Harness engineering: leveraging Codex in an agent-first world》和 LangChain《The Anatomy of an Agent Harness》两篇文章里的核心方法论,落地成可以直接放进任意仓库的可执行工件。

> Agent = Model + Harness。模型提供智能,harness 提供让这份智能变成可靠产出所需要的一切:状态、工具、反馈回路、可机械强制的约束。这套工具集就是 harness 的一部分。

## 来源与核心论点

- **OpenAI**(`harness-engineering`,2026-02):用三位工程师、五个月时间,以"0 行人工手写代码"的约束,生成了百万行代码的产品。核心经验:AGENTS.md 应该是地图不是百科全书,docs/ 才是知识系统记录;架构边界要被机械强制而不是靠人工 review 维持品味;熵增需要持续的小颗粒度清扫而不是定期大扫除;agent 看不见的知识等于不存在。
- **LangChain**(`The Anatomy of an Agent Harness`,2026-03):把 harness 拆解为文件系统、bash/代码执行、沙箱、记忆与搜索、对抗 context rot 的机制(压缩、工具输出卸载、skills 渐进式披露)、长时程自主执行(规划 + 自验证 + Ralph Loop)。核心论点:这些都是"模型出厂时不具备、必须靠 harness 补上"的能力。

两篇文章的方法论高度互补——OpenAI 提供了"在真实大规模工程里怎么落地"的具体经验,LangChain 提供了"为什么每一个 harness 组件存在"的第一性原理推导。这套工具集按两者共同强调的几个支点组织。

## 目录结构

```
harness-engineering-kit/
├── skills/                              # 安装到 .claude/skills/<name>/SKILL.md
│   ├── harness-repo-map/                # AGENTS.md 地图 + docs/ 系统记录
│   ├── harness-exec-plans/              # 执行计划作为一等公民工件
│   ├── harness-architecture-boundaries/ # 分层架构与依赖方向的机械强制
│   ├── harness-verification-loop/       # Ralph Wiggum 自验证循环
│   ├── harness-observability-and-browser/ # 浏览器 + 可观测性反馈传感器
│   ├── harness-golden-principles/       # 黄金原则与持续垃圾回收
│   └── harness-authoring/               # 元技能:如何给这套体系本身加新能力
├── agents/                              # 安装到 .claude/agents/<name>.md
│   ├── plan-architect.md
│   ├── boundary-auditor.md
│   ├── verification-loop-runner.md
│   ├── qa-verifier.md
│   ├── doc-gardener.md
│   └── entropy-collector.md
```

> 模板文件(AGENTS.md、ARCHITECTURE.md、QUALITY_SCORE.md、docs/ 骨架等)已内嵌到各 skill 的 `references/` 子目录中,无需单独复制。

## 概念到组件的映射

| 文章里的概念 | 落地为 |
|---|---|
| AGENTS.md 作为地图,docs/ 作为系统记录,渐进式披露 | `harness-repo-map` skill + `doc-gardener` agent |
| 执行计划作为一等公民工件,跨上下文窗口接力 | `harness-exec-plans` skill + `plan-architect` agent |
| 分层架构、依赖方向、"约束不变量不管实现" | `harness-architecture-boundaries` skill + `boundary-auditor` agent |
| Ralph Wiggum Loop、"失败时问缺了什么能力" | `harness-verification-loop` skill + `verification-loop-runner` agent |
| Chrome DevTools 驱动验证、可观测性栈(日志/指标/追踪) | `harness-observability-and-browser` skill + `qa-verifier` agent |
| 黄金原则、熵增与垃圾回收、避免"AI 屎山大扫除日" | `harness-golden-principles` skill + `entropy-collector` agent |
| 文件系统作为持久状态、上下文是稀缺资源、skills 渐进式披露对抗 context rot | `harness-authoring` skill(指导如何写新的 skill/agent 而不破坏上下文预算) |
| 沙箱/隔离环境、bash 作为通用工具 | 不单独成一个 skill——这是 Claude Code 本身已经提供的基础能力,套件假定它存在并在 `harness-observability-and-browser` 里建议按 worktree 隔离环境 |

## 安装方式

Claude Code 的 skill 和 subagent 都是按位置发现的纯文本文件,直接复制即可,不需要额外注册步骤。

**项目级(推荐,纳入版本控制,团队共享)**

```bash
cp -r skills/*  <你的项目>/.claude/skills/
cp agents/*.md  <你的项目>/.claude/agents/
```

**用户级(跨项目个人习惯)**

```bash
cp -r skills/*  ~/.claude/skills/
cp agents/*.md  ~/.claude/agents/
```

项目级与用户级同名时,项目级优先。

**模板**:模板文件已内嵌在各 skill 的 `references/` 子目录中(如 `agents-md-map-template.md`、`architecture-template.md`、`quality-score-template.md` 等),由 agent 首次为项目初始化 docs/ 骨架时按需生成,无需手动拷贝。按项目实际架构和领域划分填空,不要把示例里的占位内容(如六层架构图)当作必须照搬的标准——它只是展示"固定方向 + 有限合法边数"这个模式。

## 推荐的接入顺序

1. 先落地 `harness-repo-map`:整理/瘦身 AGENTS.md,搭好 `docs/` 骨架。这是地基,其他一切都要靠 agent 能发现知识才生效。
2. 落地 `harness-architecture-boundaries`:明确依赖方向规则,哪怕一开始只能靠文档,逐步补上 lint。
3. 接入 `harness-exec-plans` + `plan-architect`:复杂任务开始用落盘计划驱动,而不是纯对话规划。
4. 接入 `harness-verification-loop` + `verification-loop-runner`:让改动的"完成"有可机械检查的定义。
5. 视项目类型接入 `harness-observability-and-browser` + `qa-verifier`(尤其是有 UI 或明确性能预算的项目)。
6. 最后接入 `harness-golden-principles` + `entropy-collector`,建立周期性清扫节奏,防止前面四步积累的产出慢慢腐化。
7. 任何时候要扩展这套体系本身,参考 `harness-authoring`。

## 关于 model / tools 字段的选择

各 agent 的 `model` 字段已经按"判断复杂度"而不是"任务大小"做了初步选择(`plan-architect` 用 `opus` 因为需要拆解判断;其余偏机械化巡检/执行的用 `sonnet`),`tools` 字段已经按最小权限原则配置(只读型 agent 不给 `Edit`/`Write`)。这些都是起点,不是教条——按你实际的成本预算和模型可用性调整,调整时建议保留"判断复杂度高的环节用更强模型"这条原则本身。

## 这套工具集刻意没有做的事

- 没有绑定任何具体语言/框架的 lint 工具链——每个 skill 里只给出"要机械强制什么、报错信息要包含什么"的模式,具体用 ESLint/dependency-cruiser/import-linter 还是自己写 AST 脚本,留给你的项目栈决定。
- 没有提供具体的 CI 配置文件——hook 接入方式因项目的 CI 系统而异,套件只规定"这些检查必须在 CI 里跑、报错要带修复指令",不规定怎么接。
- 没有附带浏览器自动化或可观测性后端的具体安装步骤——这部分应该使用 Claude Code 已连接的工具或项目已有的基础设施,本套件只规定"要有这类反馈传感器、怎么用它构成验证循环"。
