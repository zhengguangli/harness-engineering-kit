# End-to-End Example: Node.js E-Commerce Platform Architecture Boundary Audit

## Scenario Background

A medium-sized Node.js e-commerce platform, approximately 50,000 lines of code, with an 8-person team. Recently the following issues have emerged:
- `OrderService` directly `require`s `UserRepository` (cross-layer boundary violation)
- Authentication logic scattered across 3 different Services (cross-cutting concerns not unified)
- A circular dependency causing intermittent startup crashes

Goal: Establish layered architecture rules and prevent recurrence through mechanical checks.

---

## Step 1: Analyze Project Current State

**Input**: Project code directory

**Actions**:

```bash
# List top-level directory structure
ls src/

# Identify main modules
find src -maxdepth 2 -type d | head -30
```

**Output**:
```
src/
├── types/          # TypeScript type definitions
├── config/         # Configuration management
├── repositories/   # Data access layer
├── services/       # Business logic layer
├── controllers/    # Controller layer
├── routes/         # Routing layer
├── middleware/     # Middleware (authentication, logging, etc.)
└── utils/          # Utility functions
```

**Findings**:
- The project has a clear 6-layer structure
- `middleware/` directory exists but is not uniformly referenced
- Business logic is mixed into `utils/`

---

## Step 2: Identify Dependency Direction

**Input**: Project directory structure

**Actions**:

```bash
# Check current dependency direction (search import/require statements)
rg "require\(|from ['\"]" src/ --no-filename | sort | uniq -c | sort -rn | head -20

# Check cross-layer dependencies
rg "require.*repositories" src/services/  # Whether Service directly references Repository
rg "require.*services" src/routes/        # Whether Route directly references Service
```

**Output**:
```
# Violations found:
src/services/OrderService.ts:1  const userRepo = require('../repositories/UserRepository')
src/services/PaymentService.ts:1  const { verifyToken } = require('../middleware/auth')
src/controllers/UserController.ts:1  const { db } = require('../repositories')
```

**Identified Dependency Direction**:
```
types → config → repositories → services → controllers → routes
```

**Cross-Cutting Concerns**: `middleware/` (authentication, logging, error handling)

---

## Step 3: Define Architecture Rules

**Input**: Analysis results from Steps 1-2

**Actions**: Confirm the following rules with the user

```markdown
## Dependency Direction Rules

### Forward Dependencies (must be unidirectional)
types → config → repositories → services → controllers → routes

### Cross-Cutting Concern Entry Point
middleware/ can only be referenced by routes/, not directly by services/ or controllers/.

### Prohibited Dependencies
- services/ must not directly import repositories/ implementations (must go through interfaces)
- controllers/ must not directly import repositories/ (must go through services/)
- No layer may reverse-depend on an upper layer
```

**Output**: Write to `docs/ARCHITECTURE.md`

---

## Step 4: Generate Check Rules

**Input**: Architecture rules from Step 3

**Actions**: boundary-auditor agent executes checks inline

```bash
# Check 1: Service layer directly referencing Repository
rg "require.*repositories|from.*repositories" src/services/

# Check 2: Controller layer directly referencing Repository
rg "require.*repositories|from.*repositories" src/controllers/

# Check 3: Cross-cutting concerns scattered
rg "require.*middleware|from.*middleware" src/services/ src/controllers/

# Check 4: Circular dependency detection
# Use madge or manually inspect import chains
npx madge --circular src/
```

---

## Step 5: Execute Audit and Generate Report

**Input**: Check results from Step 4

**Output**:

```markdown
## Architecture Boundary Audit Report

### Summary
- Total violations: 5
- CRITICAL: 1
- HIGH: 3
- MEDIUM: 1
- LOW: 0
- Recommendation: Block merge (CRITICAL-level circular dependency exists)

### Detailed Findings

### [CRITICAL] Circular dependency causing startup crash
- File: `src/services/OrderService.ts`, line: L1-L5
- Rule violated: Dependency direction must be unidirectional, no cycles allowed
- Impact: Causes module loading order uncertainty, intermittent startup crashes
- Suggested Fix:
  1. Extract `OrderService`'s dependency on `UserService` into an interface
  2. Use dependency injection instead of direct require
  ```typescript
  // Before
  const UserService = require('./UserService');

  // After
  interface UserServiceInterface {
    getUser(id: string): User;
  }
  constructor(private userService: UserServiceInterface) {}
  ```

### [HIGH] Service layer directly referencing Repository implementation
- File: `src/services/OrderService.ts`, line: L1
- Rule violated: services/ must not directly import repositories/ implementations
- Impact: Violates layered architecture, Service coupled with data access layer
- Suggested Fix:
  1. Define `UserRepositoryInterface` in `src/types/`
  2. Pass Repository instance through dependency injection
  ```typescript
  // Before
  const userRepo = require('../repositories/UserRepository');

  // After (inject in constructor)
  constructor(private userRepo: UserRepositoryInterface) {}
  ```

### [HIGH] Cross-cutting concern leaking into Service layer
- File: `src/services/PaymentService.ts`, line: L1
- Rule violated: middleware/ can only be referenced by routes/
- Impact: Authentication logic coupled with business logic, cannot be managed uniformly
- Suggested Fix:
  1. Remove the `verifyToken` call from `PaymentService`
  2. Move authentication check to the middleware chain in `routes/payment.ts`
  ```typescript
  // routes/payment.ts
  router.post('/pay', authMiddleware, PaymentController.pay);
  ```

### [HIGH] Controller layer directly referencing Repository
- File: `src/controllers/UserController.ts`, line: L1
- Rule violated: controllers/ must not directly import repositories/
- Impact: Bypasses business logic layer, directly operates on data
- Suggested Fix:
  1. Move data operation logic into `UserService`
  2. Controller only calls Service methods
  ```typescript
  // Before
  const { db } = require('../repositories');

  // After
  const user = await this.userService.getUser(id);
  ```

### [MEDIUM] Business logic mixed into utils/
- File: `src/utils/validation.ts`, line: L10-L25
- Rule violated: utils/ should only contain generic utility functions
- Impact: Utility functions coupled with business logic, hard to reuse
- Suggested Fix:
  1. Move `validateOrder` into `src/services/OrderService`
  2. utils/ should only keep pure utility functions (e.g., date formatting, string processing)
```

---

## Step 6: Integrate into Verification Loop

**Input**: Audit report from Step 5

**Actions**: Integrate checks into `harness-verification-loop`

```yaml
# Add to verification-loop configuration
verification_steps:
  - name: architecture-boundaries-check
    command: |
      # Executed inline by boundary-auditor agent
      # Check dependency direction, circular dependencies, cross-cutting concerns
    blocking: true  # CRITICAL/HIGH violations block merge
```

---

## Step 7: Regular Audits

**Frequency**: Monthly / After major refactoring

**Actions**:
```bash
# Run boundary check
# boundary-auditor agent executes Step 4 checks
# Compare with previous audit results to identify new violations
```

---

## Error Handling

### Scenario 1: ARCHITECTURE.md does not exist
**Handling**: boundary-auditor reports "Architecture rules are not documented," recommends using the `harness-architecture-boundaries` skill first, then makes reasonable inferences based on the current codebase state.

### Scenario 2: Rule definition too vague to judge
**Handling**: boundary-auditor reports "Rule needs to be encoded more precisely" as a finding item, without loosening the rule on its own.

### Scenario 3: Fix suggestion is not actionable
**Handling**: boundary-auditor supplements with concrete fix directions, including code examples and operational steps.

---

## Acceptance Criteria

- [ ] `docs/ARCHITECTURE.md` contains the complete layering model and dependency direction rules
- [ ] boundary-auditor can identify all CRITICAL/HIGH violations
- [ ] Each violation comes with an actionable fix suggestion
- [ ] Circular dependencies eliminated (`npx madge --circular src/` produces no output)
- [ ] Cross-cutting concerns uniformly routed through the middleware/ entry point
