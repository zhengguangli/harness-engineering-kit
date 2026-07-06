# Docs index template

This file combines the templates for `design-docs/index.md` and `product-specs/index.md` — their structure is similar; use them together during initialization only.

---

## Design document index (`docs/design-docs/index.md`)

Records each design document's location, current verification status, and last verification date. The `doc-gardener` agent compares this index against the actual document / code state.

| Document | Topic | Verification status | Last verified |
|---|---|---|---|
| `core-beliefs.md` | Core operating beliefs of agent-first | ✅ Verified | <YYYY-MM-DD> |
| <Add other design documents> | | | |

Verification status descriptions:
- ✅ Verified: Recently confirmed to be consistent with current code state
- ⚠️ Pending verification: Not confirmed within the agreed period, may be outdated
- ❌ Known outdated: Confirmed inconsistent with current code state, awaiting fix

---

## Product spec index (`docs/product-specs/index.md`)

Records the location of product feature spec documents, as the entry point for agents to understand "what to build, for whom".

| Spec | One-line description | Status |
|---|---|---|
| <e.g. new-user-onboarding.md> | <One-line description> | draft / shipped / deprecated |

> It's recommended to keep spec documents concise — if detailed interaction specs and visual mockups live outside the repo (design tools, etc.), at least leave a "current status summary + where to find the full version" note here, so agents aren't completely blind to this context.
