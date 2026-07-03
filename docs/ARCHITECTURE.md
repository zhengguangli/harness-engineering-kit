# ARCHITECTURE.md

<!-- Canonical owner: harness-architecture-boundaries -->

This document defines the domain division and dependency direction rules for the harness-engineering-kit.

## Domain Division

| Domain | Description | Path |
|---|---|---|
| skills | 13 skills (methodology + agent prompts + templates) | `skills/harness-*/` |
| scripts | Validation scripts (frontmatter, keyword consistency, regression) | `scripts/` |
| tests | Trigger regression test cases and reports | `tests/` |
| ci | GitHub Actions workflows and PR templates | `.github/` |

## Skill Layering & Dependency Direction

```
Layer 0 Information Collection    harness-project-intake
       ↓
Layer 1 Scaffolding Setup        harness-bootstrap
       ↓
Layer 2 Knowledge & Constraints  harness-repo-map, harness-architecture-boundaries,
                                 harness-golden-principles, harness-prompt-optimizer
       ↓
Layer 3 Plan-Driven              harness-exec-plans
       ↓
Layer 4 Execution & Verification harness-verification-loop, harness-observability-and-browser
       ↓
Layer 5 Commit Gate              harness-commit-gate

Meta-layer                       harness-orchestration, harness-authoring
```

- Dependencies flow downward only: Layer N skills may reference outputs from Layer < N, but not the reverse.
- Skills within the same layer can run in parallel and do not depend on each other.
- Meta-layer skills can be called from any layer (orchestration handles routing, authoring extends the system itself).

## Internal Structure of Each Skill

```
skills/<name>/
├── SKILL.md          # Methodology body + agent prompt (including frontmatter)
└── references/       # Template files
```

Agent prompts have been inlined into the `## Agent 提示词` section of SKILL.md.

## Supporting Infrastructure Dependency Direction

```
scripts/ → skills/    (Scripts validate skill frontmatter and keywords)
tests/   → skills/    (Regression test cases verify skill trigger logic)
.github/ → scripts/   (CI invokes validation scripts)
```

- scripts/ only reads from skills/, never modifies it.
- Regression test cases in tests/ depend on keyword mappings defined in scripts/.
- .github/workflows/ invokes `make triggers-all` to trigger the full validation chain.

## Data Boundary Rules

- Each `SKILL.md`'s frontmatter is a contract between the skill and the platform -- the platform only reads fields it recognizes and ignores unknown fields.
- The canonical version of agent prompts lives in the `## Agent 提示词` section of `SKILL.md`.

## Current Enforcement Status

| Rule | Enforcement Method | Status |
|---|---|---|
| Required frontmatter fields | `scripts/validate-skill-triggers.sh` | ✅ Enforced |
| Keyword consistency | Covered in regression tests | ⚠️ Merged into regression checks |
| Trigger regression | `scripts/run-trigger-regression.sh` | ✅ Enforced |
| Agent prompt existence | `scripts/validate-agent-prompt-sync.sh` | ✅ Enforced |
| No circular dependencies between skills | Manual review | ⚠️ Documented only, not enforced |

## Lessons Learned

Key lessons from the three-round skill quality evaluation and optimization:

1. **Three-round iterative optimization works**: Continuous improvement in skill quality was achieved through three rounds of iteration
2. **Trigger condition descriptions matter**: Users need clear trigger conditions to understand when to use a skill
3. **Usage examples are critical**: Concrete usage examples help users understand how to use a skill
4. **Error handling guidance needs improvement**: Users need to know how to handle issues encountered during use
5. **Automated checks improve efficiency**: Automated validation scripts quickly identify basic issues
6. **Manual review ensures quality**: Manual review catches issues that automation cannot
7. **Quality baselines are important**: Establishing clear quality baselines supports continuous improvement
8. **Documentation style needs consistency**: Unified documentation style helps users understand and use skills

Key lessons from the full A+-grade optimization:

1. **Full optimization requires a systematic approach**: Establish unified optimization standards and execute in priority batches
2. **Edge case handling is key to A+ grade**: Every skill must handle a variety of edge cases
3. **Best practices improve content quality**: Provide best practices to help users get the most from skills
4. **Agent prompts need careful design**: Ensure clear roles, explicit flows, and reasonable constraints
5. **Automation support boosts efficiency**: Provide automated validation scripts and CI/CD integration
6. **User experience requires continuous optimization**: Ensure a gentle learning curve, convenient usage, and strong error recovery

See `docs/lessons-learned/skills-quality-optimization-2026-07-02.md` for detailed lessons.

---
Last updated: 2026-07-02 (Change: added full A+-grade optimization lessons)
