# Common Edge Cases Reference

## Overview

This document summarizes shared edge case handling solutions across all skills in the Harness framework. Each skill should reference this document when handling these edge cases rather than redefining them.

## Common Edge Cases

### 1. Extremely Small Project

**Scenario**: The project only has a few files with no clear need for module layering

**Handling Principles**:
- Simplify initialization, only create necessary files
- Skip heavyweight skills (e.g., architecture-boundaries)
- Use a simple directory structure, no complex architecture constraints needed

**Judgment Criteria**:
- File count < 10
- Lines of code < 1000
- Development team < 3 people

### 2. Legacy Project Refactoring

**Scenario**: Legacy project has extensive architecture violations or code smells that need gradual improvement

**Handling Principles**:
- Adopt an incremental refactoring strategy, prioritize fixing severe violations
- Don't break existing structure, update incrementally
- Preserve existing valuable content

**Refactoring Steps**:
1. Identify all violations/smells
2. Classify by severity (CRITICAL/HIGH/MEDIUM/LOW)
3. Prioritize fixing CRITICAL and HIGH level issues
4. Establish new rules to prevent new violations
5. Gradually clean up MEDIUM and LOW level issues

### 3. Multi-Team Collaboration

**Scenario**: Multiple teams collaborating on development, need unified standards

**Handling Principles**:
- Establish unified standards, each team implements freely within those standards
- Conduct regular audits of standard compliance
- Establish a standard review process

**Collaboration Plan**:
1. Create a unified standard template
2. Provide customized configuration per team
3. Conduct regular audits of standard compliance
4. Establish a standard review process

### 4. Missing Infrastructure

**Scenario**: Project lacks necessary test/build/lint configuration

**Handling Principles**:
- Complete the infrastructure first, then start related processes
- Report capability gaps, don't fall back to reading code guessing
- Use alternative verification methods (e.g., static analysis)

**Completion Steps**:
1. Identify missing infrastructure
2. Report capability gaps
3. Suggest running harness-bootstrap first
4. Complete configuration before starting related processes

### 5. Goal Clarification

**Scenario**: User's requirements are vague, unable to determine specific scope

**Handling Principles**:
- Clarify the user's goal first, then route
- List questions as "Items to clarify", don't make decisions for the user
- Create an execution plan after clarification

**Clarification Method**:
1. List questions to clarify
2. Wait for user clarification
3. Execute after clarification

## Usage Guide

When each skill handles edge cases:
1. If the edge case falls under the above general types, directly reference the corresponding section of this document
2. If the edge case is skill-specific, keep it in the skill's SKILL.md and explain in detail
3. Maintain the skill-specific edge case format: Scenario → Handling Principles (1-2 lines)

---
Last updated: 2026-07-02
