# Validation Checks（维护者参考）

## Skill Frontmatter QA（frontmatter 质量校验）

每个 `SKILL.md` 的 frontmatter 应包含 `description`、`when_to_use`、`compatibility` 字段，不应包含已废弃的 `version` 字段或正文中的 `## 触发信号` 节。仓库提供轻量校验脚本，用于防止格式漂移。

### 本地运行

```bash
python3 scripts/run-all.py --run-type check
```

### 校验规则

- 每个 skill 必须有 `description` 字段（≥ 20 字符）
- 每个 skill 必须有 `when_to_use` 字段
- 每个 skill 必须有 `compatibility` 字段
- 不应包含 `version` 字段或 `## 触发信号` 正文章节

> 该校验是**硬门禁**：字段缺失时 `validate_skill_triggers.py` 以 exit 1 结束，`scripts/run-all.py` 第一阶段即失败并阻断 CI（2026-10-08 修正了此前“warn-only 不阻断”的过时描述，并将输出标签由误导性的 `[WARN]` 改为 `[FAIL]`）。
### 本地全量检查（推荐）

六个阶段依次执行：frontmatter 校验 → 触发词回归 → Agent Prompt 存在性 → 依赖方向校验 → 单元测试 → 输出规格与任务覆盖审计。

```bash
python3 scripts/run-all.py
```

### Agent Prompt 存在性校验

`python3 scripts/run-all.py --run-type prompt` 验证每个 SKILL.md 是否包含 `## Agent 提示词` section。

```bash
python3 scripts/run-all.py --run-type prompt
```

### 依赖方向与循环依赖校验

`python3 scripts/run-all.py --run-type deps` 机械强制 skill 间的依赖方向（原 TD-001，此前仅靠人工 review）。

```bash
python3 scripts/run-all.py --run-type deps                # 校验
python3 scripts/validate_skill_dependencies.py --graph    # 打印依赖图
python3 scripts/validate_skill_dependencies.py --paths    # 列出跨 skill 路径引用
python3 tests/dependencies/test_dependency_validation.py  # 18 个回归用例
```

校验内容：

| 规则 | 级别 |
|---|---|
| `depends_on` 图中不得有环 | FAIL |
| Layer N 只能依赖 Layer ≤ N（向上引用即失败） | FAIL |
| 非 Meta 层 skill 不得依赖 Meta 层 skill | FAIL |
| `depends_on` 目标必须存在且已登记层级 | FAIL |
| SKILL.md/references 中 `../harness-*/references/*` 路径必须存在 | FAIL |
| 同层 skill 之间存在依赖 | WARN |
| `## Related Skills` 引用其他 skill 但无 `input`/`output`/`routes-to`/`see-also` 标注 | WARN |

新增 skill 时必须同步修改 `scripts/validate_skill_dependencies.py` 顶部的 `LAYERS` /
`META_LAYER` 常量——它们与 `docs/ARCHITECTURE.md` 的层级定义是同一份事实的两处拷贝。
