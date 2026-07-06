# Common Edge Cases Reference

## Overview

This document consolidates common edge cases encountered during Commit Gate processing. Reference this document to avoid redefining them in SKILL.md.

## Common Edge Cases

### 1. No Changes to Commit

**Scenario**: Working directory is clean, no pending changes to commit

**Handling Principle**:
- Check git status to confirm no changes
- Report "Working directory clean, nothing to commit"
- Do not run any check process

**Criteria**:
- `git status --porcelain` output is empty
- Both `git diff --stat` and `git diff --cached --stat` are empty

### 2. Large-Scale Changes (> 20 files or > 500 changed lines)

**Scenario**: A single commit contains a large number of file changes; running the full gate process file-by-file takes too long

**Handling Principle**:
- First determine if it is a single intent (refactoring, bulk formatting, dependency upgrades, etc.)
- Single intent: run critical checks together (lint + type check + tests), do not inspect each diff individually
- Mixed intent: suggest splitting into multiple commits, each focused on a single change intent
- If necessary, allow the user to bypass the gate

### 3. Legacy Project First-Time Commit

**Scenario**: Running commit gate for the first time on a legacy project with many pre-existing lint/type/test issues

**Handling Principle**:
- Distinguish between pre-existing issues and newly introduced issues
- Only block newly introduced issues; pre-existing issues are logged in tech-debt-tracker
- Clearly label in the report which issues are pre-existing and which are new

**Differentiation Method**:
1. First run lint/type check/tests before committing, recording pre-existing failures
2. Apply changes and run again, reporting only new failures

### 4. Missing Build/Test Infrastructure

**Scenario**: The project lacks the minimum required check configuration (e.g., no lint config, no test framework)

**Handling Principle**:
- Report capability gaps (explicitly list missing configuration items)
- Suggest running harness-bootstrap first to fill in the infrastructure
- Do not force-block the commit (allow skipping checks corresponding to missing items)
- Note in the report "Skipping Y check due to missing X configuration"

### 5. Non-Code File Changes

**Scenario**: The commit only contains non-code files such as documentation, configuration files, images, etc.

**Handling Principle**:
- Skip code quality checks (lint, type check, tests)
- Trigger documentation/configuration consistency checks (if any)
- If CLAUDE.md is changed, trigger repo-map related checks

**Criteria**:
- All changed files are in non-source extensions such as `docs/`, `*.md`, `*.json`, `*.yaml`, `*.png`, etc.

### 6. Emergency Fix Bypass

**Scenario**: An urgent production issue requires immediate fix and cannot wait for the full gate process

**Handling Principle**:
- The user must explicitly state the reason for the emergency bypass
- Record the bypass reason in the commit message under a `Hotfix:` prefix
- Require running the gate process post-fix (create a follow-up task)
- Do not allow more than 3 consecutive emergency bypasses

### 7. Sensitive Information Detection

**Scenario**: Changes contain suspected sensitive information (keys, tokens, passwords, internal network addresses)

**Handling Principle**:
- Block the commit and list the locations of suspected sensitive information
- Suggest using environment variables or a secrets management service instead
- If it is a fake key for testing, annotate it with `[test-key]` in the commit message
- If it is an internal network address, annotate it with `[internal]`

## Usage Guide

Commit Gate-specific edge cases are written directly in this file. When handling edge cases:
1. If it is a common type, reference the corresponding section in this document
2. Follow the format: Scenario → Handling Principle (1-2 lines)

---
Last updated: 2026-07-03
