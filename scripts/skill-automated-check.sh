#!/bin/bash
# Skill Automated Check Script (shared)
# Usage: bash scripts/skill-automated-check.sh <skill-dir> <skill-name>
# Output: JSON

SKILL_DIR="${1:?Missing skill dir}"
SKILL_NAME="${2:?Missing skill name}"
FILE="$SKILL_DIR/$SKILL_NAME/SKILL.md"

# Counters and results
TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0
WARNINGS=0
ISSUES=()
WARNINGS_LIST=()

check_pass() {
    ((TOTAL_CHECKS++))
    ((PASSED_CHECKS++))
}

check_fail() {
    ((TOTAL_CHECKS++))
    ((FAILED_CHECKS++))
    local severity="${2:-HIGH}"
    ISSUES+=("{\"check\":\"$1\",\"severity\":\"$severity\",\"detail\":\"$3\"}")
}

check_warn() {
    ((TOTAL_CHECKS++))
    ((WARNINGS++))
    WARNINGS_LIST+=("{\"check\":\"$1\",\"detail\":\"$2\"}")
}

# Check file exists
if [ ! -f "$FILE" ]; then
    echo '{"error":"SKILL.md not found for '$SKILL_NAME'"}'
    exit 1
fi
check_pass "file-exists"

# Check frontmatter fields
for field in name description when_to_use compatibility; do
    grep -qE "^${field}:" "$FILE" && check_pass "fm-$field" || check_fail "fm-$field" "HIGH" "Missing $field"
done

# Check key sections
for section in "核心原则" "何时使用" "方法论" "关键要点"; do
    grep -qE "^##\s+${section}" "$FILE" && check_pass "section-$section" || check_warn "section-$section" "Missing $section"
done

# Check Agent prompt
grep -qE "^##\s+Agent 提示词" "$FILE" && check_pass "agent-prompt" || check_warn "agent-prompt" "Missing Agent 提示词 section"

# Check last updated
grep -qE "最后更新" "$FILE" && check_pass "last-updated" || check_warn "last-updated" "Missing last updated date"

# Check common-edge-cases
grep -qE "边界情况" "$FILE" && check_pass "edge-cases" || check_warn "edge-cases" "No edge cases section"

# Calculate score
if [ $TOTAL_CHECKS -gt 0 ]; then
    SCORE=$(echo "scale=2; $PASSED_CHECKS * 10 / $TOTAL_CHECKS" | bc)
else
    SCORE=0
fi

# Build JSON output
join_by_comma() {
    local items=("$@")
    if [ ${#items[@]} -eq 0 ]; then
        echo ""
    else
        local result=""
        for item in "${items[@]}"; do
            result="$result$item,"
        done
        echo "${result%,}"
    fi
}
ISSUES_JSON=$(join_by_comma "${ISSUES[@]}")
WARNINGS_JSON=$(join_by_comma "${WARNINGS_LIST[@]}")

cat <<EOF
{
  "skill_name": "$SKILL_NAME",
  "auto_check_score": $SCORE,
  "stats": {
    "total": $TOTAL_CHECKS,
    "passed": $PASSED_CHECKS,
    "failed": $FAILED_CHECKS,
    "warnings": $WARNINGS
  },
  "issues": [$ISSUES_JSON],
  "warnings": [$WARNINGS_JSON]
}
EOF
