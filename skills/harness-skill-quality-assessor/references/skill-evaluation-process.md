# Skills Quality Assessment Process Detailed Description

Update time: 2026-07-02
Updated by: claude-code

## Evaluation Process Overview

This process defines how to systematically evaluate the quality of skills in the harness system, including both automated checks and manual review.

## Evaluation Preparation

### 1. Environment Preparation

**Required Tools**:
- File system access permissions
- Markdown parser
- JSON processing capability

**Evaluation Data**:
- SKILL.md file to be evaluated
- Reference skill (default: harness-prompt-optimizer)
- Evaluation dimension system (see `skill-quality-dimensions.md`)

### 2. Evaluation Input

**Required Input**:
- `skills_directory`: Path to the skills directory
- `target_skill`: Name of the skill to evaluate

**Optional Input**:
- `reference_skill`: Reference skill name (default: harness-prompt-optimizer)
- `evaluation_mode`: Evaluation mode (Detailed/Summary/Scorecard)
- `output_format`: Output format (JSON/Markdown/HTML)

## Automated Check Process

### Step 1: File Structure Validation

**Check Items**:
1. Check whether SKILL.md file exists
2. Check whether file is readable
3. Check file encoding (UTF-8)

**Check Commands**:
```bash
# Check file existence
test -f skills/<skill-name>/SKILL.md && echo "File exists" || echo "File does not exist"

# Check file readability
test -r skills/<skill-name>/SKILL.md && echo "File is readable" || echo "File is not readable"

# Check file encoding
file -I skills/<skill-name>/SKILL.md
```

**Scoring Rules**:
- File exists and is readable: +2 points
- File encoding is correct (UTF-8): +1 point

### Step 2: Frontmatter Validation

**Check Items**:
1. Whether frontmatter exists
2. Required field completeness
3. Field format correctness

**Check Commands**:
```bash
# Extract frontmatter
sed -n '/^---$/,/^---$/p' skills/<skill-name>/SKILL.md

# Check required fields
grep -q "^name:" skills/<skill-name>/SKILL.md && echo "name field exists" || echo "name field missing"
grep -q "^description:" skills/<skill-name>/SKILL.md && echo "description field exists" || echo "description field missing"
grep -q "^when_to_use:" skills/<skill-name>/SKILL.md && echo "when_to_use field exists" || echo "when_to_use field missing"
grep -q "^compatibility:" skills/<skill-name>/SKILL.md && echo "compatibility field exists" || echo "compatibility field missing"
```

**Scoring Rules**:
- Frontmatter exists: +1 point
- name field exists and is not empty: +1 point
- description field exists and >= 20 characters: +1 point
- when_to_use field exists and is not empty: +1 point
- compatibility field exists and is not empty: +1 point

### Step 3: Section Structure Validation

**Check Items**:
1. Whether standard sections exist
2. Whether section hierarchy is correct
3. Whether section content is empty

**Check Commands**:
```bash
# Check standard sections
grep -q "^## Core Principles" skills/<skill-name>/SKILL.md && echo "Core Principles section exists" || echo "Core Principles section missing"
grep -q "^## When to Use" skills/<skill-name>/SKILL.md && echo "When to Use section exists" || echo "When to Use section missing"
grep -q "^## When Not to Use" skills/<skill-name>/SKILL.md && echo "When Not to Use section exists" || echo "When Not to Use section missing"
grep -q "^## Methodology" skills/<skill-name>/SKILL.md && echo "Methodology section exists" || echo "Methodology section missing"
grep -q "^## Key Points" skills/<skill-name>/SKILL.md && echo "Key Points section exists" || echo "Key Points section missing"
grep -q "^## Common Pitfalls" skills/<skill-name>/SKILL.md && echo "Common Pitfalls section exists" || echo "Common Pitfalls section missing"
```

**Scoring Rules**:
- Each standard section exists: +0.5 points (max 3 points)
- Section hierarchy correct: +1 point
- Section content not empty: +1 point

### Step 4: Markdown Format Validation

**Check Items**:
1. Whether heading hierarchy is correct
2. Whether list format is standard
3. Whether code block format is correct
4. Whether link format is correct

**Check Commands**:
```bash
# Check heading hierarchy
grep -n "^#" skills/<skill-name>/SKILL.md | head -10

# Check list format
grep -n "^- " skills/<skill-name>/SKILL.md | head -10

# Check code blocks
grep -n "^```" skills/<skill-name>/SKILL.md | head -10
```

**Scoring Rules**:
- Heading hierarchy correct: +1 point
- List format standard: +0.5 points
- Code block format correct: +0.5 points
- Link format correct: +0.5 points

### Step 5: Automation Script Support Check

**Check Items**:
1. Whether an automated check script is provided
2. Whether the script is executable
3. Whether the script covers key checkpoints

**Check Commands**:
```bash
# Check for automation script
test -f scripts/quality_check.py && echo "Automation script exists" || echo "Automation script does not exist"

# Check script executability
test -x scripts/quality_check.py && echo "Script is executable" || echo "Script is not executable"
```

**Scoring Rules**:
- Provides automation script: +2 points
- Script is executable: +1 point
- Script covers key checkpoints: +2 points

### Step 6: CI/CD Integration Check

**Check Items**:
1. Whether CI/CD integration is supported
2. Whether CI/CD configuration examples are provided
3. Whether automated report generation is supported

**Check Commands**:
```bash
# Check CI/CD configuration
test -f .github/workflows/quality-check.yml && echo "CI/CD configuration exists" || echo "CI/CD configuration does not exist"
```

**Scoring Rules**:
- Supports CI/CD integration: +2 points
- Provides CI/CD configuration example: +1 point
- Supports automated report generation: +2 points

## Manual Review Process

### Review 1: Content Quality Review

**Review Criteria**:
1. Core principles are clear and specific
2. Methodology steps are detailed and actionable
3. Examples and use cases are specific and practical
4. No ambiguous expressions
5. No redundant information

**Review Method**:
1. Read the core principles section
2. Evaluate the executability of the methodology
3. Check the practicality of examples
4. Identify ambiguity and redundancy

**Scoring Rules**:
- Excellent (9.5-10): Content is perfectly clear, complete, and directly executable
- Great (9.0-9.4): Content is excellent, clear, complete, and executable
- Good (8.5-8.9): Content is basically clear and complete
- Adequate (8.0-8.4): Content is partially clear, has some ambiguity
- Fair (7.0-7.9): Content is vague, difficult to execute
- Poor (6.0-6.9): Content is confusing, unusable
- Failing (0-5.9): Content is completely unusable

### Review 2: Usability Review

**Review Criteria**:
1. Trigger conditions are clear and specific
2. Execution process is clear
3. Output format is standard
4. Usage examples are specific

**Review Method**:
1. Evaluate the specificity of "When to Use" scenarios
2. Evaluate the clarity of "When Not to Use" scenarios
3. Evaluate the clarity of the execution process
4. Evaluate the standardization of output format

**Scoring Rules**:
- Excellent (9.5-10): Trigger conditions are perfectly clear, execution process is clear, output format is standard
- Great (9.0-9.4): Trigger conditions are clear, execution process is clear, output format is standard
- Good (8.5-8.9): Basically usable, some aspects could be optimized
- Adequate (8.0-8.4): Usable but has confusing points
- Fair (7.0-7.9): Difficult to use, requires a lot of guessing
- Poor (6.0-6.9): Almost unusable
- Failing (0-5.9): Completely unusable

### Review 3: Design Pattern Review

**Review Criteria**:
1. Follows harness system design patterns
2. Structure is clearly modular
3. Allows for future extension
4. Consistent with other skills' style

**Review Method**:
1. Compare design patterns with the reference skill
2. Evaluate the degree of modularity in the structure
3. Evaluate extensibility
4. Evaluate consistency with other skills

**Scoring Rules**:
- Excellent (9.5-10): Perfect design, clear modularity, extensible, highly consistent
- Great (9.0-9.4): Excellent design, clear modularity, extensible, highly consistent
- Good (8.5-8.9): Good design, basically follows system design patterns
- Adequate (8.0-8.4): Average design, partially follows system design patterns
- Fair (7.0-7.9): Poor design, inconsistent with system design patterns
- Poor (6.0-6.9): Confusing design, no modularity
- Failing (0-5.9): Design completely unusable

### Review 4: Documentation Quality Review

**Review Criteria**:
1. Example richness
2. Explanation clarity
3. Error handling guidance
4. Troubleshooting suggestions

**Review Method**:
1. Count the number of examples
2. Evaluate explanation clarity
3. Check error handling guidance
4. Check troubleshooting suggestions

**Scoring Rules**:
- Excellent (9.5-10): Perfect documentation, rich examples, clear explanations, includes error handling
- Great (9.0-9.4): Excellent documentation, rich examples, clear explanations, includes error handling
- Good (8.5-8.9): Good documentation, basically sufficient
- Adequate (8.0-8.4): Average documentation, missing some examples or explanations
- Fair (7.0-7.9): Poor documentation, difficult to understand
- Poor (6.0-6.9): Barely any documentation
- Failing (0-5.9): No documentation at all

### Review 5: Agent Prompt Quality Review

**Review Criteria**:
1. Role definition is clear
2. Core capabilities are clear
3. Execution process is detailed
4. Constraints are reasonable
5. Output specification is clear

**Review Method**:
1. Evaluate the clarity of role definition
2. Evaluate the clarity of core capabilities
3. Evaluate the detail of the execution process
4. Evaluate the reasonableness of constraints
5. Evaluate the clarity of output specifications

**Scoring Rules**:
- Excellent (9.5-10): Perfect agent prompt, clear role, clear process, reasonable constraints
- Great (9.0-9.4): Excellent agent prompt, clear role, clear process, reasonable constraints
- Good (8.5-8.9): Good agent prompt, basically usable
- Adequate (8.0-8.4): Average agent prompt, has confusing points
- Fair (7.0-7.9): Poor agent prompt, difficult to execute
- Poor (6.0-6.9): Barely any agent prompt
- Failing (0-5.9): No agent prompt at all

### Review 6: Automation Friendliness Review

**Review Criteria**:
1. Degree of automated checkability
2. Script support
3. CI/CD integration

**Review Method**:
1. Evaluate the proportion of items that can be automated
2. Check the completeness of automation scripts
3. Evaluate the level of CI/CD integration support

**Scoring Rules**:
- Excellent (9.5-10): Fully automated, complete scripts provided, CI/CD integration supported
- Great (9.0-9.4): Highly automated, complete scripts provided, CI/CD integration supported
- Good (8.5-8.9): Mostly automatable, basic scripts provided
- Adequate (8.0-8.4): Partially automatable, scripts incomplete
- Fair (7.0-7.9): Low automation, missing scripts
- Poor (6.0-6.9): Almost impossible to automate
- Failing (0-5.9): Completely impossible to automate

### Review 7: User Experience Review

**Review Criteria**:
1. Learning curve
2. Ease of use
3. Error recovery capability

**Review Method**:
1. Evaluate the steepness of the learning curve
2. Evaluate ease of use
3. Evaluate error recovery capability

**Scoring Rules**:
- Excellent (9.5-10): Gentle learning curve, easy to use, strong error recovery
- Great (9.0-9.4): Gentle learning curve, easy to use, strong error recovery
- Good (8.5-8.9): Moderate learning curve, fairly easy to use, fairly strong error recovery
- Adequate (8.0-8.4): Steeper learning curve, average ease of use, average error recovery
- Fair (7.0-7.9): Steep learning curve, inconvenient to use, weak error recovery
- Poor (6.0-6.9): Very steep learning curve, very inconvenient, almost no error recovery
- Failing (0-5.9): Completely unusable

## Evaluation Report Generation

### Report Structure

```json
{
  "skill_name": "Skill Name",
  "evaluation_date": "Evaluation Date",
  "evaluator": "Evaluator",
  "evaluation_mode": "Evaluation Mode",
  "total_score": 9.2,
  "grade": "A",
  "dimensions": {
    "structure_completeness": {
      "score": 9.5,
      "weight": 0.15,
      "automated_score": 9.0,
      "manual_score": 10.0,
      "comments": "Complete structure, conforms to standards"
    },
    "content_quality": {
      "score": 9.0,
      "weight": 0.20,
      "comments": "Clear content, strong executability"
    },
    "usability": {
      "score": 9.0,
      "weight": 0.15,
      "comments": "Good usability, clear trigger conditions"
    },
    "design_patterns": {
      "score": 9.5,
      "weight": 0.10,
      "comments": "Excellent design, clear modularity"
    },
    "documentation_quality": {
      "score": 9.0,
      "weight": 0.10,
      "comments": "Good documentation, sufficient examples"
    },
    "agent_prompt_quality": {
      "score": 9.0,
      "weight": 0.10,
      "comments": "Good agent prompt quality"
    },
    "automation_friendliness": {
      "score": 9.0,
      "weight": 0.10,
      "comments": "High automation friendliness"
    },
    "user_experience": {
      "score": 9.0,
      "weight": 0.10,
      "comments": "Good user experience"
    }
  },
  "automated_checks": {
    "file_structure": {
      "status": "PASS",
      "score": 3,
      "max_score": 3,
      "details": "File exists, readable, correct encoding"
    },
    "frontmatter": {
      "status": "PASS",
      "score": 5,
      "max_score": 5,
      "details": "All required fields exist and format is correct"
    },
    "section_structure": {
      "status": "PASS",
      "score": 5,
      "max_score": 5,
      "details": "All standard sections exist"
    },
    "markdown_format": {
      "status": "PASS",
      "score": 2.5,
      "max_score": 3,
      "details": "Standard format, clear hierarchy"
    },
    "automation_support": {
      "status": "PASS",
      "score": 5,
      "max_score": 5,
      "details": "Provides complete automation scripts, supports CI/CD"
    }
  },
  "manual_review": {
    "content_quality": {
      "score": 9.0,
      "reviewer_comments": "Clear content, strong executability"
    },
    "usability": {
      "score": 9.0,
      "reviewer_comments": "Good usability, clear trigger conditions"
    },
    "design_patterns": {
      "score": 9.5,
      "reviewer_comments": "Excellent design, clear modularity"
    },
    "documentation_quality": {
      "score": 9.0,
      "reviewer_comments": "Good documentation, sufficient examples"
    },
    "agent_prompt_quality": {
      "score": 9.0,
      "reviewer_comments": "Good agent prompt quality"
    },
    "automation_friendliness": {
      "score": 9.0,
      "reviewer_comments": "High automation friendliness"
    },
    "user_experience": {
      "score": 9.0,
      "reviewer_comments": "Good user experience"
    }
  },
  "issues": [
    {
      "dimension": "Content Quality",
      "severity": "LOW",
      "description": "Some expressions could be clearer",
      "suggestion": "Suggest optimizing wording",
      "location": "Methodology section",
      "automated": false
    }
  ],
  "recommendations": [
    "Suggest adding more usage examples",
    "Suggest optimizing trigger condition description"
  ],
  "comparison_with_reference": {
    "reference_skill": "harness-prompt-optimizer",
    "strengths": ["More concise structure", "Clearer trigger conditions"],
    "weaknesses": ["Lack of examples", "Documentation not detailed enough"],
    "suggestions": ["Refer to prompt-optimizer's example design", "Add more usage scenarios"]
  }
}
```

## Evaluation Result Application

### 1. Quality Grade Application

**A+ Grade (9.5-10)**:
- Can serve as an industry benchmark
- Can be used to train new skills
- Can be prominently recommended in documentation

**A Grade (9.0-9.4)**:
- Can serve as a reference example
- Can be used to train new skills
- Can be recommended in documentation

**B+ Grade (8.5-8.9)**:
- Meets high standards, can be used normally
- Minor optimizations can be made
- Can serve as a foundation for improvement

**B Grade (8.0-8.4)**:
- Meets basic standards, can be used normally
- Needs optimization
- Can serve as a foundation for improvement

**C Grade (7.0-7.9)**:
- Needs improvement
- Create an improvement plan
- Re-evaluate periodically

**D Grade (6.0-6.9)**:
- Needs significant improvement
- Suspend use until improvements are complete
- Provide specific improvement guidance

**F Grade (0-5.9)**:
- Failing, needs rewrite
- Remove from skills collection
- Provide rewrite guidance

### 2. Improvement Suggestion Application

**Short-term Improvements (1-2 days)**:
- Fix obvious issues
- Supplement missing content
- Optimize formatting

**Medium-term Improvements (1 week)**:
- Redesign parts of the content
- Add examples and use cases
- Optimize user experience

**Long-term Improvements (1 month)**:
- Re-evaluate design patterns
- Consider whether splitting or merging is needed
- Evaluate whether a new skill is needed

## Evaluation Automation

### 1. Automation Script

**Check Script Example**:
```bash
#!/bin/bash
# skill-quality-check.py

SKILL_DIR=$1
SKILL_NAME=$2

# Check file existence
if [ ! -f "$SKILL_DIR/$SKILL_NAME/SKILL.md" ]; then
    echo "Error: SKILL.md file does not exist"
    exit 1
fi

# Check frontmatter
echo "Checking frontmatter..."
grep -q "^name:" "$SKILL_DIR/$SKILL_NAME/SKILL.md" && echo "✓ name field exists" || echo "✗ name field missing"
grep -q "^description:" "$SKILL_DIR/$SKILL_NAME/SKILL.md" && echo "✓ description field exists" || echo "✗ description field missing"
grep -q "^when_to_use:" "$SKILL_DIR/$SKILL_NAME/SKILL.md" && echo "✓ when_to_use field exists" || echo "✗ when_to_use field missing"
grep -q "^compatibility:" "$SKILL_DIR/$SKILL_NAME/SKILL.md" && echo "✓ compatibility field exists" || echo "✗ compatibility field missing"

# Check section structure
echo "Checking section structure..."
grep -q "^## Core Principles" "$SKILL_DIR/$SKILL_NAME/SKILL.md" && echo "✓ Core Principles section exists" || echo "✗ Core Principles section missing"
grep -q "^## When to Use" "$SKILL_DIR/$SKILL_NAME/SKILL.md" && echo "✓ When to Use section exists" || echo "✗ When to Use section missing"
grep -q "^## When Not to Use" "$SKILL_DIR/$SKILL_NAME/SKILL.md" && echo "✓ When Not to Use section exists" || echo "✗ When Not to Use section missing"
grep -q "^## Methodology" "$SKILL_DIR/$SKILL_NAME/SKILL.md" && echo "✓ Methodology section exists" || echo "✗ Methodology section missing"
grep -q "^## Key Points" "$SKILL_DIR/$SKILL_NAME/SKILL.md" && echo "✓ Key Points section exists" || echo "✗ Key Points section missing"
grep -q "^## Common Pitfalls" "$SKILL_DIR/$SKILL_NAME/SKILL.md" && echo "✓ Common Pitfalls section exists" || echo "✗ Common Pitfalls section missing"

echo "Check complete"
```

### 2. CI/CD Integration

**GitHub Actions Example**:
```yaml
name: Skill Quality Check

on:
  push:
    paths:
      - 'skills/**/SKILL.md'
  pull_request:
    paths:
      - 'skills/**/SKILL.md'

jobs:
  quality-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Check skill quality
        run: |
          for skill_dir in skills/*/; do
            skill_name=$(basename "$skill_dir")
            echo "Checking $skill_name..."
            python3 "$skill_dir/references/automated_check_script.py"
          done
```

---
Last updated: 2026-07-02
