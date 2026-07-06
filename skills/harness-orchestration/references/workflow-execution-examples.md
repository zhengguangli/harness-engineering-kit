# Workflow Execution Examples

## Workflow 1: Greenfield Initialization Example

**Scenario**: A newly created Node.js/React frontend project that needs harness structure initialization

```
User says: "Help me initialize the harness for this project"

1. project-intake → analyze package.json → identify React+TypeScript+Vite
2. bootstrap → generate CLAUDE.md (routing table) + docs/ (ARCHITECTURE.md, QUALITY_SCORE.md)
3. repo-map → verify: CLAUDE.md ≤ 100 lines? Links valid?
4. architecture-boundaries → define 3-layer model: Types → Components → Pages
   golden-principles → register ESLint rules and code style standards
```

**Trimming Decision**: Project scale is "small", skip exec-plans/completed directory, keep only active/.

---

## Workflow 2: Daily Feature Development Example

**Scenario**: An existing harness project needs to add a "user login" feature

```
User says: "Implement user login functionality, backend API + frontend page"

1. exec-plans → create auth-implementation.md
   - Goal: User can log in with email and password
   - Steps: [POST /api/auth/login] [Login form component] [Error handling]
2. Implementation → agent writes API routes + React components
3. verification-loop → implement→self-check→test→fix loop
4. commit-gate → diff review → test → commit message formatting
```

---

## Workflow 3: Code Quality Repair Example

**Scenario**: Existing code has widespread `any` type abuse

```
User says: "There are too many 'any' types in the code, clean them up"

1. golden-principles → register "no any" principle → scan all .ts files
2. architecture-boundaries (optional) → if any appears at data boundaries, add Parse rules
3. verification-loop → fix file by file → type check passes
4. commit-gate → atomic commits
```

---

## Workflow 4: Extending the Harness System Example

**Scenario**: The team decides to add a new database migration skill

```
User says: "I want to add a database migration management skill"

1. authoring → create skills/harness-db-migration/
   - Decision: skill (methodology needs main conversation reference)
   - description: clearly state "when to use" + "what it does"
   - Template: generate per scaffold-templates.md
2. bootstrap (optional) → if new docs/ structure is involved
3. repo-map → add routing entry in CLAUDE.md
```

---

## Workflow 5: Prompt Optimization Example

**Scenario**: A skill's Agent prompt is underperforming

```
User says: "Optimize the Agent prompt for verification-loop"

1. prompt-optimizer → read verification-loop SKILL.md
   - Analyze existing prompt → five-dimension evaluation (role clarity, execution chain completeness, etc.)
   - Refactor → six-block template reorganization
   - Output → optimized ## Agent Prompt section
```

---

## Cross-Flow Combination Example

**Scenario**: A new project needs harness initialization, and existing code style needs cleanup

```
User says: "New project, first initialize harness, then standardize the existing code style"

Cross-flow: Workflow 1 + Workflow 3

Execution order:
1. project-intake (analyze existing code)
2. bootstrap (initialize skeleton)
3. repo-map (verify)
4. golden-principles (register style rules + scan)
5. commit-gate (commit)
```
