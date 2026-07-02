# 端到端示例：微服务重构执行计划

## 场景背景

一个电商平台从单体架构迁移到微服务架构，需要将订单模块拆分为独立服务。任务复杂度高，预计需要 3-5 天，跨多个会话完成。

---

## 步骤 1：判断任务类型

**输入**：用户需求"把订单模块拆成独立微服务"

**判断**：
- 任务复杂度：高
- 预计完成时间：3-5 天
- 是否需要多轮接力：是
- 是否需要多人协作：是

**结论**：需要创建 exec-plan，不能用临时计划。

---

## 步骤 2：创建执行计划

**操作**：plan-architect agent 创建 `docs/exec-plans/active/order-service-extraction.md`

**输出**：

```markdown
---
id: order-service-extraction
title: 订单模块微服务拆分
status: active
owner: agent-1
created: 2026-07-02
---

# 订单模块微服务拆分

## 目标
将订单模块从单体中拆分为独立的 `order-service`，通过 REST API 与其他模块通信，保持现有功能不变。

## 范围
- 拆分订单创建、查询、状态管理功能
- 定义订单服务 API 接口
- 实现服务间通信（HTTP）
- 数据库独立迁移

## 非目标
- 不重构支付模块（后续单独处理）
- 不引入消息队列（保持简单 HTTP 通信）
- 不修改前端代码（通过 API 网关保持兼容）

## 步骤
- [ ] 1.1 分析现有订单模块依赖关系
- [ ] 1.2 定义订单服务 API 规范（OpenAPI）
- [ ] 2.1 创建 order-service 项目骨架
- [ ] 2.2 实现订单 CRUD 接口
- [ ] 2.3 实现订单状态机
- [ ] 3.1 数据库迁移脚本
- [ ] 3.2 验证数据一致性
- [ ] 4.1 更新网关路由配置
- [ ] 4.2 集成测试

## 验收标准
- [ ] order-service 独立启动，监听 3001 端口
- [ ] 所有订单 API 返回与单体版本一致
- [ ] 数据库表结构与单体版本兼容
- [ ] 端到端测试通过率 ≥ 95%
- [ ] 性能指标：P99 延迟 < 200ms

## 决策日志
| 日期 | 决策 | 理由 |
|------|------|------|
| 2026-07-02 | 选择 REST 而非 gRPC | 团队更熟悉 REST，无需额外学习成本 |
| 2026-07-02 | 数据库独立而非共享 | 避免服务间数据库耦合，便于独立部署 |

## 风险
- 数据迁移可能导致短暂数据不一致
- 服务间网络延迟可能影响性能

## 待澄清问题
- 订单与用户服务的边界如何划分？（用户信息查询走哪个服务？）
```

---

## 步骤 3：执行计划

**操作**：verification-loop-runner agent 按步骤执行

### 步骤 1.1：分析现有订单模块依赖关系

```bash
# 查找订单相关文件
find src -name "*order*" -o -name "*Order*" | head -20

# 检查依赖
rg "require.*order|from.*order" src/ --no-filename
```

**输出**：记录到 exec-plan 的决策日志

### 步骤 1.2：定义 API 规范

创建 `docs/api/order-service.yaml`：

```yaml
openapi: 3.0.0
info:
  title: Order Service API
  version: 1.0.0
paths:
  /orders:
    post:
      summary: 创建订单
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateOrderRequest'
      responses:
        '201':
          description: 订单创建成功
components:
  schemas:
    CreateOrderRequest:
      type: object
      properties:
        userId:
          type: string
        items:
          type: array
          items:
            $ref: '#/components/schemas/OrderItem'
```

### 步骤 2.1：创建项目骨架

```bash
mkdir -p order-service/src/{routes,services,repositories,types}
cd order-service
npm init -y
npm install express typescript @types/express
```

### 步骤 2.2-2.3：实现接口和状态机

```typescript
// src/services/OrderService.ts
export class OrderService {
  async createOrder(userId: string, items: OrderItem[]): Promise<Order> {
    const order = {
      id: generateId(),
      userId,
      items,
      status: 'pending',
      createdAt: new Date(),
    };
    await this.orderRepository.save(order);
    return order;
  }

  async updateStatus(orderId: string, status: OrderStatus): Promise<Order> {
    const order = await this.orderRepository.findById(orderId);
    if (!order) throw new NotFoundError('Order not found');
    
    // 状态机验证
    if (!this.isValidTransition(order.status, status)) {
      throw new InvalidTransitionError(order.status, status);
    }
    
    order.status = status;
    await this.orderRepository.save(order);
    return order;
  }
}
```

### 步骤 3.1：数据库迁移

```sql
-- migrations/001_create_orders_table.sql
CREATE TABLE orders (
  id VARCHAR(36) PRIMARY KEY,
  user_id VARCHAR(36) NOT NULL,
  status VARCHAR(20) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE order_items (
  id VARCHAR(36) PRIMARY KEY,
  order_id VARCHAR(36) NOT NULL,
  product_id VARCHAR(36) NOT NULL,
  quantity INT NOT NULL,
  price DECIMAL(10, 2) NOT NULL,
  FOREIGN KEY (order_id) REFERENCES orders(id)
);
```

---

## 步骤 4：更新执行计划状态

**操作**：每完成一步，勾选 `- [x]`

```markdown
## 步骤
- [x] 1.1 分析现有订单模块依赖关系
- [x] 1.2 定义订单服务 API 规范（OpenAPI）
- [x] 2.1 创建 order-service 项目骨架
- [x] 2.2 实现订单 CRUD 接口
- [x] 2.3 实现订单状态机
- [ ] 3.1 数据库迁移脚本
- [ ] 3.2 验证数据一致性
- [ ] 4.1 更新网关路由配置
- [ ] 4.2 集成测试
```

---

## 步骤 5：验收关闭

**操作**：逐项核对验收标准

```bash
# 验收 1：order-service 独立启动
cd order-service && npm start
curl http://localhost:3001/health
# 期望：{"status":"ok"}

# 验收 2：API 返回一致
curl -X POST http://localhost:3001/orders \
  -H "Content-Type: application/json" \
  -d '{"userId":"u123","items":[{"productId":"p456","quantity":2}]}'
# 期望：201 Created

# 验收 3：数据库表结构
psql -d order_db -c "\dt orders"
# 期望：表存在

# 验收 4：端到端测试
npm run test:e2e
# 期望：通过率 ≥ 95%

# 验收 5：性能测试
npm run test:performance
# 期望：P99 < 200ms
```

**输出**：

```markdown
## 验收结果
- [x] order-service 独立启动，监听 3001 端口
- [x] 所有订单 API 返回与单体版本一致
- [x] 数据库表结构与单体版本兼容
- [x] 端到端测试通过率 98%
- [x] 性能指标：P99 延迟 150ms
```

---

## 步骤 6：归档计划

**操作**：移动文件到 `completed/`

```bash
mv docs/exec-plans/active/order-service-extraction.md \
   docs/exec-plans/completed/
```

---

## 错误处理

### 场景 1：步骤 2.2 实现失败
**处理**：
1. 在 exec-plan 中标注该步骤为 `blocked`
2. 记录失败原因："依赖的 `generateId` 函数未实现"
3. 添加到 `tech-debt-tracker.md`
4. 后续 agent 可以从这里接手

### 场景 2：验收标准不通过
**处理**：
1. 记录具体失败信息
2. 回溯到对应步骤重新执行
3. 更新决策日志："发现 XXX 问题，需要调整方案"

### 场景 3：任务被中断
**处理**：
1. 提交当前进度到文件
2. 下一个 agent 读取 exec-plan 继续执行
3. active/ 目录作为协调台账

---

## 验收标准

- [ ] exec-plan 文件存在于 `docs/exec-plans/active/` 或 `completed/`
- [ ] 每个步骤可独立验证
- [ ] 验收标准可机械检查（非"看起来不错"）
- [ ] 决策日志记录了关键选择
- [ ] 风险已识别并有应对措施
