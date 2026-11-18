# ARCHITECTURE.md

<!-- Canonical owner: harness-architecture-boundaries -->

This document defines the domain division and dependency direction rules for the harness-engineering-kit.

## Domain Division

| Domain | Description | Path |
|---|---|---|
| skills | 9 skills (lean contracts + agent prompts + templates) | `skills/harness-*/` |
| scripts | Validation scripts (frontmatter, keyword consistency, regression) | `scripts/` |
| diagnostics | Trigger-matching measurement experiments (not gate; TD-006) | `scripts/diagnostics/` |
| tests | Trigger regression test cases and reports | `tests/` |
| ci | GitHub Actions workflows and PR templates | `.github/` |

## Skill Layering & Dependency Direction

```
Layer 0 Intake & Bootstrap       harness-bootstrap
       ↓
Layer 1 Knowledge & Constraints  harness-repo-map, harness-architecture-boundaries,
                                 harness-golden-principles
       ↓
Layer 2 Plan-Driven              harness-exec-plans
       ↓
Layer 3 Execution & Verification harness-verification-loop, harness-observability-and-browser
       ↓
Layer 4 Commit Gate              harness-commit-gate

Meta-layer                       harness-orchestration
```

- Dependencies flow downward only: Layer N skills may reference outputs from Layer < N, but not the reverse.
- Skills within the same layer can run in parallel and do not depend on each other.
- Meta-layer skills can be called from any layer (`harness-orchestration` handles routing).

### Declaring a dependency

A skill's real data dependencies are declared in `SKILL.md` frontmatter:

```yaml
depends_on:
  - harness-bootstrap
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

Every `SKILL.md` uses the lean contract format (target 80–120 lines, soft cap 150 lines) in this fixed order:

```
1. Scope & Skip Conditions
2. Standard Workflows           (optional, orchestration only)
3. Hard Constraints
4. Related Skills
5. Related Templates
6. Agent 提示词                 (+ agent heading + Role & Execution Contract / Constraints / Output Specification)
```

`scripts/lib/harness_check.py` enforces this contract, line budget (`<= 150` pass, `151-180` warn, `> 180` fail), and `Last updated` presence across all 9 skills.

## Internal Structure of Each Skill

```
skills/<name>/
├── SKILL.md          # Lean contract + inline agent prompt (including frontmatter)
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
- .github/workflows/ invokes `python3 scripts/run-all.py` to trigger the full validation chain.
- 门禁面（gate surface）= `scripts/*.py`（顶层，含 `lib/`）+ `tests/**/test_*.py` + `tests/triggers/cases.json`。`scripts/diagnostics/` 及其中的 `cases.diagnostic.json` 是测量/实验区，不属于门禁（TD-006）。

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
Last updated: 2026-11-18 (Change: 13→9 subtraction and 5-layer lean contract standard recorded after Tier-3 A/B evaluation)
