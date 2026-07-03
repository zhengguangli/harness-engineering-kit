# 端到端示例：React 项目知识库重构

## 场景背景

一个 React + TypeScript 项目，AGENTS.md 已膨胀到 350 行，包含架构说明、API 文档、部署流程、故障排查等所有内容。agent 经常找不到信息或读取过时内容。

目标：将百科全书式 AGENTS.md 重构为地图 + 结构化 docs/ 的渐进式披露模式。

---

## 步骤 1：盘点现状

**输入**：项目根目录

**操作**：

```bash
# 检查 AGENTS.md 行数
wc -l AGENTS.md

# 检查 docs/ 目录
ls -la docs/ 2>/dev/null || echo "docs/ 不存在"

# 检查现有文档结构
find . -name "*.md" -not -path "./node_modules/*" | head -20
```

**输出**：
```
350 AGENTS.md
docs/ 不存在
./README.md
./AGENTS.md
./CHANGELOG.md
```

**现状分析**：
- AGENTS.md：350 行（严重超标，应 ≤ 100 行）
- docs/：不存在
- 内容混杂：架构、API、部署、故障排查全在一个文件

---

## 步骤 2：设计目录骨架

**输入**：项目技术栈（React + TypeScript）和现状分析

**操作**：按需裁剪目标骨架

```
AGENTS.md                  # 瘦身到 ~80 行的地图
docs/
├── ARCHITECTURE.md        # 架构说明
├── QUALITY_SCORE.md       # 质量评分
├── design-docs/
│   ├── index.md           # 设计文档索引
│   └── core-beliefs.md    # 核心信念
├── exec-plans/
│   ├── active/
│   ├── completed/
│   └── tech-debt-tracker.md
├── generated/
├── product-specs/
│   └── index.md
└── references/
```

---

## 步骤 3：拆分搬运

**输入**：现有 AGENTS.md（350 行）

**操作**：按主题拆分到 docs/

### 3.1 创建 ARCHITECTURE.md

从 AGENTS.md 提取架构相关内容：

```markdown
---
title: React 项目架构
last_verified: 2026-07-02
related_code: src/
---

# 架构说明

## 技术栈
- React 18 + TypeScript
- Zustand 状态管理
- React Query 数据获取
- Tailwind CSS 样式

## 目录结构
src/
├── components/     # 可复用 UI 组件
├── pages/          # 页面组件
├── hooks/          # 自定义 hooks
├── services/       # API 服务层
├── stores/         # Zustand stores
└── types/          # TypeScript 类型

## 依赖方向
types → services → hooks → components → pages
stores → hooks → components → pages

## 状态管理
- 全局状态：Zustand stores（用户认证、主题设置）
- 服务端状态：React Query（API 数据缓存）
- 局部状态：useState/useReducer（组件内部状态）
```

### 3.2 创建 design-docs/core-beliefs.md

```markdown
---
title: 核心信念
last_verified: 2026-07-02
---

# 核心信念

## Agent-First 设计
- 所有文档必须可被 agent 机械化发现和校验
- 避免依赖人脑记忆或口头共识
- 渐进式披露：从小入口开始，教会 agent 去哪找更多

## 代码即文档
- 代码结构本身就是最好的文档
- 类型定义即接口契约
- 测试即使用示例

## 持续验证
- 文档必须与代码行为一致
- 过时的文档比没有文档更危险
- 定期审计确保文档新鲜度
```

### 3.3 创建 design-docs/index.md

```markdown
---
title: 设计文档索引
last_verified: 2026-07-02
---

# 设计文档索引

| 文档 | 用途 | 最后校验 |
|------|------|----------|
| [core-beliefs.md](./core-beliefs.md) | 核心运作信念 | 2026-07-02 |

## 新增文档
设计新功能时，先在 `docs/design-docs/` 创建 ADR（Architecture Decision Record）。
```

### 3.4 创建 product-specs/index.md

```markdown
---
title: 产品规格索引
last_verified: 2026-07-02
---

# 产品规格索引

| 规格 | 状态 | 最后更新 |
|------|------|----------|
| 用户认证流程 | 已实现 | 2026-06-15 |
| 订单管理功能 | 开发中 | 2026-07-01 |
```

### 3.5 创建 tech-debt-tracker.md

```markdown
---
title: 技术债跟踪
last_verified: 2026-07-02
---

# 技术债跟踪

## 待处理
| 项目 | 影响范围 | 创建日期 | 原因 |
|------|----------|----------|------|
| 迁移到 React Query v5 | services/ | 2026-06-20 | 旧版本不支持 Suspense |

## 已完成
| 项目 | 完成日期 | 解决方案 |
|------|----------|----------|
| - | - | - |
```

---

## 步骤 4：改写 AGENTS.md 为地图

**输入**：原 AGENTS.md（350 行）+ 步骤 3 的 docs/

**操作**：精简为 ~80 行的导航地图

```markdown
# 项目地图

> 这个文件是地图，不是百科全书；深入信息请看 docs/

## 快速导航

| 我想知道… | 去看这里 |
|---|---|
| 项目架构和分层规则 | `docs/ARCHITECTURE.md` |
| 设计决策和核心信念 | `docs/design-docs/` |
| 产品功能规格 | `docs/product-specs/index.md` |
| 执行计划和技术债 | `docs/exec-plans/` |
| 质量评分 | `docs/QUALITY_SCORE.md` |

## 目录结构

```
docs/
├── ARCHITECTURE.md        # 架构说明
├── QUALITY_SCORE.md       # 质量评分
├── design-docs/           # 设计文档
├── exec-plans/            # 执行计划
├── generated/             # 自动生成
├── product-specs/         # 产品规格
└── references/            # 第三方参考
```

## 工作方式

1. 先看本文件了解信息分布
2. 按需深入 docs/ 子目录
3. 不确定时，问用户或检查 docs/
```

---

## 步骤 5：质量验证

**输入**：重构后的 docs/ 结构

**操作**：doc-gardener agent 内联执行校验

### 5.1 断链检测

```bash
# 扫描 docs/ 内部链接
rg '\]\(\./' docs/ --no-filename | while read -r link; do
  # 提取链接目标并验证
  target=$(echo "$link" | sed 's/.*](\(.*\)).*/\1/')
  if [ ! -f "docs/$target" ]; then
    echo "断链: $link -> $target"
  fi
done
```

### 5.2 新鲜度检测

```bash
# 检查文档最后更新日期
rg "last_verified:" docs/ --no-filename | while read -r line; do
  date=$(echo "$line" | sed 's/.*: //')
  # 计算天数差
  days=$(( ($(date +%s) - $(date -j -f "%Y-%m-%d" "$date" +%s)) / 86400 ))
  if [ "$days" -gt 30 ]; then
    echo "过期文档: $line (已 $days 天)"
  fi
done
```

### 5.3 覆盖率检测

```bash
# 检查 ARCHITECTURE.md 是否覆盖所有目录
for dir in src/*/; do
  dirname=$(basename "$dir")
  if ! grep -q "$dirname" docs/ARCHITECTURE.md; then
    echo "未覆盖目录: $dirname"
  fi
done
```

---

## 步骤 6：生成报告

**输出**：

```markdown
## 文档健康报告

### 总结
- 问题总数：3
- HIGH：1（断链）
- MEDIUM：1（覆盖率不足）
- LOW：1（建议改进）

### 详细发现

### [HIGH] AGENTS.md 导航表断链
- 文件: `AGENTS.md`, 行号: L15
- 问题: 导航表指向 `docs/QUALITY_SCORE.md`，但该文件不存在
- 影响: agent 无法找到质量评分信息
- 修复: 创建 `docs/QUALITY_SCORE.md` 或更新导航表

### [MEDIUM] ARCHITECTURE.md 未覆盖 hooks/ 目录
- 文件: `docs/ARCHITECTURE.md`
- 问题: `src/hooks/` 目录存在但未在架构说明中描述
- 影响: agent 不了解 hooks 层的职责
- 修复: 在 ARCHITECTURE.md 中添加 hooks/ 说明

### [LOW] design-docs/ 文档较少
- 文件: `docs/design-docs/`
- 问题: 只有 2 个文档，建议补充更多设计决策记录
- 影响: 团队决策历史不完整
- 修复: 新功能开发时创建 ADR 文档
```

---

## 错误处理

### 场景 1：docs/ 目录创建失败
**处理**：检查文件系统权限，确认父目录存在，重新创建。

### 场景 2：内容拆分后信息丢失
**处理**：对比原 AGENTS.md 和新 docs/，确保所有关键信息被迁移。

### 场景 3：文档与代码不一致
**处理**：doc-gardener 标记为 HIGH 优先级，优先修复误导性内容。

---

## 验收标准

- [ ] AGENTS.md ≤ 100 行
- [ ] docs/ 断链率 = 0
- [ ] 每个 docs/ 文件有元数据头（title, last_verified）
- [ ] ARCHITECTURE.md 覆盖所有顶层目录
- [ ] 导航表指向的文件全部存在
