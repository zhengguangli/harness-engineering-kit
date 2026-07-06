# Loop Troubleshooting Guide

> Diagnosis guide for stuck verification loops. Referenced when the verification-loop runner detects two consecutive iterations with substantially unchanged `git diff` output.

## Stuck Detection Triggers

The stuck detector activates when **both** conditions are met:

1. Consecutive iterations ≥ 2 with `git diff` output > 80% identical (same files, same changed lines)
2. At least one acceptance criterion remains failing

## Diagnosis Matrix

### Symptom: Tests keep failing, no code change between rounds

| Possible Cause | Check | Fix |
|---------------|-------|-----|
| Test misconfiguration | Are tests failing on `main` too? | Flag as pre-existing; skip and document |
| Non-deterministic test | Run the failed test 3 times individually | Add retry-with-clean-state pattern or mark as flaky |
| Missing mock/dependency | Does the test require external services? | Skip integration tests; flag "needs environment setup" |

### Symptom: Lint keeps failing, auto-fix not applied

| Possible Cause | Check | Fix |
|---------------|-------|-----|
| Lint auto-fix disabled | Does `eslint --fix` / `prettier --write` exist? | Run auto-fix, then re-check |
| Custom lint rule violation | Is the rule documented in golden-principles? | If new, add to principles; if existing, follow the principle's fix recommendation |
| Formatting drift large | Multiple files with style violations | Delegate to `golden-principles` as a separate cleanup PR |

### Symptom: Build keeps failing

| Possible Cause | Check | Fix |
|---------------|-------|-----|
| Type error in changed code | `tsc --noEmit` output stable between rounds? | Re-read the type definition and fix the type |
| Missing import | `git diff` shows the new file but import missing? | Add the import |
| Dependency not installed | `npm install` / `bun install` needed? | Run install step |

### Symptom: Diff unchanged after claimed "fix"

| Possible Cause | Check | Fix |
|---------------|-------|-----|
| Agent hallucinated the fix | Did it actually `Write`/`Edit` the file? | Check shell output for write confirmation |
| Fix in the wrong file | Did it edit the test instead of the source? | Re-read both files; redirect Edit to the correct file |
| Fix reverted by later step | Did a subsequent tool call overwrite the fix? | Re-execute the fix as the last step before re-checking |

### Symptom: Infinite review loop (review → fix → more review)

| Possible Cause | Check | Fix |
|---------------|-------|-----|
| Review requirements too broad | Unclear definition of done? | Narrow acceptance criteria to the minimum verifiable |
| Reviewer and fixer disagree on approach | Divergent design opinions? | Escalate to human for decision |
| New issues found in fixed area | Scope creep via review | Log new issues as tech debt, don't block this iteration |

## Resolution Steps

When stuck is detected:

1. **Stop** — Abort the current iteration immediately. Do not attempt another fix-and-check.
2. **Diagnose** — Read this guide; match symptoms to the matrix above.
3. **Document** — Write the stuck reason in the iteration log: what was attempted, what failed, and what capability is missing.
4. **Decide** — Choose one of:
   - **Fix root cause** (clear misconfiguration or missing tool)
   - **Skip this criterion** (pre-existing failure, document reason)
   - **Escalate to human** (design disagreement, irreversible operation)
5. **Resume or abort** — After resolution, either continue with the fix applied or close the loop with the documented reason.

## Prevention

- Keep each iteration's change small and focused — large diffs are harder to diagnose when stuck.
- Run lint and type checks *before* the first test run, so the loop doesn't get stuck on formatting.
- For long-running loops, checkpoint in `docs/exec-plans/active/` every 3 iterations so the next agent can pick up from the last checkpoint.

## See Also

- `references/completion-summary-template.md` — output format for the completion summary
- `references/stuck-loop-diagnostics.md` — original diagnostics reference (kept for historical compatibility)
