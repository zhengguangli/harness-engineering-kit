# Skills Quality Assessment Dimensions Detailed Description

Update time: 2026-07-02
Updated by: claude-code

## Evaluation Dimension System (8 Dimensions)

### 1. Structure Completeness (Weight: 15%)

**Evaluation Criteria**:
- Frontmatter completeness: includes required fields such as name, description, when_to_use, compatibility
- Section structure: includes standard sections such as core principles, when to use, when not to use, methodology, key takeaways, common pitfalls
- Format standardization: correct Markdown format, clear hierarchical structure

**Scoring Rules (0-10)**:
- 9.5-10: Fully conforms to harness system standards, perfect structure, standard format
- 9.0-9.4: Fully conforms to standards, excellent structure
- 8.5-8.9: Basically conforms to standards, missing 1-2 non-required fields or sections
- 8.0-8.4: Partially conforms to standards, missing required fields or sections
- 7.0-7.9: Confusing structure, missing multiple required parts
- 6.0-6.9: Almost no structure, does not conform to standards
- 0-5.9: No structure at all, needs rewrite

**Checkpoints**:
- [ ] Frontmatter includes name field
- [ ] Frontmatter includes description field (>= 20 characters)
- [ ] Frontmatter includes when_to_use field
- [ ] Frontmatter includes compatibility field
- [ ] Includes "Core Principles" section
- [ ] Includes "When to Use" section
- [ ] Includes "When Not to Use" section
- [ ] Includes "Methodology" section
- [ ] Includes "Key Takeaways" section
- [ ] Includes "Common Pitfalls" section
- [ ] Includes "Agent Prompt" section (if applicable)

### 2. Content Quality (Weight: 20%)

**Evaluation Criteria**:
- Clarity: Content is clearly expressed, no ambiguity
- Completeness: Covers all key information needed for the skill
- Executability: Provided guidance can be directly executed

**Scoring Rules (0-10)**:
- 9.5-10: Content is perfectly clear, complete, directly executable, no redundancy
- 9.0-9.4: Content is excellent, clear, complete, executable
- 8.5-8.9: Content is basically clear and complete, minor improvements possible
- 8.0-8.4: Content is partially clear, but has ambiguity or omissions
- 7.0-7.9: Content is vague, difficult to execute
- 6.0-6.9: Content is confusing, almost unusable
- 0-5.9: Content is completely unusable, needs rewrite

**Checkpoints**:
- [ ] Core principles are clear and specific
- [ ] Methodology steps are detailed and actionable
- [ ] Examples and use cases are specific and practical
- [ ] No ambiguous expressions
- [ ] No redundant information

### 3. Usability (Weight: 15%)

**Evaluation Criteria**:
- Trigger conditions are clear: users know when to use the skill
- Execution process is clear: agent knows how to execute
- Output format is standard: results are easy to understand and use

**Scoring Rules (0-10)**:
- 9.5-10: Trigger conditions are perfectly clear, execution process is clear, output format is standard
- 9.0-9.4: Trigger conditions are clear, execution process is clear, output format is standard
- 8.5-8.9: Basically usable, some aspects could be optimized
- 8.0-8.4: Usable but has confusing points
- 7.0-7.9: Difficult to use, requires a lot of guessing
- 6.0-6.9: Almost unusable
- 0-5.9: Completely unusable, needs rewrite

**Checkpoints**:
- [ ] "When to Use" scenarios are specific and clear
- [ ] "When Not to Use" scenarios are clear
- [ ] Execution process steps are clear
- [ ] Output format has clear specification
- [ ] Has specific usage examples

### 4. Design Patterns (Weight: 10%)

**Evaluation Criteria**:
- Modularity: Skill structure is modular, easy to understand and maintain
- Extensibility: Design allows for future extension and modification
- Consistency: Maintains design consistency with other skills

**Scoring Rules (0-10)**:
- 9.5-10: Perfect design, clear modularity, extensible, highly consistent
- 9.0-9.4: Excellent design, clear modularity, extensible, highly consistent
- 8.5-8.9: Good design, basically follows system design patterns
- 8.0-8.4: Average design, partially follows system design patterns
- 7.0-7.9: Poor design, inconsistent with system design patterns
- 6.0-6.9: Confusing design, no modularity
- 0-5.9: Design completely unusable, needs rewrite

**Checkpoints**:
- [ ] Follows harness system design patterns
- [ ] Structure is clearly modular
- [ ] Allows for future extension
- [ ] Consistent with other skills' style

### 5. Documentation Quality (Weight: 10%)

**Evaluation Criteria**:
- Example richness: Provides sufficient examples and use cases
- Explanation clarity: Documentation explanations are clear and understandable
- Error handling: Includes error handling and troubleshooting guidance

**Scoring Rules (0-10)**:
- 9.5-10: Perfect documentation, rich examples, clear explanations, includes error handling
- 9.0-9.4: Excellent documentation, rich examples, clear explanations, includes error handling
- 8.5-8.9: Good documentation, basically sufficient
- 8.0-8.4: Average documentation, missing some examples or explanations
- 7.0-7.9: Poor documentation, difficult to understand
- 6.0-6.9: Barely any documentation
- 0-5.9: No documentation at all, needs rewrite

**Checkpoints**:
- [ ] Includes usage examples
- [ ] Includes error handling guidance
- [ ] Includes troubleshooting suggestions
- [ ] Explanations are clear and understandable

### 6. Agent Prompt Quality (Weight: 10%)

**Evaluation Criteria**:
- Role definition is clear: agent knows its role and responsibilities
- Execution process is clear: agent knows how to execute
- Constraints are reasonable: constraints are reasonable and actionable

**Scoring Rules (0-10)**:
- 9.5-10: Perfect agent prompt, clear role, clear process, reasonable constraints
- 9.0-9.4: Excellent agent prompt, clear role, clear process, reasonable constraints
- 8.5-8.9: Good agent prompt, basically usable
- 8.0-8.4: Average agent prompt, has confusing points
- 7.0-7.9: Poor agent prompt, difficult to execute
- 6.0-6.9: Barely any agent prompt
- 0-5.9: No agent prompt at all, needs rewrite

**Checkpoints**:
- [ ] Role definition is clear
- [ ] Core capabilities are clear
- [ ] Execution process is detailed
- [ ] Constraints are reasonable
- [ ] Output specification is clear

### 7. Automation Friendliness (Weight: 10%)

**Evaluation Criteria**:
- Degree of automated checkability: how many check items can be automated
- Script support: whether automated check scripts are provided
- CI/CD integration: whether CI/CD integration is supported

**Scoring Rules (0-10)**:
- 9.5-10: Fully automated, complete scripts provided, CI/CD integration supported
- 9.0-9.4: Highly automated, complete scripts provided, CI/CD integration supported
- 8.5-8.9: Mostly automatable, basic scripts provided
- 8.0-8.4: Partially automatable, scripts incomplete
- 7.0-7.9: Low automation, missing scripts
- 6.0-6.9: Almost impossible to automate
- 0-5.9: Completely impossible to automate, needs rewrite

**Checkpoints**:
- [ ] Provides automated check script
- [ ] Supports CI/CD integration
- [ ] High proportion of check items can be automated
- [ ] Automated check results are quantifiable

### 8. User Experience (Weight: 10%)

**Evaluation Criteria**:
- Learning curve: difficulty for users to learn the skill
- Ease of use: convenience of using the skill
- Error recovery capability: ability to recover when errors occur

**Scoring Rules (0-10)**:
- 9.5-10: Gentle learning curve, easy to use, strong error recovery
- 9.0-9.4: Gentle learning curve, easy to use, strong error recovery
- 8.5-8.9: Moderate learning curve, fairly easy to use, fairly strong error recovery
- 8.0-8.4: Steeper learning curve, average ease of use, average error recovery
- 7.0-7.9: Steep learning curve, inconvenient to use, weak error recovery
- 6.0-6.9: Very steep learning curve, very inconvenient, almost no error recovery
- 0-5.9: Completely unusable, needs rewrite

**Checkpoints**:
- [ ] Gentle learning curve
- [ ] Easy to use
- [ ] Strong error recovery capability
- [ ] Provides sufficient help information

### Supplementary Check: allowed-tools Declaration Check

| Check Item | Pass Condition | Fail Condition | Severity |
|--------|----------|----------|----------|
| allowed-tools exists | Frontmatter includes `allowed-tools:` field | Missing | WARN |
| allowed-tools syntax | Format is `Tool(cmd1 cmd2)` | Wrong format or invalid tool name | WARN |
| allowed-tools least privilege | Read-only skill does not include Edit/Write | Includes tools it shouldn't have | WARN |
| context field exists | Frontmatter includes `context:` field | Missing | WARN |
| metadata.category exists | Frontmatter includes `metadata.category:` field | Missing | WARN |

### Supplementary Check: Cross-Skill Handoff Check

| Check Item | Pass Condition | Fail Condition | Severity |
|--------|----------|----------|----------|
| Upstream skill description | Clearly lists upstream skills and received outputs | Not mentioned | WARN |
| Downstream skill description | Clearly lists downstream skills and transmitted outputs | Not mentioned | WARN |
| Handoff timing | Explains when handoff is triggered | Not explained | WARN |
| Error handling | Recovery method for failed handoff | Not explained | WARN |

### Supplementary Check: Last Update Freshness Check

| Check Item | Pass Condition | Fail Condition | Severity |
|--------|----------|----------|----------|
| Last update exists | Includes "Last updated" date marker | Missing | WARN |
| Freshness | Update date within 90 days | Over 90 days | LOW |

## Composite Score Calculation

**Total Score Formula**:
```
Total = (Structure Completeness x 0.15) + (Content Quality x 0.20) + (Usability x 0.15) +
        (Design Patterns x 0.10) + (Documentation Quality x 0.10) + (Agent Prompt Quality x 0.10) +
        (Automation Friendliness x 0.10) + (User Experience x 0.10)
```

Each dimension score = arithmetic mean of sub-dimension scores (each sub-dimension 0-10).

**Grade Classification**:
- A+ (9.5-10): Excellent, can serve as an industry benchmark
- A (9.0-9.4): Great, can serve as a reference example
- B+ (8.5-8.9): Good, meets high standards
- B (8.0-8.4): Adequate, meets basic standards
- C (7.0-7.9): Fair, needs improvement
- D (6.0-6.9): Poor, needs significant improvement
- F (0-5.9): Failing, needs rewrite

## Evaluation Process

### Automated Checks (Weight: 40%)

1. Frontmatter field completeness check
2. Section structure check
3. Markdown format validation
4. Keyword consistency check
5. Automation script support check
6. CI/CD integration check

### Manual Review (Weight: 60%)

1. Content quality review
2. Usability review
3. Design pattern review
4. Documentation quality review
5. Agent prompt quality review
6. Automation friendliness review
7. User experience review

## Evaluation Report Format

```json
{
  "skill_name": "skill name",
  "evaluation_date": "evaluation date",
  "total_score": 9.2,
  "grade": "A",
  "dimensions": {
    "structure_completeness": {
      "score": 9.5,
      "weight": 0.15,
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
  "issues": [
    {
      "dimension": "Content Quality",
      "severity": "LOW",
      "description": "Some expressions could be clearer",
      "suggestion": "Recommend optimizing wording"
    }
  ],
  "recommendations": [
    "Recommend adding more usage examples",
    "Recommend optimizing trigger condition descriptions"
  ]
}
```

## Evaluator Guide: Common Misjudgment Scenarios

### 1. Automation Friendliness Scoring Pitfalls

| Misjudgment Pattern | Wrong Approach | Correct Approach |
|----------|----------|----------|
| Give high score if script exists | Give 9.0+ just for having automated-check-script.sh | Also check the number of check items covered and verification accuracy |
| Give zero score if no script | Give 0 for no automated-check-script.sh | Check if there are other automation methods (e.g., shared scripts under project-level scripts/), reasonably score 6.0-7.0 |
| Ignore CI/CD integration | Only look at scripts, not CI configuration | Check if .github/workflows integrates the script |

### 2. Documentation Quality Scoring Pitfalls

| Misjudgment Pattern | Wrong Approach | Correct Approach |
|----------|----------|----------|
| Only count refs quantity, not quality | Give high score for many refs | Also check the actual content quality of refs files and example completeness |
| Miss common-edge-cases | Fail to notice the file exists | Must check whether `references/common-edge-cases.md` exists |
| Ignore last update date | Just check existence, not recency | Deduct points ( -0.5 to -1.0 ) in documentation quality dimension if over 90 days |

### 3. Design Pattern Scoring Pitfalls

| Misjudgment Pattern | Wrong Approach | Correct Approach |
|----------|----------|----------|
| Ignore cross-skill handoff | Only evaluate internal skill structure | Must check whether upstream/downstream skill handoff relationships are described |
| Over-reliance on reference skill comparison | Reference skill is 9.5 so give others 9.5 | Score based on actual quality, do not automatically give high scores because of high reference skill score |
| Consistency check too broad | Broad structure consistency is enough | Need to check down to section naming style, hard constraint format, heading hierarchy |

### 4. Low Score Trigger Patterns

The following conditions should automatically trigger a low score (<=7.0):

| Condition | Affected Dimension | Suggested Score |
|------|-----------|---------|
| Missing `## Agent Prompt` section | Agent Prompt Quality | 0 |
| Missing `## Methodology` section | Content Quality | <=5.0 |
| Frontmatter missing 2+ required fields | Structure Completeness | <=6.0 |
| No reference files under `references/` directory | Documentation Quality | <=6.5 |
| No allowed-tools declaration | Automation Friendliness | <=7.0 |
| No common-edge-cases.md | Documentation Quality | <=8.0 |

### 5. Cross-Dimension Interaction Notes

| Relationship | Description |
|----------|------|
| allowed-tools affects 2 dimensions | Missing affects both structure completeness (incomplete frontmatter) and automation friendliness (violates least privilege principle) |
| common-edge-cases affects 2 dimensions | Missing affects both documentation quality (insufficient examples) and user experience (missing edge case handling) |
| Hard constraint richness affects 2 dimensions | Rich hard constraints (>= 3) benefit content quality; missing affects structure completeness |
| Standardized report output path affects 2 dimensions | Standardized output path benefits usability (clear output) and user experience (predictable results) |

## Sub-Dimension and Checkpoint Mapping

| Dimension | Sub-Dimension | Corresponding Checkpoints |
|------|--------|-----------|
| Structure Completeness(15%) | frontmatter completeness | name/description/when_to_use/compatibility/context/agent/metadata/category/allowed-tools/version(should not contain) |
| Structure Completeness(15%) | section structure complete | Core Principles/When to Use/When Not to Use/Methodology/Key Takeaways/Common Pitfalls/Edge Case Handling/Hard Constraints/Agent Prompt |
| Structure Completeness(15%) | format standardization | heading hierarchy/list format/code block pairing/link format |
| Content Quality(20%) | clarity | precise core principles, no ambiguous expressions |
| Content Quality(20%) | completeness | covers skill key information, complete methodology |
| Content Quality(20%) | executability | steps reproducible, examples copyable |
| Usability(15%) | trigger condition clarity | When to Use/When Not to Use scenarios specific |
| Usability(15%) | execution process clarity | process steps clear and executable |
| Usability(15%) | output format standardization | output path/format has clear convention |
| Design Patterns(10%) | modularity | structure modular and understandable |
| Design Patterns(10%) | extensibility | design allows extension |
| Design Patterns(10%) | consistency | consistent style with other skills |
| Design Patterns(10%) | cross-skill handoff | upstream/downstream/handoff timing/outputs |
| Documentation Quality(10%) | example richness | example count >= 2 |
| Documentation Quality(10%) | explanation clarity | common-edge-cases exists |
| Documentation Quality(10%) | error handling | edge cases/troubleshooting |
| Documentation Quality(10%) | last update freshness | update date <= 90 days |
| Agent Prompt Quality(10%) | 6 sub-section completeness | skip conditions/role definition/core capabilities/execution process/constraints/output specifications |
| Agent Prompt Quality(10%) | constraint quality | constraints include violation consequences |
| Agent Prompt Quality(10%) | output path | standardized output path |
| Automation Friendliness(10%) | script support | automated-check-script.sh |
| Automation Friendliness(10%) | check coverage | number and quality of check items |
| Automation Friendliness(10%) | CI/CD integration | .github/workflows configuration |
| User Experience(10%) | learning curve | trigger scenarios intuitive |
| User Experience(10%) | ease of use | edge case coverage |
| User Experience(10%) | error recovery | common pitfalls coverage |

## Automated Check Weighted Scoring Model

The automated check scoring has been upgraded from a simple pass-rate model to a weighted model:

| Level | Weight Score | Meaning |
|------|--------|------|
| PASS | +1 | Check passed |
| WARN | 0 | Warning, no deduction |
| LOW | -1 | Low severity issue |
| MEDIUM | -2 | Medium severity issue |
| HIGH | -3 | High severity issue |
| CRITICAL | -5 | Blocking-level issue |

**Final Automated Score** = max(0, min(10, (pass_count x 1 + penalty_score) x 10 / total_check_count))

---
Last updated: 2026-07-03 (Change: Added supplementary checkpoints, evaluator guide, sub-dimension mapping, weighted scoring model)
