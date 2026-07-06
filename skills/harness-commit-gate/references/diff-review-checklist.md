# Diff Review Checklist

> Standardized `git diff --staged` review checklist. Used by commit-gate to systematically inspect every staged change before committing.

## 1. Sensitive Information Scan

Check each added/modified line for:

| Pattern | Example | Action |
|---------|---------|--------|
| API keys / tokens | `sk-...`, `ghp_...`, `AKIA...` | **BLOCK** — abort commit, instruct removal |
| Hardcoded passwords | `password: "..."` | **BLOCK** — move to env var |
| Connection strings | `postgres://user:pass@host` | **BLOCK** — move to env var |
| Private URLs / IPs | `http://127.0.0.1`, internal hostnames | **REVIEW** — confirm intended exposure |
| `.env` files or `.env.*` content | Environment variable dumps | **BLOCK** — remove from tracked files |

**Script check**: `git diff --staged | grep -iE '(api.key|secret|token|password|sk-[a-zA-Z0-9]|ghp_|AKIA)'`

## 2. Debug / Temporary Code

| Pattern | Example | Action |
|---------|---------|--------|
| Console/print statements | `console.log("debug")`, `print(...)`, `fmt.Println(...)` | **WARN** — confirm intentional |
| TODO / FIXME / HACK | `// TODO: fix this later` | **WARN** — add issue reference or remove |
| Commented-out code | `// const oldVersion = ...` | **WARN** — remove unless documentation value |
| `.only` in test files | `it.only(...)`, `describe.only(...)` | **BLOCK** — removes isolated testing |
| Skip markers | `it.skip(...)` | **REVIEW** — confirm intentional |

**Script check**: `git diff --staged | grep -E '^\+\s*(console\.log|print\s*\(|fmt\.Print|#\s*TODO|FIXME|HACK|\.only\s*\(|\.skip\s*\()'`

## 3. Scope Creep Detection

Review the diff as a whole:

- **One concern per commit**: Does the diff touch unrelated areas? (e.g., a bugfix commit also refactoring unrelated code)
  - **Action**: Split into multiple commits; commit-gate aborts and suggests `git reset HEAD~` for re-splitting.
- **File count**: >10 files changed for a single commit on a small change
  - **Action**: Request clarification — is this really one change set?
- **Configuration drift**: Changes to `ci/*.yml`, `Dockerfile`, or deployment configs in a feature commit
  - **Action**: Flag for second review; these should typically be in separate commits.

## 4. Commit Message Quality

Check the generated commit message:

- **Format**: ≤ 72 characters first line, blank line, then body
- **Language**: English only, imperative mood (`Add`, `Fix`, `Refactor`, `Remove`)
- **Content**: Explain *why*, not just *what*

```
Good:  feat(auth): add refresh token rotation
       
       Rotate refresh tokens on each renewal to limit 
       exposure window if a token is leaked.

Bad:   fix bug
```

## 5. File-by-File Quick Scan

For each changed file (especially new ones):

- [ ] File extension is appropriate for content
- [ ] No binary file committed unintentionally (check `git diff --stat` for binary markers)
- [ ] New file has appropriate copyright/header if project convention requires it
- [ ] File is not empty (0-line files add noise)
- [ ] File path follows project naming conventions

## Usage

Run as part of commit-gate's diff review step:

```bash
# Full checklist (automated checks run first, then manual review items flagged)
python3 skills/harness-commit-gate/references/automated_check_script.py
# If warnings detected, prompt the user before proceeding
```
