# 技术债追踪

已知但暂不处理的技术债。每条记录应说明：是什么、为什么不现在处理、什么条件下应该处理。

## 当前列表

| ID | 描述 | 发现日期 | 优先级 | 处理条件 |
|---|---|---|---|---|
| TD-001 | skill 间循环依赖未被脚本机械强制，仅靠人工 review | 2026-07-01 | Medium | 当 skill 数量增长到 15+ 或出现实际循环时 |
| TD-002 | openai.yaml 的 system_prompt 字段仍引用旧的 agent 提示词内容，需与 SKILL.md 中的 `## Agent 提示词` section 同步 | 2026-07-02 | Low | 当 Codex 平台需要使用 agent 提示词时 |
| TD-003 | 12 skills 五维审计发现 20 条 LOW 级建议（标点/文案/次级措辞），完整清单见 `docs/exec-plans/completed/skills-audit-2026-07-02.md` | 2026-07-02 | Low | 累计 LOW 数 > 50 或下一次审计周期 |

---
最后更新: 2026-07-02

## TD-003 详细清单

来自 12 skills 五维审计（`docs/exec-plans/completed/skills-audit-2026-07-02.md`），共 20 条 LOW 级建议：

| Skill | 位置 | 摘要 |
|---|---|---|
| harness-architecture-boundaries | L3 | description 补"数据边界"（已与 CRITICAL #3 合并处理） |
| harness-authoring | L139 | 全角标点"：""，"改半角 |
| harness-authoring | L84 | 自检清单补"agent 提示词位置"项 |
| harness-bootstrap | L22 | "何时使用"段删"run harness"触发词 |
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
| harness-observability-and-browser | L95 | 缺 "## 输出规范" section（已与 MEDIUM 合并处理） |
| harness-commit-gate | L120 | Agent 段缺"## 跳过条件"section（已与 MEDIUM 合并处理） |
