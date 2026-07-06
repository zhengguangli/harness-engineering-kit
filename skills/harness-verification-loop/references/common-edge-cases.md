# General Edge Cases Reference

## Overview

This document consolidates common edge case handling approaches shared across all skills in the Harness system. Each skill should reference this document rather than duplicating definitions when handling these edge cases.

## General Edge Cases

### 1. Very Small Project

**Scenario**: The project has only a few files with no clear modular layering requirements.

**Handling Principles**:
- Simplify initialization; only create necessary files
- Skip heavyweight skills (e.g., architecture-boundaries)
- Use a simple directory structure without complex architectural constraints

**Criteria**:
- File count < 10
- Lines of code < 1000
- Development team < 3 people

### 2. Legacy Project Refactoring

**Scenario**: A legacy project has extensive architectural violations or code smells that need gradual remediation.

**Handling Principles**:
- Adopt an incremental refactoring strategy; fix severe violations first
- Do not break existing structure; update incrementally
- Preserve existing valuable content

**Refactoring Steps**:
1. Identify all violations/smells
2. Classify by severity (CRITICAL/HIGH/MEDIUM/LOW)
3. Fix CRITICAL and HIGH level issues first
4. Establish new rules to prevent new violations
5. Gradually clean up MEDIUM and LOW level issues

### 3. Multi-team Collaboration

**Scenario**: Multiple teams collaborate on development and need unified standards.

**Handling Principles**:
- Establish unified standards; each team implements freely within those standards
- Regularly audit compliance with standards
- Set up a standards review process

**Collaboration Plan**:
1. Establish a unified standards template
2. Provide customized configuration for each team
3. Regularly audit compliance with standards
4. Set up a standards review process

### 4. Missing Infrastructure

**Scenario**: The project lacks necessary test/build/lint configuration.

**Handling Principles**:
- First fill in the missing infrastructure, then start related workflows
- Report capability gaps; do not fall back to guessing by reading code
- Use fallback verification methods (e.g., static analysis)

**Fill-in Steps**:
1. Identify missing infrastructure
2. Report capability gaps
3. Suggest running harness-bootstrap first
4. Fill in configuration before starting related workflows

### 5. Goal Clarification

**Scenario**: The user's requirement description is ambiguous and the specific scope cannot be determined.

**Handling Principles**:
- First clarify the user's goal, then proceed with routing
- List as "questions to clarify"; do not make decisions for the user
- Create an execution plan only after clarification

**Clarification Method**:
1. List questions to clarify
2. Wait for user clarification
3. Execute after clarification

## Usage Guide

When each skill handles edge cases:
1. If the edge case falls under the general types above, directly reference the corresponding section of this document
2. If the edge case is skill-specific, keep and detail it in the skill's SKILL.md
3. Maintain the format for skill-specific edge cases: Scenario -> Handling Principles (1-2 lines)

---
Last updated: 2026-07-02