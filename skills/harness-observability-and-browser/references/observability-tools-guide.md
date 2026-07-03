# 可观测性工具使用指南

## 三大支柱

可观测性由三个核心支柱组成：

| 支柱 | 数据类型 | 查询方式 | 适用场景 |
|---|---|---|---|
| 日志（Logs） | 离散事件 | 全文搜索/结构化查询 | 调试具体错误、审计 |
| 指标（Metrics） | 聚合数值 | PromQL/查询语言 | 性能监控、告警 |
| 追踪（Traces） | 请求链路 | Trace ID 查询 | 跨服务延迟分析 |

## 日志验证

### 结构化日志标准

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

**必备字段**：
- `timestamp`：ISO 8601 格式
- `level`：info/warn/error
- `message`：人类可读描述
- `service`：服务名称
- `requestId`：请求追踪 ID

### 日志查询验证模式

**验证异常是否被捕获**：

```
# 查询特定时间段内的错误日志
service="order-service" level="error" timestamp >= "2026-07-02T10:00:00Z"

# 验证特定错误是否出现
service="order-service" level="error" message="*timeout*"

# 验证错误率
count(service="order-service" level="error") / count(service="order-service")
```

**验证业务事件**：

```
# 验证订单创建成功
service="order-service" message="Order created" orderId="order-789"

# 验证支付完成
service="payment-service" message="Payment processed" orderId="order-789"
```

### 日志验证最佳实践

| 实践 | 说明 |
|---|---|
| 使用唯一标识 | 用 requestId/orderId 过滤，避免历史数据污染 |
| 时间范围过滤 | 始终指定时间范围，避免查询全量数据 |
| 结构化查询 | 使用字段查询而非全文搜索 |
| 保存查询结果 | 将查询结果保存为证据 |

## 指标验证

### PromQL 基础查询

```promql
# P99 延迟
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))

# 错误率
sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))

# QPS（每秒请求数）
sum(rate(http_requests_total[5m]))

# 活跃连接数
sum(http_connections_active)
```

### 性能约束验证

**验证 P99 延迟 < 800ms**：

```promql
# 查询 P99 延迟
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket{service="api-gateway"}[5m]))

# 阈值告警
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m])) > 0.8
```

**验证错误率 < 0.1%**：

```promql
# 计算错误率
sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) < 0.001
```

**验证吞吐量 > 100 QPS**：

```promql
sum(rate(http_requests_total{service="api-gateway"}[5m])) > 100
```

### 指标查询工具

| 工具 | 用途 | 查询语言 |
|---|---|---|
| Prometheus | 时序数据库 | PromQL |
| Grafana | 可视化+查询 | PromQL/SQL |
| Datadog | 公有云监控 | DQL |
| CloudWatch | AWS 监控 | CLI/Query |

### 指标验证最佳实践

| 实践 | 说明 |
|---|---|
| 基线对比 | 先获取改动前的指标基线，再对比改动后 |
| 足够时间窗口 | 至少观察 5-15 分钟，避免瞬时波动 |
| 多维度验证 | 不只看 P99，同时看 P50/P95/P99 |
| 标签过滤 | 使用服务名、环境等标签精确过滤 |

## 追踪验证

### 分布式追踪基础

```
请求链路：
[Gateway] → [Service A] → [Service B] → [Database]
   10ms       50ms          30ms          20ms

总延迟：110ms
瓶颈：Service A（50ms）
```

### Trace ID 验证

```
# 查询特定请求的完整链路
traceId="trace-abc-123"

# 查询特定服务的延迟
service="order-service" duration > 100ms

# 查询错误链路
service="order-service" status="error"
```

### 追踪工具

| 工具 | 适用场景 |
|---|---|
| Jaeger | 开源，Kubernetes 原生 |
| Zipkin | 开源，轻量级 |
| AWS X-Ray | AWS 环境 |
| Datadog APM | 公有云，全栈 |

## 验证流程模板

### 性能验证流程

```markdown
1. **获取基线**
   - 记录改动前的 P99/P95/P50 延迟
   - 记录改动前的错误率
   - 记录改动前的 QPS

2. **执行改动**
   - 部署改动到测试环境

3. **收集数据**
   - 等待 5-15 分钟
   - 收集改动后的指标

4. **对比分析**
   - P99 延迟变化：基线 → 改动后
   - 错误率变化：基线 → 改动后
   - QPS 变化：基线 → 改动后

5. **产出结论**
   - 是否满足性能约束
   - 是否有性能退化
   - 是否需要优化
```

### 可靠性验证流程

```markdown
1. **定义可靠性约束**
   - 错误率 < X%
   - 可用性 > Y%
   - 恢复时间 < Z 秒

2. **注入故障**（如需要）
   - 模拟服务不可用
   - 模拟网络延迟
   - 模拟资源耗尽

3. **验证恢复**
   - 故障注入后系统行为
   - 故障恢复后系统行为
   - 是否满足恢复时间约束

4. **产出证据**
   - 故障注入前/中/后的日志
   - 故障注入前/中/后的指标
   - 恢复时间实测值
```

## 常见问题排查

| 问题 | 可能原因 | 排查方法 |
|---|---|---|
| 指标查询无数据 | 标签不匹配、时间范围错误 | 检查标签值、调整时间范围 |
| 日志查询结果过多 | 缺少过滤条件 | 添加 service/level/requestId 过滤 |
| 追踪数据不完整 | 采样率过低 | 调整采样率、使用 head-based sampling |
| 延迟指标异常 | 网络抖动、GC 停顿 | 检查多个时间窗口、对比不同实例 |
