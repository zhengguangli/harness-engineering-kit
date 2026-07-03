#!/bin/bash
# Skills质量评估 - 自动化检查脚本（v2.0 加权评分版）
# 用法: bash automated-check-script.sh [skill-name|all]
# 输出: JSON格式的检查结果，含加权评分

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
SCORE_FILE="$RESULTS_DIR/score.txt"

cleanup() { rm -rf "$RESULTS_DIR"; }
trap cleanup EXIT

echo "[]" > "$ISSUES_FILE"
echo "[]" > "$WARNINGS_FILE"
echo "0 0 0 0 0" > "$STATS_FILE"
echo "0" > "$SCORE_FILE"

# --- 加权评分模型 ---
# CRITICAL=5, HIGH=3, MEDIUM=2, LOW=1, WARN=0

# --- 工具函数 ---

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

# --- 文件结构检查 ---

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

# --- Frontmatter 深度检查 ---

check_fm_field() {
    local file="$1" field="$2" required="${3:-true}"
    if grep -qE "^${field}:\s" "$file"; then
        check_pass
    else
        if [[ "$required" == "true" ]]; then
            check_fail "frontmatter-$field" "HIGH" "缺少必需字段: $field"
        else
            check_warn "frontmatter-$field" "缺少可选字段: $field"
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
    grep -qE "^metadata:" "$1" && check_pass || check_warn "frontmatter-metadata" "缺少 metadata 字段（推荐）"
}

check_fm_context() {
    if grep -qE "^context:\s" "$1"; then
        check_pass
        local ctx
        ctx=$(grep -E "^context:\s" "$1" | head -1 | sed 's/^context:\s*//')
        if [[ "$ctx" != "fork" && "$ctx" != "merge" && "$ctx" != "edit" ]]; then
            check_warn "frontmatter-context值" "context值为 '$ctx'，非标准值(fork/merge/edit)"
        fi
    else
        check_warn "frontmatter-context" "缺少 context 字段（推荐）"
    fi
}

check_fm_allowed_tools() {
    if grep -qE "^allowed-tools:" "$1"; then
        check_pass
        local line
        line=$(grep -E "^allowed-tools:" "$1" | head -1)
        local len=${#line}
        if [[ $len -lt 20 ]]; then
            check_warn "frontmatter-allowed-tools值" "allowed-tools 声明过短($len字符)，可能是空声明"
        fi
    else
        check_warn "frontmatter-allowed-tools" "缺少 allowed-tools 字段（不符合最小权限原则）"
    fi
}

check_fm_metadata_category() {
    grep -qE "category:" "$1" && check_pass || check_warn "frontmatter-category" "缺少 metadata.category 字段"
}

# --- 章节结构检查 ---

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

check_hard_constraints_section() {
    local file="$1"
    if grep -qE "^##\s+(硬约束|Hard.Constraints)" "$file"; then
        check_pass
        local count
        count=$(grep -cE "^\s*[0-9]+\.|^\s*-\s" <(sed -n '/^## 硬约束/,/^## /p' "$file" 2>/dev/null))
        [[ $count -ge 2 ]] && check_pass || check_warn "硬约束-数量" "硬约束数量 < 2 条"
    else
        check_warn "section-硬约束" "缺少硬约束章节（推荐）"
    fi
}

# --- Agent 提示词检查 ---

check_agent_prompt() {
    local file="$1"
    if grep -qE "^##\s+Agent 提示词" "$file"; then
        check_pass
        local subs=("跳过条件" "角色定义" "核心能力" "执行流程" "约束" "输出规范")
        for s in "${subs[@]}"; do
            if grep -qE "^\s*###\s+${s}" "$file"; then
                check_pass
            else
                check_warn "Agent提示词-$s" "缺少 Agent 提示词子节: $s"
            fi
        done
    else
        check_fail "Agent提示词" "HIGH" "缺少必含 Agent 提示词 章节"
    fi
}

# --- 内容深度检查 ---

check_last_updated_freshness() {
    local file="$1"
    local last_date
    last_date=$(grep -oE '最后更新[:\s]+[0-9]{4}-[0-9]{2}-[0-9]{2}' "$file" | head -1 | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}')
    if [[ -n "$last_date" ]]; then
        local file_epoch now_epoch diff_days
        file_epoch=$(date -j -f "%Y-%m-%d" "$last_date" "+%s" 2>/dev/null || date -d "$last_date" "+%s" 2>/dev/null)
        now_epoch=$(date "+%s")
        diff_days=$(( (now_epoch - file_epoch) / 86400 ))
        if [[ $diff_days -le 90 ]]; then
            check_pass
        else
            check_fail "内容-新鲜度" "LOW" "最后更新距今 ${diff_days} 天，超过 90 天阈值"
        fi
    else
        check_warn "内容-最后更新" "缺少最后更新日期"
    fi
}

check_content_examples() {
    local count
    count=$(grep -ciE "示例|example|用例" "$1" || echo "0")
    if [[ $count -ge 3 ]]; then check_pass
    elif [[ $count -ge 1 ]]; then check_warn "内容-示例" "仅 $count 个示例引用（建议 ≥3）"
    else check_fail "内容-示例" "MEDIUM" "缺少使用示例"; fi
}

check_content_error_handling() {
    grep -qE "错误处理|故障排除|常见问题|边界情况" "$1" && check_pass || check_warn "内容-错误处理" "缺少错误处理指导"
}

check_content_best_practices() {
    grep -qE "最佳实践|best.?practice" "$1" && check_pass || check_warn "内容-最佳实践" "缺少最佳实践章节"
}

check_cross_skill_handoff() {
    local count
    count=$(grep -ciE "交接|handoff|上游|下游|依赖" "$1" || echo "0")
    if [[ $count -ge 1 ]]; then check_pass; else check_warn "跨skill交接" "未提及跨skill交接点"; fi
}

check_common_edge_cases() {
    local skill_dir
    skill_dir=$(dirname "$(dirname "$1")")
    if [[ -f "$skill_dir/references/common-edge-cases.md" ]]; then
        check_pass
    else
        check_warn "common-edge-cases" "缺少 references/common-edge-cases.md"
    fi
}

check_automated_check_script() {
    local skill_dir
    skill_dir=$(dirname "$(dirname "$1")")
    if [[ -f "$skill_dir/references/automated-check-script.sh" ]]; then
        check_pass
        [[ -x "$skill_dir/references/automated-check-script.sh" ]] && check_pass || check_warn "自动化脚本" "automated-check-script.sh 不可执行"
    else
        check_warn "自动化脚本" "缺少 references/automated-check-script.sh"
    fi
}

# --- Markdown 格式检查 ---

check_markdown_headings() {
    grep -qE "^#\s+" "$1" && check_pass || check_warn "Markdown-H1" "缺少 H1 标题"
}

check_markdown_code_blocks() {
    local count
    count=$(grep -c '^\s*```' "$1" 2>/dev/null || echo "0")
    (( count % 2 == 0 )) && check_pass || check_fail "Markdown-代码块" "MEDIUM" "代码块未配对 ($count 个标记)"
}

# --- 自引用检测 ---

check_no_self_ref() {
    local name
    name=$(grep -E "^name:\s" "$1" | head -1 | sed 's/^name:\s*//')
    local count
    count=$(grep -c "$name" "$1" 2>/dev/null || echo "0")
    [[ $count -le 3 ]] && check_pass || check_warn "自引用检测" "可能的自引用 ($count 次)"
}

# --- 跨skill引用检查 ---

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
    echo "0 0 0 0 0" > "$STATS_FILE"
    echo "0" > "$SCORE_FILE"
    echo "[]" > "$ISSUES_FILE"
    echo "[]" > "$WARNINGS_FILE"

    # 文件结构检查
    check_file_exists "$file" || return 1
    check_file_readable "$file"
    check_file_encoding "$file"

    # Frontmatter 深度检查
    check_fm_field "$file" "name"
    check_fm_field "$file" "description"
    check_fm_field "$file" "when_to_use"
    check_fm_field "$file" "compatibility"    # 原为可选，现改为必需
    check_fm_field "$file" "context" "false"
    check_fm_field "$file" "agent" "false"
    check_fm_no_version "$file"
    check_fm_metadata "$file"
    check_fm_context
    check_fm_allowed_tools
    check_fm_metadata_category
    check_fm_description_length "$file"

    # 章节结构检查（含硬约束）
    for s in "核心原则" "何时使用" "何时不该用" "方法论" "关键要点" "常见陷阱" "边界情况处理"; do
        check_section "$file" "$s"
    done
    check_hard_constraints_section "$file"
    check_agent_prompt "$file"

    # Markdown 格式检查
    check_markdown_headings "$file"
    check_markdown_code_blocks "$file"

    # 内容深度检查
    check_content_examples "$file"
    check_content_error_handling "$file"
    check_content_best_practices "$file"
    check_last_updated_freshness "$file"

    # 跨技能检查
    check_cross_skill_handoff "$file"
    check_common_edge_cases "$file"
    check_automated_check_script "$file"

    # 引用检查
    check_no_self_ref "$file"
    check_skill_refs "$file"

    # 计算加权得分
    get_stats
    # score 已由加权模型维护，映射到 0-10 分
    local max_possible=$total
    local weighted_score=0
    if [[ $total -gt 0 ]]; then
        weighted_score=$(echo "scale=2; $score * 10 / $total" | bc 2>/dev/null || echo "0")
    fi
    # 保证结果范围
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

    # 共性问题分析
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

# --- 入口 ---
target="${1:-all}"
if [[ "$target" == "all" ]]; then
    assess_all
else
    [[ -d "$SKILLS_DIR/$target" ]] || { echo "{\"error\": \"Skill not found: $target\"}" >&2; exit 1; }
    assess_skill "$target"
fi
