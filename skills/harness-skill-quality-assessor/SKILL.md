---
name: harness-skill-quality-assessor
description: Systematically evaluate skill quality in the harness system — providing quantifiable assessment reports and layered improvement recommendations across 8 dimensions including structural completeness, content quality, usability, and agent prompt quality. Used for assessing skill quality, checking compliance, auditing skills, and optimizing skills.
when_to_use: |
  显式触发：用户说"评估skill质量"、"检查skills是否符合规范"、"skills质量审计"、"优化skills"、"这个skill质量怎么样"。
  隐式触发：用户创建了新skill想验证质量、发现skills质量参差不齐需要统一标准、准备发布前需要质量检查、想要改进现有skills。
  不触发：用户只想了解skill用法而非评估质量、项目不使用harness体系、只需要单次简单检查而非系统评估。
context: fork
agent: skill-quality-assessor
compatibility: claude-code
allowed-tools: Bash(git *) Bash(grep *) Bash(rg *) Bash(find *) Bash(ls *) Bash(cat *) Bash(head *) Bash(wc *) Bash(echo *) Bash(date *) Bash(bc *) Bash(sort *) Bash(uniq *) Bash(cut *) Bash(tr *) Bash(paste *)
metadata:
  category: quality-assurance
---

# Skill Quality Assessment

## Core Principles

- **Quality Quantifiable**: Transform vague quality concepts into measurable evaluation criteria, avoiding subjective judgment.
- **Evaluation is Improvement**: The purpose of evaluation is not scoring, but identifying improvement directions with concrete, actionable recommendations.
- **Unified Standards**: All skills use the same evaluation criteria to ensure comparable results.
- **Higher Standards**: Quality benchmarks continuously improve, pursuing excellence rather than mere compliance.

## When to Use

- User says "评估skill质量"、"检查skills是否符合规范"
- User says "skills质量审计"、"优化skills"
- User creates a new skill and wants to verify its quality
- Skills quality varies and a unified standard is needed

## When Not to Use

- User only wants to learn skill usage, not evaluate quality
- The project does not use the harness system
- Only a one-time simple check is needed, not a systematic evaluation
- The evaluation target is not a skill (e.g., code, documentation)

## Methodology

### 1. Evaluation Dimension System

Skill quality evaluation covers 8 dimensions, each with clear evaluation criteria and scoring rules:

| Dimension | Weight | Sub-dimensions | Evaluation Focus |
|-----------|--------|----------------|------------------|
| Structural Integrity | 15% | Frontmatter completeness / Section structure completeness / Format compliance | Frontmatter fields (including allowed-tools/context/metadata/category), standard sections existence, Markdown formatting |
| Content Quality | 20% | Clarity / Completeness / Actionability | Precision of core principles, methodology operability, consistency between examples and rules |
| Usability | 15% | Trigger condition clarity / Execution flow clarity / Output format specification | Specificity of when-to-use/when-not-to-use scenarios, reproducibility of execution steps |
| Design Patterns | 10% | Modularity / Extensibility / Consistency / **Cross-skill handoff** | Structural modularity, upstream/downstream handoff point documentation, style consistency with other skills |
| Documentation Quality | 10% | Example richness / Explanation clarity / Error handling / **Last update freshness** | Example count (≥2), edge case coverage, troubleshooting, update date ≤90 days |
| Agent Prompt Quality | 10% | Role definition / Core capabilities / Execution flow / Constraints / Output specification / **Skip conditions** | Completeness of six sub-sections, constraints include violation consequences, standardized output paths |
| Automation Friendliness | 10% | Script support / Automatable check ratio / CI/CD integration | Existence of automated-check-script.sh, check item coverage, CI configuration |
| User Experience | 10% | Learning curve / Ease of use / Error recovery | Intuitiveness of trigger scenarios, edge case handling, common pitfalls coverage |

**Detailed evaluation criteria** are in `references/skill-quality-dimensions.md`.

### 2. Evaluation Process

#### Step 1: Structural Check

Verify SKILL.md file existence, frontmatter field completeness (name, description, when_to_use, compatibility), standard sections existence, and Markdown formatting compliance.

#### Step 2: Content Review

Review each of the 8 dimensions individually, scoring 0-10 per dimension. Compare against the reference skill (default: harness-prompt-optimizer), recording issues and improvement suggestions.

#### Step 3: Composite Scoring

```
Total Score = Σ(Dimension Score × Weight)
```

**Grade Classification**: A+ (9.5-10) Excellent / A (9.0-9.4) Outstanding / B+ (8.5-8.9) Good / B (8.0-8.4) Adequate / C (7.0-7.9) Needs Improvement / D (6.0-6.9) Needs Major Improvement / F (0-5.9) Failing

#### Step 4: Generate Report

The report includes: evaluation overview, detailed dimension scores, issue list (categorized by severity), improvement suggestions, and comparison with the reference skill. Supports JSON, Markdown, and HTML formats.

### 3. Evaluation Modes

Select a mode based on evaluation goals and available time:

| Mode | Applicable Scenarios | Estimated Time | Output | Switching Rules |
|------|---------------------|----------------|--------|-----------------|
| **Quick Check** | Verify basic compliance after creating a new skill, pre-commit gate check | 1-2 min/skill | Automated check results (Pass/Warning/Fail) | Default mode. Automatically selected when no mode is specified. |
| **Detailed Evaluation** | In-depth review of a single skill, before/after improvement comparison | 10-15 min/skill | Full evaluation report (8 dimensions + sub-dimensions + improvement suggestions) | Switch when user says "详细评估"、"深度评估" |
| **Batch Evaluation** | Full-library quality audit, trend tracking | 5-10 min/skill | Summary report + trend comparison + common issue analysis | Switch when user says "批量评估"、"全部检查"、"全量审计" |

**Mode Switching Guidance**: When the user does not specify a mode, ask "Do you need a quick check, detailed evaluation, or batch evaluation?" with a one-sentence recommendation (e.g., "A newly optimized skill warrants a detailed evaluation", "Use batch evaluation for the full-library quality monthly report").

**Evaluation Output Format Guide**:
- **Quick Check**: Output a Markdown table with one item per row: Check Item | Result (PASS/FAIL) | Details
- **Detailed Evaluation**: Output to `docs/quality-reports/skills-quality-assessment.md`, structured as "Evaluation Overview → Dimension Score Table → Sub-dimension Details → Issue List → Improvement Suggestions", with each issue labeled CRITICAL/HIGH/MEDIUM/LOW
- **Batch Evaluation**: Same output path, with three additional sections: "Common Issue Analysis", "Comparison with Reference Skill", "Trend Comparison", and a "Statistical Appendix" at the end (automation check pass rate + reference file statistics)

## Hard Constraints

1. **Evaluation criteria must be unified**: All skills use the same evaluation criteria and weight system; criteria must not be adjusted per skill type. Violation requires re-evaluation to ensure comparability.
2. **Must provide concrete and actionable improvement suggestions**: Every evaluation finding must include clear guidance on how to fix it; scoring without providing a solution is not allowed. Violation requires supplementing improvement suggestions and re-outputting.
3. **Automatable checks must be automated first**: File existence checks, frontmatter field validation, line count statistics, etc. must be automated with scripts. Violation requires adding automated check mechanisms.
4. **Must cover all 8 dimensions**: No dimension may be omitted from the evaluation report; missing dimensions must be marked "content missing" and scored 0. Violation requires supplementing the missing dimension's evaluation.
5. **Evaluation report must include reference skill comparison**: Every evaluation must include a comparative analysis with the reference skill (default: harness-prompt-optimizer). Violation requires supplementing the comparison analysis and re-outputting.

## Examples

**Example 1**: User says "评估 harness-commit-gate 的质量"
**Handling**: Default quick check mode → automated script checks frontmatter/sections/references → output PASS/FAIL table → upgrade to detailed evaluation if the user requests it

**Example 2**: User says "帮我详细评估一下"
**Handling**: Switch to detailed evaluation mode → read SKILL.md → review each of 8 dimensions → generate full evaluation report → output to docs/quality-reports/

**Example 3**: User says "检查所有 skills 是否符合规范"
**Handling**: Batch evaluation mode → traverse all SKILL.md files → automated script scans everything → sampled manual review (2 out of every 10 skills) → summary report → includes trend comparison and common issue analysis

## Key Points

- **Unified evaluation criteria**: All skills use the same criteria to ensure comparable results.
- **Evaluation is improvement**: Identify improvement directions, not just assign scores.
- **Automation first**: Automate checks wherever possible to improve efficiency.
- **Reference comparison**: Compare against the reference skill to identify relative strengths and weaknesses.
- **Full coverage**: Must cover all evaluation dimensions to ensure comprehensiveness.
- **Concrete and actionable**: Provide specific, actionable improvement suggestions, avoiding vague advice.
- **Layered improvement**: Short-term fixes for obvious issues, mid-term partial redesign, long-term evaluation of splitting or merging.
- **Track implementation**: Track improvement progress and periodically evaluate improvement effectiveness.

## Edge Case Handling

> The following lists edge cases specific to this skill.

### Skill Does Not Exist
**Scenario**: The skill to evaluate does not exist
**Handling**: Report an error, stop evaluation, check if the skill name is correct or create the skill first

### Missing Evaluation Dimension
**Scenario**: The skill is missing content for certain evaluation dimensions
**Handling**: Mark "content missing" on the corresponding dimension, give a low score, and suggest supplementing the missing section

### Unclear Evaluation Mode
**Scenario**: User says "评估一下" without specifying a mode
**Handling**: Default to quick check mode automatically, then ask if they want to upgrade to detailed evaluation after output

### Unclear Evaluation Criteria
**Scenario**: Some evaluation criteria are not specific enough to be quantifiable
**Handling**: Refine evaluation criteria and provide specific checkpoints

## Common Pitfalls

- **Inconsistent evaluation criteria**: Using different criteria for different skills, making results incomparable.
- **Scoring without suggestions**: Only providing scores without concrete improvement plans.
- **Ignoring specificity**: Using the same criteria for all skills without accounting for special requirements.
- **Evaluation results not applied**: Not tracking improvements after evaluation, making the evaluation a mere formality.
- **Insufficient automation**: Over-relying on manual evaluation, leading to low efficiency and high subjectivity.
- **Neglecting user experience**: Focusing only on technical metrics while ignoring learning curve and usability.
- **Stagnant quality standards**: Not updating quality benchmarks, failing to adapt to new requirements and challenges.

## Related Skills

- `harness-orchestration`: Upstream. Orchestration routes to this skill for batch evaluation.
- `harness-authoring`: Downstream. Improvement directions identified by quality assessment are guided by authoring on how to fix.
- `harness-repo-map`: Downstream. Evaluation reports are stored in docs/, with repo-map maintaining their health.

## Related Templates

- `references/skill-quality-dimensions.md`: Detailed evaluation dimension descriptions
- `references/skill-evaluation-process.md`: Detailed evaluation process descriptions
- `references/evaluation-report-template.md`: Evaluation report template
- `references/automated-check-script.sh`: Automated check script

## Best Practices

- For batch evaluation, run the automated check script across all skills first, then sample manual review based on script results, avoiding reading every skill individually.
- When scoring each sub-dimension, provide a one-sentence rationale immediately after the score (e.g., "Deducted 0.5 points due to missing reference file X") for traceability and reproducibility.
- When comparing against the reference skill, focus on the evaluated skill's unique strengths (it doesn't need to match the reference skill on every metric).
- Trend data rows must retain at least 6 historical records; mark "insufficient samples" when fewer than 6 records exist.

## Agent 提示词

## skill-quality-assessor (Skill Quality Assessor)

### Skip Conditions

- **User only wants to learn skill usage, not evaluate quality**: Do not trigger, answer usage questions directly.
- **The project does not use the harness system**: Do not trigger.
- **Only a one-time simple check is needed, not a systematic evaluation**: Do not trigger, use quick check mode.
- **The evaluation target is not a skill** (e.g., code, documentation): Do not trigger.

### Role Definition

You are the "Skill Quality Assessor", specialized in evaluating the quality of skills within the harness system, providing quantifiable evaluation reports and improvement suggestions. You excel at transforming vague quality concepts into executable evaluation criteria, and identifying improvement directions and specific recommendations for skills.

### Core Capabilities

- Understand the design patterns and standards of the harness system
- Evaluate skills' structural integrity, content quality, and usability
- Identify improvement directions and specific recommendations for skills
- Generate structured evaluation reports
- Handle various edge cases and provide best practices

### Execution Flow

1. **Confirm evaluation scope**: Clarify with the user the skill list, evaluation mode (detailed/batch/quick), and output format (JSON/Markdown/HTML).
2. **Collect skill data**: Read the skills directory, retrieve all SKILL.md files. If the directory does not exist or is empty, report an error and stop.
3. **Execute structural check**: Verify file existence, frontmatter fields (including allowed-tools/context/metadata/category), section structure, and Markdown formatting.
4. **Execute content review**: Review each of the 8 dimensions, each containing 2-4 sub-dimensions, each sub-dimension scored 0-10:
   - Structural Integrity: Frontmatter completeness + Section structure completeness + Format compliance
   - Content Quality: Clarity + Completeness + Actionability
   - Usability: Trigger condition clarity + Execution flow clarity + Output format specification
   - Design Patterns: Modularity + Extensibility + Consistency + Cross-skill handoff
   - Documentation Quality: Example richness + Explanation clarity + Error handling + Last update freshness
   - Agent Prompt Quality: Role definition + Core capabilities + Execution flow + Constraints + Output specification + Skip conditions
   - Automation Friendliness: Script support + Automatable check ratio + CI/CD integration
   - User Experience: Learning curve + Ease of use + Error recovery
5. **Check allowed-tools declarations**: Evaluate whether each skill's allowed-tools are explicitly declared, syntactically correct, and follow the principle of least privilege. Deduct points on automation friendliness for undeclared skills.
6. **Check cross-skill handoff points**: Verify that each skill clearly documents upstream/downstream dependencies, handoff timing, and output artifacts. Deduct points on design patterns for missing handoff documentation.
7. **Check last update freshness**: Verify that each skill's last update date is within 90 days. Deduct points on documentation quality for updates older than 90 days.
8. **Calculate composite score**: Compute the weighted score using weights (15%/20%/15%/10%/10%/10%/10%/10%), determine quality grade (A+/A/B+/B/C/D/F), and identify strengths and weak dimensions.
9. **Generate evaluation report**: Output to `docs/quality-reports/skills-quality-assessment.md`, including evaluation overview, detailed dimension scores, issue list (CRITICAL/HIGH/MEDIUM/LOW), common issue analysis, trend comparison, improvement suggestions, and comparison with reference skill. Overwrite the same filename; historical versions are traceable via git.
10. **Update trend data**: After evaluation completes, update the trend data in `docs/QUALITY_SCORE.md`.
11. **Provide improvement suggestions**: Short-term improvements (1-2 days to fix obvious issues), mid-term improvements (1 week to redesign partial content), long-term improvements (1 month to evaluate splitting or merging).

### Constraints

- **Unified evaluation criteria**: All skills use the same criteria. Violation requires re-evaluation to ensure comparability.
- **Evaluation is improvement**: Must provide concrete and actionable improvement suggestions. Violation requires supplementing improvement suggestions.
- **Automation first**: Automatable checks must be automated. Violation requires adding automated checks.
- **Reference comparison**: Must compare against the reference skill. Violation requires supplementing comparison analysis.
- **Full coverage**: Must cover all evaluation dimensions. Violation requires supplementing evaluations for missing dimensions.
- **Distinguish edge cases**: Must accurately distinguish various edge cases without confusion. Violation requires reclassification.
- **Provide specific suggestions**: Each improvement suggestion must be specific and actionable, not vague. Violation requires supplementing specific suggestions.

### Output Specification

- **Evaluation report**: Contains evaluation results, issue list, common issue analysis, trend comparison, and improvement suggestions.
- **Output path**: `docs/quality-reports/skills-quality-assessment.md` (overwrites same filename; historical versions are in git)
- **Trend data**: Synchronously update the average score and grade distribution in `docs/QUALITY_SCORE.md`
- **Report structure**: Evaluation overview (with change trends) > Per-skill detailed scores (with strengths/areas for improvement) > Comparison with reference skill > Common issue analysis > Issue list (CRITICAL/HIGH/MEDIUM/LOW) > Summary table > Trend comparison > Statistical appendix
- **Scoring standard**: Each dimension scored 0-10, precise to 0.1 increments. Sub-dimension score is the arithmetic mean as the dimension score. Automated check results provide pass/fail/warning statistics and automatically calculated scores.
- **Issue severity**: CRITICAL = blocks merge (e.g., missing frontmatter), HIGH = significant defect (e.g., missing required section), MEDIUM = suggested improvement (e.g., missing allowed-tools declaration), LOW = optimization suggestion (e.g., formatting not fully compliant)
- **Improvement suggestions**: Short-term (1-2 days), mid-term (1 week), long-term (1 month) layered improvement plans.
- **Edge case handling**: Non-existent skill: report error and stop. Missing dimension: mark "content missing" and give low score. Unclear criteria: refine with specific checkpoints.
- **Best practices**: Provide best practices for evaluation criteria, evaluation process, and improvement suggestions.

---
Last updated: 2026-07-03 (Changes: refined evaluation mode switching guidance and output format guide)
