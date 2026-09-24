# CLAUDE.md

这个文件是地图，不是百科全书。如果你在这里没找到答案，去下面对应的 `docs/` 文件里找——不要假设这个文件之外的信息不存在，只是它被放在了别处。DO NOT send optional commentary.

> 本仓库是 **Harness Engineering Kit** 自身，不是被初始化的目标项目。目标项目在你执行 `harness-bootstrap` 后各自生成自己的 **CLAUDE.md**。
>
> Harness Engineering Kit：一套通用、与具体项目无关的 skills 套件，完美适配 Claude Code CLI。把 OpenAI 和 LangChain 两篇 harness engineering 文章的核心方法论，落地为可直接放进任意仓库的可执行工件。

## Quick start

```bash
python3 scripts/run-all.py                          # 全量验证
python3 scripts/run-all.py --run-type check         # 仅 frontmatter 校验
python3 scripts/run-all.py --run-type regression    # 仅关键词回归测试
python3 scripts/run-all.py --run-type regression --json  # 回归 JSON 报告
python3 scripts/run-all.py --run-type prompt        # 仅 agent prompt 检查
python3 scripts/run-all.py --run-type deps          # 仅依赖方向/循环依赖校验
python3 scripts/run-all.py --sync                   # 验证 + 同步到 ~/.agents/skills/ (并维护软链接)
```

## Navigation

关键文档：

| 我想知道… | 去看这里 |
|---|---|
| 13 个 skill 的分层架构与依赖方向 | `docs/ARCHITECTURE.md` |
| agent-first 的核心运作信念 | `docs/design-docs/core-beliefs.md` |
| 设计决策索引 | `docs/design-docs/index.md` |
| Agent Prompt 内联迁移设计 | `docs/design-docs/agent-prompt-inline-migration.md` |
| 设计决策详情 | `docs/design-docs/` |
| 当前执行计划 | `docs/exec-plans/active/` |
| Skill Quality Assessor 精炼计划 | `docs/exec-plans/completed/skill-quality-assessor-refinement.md` |
| 已知但暂不处理的技术债 | `docs/exec-plans/tech-debt-tracker.md` |
| 产品功能规格 | `docs/product-specs/index.md` |
| 各 skill 质量评分与趋势追踪 | `docs/QUALITY_SCORE.md` |
| 架构级变更记录（契约/CI/方法论变更） | `CHANGELOG.md` |
| Skills 质量评估报告 | `docs/quality-reports/skills-quality-assessment.md` |
| 质量报告详情 | `docs/quality-reports/` |
| 13 个 skill 的方法论正文 + agent 提示词 + 模板 | `skills/` |
| 详细的安装方式、触发速查表、回归用例维护规范 | `README.md` |

## 硬约束（违反即阻塞合并）

- 每个 `SKILL.md` 的 frontmatter 必须包含 `description`（>= 20 字符）、`when_to_use`、`compatibility` 字段，不含已废弃的 `version` 字段。
- 每个 skill 的 agent 提示词维护在 `SKILL.md` 的 `## Agent 提示词` section，不再使用独立的 `agents/<name>.md` 文件。
- 每个 `SKILL.md` 的 frontmatter 必须声明 `depends_on`（无依赖写 `depends_on: []`），只表达真实数据依赖；路由/参见/模板出处指针放 `## Related Skills`，用 `input`/`output`/`routes-to`/`see-also` 四标签标注。
- Skills 之间不允许循环依赖，依赖只能向下流动（Layer N → Layer ≤ N）；由 `scripts/validate_skill_dependencies.py` 机械强制。
- `compatibility` 和 `metadata`（含 `category`）为 harness 自定义 frontmatter 扩展字段，非 Claude Code 标准字段。Claude Code 会静默忽略未识别的字段。

## Architecture

详见 `docs/ARCHITECTURE.md`。依赖只能向下流动。同层可并行。元层可被任意层调用。

## Skill Invocation

所有 skill 均使用 `context: fork`，通过 subagent 独立执行。

- **3 个 `disable-model-invocation: true`**：`harness-bootstrap`、`harness-commit-gate`、`harness-verification-loop` — 不能直接用 Skill tool 调用，必须通过 `Agent` tool 或 Workflow 使用。
- **2 个 `allowed-tools` 受限**：`harness-commit-gate` 和 `harness-verification-loop` 分别将 Bash 限制为 `git`/`npm`/`bun`/`cargo`/`make`/`just` 子集。其余 skill 默认继承全部工具，不符合最小权限原则时应手动限制。
- Agent 提示词 canonical 版本在 `SKILL.md` 的 `## Agent 提示词` section，不再使用独立的 `agents/<name>.md` 文件。

## Quality gates

提交前必须运行全量验证脚本（`python3 scripts/run-all.py`，四阶段：frontmatter / 触发回归 / Agent Prompt / 依赖校验）。最后一次主观加权评分为第 33 次（2026-07-10，平均 9.46，5 A+ / 8 A）；第 34 次（2026-09-23）为机械检查点审计，13/13 全绿。详见 `docs/QUALITY_SCORE.md`。

## Skill 文件结构

```
skills/<name>/
├── SKILL.md           # 方法论正文 + frontmatter + ## Agent 提示词
└── references/         # 模板文件、边界情况指南
```

**frontmatter 字段说明**：`description`（做什么 + 什么时候用）、`when_to_use`（触发场景）、`context`（执行模式，如 `fork`）、`allowed-tools`（工具白名单）、`depends_on`（真实数据依赖，harness 自定义字段，仅本仓库校验脚本读取）。Claude Code 会静默忽略 `depends_on`。

## Testing

测试分两处：
- `tests/triggers/cases.json`（48 个触发回归用例）。关键词映射在 `scripts/run_trigger_regression.py` 的 `SKILL_KW` 字典。新增 skill 时必须同时更新关键词映射和测试用例。
- `tests/dependencies/test_dependency_validation.py`（18 个依赖校验用例，标准库 unittest）。新增 skill 时必须同时在 `scripts/validate_skill_dependencies.py` 的 `LAYERS`/`META_LAYER` 登记层级，否则该用例会失败。

## Development Workflow

修改 skill 后按此顺序操作：

1. 修改 `skills/<name>/SKILL.md`
2. 运行全量验证脚本（`python3 scripts/run-all.py`） 确保无断裂
3. 用 `harness-skill-quality-assessor` 评估修改质量
4. 提交前运行全量验证脚本（`python3 scripts/run-all.py`） — **这是硬约束，提交前必须通过**
5. 推送到 `develop` 分支（本仓库 PR 合并到 `main`）

> 工作方式提示详见 `docs/design-docs/core-beliefs.md`
> CI Pipeline 详见 `docs/references/ci-pipeline.md`

---

最后更新: 2026-09-24（变更：移除导航表中指向不存在文件的 `golden-principles-scan.md` 行——该路径是 golden-principles 在**目标项目**中的输出位置，不是本仓库的文件，放进导航表是错的）
