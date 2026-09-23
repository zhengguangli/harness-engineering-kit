# CI Pipeline

```yaml
push → main:      python3 scripts/run-all.py
PR → main:        确保 source 为 develop 分支 + python3 scripts/run-all.py
```

详情见 `.github/workflows/skill-triggers.yml`。PR 必须从 `develop` 分支发起，不可直接从特性分支向 `main` 提 PR。

---

Last updated: 2026-09-23 (Change: refreshed freshness stamp; content unchanged)
