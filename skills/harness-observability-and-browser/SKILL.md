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
allowed-tools: Bash(git *) Bash(grep *) Bash(rg *) Bash(find *) Bash(ls *) Bash(cat *) Bash(head *) Bash(wc *) Bash(echo *) Bash(date *) Bash(npx *)
metadata:
  category: verification
---
# Observability & Browser Verification

## Core Principles
- **Replace inference with real signals**: Every agent judgment should be based on first-hand signals — the actual state rendered in the browser, errors actually logged, latency actually measured by metrics. Without these, the agent can only statically infer by reading code.
- **Feedback sensors are first-class citizens**: Browser snapshots, structured logs, metric queries, and trace data are all "feedback sensors." Verification results must be accompanied by this evidence.
- **Acceptance criteria must be machine-checkable**: Write "P99 latency < 800ms", not "looks good."

## When to Use
- When you need to reproduce a UI bug or verify whether a user journey is working correctly.
- When you need to confirm performance/reliability constraints (startup time, P99 latency).
- When there is no automated means to confirm whether a change actually fixed the problem.

## When Not to Use
- The change does not involve UI behavior or performance/reliability constraints.
- The change can be fully verified through static analysis (type checking, lint, unit tests).
- Pure documentation/configuration changes.
- No browser automation tool is available in the environment and the task does not depend on runtime signals — just report the capability gap.

## Methodology

### Two Types of Feedback Sensors

1. **Browser-driven verification**: Reproduce UI bugs, verify interaction flows, check visual regressions. For the full cycle, see `references/browser-verification-cycle.md`.
2. **Observability loop**: Performance budgets, reliability constraints, cross-service behavior verification. The application outputs structured logs/metrics/traces, and the agent validates constraints through query interfaces without reading code to guess runtime behavior.

Chained usage: Implement fix → Observability confirms underlying behavior → Browser confirms user-visible results → Both types of evidence attached in PR/exec-plan.

### Browser Automation Configuration Reference

Playwright and Puppeteer are two mainstream browser automation tools. In this skill, install the browser engine on demand via `npx playwright install` before use.

**Common configurations**:
- **Chrome/Chromium headless mode**: `npx playwright install chromium` → `npx playwright test --headed=false`
- **Mobile emulation**: `playwright.devices['iPhone 14']` (Playwright) or `puppeteer.devices['iPhone 14']` (Puppeteer)
- **Visual regression**: Playwright's `page.screenshot({fullPage: true})` + pixel-level diff tools (e.g. `pixelmatch`)
- **Network throttling**: Playwright's `page.route()` intercepts requests to simulate poor network conditions
- **Real device cloud**: BrowserStack / Sauce Labs integration (see configuration in `references/browser-automation-guide.md`)

### Acceptance Criteria Examples

- "P99 latency < 800ms" (metric query verification)
- "Screenshots of critical user journeys show no anomalies in before/after comparison" (browser screenshot verification)
- "Zero occurrences of a specific error log in the last N runs" (log query verification)
- "Page load time < 3 seconds" (performance measurement verification)
- "Mobile login flow screenshot matches the design mockup" (visual regression verification)
- "HTTP response status for endpoint X is 200 and response body contains field Y" (API verification)
- "Console has zero errors after executing user journey Z" (browser console verification)
- "Network waterfall shows asset X loads within 2 seconds under 3G throttling" (network performance verification)

### Verification Procedure
1. **Clarify the verification target and route it**: Involves UI → browser verification; involves performance/reliability → observability verification; involves both → observability first, then browser.
2. **Browser verification**: Execute the browser-driven verification cycle, producing before/after comparison evidence (screenshots/DOM snapshots).
3. **Observability verification**: Write constraints as queryable assertions, use observability tools to verify and record the values.
4. **Attach evidence**: Attach verification results (screenshots, query results) in the change description — all checks must pass for verification to be complete.
5. **Capability gaps**: If the project lacks necessary observability capabilities, record the gap itself as a to-be-fixed "environment deficiency."

## Hard Constraints
- **Conclusions without supporting evidence must not be attached to a PR**: Violations will be rejected by verification-loop, requiring supplemental verification evidence before resubmission.
- **Browser screenshots must include a timestamp and URL**: Screenshots lacking metadata are considered invalid evidence and will be rejected by verification-loop.
- **Acceptance criteria must be machine-checkable**: Subjective criteria (e.g., "looks good", "feels fast") are not allowed. Violation → reject the criteria and require rewrite with measurable conditions (e.g., "P99 < 800ms", "screenshot matches design within 5% pixel diff").
- **Observability verification must use structured logs**: Free-text logs are not queryable or aggregatable. Violation → report the gap and recommend converting to structured JSON logs before verification can proceed.
- **Verification type must be correctly distinguished**: UI verification, performance verification, and reliability verification must not be conflated. Violation → reclassify the verification type and re-run with the correct method.

## Examples

**Example 1**: User says "登录页面白屏了"
**Handling**: Browser verification → Open page → Compare screenshots → Discover JS error → Report to the implementation agent

**Example 2**: User says "P99 延迟是否达标"
**Handling**: Observability verification → Query metrics → Compare against thresholds → Output yes/no + evidence

**Example 3**: User says "修复了 checkout 流程，帮我验证一下"
**Handling**: Chained verification → Observability first (check API response times and error rates for /checkout endpoints) → Browser second (drive the full checkout user journey, capture before/after screenshots) → Attach both evidence sets in the PR description

**Example 4**: User says "移动端首页加载太慢了"
**Handling**: Browser verification with mobile emulation → Throttle to 3G → Capture waterfall + screenshot → Identify render-blocking resources → Report findings with network timeline evidence

## Key Points
- Do not draw conclusions without supporting evidence — either add validation methods, or explicitly state "cannot be verified in the current environment."
- Browser and observability are complementary: the browser sees the user's perspective, observability sees the system's perspective.
- Verification outputs should be concrete enough to be directly attached in PR descriptions or exec-plan acceptance records.
- Use a stable test environment that is consistent with the production environment.
- Design repeatable tests using fixed data and state.
- Capture sufficient evidence: screenshots with timestamps and URLs, record console logs.
- Use structured logs (JSON format) including timestamps, levels, and request IDs.
- Monitor critical paths, identifying error rates and latency for key business flows.
- Pre-validate acceptance criteria before starting: reject subjective criteria in favor of machine-checkable conditions.
- When both verification types are needed, run observability first (system-level), then browser (user-level).

## Edge Case Handling

> For general edge cases (infrastructure deficiencies, etc.) see `references/common-edge-cases.md`. Only the edge cases unique to this skill are listed below.

### Historical Data Contamination
**Scenario**: Historical logs/metrics interfere with current verification
**Handling**: Clean historical data before verification, or use time-range filtering, add unique identifiers to isolate verification

### Cross-Service Verification
**Scenario**: Need to verify a request chain spanning multiple services
**Handling**: Use distributed tracing (e.g., Jaeger, Zipkin), record request chains, verify performance metrics for each service

### Mobile Verification
**Scenario**: Need to verify mobile page rendering and interaction
**Handling**: Use Playwright's mobile emulation or real device testing (e.g., BrowserStack, Sauce Labs)

## Common Pitfalls
- **Reading code to guess runtime behavior**: Just because code has a try-catch doesn't mean the exception is actually being caught — check the logs.
- **Free-text logs**: Not queryable, not aggregatable — must use structured logs.
- **Verification without evidence**: Claiming "it's fixed" without providing screenshots or query results.
- **Environmental data contamination**: Historical logs/metrics interfere with current verification, used without cleanup.
- **Browser automation tool unavailable**: No browser automation tool is installed in the environment.
- **Performance metric query failure**: Monitoring system is unavailable or the query syntax is wrong.

## Best Practices

- Before browser verification, confirm the dev server is accessible: `curl -o /dev/null -s -w "%{http_code}" http://localhost:<port>`.
- Include test case identifier and timestamp in screenshot filenames: `login-flow-before-20260703T1430Z.png`, for easy archiving and comparison.
- For performance verification, use the median of the last N runs rather than the average to exclude single-spike interference.
- When embedding screenshots in PR descriptions, use `<details><summary>Before / After</summary>![screenshot]</details>` to collapse them and avoid overly long PR bodies.

## Related Skills

- Upstream **harness-verification-loop**: Receives outputs (verification cycle trigger signals) as the trigger for runtime verification
- Upstream **harness-exec-plans**: Execution plan acceptance criteria may require observability/browser verification evidence
- Downstream **harness-commit-gate**: This skill's outputs (verification result evidence) are passed downstream as the basis for quality gate pass
- Peer **harness-golden-principles**: Observability patterns (structured logs, metric naming) can be encoded as golden principles for consistent instrumentation

## Related Templates

- `references/browser-verification-cycle.md`: Complete browser-driven verification cycle flow
- `references/browser-automation-guide.md`: Playwright/Puppeteer configuration and usage guide
- `references/verification-checklist-template.md`: Verification checklist template
- `references/verification-standards-design-guide.md`: Verification standards design guide
- `references/capability-gap-report-template.md`: Capability gap report template
- `references/observability-tools-guide.md`: Observability tools configuration guide
- `references/common-edge-cases.md`: General edge case handling guide

## Agent 提示词

## QA Verifier

### Skip Conditions

- **Pure documentation/configuration changes with no runtime behavior change**: Skip the entire verification process.
- **Changes that can be fully verified through static analysis** (type checking, lint, unit tests): Skip browser and observability verification.
- **No browser automation tool in the environment and the task does not depend on runtime signals**: Report the capability gap and terminate.
- **Change only affects backend API responses with no user-visible UI impact**: Skip browser verification; observability verification may still apply.
- **User explicitly says "不需要验证" or "直接提交"**: Respect the user's intent; do not trigger verification.
- **Performance metrics system is unavailable and the task requires metric verification**: Report the capability gap and fall back to log analysis if available.

### Role Definition

Produces verification evidence based on real runtime signals (browser rendering, structured logs, metrics, traces). Does not modify code — only confirms "whether the problem actually exists / whether it has actually been resolved." Skilled at using browser automation and observability tools for verification.

### Core Capabilities

- Detect available browser automation tools in the environment and drive the verification cycle.
- Translate performance/reliability constraints into queryable assertions and execute verification.
- Pre-validate acceptance criteria to ensure they are machine-checkable before starting verification.
- Produce before/after comparison evidence (screenshots, DOM snapshots, query values).
- Distinguish verification types (UI, performance, reliability) and apply the correct method for each.
- Give clear "yes/no + evidence" conclusions.

### Execution Flow

0. **Pre-check acceptance criteria**: Confirm verification targets are machine-checkable. Reject subjective criteria (e.g., "看起来不错") and ask for rewrite with measurable conditions.
1. **Clarify the target**: Verify user-visible behavior (UI), underlying runtime constraints (performance/reliability), or both.
2. **Environment check**: Detect whether browser automation tools are available. If unavailable and the task is UI verification → report the capability gap, do not fall back to reading code and guessing.
3. **UI verification**: Drive the application, capture before/after state snapshots (DOM/screenshots), observe console output and network requests.
4. **Performance verification**: Write constraints as queryable assertions (e.g., "P99 < 2s"), verify via log/metric query tools.
5. **Produce evidence**: Present before vs. after state, query values vs. constraint thresholds as paired comparisons.
6. **Clear conclusion**: Whether the problem was reproduced, whether the fix took effect, whether constraints are satisfied — in "yes/no + evidence" format.

### Constraints

- **Read-only, no modifications**: Do not modify business code — when a problem is found, report it to the implementation agent for handling. Violations: revert the modification operation.
- **No conclusion without evidence**: Every conclusion must be accompanied by evidence (screenshots, log excerpts, query results). Violations: supply the missing evidence.
- **Do not fall back to reading code and guessing**: When the environment lacks browser automation tools and the task is UI verification, report the capability gap rather than inferring by reading code. Violations: stop inferring and report the environment deficiency.
- **Distinguish verification types**: Must accurately distinguish between UI verification, performance verification, and reliability verification — do not conflate them. Violations: reclassify.
- **Screenshot metadata mandatory**: Every screenshot must include a timestamp and page URL — screenshots missing either element are considered invalid evidence. Violations: re-take screenshots with complete metadata.
- **Pre-check acceptance criteria before starting**: If the acceptance criteria are subjective ("看起来不错"), reject and request rewrite with machine-checkable conditions before proceeding. Violations: stop verification, request corrected criteria.

### Output Specification

- Evidence list presented in "before vs. after / expected vs. actual" paired format.
- Conclusion format: "yes/no + evidence link + timestamp".
- If the environment lacks tools, mark "Environment missing X, only static inference performed this round, low confidence in conclusion."
- Categorize by UI issues, performance issues, and reliability issues, each with remediation suggestions.
- Output primarily in conversation — if archiving is needed, attach screenshots and query results in the PR description or exec-plan acceptance records, not as standalone files.

---
Last updated: 2026-07-10 (Change: Hard Constraints 2→5, Examples 2→4, Related Skills 2→4, Related Templates 2→7)
