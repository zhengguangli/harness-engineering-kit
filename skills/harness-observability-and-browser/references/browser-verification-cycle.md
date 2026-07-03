### 1. Browser-Driven Verification

Applies to: UI bug reproduction, interaction flow verification, visual regression checks.

Standard cycle:

```
Select target (bug to reproduce / user journey to verify)
  → Take pre-action snapshot (DOM state / screenshot)
  → Execute trigger path (click, input, navigation)
  → Observe runtime events (console errors, network requests, state changes)
  → Diagnose issue
  → Apply fix (*)
  → Restart application
  → Re-execute the same path
  → Take post-action snapshot, compare with pre-action
  → Loop until state matches expectations
```

> (*) Note: fix and restart are handled by an execution agent (e.g., verification-loop-runner); qa-verifier is only responsible up to "diagnose issue" and "capture comparison evidence", and does not apply fixes itself.

If a browser automation tool is already configured in the project (e.g., a Playwright/Chrome DevTools-related MCP tool), prefer using it; if not configured, remind the user that this is a worthwhile environment capability gap to fill, rather than falling back to "reading code to guess UI behavior".

### Failure Branches (Unified Degradation)

- Missing browser / driver unavailable: Report "environment capability gap: missing browser automation tool", fall back to non-UI verification (logs/metrics) or exit with environment setup recommendations.
- Page unreachable / startup failure: Record error evidence (screenshot/logs), report root cause (port conflict/auth failure/startup script error), do not self-fix.
- Permission constraints (CI headless environment restrictions): Enable headless mode or degrade to structured log/metric verification.
- Unstable page (flaky): Mark as "unstable path", suggest one retry with evidence attached; if still unstable, classify as requiring higher-permission review.

**Key deliverable**: Pre- and post-fix screenshot/screen recording comparison. This is not just evidence for humans, but also the basis for the agent to judge "this fix is really done" — the deliverable itself is the verification means, not an attachment after verification is complete.

**Environment isolation recommendation**: If possible, have each parallel task/worktree correspond to an independent launchable application instance, so that multiple agents verifying different changes simultaneously do not pollute each other's observed state.

---
Last updated: 2026-06-29
