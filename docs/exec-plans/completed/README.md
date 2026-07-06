# Completed Execution Plans

This directory stores **completed** execution plans — plans whose goals have been fully achieved and whose details no longer require active tracking.

## Purpose

- Archive plans that are done but worth keeping for historical reference.
- Prevent `docs/exec-plans/active/` from accumulating stale entries.
- Provide stable file paths that `docs/exec-plans/tech-debt-tracker.md` and other documents can reference by name.

## Lifecycle

1. Plan is created → placed in `docs/exec-plans/active/`.
2. Plan is fully executed → moved or copied here.
3. Stale, superseded, or fully absorbed plans → kept as stubs pointing to current documentation.

## Naming Convention

`<short-description>-<YYYY-MM-DD>.md`

Dates indicate when the plan was finalized or moved to completed status.

## Related Docs

- Active plans: `docs/exec-plans/active/`
- Tech debt tracker: `docs/exec-plans/tech-debt-tracker.md`
