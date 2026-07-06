# Common Boundary Cases Reference

## Overview

This document summarizes shared common boundary case handling approaches across all skills in the Harness system. When handling these boundary cases, each skill should reference this document rather than redefining them.

## Common Boundary Cases

### 1. Very Small Project Size

**Scenario**: Project has only a few files with no clear layering requirements between modules

**Handling Principles**:
- Simplify initialization, only create necessary files
- Skip heavyweight skills (e.g., architecture-boundaries)
- Use simple directory structure, no complex architecture constraints needed

**Criteria**:
- File count < 10
- Lines of code < 1000
- Development team < 3 people

### 2. Legacy Project Migration

**Scenario**: Legacy project has extensive architecture violations or code smells, requiring incremental migration

**Handling Principles**:
- Adopt incremental migration strategy, fix critical violations first
- Don't break existing structure, make additive changes
- Preserve existing valuable content

**Migration Steps**:
1. Identify all violations/smells
2. Classify by severity (CRITICAL/HIGH/MEDIUM/LOW)
3. Fix CRITICAL and HIGH priority issues first
4. Establish new rules to prevent new violations
5. Gradually clean up MEDIUM and LOW priority issues

### 3. Multi-team Collaboration

**Scenario**: Multiple teams collaborating on development, need unified standards

**Handling Principles**:
- Establish unified standards, each team implements freely within those standards
- Regularly audit compliance with standards
- Establish a standards review process

**Collaboration Plan**:
1. Create unified standard templates
2. Provide customized configuration for each team
3. Regularly audit compliance with standards
4. Establish a standards review process

### 4. Missing Infrastructure

**Scenario**: Project lacks necessary test/build/lint configuration

**Handling Principles**:
- Fill in infrastructure gaps first, then start related processes
- Report capability gaps, don't fall back to reading code and guessing
- Use fallback verification methods (e.g., static analysis)

**Remediation Steps**:
1. Identify missing infrastructure
2. Report capability gaps
3. Suggest running harness-bootstrap first
4. Fill in configuration before starting related processes

### 5. Goal Clarification

**Scenario**: User's requirements are vague, specific scope cannot be determined

**Handling Principles**:
- Clarify user goals first, then route
- List as "Questions to clarify", don't make decisions for the user
- Create execution plan after clarification

**Clarification Method**:
1. List questions to clarify
2. Wait for user clarification
3. Execute after clarification

## Usage Guide

When each skill handles boundary cases:
1. If the boundary case falls under the above common types, directly reference the corresponding section of this document
2. If the boundary case is skill-specific, keep it in the skill's SKILL.md with detailed explanation
3. Keep skill-specific boundary case format: Scenario → Handling Principles (1-2 lines)

---
Last updated: 2026-07-02
