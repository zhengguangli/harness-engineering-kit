# Changelog

All notable changes to this project will be documented in this file.

## [v0.1.1] - 2026-06-30

### Changed
- Unified agent tool mapping across skills to reduce cross-platform ambiguity
- Strengthened `harness-commit-gate` defaults and failure-handling behavior
- Improved `harness-verification-loop` clarity, numbering consistency, and references
- Enhanced `harness-orchestration` to discover available skills dynamically
- Added cross-platform prerequisites and fallback notes in multiple skills

### Fixed
- Resolved dual-source maintenance drift between `agents/*.md` and `openai.yaml`
- Fixed sequential numbering inconsistencies in workflow documents
- Corrected duplicate/conflicting tool declarations in agent definitions

### Verification
- Full read-only regression across 12 skills completed successfully
- Duplicate-number and reference-mismatch checks passed
- Key policy checks confirmed (staged-first gating, failure classification, orchestration discovery)

## [v0.1.0] - 2026-06-30

### Added
- New skill: `harness-prompt-optimizer` for structured LLM prompt engineering
- "When not to use" sections to all 12 skills to prevent mis-triggering
- "Common pitfalls" sections with 4-5 specific items per skill
- `harness-bootstrap` skill for one-click harness initialization
- `harness-commit-gate` skill for commit quality gates
- `harness-orchestration` skill for skill routing and workflow
- `harness-project-intake` skill for project analysis and intake

### Changed
- Standardized all SKILL.md structure: core principles → when to use → when not to use → methodology → key points → common pitfalls
- Standardized all agents/*.md structure: role definition → core capabilities → execution flow → output spec
- Simplified redundant content across all skills for clarity
- Converted agent files from prose to structured four-section format
- Removed docs/ coupling to decouple skills as standalone library
- Eliminated template duplication across skills
- Slimmed context for better agent performance

### Fixed
- Resolved quality issues across all 12 skill definitions
- Fixed cross-platform consistency issues
- Hardened defensive boundaries in architecture-related skills

### Removed
- `.gitignore` (moved to project-specific configuration)
- Redundant template files (consolidated into references/)

## Skills Inventory

| Skill | Version | Description |
|-------|---------|-------------|
| harness-architecture-boundaries | 0.1.0 | Layered architecture and dependency direction enforcement |
| harness-authoring | 0.1.0 | Meta-skill for creating new skills/agents |
| harness-bootstrap | 0.1.0 | One-click harness initialization |
| harness-commit-gate | 0.1.0 | Commit quality gates |
| harness-exec-plans | 0.1.0 | Execution plans as first-class artifacts |
| harness-golden-principles | 0.1.0 | Golden principles and continuous garbage collection |
| harness-observability-and-browser | 0.1.0 | Browser and observability feedback sensors |
| harness-orchestration | 0.1.0 | Skill routing and workflow orchestration |
| harness-project-intake | 0.1.0 | Project analysis and intake |
| harness-prompt-optimizer | 0.1.0 | Structured LLM prompt engineering |
| harness-repo-map | 0.1.0 | Repository knowledge map and docs structure |
| harness-verification-loop | 0.1.0 | Ralph Wiggum self-verification loop |

---

## Release Process

```
feature/* → developer → main
              PR         PR
                          ↓
                       tag vX.Y.Z
                          ↓
                     sync to skill-repo
```
