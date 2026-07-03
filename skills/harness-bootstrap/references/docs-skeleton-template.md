<!-- docs/ 目录骨架模板 — 由 harness-bootstrapper agent 使用 -->
<!-- 注意: ARCHITECTURE.md 和 QUALITY_SCORE.md 的 canonical 模板分别位于 harness-architecture-boundaries 和 harness-golden-principles。 -->

## 需要创建的文件列表

### docs/ARCHITECTURE.md

> 此文件的 canonical 模板位于 `harness-architecture-boundaries/references/architecture-template.md`。
> 初始化时请使用该模板的结构，保持评分维度与 golden-principles 体系一致。

### docs/QUALITY_SCORE.md

> 此文件的 canonical 模板位于 `harness-golden-principles/references/quality-score-template.md`。
> 初始化时请使用该模板的结构（结构一致性 / 黄金原则遵循度 / 测试覆盖 / 文档新鲜度），不要使用自定义评分维度。

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
