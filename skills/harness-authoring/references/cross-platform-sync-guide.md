# 跨平台 System Prompt 同步指南

## 核心规则

每个 agent 在 Claude Code 平台（`SKILL.md` 的 `## Agent 提示词` section）和 Codex 平台（`agents/openai.yaml` 的 `system_prompt` 字段）的 system_prompt **必须逐字一致**。

## 仅允许的差异：工具名映射

| Claude Code | Codex | 说明 |
|---|---|---|
| `Bash` | `exec_command` | 命令执行 |
| `Edit` | `apply_patch` | 文件编辑 |
| `Write` | `create_file` | 文件创建 |
| `Read` | `read_file` | 文件读取 |
| `Grep` | `search_content` | 内容搜索 |
| `Glob` | `search_files` | 文件搜索 |

**注意**：仅工具名不同，工具的描述、参数、行为说明必须完全一致。

## 同步验证流程

### 手动验证

1. 提取 SKILL.md 中 `## Agent 提示词` 下的 system_prompt
2. 提取 agents/openai.yaml 中的 `system_prompt` 字段
3. 替换工具名映射
4. 逐字对比差异

### 自动化验证脚本

```bash
#!/bin/bash
# 跨平台同步检查脚本

SKILL_DIR="$1"
SKILL_MD="$SKILL_DIR/SKILL.md"
OPENAI_YAML="$SKILL_DIR/agents/openai.yaml"

if [ ! -f "$SKILL_MD" ] || [ ! -f "$OPENAI_YAML" ]; then
    echo "❌ 文件缺失：SKILL.md 或 agents/openai.yaml"
    exit 1
fi

# 提取 SKILL.md 中的 agent prompt（## Agent 提示词 section 之后的内容）
md_prompt=$(awk '/^## Agent 提示词$/,0' "$SKILL_MD" | tail -n +2)

# 提取 openai.yaml 中的 system_prompt
yaml_prompt=$(awk '/^system_prompt:/,/^[a-z]/' "$OPENAI_YAML" | head -n -1 | tail -n +2 | sed 's/^  //')

# 替换工具名映射（Codex → Claude Code）
yaml_prompt_normalized=$(echo "$yaml_prompt" \
    | sed 's/exec_command/Bash/g' \
    | sed 's/apply_patch/Edit/g' \
    | sed 's/create_file/Write/g' \
    | sed 's/read_file/Read/g' \
    | sed 's/search_content/Grep/g' \
    | sed 's/search_files/Glob/g')

# 对比
if [ "$md_prompt" = "$yaml_prompt_normalized" ]; then
    echo "✅ 同步检查通过"
else
    echo "❌ 同步检查失败：system_prompt 不一致"
    echo "--- 差异 ---"
    diff <(echo "$md_prompt") <(echo "$yaml_prompt_normalized")
    exit 1
fi
```

### CI/CD 集成

```yaml
# .github/workflows/sync-check.yml
name: Cross-Platform Sync Check

on:
  push:
    paths:
      - 'skills/*/SKILL.md'
      - 'skills/*/agents/openai.yaml'
  pull_request:
    paths:
      - 'skills/*/SKILL.md'
      - 'skills/*/agents/openai.yaml'

jobs:
  sync-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Check sync for all skills
        run: |
          for skill_dir in skills/*/; do
            if [ -f "$skill_dir/agents/openai.yaml" ]; then
              echo "检查 $skill_dir ..."
              bash scripts/cross-platform-sync-check.sh "$skill_dir"
            fi
          done
```

## 常见漂移场景与预防

### 场景一：只改了一处

**问题**：修改了 SKILL.md 的 agent prompt，忘记同步 openai.yaml

**预防**：
- 修改 agent prompt 时，同时打开两个文件
- 用自动化检查脚本验证
- 在 CI/CD 中加入同步检查

### 场景二：措辞微妙不同

**问题**：两处内容"意思一样但措辞不同"

**预防**：
- 明确"逐字一致"的标准——不是"意思一致"而是"文字一致"
- 用 diff 工具对比，不靠肉眼

### 场景三：一处比另一处更详细

**问题**：SKILL.md 的 prompt 比 openai.yaml 的更详细（或反之）

**预防**：
- 确定 canonical 版本（SKILL.md 的 `## Agent 提示词`）
- 修改时以 canonical 版本为准
- openai.yaml 必须与 canonical 版本同步

## Canonical 版本约定

- **`SKILL.md` 的 `## Agent 提示词` section** 是 canonical 版本
- 修改 agent prompt 时，**只改此处**
- openai.yaml 的 `system_prompt` 必须从 canonical 版本同步过来
- 仓库硬约束：不再使用独立的 `agents/<name>.md` 文件

## 同步检查清单

每次修改 agent prompt 时：

- [ ] 修改的是 SKILL.md 的 `## Agent 提示词` section（canonical 版本）
- [ ] agents/openai.yaml 的 `system_prompt` 已同步
- [ ] 工具名已正确映射
- [ ] 逐字对比无差异
- [ ] 自动化检查脚本通过
- [ ] 没有创建独立的 `agents/<name>.md` 文件

## 新建 Agent 时的同步流程

1. 先写 SKILL.md 的 `## Agent 提示词` section（canonical 版本）
2. 从 canonical 版本生成 openai.yaml 的 `system_prompt`（替换工具名）
3. 用同步检查脚本验证
4. 不要创建 `agents/<name>.md` 文件
