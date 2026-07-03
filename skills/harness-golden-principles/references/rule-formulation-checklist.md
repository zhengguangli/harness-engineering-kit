# Golden Principle Formulation Checklist

Before encoding a piece of "human taste" as a golden principle, verify each item below. Pass all items to indicate the principle is suitable for inclusion.

## 1. Signal Source Check

| Check | Passed? | Notes |
|-------|---------|-------|
| The feedback has appeared ≥ 2 times in recent reviews | □ | From at least two independent reviews |
| Corresponds to a traceable bug/defect report | □ | Not "it just feels this way" |
| Comes from style discussion, not architectural debate | □ | Architectural issues belong to architecture-boundaries |
| Has concrete code examples showing "what is bad" | □ | Cannot rely on abstract description alone |

## 2. Executability Check

| Check | Passed? | Notes |
|-------|---------|-------|
| Can it be written as a lint rule? | □ Yes □ No | If yes, prefer writing a lint rule |
| If not a lint rule, can it be detected via grep? | □ | At least 80% detection rate |
| Are the fix steps specific enough to say "which file to change what"? | □ | Cannot just say "refactor XXX" |
| Does the fix require ≥ 10 minutes? | □ Yes □ No | If yes, consider splitting the principle |

## 3. Impact Scope Check

| Check | Passed? | Notes |
|-------|---------|-------|
| Does the principle apply to > 80% of project files? | □ | Rules affecting only a few files are not worth scanning weekly |
| Does violating the principle lead to deteriorating consequences over time? | □ | e.g., "unaddressed, it accumulates significant tech debt" |
| Can an auto-fix be reviewed in under a minute? | □ | Fix PRs must be small enough |

## 4. Periodic Review Reminder

- Re-check this checklist during quarterly audits. Principles with no matches for three consecutive cycles should be retired.
- When a principle becomes obsolete due to framework upgrades or refactoring, mark it as deprecated rather than deleting it directly (preserve historical context).
