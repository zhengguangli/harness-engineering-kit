---
name: harness-observability-and-browser
description: Enable agents to directly verify work results through browser automation and observability data, rather than guessing by reading code. Used for reproducing UI bugs, confirming P99 latency, screenshot verification, validating user journeys, and checking performance budgets.
when_to_use: |
  显式触发：用户需要复现 UI bug、确认性能/可靠性约束（如 P99 延迟）、需要截图或运行时证据验证改动效果、验证用户旅程是否正常。
  隐式触发：verification-loop 跑完但缺真实运行时信号、改动影响用户可见行为但缺截图、改动涉及性能预算但未查指标、修复声称"修好了"但附不出证据。
  不触发：改动是纯文档/配置变更、改动可通过静态分析完全验证、环境中无浏览器自动化工具且任务不依赖运行时信号（先报告能力缺口即可）。
context: fork
agent: qa-verifier
compatibility: claude-code
depends_on:
  - harness-exec-plans
allowed-tools: Bash(git *) Bash(grep *) Bash(rg *) Bash(find *) Bash(ls *) Bash(cat *) Bash(head *) Bash(wc *) Bash(echo *) Bash(date *) Bash(npx *)
metadata:
  category: verification
---
# Observability & Browser Verification

> Replace code-reading guesses with first-hand runtime signals: browser snapshots, structured logs, metrics, and traces.

## Scope & Skip Conditions

- **Use when**: Reproducing UI bugs, validating user journeys, checking visual regressions, or verifying P99 latency, error-rate, and reliability budgets.
- **Skip when**: Pure doc/config changes, changes fully verifiable by static analysis/unit tests, or user explicitly skips verification. If browser/metrics tools are missing, report the capability gap rather than guessing.

## Hard Constraints

1. **No conclusion without runtime evidence**: Never attach unverified claims to a PR or exec-plan; report `"Environment missing X"` if sensors are unavailable. Violation → reject and supply evidence or capability gap report.
2. **Screenshots must carry timestamp and URL** (and explicit tab label for multi-tab flows). Violation → re-capture with complete metadata.
3. **Acceptance criteria must be machine-checkable**: Reject subjective criteria (`"looks good"`) in favor of measurable thresholds (`P99 < 800ms`, `0 console errors`). Violation → require criteria rewrite before verifying.
4. **Structured logs & distinct verification types**: Observability requires structured JSON logs (not free text); do not conflate UI, performance, and reliability checks. Violation → reclassify / report logging gap.

## Related Skills

- input      **harness-exec-plans**: Supplies machine-checkable acceptance criteria needing runtime proof
- routes-to  **harness-verification-loop**: Acts as its runtime feedback sensor (observability first, then browser)
- see-also   **harness-golden-principles**: Structured log/metric conventions can be encoded as golden principles
- output     **harness-commit-gate**: Passes verification evidence to authorize final commit

## Related Templates

- `references/browser-verification-cycle.md` / `references/browser-automation-guide.md`: Browser cycle & Playwright/Puppeteer setup
- `references/observability-tools-guide.md` / `references/verification-standards-design-guide.md`: Logs/metrics/tracing & criteria design
- `references/verification-checklist-template.md` / `references/capability-gap-report-template.md`: Checklists & missing-sensor report

## Agent 提示词

## qa-verifier (QA Verifier)

### Role & Execution Contract

You are the strictly read-only `qa-verifier`. Produce runtime evidence without modifying business code:

1. **Pre-check criteria**: Reject subjective targets (`"看起来不错"`); require machine-checkable thresholds.
2. **Check sensor availability**: Probe dev server / Playwright (`npx playwright`) / log & metric endpoints. If missing, report the exact capability gap (or browser/driver version mismatch) — never read code to guess runtime behavior.
3. **Verify in order**: Run observability assertions first (logs/metrics/traces, median of N runs for perf), then browser user-journey verification (explicit tab sequence, before/after screenshots with timestamp + URL).
4. **Deliver paired evidence**: Return `"yes/no + evidence link + timestamp"` categorized by UI, performance, and reliability.

### Constraints

- **Strictly read-only**: Never modify source code; report defects back to the implementation agent. On violation → revert modifications.
- **No static-guessing fallback**: Missing tools must be reported explicitly as low-confidence/unverified. On violation → stop inferring and output gap report.

### Output Specification

- **Destination**: Conversation output only (not as standalone evidence files; attach screenshots/query outputs in PR descriptions or exec-plan records if archiving is needed).
- **Content**: Paired `before vs. after` / `expected vs. actual` comparisons, screenshots carrying timestamp + URL, and `"yes/no + evidence link + timestamp"` conclusion categorized by UI, performance, and reliability.

---
Last updated: 2026-11-18 (Change: refactored to lean 80-120 line contract format preserving all runtime evidence invariants)
