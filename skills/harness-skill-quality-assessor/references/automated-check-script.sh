#!/bin/bash
# Skills quality assessment - automated check script (v2.0 weighted scoring edition)
# Usage: bash automated-check-script.sh [skill-name|all]
# Output: JSON-formatted check results with weighted scores

# Ensure UTF-8 support
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

SKILLS_DIR="${SKILLS_DIR:-./skills}"

# Temporary file for collecting results
TMPDIR="${TMPDIR:-/tmp}"
RESULTS_DIR=$(mktemp -d "$TMPDIR/skill-check-XXXXXX")
ISSUES_FILE="$RESULTS_DIR/issues.json"
WARNINGS_FILE="$RESULTS_DIR/warnings.json"
STATS_FILE="$RESULTS_DIR/stats.txt"
SCORE_FILE="$RESULTS_DIR/score.txt"

cleanup() { rm -rf "$RESULTS_DIR"; }
trap cleanup EXIT

echo "[]" > "$ISSUES_FILE"
echo "[]" > "$WARNINGS_FILE"
echo "0 0 0 0 0" > "$STATS_FILE"
echo "0" > "$SCORE_FILE"

# --- Weighted scoring model ---
# CRITICAL=5, HIGH=3, MEDIUM=2, LOW=1, WARN=0

# --- Utility functions ---

get_stats() {
    read -r total passed failed warnings score < "$STATS_FILE"
}

update_stats() {
    local total passed failed warnings score
    read -r total passed failed warnings score < "$STATS_FILE"
    echo "$((total+1)) $((passed+1)) $failed $warnings $((score+1))" > "$STATS_FILE"
}

update_stats_fail() {
    local total passed failed warnings score sev="$1"
    read -r total passed failed warnings score < "$STATS_FILE"
    local penalty=0
    case "$sev" in
        CRITICAL) penalty=5;;
        HIGH)     penalty=3;;
        MEDIUM)   penalty=2;;
        LOW)      penalty=1;;
        *)        penalty=1;;
    esac
    echo "$((total+1)) $passed $((failed+1)) $warnings $((score>penalty ? score-penalty : 0))" > "$STATS_FILE"
}

update_stats_warn() {
    local total passed failed warnings score
    read -r total passed failed warnings score < "$STATS_FILE"
    echo "$((total+1)) $passed $failed $((warnings+1)) $score" > "$STATS_FILE"
}

add_issue() {
    local check="$1" detail="$2" severity="$3"
    local tmp
    tmp=$(mktemp)
    python3 -c "
import json, sys
with open('$ISSUES_FILE') as f: data = json.load(f)
data.append({'check': sys.argv[1], 'severity': sys.argv[2], 'detail': sys.argv[3]})
with open('$tmp', 'w') as f: json.dump(data, f, ensure_ascii=False)
" "$check" "$severity" "$detail"
    mv "$tmp" "$ISSUES_FILE"
}

add_warning() {
    local check="$1" detail="$2"
    local tmp
    tmp=$(mktemp)
    python3 -c "
import json, sys
with open('$WARNINGS_FILE') as f: data = json.load(f)
data.append({'check': sys.argv[1], 'detail': sys.argv[2]})
with open('$tmp', 'w') as f: json.dump(data, f, ensure_ascii=False)
" "$check" "$detail"
    mv "$tmp" "$WARNINGS_FILE"
}

check_pass() { update_stats; }
check_fail() { update_stats_fail "$2"; add_issue "$1" "$3" "$2"; }
check_warn() { update_stats_warn; add_warning "$1" "$2"; }

# --- File structure check ---

check_file_exists() {
    local f="$1"
    if [[ -f "$f" ]]; then check_pass; else check_fail "File exists" "CRITICAL" "SKILL.md does not exist: $f"; return 1; fi
}

check_file_readable() { [[ -r "$1" ]] && check_pass || check_fail "File readable" "CRITICAL" "File is not readable"; }

check_file_encoding() {
    local enc
    enc=$(file -b --mime-encoding "$1" 2>/dev/null || echo "unknown")
    [[ "$enc" == "utf-8" || "$enc" == "ascii" ]] && check_pass || check_warn "File encoding" "Encoding is $enc, UTF-8 recommended"
}

# --- Frontmatter deep check ---

check_fm_field() {
    local file="$1" field="$2" required="${3:-true}"
    if grep -qE "^${field}:\s" "$file"; then
        check_pass
    else
        if [[ "$required" == "true" ]]; then
            check_fail "frontmatter-$field" "HIGH" "Missing required field: $field"
        else
            check_warn "frontmatter-$field" "Missing optional field: $field"
        fi
    fi
}

check_fm_description_length() {
    local file="$1"
    local desc
    desc=$(grep -E "^description:\s" "$file" | head -1 | sed 's/^description:\s*//')
    local len=${#desc}
    if [[ $len -ge 20 ]]; then check_pass; else check_fail "frontmatter-description-length" "HIGH" "Description length $len < 20"; fi
}

check_fm_no_version() {
    grep -qE "^version:\s" "$1" && check_fail "frontmatter-no-version" "MEDIUM" "Contains deprecated version field" || check_pass
}

check_fm_metadata() {
    grep -qE "^metadata:" "$1" && check_pass || check_warn "frontmatter-metadata" "Missing metadata field (recommended)"
}

check_fm_context() {
    if grep -qE "^context:\s" "$1"; then
        check_pass
        local ctx
        ctx=$(grep -E "^context:\s" "$1" | head -1 | sed -e 's/^context:\s*//' -e 's/[[:space:]]*$//')
        if [[ "$ctx" != "fork" && "$ctx" != "merge" && "$ctx" != "edit" ]]; then
            check_warn "frontmatter-context-value" "Context value is '$ctx', not a standard value (fork/merge/edit)"
        fi
    else
        check_warn "frontmatter-context" "Missing context field (recommended)"
    fi
}

check_fm_allowed_tools() {
    if grep -qE "^allowed-tools:" "$1"; then
        check_pass
        local line
        line=$(grep -E "^allowed-tools:" "$1" | head -1)
        local len=${#line}
        if [[ $len -lt 20 ]]; then
            check_warn "frontmatter-allowed-tools-value" "allowed-tools declaration too short ($len chars), may be empty"
        fi
    else
        check_warn "frontmatter-allowed-tools" "Missing allowed-tools field (violates least privilege principle)"
    fi
}

check_fm_metadata_category() {
    grep -qE "category:" "$1" && check_pass || check_warn "frontmatter-category" "Missing metadata.category field"
}

# --- Section structure check ---

check_section() {
    local file="$1" name="$2" required="${3:-true}"
    if grep -qE "^##\s+${name}" "$file"; then
        check_pass
    else
        if [[ "$required" == "true" ]]; then
            check_fail "section-$name" "HIGH" "Missing required section: $name"
        else
            check_warn "section-$name" "Missing optional section: $name"
        fi
    fi
}

check_hard_constraints_section() {
    local file="$1"
    if grep -qE "^##\s+Hard\s*Constraints" "$file"; then
        check_pass
        local count
        count=$(grep -cE "^\s*[0-9]+\.|^\s*-\s" <(sed -n '/^## Hard Constraints/,/^## /p' "$file" 2>/dev/null))
        [[ $count -ge 2 ]] && check_pass || check_warn "hard-constraints-count" "Hard constraints count < 2"
    else
        check_warn "section-hard-constraints" "Missing Hard Constraints section (recommended)"
    fi
}

# --- Agent prompt check ---

check_agent_prompt() {
    local file="$1"
    if grep -qE "^##\s+(Agent Prompt|Agent 提示词)" "$file"; then
        check_pass
        local subs=("Skip Conditions" "Role Definition" "Core Capabilities" "Execution Flow" "Constraints" "Output Specification")
        for s in "${subs[@]}"; do
            if grep -qE "^\s*###\s+${s}" "$file"; then
                check_pass
            else
                check_warn "agent-prompt-$s" "Missing Agent Prompt subsection: $s"
            fi
        done
    else
        check_fail "agent-prompt" "HIGH" "Missing required Agent Prompt section"
    fi
}

# --- Content depth check ---

check_last_updated_freshness() {
    local file="$1"
    local last_date
    last_date=$(grep -oE 'Last updated[:\s]+[0-9]{4}-[0-9]{2}-[0-9]{2}' "$file" | head -1 | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}')
    if [[ -n "$last_date" ]]; then
        local file_epoch now_epoch diff_days
        file_epoch=$(date -j -f "%Y-%m-%d" "$last_date" "+%s" 2>/dev/null || date -d "$last_date" "+%s" 2>/dev/null)
        now_epoch=$(date "+%s")
        diff_days=$(( (now_epoch - file_epoch) / 86400 ))
        if [[ $diff_days -le 90 ]]; then
            check_pass
        else
            check_fail "content-freshness" "LOW" "Last updated ${diff_days} days ago, exceeds 90-day threshold"
        fi
    else
        check_warn "content-last-updated" "Missing last updated date"
    fi
}

check_content_examples() {
    local count
    count=$(grep -ciE "example|use.case" "$1" || echo "0")
    if [[ $count -ge 3 ]]; then check_pass
    elif [[ $count -ge 1 ]]; then check_warn "content-examples" "Only $count example references (recommend >=3)"
    else check_fail "content-examples" "MEDIUM" "Missing usage examples"; fi
}

check_content_error_handling() {
    grep -qE "error.handling|troubleshooting|FAQ|edge.case" "$1" && check_pass || check_warn "content-error-handling" "Missing error handling guidance"
}

check_content_best_practices() {
    grep -qE "best.?practice" "$1" && check_pass || check_warn "content-best-practices" "Missing best practices section"
}

check_cross_skill_handoff() {
    local count
    count=$(grep -ciE "handoff|upstream|downstream|dependency" "$1" || echo "0")
    if [[ $count -ge 1 ]]; then check_pass; else check_warn "cross-skill-handoff" "No cross-skill handoff points mentioned"; fi
}

check_common_edge_cases() {
    local skill_dir
    skill_dir=$(dirname "$1")
    if [[ -f "$skill_dir/references/common-edge-cases.md" ]]; then
        check_pass
    else
        check_warn "common-edge-cases" "Missing references/common-edge-cases.md"
    fi
}

check_automated_check_script() {
    local skill_dir
    skill_dir=$(dirname "$1")
    if [[ -f "$skill_dir/references/automated-check-script.sh" ]]; then
        check_pass
        [[ -x "$skill_dir/references/automated-check-script.sh" ]] && check_pass || check_warn "automation-script" "automated-check-script.sh is not executable"
    else
        check_warn "automation-script" "Missing references/automated-check-script.sh"
    fi
}

# --- Markdown format check ---

check_markdown_headings() {
    grep -qE "^#\s+" "$1" && check_pass || check_warn "Markdown-H1" "Missing H1 heading"
}

check_markdown_code_blocks() {
    local count
    count=$(grep -c '^\s*```' "$1" 2>/dev/null || echo "0")
    (( count % 2 == 0 )) && check_pass || check_fail "Markdown-code-blocks" "MEDIUM" "Code blocks not paired ($count markers)"
}

# --- Self-reference detection ---

check_no_self_ref() {
    local name
    name=$(grep -E "^name:\s" "$1" | head -1 | sed 's/^name:\s*//')
    local count
    count=$(grep -c "$name" "$1" 2>/dev/null || echo "0")
    [[ $count -le 3 ]] && check_pass || check_warn "self-reference" "Possible self-reference ($count times)"
}

# --- Cross-skill reference check ---

check_skill_refs() {
    local refs missing=0
    refs=$(grep -oE "harness-[a-z-]+" "$1" 2>/dev/null | sort -u || true)
    while IFS= read -r ref; do
        [[ -z "$ref" || "$ref" == "harness-" ]] && continue
        [[ -d "$SKILLS_DIR/$ref" ]] || { check_warn "skill-reference" "Reference does not exist: $ref"; ((missing++)); }
    done <<< "$refs"
    [[ $missing -eq 0 ]] && check_pass
}

# --- Main assessment ---

assess_skill() {
    local skill="$1" file="$SKILLS_DIR/$1/SKILL.md"
    echo "0 0 0 0 0" > "$STATS_FILE"
    echo "0" > "$SCORE_FILE"
    echo "[]" > "$ISSUES_FILE"
    echo "[]" > "$WARNINGS_FILE"

    # File structure check
    check_file_exists "$file" || return 1
    check_file_readable "$file"
    check_file_encoding "$file"

    # Frontmatter deep check
    check_fm_field "$file" "name"
    check_fm_field "$file" "description"
    check_fm_field "$file" "when_to_use"
    check_fm_field "$file" "compatibility"    # Was optional, now required
    check_fm_field "$file" "context" "false"
    check_fm_field "$file" "agent" "false"
    check_fm_no_version "$file"
    check_fm_metadata "$file"
    check_fm_context "$file"
    check_fm_allowed_tools "$file"
    check_fm_metadata_category "$file"
    check_fm_description_length "$file"

    # Section structure check (including hard constraints)
    for s in "Core Principles" "When to Use" "When Not to Use" "Methodology" "Key Points" "Common Pitfalls" "Edge Case Handling"; do
        check_section "$file" "$s"
    done
    check_hard_constraints_section "$file"
    check_agent_prompt "$file"

    # Markdown format check
    check_markdown_headings "$file"
    check_markdown_code_blocks "$file"

    # Content depth check
    check_content_examples "$file"
    check_content_error_handling "$file"
    check_content_best_practices "$file"
    check_last_updated_freshness "$file"

    # Cross-skill check
    check_cross_skill_handoff "$file"
    check_common_edge_cases "$file"
    check_automated_check_script "$file"

    # Reference check
    check_no_self_ref "$file"
    check_skill_refs "$file"

    # Calculate weighted score
    get_stats
    # score already maintained by weighted model, map to 0-10
    local max_possible=$total
    local weighted_score=0
    if [[ $total -gt 0 ]]; then
        weighted_score=$(echo "scale=2; $score * 10 / $total" | bc 2>/dev/null || echo "0")
    fi
    # Clamp result range
    if (( $(echo "$weighted_score > 10" | bc -l 2>/dev/null) )); then weighted_score=10; fi
    if (( $(echo "$weighted_score < 0" | bc -l 2>/dev/null) )); then weighted_score=0; fi

    local grade
    if (( $(echo "$weighted_score >= 9.5" | bc -l 2>/dev/null || echo 0) )); then grade="A+"
    elif (( $(echo "$weighted_score >= 9.0" | bc -l 2>/dev/null || echo 0) )); then grade="A"
    elif (( $(echo "$weighted_score >= 8.5" | bc -l 2>/dev/null || echo 0) )); then grade="B+"
    elif (( $(echo "$weighted_score >= 8.0" | bc -l 2>/dev/null || echo 0) )); then grade="B"
    elif (( $(echo "$weighted_score >= 7.0" | bc -l 2>/dev/null || echo 0) )); then grade="C"
    elif (( $(echo "$weighted_score >= 6.0" | bc -l 2>/dev/null || echo 0) )); then grade="D"
    else grade="F"; fi

    python3 -c "
import json, sys
issues = json.load(open('$ISSUES_FILE'))
warnings = json.load(open('$WARNINGS_FILE'))
result = {
    'skill_name': sys.argv[1],
    'auto_check_score': float(sys.argv[2]),
    'weighted_score': float(sys.argv[2]),
    'grade': sys.argv[3],
    'scoring_model': 'weighted (CRITICAL=5, HIGH=3, MEDIUM=2, LOW=1, WARN=0)',
    'stats': {'total_checks': int(sys.argv[4]), 'passed': int(sys.argv[5]), 'failed': int(sys.argv[6]), 'warnings': int(sys.argv[7]), 'penalty_score': int(sys.argv[8])},
    'issues': issues,
    'warnings': warnings
}
json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
" "$skill" "$weighted_score" "$grade" "$total" "$passed" "$failed" "$warnings" "$score"
}

assess_all() {
    local skills=()
    for d in "$SKILLS_DIR"/*/; do
        [[ -f "$d/SKILL.md" ]] && skills+=("$(basename "$d")")
    done

    local all_results="$RESULTS_DIR/all.json"
    echo "[]" > "$all_results"
    local total_score=0 count=0

    for skill in "${skills[@]}"; do
        local result
        result=$(assess_skill "$skill" 2>/dev/null) || continue
        local tmp
        tmp=$(mktemp)
        python3 -c "
import json, sys
with open('$all_results') as f: data = json.load(f)
data.append(json.loads(sys.stdin.read()))
with open('$tmp', 'w') as f: json.dump(data, f, ensure_ascii=False)
" <<< "$result"
        mv "$tmp" "$all_results"
        local s
        s=$(echo "$result" | grep -oE '"weighted_score": [0-9.]+' | grep -oE '[0-9.]+')
        total_score=$(echo "$total_score + ${s:-0}" | bc 2>/dev/null || echo "0")
        ((count++)) || true
    done

    local avg=0
    [[ $count -gt 0 ]] && avg=$(echo "scale=2; $total_score / $count" | bc 2>/dev/null || echo "0")

    # Common issues analysis
    python3 -c "
import json, sys
results = json.load(open('$all_results'))
output = {
    'evaluation_date': '$(date -u +%Y-%m-%dT%H:%M:%SZ)',
    'total_skills': len(results),
    'average_score': float(sys.argv[1]),
    'scoring_model': 'weighted (CRITICAL=5, HIGH=3, MEDIUM=2, LOW=1, WARN=0)',
    'results': results
}
json.dump(output, sys.stdout, ensure_ascii=False, indent=2)
" "$avg"
}

# --- Entry point ---
target="${1:-all}"
if [[ "$target" == "all" ]]; then
    assess_all
else
    [[ -d "$SKILLS_DIR/$target" ]] || { echo "{\"error\": \"Skill not found: $target\"}" >&2; exit 1; }
    assess_skill "$target"
fi
