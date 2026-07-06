# Golden Principle Prioritization Guide

## Scoring Dimensions

Each candidate golden principle is scored on three dimensions (1-5 points). The total score determines processing priority.

| Dimension | 1 point | 3 points | 5 points |
|-----------|---------|----------|----------|
| **Impact Scope** (weight 3x) | Affects < 5% of code | Affects 20-50% of code | Affects > 80% of code |
| **Harm Severity** (weight 2x) | Style inconsistency only | Causes minor but accumulating maintenance cost | Directly causes defects or performance degradation |
| **Fix Cost** (weight 1x) | Requires manual review per occurrence (> 1 min/occurrence) | Semi-automated repair possible | Bulk-modifiable via `sed` / `lint --fix` |

**Total Score = Impact Scope × 3 + Harm Severity × 2 + Fix Cost × 1**

## Priority Matrix

| Score Range | Priority | Action Strategy |
|-------------|----------|-----------------|
| ≥ 25 | P0 -- Immediate | Include in this week's sweep |
| 18-24 | P1 -- This Week | Schedule into this week's queue |
| 10-17 | P2 -- This Month | Include in monthly plan |
| ≤ 9 | P3 -- Standby | Re-evaluate at quarterly audit; retire after three consecutive P3 ratings |

## Example Calculation

**Principle: Prohibit `console.log` in loops**
- Impact Scope: 4 (40% of files contain loop logic and may violate during logging)
- Harm Severity: 3 (causes cluttered logs, but does not affect functionality)
- Fix Cost: 5 (detectable via lint rule `no-console` with `allow: []` configuration)

Total Score = 4×3 + 3×2 + 5×1 = 23 → P1 (process this week)
