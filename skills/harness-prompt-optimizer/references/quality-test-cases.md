# Prompt Optimizer Quality Assessment Tests

## Test Description

This file contains quality assessment test cases for the `harness-prompt-optimizer` skill. Tests cover four dimensions:
1. Trigger Accuracy
2. Input Type Judgment
3. Language Confirmation
4. Output Quality

Each test case includes: Input, Expected Behavior, Evaluation Criteria.

---

## 1. Trigger Accuracy Tests

### Should Trigger (Explicit Trigger)

| ID | Input | Expected Behavior | Evaluation Criteria |
|---|---|---|---|
| T1.1 | "优化一下 我希望AI能帮我review代码" | Enter optimization flow directly | Recognize "优化一下" trigger word |
| T1.2 | "帮我优化我的描述：写一个数据分析的prompt" | Enter optimization flow directly | Recognize "帮我优化" trigger word |
| T1.3 | "改进一下 这个prompt效果不好：You are a code reviewer" | Enter optimization flow directly | Recognize "改进一下" trigger word |
| T1.4 | "帮我写个prompt 让AI帮我写营销文案" | Enter optimization flow directly | Recognize "帮我写个prompt" trigger word |
| T1.5 | "给我一个system prompt 处理客服对话" | Enter optimization flow directly | Recognize "给我一个" trigger word |

### Should Trigger (Implicit Trigger)

| ID | Input | Expected Behavior | Evaluation Criteria |
|---|---|---|---|
| T2.1 | "You are a code reviewer. Find bugs." | Quick confirmation, then enter optimization flow | Recognize as system prompt |
| T2.2 | "我希望AI能帮我分析数据，要输出JSON格式" | Quick confirmation, then enter optimization flow | Recognize as requirement description |
| T2.3 | "这个agent行为不对，输出格式不稳定" | Assess whether prompt optimization is needed | Recognize as agent behavior issue |
| T2.4 | "我在做一个code review bot" | Proactively offer prompt optimization | Recognize as building agent scenario |

### Should NOT Trigger

| ID | Input | Expected Behavior | Evaluation Criteria |
|---|---|---|---|
| T3.1 | "帮我写个函数" | Do not trigger, handle code request normally | Recognize as code implementation |
| T3.2 | "这个bug怎么修" | Do not trigger, handle bug fix normally | Recognize as debugging request |
| T3.3 | "今天天气怎么样" | Do not trigger, normal conversation | Recognize as casual chat |
| T3.4 | "读一下这个文件" | Do not trigger, read file normally | Recognize as file operation |

### Boundary Cases

| ID | Input | Expected Behavior | Evaluation Criteria |
|---|---|---|---|
| T3.5 | "优化" (no content provided) | Ask: "Please provide the content to optimize" | Recognize trigger word but missing content |
| T3.6 | "帮我写个prompt" (no requirements described) | Ask: "Please describe your requirements and use case" | Recognize trigger word but missing requirements |
| T3.7 | "优化这个" (nothing follows) | Ask: "Please provide the content to optimize" | Recognize trigger word but missing content |

### Simple Task Judgment Tests

| ID | Input | Expected Behavior | Evaluation Criteria |
|---|---|---|---|
| T3.8 | "帮我写个hello world" | Skip conditional trigger, output simplified version | Recognize as simple task |
| T3.9 | "翻译这段话" | Skip conditional trigger, output simplified version | Recognize as simple task |
| T3.10 | "总结这篇文章" | Skip conditional trigger, output simplified version | Recognize as simple task |
| T3.11 | "帮我起个名字" | Skip conditional trigger, output simplified version | Recognize as simple task |

---

## 2. Input Type Judgment Tests

| ID | Input | Expected Judgment | Evaluation Criteria |
|---|---|---|---|
| T4.1 | "帮我写一个代码审查的prompt" | Requirement description, write from scratch | User describes requirements, no existing prompt |
| T4.2 | "优化这个：You are a helpful assistant. Answer questions." | System prompt, optimize existing | User pasted an existing prompt |
| T4.3 | "我希望AI能帮我分析数据，要输出JSON格式" | Requirement description, write from scratch | User describes requirements, no existing prompt |
| T4.4 | "这个prompt效果不好：You are a code reviewer. Find bugs and bad practices. Output JSON." | System prompt, optimize existing | User pasted an existing prompt with structure |
| T4.5 | "帮我优化：我希望AI能review代码，要求：1.找出bug 2.输出JSON格式" | Mixed content, split | Both requirement description and format constraints |

---

## 3. Language Confirmation Tests

| ID | Input | Expected Behavior | Evaluation Criteria |
|---|---|---|---|
| T5.1 | "优化一下 帮我写营销文案" | Ask: "Should the prompt be in Chinese or English?" | Chinese requirement, unspecified language |
| T5.2 | "优化这个prompt：You are a code reviewer" | Default output in English | English content |
| T5.3 | "帮我写个英文prompt 处理客服对话" | Output directly in English | User explicitly requested English |
| T5.4 | "写一个中文prompt 分析数据" | Output directly in Chinese | User explicitly requested Chinese |
| T5.5 | "优化这个：我希望AI能review代码，要求output JSON" | Ask: "Should the prompt be in Chinese or English?" | Mixed Chinese/English, unspecified language |

---

## 4. Output Quality Tests

### Existing Prompt Optimization Flow Tests

| ID | Test Scenario | Check Item | Evaluation Criteria |
|---|---|---|---|
| T6.0 | Optimize existing system prompt | Preserve good parts | Identify and retain effective parts of the original prompt |
| T6.0.1 | Optimize existing system prompt | Improve problematic parts | Identify and improve issues in the original prompt |
| T6.0.2 | Optimize existing system prompt | Supplement missing parts | Identify and supplement missing six-block sections in the original prompt |

### Six-Block Completeness Check

| ID | Test Scenario | Check Item | Evaluation Criteria |
|---|---|---|---|
| T6.1 | Complex task (code review) | Role / Context / Variables / Execution / Constraints / Examples | All six blocks present |
| T6.2 | Simple task (write hello world) | Role / Execution / Constraints | Can be simplified, but at least three blocks |

### Constraint Quality Check

| ID | Check Item | Evaluation Criteria |
|---|---|---|
| T7.1 | Each constraint includes violation consequences | Constraint format: "Rule + behavior when violated" |
| T7.2 | Constraint count ≤ 8 | No more than 8 constraints |
| T7.3 | Includes required constraints | Output format, hallucination prevention, safety guard (based on task type) |

### Example Coverage Check

| ID | Check Item | Evaluation Criteria |
|---|---|---|
| T8.1 | At least 2 examples | Standard + edge case |
| T8.2 | Examples consistent with Schema | Output format conforms to defined Schema |
| T8.3 | Examples cover boundary cases | Include scenarios like missing data, ambiguity, erroneous input |

### Domain Adaptation Check

| ID | Domain | Expected Emphasis | Evaluation Criteria |
|---|---|---|---|
| T9.1 | Code review | Constraints first | Severity Anchoring, Actionable Fixes |
| T9.2 | Copywriting | Examples first | Multiple Variants, Platform Calibration |
| T9.3 | Data analysis | Execution Chain first | Data Anchoring, Confidence Levels |
| T9.4 | Customer service dialogue | Constraints first | Empathy First, Escalation Triggers |

---

## 5. Test Execution Method

### Manual Test Flow

1. Prepare test environment: Ensure the skill is loaded
2. Execute test cases in order: Input → Observe behavior → Record results
3. Compare against expected behavior: Pass/Fail
4. Record failing cases: Analyze causes, propose improvement directions

### Automated Testing (Future)

```bash
# Pseudo code
for test_case in test_cases:
    result = run_skill(test_case.input)
    assert result.behavior == test_case.expected_behavior
    assert result.output_quality == test_case.quality_criteria
```

---

## 6. Test Results Recording Template

| Test Date | Test Case ID | Result | Issue Description | Improvement Suggestion |
|---|---|---|---|---|
| YYYY-MM-DD | T1.1 | PASS/FAIL | - | - |

---

## 7. Continuous Improvement

1. **Run tests weekly**: Check for skill regression
2. **Add new cases**: When encountering new scenarios / edge cases, add to the test file
3. **Update expected behavior**: When skill logic is adjusted, update expected behavior accordingly
4. **Analyze failing cases**: Identify common issues, optimize skill design

---
Last updated: 2026-07-02
