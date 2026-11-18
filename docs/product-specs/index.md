# 产品规格索引

记录 harness-engineering-kit 的功能规格，作为 agent 理解"这套工具做什么、怎么用"的入口。

| 规格 | 一句话描述 | 状态 |
|---|---|---|
| README.md | 安装方式、触发速查表、接入顺序（维护者参考见 `docs/references/`） | shipped |
| skills/harness-bootstrap | 5 维度项目卡片分析 + 一键初始化（AGENTS.md + docs/ + .gitignore + CI） | shipped |
| skills/harness-repo-map | 入口文件地图 + docs/ 系统记录 | shipped |
| skills/harness-architecture-boundaries | 分层架构与依赖方向的机械强制 | shipped |
| skills/harness-exec-plans | 执行计划作为一等公民工件 | shipped |
| skills/harness-verification-loop | Ralph Wiggum 自验证循环 | shipped |
| skills/harness-golden-principles | 黄金原则与持续垃圾回收 | shipped |
| skills/harness-commit-gate | 提交质量门 | shipped |
| skills/harness-observability-and-browser | 浏览器 + 可观测性反馈传感器 | shipped |
| skills/harness-orchestration | 技能编排与工作流路由 | shipped |
| harness-project-intake | 项目卡片与侦察规范（已并入 `harness-bootstrap`） | merged |
| harness-authoring | 内部 skill 编写规范（已收归 `docs/references/skill-authoring-guide.md`） | retired |
| harness-skill-quality-assessor | skill 质量检查（已收归脚本门禁 `run-all.py` / `harness_check.py`） | retired |
| harness-prompt-optimizer | 结构化 Prompt 优化（已剥离出代码工程套件） | retired |

> 详细的 skill 触发场景和使用流程见 README.md 的"9 个 Skill 的触发场景"和"单次任务的使用流程"章节。

---
最后更新: 2026-11-18（变更：记录 13→9 套件减法，将 project-intake 标为 merged 并入 bootstrap，authoring/assessor/prompt-optimizer 标为 retired）
