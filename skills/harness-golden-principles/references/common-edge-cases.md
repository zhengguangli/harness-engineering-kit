# Common Edge Cases Reference

## Overview

This document summarizes common edge case handling solutions shared across skills in the Harness ecosystem. When handling these edge cases, each skill should reference this document rather than redefine them.

## Common Edge Cases

### 1. Very Small Project

**Scenario**: The project has only a few files with no clear layering requirements between modules.

**Handling Principles**:
- Simplify initialization; only create necessary files.
- Skip heavyweight skills (e.g., architecture-boundaries).
- Use a simple directory structure without complex architectural constraints.

**Judgment Criteria**:
- File count < 10
- Lines of code < 1000
- Development team < 3 people

### 2. Legacy Project Migration

**Scenario**: A legacy project has extensive architectural violations or code smells requiring gradual improvement.

**Handling Principles**:
- Adopt an incremental migration strategy; prioritize fixing critical violations.
- Do not break the existing structure; apply incremental updates.
- Preserve existing valuable content.

**Migration Steps**:
1. Identify all violations/smells.
2. Classify by severity (CRITICAL / HIGH / MEDIUM / LOW).
3. Prioritize fixing CRITICAL and HIGH issues.
4. Establish new rules to prevent new violations.
5. Gradually clean up MEDIUM and LOW issues.

### 3. Multi-team Collaboration

**Scenario**: Multiple teams collaborate and need unified standards.

**Handling Principles**:
- Establish unified standards; each team implements freely within those standards.
- Regularly audit standard compliance.
- Establish a standard review process.

**Collaboration Approach**:
1. Create a unified standard template.
2. Provide customized configuration for each team.
3. Regularly audit standard compliance.
4. Establish a standard review process.

### 4. Missing Infrastructure

**Scenario**: The project lacks necessary test/build/lint configuration.

**Handling Principles**:
- Complete the infrastructure first, then start related processes.
- Report capability gaps instead of falling back to reading code and guessing.
- Use fallback verification methods (e.g., static analysis).

**Completion Steps**:
1. Identify missing infrastructure.
2. Report capability gaps.
3. Recommend running harness-bootstrap first.
4. Complete configuration before starting related processes.

### 5. Goal Clarification

**Scenario**: The user's description is ambiguous and the specific scope cannot be determined.

**Handling Principles**:
- Clarify user goals first, then route.
- List as "questions to clarify"; do not make decisions for the user.
- Create an execution plan after clarification.

**Clarification Method**:
1. List questions to clarify.
2. Wait for user clarification.
3. Execute after clarification.

## Usage Guide

When each skill handles edge cases:
1. If the edge case falls under the general types above, directly reference the corresponding section of this document.
2. If the edge case is skill-specific, keep it in the skill's SKILL.md with detailed explanation.
3. Maintain the format for skill-specific edge cases: Scenario → Handling Principles (1-2 lines).

---
Last updated: 2026-07-02
