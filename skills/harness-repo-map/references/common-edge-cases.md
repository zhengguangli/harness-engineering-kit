# Common edge cases reference

## Overview

This document consolidates common edge case handling approaches shared across skills in the Harness system. When handling these edge cases, skills should reference this document rather than redefining them.

## Common edge cases

### 1. Very small project

**Scenario**: The project has only a few files with no clear need for modular layering

**Handling principles**:
- Simplify initialization, only create necessary files
- Skip heavyweight skills (e.g., architecture-boundaries)
- Use a simple directory structure without complex architecture constraints

**Criteria**:
- File count < 10
- Lines of code < 1000
- Development team < 3 people

### 2. Legacy project migration

**Scenario**: A legacy project has extensive architecture violations or code smells that need gradual remediation

**Handling principles**:
- Adopt an incremental migration strategy, prioritize fixing critical violations
- Don't break existing structure, update incrementally
- Preserve existing valuable content

**Migration steps**:
1. Identify all violations/smells
2. Classify by severity (CRITICAL/HIGH/MEDIUM/LOW)
3. Prioritize fixing CRITICAL and HIGH issues
4. Establish new rules to prevent new violations
5. Gradually clean up MEDIUM and LOW issues

### 3. Multi-team collaboration

**Scenario**: Multiple teams collaborating on development need unified standards

**Handling principles**:
- Establish unified standards, with each team free to implement within them
- Regularly audit standards compliance
- Set up a standards review process

**Collaboration approach**:
1. Create a unified standard template
2. Provide customized configuration for each team
3. Regularly audit standards compliance
4. Set up a standards review process

### 4. Missing infrastructure

**Scenario**: The project lacks necessary test/build/lint configuration

**Handling principles**:
- Fill in the missing infrastructure first, then proceed with related workflows
- Report capability gaps rather than falling back to reading code and guessing
- Use alternative verification methods (e.g., static analysis)

**Remediation steps**:
1. Identify missing infrastructure
2. Report capability gaps
3. Suggest running harness-bootstrap first
4. Fill in configuration before proceeding with related workflows

### 5. Goal clarification

**Scenario**: The user's requirements are vague and the specific scope cannot be determined

**Handling principles**:
- Clarify the user's goal before routing
- List as "questions to clarify" rather than making decisions for the user
- Create an execution plan after clarification

**Clarification method**:
1. List questions to clarify
2. Wait for user clarification
3. Proceed after clarification

## Usage guide

When handling edge cases, each skill should:
1. If the edge case falls under the above common types, directly reference the corresponding section of this document
2. If the edge case is skill-specific, keep it in the skill's SKILL.md and describe it in detail
3. Maintain the format for skill-specific edge cases: Scenario → Handling principles (1-2 lines)

---
Last updated: 2026-07-02
