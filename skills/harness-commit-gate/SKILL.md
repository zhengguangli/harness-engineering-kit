---
name: harness-commit-gate
description: Run a lightweight pre-commit quality gate on staged changes — diff review (secrets/debug/scope), toolchain-detected tests/build/lint, and imperative commit message formatting. Used for committing code, preparing to push, and pre-commit checks.
when_to_use: |
  显式触发：用户说"提交代码"、"commit"、"git commit"、"代码提交"、"修复后提交代码"。
  隐式触发：用户完成了代码修改并准备提交、verification-loop 已完成并需要提交、用户询问如何提交代码。
  不触发：已在 verification-loop 完成全部检查（不要重复跑）、无 staged 文件（没有东西需要门检）、纯调研/分析不产出代码变更。
disable-model-invocation: true
context: fork
allowed-tools: Read Grep Glob Bash(git *) Bash(ls *) Bash(npm *) Bash(bun *) Bash(cargo *) Bash(vitest *) Bash(tsc *) Bash(bunx *) Bash(make *) Bash(just *) Bash(python3 *) Bash(pytest *) Bash(go *) Bash(ruff *) Bash(mypy *)
agent: commit-gate-runner
compatibility: claude-code
depends_on:
  - harness-verification-loop
  - harness-observability-and-browser
  - harness-exec-plans
metadata:
  category: workflow
---
# Commit Gate

> Single-pass pre-commit gate, not an iterative repair loop: inspect staged diff, run project-detected checks, format message, and block cleanly on any new failure or secret leak.

## Scope & Skip Conditions

- **Use when**: Changes are staged (`git diff --staged`) and ready for a final pre-commit gate.
- **Skip when**: No staged files (prompt `git add`), pure `git status`/`git log` inspection, doc-only changes (skip test run, keep diff review + commit), or user explicitly opts out of tests. If tests never ran and fail, block and hand back to `harness-verification-loop`.

## Hard Constraints

1. **Test/build/secret failure blocks commit**: Immediately abort on newly introduced test/build/type/lint failures or detected secrets (`API_KEY`, `TOKEN`, `SECRET`). For pre-existing failures, proceed only after verifying baseline failure status on the base commit and noting them separately. Violation → abort commit.
2. **Commit message subject line ≤ 72 characters (body lines ≤ 72)**: English, imperative mood, explaining *why*, one concern per commit. Violation → regenerate compliant message.
3. **Complete `allowed-tools` coverage**: All commands used in diff scanning and toolchain detection (`git`, `Grep`/`Read`, `ls`, `npm`/`bun`/`cargo`/`pytest`/`go`/`make`/`just`) must stay declared in frontmatter. Violation → update `allowed-tools` before running.
4. **Strict push intent**: Default to local commit only; run `git push` solely if the original request asks to push. Never run `git push --force-with-lease` if wrongly pushed — report immediately.

## Related Skills

- input      **harness-verification-loop**: Hands off converged diff after iterative checks pass
- input      **harness-observability-and-browser**: Supplies verified UI/runtime evidence
- input      **harness-exec-plans**: Hands off after plan acceptance criteria pass
- see-also   **harness-golden-principles**: Advisory style/commit conventions

## Related Templates

- `references/diff-review-checklist.md`: Staged diff secret/debug/scope checklist
- `references/commit-message-guide.md`: Conventional Commits & message format guide
- `references/ci-integration-guide.md`: CI alignment across Node/Rust/Python/Go

## Agent 提示词

## commit-gate-runner (Commit Gate Runner)

### Role & Execution Contract

1. **Check workspace & staged diff**: Run `git status` and `git diff --stat`. If nothing is staged, prompt `git add` and stop. Inspect every file in `git diff --staged` via `Grep`/checklist (`references/diff-review-checklist.md`) for secrets, debug code, and scope creep (abort and suggest `git reset HEAD` if mixed concerns).
2. **Detect & run toolchain**: Probe `package.json`/`bun.lock`, `Cargo.toml`, `pyproject.toml`/`pytest`, `go.mod`, `Makefile`, or `Justfile` (skip automated tests only for doc-only diffs or explicit user skip; hand back to `harness-verification-loop` if un-converged tests fail).
3. **Format & commit**: Generate an English imperative subject ≤ 72 chars (`references/commit-message-guide.md`), run `git commit -m ...`, and evaluate push intent strictly from the original request (default: local commit only).

### Constraints

- **No silent skips & no force-push**: Report every check's `PASS/FAIL` explicitly; never force-push on error. On violation → emit missing failure details / report push error.
- **Atomic commits & conversation-only reports**: Never persist report files to disk. On violation → retract report files and split mixed changes.

### Output Specification

- **Destination**: Conversation only — no report file is persisted to disk.
- **Content**: Per-check `PASS/FAIL` summary, commit hash + changed file/line counts on pass, or explicit failure reasons and fix direction when blocked.

---
Last updated: 2026-11-18 (Change: refactored to lean contract format; fixed allowed-tools coverage gap and subject-line/pre-existing failure wording)
