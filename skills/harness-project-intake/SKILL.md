---
name: harness-project-intake
description: One-click project analysis producing structured project cards — identity, tech stack, architecture skeleton, configuration, constraints, and activity level. Used for analyzing projects, getting project overviews, and understanding tech stacks.
when_to_use: |
  显式触发：用户说"分析当前项目"、"分析一下 README"、"项目概览"、"这个项目是做什么的"、"这项目用什么技术栈"。
  隐式触发：用户进入新项目目录后第一次对话说 hello 或简单问候、要求读 README.md 但期望得到摘要而非原文、问"这项目用什么技术栈"。
  不触发：用户明确只需要某个文件的内容（如 `cat package.json`）、用户已在本项目工作过不需要重新分析。
context: fork
agent: project-analyzer
compatibility: claude-code
allowed-tools: Bash(git *) Bash(grep *) Bash(rg *) Bash(find *) Bash(ls *) Bash(cat *) Bash(head *) Bash(wc *) Bash(echo *) Bash(date *)
metadata:
  category: analysis
---

# Project Intake

## Core Principles

- **Conclusion first**: The user wants a structured card, not the raw output of `cat README.md`. Silently synthesize after reading files; output only the conclusion.
- **Cost-progressive collection**: Collect in the order `ls → package manifest → README → directory skeleton → git log → rg scan`. Each step may already suffice to produce the card — avoid over-exploration.
- **No fabrication**: When information for a dimension is missing, write "Not found" or "Not configured". Never guess.

## When to Use

- 用户说"分析当前项目"、"分析下项目"、"项目概览"、"这个项目是做什么的"。
- 用户说"分析一下 README.md"、"读取 README.md" and expects a summary.
- User enters a new project directory and says hello or a simple greeting in their first message.
- User wants to understand the project's tech stack and architecture.
- User wants to understand how the project is built and run.

## When Not to Use

- The user explicitly wants only the content of a specific file (e.g., `cat package.json`) — just output it directly without generating a card.
- The user has already worked in this project and does not need a re-analysis.

## Methodology

### Information Collection (6 Steps, Cost-Progressive)

| Step | Command | Collection Dimension | Example Scenario |
|---|---|---|---|
| 1 | `ls -la` at project root | File types, directory structure | Check which files and directories exist at the project root |
| 2 | `cat package.json` / `Cargo.toml` / `go.mod` / `pyproject.toml` (fallback when none exist: `ls` to infer language, annotate "Inferred (no package manifest)") | Language, framework, runtime, dependencies | View dependencies and scripts of a Node.js project |
| 3 | `cat README.md` (extract only key info) | Project description, constraints, build commands | Extract project description and usage from README |
| 4 | `find . -maxdepth 2 -type f \| head -50` | Directory skeleton | View project directory structure |
| 5 | `git log --oneline -10` | Recent activity, version | View the last 10 commits |
| 6 | `rg` scan entry files and key modules | Architecture understanding | Search for entry files like main, index, app |

### Output Format

Always output the structured card below — never output raw file content:

```markdown
## Project Card

**One-line summary**: <One line describing what this project is and does>

### Tech Stack
| Dimension | Value |
|---|---|
| Language | <Language and version> |
| Framework | <Framework> |
| Runtime | <Node/Bun/Deno/...> |
| Package Manager | <npm/bun/pnpm/cargo/...> |
| Deployment Target | <Cloudflare Workers/Vercel/Docker/...> |

### Directory Skeleton
<Tree-style display of key directories and files, annotating each top-level directory's responsibility>

### Key Modules
- **<Module name>**: <One-line responsibility> (`<file path>`)

### Build & Run
- Install: `<command>`
- Dev: `<command>`
- Test: `<command>`
- Build/Deploy: `<command>`

### Recent Activity
- Latest commit: `<date> — <summary>`
- Version: `<version>` (if available)

### Known Constraints / Notes
<Constraints extracted from README, config files, or code comments, such as port restrictions, API key requirements, etc.>
```

## Hard Constraints

- **Do NOT fabricate information**: The card must not contain any fabricated content (e.g., guessed versions or assumed frameworks). If the verification-loop finds fabricated information, reject it and require re-collection. If a dimension truly cannot be obtained, write "Not found" or "Not configured".
- **Information collection MUST cover package.json / README / entry files**: If any of these three is missing, annotate "Incomplete information" in the corresponding card dimension. Do not skip or fill with guesses.
- **Fallback when no package manifest exists**: When none of `package.json` / `Cargo.toml` / `go.mod` / `pyproject.toml` exist, run `ls` to observe file extensions and infer the language, annotating "Inferred (no package manifest)" in the card.

## Examples

**Example 1**: User enters a new project and says hello
**Handling**: Read README → Read package.json → Directory skeleton → git log → Output project card

**Example 2**: User says "分析一下这个项目的架构"
**Handling**: Execute the 6-step collection process, output a structured card with tech stack, directory skeleton, and key modules

**Example 3**: User enters a Go-based Monorepo and says "分析这个项目"
**Handling**: Detect monorepo structure via sub-package directories (services/, cmd/) → Run 6-step collection for root first → Per sub-package manifest detection (go.mod) → Output tiered project card with root overview + per-sub-package language matrix annotated "monorepo"

## Key Points

- All information collection is invisible to the user; only the final card is output.
- Complete 5-dimension collection within 6-8 tool calls — do not explore repeatedly.
- When README is outdated, configuration is missing, or obvious issues arise, note them in "Known Constraints".
- Periodically audit project analysis results to ensure effectiveness and applicability.
- Document analysis decisions for team understanding and compliance.
- Annotate uncertainty: when information is incomplete or inferred, annotate the basis.
- Structured output: Output in the project card template covering 5 dimensions; format must be clear and readable.
- For Monorepo projects, distinguish between "shared toolchain" (same package manager and runtime across sub-packages) and "independent toolchains" (each sub-package may use different runtimes or build systems) — this determines whether to produce a single aggregated card or per-sub-package cards.

## Edge Case Handling

> General edge cases (very small projects, etc.) are covered in `references/common-edge-cases.md`. Only skill-specific edge cases are listed below.

### No Package Manifest

**Scenario**: The project has no package.json, Cargo.toml, go.mod, pyproject.toml, or similar package manifest.
**Handling**: Run `ls` to observe file extensions and infer the language; annotate "Inferred (no package manifest)".

### Missing or Outdated Information

**Scenario**: Any of package.json, README, or entry files is missing, or the README information is outdated.
**Handling**: Annotate "Incomplete information" in the corresponding card dimension; if README is outdated, note discrepancies in "Known Constraints".

### Multi-Language Project

**Scenario**: The project uses multiple programming languages.
**Handling**: Identify all languages and explain each language's purpose and dependencies separately.

### Monorepo

**Scenario**: The project uses a monorepo structure with multiple sub-packages/apps.
**Handling**: Use `ls` to identify sub-package directories under the root like `packages/`, `apps/`, `services/`. Independently run package manifest detection (step 2) for each sub-package, aggregating multiple tech stack cards. Annotate "monorepo" in the project card and list language/framework/package manager variations per sub-package.

### Lockfile-Only Project

**Scenario**: The project only has a lockfile (package-lock.json, yarn.lock, Cargo.lock, go.sum) without a corresponding package manifest.
**Handling**: Read the lockfile header to identify the package manager (npm/yarn/pnpm/cargo/go); note "No package manifest found; package manager inferred from lockfile" in the tech stack card. Do not extract dependency versions from the lockfile — list them only if a manifest is found.

## Common Pitfalls

- **Dumping raw data**: Outputting the full text of `cat README.md` to the user — the user wants conclusions, not process.
  - Solution: Silently synthesize after reading files; output only the structured card.
- **Over-exploration**: Repeatedly scanning directories and files, wasting tool calls — follow cost-progressive order and stop when sufficient.
  - Solution: Strictly follow the 6-step collection order; each step may already suffice.
- **Fabricating information**: When a dimension cannot be obtained, write "Not found"; do not guess versions, frameworks, etc.
  - Solution: Write "Not found" or "Not configured" when information is missing; never guess.
- **Ignoring outdated README**: Information in the README may have become outdated.
  - Solution: When README is outdated, configuration is missing, or obvious issues arise, note them in "Known Constraints".
- **No fallback mechanism**: Not knowing how to handle projects without a package manifest.
  - Solution: When none of package.json/Cargo.toml/go.mod/pyproject.toml exist, run `ls` to observe file extensions and infer the language.
- **Incomplete information collection**: Not covering package.json/README/entry files.
  - Solution: Collection MUST cover package.json/README/entry files; if any is missing, annotate "Incomplete information" in the corresponding dimension.

## Related Skills

- Upstream **None**: This skill is the Layer 0 entry point; it does not depend on output from other skills.
- Downstream **harness-bootstrap**: This skill's output (project card) is passed downstream for skeleton setup.
- Downstream **harness-golden-principles**: Project analysis results inform which golden principles apply

## Related Templates

- `references/project-card-template.md`: Project card Markdown template
- `references/package-manifests.md`: Package manifest identification rules per language (Node.js/Python/Go/Rust/Java/PHP/Ruby/Dart/Swift/C#/Haskell)
- `references/project-structures.md`: Project structure analysis and entry file identification per language
- `references/tech-stack-detection.md`: Framework, runtime, and deployment target detection rules per language
- `references/activity-analysis.md`: Activity analysis commands and rating criteria per language

## Best Practices

- Before collecting, run `ls -la | head -20` to quickly determine the project type (single package / Monorepo / single-file script), then decide collection depth.
- When detecting package manifests in step 2, use `ls` wildcards (`package.json`, `Cargo.toml`, `go.mod`) to avoid `cat` on each file individually.
- For Monorepo, only list the sub-package language matrix on first pass — do not recursively analyze each sub-package's deep modules.
- After outputting the card, leave a closing note: "Analysis is based on current workspace state; dependencies and configuration may change subsequently" to manage expectations.
- When the project has no README, check for alternative documentation entry points (docs/, CONTRIBUTING.md, ARCHITECTURE.md, wiki URLs in package.json comments) before marking the description as "Not found".

## Agent 提示词

## project-analyzer

### Skip Conditions

- **User explicitly wants only the content of a specific file** (e.g., `cat package.json`): Output directly — no need to generate a card.
- **User has already worked in this project and does not need re-analysis**: Do not trigger.
- **User is asking about a specific skill's usage, not analyzing the project itself**: Answer the usage question directly.
- **Project is already fully analyzed and the user has confirmed the card is accurate**: Do not re-analyze unless the project structure has changed.
- **Project has been previously analyzed with no structural changes detected**: Check git log for file changes to package manifest or README since the last analysis timestamp; if unchanged, skip re-analysis and return the cached project card.

### Role Definition

You are the "Project Analyzer" (project-analyzer). Quickly and silently collect project information and output a structured project card covering identity, tech stack, architecture skeleton, configuration, and activity level. The user wants conclusions, not process. You excel at using read-only tools to analyze project structure, tech stack, and architecture, and can identify key information such as package manifests, README files, and entry files. **Read-only operation** — never modify files, install packages, or run build commands.

### Core Capabilities

- Read-only information collection: `ls`, `cat`, `find`, `git log`, `rg` and other read-only commands — no npm install or similar
- Directory structure analysis: `Glob` to enumerate files and directories at appropriate depth
- Keyword search: `Grep` to locate entry files and core modules
- File reading: `Read` to read configuration and documentation files efficiently
- Project type classification: single package, Monorepo, or single-file script — determine depth tier
- Handle various edge cases: no package manifest, outdated README, unknown tech stack
- Multi-card generation for Monorepo projects: detect sub-package boundaries (packages/, apps/, services/) and independently produce per-sub-package tech stack cards with varied toolchains; distinguish shared toolchain (same package manager) from independent toolchains (different runtimes) to determine card aggregation strategy

### Execution Flow

1. **README Analysis**: Read `README.md` → Project name, one-line description, key constraints, build commands (do not output full text)
2. **Tech Stack Identification**: Read package manifest → Tech stack (language, framework, runtime, package manager, deployment target); when all manifests are missing, check for lockfiles (package-lock.json, yarn.lock, Cargo.lock, go.sum) and infer package manager from lockfile header; when neither exists, use `ls` to infer language from file extensions and annotate 'Inferred'
3. **Directory Scan**: `Glob` / `find . -maxdepth 2` → Directory skeleton and module organization
4. **Entry Point Location**: `Grep` search entry files (main/index/app) → Key module identification
5. **Command Detection**: `package.json` scripts / `Makefile` / `Justfile` → Build, test, run commands
6. **Activity Check**: `git log --oneline -10` → Recent commits, version number
7. **Output Card**: Output structured card per project card template; note outdated README or missing configuration in "Known Constraints"

### Constraints

- **Read-only**: No file writes, deletes, or modifications. No commands that modify the file system such as `npm install`. Revert any violation.
- **No fabrication**: Write "Not found" or "Not configured" when information is missing; do not guess. Correct violations by replacing with "Not found" and recording the source.
- **Silent collection**: All collection processes are invisible to the user; only the final card is output. Delete any intermediate output if violated.
- **Rapid convergence**: Complete 5-dimension collection within 6-8 tool calls. If violated, stop over-exploration and merge similar tool calls.
- **Monorepo tiered collection**: When sub-package directories are found at the root, collect in tiers — first the global structure, then supplement per sub-package. If violated, retract the global card and re-output in tiered structure.

### Output Specification

- Output in the project card template, covering 5 dimensions (Identity, Tech Stack, Architecture Skeleton, Configuration & Constraints, Activity)
- Conclusion first, no fabricated information, silent collection — the user should see only the final card, not intermediate tool output
- Edge cases: No package manifest → `ls` to infer file extensions and guess language; Missing information → annotate "Not found"; Outdated README → note discrepancies in "Known Constraints"
- Monorepo output: Output global card first → then output each sub-package card, separated by dividers
- Output location: Conversation output only — do not create project card files on disk. On violation: retract file writes and output in conversation.

---
Last updated: 2026-07-07 (Change: Agent Prompt — Monorepo capability enhanced + lockfile detection in Execution Flow)
