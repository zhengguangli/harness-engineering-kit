# Common Edge Cases Reference Document

## Overview

This document summarizes common edge case handling approaches shared across all skills in the Harness system. Skills should reference this document rather than redefining these approaches when handling edge cases.

## Common Edge Cases

### 1. Very Small Projects

**Scenario**: The project has only a few files, with no clear need for modular layering

**Handling Principles**:
- Simplify initialization, only create necessary files
- Skip heavyweight skills (e.g., architecture-boundaries)
- Use a simple directory structure without complex architecture constraints

**Criteria**:
- Fewer than 10 files
- Fewer than 1000 lines of code
- Development team smaller than 3 people

### 2. Legacy Project Refactoring

**Scenario**: A legacy project has extensive architecture violations or code smells that need gradual refactoring

**Handling Principles**:
- Adopt an incremental refactoring strategy, prioritizing severe violations
- Do not break existing structure, update incrementally
- Preserve existing valuable content

**Refactoring Steps**:
1. Identify all violations/smells
2. Classify by severity (CRITICAL/HIGH/MEDIUM/LOW)
3. Prioritize fixing CRITICAL and HIGH issues
4. Establish new rules to prevent new violations
5. Gradually clean up MEDIUM and LOW issues

### 3. Multi-Team Collaboration

**Scenario**: Multiple teams collaborating on development need unified standards

**Handling Principles**:
- Establish unified standards, allowing each team freedom within those standards
- Regularly audit standards compliance
- Establish a standards review process

**Collaboration Plan**:
1. Create unified standards templates
2. Provide customized configuration for each team
3. Regularly audit standards compliance
4. Establish a standards review process

### 4. Missing Infrastructure

**Scenario**: The project lacks necessary test/build/lint configuration

**Handling Principles**:
- Fill in infrastructure gaps first, then start related processes
- Report capability gaps rather than falling back to reading code and guessing
- Use alternative verification methods (e.g., static analysis)

**Remediation Steps**:
1. Identify missing infrastructure
2. Report capability gaps
3. Recommend running harness-bootstrap first
4. Fill in configuration before starting related processes

### 5. Goal Clarification

**Scenario**: The user's description of requirements is vague, making it impossible to determine the specific scope

**Handling Principles**:
- Clarify the user's goal first, then route
- List as "questions to clarify" without making decisions for the user
- Create an execution plan only after clarification

**Clarification Method**:
1. List questions to clarify
2. Wait for user response
3. Proceed after clarification

## Usage Guide

When handling edge cases, each skill should:
1. If the edge case falls under the above common types, directly reference this document's corresponding section
2. If the edge case is unique to the skill, keep it in the skill's SKILL.md with detailed explanation
3. Maintain the edge case format: Scenario → Handling Principles (1-2 lines)

---
Last updated: 2026-07-02