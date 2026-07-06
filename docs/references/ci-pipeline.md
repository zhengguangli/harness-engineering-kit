# CI Pipeline

```yaml
push → main:      全量验证脚本（scripts/validate_skill_triggers.py → run_trigger_regression.py → validate_agent_prompt_sync.py）
PR → main:        确保 source 为 developer 分支 + 全量验证脚本
```

详情见 `.github/workflows/skill-triggers.yml`。PR 必须从 `developer` 分支发起，不可直接从特性分支向 `main` 提 PR。

---

Last updated: 2026-07-06
