# Domain-Specific Patterns

Different domains have different emphases in prompt design. This document provides design pattern references for common domains.

---

## Code (Code Review, Code Generation, Debugging)

**Emphasis**: Constraints > Execution Chain > Examples

**Design Points**:
- **Constraints must be strict**: Code tasks require precise definition of what constitutes a "problem" to prevent the LLM from "finding issues for the sake of finding issues"
- **Severity Anchoring**: Clearly define the meaning of CRITICAL / HIGH / MEDIUM / LOW
- **Actionable Fixes**: Every finding must include a concrete fix suggestion
- **Line References**: Require output to include file names and line numbers

**Required Constraints**:
- `No Speculation`: Only flag issues you can point to with specific line references
- `Severity Anchoring`: CRITICAL = data loss/security breach, HIGH = runtime errors, MEDIUM = tech debt, LOW = style
- `Actionable Fixes`: Every finding must include a concrete fix suggestion

**Example Structure**:
```
Role: Senior [Language] Engineer with [X] years of experience in [domain]
Execution Chain:
1. Parse & Understand intent
2. Check correctness (logic errors, edge cases)
3. Check security (injection, secrets, SSRF)
4. Check maintainability (naming, complexity)
5. Format findings
Constraints: No Speculation, Severity Anchoring, Actionable Fixes
Examples: Standard review, Clean code (no issues found), Critical security issue
```

---

## Copywriting (Copywriting, Marketing, Content)

**Emphasis**: Examples > Execution Chain > Constraints

**Design Points**:
- **Examples matter more than rules**: For copywriting tasks, the LLM relies more on examples to understand style
- **Platform Calibration**: Different platforms (Instagram, TikTok, Email, Landing Page) have completely different copy structures
- **Tone Override**: Provide optional tone override parameters
- **Ban List**: Giving the LLM a specific exclusion list (e.g., "don't use corporate buzzwords") is more enforceable than "write naturally"

**Required Constraints**:
- `No Corporate Speak`: Ban specific words/phrases (leverage, synergy, empower, etc.)
- `Show Don't Tell`: Prefer concrete specifics over vague superlatives
- `Respect Platform Limits`: Hard stop on character limits

**Example Structure**:
```
Role: Creative Copywriter specializing in [industry] targeting [demographic]
Execution Chain:
1. Understand product → extract core benefit (≤8 words)
2. Platform calibration → adjust format per platform
3. Write 3 variants (benefit-led, pain-point-led, social-proof-led)
4. Self-rate each variant (hook strength, clarity, platform fit)
Constraints: No Corporate Speak, Show Don't Tell, Respect Platform Limits
Examples: Instagram post, Email subject line, Landing page headline
```

---

## Analysis (Data Analysis, Research, Report Generation)

**Emphasis**: Execution Chain > Constraints > Output Schema

**Design Points**:
- **Execution Chain must be clear**: Analysis tasks require a well-defined step sequence
- **Data Anchoring**: Require the LLM to work only with provided data, not fabricate
- **Confidence Levels**: Output should include confidence or uncertainty declarations
- **Structured Output**: Analysis results typically need structured output (JSON/table)

**Required Constraints**:
- `Data Anchoring`: Only analyze provided data. Do not use external knowledge
- `Confidence Declaration`: State confidence level for each conclusion (HIGH/MEDIUM/LOW)
- `Source Citation`: Every claim must reference specific data points

**Example Structure**:
```
Role: Senior Data Analyst specializing in [domain]
Execution Chain:
1. Understand the data structure and variables
2. Identify key patterns and anomalies
3. Calculate relevant metrics
4. Draw conclusions with confidence levels
Constraints: Data Anchoring, Confidence Declaration, Source Citation
Examples: Standard analysis, Missing data handling, Ambiguous data interpretation
```

---

## Customer Service (Customer Service, Support, Chatbot)

**Emphasis**: Constraints > Examples > Output Schema

**Design Points**:
- **Empathy Constraints**: Require the LLM to acknowledge the customer's feelings before providing a solution
- **Escalation Triggers**: Clearly define when to escalate to a human (legal threats, emotional distress, complex issues)
- **Policy Anchoring**: Strictly answer according to policy; do not promise what cannot be delivered
- **Response Tone**: Define tone (friendly but professional, empathetic but not submissive)

**Required Constraints**:
- `Empathy First`: Acknowledge customer frustration before delivering bad news
- `Policy Anchoring`: Never promise refunds/benefits that violate policy
- `Escalation Trigger`: If customer mentions "lawyer" or "sue", immediately offer human agent
- `No Speculation`: Do not invent reasons for denial

**Example Structure**:
```
Role: Customer Service Specialist for [company/industry]
Execution Chain:
1. Identify intent (refund, status check, policy question)
2. Validate eligibility (check order info, policy)
3. Apply policy (eligible → process, not eligible → explain + alternatives)
4. Respond with empathy
Constraints: Empathy First, Policy Anchoring, Escalation Trigger
Examples: Eligible refund, Ineligible refund, Fraudulent claim, Angry customer
```

---

## Translation (Translation, Localization)

**Emphasis**: Constraints > Examples > Variables Dictionary

**Design Points**:
- **Style Preservation**: Require preserving the original style (formal/informal, technical/colloquial)
- **Cultural Adaptation**: Not just language translation, but cultural adaptation
- **Terminology Consistency**: Professional terminology must be consistent
- **Format Preservation**: Preserve original formatting (Markdown, HTML, code blocks)

**Required Constraints**:
- `Style Preservation`: Maintain the original tone and formality level
- `Cultural Adaptation`: Adapt idioms and cultural references for target audience
- `Terminology Consistency`: Use consistent translations for technical terms
- `Format Preservation`: Keep original formatting (Markdown, HTML, code blocks)

**Example Structure**:
```
Role: Professional Translator specializing in [domain] (e.g., legal, medical, technical)
Variables:
- `{{source_text}}`: Text to translate (String, Required)
- `{{source_language}}`: Source language (String, Required)
- `{{target_language}}`: Target language (String, Required)
- `{{style_guide}}`: Terminology preferences (String, Optional)
Execution Chain:
1. Identify domain and terminology
2. Translate preserving style and format
3. Adapt cultural references
4. Verify terminology consistency
Constraints: Style Preservation, Cultural Adaptation, Terminology Consistency
Examples: Technical document, Marketing copy, Legal text
```

---

## Education (Tutoring, Explanation, Teaching)

**Emphasis**: Execution Chain > Examples > Constraints

**Design Points**:
- **Scaffolding**: Progress from simple to complex step by step
- **Check Understanding**: Require the LLM to check if the user understands
- **Multiple Explanations**: Explain the same concept in different ways
- **Practice Problems**: Provide practice questions to reinforce understanding

**Required Constraints**:
- `Check Understanding`: After each concept, ask "Does this make sense?" or provide a quick quiz
- `Multiple Angles`: Explain each concept at least 2 different ways
- `No Jargon Without Definition`: Define technical terms before using them

**Example Structure**:
```
Role: [Subject] Tutor with [X] years of teaching experience
Execution Chain:
1. Assess current understanding level
2. Break concept into smaller parts
3. Explain each part with analogies and examples
4. Check understanding with questions
5. Provide practice problems
Constraints: Check Understanding, Multiple Angles, No Jargon Without Definition
Examples: Beginner explanation, Advanced explanation, Misconception correction
```

---

## Quick Selection Guide

| Your Task Type | Emphasis | Key Design Elements |
|---|---|---|
| Code Review/Generation | Constraints | Severity Anchoring, Actionable Fixes, Line References |
| Copywriting | Examples | Platform Calibration, Ban List, Multiple Variants |
| Data Analysis | Execution Chain | Data Anchoring, Confidence Levels, Source Citation |
| Customer Service | Constraints | Empathy First, Policy Anchoring, Escalation Triggers |
| Translation | Constraints | Style Preservation, Cultural Adaptation, Terminology |
| Education/Explanation | Execution Chain | Scaffolding, Check Understanding, Multiple Angles |

---
Last updated: 2026-07-02
