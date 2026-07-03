#!/bin/bash
# Skills质量评估 - 自动化检查脚本（优化版）
# 用法: bash automated-check-script.sh [skill-name|all]
# 输出: JSON格式的检查结果

# 确保 UTF-8 支持
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

SKILLS_DIR="${SKILLS_DIR:-./skills}"

# 临时文件用于收集结果
TMPDIR="${TMPDIR:-/tmp}"
RESULTS_DIR=$(mktemp -d "$TMPDIR/skill-check-XXXXXX")
ISSUES_FILE="$RESULTS_DIR/issues.json"
WARNINGS_FILE="$RESULTS_DIR/warnings.json"
STATS_FILE="$RESULTS_DIR/stats.txt"

cleanup() { rm -rf "$RESULTS_DIR"; }
trap cleanup EXIT

echo "[]" > "$ISSUES_FILE"
echo "[]" > "$WARNINGS_FILE"
echo "0 0 0 0" > "$STATS_FILE"

# --- 工具函数 ---

get_stats() {
    read -r total passed failed warnings < "$STATS_FILE"
}

update_stats() {
    local total passed failed warnings
    read -r total passed failed warnings < "$STATS_FILE"
    echo "$((total+1)) $((passed+1)) $failed $warnings" > "$STATS_FILE"
}

update_stats_fail() {
    local total passed failed warnings
    read -r total passed failed warnings < "$STATS_FILE"
    echo "$((total+1)) $passed $((failed+1)) $warnings" > "$STATS_FILE"
}

update_stats_warn() {
    local total passed failed warnings
    read -r total passed failed warnings < "$STATS_FILE"
    echo "$((total+1)) $passed $failed $((warnings+1))" > "$STATS_FILE"
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
check_fail() { update_stats_fail; add_issue "$1" "$3" "$2"; }
check_warn() { update_stats_warn; add_warning "$1" "$2"; }

# --- 检查函数 ---

check_file_exists() {
    local f="$1"
    if [[ -f "$f" ]]; then check_pass; else check_fail "文件存在" "CRITICAL" "SKILL.md 不存在: $f"; return 1; fi
}

check_file_readable() { [[ -r "$1" ]] && check_pass || check_fail "文件可读" "CRITICAL" "文件不可读"; }

check_file_encoding() {
    local enc
    enc=$(file -b --mime-encoding "$1" 2>/dev/null || echo "unknown")
    [[ "$enc" == "utf-8" || "$enc" == "ascii" ]] && check_pass || check_warn "文件编码" "编码为 $enc，建议 UTF-8"
}

check_fm_field() {
    local file="$1" field="$2" required="${3:-true}"
    if grep -qE "^${field}:\s" "$file"; then
        check_pass
    else
        if [[ "$required" == "true" ]]; then
            check_fail "frontmatter-$field" "HIGH" "缺少 $field 字段"
        else
            check_warn "frontmatter-$field" "缺少 $field 字段"
        fi
    fi
}

check_fm_description_length() {
    local file="$1"
    local desc
    desc=$(grep -E "^description:\s" "$file" | head -1 | sed 's/^description:\s*//')
    local len=${#desc}
    if [[ $len -ge 20 ]]; then check_pass; else check_fail "frontmatter-description长度" "HIGH" "description 长度 $len < 20"; fi
}

check_fm_no_version() {
    grep -qE "^version:\s" "$1" && check_fail "frontmatter-no-version" "MEDIUM" "包含废弃 version 字段" || check_pass
}

check_fm_metadata() {
    grep -qE "^metadata:" "$1" && check_pass || check_warn "frontmatter-metadata" "缺少 metadata 字段"
}

check_section() {
    local file="$1" name="$2" required="${3:-true}"
    if grep -qE "^##\s+${name}" "$file"; then
        check_pass
    else
        if [[ "$required" == "true" ]]; then
            check_fail "section-$name" "HIGH" "缺少必需章节: $name"
        else
            check_warn "section-$name" "缺少可选章节: $name"
        fi
    fi
}

check_agent_prompt() {
    local file="$1"
    if grep -qE "^##\s+Agent 提示词" "$file"; then
        check_pass
        local sections=("角色定义" "核心能力" "执行流程" "约束" "输出规范")
        for s in "${sections[@]}"; do
            grep -qE "^\s*##?\s+${s}" "$file" && check_pass || check_warn "Agent提示词-$s" "缺少 $s 子节"
        done
    else
        check_warn "Agent提示词" "缺少 Agent 提示词 章节"
    fi
}

check_markdown_headings() {
    grep -qE "^#\s+" "$1" && check_pass || check_warn "Markdown-H1" "缺少 H1 标题"
}

check_markdown_code_blocks() {
    local count
    count=$(grep -c '^\s*```' "$1" 2>/dev/null || echo "0")
    (( count % 2 == 0 )) && check_pass || check_fail "Markdown-代码块" "MEDIUM" "代码块未配对 ($count 个标记)"
}

check_content_examples() {
    local count
    count=$(grep -ciE "示例|example|用例" "$1" || echo "0")
    if [[ $count -ge 2 ]]; then check_pass
    elif [[ $count -ge 1 ]]; then check_warn "内容-示例" "仅 $count 个示例引用"
    else check_fail "内容-示例" "MEDIUM" "缺少使用示例"; fi
}

check_content_error_handling() {
    grep -qE "错误处理|故障排除|常见问题|边界情况" "$1" && check_pass || check_warn "内容-错误处理" "缺少错误处理指导"
}

check_content_best_practices() {
    grep -qE "最佳实践|best.?practice" "$1" && check_pass || check_warn "内容-最佳实践" "缺少最佳实践章节"
}

check_content_last_updated() {
    grep -qE "最后更新|Last.?Updated" "$1" && check_pass || check_warn "内容-最后更新" "缺少最后更新日期"
}

check_no_self_ref() {
    local name
    name=$(grep -E "^name:\s" "$1" | head -1 | sed 's/^name:\s*//')
    local count
    count=$(grep -c "$name" "$1" 2>/dev/null || echo "0")
    [[ $count -le 2 ]] && check_pass || check_warn "自引用检测" "可能的自引用 ($count 次)"
}

check_skill_refs() {
    local refs missing=0
    refs=$(grep -oE "harness-[a-z-]+" "$1" 2>/dev/null | sort -u || true)
    while IFS= read -r ref; do
        [[ -z "$ref" || "$ref" == "harness-" ]] && continue
        [[ -d "$SKILLS_DIR/$ref" ]] || { check_warn "Skill引用" "引用不存在: $ref"; ((missing++)); }
    done <<< "$refs"
    [[ $missing -eq 0 ]] && check_pass
}

# --- 主评估 ---

assess_skill() {
    local skill="$1" file="$SKILLS_DIR/$1/SKILL.md"
    echo "0 0 0 0" > "$STATS_FILE"
    echo "[]" > "$ISSUES_FILE"
    echo "[]" > "$WARNINGS_FILE"

    check_file_exists "$file" || return 1
    check_file_readable "$file"
    check_file_encoding "$file"

    check_fm_field "$file" "name"
    check_fm_field "$file" "description"
    check_fm_field "$file" "when_to_use"
    check_fm_field "$file" "compatibility" "false"
    check_fm_no_version "$file"
    check_fm_metadata "$file"
    check_fm_description_length "$file"

    for s in "核心原则" "何时使用" "何时不该用" "方法论" "关键要点" "常见陷阱" "边界情况处理" "最佳实践"; do
        check_section "$file" "$s"
    done
    check_agent_prompt "$file"

    check_markdown_headings "$file"
    check_markdown_code_blocks "$file"

    check_content_examples "$file"
    check_content_error_handling "$file"
    check_content_best_practices "$file"
    check_content_last_updated "$file"

    check_no_self_ref "$file"
    check_skill_refs "$file"

    get_stats
    local score
    score=$(echo "scale=2; $passed / $total * 10" | bc 2>/dev/null || echo "0")
    local grade
    if (( $(echo "$score >= 9.5" | bc -l 2>/dev/null || echo 0) )); then grade="A+"
    elif (( $(echo "$score >= 9.0" | bc -l 2>/dev/null || echo 0) )); then grade="A"
    elif (( $(echo "$score >= 8.5" | bc -l 2>/dev/null || echo 0) )); then grade="B+"
    elif (( $(echo "$score >= 8.0" | bc -l 2>/dev/null || echo 0) )); then grade="B"
    elif (( $(echo "$score >= 7.0" | bc -l 2>/dev/null || echo 0) )); then grade="C"
    elif (( $(echo "$score >= 6.0" | bc -l 2>/dev/null || echo 0) )); then grade="D"
    else grade="F"; fi

    python3 -c "
import json, sys
issues = json.load(open('$ISSUES_FILE'))
warnings = json.load(open('$WARNINGS_FILE'))
result = {
    'skill_name': sys.argv[1],
    'auto_check_score': float(sys.argv[2]),
    'grade': sys.argv[3],
    'stats': {'total_checks': int(sys.argv[4]), 'passed': int(sys.argv[5]), 'failed': int(sys.argv[6]), 'warnings': int(sys.argv[7])},
    'issues': issues,
    'warnings': warnings
}
json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
" "$skill" "$score" "$grade" "$total" "$passed" "$failed" "$warnings"
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
        s=$(echo "$result" | grep -oE '"auto_check_score": [0-9.]+' | grep -oE '[0-9.]+')
        total_score=$(echo "$total_score + ${s:-0}" | bc)
        ((count++)) || true
    done

    local avg=0
    [[ $count -gt 0 ]] && avg=$(echo "scale=2; $total_score / $count" | bc)

    python3 -c "
import json, sys
results = json.load(open('$all_results'))
output = {
    'evaluation_date': '$(date -u +%Y-%m-%dT%H:%M:%SZ)',
    'total_skills': len(results),
    'average_score': float(sys.argv[1]),
    'results': results
}
json.dump(output, sys.stdout, ensure_ascii=False, indent=2)
" "$avg"
}

# --- 入口 ---
target="${1:-all}"
if [[ "$target" == "all" ]]; then
    assess_all
else
    [[ -d "$SKILLS_DIR/$target" ]] || { echo "{\"error\": \"Skill not found: $target\"}" >&2; exit 1; }
    assess_skill "$target"
fi
