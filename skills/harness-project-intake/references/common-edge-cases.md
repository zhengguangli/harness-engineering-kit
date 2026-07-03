# Common Edge Cases Reference

## Overview

This document summarizes common edge case handling approaches shared across skills in the Harness system. Each skill should reference this document instead of redefining these approaches when handling these edge cases.

## Common Edge Cases

### 1. Minimal Project Size

**Scenario**: Project has only a few files, no obvious need for modular layering

**Processing Principles**:
- Simplify initialization, create only necessary files
- Skip heavyweight skills (e.g., architecture-boundaries)
- Use a simple directory structure, no complex architecture constraints

**Judgment Criteria**:
- File count < 10
- Lines of code < 1000
- Development team < 3 people

### 2. Legacy Project Migration

**Scenario**: Legacy project with significant architecture violations or code smells requiring gradual migration

**Processing Principles**:
- Adopt incremental migration strategy, prioritize fixing critical violations
- Do not break existing structure, update incrementally
- Preserve existing valuable content

**Migration Steps**:
1. Identify all violations/smells
2. Classify by severity (CRITICAL/HIGH/MEDIUM/LOW)
3. Fix CRITICAL and HIGH level issues first
4. Establish new rules to prevent new violations
5. Gradually clean up MEDIUM and LOW level issues

### 3. Multi-Team Collaboration

**Scenario**: Multiple teams collaborating on development, requiring unified standards

**Processing Principles**:
- Establish unified standards, each team implements freely within those standards
- Regularly audit standard compliance
- Establish standard review process

**Collaboration Plan**:
1. Create unified standard templates
2. Provide customized configuration for each team
3. Regularly audit standard compliance
4. Establish standard review process

### 4. Missing Infrastructure

**Scenario**: Project lacks necessary test/build/lint configuration

**Processing Principles**:
- First fill in missing infrastructure, then start relevant processes
- Report capability gaps, do not fall back to reading code guesses
- Use alternative verification methods (e.g., static analysis)

**Remediation Steps**:
1. Identify missing infrastructure
2. Report capability gaps
3. Recommend running harness-bootstrap first
4. Fill in configuration before starting relevant processes

### 5. Goal Clarification

**Scenario**: User requirements are vague, cannot determine exact scope

**Processing Principles**:
- First clarify user goals, then route
- List as "Questions to clarify", do not decide for the user
- Create execution plan after clarification

**Clarification Method**:
1. List questions to clarify
2. Wait for user clarification
3. Execute after clarification

## Usage Guide

When each skill handles edge cases:
1. If the edge case falls under one of the general types above, directly reference the corresponding section of this document
2. If the edge case is skill-specific, keep it in the skill's SKILL.md and describe in detail
3. Maintain the skill-specific edge case format: Scenario → Processing Principles (1-2 lines)

---
Last updated: 2026-07-02
