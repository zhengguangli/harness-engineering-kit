# Standardize SKILL.md Frontmatter Fields

- Status: completed
- Created: 2026-07-06
- Last updated: 2026-07-06
- Related PR / issue: commit 39c498a
- Responsible agent / person: harness-exec-plans

## Goal

All 13 SKILL.md files use only recognized Claude Code frontmatter fields, with any custom extensions clearly documented and validated — no silent "shadow fields" that developers might mistake for standard Claude Code features.

## Scope / Non-goals

**In scope:**
- Audit all 13 SKILL.md frontmatter fields against the official Claude Code recognized field set
- Identify non-standard fields (`agent`, `metadata`) and their usage
- Propose and execute a fix strategy for each non-standard field
- Update validation scripts and quality checks to reflect the fix
- Update `docs/ARCHITECTURE.md` and/or `CLAUDE.md` to document custom extensions

**Explicitly out of scope (non-goals):**
- Do NOT change the functionality of the harness system — `agent` and `metadata` are used internally for agent routing and categorization, and must still work after the fix
- Do NOT rename skill directory names or SKILL.md file locations
- Do NOT change `## Agent 提示词` section content (that's governed by separate standardization)
- Do NOT fix non-frontmatter content issues in the SKILL.md body

## Steps

### Phase 1: Investigate & Confirm (1 step)

- [x] Step 1.1 — Confirm the complete set of recognized Claude Code SKILL.md frontmatter fields by consulting the official Claude Code docs (`context7`, `/websites/code_claude`). Identified suspects: `agent` and `metadata` fields need confirmation of their (non-)standard status. **Result**: `agent` IS a standard field (docs line 241). `metadata` is NOT a standard field. `compatibility` is also NOT a standard field.

### Phase 2: Decide Fix Strategy (2 steps)

- [x] Step 2.1 — For the `agent` field: Keep as-is. It is a recognized standard Claude Code frontmatter field. **Decision**: No action needed.
- [x] Step 2.2 — For the `metadata.category` field: Keep as documented custom extension. It has script dependencies (`skills/harness-skill-quality-assessor/references/automated_check_script.py` checks its existence) and provides useful categorization. **Decision**: Keep, document explicitly as harness extension.

### Phase 3: Execute Fixes (2 steps)

- [x] Step 3.1 — No SKILL.md file changes needed. `agent` is standard, `metadata` and `compatibility` are custom extensions but Claude Code silently ignores unrecognized fields — no functional impact.
- [x] Step 3.2 — No validation script changes needed. Existing checks already correctly cover `compatibility` and `metadata`. No script needs updating.

### Phase 4: Update Documentation (2 steps)

- [x] Step 4.1 — Updated `CLAUDE.md` (Hard Constraints section) and `docs/ARCHITECTURE.md` (Data Boundary Rules section) to document `compatibility` and `metadata` as harness-specific custom frontmatter extensions.
- [x] Step 4.2 — Verified `~/.claude/skills/` is in sync with repo `skills/` (no SKILL.md changes were made, so they were already identical). Verified via `diff -r`.

### Phase 5: Final Verification (1 step)

- [x] Step 5 — `make triggers-all` passes (frontmatter validation + 48 trigger regression tests + agent prompt presence check), exit code 0. No quality regression.

## Decision Log

| Date | Decision | Rationale | Rejected Alternatives |
|---|---|---|---|
| 2026-07-06 | `agent`字段：保留，不处理 | 官方文档确认其为标准字段（"Which subagent type to use when `context: fork` is set."） | 重命名为 `trigger-agent` 或 `subagent` — 无必要，官方已认可 |
| 2026-07-06 | `metadata`(含`category`)：保留，文档化为自定义扩展 | 有脚本依赖（质量评估器检查其存在性），提供有用分类信息，Claude Code 静默忽略非标准字段 | 移除 — 会破坏质量评估器检查；重命名 — 无必要 |
| 2026-07-06 | `compatibility`：保留，文档化为自定义扩展 | 有脚本依赖（3个脚本检查其存在性），标示 Claude Code 兼容性有用 | 移除 — 会破坏验证脚本检查 |
| 2026-07-06 | 无需修改验证脚本 | 已有检查已正确覆盖自定义字段的存在性，且无脚本解析其值 | 添加白名单 — 当前未报错，过度工程 |

## Acceptance Criteria

- [x] `grep "^metadata:" skills/*/SKILL.md` returns results (kept as documented custom extension) — `metadata` field is explicitly documented as a harness-specific custom extension in CLAUDE.md
- [x] `grep "^compatibility:" skills/*/SKILL.md` returns results (kept as documented custom extension) — `compatibility` field is explicitly documented as a harness-specific custom extension in CLAUDE.md
- [x] `make triggers-all` passes with exit code 0 after all changes
- [x] Custom field documentation exists in CLAUDE.md's Hard Constraints section and ARCHITECTURE.md's Data Boundary Rules section
- [x] `~/.claude/skills/*/SKILL.md` frontmatter matches `skills/*/SKILL.md` (verified by `diff -r`)

## Risks / Known Unknowns

- [resolved] **Risk: `agent` field may be silently consumed by Claude Code's Agent tool routing** — RESOLVED: `agent` IS a documented standard field for SKILL.md, not just for `.claude/agents/*.md` files.
- [resolved] **Risk: Changing field names may break harness-internal scripts** — AVOIDED: no field renames were performed.

## Change History

- 2026-07-06: Plan created
- 2026-07-06: Plan completed — decision log filled, acceptance criteria verified, commit 39c498a
