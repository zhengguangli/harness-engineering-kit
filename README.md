# Harness Engineering Kit

一套通用、与具体项目无关的 **skills + agents** 套件,适用于 **Claude Code** 和 **Codex**。把 OpenAI《Harness engineering: leveraging Codex in an agent-first world》和 LangChain《The Anatomy of an Agent Harness》两篇文章里的核心方法论,落地成可以直接放进任意仓库的可执行工件。

> Agent = Model + Harness。模型提供智能,harness 提供让这份智能变成可靠产出所需要的一切:状态、工具、反馈回路、可机械强制的约束。这套工具集就是 harness 的一部分。

## 来源与核心论点

- **OpenAI**(`harness-engineering`,2026-02):用三位工程师、五个月时间,以"0 行人工手写代码"的约束,生成了百万行代码的产品。核心经验:AGENTS.md 应该是地图不是百科全书,docs/ 才是知识系统记录;架构边界要被机械强制而不是靠人工 review 维持品味;熵增需要持续的小颗粒度清扫而不是定期大扫除;agent 看不见的知识等于不存在。
- **LangChain**(`The Anatomy of an Agent Harness`,2026-03):把 harness 拆解为文件系统、bash/代码执行、沙箱、记忆与搜索、对抗 context rot 的机制(压缩、工具输出卸载、skills 渐进式披露)、长时程自主执行(规划 + 自验证 + Ralph Loop)。核心论点:这些都是"模型出厂时不具备、必须靠 harness 补上"的能力。

两篇文章的方法论高度互补——OpenAI 提供了"在真实大规模工程里怎么落地"的具体经验,LangChain 提供了"为什么每一个 harness 组件存在"的第一性原理推导。这套工具集按两者共同强调的几个支点组织。

## 目录结构

```
harness-engineering-kit/
├── .gitignore                           # 忽略 docs/、AGENTS.md、CLAUDE.md（均由 agent 按项目生成）
└── skills/                              # 11 个 skill（方法论 + agent 提示词 + 模板）
    ├── harness-architecture-boundaries/ # 分层架构与依赖方向的机械强制
    ├── harness-authoring/               # 元技能:如何给这套体系本身加新能力
    ├── harness-bootstrap/               # 一键初始化 harness 结构
    ├── harness-commit-gate/             # 提交质量门
    ├── harness-exec-plans/              # 执行计划作为一等公民工件
    ├── harness-golden-principles/       # 黄金原则与持续垃圾回收
    ├── harness-observability-and-browser/ # 浏览器 + 可观测性反馈传感器
    ├── harness-orchestration/           # 技能编排与工作流路由
    ├── harness-project-intake/          # 项目接入分析与项目卡片
    ├── harness-repo-map/                # 入口文件地图 + docs/ 系统记录
    └── harness-verification-loop/       # Ralph Wiggum 自验证循环
```

安装后由 agent 按项目生成的文件(不在仓库中):
- `AGENTS.md` — Codex 入口地图
- `CLAUDE.md` — Claude Code 入口地图
- `docs/` — 架构文档、执行计划、质量评分等

每个 skill 内部结构:
```
skills/<name>/
├── SKILL.md                             # 方法论正文
├── agents/
│   ├── <agent-name>.md                  # 配对 agent 的系统定义
│   └── openai.yaml                      # Codex UI 元数据（Claude Code 忽略）
└── references/
    ├── *-template.md                    # 模板文件（生成到目标项目的 docs/）
    └── *-prompt.md                      # Agent 系统提示词
```

## Skill 与 Agent 的使用方式

### 核心关系

```
Skill = 方法论（告诉"怎么做"）     → 注入主对话上下文
Agent = 执行者（在独立上下文中"动手做"） → spawn 后独立运行

主对话读 Skill → 理解方法论 → spawn Agent 去执行 → Agent 返回结果
```

Skill 不直接"调用" Agent。主对话根据 Skill 的指导决定何时 spawn 哪个 Agent。

### 单次任务的使用流程

以"实现一个新功能"为例:

```
用户: "帮我实现用户登录模块"
         │
         ▼
① harness-exec-plans 触发（主对话获得"如何做计划"的知识）
         │
         ▼
② spawn plan-architect agent
   → 独立上下文中创建 exec-plan 文件
   → 返回计划
         │
         ▼
③ spawn verification-loop-runner agent
   → 独立上下文中按计划逐步实现
   → 每步自检，必要时委派:
      ├── spawn boundary-auditor（检查架构边界）
      └── spawn qa-verifier（验证 UI/性能）
   → 返回完成结果
         │
         ▼
④ 验收通过 → 完成
```

### 11 个 Skill 的触发场景

| Skill | 触发时 | spawn 的 Agent |
|---|---|---|
| harness-repo-map | 搭建/重构入口文件和 docs/ | doc-gardener |
| harness-architecture-boundaries | 建立或检查架构边界规则 | boundary-auditor |
| harness-exec-plans | 复杂任务需要落盘计划 | plan-architect |
| harness-verification-loop | 把改动推进到"可合并"状态 | verification-loop-runner |
| harness-observability-and-browser | 需要 UI 或性能验证 | qa-verifier |
| harness-golden-principles | 周期性代码质量清扫 | entropy-collector |
| harness-authoring | 创建新的 skill 或 agent | skill-scaffolder |
| harness-bootstrap | 新项目首次初始化 harness 结构 | harness-bootstrapper |
| harness-commit-gate | 提交代码前质量门检查 | commit-gate-runner |
| harness-orchestration | 多 skill 组合路由决策 | （纯知识型，主对话直接执行） |
| harness-project-intake | 分析项目产出结构化卡片 | project-analyzer |

## 安装方式

### Claude Code

Skills 和 agents 都是按位置发现的纯文本文件,直接复制即可。

**项目级(推荐,纳入版本控制,团队共享)**

```bash
cp -r skills/*  <你的项目>/.claude/skills/
cp skills/*/agents/*.md  <你的项目>/.claude/agents/
```

**用户级(跨项目个人习惯)**

```bash
cp -r skills/*  ~/.claude/skills/
cp skills/*/agents/*.md  ~/.claude/agents/
```

项目级与用户级同名时,项目级优先。

### Codex

Skills 是 Codex 的能力扩展机制。安装到项目的 `.codex/skills/` 目录即可。

**项目级(推荐)**

```bash
mkdir -p <你的项目>/.codex/skills/
cp -r skills/*  <你的项目>/.codex/skills/
```

**用户级(跨项目)**

```bash
cp -r skills/*  ~/.codex/skills/
```

安装后重启 Codex 生效。

> 模板文件已内嵌在各 skill 的 `references/` 子目录中,由 agent 首次为项目初始化 docs/ 骨架时按需生成,无需手动拷贝。

## 推荐的接入顺序

1. 先落地 `harness-repo-map`:整理/瘦身入口文件,搭好 `docs/` 骨架。这是地基,其他一切都要靠 agent 能发现知识才生效。
2. 落地 `harness-architecture-boundaries`:明确依赖方向规则,哪怕一开始只能靠文档,逐步补上 lint。
3. 接入 `harness-exec-plans` + `plan-architect`:复杂任务开始用落盘计划驱动,而不是纯对话规划。
4. 接入 `harness-verification-loop` + `verification-loop-runner`:让改动的"完成"有可机械检查的定义。
5. 视项目类型接入 `harness-observability-and-browser` + `qa-verifier`(尤其是有 UI 或明确性能预算的项目)。
6. 最后接入 `harness-golden-principles` + `entropy-collector`,建立周期性清扫节奏,防止前面四步积累的产出慢慢腐化。
7. 任何时候要扩展这套体系本身,参考 `harness-authoring` + `skill-scaffolder`。

## 概念到组件的映射

| 文章里的概念 | 落地为 |
|---|---|
| 入口文件作为地图,docs/ 作为系统记录,渐进式披露 | `harness-repo-map` skill + `doc-gardener` agent |
| 执行计划作为一等公民工件,跨上下文窗口接力 | `harness-exec-plans` skill + `plan-architect` + `verification-loop-runner` agent |
| 分层架构、依赖方向、"约束不变量不管实现" | `harness-architecture-boundaries` skill + `boundary-auditor` agent |
| Ralph Wiggum Loop、"失败时问缺了什么能力" | `harness-verification-loop` skill + `verification-loop-runner` agent |
| Chrome DevTools 驱动验证、可观测性栈(日志/指标/追踪) | `harness-observability-and-browser` skill + `qa-verifier` agent |
| 黄金原则、熵增与垃圾回收、避免"AI 屎山大扫除日" | `harness-golden-principles` skill + `entropy-collector` agent |
| 渐进式披露、上下文预算、skill/agent 撰写规范 | `harness-authoring` skill + `skill-scaffolder` agent |

## 关于 model / tools 字段的选择

各 agent 的 `model` 字段已经按"判断复杂度"而不是"任务大小"做了初步选择(`plan-architect` 用 `opus` 因为需要拆解判断;其余偏机械化巡检/执行的用 `sonnet`),`tools` 字段已经按最小权限原则配置(只读型 agent 不给 `Edit`/`Write`)。这些都是起点,不是教条——按你实际的成本预算和模型可用性调整,调整时建议保留"判断复杂度高的环节用更强模型"这条原则本身。

## 这套工具集刻意没有做的事

- 没有绑定任何具体语言/框架的 lint 工具链——每个 skill 里只给出"要机械强制什么、报错信息要包含什么"的模式,具体用 ESLint/dependency-cruiser/import-linter 还是自己写 AST 脚本,留给你的项目栈决定。
- 没有提供具体的 CI 配置文件——hook 接入方式因项目的 CI 系统而异,套件只规定"这些检查必须在 CI 里跑、报错要带修复指令",不规定怎么接。
- 没有附带浏览器自动化或可观测性后端的具体安装步骤——这部分应该使用平台已连接的工具或项目已有的基础设施,本套件只规定"要有这类反馈传感器、怎么用它构成验证循环"。
