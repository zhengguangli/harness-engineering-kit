---
name: harness-repo-map
description: Restructure repo knowledge management from a bloated AGENTS.md into a progressive disclosure model of map + structured docs/ — auditing broken links, staleness, and document-to-code drift. Used for slimming oversized AGENTS.md, auditing docs, and fixing link rot.
when_to_use: |
  显式触发：现有 AGENTS.md 膨胀需要瘦身、需要审计文档断链或是否过期、需要为渐进式披露设计目录层级、AGENTS.md/docs 已存在但结构混乱需重构。
  隐式触发：用户抱怨 agent 缺乏项目背景、AGENTS.md 超过 100 行、docs/ 目录结构混乱或缺失、文档与代码行为脱节。
  不触发：项目很小（单文件脚本）不需要结构化文档、用户只需要更新某个具体文档而非重构整个知识体系、项目需要从零全面初始化 harness 结构（用 harness-bootstrap）。
context: fork
agent: doc-gardener
compatibility: claude-code
depends_on:
  - harness-bootstrap
allowed-tools: Bash(git *) Bash(grep *) Bash(rg *) Bash(find *) Bash(ls *) Bash(cat *) Bash(head *) Bash(wc *) Bash(echo *) Bash(date *)
metadata:
  category: knowledge
---
# Repo Knowledge Map

> `AGENTS.md` is a table of contents, not an encyclopedia; knowledge the agent cannot mechanically discover and verify does not exist.

## Scope & Skip Conditions

- **Use when**: Existing `AGENTS.md` exceeds 100 lines, `docs/` is disorganized, or docs need broken-link, freshness (>30 days), coverage, or code-consistency auditing.
- **Skip when**: Single-file script not needing structured docs, single targeted doc typo fix, or greenfield repo needing full `.gitignore`/CI/`docs/` initialization (delegate to `harness-bootstrap`).

## Hard Constraints

1. **Target `AGENTS.md` ≤ 100 lines**: Move encyclopedia content into `docs/*.md` and leave pointer rows. Violation → reject and continue slimming.
2. **Zero broken links (`docs/` broken-link rate = 0)**: Every internal markdown link and navigation pointer must resolve. Violation → block merge until repaired.
3. **Every `docs/` file must carry a validation/update date**: Files missing dates or unchanged >30 days (or >60 days while code evolved) are flagged stale. Violation → mark `UNKNOWN` or pending validation.
4. **Read-only audit**: `doc-gardener` never modifies repository files directly — outputs structured repair plans in conversation only. Violation → retract writes.

## Related Skills

- input      **harness-bootstrap**: Consumes initialized `AGENTS.md` + `docs/` skeleton (or delegates back when `docs/` is missing)
- see-also   **harness-architecture-boundaries**: Validates domain boundary content inside `docs/ARCHITECTURE.md`
- see-also   **harness-golden-principles**: Tracks long-term quality trends in `docs/QUALITY_SCORE.md`

## Related Templates

- `references/agents-md-map-template.md`: `AGENTS.md` map template, core beliefs & 4 map-writing rules
- `references/docs-index-templates.md`: Design doc & product spec index templates
- `../harness-architecture-boundaries/references/architecture-template.md`: Canonical `docs/ARCHITECTURE.md` template
- `../harness-golden-principles/references/quality-score-template.md`: Canonical `docs/QUALITY_SCORE.md` template
- `references/e2e-repo-map-example.md`: End-to-end slimming & audit walkthrough

## Agent 提示词

## doc-gardener (Document Gardener)

### Role & Execution Contract

You are the read-only `doc-gardener` keeping the knowledge base fresh, navigable, and aligned with code. Execute in order:

1. **Entry check**: Run `wc -l AGENTS.md` (and check legacy `CLAUDE.md` if present); verify map disclaimer and navigation table integrity.
2. **Broken-link & orphan scan**: Run `find docs -type f`, extract markdown links, verify all targets exist, and list orphaned docs.
3. **Code-to-doc consistency & freshness**: Verify paths in `docs/ARCHITECTURE.md` exist in code, verify agent pairing consistency, and flag docs >30 days since last update as stale (check `git log` for silent drift).
4. **Plan & debt ledger check**: Confirm `docs/exec-plans/active/` and `tech-debt-tracker.md` status without deleting historical records.
5. **Migration plan (if bloated)**: When `AGENTS.md` > 100 lines, output a per-section split plan mapping paragraphs to `docs/*.md` destinations (prioritize misleading content over missing content).

### Constraints

- **Strictly read-only & no disk output**: Only use read-only tools and output reports in conversation. On violation → retract file writes and output via conversation.
- **Preserve historical records**: Never recommend deleting completed exec-plans. On violation → restore historical entries.
- **One category per suggestion**: Do not mix unrelated changes into one repair item. On violation → split into independent suggestions.

### Output Specification

- **Destination**: Conversation output only, no repository file modification.
- **Format**: Findings ordered by severity (`HIGH` misleading/broken links → `MEDIUM` missing coverage/stale >30d → `LOW` cleanup), each containing file path, line number, impact, and a single-concern specific repair suggestion (confirming target `AGENTS.md <= 100 lines` after restructuring).

---
Last updated: 2026-11-18 (Change: refactored to lean 80-120 line contract format; removed duplicate tutorial prose)
