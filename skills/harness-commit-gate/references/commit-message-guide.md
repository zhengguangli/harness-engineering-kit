# Commit Message Guide

## Format Selection

First, check the project's git log style:

```bash
git log --oneline -10
```

If the project uses Conventional Commits:

```
type(scope): Describe the change in imperative mood

Optional detailed explanation (why this change was made)

Optional BREAKING CHANGE or issue reference
```

type types:
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Refactor (no external behavior change)
- `docs`: Documentation only
- `chore`: Build/tool/dependency changes
- `test`: Add or modify tests
- `style`: Code style adjustments (no logic change)
- `perf`: Performance optimization

If the project does not use Conventional Commits, use a concise imperative sentence:

```
Describe the core change in one sentence
```

## Good Commit Message Examples

- `feat(auth): add API key validation with minimum length check`
- `fix(stream): handle empty delta in SSE translation`
- `refactor: split monolithic logger into modular structure`
- `docs: update README with new endpoint documentation`

## Bad Commit Message Examples

- `fix bug` (What bug was fixed?)
- `update` (What was updated?)
- `changes` (What changes?)
- `WIP` (Don't commit WIP to main branch)

## Principles

- State "what was done", not file names
- Use imperative mood ("add" not "added")
- First line no more than 72 characters
- If more context is needed, write details after a blank line
- Commit messages must use **English**, no mixing of Chinese and English
- Keep each commit **atomic**: one commit does one thing, split by responsibility (don't bundle unrelated changes into one commit)

Last updated: 2026-06-30

## Machine-Verifiable Rules (Recommended)

- First line length: `subject <= 72`.
- Imperative mood hint (recommended): Start with a verb, e.g. `add/fix/refactor/docs/chore/test/style/perf`.
- Prohibit uninformative words (recommended): `fix bug` / `update` / `changes` / `WIP`.
- Language: English.
