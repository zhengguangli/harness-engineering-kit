# End-to-end example: React project knowledge base refactoring

## Scenario background

A React + TypeScript project with CLAUDE.md bloated to 350 lines, containing architecture descriptions, API docs, deployment workflows, troubleshooting, and everything else. The agent frequently can't find information or reads stale content.

Goal: Refactor the encyclopedia-style CLAUDE.md into a "map + structured docs/" progressive disclosure model.

---

## Step 1: Inventory current state

**Input**: Project root directory

**Operations**:

```bash
# Check CLAUDE.md line count
wc -l CLAUDE.md

# Check docs/ directory
ls -la docs/ 2>/dev/null || echo "docs/ does not exist"

# Check existing document structure
find . -name "*.md" -not -path "./node_modules/*" | head -20
```

**Output**:
```
350 CLAUDE.md
docs/ does not exist
./README.md
./CLAUDE.md
./CHANGELOG.md
```

**Current state analysis**:
- CLAUDE.md: 350 lines (severely over limit; should be <= 100 lines)
- docs/: does not exist
- Content mixed: architecture, API, deployment, troubleshooting all in one file

---

## Step 2: Design directory skeleton

**Input**: Project tech stack (React + TypeScript) and current state analysis

**Operations**: Trim the target skeleton as needed

```
CLAUDE.md                  # Slimmed down to ~80 line map
docs/
├── ARCHITECTURE.md        # Architecture description
├── QUALITY_SCORE.md       # Quality score
├── design-docs/
│   ├── index.md           # Design document index
│   └── core-beliefs.md    # Core beliefs
├── exec-plans/
│   ├── active/
│   ├── completed/
│   └── tech-debt-tracker.md
├── generated/
├── product-specs/
│   └── index.md
└── references/
```

---

## Step 3: Split and relocate

**Input**: Existing CLAUDE.md (350 lines)

**Operations**: Split by topic into docs/

### 3.1 Create ARCHITECTURE.md

Extract architecture-related content from CLAUDE.md:

```markdown
---
title: React Project Architecture
last_verified: 2026-07-02
related_code: src/
---

# Architecture Description

## Tech Stack
- React 18 + TypeScript
- Zustand for state management
- React Query for data fetching
- Tailwind CSS for styling

## Directory Structure
src/
├── components/     # Reusable UI components
├── pages/          # Page components
├── hooks/          # Custom hooks
├── services/       # API service layer
├── stores/         # Zustand stores
└── types/          # TypeScript types

## Dependency Direction
types -> services -> hooks -> components -> pages
stores -> hooks -> components -> pages

## State Management
- Global state: Zustand stores (user auth, theme settings)
- Server state: React Query (API data caching)
- Local state: useState/useReducer (component internal state)
```

### 3.2 Create design-docs/core-beliefs.md

```markdown
---
title: Core Beliefs
last_verified: 2026-07-02
---

# Core Beliefs

## Agent-First Design
- All documentation must be mechanically discoverable and verifiable by agents
- Avoid relying on human memory or verbal consensus
- Progressive disclosure: start with a small entry point, teach the agent where to find more

## Code as Documentation
- Code structure itself is the best documentation
- Type definitions are the interface contract
- Tests are usage examples

## Continuous Verification
- Documentation must stay consistent with code behavior
- Outdated documentation is more dangerous than no documentation
- Regular audits ensure documentation freshness
```

### 3.3 Create design-docs/index.md

```markdown
---
title: Design Document Index
last_verified: 2026-07-02
---

# Design Document Index

| Document | Purpose | Last Verified |
|----------|---------|---------------|
| [core-beliefs.md](./core-beliefs.md) | Core operating beliefs | 2026-07-02 |

## New Documents
When designing new features, first create an ADR (Architecture Decision Record) in `docs/design-docs/`.
```

### 3.4 Create product-specs/index.md

```markdown
---
title: Product Spec Index
last_verified: 2026-07-02
---

# Product Spec Index

| Spec | Status | Last Updated |
|------|--------|--------------|
| User Authentication Flow | Shipped | 2026-06-15 |
| Order Management Feature | In Development | 2026-07-01 |
```

### 3.5 Create tech-debt-tracker.md

```markdown
---
title: Tech Debt Tracker
last_verified: 2026-07-02
---

# Tech Debt Tracker

## Pending
| Item | Affected Area | Created | Reason |
|------|---------------|---------|--------|
| Migrate to React Query v5 | services/ | 2026-06-20 | Old version does not support Suspense |

## Completed
| Item | Completed | Solution |
|------|-----------|----------|
| - | - | - |
```

---

## Step 4: Rewrite CLAUDE.md as a map

**Input**: Original CLAUDE.md (350 lines) + docs/ from step 3

**Operations**: Condense into an ~80-line navigation map

```markdown
# Project Map

> This file is a map, not an encyclopedia; in-depth information can be found in docs/

## Quick Navigation

| I want to know... | Go here |
|---|---|
| Project architecture and layering rules | `docs/ARCHITECTURE.md` |
| Design decisions and core beliefs | `docs/design-docs/` |
| Product feature specs | `docs/product-specs/index.md` |
| Execution plans and tech debt | `docs/exec-plans/` |
| Quality scores | `docs/QUALITY_SCORE.md` |

## Directory Structure

```
docs/
├── ARCHITECTURE.md        # Architecture description
├── QUALITY_SCORE.md       # Quality score
├── design-docs/           # Design documents
├── exec-plans/            # Execution plans
├── generated/             # Auto-generated
├── product-specs/         # Product specs
└── references/            # Third-party references
```

## How It Works

1. First look at this file to understand information distribution
2. Dive into docs/ subdirectories as needed
3. When uncertain, ask the user or check docs/
```

---

## Step 5: Quality verification

**Input**: Refactored docs/ structure

**Operations**: doc-gardener agent runs inline checks

### 5.1 Broken link detection

```bash
# Scan internal links in docs/
rg '\]\(\./' docs/ --no-filename | while read -r link; do
  # Extract link target and verify
  target=$(echo "$link" | sed 's/.*](\(.*\)).*/\1/')
  if [ ! -f "docs/$target" ]; then
    echo "Broken link: $link -> $target"
  fi
done
```

### 5.2 Freshness detection

```bash
# Check document last updated dates
rg "last_verified:" docs/ --no-filename | while read -r line; do
  date=$(echo "$line" | sed 's/.*: //')
  # Calculate day difference
  days=$(( ($(date +%s) - $(date -j -f "%Y-%m-%d" "$date" +%s)) / 86400 ))
  if [ "$days" -gt 30 ]; then
    echo "Outdated document: $line ($days days old)"
  fi
done
```

### 5.3 Coverage detection

```bash
# Check if ARCHITECTURE.md covers all directories
for dir in src/*/; do
  dirname=$(basename "$dir")
  if ! grep -q "$dirname" docs/ARCHITECTURE.md; then
    echo "Uncovered directory: $dirname"
  fi
done
```

---

## Step 6: Generate report

**Output**:

```markdown
## Document Health Report

### Summary
- Total issues: 3
- HIGH: 1 (broken link)
- MEDIUM: 1 (insufficient coverage)
- LOW: 1 (suggested improvement)

### Detailed Findings

### [HIGH] CLAUDE.md navigation table broken link
- File: `CLAUDE.md`, Line: L15
- Issue: Navigation table points to `docs/QUALITY_SCORE.md`, but the file does not exist
- Impact: Agent cannot find quality score information
- Fix: Create `docs/QUALITY_SCORE.md` or update the navigation table

### [MEDIUM] ARCHITECTURE.md does not cover hooks/ directory
- File: `docs/ARCHITECTURE.md`
- Issue: `src/hooks/` directory exists but is not described in the architecture documentation
- Impact: Agent does not understand the hooks layer's responsibilities
- Fix: Add hooks/ description to ARCHITECTURE.md

### [LOW] design-docs/ has few documents
- File: `docs/design-docs/`
- Issue: Only 2 documents, suggest adding more design decision records
- Impact: Incomplete team decision history
- Fix: Create ADR documents when developing new features
```

---

## Error handling

### Scenario 1: docs/ directory creation fails
**Handling**: Check filesystem permissions, confirm parent directory exists, and re-create.

### Scenario 2: Information lost during content splitting
**Handling**: Compare the original CLAUDE.md against the new docs/ to ensure all critical information was migrated.

### Scenario 3: Document and code are inconsistent
**Handling**: doc-gardener marks as HIGH priority, proactively fix misleading content.

---

## Acceptance criteria

- [ ] CLAUDE.md <= 100 lines
- [ ] docs/ broken link rate = 0
- [ ] Every docs/ file has metadata headers (title, last_verified)
- [ ] ARCHITECTURE.md covers all top-level directories
- [ ] All files pointed to by the navigation table exist
