# Common Edge Cases Reference Document

## Overview

This document summarizes common edge cases encountered when processing with the Skill Quality Assessor. Reference this document to avoid redundant definitions in SKILL.md.

## Common Edge Cases

### 1. Minimal Skill Evaluation (file lines < 80)

**Scenario**: The evaluated skill file has very few lines (< 80 lines), with concise content

**Handling Principles**:
- Do not automatically deduct points for fewer lines
- Evaluate whether fewer lines means "sufficient" or "missing"
- If the concise structure is complete and core information is comprehensive, structure completeness can still score high
- Deductions should focus on content quality and documentation quality dimensions

**Judgment Criteria**:
- Lines < 80: Enable streamlined evaluation mode
- Lines 80-150: Standard mode
- Lines > 150: Detailed mode (full 8-dimension evaluation)

### 2. Newly Created Skill

**Scenario**: The evaluated skill was recently created (last update date < 3 days ago)

**Handling Principles**:
- Appropriately reduce the weighting for reference file count (references may be incomplete when newly created)
- Focus evaluation on: structure completeness, agent prompt quality, core principles
- Label as "New Skill" to indicate that subsequent evaluations may improve as content becomes more substantial

### 3. Skill Type is disable-model-invocation

**Scenario**: The evaluated skill has `disable-model-invocation: true` (requires subagent invocation)

**Handling Principles**:
- Shift the evaluation focus of agent prompt quality from "can it be used directly" to "can it be correctly understood by the subagent"
- Slightly deduct automation friendliness points (requires additional steps to invoke)
- Mark "disable-model-invocation" in the evaluation report to explain scores in certain dimensions

### 4. Large Score Fluctuation (standard deviation > 1.0)

**Scenario**: The same skill's score varies by more than 1.0 points across different evaluation rounds

**Handling Principles**:
- Check if there were evaluation standard changes (e.g., weight adjustments, new dimensions)
- Check if there were substantial content changes (e.g., removal/addition of large sections)
- Note the reason for fluctuation in trend comparisons
- Fluctuations with valid justifications are not considered issues

### 5. Skill Has No references/ Directory

**Scenario**: The evaluated skill has no references/ directory or the directory is empty

**Handling Principles**:
- Significantly deduct points in the documentation quality dimension (50% of this dimension's weight relates to reference files)
- Cap the total score at B grade
- Recommend immediately supplementing reference files in the evaluation report

### 6. Self-Evaluation Conflict

**Scenario**: Skill Quality Assessor evaluating itself (self-evaluation)

**Handling Principles**:
- Still execute the full evaluation process
- Mark "self-evaluation" in the report
- Score serves as a reference value, not a final quality conclusion
- Recommend cross-validation with other skills (e.g., prompt-optimizer)

## Usage Guide

Skill Quality Assessor specific edge cases are written directly in this document. When handling edge cases:
1. If it is a general type, reference the corresponding section of this document
2. Follow the format: Scenario -> Handling Principles (1-2 lines)

---
Last updated: 2026-07-03
