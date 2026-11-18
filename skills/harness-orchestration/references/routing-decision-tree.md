# Routing Decision Tree Reference

This file is an independently loadable reference for `harness-orchestration`.

## Three-Level Routing

```
What does the user want?
├── Initialize / Analyze new project → Workflow 1 (`bootstrap` → `repo-map` → optional `architecture-boundaries` + `golden-principles`)
├── Write / Modify code → Workflow 2
│   ├── Simple (single session) → skip `exec-plans`, `verification-loop` + `commit-gate`
│   └── Complex (cross-session) → `exec-plans` → `verification-loop` → `commit-gate`
│   └── Involves UI/performance? → trigger `observability-and-browser` within `verification-loop`
└── Fix quality / Clean up → Workflow 3
    ├── Pure taste drift → `golden-principles` → `verification-loop` → `commit-gate`
    └── Structural violations → `golden-principles` + `architecture-boundaries` → `verification-loop` → `commit-gate`
```

## Transition Point Table

| Upstream Skill | Artifact | Downstream Consumer |
|---|---|---|
| `bootstrap` | 5-dimension Project Card + `AGENTS.md` + `docs/` skeleton | `repo-map`, `exec-plans`, `architecture-boundaries`, `golden-principles` |
| `exec-plans` | `docs/exec-plans/active/<plan-id>.md` | `verification-loop` (executes steps & writes progress back) |
| `architecture-boundaries` | Layering rules / audit report | `verification-loop`, `commit-gate` |
| `observability-and-browser` | Screenshots / metric query evidence | `verification-loop`, `commit-gate` |
| `golden-principles` | Scan report / deviation queue | `verification-loop` |
| `repo-map` | `AGENTS.md` + doc health repair plan | `bootstrap` (verifies skeleton completeness) |

## Common Omissions

These 9 skills are used on demand — never run all of them every time:

- Small projects do not need `architecture-boundaries` (no multi-layer architecture to guard).
- Pure documentation changes do not need `verification-loop` or `observability-and-browser`.
- Projects that already have a well-established harness structure do not need to re-run Workflow 1.

---
Last updated: 2026-11-18 (Change: aligned routing tree and transition table with 9-skill / 3-workflow roster)
