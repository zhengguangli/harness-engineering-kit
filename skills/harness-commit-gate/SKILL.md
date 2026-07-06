---
name: harness-commit-gate
description: Run a set of quality gate checks before committing code (lint/build/test/sensitive info leaks), applying CI-level rules while ensuring not all code needs the full suite. Used for committing code, preparing to push, checking code quality, and pre-commit verification.
when_to_use: |
  显式触发：用户说"提交代码"、"commit"、"git commit"、"代码提交"、"修复，提交代码"。
  隐式触发：用户完成了代码修改并准备提交、verification-loop 已完成并需要提交、用户询问如何提交代码。
  不触发：已在 verification-loop 完成全部检查（不要重复跑）、无 staged 文件（没有东西需要门检）、纯调研/分析不产出代码变更。
disable-model-invocation: true
context: fork
allowed-tools: Bash(git *) Bash(npm *) Bash(bun *) Bash(cargo *) Bash(vitest *) Bash(tsc *) Bash(bunx *) Bash(make *) Bash(just *)
agent: commit-gate-runner
compatibility: claude-code
metadata:
  category: workflow
---
# Commit Gate

## Core Principles

- **Committing is a "verification passed" signal**: Before every commit, run a lightweight quality gate: review what changed, run relevant tests, and format the commit message. Only pass if checks succeed; fix until they do.
- **Check before commit**: Better to spend 30 extra seconds running tests than to commit something that breaks the build.
- **Commit messages are for the future**: Clearly state "what was done" and "why". Do not write uninformative messages like "fix bug" or "update".

## When to Use

- User says "提交代码", "commit", "git commit"
- User says "修复，提交代码" (fix first, then commit)
- User has completed code changes and is preparing to commit
- verification-loop is complete and requires a commit
- User asks how to commit code

## When Not to Use

- All checks already completed in `verification-loop` — do not re-run
- No staged files — nothing to gate check
- Pure research/analysis, no code changes produced

## Methodology

### 1. Three Checks of the Quality Gate

1. **Diff Review**: Read through the changes with `git diff --staged`, checking for:
   - Residual debug code (console.log, print, TODO hack)
   - Changes beyond the scope of the current task (scope creep)
   - Sensitive information leaks (API keys, passwords, tokens)
2. **Automated Verification**: Run based on the project's configuration:
   - Tests: `bun test` / `npm test` / `vitest run` / `cargo test`
   - Build: `bun run build` / `npm run build`
   - Type check: `tsc --noEmit` / `bunx tsc --noEmit`
   - Lint: if configured
3. **Commit Message Formatting**: Generate the message according to project conventions:
   - If the project follows conventional commits, use `type(scope): description`
   - Otherwise, use a concise imperative sentence describing the change

### 2. Check Strategy: Based on Project Configuration

Do not hardcode all check commands. First probe the project to see which tools it uses:

1. Check `package.json` scripts → look for test / build / lint commands
2. Check `Makefile` / `Justfile` → find the corresponding targets
3. Check `Cargo.toml` → use `cargo test` / `cargo check`
4. If nothing is found, only perform diff review + commit

### 3. Toolchain Detection Flow

```
是否有 package.json?
├─ 是 → 读取 scripts 字段
│  ├─ test? → bun test / npm test / vitest run
│  ├─ build? → npm run build
│  └─ lint? → npm run lint
├─ 否 → 是否有 Cargo.toml?
│  ├─ 是 → cargo test / cargo check
│  └─ 否 → 是否有 Makefile?
│     ├─ 是 → make test / make build
│     └─ 否 → 只做 diff 审查
是否有 bun.lock / bun.lockb?
└─ 是 → 优先用 bun 运行（bun test > npm test）
```

**Recommended Order for Detection Commands**:
1. `ls package.json bun.lock 2>/dev/null && bun test` (Bun preferred)
2. `ls package.json 2>/dev/null && npm test` (npm fallback)
3. `ls Cargo.toml 2>/dev/null && cargo test` (Rust)
4. `ls Makefile 2>/dev/null && make test` (Makefile)
5. `ls Justfile 2>/dev/null && just test` (Justfile)
6. None found → diff review only

### 4. When to Skip Automated Verification

- Project has no test or build configuration → diff review only
- User explicitly says "不要跑测试" → skip automated verification
- Changes involve only documentation (.md files) → diff review + commit only
- All checks already completed in verification-loop → do not re-run
- No staged files → nothing to gate check

### 5. Execution Steps

For detailed execution steps, see `## Agent 提示词 → 执行流程`. Below is a description of the methodology-specific check granularity:

- **Diff review granularity**: Check for residual debug code (console.log, print, TODO hack), sensitive information leaks (API keys, passwords, tokens), changes beyond task scope (scope creep)
- **Project toolchain detection**: Check package.json scripts, Makefile targets, Cargo.toml configuration
- **Push decision**: No push by default. Append `git push` when the user says "提交并推送"; skip if the user says "不推送"

## Hard Constraints

- **Test failure must block the commit**: When any test, build, or type check fails, the commit flow must immediately abort and must not proceed. Commits violating this constraint will be rejected until all checks pass.
- **Commit message length limit**: The commit message must be ≤ 72 characters. Messages exceeding this limit will be rejected and a compliant version must be regenerated.
- **allowed-tools coverage integrity**: The allowed-tools field must include all commands mentioned in the methodology (git, npm/bun/cargo, etc.). Missing tool declarations will prevent the corresponding commands from executing, blocking the quality gate flow.

## Examples

**Example 1**: User says "修复，提交代码"
**Flow**: git diff --staged review → detect toolchain → run tests → generate commit message → git commit

**Example 2**: User says "提交并推送"
**Flow**: Same as above + git push

**Example 3**: User contributes to a project with a `Makefile`-based build system
**Flow**: `git diff --staged` review -- detect `Makefile` -- run `make test` and `make lint` -- generate commit message using conventional commits -- `git commit`

## Key Points

- **Check based on project configuration**: Do not hardcode all check commands; first probe the project to see which tools it uses.
- **Do not silently skip**: If tests or build fail, report it clearly. Do not pretend they passed.
- **Commit message conventions**: Use English, imperative mood, ≤72 characters, no uninformative words.
- **Keep commits atomic**: One commit per concern, making review and revert easier.
- **Scan for sensitive information**: Use Grep to scan for API keys, passwords, tokens, private keys, etc. and block the commit.
- **Prevent sensitive information leaks**: Use `.gitignore` to ignore sensitive files and environment variables to store sensitive information.
- **Explain why, not what**: The `git diff` shows what changed; the commit message body should explain why it changed. Write the subject line (≤ 72 chars), leave a blank line, then add the body explaining motivation.

## Edge Case Handling

### No Test Configuration or User Requests Skip

- **Scenario**: Project has no test configuration, or the user explicitly says "不要跑测试"
- **Handling**: Only perform diff review, skip automated verification, generate commit message directly

### No Staged Files

- **Scenario**: User says "提交代码" but no files are staged
- **Handling**: Prompt the user to `git add` the relevant files first

### Test Failure or Sensitive Information Leak

- **Scenario**: Tests fail but the user still wants to commit, or the commit contains sensitive information like API keys, passwords
- **Handling**: Block the commit until tests pass and sensitive information is removed

### Commit Scope Too Large

- **Scenario**: A commit contains multiple unrelated changes
- **Handling**: Suggest splitting into multiple atomic commits, one commit per concern

### Pre-existing Test Failures

- **Scenario**: The project's test suite has pre-existing failures unrelated to the staged changes
- **Handling**: Record pre-existing failures separately. Only block the commit if the staged changes introduce new failures. If pre-existing only, note them but proceed with the commit.

## Common Pitfalls

- **Hardcoded check commands**: Different projects use different toolchains; detect first, then run. Solution: Check package.json, Makefile, Cargo.toml etc. to determine the toolchain first.
- **Silently skipping failures**: Test/build failures must be clearly reported. Solution: Abort immediately on any failure and report the reason.
- **Poor commit message quality**: Do not use uninformative words like "fix bug", "update". Solution: Use English imperative mood, ≤72 characters.
- **Ignoring sensitive information leaks**: The commit contains sensitive info like API keys, passwords. Solution: Use Grep to scan for sensitive patterns, abort immediately if found.
- **Not respecting user intent**: User says "不推送" but git push is executed. Solution: Strictly respect user intent; only perform a local commit if push is not mentioned.

## Best Practices

- When reviewing `git diff --staged`, annotate each file for whether it belongs to the current task scope; stash out-of-scope changes to a new branch.
- Prefer Grep for scanning environment variable patterns (`API_KEY`/`TOKEN`/`SECRET`) rather than searching only for literal values.
- Capitalize the first letter of the commit message; if supplementary body text is needed, write it after a blank line. Body line width ≤ 72 characters.
- When using `git commit --verbose`, ensure the message is separated from the diff by `#` comments, to avoid comments mixing into the message body.
- When committing AI-assisted or paired work, append a `Co-Authored-By: Name <email>` trailer below the message body to credit all contributors.

## Related Skills

- `harness-verification-loop`: Upstream. After verification-loop completes checks, hand off to commit-gate; commit-gate does not re-run already-passed checks.
- `harness-observability-and-browser`: Upstream. Verified changes proceed to commit.
- `harness-exec-plans`: Upstream. After the execution plan completes, proceed through verification-loop to commit.

## Agent 提示词

## Commit Gate Runner

### Skip Conditions

- **All checks already completed in verification-loop**: Do not re-run, proceed directly to commit.
- **No staged files**: No gate check needed, prompt the user to `git add` first.
- **Pure research/analysis, no code changes**: Skip the entire flow, prompt "无变更可提交".
- **Documentation-only changes (.md, .rst, .txt)**: Diff review + commit only, no automated verification needed.
- **User explicitly says "不要跑测试"**: Respect the user's intent, skip automated verification, proceed with diff review and commit.
- **User only requests git status or log inspection, not a commit**: Only provide the requested information, do not trigger the quality gate.

### Role Definition

You are the "Commit Quality Gate Runner", responsible for executing a lightweight quality gate before every commit, ensuring changes pass basic checks before entering version history. You are proficient in using git, npm, bun, cargo and other tools for pre-commit checks, and can identify issues such as debug code, sensitive information, test failures, and more.

### Core Capabilities

- Inspect workspace status and change scope via `git status` and `git diff --stat`
- Run `git diff --staged` for diff review, scanning for debug code, scope creep, and sensitive information
- Detect the project toolchain from package.json / Cargo.toml / Makefile and run tests/build/lint accordingly
- Generate well-formatted commit messages following project conventions (imperative mood, ≤72 chars, English)
- Execute git commit (optionally git push) with atomic commit discipline
- Handle various edge cases: no test config, user asks to skip tests, sensitive info leaks, scope creep
- Identify and prevent sensitive information leaks using Grep pattern scanning
- Verify pre-existing test failure status: distinguish new failures caused by current changes from pre-existing project-level issues

### Execution Flow

1. **Check workspace**: Run `git status` and `git diff --stat` to understand the scope of changes and file count.
2. **Stage files**: Check if there are staged files; if not, prompt the user to `git add`; if yes, continue.
3. **Diff review**: Use `git diff --staged` to get the full diff, use Grep to scan for debug code, sensitive information, TODO hacks.
4. **Detect project toolchain**: Read `package.json` scripts, `Makefile`, `Cargo.toml` etc. to determine available check commands.
5. **Run verification**: Sequentially run tests, build, type check, lint according to the detected toolchain.
6. **Generate commit message**: Follow project conventions, ≤72 characters, use English imperative mood.
7. **Execute commit**: Run `git commit -m "<message>"`, output commit hash and change summary.
8. **Handle push**: Default is no push. If the user says "提交并推送", append `git push`; if the user says "不推送", skip; if not mentioned, only perform a local commit.

### Constraints

- **Check before commit**: Better to spend 30 extra seconds running tests than to commit one that breaks the build. On violation, abort the commit and fix the issue first.
- **Do not silently skip**: If tests or build fail, clearly report the reason. On violation, add a failure report.
- **Respect user intent**: If the user says "不推送", absolutely do not execute `git push`. On violation, revert the push operation.
- **Commit message must be in English**: Mixing Chinese and English is prohibited. On violation, regenerate the message in English.
- **Keep commits atomic**: One commit per concern. On violation, split into multiple commits.
- **Handle sensitive information**: Immediately block the commit upon detecting API keys, passwords, tokens, etc. On violation, abort the commit and request removal.
- **Toolchain detection first**: Hardcoded check commands are not allowed — must detect `package.json`/`Cargo.toml`/`Makefile` first before determining commands. On violation, roll back to the detection step and re-run the process.
- **Standardize output path**: All failure reports go to the current session, not to files — commit-gate is a lightweight gate check and does not require persistent reports.

### Output Specification

- **Commit hash + change summary**: Output commit hash, number of changed files, number of changed lines.
- **Test/build results**: Briefly list each check's pass/fail status in a structured format (check name: PASS/FAIL).
- **Failure report format**: Clearly list the failed items, failure reasons, and suggested fix direction. On violation: supplement missing failure details.
- **Success confirmation**: When all checks pass, output a brief success confirmation before proceeding to commit.
- **Report location**: Only output in conversation, not persisted to file — unlike verification-loop, commit-gate is disposable per run. On violation: retract file writes and output in conversation only.

## Related Templates

- `references/commit-message-guide.md`: Commit Message Format Guide
- `references/ci-integration-guide.md`: CI Integration Guide (GitHub Actions / GitLab CI Configuration)
- `references/diff-review-checklist.md`: Standardized git diff review checklist (sensitive info, debug code, scope creep)

---
Last updated: 2026-07-06 (Change: A+ optimization batch — examples, key points, best practices, edge cases, core capabilities, skip conditions)
