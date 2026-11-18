# Workflow Execution Examples

## Workflow 1: Greenfield Initialization Example

```
User says: "Help me initialize the harness for this project"

1. bootstrap → reconnaissance + 5-dimension Project Card → generate AGENTS.md + docs/ + .gitignore
2. repo-map → verify: AGENTS.md ≤ 100 lines? Links valid?
3. architecture-boundaries → define 3-layer model: Types → Components → Pages
   golden-principles → register ESLint rules and code style standards
```

## Workflow 2: Daily Feature Development Example

```
User says: "Implement user login functionality, backend API + frontend page"

1. exec-plans → create auth-implementation.md (Goal, Non-goals, mechanical Acceptance Criteria)
2. Implementation → write API routes + React components
3. verification-loop → implement→self-check→test→review→fix (invokes observability-and-browser for UI)
4. commit-gate → diff review → test → commit message formatting
```

## Workflow 3: Code Quality Repair Example

```
User says: "There are too many 'any' types in the code, clean them up"

1. golden-principles → register "no any" principle → scan all .ts files
2. architecture-boundaries (optional) → if `any` crosses data boundaries, add Parse rule
3. verification-loop → fix file by file → type check passes
4. commit-gate → atomic commits
```

## Cross-Flow Combination Example

```
User says: "New project, first initialize harness, then standardize the existing code style"

1. bootstrap (reconnaissance + skeleton)
2. repo-map (verify)
3. golden-principles (register style rules + scan)
4. commit-gate (commit)
```
