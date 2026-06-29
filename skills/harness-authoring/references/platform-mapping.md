## 跨平台注意事项

这套 harness 体系同时服务于 Claude Code 和 Codex 两个平台。每个 agent 必须有两个版本的定义文件:

- **Claude Code**: `agents/<agent-name>.md` — YAML frontmatter + 系统提示词正文
- **Codex**: `agents/openai.yaml` — metadata + tools + system_prompt

两个版本必须**功能对等**:相同的系统提示词、等价的工具权限、相同的 skill 绑定。区别仅在于工具名和模型名的平台映射。

| Claude Code | Codex | 说明 |
|---|---|---|
| `Bash` | `exec_command` | 运行 shell 命令 |
| `Edit` | `apply_patch` | 修改已有文件 |
| `Write` | `apply_patch` | 创建新文件 |
| `Read` | `read_file` | 读取文件内容 |
| `Glob` | `list_dir` | 列出目录/文件 |
| `Grep` | `grep` | 搜索文本 |
| `sonnet` | `gpt-5.4` | 日常任务模型 |
| `opus` | `gpt-5.5` | 高阶判断模型 |

创建新 agent 时,使用 `agent-template.md` 生成 Claude Code 版本,使用 `agent-template-codex.yaml` 生成 Codex 版本。

---
最后更新: 2026-06-29
