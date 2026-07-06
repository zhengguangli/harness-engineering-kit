## When the Loop Gets Stuck, First Ask “What Capability Is Missing”

Note: The “Fix Direction” column in the table below references other harness skills. If the relevant skill is not installed, fall back to performing the equivalent check manually within the same context, and note in the report that “Skill X is not installed; fallback processing applied.”

Common “missing capability” patterns and their corresponding fix directions:

| Stuck Symptom | Possibly Missing Capability | Fix Direction |
|---|---|---|
| Repeatedly modifying the same code with no behavioral change | Cannot see actual runtime results | Integrate `harness-observability-and-browser`; give it logs/screenshots instead of letting it guess |
| After changes, unsure if anything else is broken | Lacks structured tests/boundary checks | Integrate lint/structured tests from `harness-architecture-boundaries` |
| Re-exploring project context every round | Lacks discoverable context | Check `harness-repo-map`; write missing knowledge into docs/ |
| Lint errors but unsure how to fix | Error messages lack fix instructions | Following `harness-architecture-boundaries` advice, embed fix methods into error text |
| Delegated review agent errors out or is unresponsive | Review agent itself lacks capabilities | Mark in the report that “review capability is unavailable,” perform equivalent checks manually within the same context, or escalate to a human |

Do not attribute these symptoms to “the model isn't strong enough.” First assume the environment is missing a piece, and fill that piece in.

---
Last updated: 2026-06-30
