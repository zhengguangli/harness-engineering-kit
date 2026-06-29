<!-- docs/ 目录骨架模板 — 由 harness-bootstrapper agent 使用 -->

## 需要创建的文件列表

### docs/ARCHITECTURE.md

```markdown
# Architecture

## 领域划分

<项目的核心领域和边界>

## 依赖方向规则

<哪些模块可以依赖哪些模块,哪些不可以>

## 目录结构说明

<每个顶层目录的职责>

---
最后更新: <YYYY-MM-DD>
```

### docs/QUALITY_SCORE.md

```markdown
# Quality Score

## 评分标准

| 维度 | 权重 | 说明 |
|---|---|---|
| 测试覆盖 | 30% | ... |
| 架构合规 | 30% | ... |
| 文档完整度 | 20% | ... |
| 代码风格 | 20% | ... |

## 各模块评分

| 模块 | 测试 | 架构 | 文档 | 风格 | 总分 |
|---|---|---|---|---|---|
| <待填写> | | | | | |

---
最后更新: <YYYY-MM-DD>
```

### docs/design-docs/index.md

```markdown
# Design Decisions

## 索引

| 编号 | 标题 | 状态 | 日期 |
|---|---|---|---|
| <待填写> | | | |

---
最后更新: <YYYY-MM-DD>
```

### docs/exec-plans/active/ 和 docs/exec-plans/completed/

创建空目录。当有执行计划时,放入 `<日期>-<简述>.md` 文件。
