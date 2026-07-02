---
name: harness-project-intake
description: 一键分析项目并产出结构化项目卡片——身份、技术栈、架构骨架、配置与约束、活跃度。用于"分析当前项目"、"项目概览"、"这个项目是做什么的"、"这项目用什么技术栈"场景。
when_to_use: |
  显式触发：用户说"分析当前项目"、"分析一下 README"、"项目概览"、"这个项目是做什么的"、"这项目用什么技术栈"。
  隐式触发：用户进入新项目目录后第一次对话说 hello 或简单问候、要求读 README.md 但期望得到摘要而非原文、问"这项目用什么技术栈"。
  不触发：用户明确只需要某个文件的内容（如 `cat package.json`）、用户已在本项目工作过不需要重新分析。
context: fork
agent: project-analyzer
compatibility: opencode
metadata:
  category: analysis
---

# Project Intake（项目接入分析）

## 核心原则

- **结论优先**：用户要的是结构化卡片，不是 `cat README.md` 的原始输出。读完文件后沉默地综合，只输出结论。
- **成本递增采集**：按 `ls → 包管理文件 → README → 目录骨架 → git log → rg 扫描` 的顺序采集，每一步都可能已足够产出卡片，避免过度探索。
- **不编造**：某维度信息缺失时写"未发现"或"未配置"，绝不猜测。

## 何时使用

- 用户说"分析当前项目"、"分析下项目"、"项目概览"、"这个项目是做什么的"。
  - 例如：用户刚克隆了一个项目，想快速了解项目概况
  - 例如：用户想了解项目的技术栈和架构
- 用户说"分析一下 README.md"、"读取 README.md"并期望得到摘要。
  - 例如：用户说"帮我看看README，这个项目是做什么的"
  - 例如：用户说"读取README，给我个摘要"
- 用户进入一个新项目目录，第一次对话时说 hello 或简单问候。
  - 例如：用户进入项目目录后说"你好"
  - 例如：用户进入项目目录后说"hi"
- 用户想了解项目的技术栈和架构。
  - 例如：用户问"这个项目用什么技术栈"
  - 例如：用户问"这个项目的架构是什么样的"
- 用户想了解项目的构建和运行方式。
  - 例如：用户问"怎么运行这个项目"
  - 例如：用户问"怎么测试这个项目"

## 何时不该用

- 用户明确只需要某个文件的内容（如 `cat package.json`），直接输出即可，无需生成卡片。
- 用户已经在该项目中工作过，不需要重新分析。

## 方法论

### 信息采集（6 步，按成本递增）

| 步骤 | 命令 | 采集维度 | 示例场景 |
|---|---|---|---|
| 1 | `ls -la` 项目根目录 | 文件类型、目录结构 | 查看项目根目录有哪些文件和目录 |
| 2 | `cat package.json` / `Cargo.toml` / `go.mod` / `pyproject.toml`（均不存在时 fallback：`ls` 推断语言，标注"推断（无包管理文件）"） | 语言、框架、运行时、依赖 | 查看Node.js项目的依赖和脚本 |
| 3 | `cat README.md`（只提取关键信息） | 项目自述、约束、构建命令 | 提取README中的项目描述和使用说明 |
| 4 | `find . -maxdepth 2 -type f \| head -50` | 目录骨架 | 查看项目目录结构 |
| 5 | `git log --oneline -10` | 近期活跃度、版本号 | 查看最近10次提交记录 |
| 6 | `rg` 扫描入口文件和关键模块 | 架构理解 | 搜索main、index、app等入口文件 |

### 分析五维度

1. **身份**：项目是什么、解决什么问题、一句话概述。
2. **技术栈**：语言、框架、运行时、包管理器、部署目标。
3. **架构骨架**：目录结构、入口文件、核心模块划分。
4. **配置与约束**：环境变量、构建命令、测试命令、部署方式。
5. **活跃度**：最近 commit、贡献者、版本号、CHANGELOG 状态。

### 输出格式

始终输出以下结构化卡片，不输出原始文件内容：

```markdown
## 项目卡片

**一句话概述**: <一句话说清楚这个项目是什么、做什么>

### 技术栈
| 维度 | 值 |
|---|---|
| 语言 | <语言及版本> |
| 框架 | <框架> |
| 运行时 | <Node/Bun/Deno/...> |
| 包管理 | <npm/bun/pnpm/cargo/...> |
| 部署目标 | <Cloudflare Workers/Vercel/Docker/...> |

### 目录骨架
<tree 风格展示关键目录和文件，标注每个顶层目录的职责>

### 关键模块
- **<模块名>**: <一句话职责>（`<文件路径>`）

### 构建与运行
- 安装: `<命令>`
- 开发: `<命令>`
- 测试: `<命令>`
- 构建/部署: `<命令>`

### 近期活跃
- 最近 commit: `<日期> — <摘要>`
- 版本: `<版本号>`（如可获取）

### 已知约束 / 注意事项
<从 README、配置文件或代码注释中提取的约束条件，如端口限制、API key 要求等>
```

## 硬约束

- **不编造信息**：卡片中不得出现任何编造内容（如猜测的版本号、臆断的框架）。若 verification-loop 发现编造信息，应打回并要求重新采集；若某维度确实无法获取，写"未发现"或"未配置"。
- **信息采集必须覆盖 package.json / README / 入口文件**：三者中任一缺失，必须在卡片对应维度标注"信息不完整"，不得跳过或用猜测填充。
- **无包管理文件时必须 fallback**：当 `package.json` / `Cargo.toml` / `go.mod` / `pyproject.toml` 均不存在时，执行 `ls` 观察文件后缀推断语言，并在卡片中标注"推断（无包管理文件）"。

## 关键要点

- 所有信息采集过程对用户不可见，只输出最终卡片。
- 5 维度信息应在 6-8 个工具调用内完成采集，不要反复探索。
- 发现 README 过时、配置缺失或明显问题时，在"已知约束"里注明。
- 定期审计项目分析结果，确保分析的有效性和适用性。
- 文档化分析决策，便于团队理解和遵循。

## 边界情况处理

> 通用边界情况（项目规模极小等）参见 `references/common-edge-cases.md`，以下仅列出本 skill 特有的边界情况。

### 项目无包管理文件

**场景**：项目没有package.json、Cargo.toml、go.mod、pyproject.toml等包管理文件
**处理**：执行ls观察文件后缀推断语言，标注"推断（无包管理文件）"

### README过时

**场景**：README中的信息已过时，与实际情况不符
**处理**：在"已知约束"里注明README过时，说明实际配置与README的差异

### 信息采集不完整

**场景**：package.json、README、入口文件三者中任一缺失
**处理**：在卡片对应维度标注"信息不完整"

### 多语言项目

**场景**：项目使用多种编程语言
**处理**：识别所有语言，分别说明每种语言的用途和依赖关系

## 最佳实践

### 信息采集最佳实践

1. **成本递增采集**
   - 按ls → 包管理文件 → README → 目录骨架 → git log → rg扫描的顺序
   - 每一步都可能已足够产出卡片
   - 避免过度探索

2. **静默采集**
   - 所有信息采集过程对用户不可见
   - 只输出最终卡片
   - 避免输出中间过程

3. **快速收敛**
   - 5维度信息采集在6-8个工具调用内完成
   - 不要反复探索
   - 够用即停

### 分析质量最佳实践

1. **结论优先**
   - 用户要的是结构化卡片，不是原始输出
   - 读完文件后沉默地综合
   - 只输出结论

2. **不编造信息**
   - 某维度信息缺失时写"未发现"或"未配置"
   - 绝不猜测
   - 确保信息真实可靠

3. **标注不确定性**
   - README过时时在"已知约束"里注明
   - 信息不完整时在对应维度标注
   - 推断信息时标注推断依据

### 输出格式最佳实践

1. **结构化输出**
   - 按项目卡片模板输出
   - 包含5个维度
   - 格式清晰易读

2. **信息完整**
   - 覆盖身份、技术栈、架构骨架、配置与约束、活跃度
   - 每个维度都有具体信息
   - 避免信息缺失

3. **问题标注**
   - README过时时注明
   - 信息不完整时标注
   - 配置缺失时说明

## 常见陷阱

- **甩原始数据**：把 `cat README.md` 的全文输出给用户——用户要的是结论，不是过程。
  - 解决方案：读取文件后沉默地综合，只输出结构化卡片
- **过度探索**：反复扫描目录和文件，浪费工具调用——按成本递增顺序，够用即停。
  - 解决方案：严格按6步采集顺序，每一步都可能已足够产出卡片
- **编造信息**：某维度无法获取时写"未发现"，不要猜测版本号、框架等。
  - 解决方案：信息缺失时写"未发现"或"未配置"，绝不猜测
- **忽略README过时**：README中的信息可能已过时。
  - 解决方案：发现README过时、配置缺失或明显问题时，在"已知约束"里注明
- **没有fallback机制**：没有包管理文件时不知道如何处理。
  - 解决方案：当package.json/Cargo.toml/go.mod/pyproject.toml均不存在时，执行ls观察文件后缀推断语言
- **信息采集不完整**：没有覆盖package.json/README/入口文件。
  - 解决方案：信息采集必须覆盖package.json/README/入口文件，三者中任一缺失必须在卡片对应维度标注"信息不完整"

## 相关模板

- `references/project-card-template.md`: 项目卡片 Markdown 模板
- `references/package-manifests.md`: 各语言包管理文件识别规则（Node.js/Python/Go/Rust/Java/PHP/Ruby/Dart/Swift/C#/Haskell）
- `references/project-structures.md`: 各语言项目结构分析与入口文件识别
- `references/tech-stack-detection.md`: 各语言框架、运行时、部署目标检测规则
- `references/activity-analysis.md`: 各语言活跃度分析命令与评级标准
- `references/automation-check-script.sh`: 自动化检查脚本

## 自动化检查

### 自动化检查脚本

```bash
#!/bin/bash
# Project Intake自动化检查脚本

SKILLS_DIR="./skills"
SKILL_NAME="harness-project-intake"
REPORT_FILE="docs/quality-reports/project-intake-check.md"

# 创建报告目录
mkdir -p docs/quality-reports

# 开始报告
echo "# Project Intake自动化检查报告" > "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "检查时间: $(date)" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

SKILL_FILE="$SKILLS_DIR/$SKILL_NAME/SKILL.md"

if [ -f "$SKILL_FILE" ]; then
    echo "## 检查结果" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    
    # 检查frontmatter
    echo "### Frontmatter检查" >> "$REPORT_FILE"
    if grep -q "^name:" "$SKILL_FILE"; then
        echo "- [x] name 字段存在" >> "$REPORT_FILE"
    else
        echo "- [ ] name 字段缺失" >> "$REPORT_FILE"
    fi
    
    if grep -q "^description:" "$SKILL_FILE"; then
        echo "- [x] description 字段存在" >> "$REPORT_FILE"
    else
        echo "- [ ] description 字段缺失" >> "$REPORT_FILE"
    fi
    
    # 检查标准章节
    echo "### 章节结构检查" >> "$REPORT_FILE"
    if grep -q "^## 核心原则" "$SKILL_FILE"; then
        echo "- [x] 核心原则章节存在" >> "$REPORT_FILE"
    else
        echo "- [ ] 核心原则章节缺失" >> "$REPORT_FILE"
    fi
    
    if grep -q "^## 何时使用" "$SKILL_FILE"; then
        echo "- [x] 何时使用章节存在" >> "$REPORT_FILE"
    else
        echo "- [ ] 何时使用章节缺失" >> "$REPORT_FILE"
    fi
    
    if grep -q "^## 方法论" "$SKILL_FILE"; then
        echo "- [x] 方法论章节存在" >> "$REPORT_FILE"
    else
        echo "- [ ] 方法论章节缺失" >> "$REPORT_FILE"
    fi
    
    # 检查示例数量
    example_count=$(grep -c "^### 示例\|^#### 示例\|^## 示例" "$SKILL_FILE" || echo "0")
    echo "### 示例统计" >> "$REPORT_FILE"
    echo "- 示例数量: $example_count" >> "$REPORT_FILE"
    
    # 检查错误处理指导
    if grep -q "错误处理\|故障排除\|常见问题" "$SKILL_FILE"; then
        echo "- [x] 包含错误处理指导" >> "$REPORT_FILE"
    else
        echo "- [ ] 缺少错误处理指导" >> "$REPORT_FILE"
    fi
    
    # 检查边界情况处理
    if grep -q "边界情况" "$SKILL_FILE"; then
        echo "- [x] 包含边界情况处理" >> "$REPORT_FILE"
    else
        echo "- [ ] 缺少边界情况处理" >> "$REPORT_FILE"
    fi
    
    # 检查最佳实践
    if grep -q "最佳实践" "$SKILL_FILE"; then
        echo "- [x] 包含最佳实践" >> "$REPORT_FILE"
    else
        echo "- [ ] 缺少最佳实践" >> "$REPORT_FILE"
    fi
    
    echo "" >> "$REPORT_FILE"
    echo "## 检查完成" >> "$REPORT_FILE"
else
    echo "## 错误" >> "$REPORT_FILE"
    echo "SKILL.md 文件不存在" >> "$REPORT_FILE"
fi

echo "自动化检查完成，报告已保存到 $REPORT_FILE"
```

### CI/CD集成

```yaml
name: Project Intake Check

on:
  push:
    paths:
      - 'skills/harness-project-intake/SKILL.md'
  pull_request:
    paths:
      - 'skills/harness-project-intake/SKILL.md'

jobs:
  quality-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Check project intake quality
        run: |
          bash scripts/project-intake-check.sh
```

## Agent 提示词

### project-analyzer

## 角色定义

你是「项目分析员」（project-analyzer）。快速、安静地采集项目信息，输出结构化项目卡片。用户要结论，不要过程。你擅长使用只读工具分析项目结构、技术栈、架构，能够识别包管理文件、README、入口文件等关键信息。

## 核心能力

- 只读信息采集：`ls`、`cat`、`find`、`git log`、`rg` 等只读命令
- 目录结构分析：`Glob` 枚举文件和目录
- 关键词搜索：`Grep` 定位入口文件和核心模块
- 文件阅读：`Read` 读取配置和文档文件
- 处理各种边界情况，提供最佳实践

## 执行流程

1. 读取 README.md → 提取项目名称和一句话描述（不输出全文）
   - 提取内容：
     - 项目名称
     - 一句话描述
     - 关键约束
     - 构建命令

2. 读取包管理文件（`package.json` / `Cargo.toml` / `go.mod` / `pyproject.toml`）→ 提取技术栈（参考 `references/package-manifests.md` 识别规则和 `references/tech-stack-detection.md` 框架检测）；若全部缺失，回退到 `ls` 观察文件后缀并标注"推断（无包管理文件）"
   - 提取内容：
     - 语言及版本
     - 框架
     - 运行时
     - 包管理器
     - 部署目标

3. `find . -maxdepth 2 -type f` 或 `ls -la` + `Glob` → 目录骨架（参考 `references/project-structures.md` 识别项目类型和入口文件）
   - 分析内容：
     - 顶层目录结构
     - 关键文件
     - 模块划分

4. `Grep` 搜索入口文件（main / index / app）→ 关键模块识别
   - 搜索内容：
     - 入口文件
     - 核心模块
     - 关键配置

5. 从 `package.json` scripts / `Makefile` / `Justfile` → 构建、测试、运行命令
   - 提取内容：
     - 安装命令
     - 开发命令
     - 测试命令
     - 构建/部署命令

6. `git log --oneline -10` → 近期 commit 和版本号（参考 `references/activity-analysis.md` 获取完整活跃度分析）
   - 提取内容：
     - 最近commit
     - 版本号
     - 贡献者

7. 按 `harness-project-intake` 的项目卡片模板输出结构化卡片
   - 输出内容：
     - 一句话概述
     - 技术栈
     - 目录骨架
     - 关键模块
     - 构建与运行
     - 近期活跃
     - 已知约束

8. 发现 README 过时、配置缺失、明显问题时在"已知约束"中注明
   - 注明内容：
     - README过时
     - 配置缺失
     - 明显问题

## 约束

- **只读不改**：禁止任何文件写入、删除、修改操作；禁止 `npm install`、`bun install` 等改变文件系统的命令。违反时撤回操作。
- **不编造信息**：信息缺失时写"未发现"或"未配置"，不猜测版本号、框架等。违反时将猜测内容替换为"未发现"。
- **静默采集**：所有信息采集过程对用户不可见，只输出最终卡片。违反时删除中间过程输出。
- **快速收敛**：5 维度信息采集在 6-8 个工具调用内完成。违反时停止探索，用已有信息输出卡片。
- **区分边界情况**：必须准确区分各种边界情况，不能混淆。违反时重新分类。
- **提供具体信息**：每个维度都必须提供具体信息，不能模糊。违反时补充具体信息。
- **处理边界情况**：必须处理各种边界情况，提供最佳实践。违反时补充边界情况处理。

## 输出规范

- **格式**：按 `harness-project-intake` 定义的项目卡片模板输出。
- **内容**：包含5个维度（身份、技术栈、架构骨架、配置与约束、活跃度）
- **原则**：结论优先，不编造信息，静默采集
- **边界情况处理**：针对不同边界情况提供处理方案
- **最佳实践**：提供信息采集、分析质量、输出格式的最佳实践

---
最后更新: 2026-07-02（变更：A+级优化，增加边界情况处理，增加最佳实践，增加自动化检查脚本，优化Agent提示词）
