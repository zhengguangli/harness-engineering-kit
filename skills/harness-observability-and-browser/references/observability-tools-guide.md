# Observability Tools Guide

## Three Pillars

Observability consists of three core pillars:

| Pillar | Data Type | Query Method | Use Cases |
|---|---|---|---|
| Logs | Discrete events | Full-text search / structured query | Debugging specific errors, auditing |
| Metrics | Aggregated values | PromQL / query language | Performance monitoring, alerting |
| Traces | Request chains | Trace ID lookup | Cross-service latency analysis |

## Log Verification

### Structured Logging Standards

```json
{
  "timestamp": "2026-07-02T10:30:00Z",
  "level": "error",
  "message": "Failed to process order",
  "service": "order-service",
  "requestId": "req-abc-123",
  "userId": "user-456",
  "error": {
    "type": "ValidationError",
    "message": "Invalid order total",
    "stack": "..."
  },
  "context": {
    "orderId": "order-789",
    "total": -100
  }
}
```

**Required Fields**:
- `timestamp`: ISO 8601 format
- `level`: info/warn/error
- `message`: Human-readable description
- `service`: Service name
- `requestId`: Request trace ID

### Log Query Verification Patterns

**Verify whether exceptions are caught**:

```
# Query error logs within a specific time range
service="order-service" level="error" timestamp >= "2026-07-02T10:00:00Z"

# Verify whether a specific error occurred
service="order-service" level="error" message="*timeout*"

# Verify error rate
count(service="order-service" level="error") / count(service="order-service")
```

**Verify business events**:

```
# Verify order creation succeeded
service="order-service" message="Order created" orderId="order-789"

# Verify payment completed
service="payment-service" message="Payment processed" orderId="order-789"
```

### Log Verification Best Practices

| Practice | Description |
|---|---|
| Use unique identifiers | Filter by requestId/orderId to avoid historical data contamination |
| Time range filtering | Always specify a time range to avoid querying the entire dataset |
| Structured queries | Use field-based queries instead of full-text search |
| Save query results | Save query results as evidence |

## Metric Verification

### Basic PromQL Queries

```promql
# P99 latency
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))

# Error rate
sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))

# QPS (queries per second)
sum(rate(http_requests_total[5m]))

# Active connections
sum(http_connections_active)
```

### Performance Constraint Verification

**Verify P99 latency < 800ms**:

```promql
# Query P99 latency
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket{service="api-gateway"}[5m]))

# Threshold alert
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m])) > 0.8
```

**Verify error rate < 0.1%**:

```promql
# Calculate error rate
sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) < 0.001
```

**Verify throughput > 100 QPS**:

```promql
sum(rate(http_requests_total{service="api-gateway"}[5m])) > 100
```

### Metric Query Tools

| Tool | Purpose | Query Language |
|---|---|---|
| Prometheus | Time-series database | PromQL |
| Grafana | Visualization + query | PromQL/SQL |
| Datadog | Cloud monitoring | DQL |
| CloudWatch | AWS monitoring | CLI/Query |

### Metric Verification Best Practices

| Practice | Description |
|---|---|
| Baseline comparison | First obtain metric baselines before changes, then compare after changes |
| Sufficient time window | Observe at least 5-15 minutes to avoid transient fluctuations |
| Multi-dimension verification | Do not only look at P99; check P50/P95/P99 simultaneously |
| Label filtering | Use service name, environment, and other labels for precise filtering |

## Trace Verification

### Distributed Tracing Basics

```
Request chain:
[Gateway] → [Service A] → [Service B] → [Database]
   10ms       50ms          30ms          20ms

Total latency: 110ms
Bottleneck: Service A (50ms)
```

### Trace ID Verification

```
# Query full trace for a specific request
traceId="trace-abc-123"

# Query latency for specific service
service="order-service" duration > 100ms

# Query error traces
service="order-service" status="error"
```

### Tracing Tools

| Tool | Use Case |
|---|---|
| Jaeger | Open source, Kubernetes native |
| Zipkin | Open source, lightweight |
| AWS X-Ray | AWS environment |
| Datadog APM | Cloud, full-stack |

## Verification Flow Templates

### Performance Verification Flow

```markdown
1. **Get Baseline**
   - Record P99/P95/P50 latency before changes
   - Record error rate before changes
   - Record QPS before changes

2. **Apply Changes**
   - Deploy changes to test environment

3. **Collect Data**
   - Wait 5-15 minutes
   - Collect post-change metrics

4. **Comparative Analysis**
   - P99 latency delta: baseline → post-change
   - Error rate delta: baseline → post-change
   - QPS delta: baseline → post-change

5. **Produce Conclusion**
   - Whether performance constraints are met
   - Whether there is performance regression
   - Whether optimization is needed
```

### Reliability Verification Flow

```markdown
1. **Define Reliability Constraints**
   - Error rate < X%
   - Availability > Y%
   - Recovery time < Z seconds

2. **Inject Fault** (if needed)
   - Simulate service unavailability
   - Simulate network latency
   - Simulate resource exhaustion

3. **Verify Recovery**
   - System behavior during fault injection
   - System behavior after fault recovery
   - Whether recovery time constraints are met

4. **Produce Evidence**
   - Logs before/during/after fault injection
   - Metrics before/during/after fault injection
   - Measured recovery time
```

## Common Troubleshooting

| Issue | Possible Cause | Troubleshooting Method |
|---|---|---|
| Metric query returns no data | Label mismatch, time range error | Check label values, adjust time range |
| Log query returns too many results | Missing filter conditions | Add service/level/requestId filters |
| Trace data incomplete | Sampling rate too low | Adjust sampling rate, use head-based sampling |
| Latency metric anomaly | Network jitter, GC pauses | Check multiple time windows, compare across instances |
