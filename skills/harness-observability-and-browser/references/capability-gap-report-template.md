# Capability Gap Report Template

## Usage

When the project lacks the observability capabilities required for verification (e.g., no browser automation tool, no performance monitoring, no structured logging), use this template to record the gap.

## Report Template

```markdown
# Capability Gap Report

## Basic Information
- **Report Time**: YYYY-MM-DD HH:MM
- **Reporter**: [agent name]
- **Project**: [project name]
- **Related Task**: [task requiring verification that cannot be completed]

## Gap List

### Gap 1: [Gap Name]

| Field | Content |
|---|---|
| **Gap Description** | [what capability is missing] |
| **Impact Scope** | [which verification tasks are affected] |
| **Current Status** | [existing workaround if any] |
| **Workaround Confidence** | High / Medium / Low ("Low" when no evidence supports it) |
| **Suggested Fix** | [how to fill this gap] |
| **Priority** | P0 / P1 / P2 |
| **Estimated Effort** | [estimate] |

**Affected Verification Tasks**:
- Task 1: [description] → Cannot execute, reason: [reason]
- Task 2: [description] → Degraded execution, reason: [reason]

**Workaround** (if any):
- [workaround description]
- Confidence note: [why confidence is High/Medium/Low]

### Gap 2: [Gap Name]

[Same format as above]
```

## Common Gap Types

### Type 1: Missing Browser Automation Tool

```markdown
### Gap: Playwright/Puppeteer Not Installed

| Field | Content |
|---|---|
| **Gap Description** | No browser automation tool is installed in the environment |
| **Impact Scope** | All UI verification tasks |
| **Current Status** | Can only infer UI behavior by reading code statically |
| **Workaround Confidence** | Low (cannot verify actual rendering results) |
| **Suggested Fix** | Run `npm init playwright@latest` to install |
| **Priority** | P0 |
| **Estimated Effort** | 10 minutes |

**Affected Verification Tasks**：
- Reproduce UI bug → Cannot execute
- Verify user journey → Cannot execute
- Screenshot comparison → Cannot execute

**Workaround**：
- Static code analysis to infer UI behavior
- Confidence: Low — writing a try-catch in code does not mean the exception was actually caught
```

### Type 2: Missing Performance Monitoring

```markdown
### Gap: Prometheus/Grafana Not Deployed

| Field | Content |
|---|---|
| **Gap Description** | Project has no performance metric collection and querying capability |
| **Impact Scope** | All performance verification tasks |
| **Current Status** | Cannot query P99 latency, error rate, etc. |
| **Workaround Confidence** | Low (unable to obtain runtime performance data) |
| **Suggested Fix** | Deploy Prometheus + Grafana, or integrate Datadog |
| **Priority** | P1 |
| **Estimated Effort** | 2-4 hours |

**Affected Verification Tasks**：
- P99 latency verification → Cannot execute
- Error rate verification → Cannot execute
- Throughput verification → Cannot execute

**Workaround**：
- Manually calculate latency using timestamps in application logs
- Confidence: Medium — log sampling may be incomplete
```

### Type 3: Missing Structured Logging

```markdown
### Gap: Logs in Free-Text Format

| Field | Content |
|---|---|
| **Gap Description** | Application logs use free-text format instead of JSON structured format |
| **Impact Scope** | Log query and analysis tasks |
| **Current Status** | Can only do full-text search, cannot filter by field |
| **Workaround Confidence** | Medium (full-text search can partially substitute) |
| **Suggested Fix** | Switch to JSON format logs, add requestId/service and other fields |
| **Priority** | P1 |
| **Estimated Effort** | 4-8 hours |

**Affected Verification Tasks**：
- Error log query → Degraded execution (full-text search)
- Request trace analysis → Cannot execute
- Error rate calculation → Degraded execution (manual counting)

**Workaround**：
- Use grep to full-text search error logs
- Confidence: Medium — cannot filter precisely by field
```

### Type 4: Missing Distributed Tracing

```markdown
### Gap: No Distributed Tracing System

| Field | Content |
|---|---|
| **Gap Description** | Multi-service architecture lacks request tracing |
| **Impact Scope** | Cross-service latency analysis, trace debugging |
| **Current Status** | Can only view per-service logs, cannot correlate request traces |
| **Workaround Confidence** | Low (cannot obtain complete trace data) |
| **Suggested Fix** | Integrate Jaeger/Zipkin, add trace ID propagation |
| **Priority** | P2 |
| **Estimated Effort** | 1-2 days |

**Affected Verification Tasks**：
- Cross-service latency analysis → Cannot execute
- Trace bottleneck identification → Cannot execute
- Cascading failure analysis → Cannot execute

**Workaround**：
- Manually search for the same requestId across each service's logs
- Confidence: Low — time-consuming and easy to miss
```

## Gap Priority Definitions

| Priority | Definition | Fix Timeline |
|---|---|---|
| P0 | Blocks core verification tasks | Fix immediately |
| P1 | Affects important verification tasks | Fix within this iteration |
| P2 | Affects auxiliary verification tasks | Fix in next iteration |

## Gap Handling Flow

```
Capability gap discovered
├── Record gap (use template)
├── Assess priority
│   ├── P0 → Report to user immediately, recommend fix
│   ├── P1 → Record and report, recommend fix this iteration
│   └── P2 → Record, recommend adding to backlog
├── Degraded verification (if workaround available)
│   ├── Workaround confidence High → Execute workaround
│   ├── Workaround confidence Medium → Execute but note confidence
│   └── Workaround confidence Low → Skip, mark as unverifiable
└── Produce report
    ├── Gap list
    ├── Degraded verification results
    └── Fix recommendations
```

## Integration with verification-loop

Add a capability gap check in the self-check step of verification-loop:

```markdown
## Self-Check List
- [ ] Is there a browser automation tool in the environment?
- [ ] Is there a performance monitoring system in the environment?
- [ ] Does the application use structured logging?
- [ ] Is there distributed tracing in a multi-service architecture?

If any item is "No", generate a capability gap report and note the affected verification tasks.
```
