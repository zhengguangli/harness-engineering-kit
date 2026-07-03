# Common Edge Cases Reference Document

## Overview

This document aggregates common edge case handling strategies shared across skills in the Harness system. Each skill should reference this document rather than redefining these patterns.

## Common Edge Cases

### 1. Very Small Project Scale

**Scenario**: The project has only a few files with no obvious layering needs

**Principles**:
- Simplify initialization, create only necessary files
- Skip heavyweight skills (e.g., architecture-boundaries)
- Use a simple directory structure without complex architecture constraints

**Judgment Criteria**:
- Fewer than 10 files
- Fewer than 1000 lines of code
- Development team of fewer than 3 people

### 2. Legacy Project Refactoring

**Scenario**: Legacy project with extensive architecture violations or code smells that need gradual improvement

**Principles**:
- Adopt an incremental refactoring strategy, prioritizing severe violations
- Do not break existing structure; update incrementally
- Preserve existing valuable content

**Refactoring Steps**:
1. Identify all violations/smells
2. Categorize by severity (CRITICAL/HIGH/MEDIUM/LOW)
3. Fix CRITICAL and HIGH level issues first
4. Establish new rules to prevent additional violations
5. Gradually clean up MEDIUM and LOW level issues

### 3. Multi-Team Collaboration

**Scenario**: Multiple teams collaborating on development, requiring unified standards

**Principles**:
- Establish unified standards, allowing teams freedom within those standards
- Regularly audit compliance with standards
- Establish a standards review process

**Collaboration Plan**:
1. Create a unified standards template
2. Provide customized configuration for each team
3. Regularly audit compliance with standards
4. Establish a standards review process

### 4. Missing Infrastructure

**Scenario**: Project lacks necessary test/build/lint configuration

**Principles**:
- Fill in infrastructure gaps first, then start relevant workflows
- Report capability gaps rather than falling back to reading code guesses
- Use fallback verification methods (e.g., static analysis)

**Filling Steps**:
1. Identify missing infrastructure
2. Report capability gaps
3. Suggest running harness-bootstrap first
4. Fill in configuration before starting relevant workflows

### 5. Goal Clarification

**Scenario**: User's description is ambiguous, unable to determine specific scope

**Principles**:
- Clarify user goals before routing
- List as "questions to clarify", do not decide for the user
- Create execution plan only after clarification

**Clarification Method**:
1. List questions to clarify
2. Wait for user clarification
3. Execute after clarification

## Usage Guide

When handling edge cases in each skill:
1. If the edge case falls under the common types above, directly reference the corresponding section of this document
2. If the edge case is skill-specific, keep it in the skill's SKILL.md with detailed explanation
3. Keep skill-specific edge case format: scenario -> principles (1-2 lines)

---
Last updated: 2026-07-02
