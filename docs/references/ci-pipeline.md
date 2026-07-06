# CI Pipeline

```yaml
push → main:      make triggers-all
PR → main:        确保 source 为 developer 分支 + make triggers-all
```

详情见 `.github/workflows/skill-triggers.yml`。PR 必须从 `developer` 分支发起，不可直接从特性分支向 `main` 提 PR。

---

Last updated: 2026-07-06
