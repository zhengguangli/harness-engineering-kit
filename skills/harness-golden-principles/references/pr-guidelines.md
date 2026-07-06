# Fix PR Specification Guide

## Purpose

Guides the `entropy-collector` agent on how to structure each fix PR, ensuring reviewers can complete the review and decide to merge or reject within one minute.

## PR Size Limits

- **Each fix PR handles only one type of deviation**: Do not mix in unrelated cleanups (e.g., "rename variable + change DB schema").
- **Max files per PR**: ≤ 5 files.
- **Max lines changed per PR**: ≤ 50 lines (additions + deletions combined).
- **Automatic splitting on exceed**: When exceeding the limit, split into multiple sequential PRs, each on its own branch chain without blocking one another.

## Auto-merge Rules

The following fix types are tagged with the `[GC-auto]` prefix and can be configured for auto-merge:

| Type | Example | Auto-merge Conditions |
|------|---------|-----------------------|
| Rename | Rename variables/functions to comply with naming conventions | Identifier-only changes, no logic changes |
| Extract common method | Extract duplicated code blocks | All original call sites reference the extraction consistently |
| Replace with standard SDK | Replace hand-written code with project's existing utility functions | Semantically equivalent after replacement, tests pass |
| Formatting | Indentation / blank lines / import order | Uses the project's configured formatter |

The following types require manual review:

- Changes to public API signatures
- Default value modifications that may affect runtime behavior
- Field/function deletions

## PR Title and Labels

```
[GC-auto] fix: Rename methods in UserRepository to camelCase
[GC-review] refactor: Extract common validateEmail function
```
