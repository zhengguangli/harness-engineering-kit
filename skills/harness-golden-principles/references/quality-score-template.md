# QUALITY_SCORE.md

<!-- Canonical owner: harness-golden-principles -->

Tracks code quality and architectural consistency scores by domain/layer, observing whether gaps are converging or widening over time. Updated by the `entropy-collector` agent during periodic sweeps.

## Scoring Dimensions (examples, adjust per project)

- **Structural Consistency**: Whether dependency directions defined in `ARCHITECTURE.md` are followed.
- **Golden Principle Compliance**: Violation density of taste/idiom rules encoded in `harness-golden-principles`.
- **Test Coverage**: Test coverage for critical paths.
- **Document Freshness**: Whether corresponding `docs/design-docs/` entries have been recently validated.

## Current Scores

| Domain | Structural Consistency | Golden Principle Compliance | Test Coverage | Document Freshness | Last Assessment Date |
|--------|------------------------|----------------------------|---------------|--------------------|----------------------|
| <Domain A> | <score/grade> | <score/grade> | <score/grade> | <score/grade> | <YYYY-MM-DD> |
| <Domain B> | | | | | |

## Trend Notes

Records which dimensions are improving or deteriorating compared to the previous cycle, along with suspected causes (e.g., "a concentrated spike of a certain violation type in a newly onboarded domain suggests that domain has not yet added the corresponding lint rules").

---
Last updated: <YYYY-MM-DD>
