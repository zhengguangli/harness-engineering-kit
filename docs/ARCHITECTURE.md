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

### Declaring a dependency

A skill's real data dependencies are declared in `SKILL.md` frontmatter:

```yaml
depends_on:
  - harness-project-intake
```

`depends_on` means **"I consume this skill's output as input"** and nothing else. Routing
hand-offs, see-also pointers and template-provenance notes do **not** belong here — they live
in the human-readable `## Related Skills` section, which is not used to build the graph.

`## Related Skills` uses four explicit labels so intent is unambiguous:

| Label | Meaning |
|---|---|
| `input` | This skill consumes the other skill's output (mirrors a `depends_on` entry) |
| `output` | The other skill consumes this skill's output |
| `routes-to` | Hand-off / routing only — no data dependency |
| `see-also` | Related, but no data flows between them |

`scripts/validate_skill_dependencies.py` enforces: no cycles, downward-only flow, Meta-layer
isolation, `depends_on` targets exist, and cross-skill `../harness-*/references/*` paths
resolve. Related Skills entries lacking any of the four labels raise a WARN.

### Canonical section order

Every `SKILL.md` uses this top-level order. Sections 4-10 may be omitted by a skill that
genuinely has nothing to say, but must never be reordered:

```
1.  Core Principles
2.  When to Use
3.  When Not to Use
4.  Methodology                (+ optional skill-specific subsections)
5.  Hard Constraints
6.  Examples
7.  Key Points
8.  Edge Case Handling
9.  Common Pitfalls
10. Best Practices
11. Related Skills
12. Related Templates
13. Agent 提示词               (+ agent name heading + its 6 sub-sections)
```

Skill-specific sections that do not fit the list above (`Workflow`, `Project Card`,
`Five Standard Workflows`, `Cross-Skill Handoff Points`, `FAQ / Troubleshooting`,
`Routing Recommendation`, `Golden Principles vs Architecture Boundaries`) go immediately
after the section they elaborate — typically after `Methodology`.

The order is the modal position across the 13 skills, not an arbitrary preference. Two
rules make it enforceable: `Hard Constraints` always precedes `Examples`, and
`Related Skills` / `Related Templates` always sit between `Best Practices` and
`Agent 提示词`.

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
- `compatibility` and `metadata` (with `category`) are harness-specific custom frontmatter extensions, not Claude Code standard fields. They are silently ignored by Claude Code.
- The canonical version of agent prompts lives in the `## Agent 提示词` section of `SKILL.md`.

## Current Enforcement Status

| Rule | Enforcement Method | Status |
|---|---|---|
| Required frontmatter fields | `scripts/validate_skill_triggers.py` | ✅ Enforced |
| Keyword consistency | Covered in regression tests | ⚠️ Merged into regression checks |
| Trigger regression | `scripts/run_trigger_regression.py` | ✅ Enforced |
| Agent prompt existence | `scripts/validate_agent_prompt_sync.py` | ✅ Enforced |
| No circular dependencies between skills | `scripts/validate_skill_dependencies.py` | ✅ Enforced |

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

See `docs/QUALITY_SCORE.md` for detailed lessons.

---
Last updated: 2026-09-24 (Change: added the canonical SKILL.md section order, derived from the modal position across all 13 skills)
