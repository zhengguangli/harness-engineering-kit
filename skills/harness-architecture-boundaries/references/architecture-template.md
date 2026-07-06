# ARCHITECTURE.md

<!-- Canonical owner: harness-architecture-boundaries -->

This file defines the cross-domain architecture map and dependency direction rules. Rules should be encoded into lint/structured tests using the methods described in the `harness-architecture-boundaries` skill as much as possible, rather than remaining as textual descriptions only.

## Domain Breakdown

| Domain | Description | Corresponding Code Path |
|---|---|---|
| <Domain A> | ... | `src/<a>/` |
| <Domain B> | ... | `src/<b>/` |

## Internal Layering and Dependency Direction for Each Domain

```
Types → Config → Repo → Service → Runtime → UI
```

> This is an example layering, not a mandatory standard — define your own layers based on the project's actual situation, but keep the pattern of "fixed direction + limited legal edges."

- Dependencies can only flow "forward;" reverse imports are not allowed.
- Cross-cutting concerns (authentication, connectors, telemetry, feature flags) must not be scattered into arbitrary layers — they must enter through a single explicit `Providers` entry point.
- `Utils` holds cross-domain pure utility functions, can only be used by `Providers`, and must not depend on internal implementations of specific domains in reverse.

## Data Boundary Rules

- All cross-boundary data (external API responses, user input, database read results) must be parsed into strongly-typed structures upon entering the boundary.
- On parse failure, the error should be surfaced explicitly at the boundary rather than allowing unparsed data to propagate downstream.

## Mechanical Enforcement Status

| Rule | Enforcement Method | Status |
|---|---|---|
| Layering dependency direction | <lint tool/script name> | ✅ Enforced / ⚠️ Documentation only, not enforced |
| Data boundary parsing | <lint tool/script name> | ✅ / ⚠️ |
| <Add other rules> | | |

> Any rule marked as "⚠️ Documentation only, not enforced" should be treated as a TODO — violations found by the `boundary-auditor` agent inspection, or add the corresponding lint rule.

---
Last updated: <YYYY-MM-DD>
