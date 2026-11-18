---
name: harness-golden-principles
description: Encode recurring review feedback into mechanized Golden Principles, run periodic read-only codebase sweeps for pattern drift, and propose small-grained fix PRs. Used for scanning code smells, cleaning AI-generated drift, and separating taste rules from CI hard blocks.
when_to_use: |
  显式触发：用户想把人类品味编码为黄金原则或机械化规则、治理 AI 生成代码的重复/不一致模式、建立周期性代码扫描机制、扫描代码异味、清理 AI 代码风格不统一、给代码库建立编码风格品味的自动化 lint 规则（结构性依赖规则归 harness-architecture-boundaries）。
  隐式触发：review 里反复出现同类反馈、代码质量参差不齐出现模式漂移与重复模式、团队靠人工定期"打扫 AI 写的代码"、用户问"怎么让代码风格统一"。
  不触发：需要结构性架构约束（用 harness-architecture-boundaries）、项目规模极小没有重复模式、用户只想了解现有规则而非建立新规则。
context: fork
agent: entropy-collector
compatibility: claude-code
depends_on:
  - harness-bootstrap
allowed-tools: Bash(git *) Bash(grep *) Bash(rg *) Bash(find *) Bash(ls *) Bash(cat *) Bash(head *) Bash(wc *) Bash(echo *) Bash(date *)
metadata:
  category: quality
---
# Golden Principles & Garbage Collection

> Code judgment once, enforce forever: taste deviations are swept continuously in small batches rather than turning into CI merge blocks or spring-cleaning marathons.

## Scope & Skip Conditions

- **Use when**: Encoding recurring review/bug feedback as lint or taste rules, running periodic sweeps for AI-generated pattern drift across files, or maintaining `docs/QUALITY_SCORE.md`.
- **Skip when**: Violation breaks a structural invariant (dependency direction / data boundary → delegate to `harness-architecture-boundaries`), repo is undergoing a major active refactor (high noise), or project is too small to have repeated patterns.

## Hard Constraints

1. **Originate from real signals**: Every principle must trace to actual review feedback, bugs, or refactoring PRs — never invent abstract rules. Violation → delete fabricated rules.
2. **Taste preferences are NOT CI hard blocks**: Structural invariants block merge (`architecture-boundaries`); taste principles run via periodic sweeps and small PRs (`[GC-auto]` for mechanical fixes). Violation → re-route structural violations to `boundary-auditor`.
3. **One deviation type per fix recommendation (~1 min review size)**: Never bundle unrelated cleanups. Violation → split into independent recommendations.
4. **Persist unprocessed findings**: Log deferred deviations in `docs/exec-plans/tech-debt-tracker.md` rather than dropping them. Violation → append missing tracker entries.
5. **Read-only scanner**: `entropy-collector` scans and writes only its report; never edits source files directly. Violation → retract code edits.

## Related Skills

- input      **harness-bootstrap**: Consumes initialized `docs/QUALITY_SCORE.md` & `tech-debt-tracker.md`
- see-also   **harness-architecture-boundaries**: Structural invariants vs. taste preferences boundary (same layer, parallel)
- output     **harness-verification-loop**: Consumes fix queue items when executing remediation PRs

## Related Templates

- `references/pr-guidelines.md`: Small-PR sizing & auto-merge rules
- `references/quality-score-template.md`: `docs/QUALITY_SCORE.md` template
- `references/principle-prioritization.md` / `references/rule-formulation-checklist.md`: Rule prioritization & formulation checklist

## Agent 提示词

## entropy-collector (Entropy Sweeper)

### Role & Execution Contract

1. **Load & filter principles**: Read encoded lint rules and taste principles (abort with `"No principles found"` if none exist). Route any structural invariant to `harness-architecture-boundaries`.
2. **Sweep & compare cross-file**: Run existing lint checks first, then grep/compare ≥2 files implementing the same concept to detect cross-file drift (prefer lint rules over manual taste checks; flag high-frequency triggers as signal annotations).
3. **Classify risk & scope**: Tag purely mechanical fixes as `suggest auto-merge` and behavioral changes as `requires manual review` (default to manual review if uncertain). Isolate one deviation type per fix recommendation.
4. **Record & retire**: Write scan report, note deferred items for `docs/exec-plans/tech-debt-tracker.md`, and flag principles with zero triggers across 3 quarterly cycles for retirement.

### Constraints

- **Read-only on code**: Only produce scan reports and fix recommendations. On violation → retract code modifications.
- **Cross-file comparison required**: Compare ≥2 files for cross-module principles. On violation → expand scan scope before reporting.

### Output Specification

- **Output path**: `docs/quality-reports/golden-principles-scan.md` (overwritten in place; history tracked in git).
- **Content**: Summary + per-deviation entries containing `location` (`file:line`), `principle reference`, `risk level` (`suggest auto-merge` / `requires manual review`), `fix recommendation`, and signal annotations for frequent triggers.

---
Last updated: 2026-11-18 (Change: refactored to lean 80-120 line contract format; depends_on updated to harness-bootstrap)
