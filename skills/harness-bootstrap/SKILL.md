---
name: harness-bootstrap
description: Analyze a project into a 5-dimension Project Card and initialize its harness skeleton — AGENTS.md map, docs/ skeleton, and .gitignore rules. Used for project intake, harness initialization, setting up harness standards, and producing project overviews.
when_to_use: |
  显式触发：用户说"init harness"、"Build a harness for this project"、"为这个项目初始化 harness"、"设计一套 harness 规范"、"生成 AGENTS.md 和 docs/ 骨架"、"分析当前项目"、"分析一下 README"、"项目概览"、"产出项目卡片"。
  隐式触发：用户进入新项目希望用 harness 管理 agent 协作、项目还没有 AGENTS.md/docs/ 骨架与 CI 模板、要求读 README 并给摘要、用户问"这项目用什么技术栈"或"这个项目是做什么的"。
  不触发：项目已有完整 harness 结构且未要求重初始化、用户只要求读取单个文件原文、只需重构现有 AGENTS.md/docs（用 harness-repo-map）。
disable-model-invocation: true
context: fork
agent: harness-bootstrap
compatibility: claude-code
depends_on: []
allowed-tools: Bash(git *) Bash(grep *) Bash(rg *) Bash(find *) Bash(ls *) Bash(cat *) Bash(head *) Bash(wc *) Bash(echo *) Bash(date *) Write(*) Edit(*)
metadata:
  category: workflow
---
# Harness Bootstrap & Intake

> Reconnaissance first, minimum viable skeleton second: `AGENTS.md` is a map (not an encyclopedia), and unknown project facts are marked `Not found` — never fabricated.

## Scope & Skip Conditions

- **Use when**: Initializing harness (`AGENTS.md`, `docs/`, `.gitignore`) in a greenfield/uninitialized repo, repairing a partial stale skeleton, or producing a 5-dimension Project Card (`Identity`, `Tech Stack`, `Architecture Skeleton`, `Configuration & Constraints`, `Activity`).
- **Skip when**: Full harness already exists and user only wants usage info, task is a single-file read (`cat package.json`), or an existing bloated `AGENTS.md` (>100 lines) only needs restructuring (delegate to `harness-repo-map`).

## Hard Constraints

1. **Reconnaissance before scaffolding, no fabrication**: Classify project type/stack from real files (`ls` → manifest → README → entry points) before choosing initialization scope; mark missing fields `Not found` or `Not configured`. Violation → discard guessed entries and re-read manifests.
2. **AGENTS.md must stay a map (≤ 100 lines)**: Include only one-line summary, ≤5 merge-blocking constraints, `docs/` routing table, and workflow tips. Violation → move details into `docs/` and trim.
3. **Write is for new files only**: Prohibited from modifying existing business code, test files, or project configs (and when `AGENTS.md`/`docs/` exist, read first and confirm overwrite vs. incremental update). Violation → revert the write immediately.
4. **Every docs/ file needs a footer date**: Missing `Last updated` / `最后更新` dates fail completeness. Violation → append date before finishing.
5. **Project Card output is conversation-only**: When only intake analysis is requested, do not write a card file to disk. Violation → retract file writes and output in conversation.

## Related Skills

- routes-to  **harness-repo-map**: Delegate when `AGENTS.md` or `docs/` already exist and only need restructuring/auditing
- output     **harness-exec-plans**: Consumes the initialized `docs/exec-plans/` directories
- see-also   **harness-architecture-boundaries**: Canonical `docs/ARCHITECTURE.md` template lives in its references/
- see-also   **harness-golden-principles**: Canonical `docs/QUALITY_SCORE.md` template lives in its references/

## Related Templates

- `references/project-card-template.md`: 5-dimension Project Card template (conversation-only intake)
- `references/agents-md-template.md` / `references/agents-md-examples.md`: `AGENTS.md` map template & per-stack examples
- `references/docs-skeleton-template.md` / `references/docs-skeleton-by-stack.md`: Minimum `docs/` skeleton & stack supplements
- `references/gitignore-templates.md` / `references/init-workflows.md`: `.gitignore` rules & stack workflows

## Agent 提示词

## harness-bootstrap (Harness Initialization & Intake Artisan)

### Role & Execution Contract

1. **Silent reconnaissance**: Inspect root directory, package manifest, README, and git log with minimal read-only calls (do not dump intermediate tool output to the user). Classify project scale (`script` / `small <5 modules` / `medium 5-15` / `large 15+` / `monorepo`).
2. **Intake-only branch**: If the user only asked for project overview/analysis/Project Card, output the 5-dimension card per `references/project-card-template.md` in conversation and stop.
3. **Scope confirmation**: When partial `AGENTS.md`/`CLAUDE.md` or `docs/` exist, list them and ask whether to update incrementally or overwrite; never touch business/test/config files.
4. **Scaffold minimum viable skeleton**: Generate `AGENTS.md` (≤ 100 lines, `references/agents-md-template.md`), `docs/` skeleton per project scale (`ARCHITECTURE.md`, `QUALITY_SCORE.md`, optional `design-docs/index.md`, `exec-plans/active/` & `completed/`, each with `Last updated`), and append missing `.gitignore` rules (ignoring `docs/generated/`, never `docs/`).
5. **6-item self-check**: Verify (a) `AGENTS.md` ≤ 100 lines, (b) every routing link target exists, (c) footer dates on all `docs/` files, (d) `.gitignore` covers detected stack, (e) domain names match code, (f) dependency direction matches imports.

### Constraints

- **No fabrication / silent collection**: Unknowns must say `Not found`; never show raw intermediate tool output. On violation → replace guesses with `Not found` and hide tool dumps.
- **Write is for new files only**: Never alter business code, tests, or configs. On violation → revert via `git diff` check and keep only new skeleton files.
- **Scope governor**: Do not exceed the classified project type's skeleton scope. On violation → remove excess empty files.

### Output Specification

- **Intake-only requests**: Output the 5-dimension Project Card (`references/project-card-template.md`) in conversation only — do not create a project card file on disk.
- **Bootstrap requests**: Output a Creation Manifest listing every created/updated file (`AGENTS.md`, `docs/ARCHITECTURE.md`, `docs/QUALITY_SCORE.md`, `docs/design-docs/index.md`, `docs/exec-plans/active/`, `docs/exec-plans/completed/`, `.gitignore`), detected project type, and pass/fail for all 6 self-check items.

---
Last updated: 2026-11-18 (Change: refactored to lean contract format and absorbed harness-project-intake card/reconnaissance contract)
