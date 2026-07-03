# End-to-End Example: Microservice Refactoring Execution Plan

## Scenario Background

An e-commerce platform migrating from a monolith to microservices needs to extract the order module into an independent service. High task complexity, estimated 3-5 days, spanning multiple sessions.

---

## Step 1: Determine Task Type

**Input**: User requirement "Extract the order module into an independent microservice"

**Assessment**:
- Task complexity: High
- Estimated completion: 3-5 days
- Multi-round handoffs needed: Yes
- Multi-person collaboration needed: Yes

**Conclusion**: Need to create an exec-plan, cannot use a light plan.

---

## Step 2: Create Execution Plan

**Action**: plan-architect agent creates `docs/exec-plans/active/order-service-extraction.md`

**Output**:

```markdown
---
id: order-service-extraction
title: Order Module Microservice Extraction
status: active
owner: agent-1
created: 2026-07-02
---

# Order Module Microservice Extraction

## Goal
Extract the order module from the monolith into an independent `order-service`, communicating with other modules via REST API, while maintaining existing functionality.

## Scope
- Extract order creation, query, and status management functionality
- Define order service API interfaces
- Implement inter-service communication (HTTP)
- Independent database migration

## Non-Goals
- Do not refactor the payment module (will be handled separately)
- Do not introduce message queues (keep simple HTTP communication)
- Do not modify frontend code (maintain compatibility through API gateway)

## Steps
- [ ] 1.1 Analyze existing order module dependencies
- [ ] 1.2 Define order service API specification (OpenAPI)
- [ ] 2.1 Create order-service project skeleton
- [ ] 2.2 Implement order CRUD interfaces
- [ ] 2.3 Implement order state machine
- [ ] 3.1 Database migration script
- [ ] 3.2 Verify data consistency
- [ ] 4.1 Update gateway routing configuration
- [ ] 4.2 Integration tests

## Acceptance Criteria
- [ ] order-service starts independently, listening on port 3001
- [ ] All order APIs return results consistent with the monolith version
- [ ] Database table structure compatible with the monolith version
- [ ] End-to-end test pass rate >= 95%
- [ ] Performance: P99 latency < 200ms

## Decision Log
| Date | Decision | Rationale |
|------|----------|----------|
| 2026-07-02 | Choose REST over gRPC | Team is more familiar with REST, no additional learning cost |
| 2026-07-02 | Independent database instead of shared | Avoid inter-service database coupling, facilitate independent deployment |

## Risks
- Data migration may cause brief data inconsistency
- Inter-service network latency may impact performance

## Questions to Clarify
- How to define the boundary between order and user services? (Which service handles user info queries?)
```

---

## Step 3: Execute Plan

**Action**: verification-loop-runner agent executes step by step

### Step 1.1: Analyze Existing Order Module Dependencies

```bash
# Find order-related files
find src -name "*order*" -o -name "*Order*" | head -20

# Check dependencies
rg "require.*order|from.*order" src/ --no-filename
```

**Output**: Record in the exec-plan decision log

### Step 1.2: Define API Specification

Create `docs/api/order-service.yaml`:

```yaml
openapi: 3.0.0
info:
  title: Order Service API
  version: 1.0.0
paths:
  /orders:
    post:
      summary: Create Order
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateOrderRequest'
      responses:
        '201':
          description: Order created successfully
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

### Step 2.1: Create Project Skeleton

```bash
mkdir -p order-service/src/{routes,services,repositories,types}
cd order-service
npm init -y
npm install express typescript @types/express
```

### Step 2.2-2.3: Implement API and State Machine

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
    
    // State machine validation
    if (!this.isValidTransition(order.status, status)) {
      throw new InvalidTransitionError(order.status, status);
    }
    
    order.status = status;
    await this.orderRepository.save(order);
    return order;
  }
}
```

### Step 3.1: Database Migration

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

## Step 4: Update Execution Plan Status

**Action**: Check off each step with `- [x]`

```markdown
## Steps
- [x] 1.1 Analyze existing order module dependencies
- [x] 1.2 Define order service API specification (OpenAPI)
- [x] 2.1 Create order-service project skeleton
- [x] 2.2 Implement order CRUD interfaces
- [x] 2.3 Implement order state machine
- [ ] 3.1 Database migration script
- [ ] 3.2 Verify data consistency
- [ ] 4.1 Update gateway routing configuration
- [ ] 4.2 Integration tests
```

---

## Step 5: Acceptance Close

**Action**: Check acceptance criteria item by item

```bash
# Acceptance 1: order-service starts independently
cd order-service && npm start
curl http://localhost:3001/health
# Expected: {"status":"ok"}

# Acceptance 2: API returns consistent results
curl -X POST http://localhost:3001/orders \
  -H "Content-Type: application/json" \
  -d '{"userId":"u123","items":[{"productId":"p456","quantity":2}]}'
# Expected: 201 Created

# Acceptance 3: Database table structure
psql -d order_db -c "\dt orders"
# Expected: Table exists

# Acceptance 4: End-to-end tests
npm run test:e2e
# Expected: Pass rate >= 95%

# Acceptance 5: Performance tests
npm run test:performance
# Expected: P99 < 200ms
```

**Output**:

```markdown
## Acceptance Results
- [x] order-service starts independently, listening on port 3001
- [x] All order APIs return results consistent with the monolith version
- [x] Database table structure compatible with the monolith version
- [x] End-to-end test pass rate: 98%
- [x] Performance: P99 latency 150ms
```

---

## Step 6: Archive Plan

**Action**: Move file to `completed/`

```bash
mv docs/exec-plans/active/order-service-extraction.md \
   docs/exec-plans/completed/
```

---

## Error Handling

### Scenario 1: Step 2.2 Implementation Failed

**Handling**:
1. Mark the step as `blocked` in the exec-plan
2. Record the failure reason: "The `generateId` function it depends on is not implemented"
3. Add to `tech-debt-tracker.md`
4. Subsequent agents can pick up from here

### Scenario 2: Acceptance Criteria Not Met

**Handling**:
1. Record specific failure details
2. Roll back to the corresponding step and re-execute
3. Update decision log: "Found issue XXX, need to adjust approach"

### Scenario 3: Task Interrupted

**Handling**:
1. Commit current progress to file
2. Next agent reads the exec-plan and continues execution
3. The `active/` directory serves as the coordination ledger

---

## Acceptance Criteria

- [ ] exec-plan file exists in `docs/exec-plans/active/` or `completed/`
- [ ] Each step can be independently verified
- [ ] Acceptance criteria are mechanically checkable (not "looks good")
- [ ] Decision log records key choices
- [ ] Risks identified with mitigation measures
