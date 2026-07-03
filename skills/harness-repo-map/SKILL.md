---
name: harness-repo-map
description: Restructure repo knowledge management from a bloated CLAUDE.md into a progressive disclosure model of map + structured docs/ — avoiding context bloat and document rot. Used for sliming oversized CLAUDE.md, building docs structure from scratch, auditing broken links, and fixing outdated docs.
when_to_use: |
  显式触发：项目需要从零搭建 CLAUDE.md/docs 结构、现有 CLAUDE.md 膨胀需要瘦身、需要审计文档是否过期、需要为渐进式披露设计目录层级。
  隐式触发：用户抱怨 agent 缺乏项目背景、CLAUDE.md 超过 100 行、docs/ 目录结构混乱或缺失、文档与代码行为脱节。
  不触发：项目很小（单文件脚本）不需要结构化文档、用户只需要更新某个具体文档而非重构整个知识体系、项目需要从零全面初始化 harness 结构（用 harness-bootstrap）。
context: fork
agent: doc-gardener
compatibility: claude-code
allowed-tools: Bash(git *) Bash(grep *) Bash(rg *) Bash(find *) Bash(ls *) Bash(cat *) Bash(head *) Bash(wc *) Bash(echo *) Bash(date *)
metadata:
  category: knowledge
---

# Repo Knowledge Map

## Core Principles

- **CLAUDE.md is a map, not an encyclopedia**: A bloated CLAUDE.md is an anti-pattern — it consumes context quota, can't be mechanically validated, and rots instantly. The right approach is to treat CLAUDE.md as a table of contents pointing to the sources of truth in `docs/`.
- **Knowledge must be mechanically discoverable and verifiable**: Google Docs, Slack discussions, and "team consensus" stored only in people's brains — if they aren't written into the repository, they might as well never have happened. Documentation must exist in a way that agents can mechanically discover and validate.
- **Progressive disclosure**: The agent starts from a small entry point and is taught where to find more. Don't cram all information into a single file.

## When to Use

- The project has no CLAUDE.md / docs structure yet and needs to be built from scratch.
- An existing CLAUDE.md has ballooned to hundreds of lines and needs to be "slimmed into a map" with content moved down to `docs/`.
- Documentation needs auditing for staleness, broken links, or divergence from actual code behavior.
- Directory hierarchy needs to be designed for progressive disclosure.
- Users report that the agent lacks project context.

## When Not to Use

- The project is small (single-file script) and doesn't need structured documentation.
- The user only needs to update a specific document rather than restructure the entire knowledge system.
- The project needs a full from-scratch harness initialization (CLAUDE.md + docs/ + .gitignore + CI) — use `harness-bootstrap` instead. This skill focuses on knowledge governance and progressive disclosure, and does not include .gitignore/CI initialization.

## Methodology

### Target Directory Skeleton

```
CLAUDE.md                  # ~100 line map: "where to look now"
docs/
├── ARCHITECTURE.md        # Top-level architecture map: domain boundaries, layering rules
├── QUALITY_SCORE.md       # Quality scores by domain/layer
├── design-docs/
│   ├── index.md           # Design document index + validation status
│   └── core-beliefs.md    # Agent-first core operating beliefs
├── exec-plans/
│   ├── active/            # Active execution plans
│   ├── completed/         # Archived completed plans
│   └── tech-debt-tracker.md
├── generated/             # Auto-generated documentation (do not hand-edit)
├── product-specs/
│   └── index.md
└── references/            # Condensed reference for third-party libraries/tools
```

Not every project needs all subdirectories — trim as needed. But the directory structure itself must be recorded in CLAUDE.md so that an agent entering the repository for the first time knows "what categories of files the information is distributed across."

The 4 core rules for writing CLAUDE.md (length, scope, change frequency, verifiability) are detailed in Appendix B of `references/claude-md-map-template.md`.

### Initialization Steps (first-time docs/ skeleton setup)

1. Create the entry file (refer to `references/claude-md-map-template.md`) — only create the one for your own platform.
2. Create `docs/ARCHITECTURE.md` (refer to `../harness-architecture-boundaries/references/architecture-template.md`) and `docs/QUALITY_SCORE.md` (refer to `../harness-golden-principles/references/quality-score-template.md`). These two files belong under `docs/`, not the root directory.
3. Create empty directories as needed: `docs/design-docs/`, `docs/exec-plans/active/`, `docs/exec-plans/completed/`, `docs/generated/`, `docs/product-specs/`, `docs/references/`.
4. Create corresponding index files from the templates in the `references/` subdirectory: `docs/design-docs/index.md`, `docs/design-docs/core-beliefs.md`, `docs/product-specs/index.md`, `docs/exec-plans/tech-debt-tracker.md`.
5. Fill in template placeholders (domain names, code paths, dates, etc.) according to the project's actual situation.
6. Document validation is performed inline by the `doc-gardener` agent within its workflow — no need to generate a separate standalone script.
7. Write at the top of the entry file: "This file is a map, not an encyclopedia; for in-depth information, see docs/."

### Procedure (setting up or restructuring the knowledge base)

1. **Assess the current state**: How long is the existing CLAUDE.md/README? Is it a map or an encyclopedia? Does `docs/` exist? Does it have structure?
2. **Design the directory skeleton**: Refer to the template above — only create subdirectories the project actually needs.
3. **Split and migrate**: Break encyclopedia-style CLAUDE.md content into `docs/*.md` files by topic, then rewrite CLAUDE.md as a pointer table.
4. **Add metadata**: For each migrated document, add "what this is about and when to read it."
5. **Set up validation**: The `doc-gardener` agent performs document validation inline within its workflow (broken-link detection, freshness checks, coverage checks, structure checks) — no need to generate a separate standalone script.
6. **Write the map disclaimer**: At the top of the entry file, write "This file is a map, not an encyclopedia; for in-depth information, see docs/."

### Mechanized Validation (executed inline by doc-gardener agent)

Relying solely on humans to remember to update documentation won't work long-term. The doc-gardener performs four types of checks inline:

1. **Broken-link detection**: Scan `docs/` internal references to ensure files/anchor points exist.
2. **Freshness check**: Key documents must have a "last validated date" — mark as stale if over 30 days since last update.
3. **Coverage check**: Cross-reference against the code domain/package list to verify `ARCHITECTURE.md` / `QUALITY_SCORE.md` coverage is complete.
4. **Structure check**: Verify the `docs/` directory conforms to the agreed skeleton.

Failures are written as agent-friendly repair instructions so whoever finds them can fix them directly.

## Hard Constraints

- **CLAUDE.md ≤ 100 lines**: Violation → must be slimmed before merging.
- **docs/ broken-link rate = 0**: Violation → blocks merge.
- **Every docs/ file must have a metadata header**: Violation → doc-gardener marks as UNKNOWN.

## Examples

**Example 1**: CLAUDE.md exceeds 300 lines
**Handling**: Move content down to docs/, rewrite CLAUDE.md as a pointer table, ensure ≤ 100 lines

**Example 2**: Broken links exist in docs/
**Handling**: doc-gardener scans and finds broken links → generates fix suggestions → re-validate after repair

## Key Points

- When CLAUDE.md exceeds 100 lines, slim it down by moving content to `docs/` — it's a map, not an encyclopedia.
- Trim the directory skeleton as needed, but record it in CLAUDE.md so the agent knows how information is organized.
- Misleading content is more dangerous than missing content — prioritize fixing it.
- Outdated execution records have historical value — don't delete them. Clean up content that is "still marked active but inaccurate."
- For each document, add "what this is about" and "when to read it."
- Document validation is performed inline by doc-gardener; failure information is written as directly actionable repair instructions.
- Each directory has a clear responsibility and naming convention; avoid excessive nesting.

## Edge Cases

> For general edge cases (cross-platform sync, etc.), see `references/common-edge-cases.md`. Below are edge cases specific to this skill only.

### CLAUDE.md exceeds 100 lines

**Scenario**: CLAUDE.md exceeds 100 lines and needs trimming.
**Handling**: Move content down to docs/, rewrite CLAUDE.md as a pointer table, ensure CLAUDE.md ≤ 100 lines.

### docs/ directory missing or disorganized

**Scenario**: The docs/ directory is missing or structurally chaotic.
**Handling**: Refer to the target directory skeleton, create or reorganize the docs/ directory, record the directory structure in CLAUDE.md.

### Document broken links

**Scenario**: Internal links in docs/ point to non-existent files/anchor points.
**Handling**: Fix broken links, ensure all links are valid, broken-link rate = 0.

### Document expired

**Scenario**: Key documents have not been updated for over 30 days.
**Handling**: Mark as pending validation, update document content, update the "last updated" date.

## Common Pitfalls

- **Encyclopedia-style CLAUDE.md**: Stuffing all rules into one file — the agent can't navigate effectively and context is consumed.
- **Build-but-don't-maintain**: Created a docs/ structure but with no validation mechanism — documentation rots quickly.
- **Deleting historical records**: Removing outdated exec-plan decision records — outdated execution records still have historical value.
- **Redundant entry files**: Creating duplicate entry files for multiple platforms simultaneously — only create the one for your own platform.

## Related Skills

- Upstream **harness-bootstrap**: Receives deliverables (initialized docs/ skeleton) as the foundation for the documentation system.
- Downstream **all skills**: This skill's output (knowledge base structure and docs/ documentation) is passed downstream for context retrieval.

## Related Templates

- `references/claude-md-map-template.md`: CLAUDE.md map template (includes core beliefs and writing rules appendix)
- `references/docs-index-templates.md`: Design document index + product spec index templates
- `../harness-architecture-boundaries/references/architecture-template.md`: ARCHITECTURE.md architecture document template (canonical version)
- `../harness-golden-principles/references/quality-score-template.md`: QUALITY_SCORE.md quality score template (canonical version)
- `references/automation-check-script.sh`: Automation check script
- `references/e2e-repo-map-example.md`: End-to-end complete example (React project knowledge base restructuring, covering the full workflow from current-state analysis → structure design → document generation → quality validation)

## Best Practices

- When splitting CLAUDE.md, group by "which content will be read by the same type of agent" — don't mechanically follow the original file's section order.
- Each doc type in docs/ (design docs, specs, references) should use an independent preface template to help agents quickly determine whether to read deeper.
- After migration, keep old CLAUDE.md entries for one collaboration cycle with soft-link comments (`# Originally in CLAUDE.md, moved to docs/xxx.md`), then remove them completely.
- After fixing broken links, run `find docs -name '*.md' -exec grep -l '\\](' {} \\;` once to confirm no residual broken links remain.

## Agent 提示词

## doc-gardener

### Skip Conditions

- **Project is small (single-file script) and doesn't need structured documentation**: Do not trigger.
- **User only needs to update a specific document**: Do not trigger a full scan — directly suggest how to update.
- **Project needs full from-scratch harness initialization**: Hand off to harness-bootstrap, do not trigger doc-gardener.

### Role Definition

You are the "document gardener" (doc-gardener). Your mission is to keep the repository knowledge base fresh, navigable, and consistent with the current code state. You excel at using read-only tools to inspect documentation health.

### Core Capabilities

- CLAUDE.md health check: line count, navigation table integrity validation
- docs/ structure scan: file enumeration, broken-link detection, orphan document identification
- Code consistency validation: component existence, pairing completeness, reference integrity, freshness check
- Execution plan audit: active plan existence, tech-debt-tracker maintenance status
- Read-only operations: only use `Bash` (grep/cat/find), `Glob`, `Grep`, `Read`; **forbidden** from writing/deleting/modifying files

### Execution Flow

Execute the following steps strictly in order, using the minimum number of tool calls for each step.

**Step 1: CLAUDE.md Location Check** — `wc -l CLAUDE.md` to check line count and navigation table integrity. Report missing if not present; flag as needing trimming if over 100 lines.

**Step 2: docs/ Structure and Broken-Link Detection** — `find docs -type f` to enumerate files, extract markdown links and verify target existence. Don't enforce structural consistency — only report broken links and orphaned documents.

**Step 3: Document-to-Code Consistency** — Only perform mechanically verifiable checks: component existence (does the path in ARCHITECTURE.md exist?), pairing completeness (does the frontmatter agent field match the Agent Prompt section?), reference integrity (does the navigation table path exist?), freshness (mark as pending validation if last updated over 30 days ago).

**Step 4: Execution Plan and Tech Debt Check** — Verify `docs/exec-plans/active/` exists and `tech-debt-tracker.md` maintenance status.

**Step 5: Generate Report** — For each finding category, generate an independent repair suggestion (down to the specific file and line), severity: HIGH (misleading content/broken links) / MEDIUM (missing but not functionally impacting) / LOW (suggested improvement).

### Constraints

- **Read-only, no modifications**: Do not modify any files — only produce reports and suggestions. If you find yourself writing, withdraw the write operation and output as a report instead.
- **Do not delete historical content**: Decision records from completed exec-plans have historical value. If you find yourself deleting, restore the deleted historical content.
- **Fix misleading content first**: Documents that say something inconsistent with reality take priority over missing documents. If you find yourself prioritizing wrong, reorder the priorities.
- **Independent repair suggestions**: Each category of finding gets its own suggestion — do not mix unrelated changes. If you find yourself mixing, split into independent suggestions.
- **No disk output**: doc-gardener only outputs report conclusions via conversation, never writes to disk. If you find yourself creating temporary files, withdraw them.

### Output Specifications

- **Report structure**: Each suggestion includes location, severity, and repair instructions — conversation output only, no repository file modifications.
- **Best practices**: Provide best practices for knowledge base management, document maintenance, and directory structure.

---
Last updated: 2026-07-03 (Changes: S1 key points/best practices deduplication)
