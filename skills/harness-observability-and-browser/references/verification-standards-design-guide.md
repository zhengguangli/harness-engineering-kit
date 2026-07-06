# Verification Standards Design Guide

## Design Principles

Acceptance criteria must satisfy the **MECE principle** (Mutually Exclusive, Collectively Exhaustive):
- **Mutually Exclusive**: Each criterion checks an independent dimension, with no overlap
- **Collectively Exhaustive**: All criteria together cover the complete verification goal

## Criteria Classification

### By Verification Type

| Type | What It Checks | Tool | Example |
|---|---|---|---|
| UI Verification | Page rendering, interaction flow | Browser automation | "A confirmation dialog appears after button click" |
| Performance Verification | Latency, throughput, resource usage | Metric query | "P99 latency < 800ms" |
| Reliability Verification | Error rate, recovery time, availability | Logs + metrics | "Error rate < 0.1%" |
| Security Verification | Permissions, input validation, encryption | Static + dynamic analysis | "SQL injection test passes" |

### By Verification Timing

| Timing | Purpose | Example |
|---|---|---|
| Smoke Test | Basic functionality works | "Login flow works correctly" |
| Regression Test | Changes do not break existing functionality | "Old API still returns correct format" |
| Performance Test | Meets performance constraints | "P99 latency < 800ms" |
| Chaos Test | Fault tolerance and recovery capability | "Recovers within 30 seconds after service outage" |

## Standards Writing Guidelines

### Format Requirements

Each criterion must include:
1. **Measurable indicator**: Numeric, queryable
2. **Threshold**: Clear pass/fail boundary
3. **Verification method**: How to obtain evidence
4. **Judgment rule**: What constitutes a pass

### Example Comparison

```markdown
# ❌ Bad: vague, not measurable
- Page load speed should be fast
- User experience should be good
- The system should be stable

# ✅ Good: specific, measurable
- Page load time < 3s (measured by Lighthouse)
- P99 API latency < 800ms (Prometheus query)
- Error rate < 0.1% (log statistics over the past hour)
- Key user journey screenshots match design specs (visual regression comparison)
```

### Standards Template

```markdown
## Acceptance Criteria

### Functional Verification
| Criterion | Threshold | Verification Method | Evidence |
|---|---|---|---|
| Login flow | Successfully redirects to dashboard | Playwright E2E test | Screenshot + logs |
| Form submission | Data correctly written to database | API test + DB query | Query results |

### Performance Verification
| Criterion | Threshold | Verification Method | Evidence |
|---|---|---|---|
| Page load time | < 3s | Lighthouse test | Report screenshot |
| API P99 latency | < 800ms | Prometheus query | Query results |
| Error rate | < 0.1% | Log analysis | Analysis results |

### Reliability Verification
| Criterion | Threshold | Verification Method | Evidence |
|---|---|---|---|
| Service availability | > 99.9% | Monitoring system | Dashboard screenshot |
| Fault recovery time | < 30s | Chaos test | Test logs |
```

## Verification Target Routing

Select verification criteria based on change type:

```
Change type determination:
├── Pure UI changes → UI verification criteria
├── API changes → Performance + functional verification criteria
├── Database changes → Functional + reliability verification criteria
├── Configuration changes → Smoke test criteria
└── Mixed changes → Combined verification criteria
```

### UI Change Verification Criteria

```markdown
- Page renders normally (no JS errors)
- Interaction flow is complete (click -> response -> result)
- Visual regression passes (screenshot difference < 1%)
- Responsive layout works (mobile/desktop)
```

### API Change Verification Criteria

```markdown
- API returns correct format (Schema validation)
- Response time < threshold
- Status codes are correct (4xx/5xx)
- Backward compatible (old client can still call)
```

### Database Change Verification Criteria

```markdown
- Data migration succeeds (no data loss)
- Query performance does not degrade (P99 < threshold)
- Data consistency (master-slave sync normal)
- Rollback plan is available

```

## Capability Gap Handling

### Gap Identification

When the project lacks the observability capabilities required for verification, record the gap:

```markdown
## Capability Gaps

| Gap | Impact | Suggested Fix |
|---|---|---|
| Missing structured logging | Cannot query specific errors | Add JSON format logs |
| Missing performance metrics | Cannot verify P99 latency | Integrate Prometheus |
| Missing E2E tests | Cannot verify user journeys | Add Playwright tests |
```

### Gap Handling Principles

1. **Do not skip verification**: A capability gap is not an excuse to "skip verification"
2. **Record the gap itself**: Gaps are "environmental deficiencies" to be fixed
3. **Degraded verification**: Use available means to perform partial verification
4. **Be explicit about confidence**: Note "Due to missing X, conclusion confidence is low"

## Verification Report Template

```markdown
## Verification Report

### Basic Information
- Verification Time: YYYY-MM-DD HH:MM
- Verification Environment: [environment name]
- Verification Scope: [change description]

### Verification Results
| Criterion | Expected | Actual | Result | Evidence |
|---|---|---|---|---|
| Page load time | < 3s | 2.1s | ✅ | Lighthouse report |
| API P99 latency | < 800ms | 650ms | ✅ | Prometheus query |
| Error rate | < 0.1% | 0.05% | ✅ | Log analysis |

### Capability Gaps
| Gap | Impact | Suggestion |
|---|---|---|
| Missing X | Cannot verify Y | Add Z |

### Conclusion
- Overall Result: ✅ Pass / ❌ Fail
- Failed Items: [list]
- Suggestion: [next steps]
```
