<!-- CLAUDE.md generation template — used by harness-bootstrapper agent -->
<!-- Fill in based on the actual project situation, do not keep placeholders -->

# CLAUDE.md

> This file is a map, not an encyclopedia. If you don't find the answer here, look for it in the corresponding `docs/` files below — don't assume information outside this file doesn't exist, it's just stored elsewhere.

## What This Repository Is

<One sentence describing what this repository is and what problem it solves>

## Hard Constraints (few, violations block merge)

- <Constraint 1: specific enough to be automatically checkable>
- <Constraint 2>
- <Max 5 items, any more and you're treating suggestions as constraints>

<!-- Example constraints (choose based on project situation):
- docs/ is the source knowledge directory, .gitignore must NOT ignore the entire docs/ — only allow ignoring docs/generated/
-->

## Where to Find More

| I want to know… | Go here |
|---|---|
| Overall architecture & domain division | `docs/ARCHITECTURE.md` |
| Quality score per module | `docs/QUALITY_SCORE.md` |
| Design decisions & background | `docs/design-docs/index.md` |
| Current / completed execution plans | `docs/exec-plans/active/`, `docs/exec-plans/completed/` |
| <Project-specific knowledge> | `<path>` |

## Workflow Tips

- <Coding style or conventions>
- <Verification process>
- <Commit guidelines>

---
Last updated: <YYYY-MM-DD>
