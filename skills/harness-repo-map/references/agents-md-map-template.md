# CLAUDE.md

> This file is a map, not an encyclopedia. If you can't find the answer here, look for it in the corresponding `docs/` files below — don't assume information outside this file doesn't exist; it's just stored elsewhere.

## What this repository is

<Describe the project in one or two sentences; don't expand into details, put details in docs/product-specs/>

## Hard constraints (very few; violations block merges)

- All external data entering the system boundary must be parsed into strong types; do not keep passing it as weak types after validation (parse, don't validate).
- Dependency direction and layering rules are in `docs/ARCHITECTURE.md`, mechanically enforced by structured tests in CI; no exceptions allowed.
- <Add based on the project's actual situation; each rule should be mechanically checkable by lint/tests>

## Where to find more

| I want to know... | Look here |
|---|---|
| Overall architecture, layering and dependency direction rules | `docs/ARCHITECTURE.md` |
| Design decision background and "core beliefs" | `docs/design-docs/index.md`, `docs/design-docs/core-beliefs.md` |
| Active/completed execution plans | `docs/exec-plans/active/`, `docs/exec-plans/completed/` |
| Known tech debt not yet addressed | `docs/exec-plans/tech-debt-tracker.md` |
| Product requirements / feature specs | `docs/product-specs/index.md` |
| Quality scores by domain/layer | `docs/QUALITY_SCORE.md` |
| Auto-generated content (do not hand-edit) | `docs/generated/` |
| Concise references for third-party libraries/tools | `docs/references/` |

## Working tips

- For complex tasks that may span multiple sessions, first create an exec-plan using `harness-exec-plans` skill; don't jump straight in.
- After making changes, run the self-verification loop (`harness-verification-loop`) instead of committing everything at once.
- For changes involving UI/performance verification, use `harness-observability-and-browser` skill to produce real evidence.
- Not sure if a rule is still valid? Check the "last verified" date in the corresponding docs file; expired rules should be flagged, not trusted.


---

## Appendix A: Core beliefs template (`docs/design-docs/core-beliefs.md`)

Define the agent-first operating principles for this repository. These are judgments that have been repeatedly confirmed and are worth keeping long-term, not temporary preferences.

## Example entries (replace based on actual project situation)

1. **If it can't be seen, it doesn't exist**: Any knowledge that only lives in chat history / verbal consensus is as good as non-existent for an agent. New architectural consensus and product decisions must be written into the corresponding docs/ files to be considered "effective".
2. **Constrain invariants, not implementation details**: Architecture boundaries must be mechanically enforced; concrete coding style within boundaries is free.
3. **Plans are artifacts, not drafts**: Plans for complex tasks must be saved to disk, versioned, and readable by subsequent agents.
4. **When failing, first ask "what capability is missing"**: Don't default to "try again" as the fix.
5. **Entropy needs continuous cleanup, don't save it for a spring cleaning**: Tech debt is a high-interest loan; small continuous repayments are better than batch processing.

---
Last updated: <YYYY-MM-DD>

---

## Appendix B: Rules for writing CLAUDE.md

(Map) rules

1. **Target length ~100 lines**. If you reach 200 lines and aren't wrapping up, you're writing an encyclopedia not a map — sink content down to the corresponding `docs/` files and leave only a one-line pointer in CLAUDE.md.
2. **Only three types of content**: (a) Repository structure overview and "start here" pointers, (b) A very small number of global hard constraints (e.g. "no hand-written code", "all data boundaries must parse, not validate"), (c) A navigation table pointing to each `docs/` subdirectory.
3. **Don't write details that change frequently** (specific API signatures, current progress, status of a particular bug) — put these in `docs/generated/`, `exec-plans/`, kept fresh by tools or agent tasks.
4. **Every rule must be actionable or verifiable**. If a rule can't be mechanically checked by lint/tests, either make it checkable or acknowledge it's just advice not a constraint — don't mix them up.

---
---
Last updated: <YYYY-MM-DD> · If you modify the structure of this file, remember to update the skeleton described in the `harness-repo-map` skill (if there's any deviation). Template file name: `claude-md-map-template.md`.
