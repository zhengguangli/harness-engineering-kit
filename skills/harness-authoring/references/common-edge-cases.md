# Common Edge Cases Reference

## Overview

This document summarizes the common edge case handling approaches shared across all skills in the Harness ecosystem. Each skill should reference this document when handling these edge cases rather than redefining them.

## Common Edge Cases

### 1. Extremely Small Projects

**Scenario**: The project has only a few files with no obvious layering needs between modules

**Handling Principles**:
- Simplify initialization; only create necessary files
- Skip heavyweight skills (e.g., architecture-boundaries)
- Use a simple directory structure without complex architectural constraints

**Criteria**:
- File count < 10
- Code lines < 1000
- Development team < 3 people

### 2. Legacy Project Migration

**Scenario**: Legacy projects with extensive architectural violations or code smells that need incremental improvement

**Handling Principles**:
- Adopt an incremental migration strategy, prioritizing severe violations first
- Do not break existing structure; apply incremental updates
- Preserve existing valuable content

**Migration Steps**:
1. Identify all violations/smells
2. Categorize by severity (CRITICAL/HIGH/MEDIUM/LOW)
3. Fix CRITICAL and HIGH level issues first
4. Establish new rules to prevent new violations
5. Gradually clean up MEDIUM and LOW level issues

### 3. Multi-Team Collaboration

**Scenario**: Multiple teams collaborating on development, needing unified standards

**Handling Principles**:
- Establish unified standards, allowing each team to implement freely within those standards
- Regularly audit standard compliance
- Set up a standard review process

**Collaboration Plan**:
1. Establish unified standard templates
2. Provide customized configuration for each team
3. Regularly audit standard compliance
4. Set up a standard review process

### 4. Missing Infrastructure

**Scenario**: The project lacks necessary test/build/lint configuration

**Handling Principles**:
- First fill in the infrastructure gaps, then start related processes
- Report capability gaps rather than falling back to guessing from reading code
- Use fallback verification methods (e.g., static analysis)

**Remediation Steps**:
1. Identify missing infrastructure
2. Report capability gaps
3. Suggest running harness-bootstrap first
4. Fill in configuration before starting related processes

### 5. Goal Clarification

**Scenario**: The user's requirements are vague, making it impossible to determine the specific scope

**Handling Principles**:
- First clarify the user's goal, then route accordingly
- Use "Questions to clarify" list; do not make decisions on behalf of the user
- Create an execution plan only after clarification

**Clarification Method**:
1. List questions needing clarification
2. Wait for user to clarify
3. Execute after clarification

## Usage Guide

When each skill handles edge cases:
1. If the edge case falls under the common types above, directly reference the corresponding section of this document
2. If the edge case is skill-specific, keep and detail it in the skill's SKILL.md
3. Maintain the skill-specific edge case format: Scenario → Handling Principles (1-2 lines)

---
Last updated: 2026-07-02
