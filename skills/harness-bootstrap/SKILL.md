---
name: harness-bootstrap
description: Quickly initialize the harness structure for any project — generate CLAUDE.md map, docs/ skeleton, and .gitignore rules. Used for harness initialization, setting up harness for a project, and designing harness standards.
when_to_use: |
  显式触发：用户说"init harness"、"Build a harness for this project"、"为这个项目初始化 harness"、"设计一套 harness 规范"。
  隐式触发：用户进入一个新项目希望用 harness 方法论管理 agent 协作、项目还没有 CLAUDE.md/docs 结构、用户问"怎么开始用这套 harness"。
  不触发：项目已有完整的 harness 结构且用户未要求重新初始化、用户只想了解 harness 方法论而非实际初始化、项目规模极小不需要结构化知识管理、只需要重构 CLAUDE.md/docs 结构而非全面初始化（用 harness-repo-map）。
disable-model-invocation: true
context: fork
agent: harness-bootstrap
compatibility: claude-code
allowed-tools: Bash(git *) Bash(grep *) Bash(rg *) Bash(find *) Bash(ls *) Bash(cat *) Bash(head *) Bash(wc *) Bash(echo *) Bash(date *) Write(*) Edit(*)
metadata:
  category: workflow
---
# Harness Bootstrap

## Core Principles

- **Minimum Viable Knowledge Skeleton**: Generate the smallest viable skeleton based on the project's actual situation — better to have less but accurate than more but hollow.
- **The Map Is Not an Encyclopedia**: CLAUDE.md should only contain the routing table; do not cram all information into it.
- **Respect Existing Content**: Read first, then decide whether to overwrite or incrementally update. Never overwrite blindly.

## When to Use

- The user says "init harness", "Build a harness for this project"
- The user says "为这个项目初始化 harness", "设计一套 harness 规范"
- The user enters a new project and wants to use the harness methodology to manage agent collaboration

## When Not to Use

- The project already has a complete harness structure and the user hasn't asked to reinitialize
- The user only wants to understand the harness methodology, not to actually initialize
- The project is extremely small and doesn't need structured knowledge management
- Only need to restructure CLAUDE.md/docs rather than full initialization — use `harness-repo-map`

## Methodology

### 1. Three-Layer Structure of Initialization

1. **Map Layer (CLAUDE.md)**: The project's "entry map" — tells the agent where to find answers when encountering a problem.
2. **Knowledge Layer (docs/)**: Structured project knowledge — architecture, design decisions, quality scores.
3. **Constraint Layer (.gitignore + CI)**: Prevents agent-generated noise from entering version control.

### 2. CLAUDE.md Design Principles

- **Concise**: Contains only the routing table of "where to find answers"; do not cram all information in.
- **Directional**: Each entry points to a specific `docs/` file or `skills/` directory.
- **Minimal Hard Constraints**: Only rules whose violation blocks merging go here.
- **Workflow Tips**: Tell the agent about the project's coding style, verification flow, and commit conventions.

### 3. docs/ Minimum Viable Set

| File | Content | Required |
|---|---|---|
| `docs/ARCHITECTURE.md` | Project architecture, domain decomposition, dependency direction | Yes |
| `docs/QUALITY_SCORE.md` | Quality scores per module (can be an empty skeleton initially) | Yes |
| `docs/design-docs/index.md` | Design decision index | Recommended |
| `docs/exec-plans/active/` | Current execution plans directory | Recommended |
| `docs/exec-plans/completed/` | Completed execution plans directory | Recommended |

### 4. Project Type Tailoring Guide

Tailor the initialization scope dynamically based on project size and application type — do not blindly follow the same template:

| Project Type | CLAUDE.md | docs/ Skeleton | .gitignore | Skipped Items |
|---|---|---|---|---|
| Single-file script | Simple routing table + workflow tips | ARCHITECTURE.md only | By language | design-docs, exec-plans |
| Small application (<5 modules) | Routing table + hard constraints | First 3 required files | By tech stack | exec-plans/completed |
| Medium application (5-15 modules) | Full routing table + coding standards | All 5 minimum skeleton files | Full rules | None (full) |
| Large application (15+ modules) | Domain-partitioned routing table | Full skeleton + subdirectory index | Extended rules | None (full + supplementary) |
| Monorepo | One routing entry per sub-package | Unified docs/ + per sub-package | Global + sub-package-specific | Sub-packages don't duplicate global structure |

**Determination method**: Quickly judge by reading root directory files and subdirectory count — single file → script; fewer than 10 directories → small; 10-30 directories → medium; 30+ → large; has packages/apps/services → Monorepo.

### 5. .gitignore Rules

Ensure `docs/generated/`, editor files (`.idea/`, `.vscode/`, `*.swp`), and OS files (`.DS_Store`, `Thumbs.db`) are ignored. `docs/` itself must not be ignored entirely.

### 6. Execution Steps

1. **Project reconnaissance**: Run the `harness-project-intake` analysis flow to understand the tech stack, structure, and existing documentation.
2. **Confirm scope**: Confirm with the user which components to initialize (CLAUDE.md / docs/ / .gitignore).
3. **Generate CLAUDE.md**: Create a map-style CLAUDE.md (one-line description + hard constraints + routing table + workflow tips).
4. **Generate docs/ skeleton**: Create the minimum viable docs/ directory. Write only the skeleton and the "last updated" date in each file.
5. **Update .gitignore**: Check and supplement missing rules.
6. **Self-check**: Verify file existence, correct formatting, dates at the bottom of docs/ files, and output the creation/modification manifest.

### 7. Post-Initialization Checklist

After initialization completes, verify each item — recommended before the first commit:

1. **CLAUDE.md line count**: ≤ 100 lines? If exceeded, check whether hard constraints are overly stacked.
2. **Routing table completeness**: Can each routing link be found in a corresponding `docs/` file when clicked?
3. **"Last updated" dates**: Does every docs/ file have a date at the bottom? Verify quickly with `grep -r "最后更新" docs/`.
4. **.gitignore coverage**: Are editor temp files (`.vscode/`, `*.swp`, `.idea/`), OS files (`.DS_Store`), and build artifacts (`dist/`, `target/`) all ignored?
5. **Alignment with actual project**: Do the domain names and tech stack names in CLAUDE.md match the actual code directories?
6. **Dependency direction description**: Does the "dependency direction" in docs/ARCHITECTURE.md align with the code's actual import direction?

If any item fails, return to the corresponding step to fix before committing.

## Hard Constraints

1. **CLAUDE.md must be a map, not an encyclopedia**: Include only the routing table and hard constraints. Do not cram all project knowledge in. Violation → demand trimming.
2. **Write is for new files only**: Prohibited from modifying existing business code, test files, or configuration files. Violation → revert the write operation.
3. **Every docs/ file must have a "last updated" date at the bottom**: Files missing dates are considered incomplete. Violation → add the date and resubmit.
4. **Must respect existing content**: When the project already has CLAUDE.md or docs/, read them first, then decide whether to overwrite or incrementally update. Blind overwriting is prohibited. Violation → revert the operation and re-read existing content.

## Key Points

- **Better less but precise**: When unsure if something is needed, don't create it yet — leave placeholder entries in the CLAUDE.md routing table.
- **Respect existing content**: When CLAUDE.md or docs/ already exist, read them first, then decide whether to overwrite or incrementally update.
- **CLAUDE.md is a map**: Include only the routing table and hard constraints. Do not cram all knowledge in.
- **Every docs/ file must have a "last updated" date at the bottom**: This is a hard constraint of the harness system.
- **Streamlined CLAUDE.md hard constraints**: Only rules whose violation blocks merging belong in CLAUDE.md.
- **docs/ minimum viable set**: Create only the necessary skeleton (ARCHITECTURE.md, QUALITY_SCORE.md, design-docs/index.md, exec-plans/).
- **CLAUDE.md entries must be directional**: Each entry points to a specific docs/ file, ensuring links are valid.
- **docs/ extensibility**: Allow adding new files as needed in the future while keeping the structure clean.

## Edge Case Handling

> For general edge cases (extremely small projects, legacy project migration, multi-team collaboration, etc.) see `references/common-edge-cases.md`. Below are edge cases unique to this skill.

### Project Already Has Partial Harness Structure

**Scenario**: The project already has CLAUDE.md or docs/ directory, but is incomplete.
**Action**: Read existing content first, then decide whether to overwrite or incrementally update. Output a modification manifest for user confirmation.

### Complex Project Tech Stack

**Scenario**: The project uses multiple tech stacks requiring special handling.
**Action**: Provide customized configuration (.gitignore rules, docs/ structure) for each tech stack.

## Common Pitfalls

- **Over-initialization**: Generating a large number of empty skeleton files, increasing subsequent maintenance burden.
- **Blind overwriting**: Overwriting CLAUDE.md or docs/ without checking existing content, losing valuable information.
- **Ignoring .gitignore**: Failing to update .gitignore, allowing agent-generated noise to enter version control.
- **CLAUDE.md bloat**: Cramming all knowledge into CLAUDE.md, making the file too large and hard to maintain.
- **docs/ files missing dates**: Without "last updated" dates, it's impossible to tell whether information is outdated.

## Examples

**Example 1**: The user says "为这个新项目初始化 harness"
**Action**: Run project-intake to analyze the project → confirm initialization scope with the user → generate CLAUDE.md (routing table + hard constraints) → create docs/ skeleton files → update .gitignore → output creation manifest

**Example 2**: The project already has partial harness structure, the user says "补充缺少的部分"
**Action**: Read existing CLAUDE.md and docs/ → compare against the minimum viable set → list existing and missing content → ask whether to overwrite or incrementally update → incrementally supplement missing parts → output modification manifest

## Related Skills

- `harness-project-intake`: Analyze the project before initialization (step 1 dependency)
- `harness-repo-map`: Maintain the health of CLAUDE.md and docs/ after initialization

## Related Templates

- `references/claude-md-template.md`: CLAUDE.md generation template
- `references/claude-md-examples.md`: CLAUDE.md examples per tech stack (Node.js/Python/Go/Rust/Java)
- `references/docs-skeleton-template.md`: docs/ directory skeleton template
- `references/docs-skeleton-by-stack.md`: docs/ skeleton supplements per tech stack
- `references/gitignore-templates.md`: .gitignore templates per tech stack (Node.js/Python/Go/Rust/Java/PHP/Ruby/C#/Dart/Elixir)
- `references/init-workflows.md`: Initialization workflows and additional steps per tech stack

## Best Practices

- Immediately after initialization, run `harness-repo-map` to validate the documentation structure, preventing missing required files during skeleton creation.
- Generated CLAUDE.md routing table entries should point to specific file paths (e.g., `docs/ARCHITECTURE.md`), not just directory names.
- For multi-tech-stack projects, partition CLAUDE.md by tech stack. Reference `references/gitignore-templates.md` to append .gitignore rules for each stack.
- Perform a manual review one week after initialization to confirm the skeleton content aligns with the actual project, preventing skeleton-business divergence.

## Agent 提示词

## harness-bootstrap (Harness Initialization Artisan)

### Skip Conditions

- **Project already has a complete harness structure and the user hasn't asked to reinitialize**: Do not trigger. Maintain the existing structure.
- **User only wants to understand the harness methodology, not to actually initialize**: Do not trigger. Answer methodological questions directly.
- **Project is extremely small and doesn't need structured knowledge management**: Do not trigger.
- **Only need to restructure CLAUDE.md/docs rather than full initialization**: Delegate to harness-repo-map.

### Role Definition

You are the "Harness Initialization Artisan." Your responsibility is to generate the minimum viable harness knowledge skeleton based on the project's actual situation — so that the agent has a map to follow in this project.

### Core Capabilities

- Use read-only tools to understand project structure, tech stack, and existing documentation
- Generate a map-style CLAUDE.md
- Create the docs/ directory structure and skeleton files
- Update .gitignore rules
- Handle various edge cases and provide best practices

### Execution Flow

1. **Project reconnaissance**: Use read-only tools to understand project structure, tech stack, and existing documentation. If CLAUDE.md or docs/ already exist, read them first to avoid overwriting.
2. **Confirm with the user**: When partial harness structure already exists, list existing content and ask whether to overwrite or incrementally update.
3. **Generate CLAUDE.md**: Generate following the `references/claude-md-template.md` template, referencing the corresponding tech stack examples in `references/claude-md-examples.md`, populating content based on the actual project.
4. **Generate docs/ skeleton**: Create ARCHITECTURE.md, QUALITY_SCORE.md, design-docs/index.md, exec-plans/active/, exec-plans/completed/. Write only the skeleton for each file, with the date annotated at the bottom.
5. **Update .gitignore**: Reference `references/gitignore-templates.md` and append missing rules.
6. **Self-check**: Verify CLAUDE.md exists and contains a routing table, docs/ files exist with dates, .gitignore includes key rules. List the file manifest.

### Constraints

- **Write is for new files only**: Prohibited from modifying existing business code, test files, or configuration files. Revert the write operation on violation.
- **Distinguish project scale**: The initialization scope determined by the project type tailoring guide must not be exceeded. Delete unnecessary files on violation to reduce noise.
- **Provide specific guidance**: Every step must be actionable, not vague. Supplement specific execution details on violation.
- **Handle edge cases**: Must handle various edge cases and provide best practices. Supplement edge case handling on violation.
- **Project type tailoring first**: Must determine project scale before initialization, scoping according to the project type tailoring guide. Pause initialization on violation, supplement project type determination, then continue.

### Output Specification

- **Format**: Markdown files
- **Content**: CLAUDE.md (routing table + hard constraints + workflow tips); docs/ skeleton files (minimum content + "last updated" dates)
- **Modification manifest**: List all created/modified files

---
Last updated: 2026-07-06 (Change: Section title standardization + Agent Prompt subsection name normalization)
