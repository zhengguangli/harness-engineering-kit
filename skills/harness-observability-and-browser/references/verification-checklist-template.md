# Verification Checklist

Populated by the `qa-verifier` agent on each verification cycle. Attached as acceptance evidence to the PR or exec-plan.

## Verification Overview

| Field | Content |
|------|------|
| Verification Goal | <!-- What this verification should confirm --> |
| Verification Type | UI / Performance / Reliability / Log |
| Environment | <!-- Browser version, device, network conditions, etc. --> |
| Verification Date | <YYYY-MM-DD> |

## UI Verification Results

| Check Item | Screenshot/Evidence | Result |
|--------|-----------|------|
| <!-- Expected behavior A --> | <!-- Screenshot or DOM snapshot path --> | ✅ Pass / ❌ Fail |
| <!-- Expected behavior B --> | | |

## Performance/Reliability Verification

| Metric | Constraint Threshold | Actual Value | Result |
|------|----------|--------|------|
| <!-- P99 latency --> | < 2s | <value> | ✅ Pass / ❌ Fail |
| <!-- Memory usage --> | < 200MB | <value> | |

## Log/Error Check

| Check Item | Result | Notes |
|--------|------|------|
| Console errors | Yes / No | <!-- List if any --> |
| Network request failures | Yes / No | |
| Expected log appears | Yes / No | |

## Conclusion

- **Pass**: All check items meet expectations
- **Partial Pass**: <!-- List check items that did not pass -->
- **Fail**: <!-- Describe key failures that require re-verification after fix -->

---
Last updated: <YYYY-MM-DD>
