<!-- 各语言活跃度分析 — 由 project-analyzer agent 使用 -->
<!-- 从 git log、包管理文件、配置文件中提取项目活跃度信息 -->

## 活跃度维度

| 维度 | 数据来源 | 命令/方式 |
|---|---|---|
| 最近提交 | git log | `git log --oneline -10` |
| 提交频率 | git log | `git log --oneline --since="30 days ago"` |
| 贡献者 | git shortlog | `git shortlog -sn --no-merges` |
| 版本号 | 包管理文件 / git tag | `git describe --tags --abbrev=0` |
| CHANGELOG | CHANGELOG.md / CHANGES.md | 文件存在性 + 最后更新 |
| 依赖更新 | lock 文件修改时间 | 文件元信息 |
| Issue 活跃度 | GitHub CLI | `gh issue list --limit 5` |
| PR 活跃度 | GitHub CLI | `gh pr list --limit 5` |

## Git 分析命令

### 基本活跃度

```bash
# 最近 10 次提交
git log --oneline -10

# 最近 30 天提交频率
git log --oneline --since="30 days ago" | wc -l

# 最近提交日期
git log -1 --format="%ai"

# 贡献者排名
git shortlog -sn --no-merges | head -10

# 最活跃的提交时间（小时分布）
git log --format="%ad" --date=format:"%H" | sort | uniq -c | sort -rn
```

### 版本信息

```bash
# 最新 tag
git describe --tags --abbrev=0 2>/dev/null

# 所有 tag（按版本排序）
git tag --sort=-v:refname | head -10

# 最近 tag 的日期
git log -1 --format="%ai" $(git describe --tags --abbrev=0 2>/dev/null) 2>/dev/null
```

### 代码量统计

```bash
# 按语言统计行数（需安装 cloc）
cloc --json .

# 简单统计（按后缀）
find . -name "*.ts" -o -name "*.js" | xargs wc -l | tail -1
```

## 各语言版本检测

### Node.js / TypeScript

```bash
# 从 package.json 提取版本
cat package.json | jq '.version'

# 从 .nvmrc 或 .node-version 提取 Node 版本
cat .nvmrc 2>/dev/null || cat .node-version 2>/dev/null

# 从 package.json engines 提取
cat package.json | jq '.engines.node'
```

### Python

```bash
# 从 pyproject.toml 提取版本
grep '^version' pyproject.toml

# 从 setup.py 提取版本
grep 'version=' setup.py

# 从 __init__.py 提取版本
grep '__version__' src/*/__init__.py 2>/dev/null
```

### Go

```bash
# 从 go.mod 提取模块名和版本
head -3 go.mod

# 从 git tag 提取版本
git describe --tags --abbrev=0 2>/dev/null
```

### Rust

```bash
# 从 Cargo.toml 提取版本
grep '^version' Cargo.toml

# 从 git tag 提取版本
git describe --tags --abbrev=0 2>/dev/null
```

### Java / Kotlin

```bash
# Maven 项目从 pom.xml 提取版本
grep '<version>' pom.xml | head -1

# Gradle 项目从 build.gradle 提取版本
grep 'version' build.gradle | head -1
```

### PHP

```bash
# 从 composer.json 提取版本
cat composer.json | jq '.version'

# 从 Laravel 获取版本
php artisan --version 2>/dev/null
```

### Ruby

```bash
# 从 gemspec 提取版本
grep 'version' *.gemspec 2>/dev/null

# 从 Rails 获取版本
rails --version 2>/dev/null
```

## CHANGELOG 检测

```bash
# 检查 CHANGELOG 文件存在性
ls CHANGELOG.md CHANGES.md HISTORY.md CHANGES.rst 2>/dev/null

# 提取最近更新条目（前 20 行）
head -20 CHANGELOG.md 2>/dev/null

# 检查最后更新日期
head -5 CHANGELOG.md | grep -i "date\|version\|##" 2>/dev/null
```

## GitHub 活跃度（如有 GitHub CLI）

```bash
# 最近 5 个 issue
gh issue list --limit 5 --json title,createdAt,state

# 最近 5 个 PR
gh pr list --limit 5 --json title,createdAt,state

# 最近 release
gh release list --limit 5

# 仓库统计
gh repo view --json stargazerCount,forkCount,createdAt,pushedAt
```

## 活跃度评级

| 指标 | 活跃 | 一般 | 不活跃 |
|---|---|---|---|
| 最近提交 | < 7 天 | 7-30 天 | > 30 天 |
| 月提交数 | > 20 | 5-20 | < 5 |
| 贡献者数 | > 5 | 2-5 | 1 |
| 版本更新 | < 3 月 | 3-12 月 | > 12 月 |
| CHANGELOG | 有且更新 | 有但过时 | 无 |

## 输出格式

活跃度信息按以下格式输出到项目卡片：

```markdown
### 近期活跃

- 最近 commit: `2024-01-15 — fix: resolve auth middleware bug`
- 版本: `v2.1.0`（2024-01-10）
- 贡献者: 5 人（近 30 天）
- 月提交数: 23 次
- 活跃度: 活跃

### 已知约束 / 注意事项

- CHANGELOG 最后更新于 2023-06，可能过时
- 依赖 `lodash` 版本较旧，建议升级
```

## 边界情况处理

### 无 git 历史

**场景**：项目没有 git 仓库或 git 历史为空
**处理**：活跃度维度标注"无 git 历史"

### 单次提交项目

**场景**：项目只有一次初始提交
**处理**：标注"单次提交项目，可能为模板或示例"

### Fork 项目

**场景**：项目是 fork 的，有上游仓库
**处理**：检查是否有独立提交，标注 fork 来源

### 空仓库

**场景**：仓库存在但没有有意义的代码
**处理**：标注"空仓库或初始化中"
