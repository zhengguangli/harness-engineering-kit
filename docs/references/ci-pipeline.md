# CI Pipeline

```yaml
push → main:      python3 scripts/run-all.py
PR → main:        确保 source ∈ {develop, main, release/*} + python3 scripts/run-all.py
                 + 逐个 skills/*/references/automated_check_script.py
```

详情见 `.github/workflows/skill-triggers.yml`。PR 必须从 `develop` / `main` / `release/*`
发起，不可直接从特性分支向 `main` 提 PR。

`run-all.py` 六阶段：frontmatter 校验 → 触发词回归（51 用例）→ Agent Prompt 存在性 →
依赖方向校验（`validate_skill_dependencies.py`）→ 单元测试 → 输出规格与任务覆盖审计。新增 skill 时第四阶段会因未登记
`LAYERS`/`META_LAYER` 而失败——这是有意的强制点。

skill 级自动化检查在 CI 中为 warn-only（不阻断）；只有 `run-all.py` 失败才阻断。

---

Last updated: 2026-10-08 (Change: corrected the pipeline description to six stages and 51 regression cases — the tests and audit stages added on 2026-09-24 were missing)
