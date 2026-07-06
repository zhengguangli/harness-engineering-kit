# Common Edge Cases Reference

## Overview

This document summarizes the common edge case handling approaches shared across skills in the Harness system. When handling these edge cases, each skill should reference this document rather than redefining them.

## Common Edge Cases

### 1. Very Small Project

**Scenario**: The project has only a few files, with no obvious need for modular layering.

**Handling Principles**:
- Simplify initialization; only create necessary files
- Skip heavyweight skills (e.g., architecture-boundaries)
- Use a simple directory structure; no need for complex architectural constraints

**Thresholds**:
- File count < 10
- Lines of code < 1000
- Development team < 3 people

### 2. Legacy Project Migration

**Scenario**: Legacy project has numerous architectural violations or code smells requiring gradual migration.

**Handling Principles**:
- Adopt incremental migration strategy; prioritize fixing critical violations
- Do not break existing structure; make incremental updates
- Preserve existing valuable content

**Migration Steps**:
1. Identify all violations/smells
2. Classify by severity (CRITICAL/HIGH/MEDIUM/LOW)
3. Prioritize fixing CRITICAL and HIGH issues
4. Establish new rules to prevent new violations
5. Gradually clean up MEDIUM and LOW issues

### 3. Multi-Team Collaboration

**Scenario**: Multiple teams collaborating on development, requiring unified standards.

**Handling Principles**:
- Establish unified standards; each team implements freely within them
- Regularly audit standards compliance
- Establish a standards review process

**Collaboration Plan**:
1. Create unified standard templates
2. Provide customized configuration for each team
3. Regularly audit standards compliance
4. Establish a standards review process

### 4. Missing Infrastructure

**Scenario**: Project lacks necessary test/build/lint configuration.

**Handling Principles**:
- Fill infrastructure gaps first, then proceed with related workflows
- Report capability gaps, do not fall back to guessing from code
- Use fallback verification methods (e.g., static analysis)

**Remediation Steps**:
1. Identify missing infrastructure
2. Report capability gaps
3. Recommend running harness-bootstrap first
4. Proceed with related workflows after filling configuration gaps

### 5. Goal Clarification

**Scenario**: User's requirements are vague, making it impossible to determine the specific scope.

**Handling Principles**:
- Clarify the user's goal first, then route to appropriate skills
- List "clarification questions" rather than making decisions for the user
- Create an execution plan only after clarification

**Clarification Method**:
1. List clarification questions
2. Wait for user response
3. Proceed only after clarification

## Usage Guide

When each skill handles edge cases:
1. If the edge case belongs to the common types above, directly reference the corresponding section of this document
2. If the edge case is skill-specific, retain it in the skill's SKILL.md with detailed explanation
3. Keep skill-specific edge case format: Scenario -> Handling Principles (1-2 lines)

---
Last updated: 2026-07-02
