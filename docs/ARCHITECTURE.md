# ARCHITECTURE.md

这个文件定义跨领域的架构地图与依赖方向规则。规则要尽量被 `harness-architecture-boundaries` 技能里描述的方式编码成 lint/结构化测试,而不是只停留在文字描述。

## 领域划分

| 领域 | 简述 | 对应代码路径 |
|---|---|---|
| harness-repo-map | 仓库知识地图:入口文件(CLAUDE.md/AGENTS.md) + docs/ 骨架 | `skills/harness-repo-map/` |
| harness-exec-plans | 执行计划作为一等公民工件,跨上下文窗口交接 | `skills/harness-exec-plans/` |
| harness-architecture-boundaries | 分层架构与依赖方向的机械强制 | `skills/harness-architecture-boundaries/` |
| harness-verification-loop | Ralph Wiggum 自验证循环:实现→自检→测试→评审→修复 | `skills/harness-verification-loop/` |
| harness-observability-and-browser | 浏览器自动化 + 可观测性(日志/指标/追踪)验证 | `skills/harness-observability-and-browser/` |
| harness-golden-principles | 黄金原则编码 + 持续熵增清扫 | `skills/harness-golden-principles/` |
| harness-authoring | 元技能:扩展 harness 体系(新 skill/agent 脚手架) | `skills/harness-authoring/` |
| harness-bootstrap | 一键初始化 harness 结构(AGENTS.md + docs/ + .gitignore) | `skills/harness-bootstrap/` |
| harness-commit-gate | 提交质量门:diff 审查 + 测试验证 + commit message | `skills/harness-commit-gate/` |
| harness-project-intake | 项目接入分析:技术栈、架构骨架、项目卡片 | `skills/harness-project-intake/` |
| harness-orchestration | 技能编排与工作流路由:4 条标准工作流 + 决策树 | `skills/harness-orchestration/` |

## 每个 skill 的内部结构

所有 skill 遵循统一内部布局:

```
skills/<name>/
├── SKILL.md           # 方法论正文（被注入主对话上下文）
├── agents/            # 配对 Agent 定义
│   ├── <agent>.md     # Claude Code agent（YAML frontmatter + 系统提示词）
│   └── openai.yaml    # 平台特定功能对等定义文件（含 metadata/tools/system_prompt）
└── references/        # 模板和提示词引用
    ├── *-template.md  # 生成到目标项目 docs/ 的模板
    └── *-prompt.md    # Agent 系统提示词（Agent 工具用场景）
```

## 依赖方向规则

```
docs/  ←──  skills/<name>/SKILL.md
              │
              ├──→  agents/<agent>.md
              │       │
              │       └──→  references/*-prompt.md
              │
              └──→  references/*-template.md
```

- `SKILL.md` 可以引用(指向)`agents/` 和 `references/` 下的文件,反过来不行。
- `agents/<agent>.md` 可以引用 `references/` 下的提示词文件,但不能引用其他 skill 的内容。
- 各 skill **之间**不应有直接依赖或 import ——它们是并列的、可按需独立使用的集合。
- 跨 skill 引用只应通过 `docs/`(地图/索引)做单向的"指向那里"。
- `docs/` 是对整个仓库的投影,不是某个 skill 的附件——它引用所有 skill,但不被任何 skill 依赖。

## 机械强制现状

| 规则 | 强制方式 | 状态 |
|---|---|---|
| 每个 skill 必须有 SKILL.md + agents/ + references/ | check-skill-structure | ✅ 已强制 |
| Agent 定义文件的 frontmatter 完整性 | check-frontmatter | ✅ 已强制 |
| skill 目录命名规范(harness- 前缀 + kebab-case) | check-naming | ✅ 已强制 |
| docs/ 文件标记最后更新日期 | check-dates | ✅ 已强制 |
| 跨平台同步(.md ↔ openai.yaml 功能对等) | check-cross-platform-sync | ✅ 已强制 |

### 检查模式（boundary-auditor / doc-gardener 直接执行）

以下检查命令可被 agent 直接在仓库根目录执行。任何失败都应输出具体的修复指令。

**check-skill-structure** — 三件套完整性

```bash
# 检查每个 skill 目录是否包含 SKILL.md + agents/ + references/
for d in skills/harness-*/; do
  missing=""
  [ ! -f "${d}SKILL.md" ] && missing="$missing SKILL.md"
  [ ! -d "${d}agents" ] && missing="$missing agents/"
  [ ! -d "${d}references" ] && missing="$missing references/"
  if [ -n "$missing" ]; then
    echo "FAIL: ${d} 缺少:${missing}"
    echo "FIX:  在 ${d} 下创建缺失的文件/目录。参考 skills/harness-repo-map/ 的结构。"
  fi
done
```

**check-frontmatter** — Agent 定义文件的 6 字段完整性

```bash
# 检查每个 agents/*.md 的 YAML frontmatter 是否包含 name/description/type/tools/model/skills
required_fields="name description type tools model skills"
for f in skills/*/agents/*.md; do
  # 跳过 openai.yaml（不是 agent 定义文件）
  frontmatter=$(sed -n '/^---$/,/^---$/p' "$f")
  missing=""
  for field in $required_fields; do
    echo "$frontmatter" | grep -q "^${field}:" || missing="$missing $field"
  done
  if [ -n "$missing" ]; then
    echo "FAIL: ${f} frontmatter 缺少:${missing}"
    echo "FIX:  在 ${f} 的 YAML frontmatter 中补齐缺失字段。参考 skills/harness-repo-map/agents/doc-gardener.md 的格式。"
  fi
done
```

**check-naming** — 目录命名规范

```bash
# 检查 skills/ 下的目录是否以 harness- 为前缀且使用 kebab-case
for d in skills/*/; do
  name=$(basename "$d")
  # 跳过非 skill 目录
  [ "$name" = "references" ] && continue
  if ! echo "$name" | grep -qE '^harness-[a-z0-9]+(-[a-z0-9]+)*$'; then
    echo "FAIL: skills/${name}/ 命名不规范"
    echo "FIX:  目录名必须以 harness- 为前缀,使用 kebab-case（小写字母+数字+连字符）。例如: harness-my-skill"
  fi
done
```

**check-dates** — docs/ 文件的"最后更新"标记

```bash
# 检查 docs/ 下所有 .md 文件是否包含"最后更新"日期
find docs/ -name '*.md' -exec sh -c '
  if ! grep -q "最后更新" "$1"; then
    echo "FAIL: ${1} 缺少最后更新日期"
    echo "FIX:  在文件末尾添加: ---\n最后更新: $(date +%Y-%m-%d)"
  fi
' _ {} \;
```

**check-cross-platform-sync** — .md 与 openai.yaml 功能对等

```bash
# 检查每个 skill 的 agents/*.md 与 agents/openai.yaml 是否存在对应关系,以及 openai.yaml 三区块完整性
for skill_dir in skills/harness-*/; do
  skill=$(basename "$skill_dir")
  md_agents=()
  for f in "${skill_dir}agents/"*.md; do
    [ -f "$f" ] && md_agents+=("$f")
  done
  yaml="${skill_dir}agents/openai.yaml"
  if [ ${#md_agents[@]} -gt 0 ] && [ ! -f "$yaml" ]; then
    echo "FAIL: ${skill} has ${#md_agents[@]} agent .md but no openai.yaml"
    echo "FIX:  Create ${yaml} with metadata/tools/system_prompt blocks"
  fi
  if [ -f "$yaml" ]; then
    blocks=$(grep -cE '^(metadata|tools|system_prompt):' "$yaml")
    [ "$blocks" -lt 3 ] && echo "FAIL: ${yaml} has only $blocks/3 required blocks (metadata/tools/system_prompt)"
  fi
done
```

> 任何标记为"⚠️ 仅文档,未强制"的规则,都应该被当作待办——用 `boundary-auditor` agent 或 `doc-gardener` agent 巡检发现的违规实施强制,或者直接补上对应的 lint 规则。

## 数据边界规则

- `agents/openai.yaml` 是平台特定功能对等定义文件，包含 metadata（display_name、short_description）、tools（工具权限映射）、system_prompt（系统提示词）三个区块，用于跨平台同步。**不是** agent 定义文件——agent 的正式定义在 `agents/<name>.md` 的 YAML frontmatter 中（包含 name、description、type、tools、model、skills 六字段）。两者用途不同，不要混淆。
- 模板文件(`references/*-template.md`)是输出边界——它们生成到目标项目的 `docs/` 中,本仓库不应反向依赖目标项目的内容。
- 系统提示词(`references/*-prompt.md`)是 agent 行为的输入边界——它们必须包含明确的工具风险声明(`本 agent 是只读的/执行型的`)以及严格的步骤指令。
- `agents/<name>.md` 的系统提示词部分与 `references/<name>-prompt.md` 内容必须保持一致。两者用途不同（前者是 Codex/平台 agent 定义,后者是可独立加载的提示词）,但正文必须逐字相同。修改任一文件时,必须同步更新另一个。

---
最后更新: 2026-06-29
