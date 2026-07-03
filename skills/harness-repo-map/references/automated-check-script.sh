#!/bin/bash
# Repo Map 自动化检查脚本（优化版）
# 用法: bash automation-check-script.sh [project-root]
# 检查: 断链检测、新鲜度检测、覆盖率检测、结构检测
# 输出: JSON格式的检查结果

# 不使用 set -e，因为 grep 无匹配时返回 1 会导致脚本退出

PROJECT_ROOT="${1:-.}"
DOCS_DIR="$PROJECT_ROOT/docs"
AGENTS_FILE="$PROJECT_ROOT/AGENTS.md"
REPORT_FORMAT="${REPORT_FORMAT:-json}"  # json 或 text

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 计数器
TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0
WARNINGS=0

# 结果收集
declare -a ISSUES=()
declare -a WARNINGS_LIST=()

# --- 工具函数 ---

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1" >&2
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1" >&2
    ((WARNINGS++)) || true
}

log_error() {
    echo -e "${RED}[FAIL]${NC} $1" >&2
}

check_pass() {
    ((TOTAL_CHECKS++)) || true
    ((PASSED_CHECKS++)) || true
    log_info "PASS: $1"
}

check_fail() {
    local severity="${2:-HIGH}"
    ((TOTAL_CHECKS++)) || true
    ((FAILED_CHECKS++)) || true
    ISSUES+=("{\"check\":\"$1\",\"severity\":\"$severity\",\"detail\":\"$3\"}")
    log_error "FAIL [$severity]: $1 - $3"
}

check_warn() {
    ((TOTAL_CHECKS++)) || true
    ((WARNINGS++)) || true
    WARNINGS_LIST+=("{\"check\":\"$1\",\"detail\":\"$2\"}")
    log_warn "WARN: $1 - $2"
}

# --- 检查1: AGENTS.md 健康检查 ---

check_agents_md() {
    log_info "=== AGENTS.md 健康检查 ==="
    
    if [[ ! -f "$AGENTS_FILE" ]]; then
        check_fail "AGENTS.md存在性" "CRITICAL" "AGENTS.md 文件不存在"
        return 1
    fi
    check_pass "AGENTS.md存在性"
    
    # 行数检查
    local line_count
    line_count=$(wc -l < "$AGENTS_FILE" | tr -d ' ')
    if [[ $line_count -le 100 ]]; then
        check_pass "AGENTS.md行数(≤100行)=$line_count"
    else
        check_fail "AGENTS.md行数" "HIGH" "AGENTS.md 有 $line_count 行，超过 100 行限制"
    fi
    
    # 导航表检查：检查是否有指向 docs/ 的链接
    local nav_links
    nav_links=$( (grep -coE '\]\(docs/[^)]+\)' "$AGENTS_FILE" 2>/dev/null || echo "0") | head -1 | tr -d '[:space:]' )
    nav_links="${nav_links:-0}"
    if [[ "$nav_links" -ge 3 ]] 2>/dev/null; then
        check_pass "AGENTS.md导航链接(≥3)=$nav_links"
    else
        check_warn "AGENTS.md导航链接" "仅有 $nav_links 个 docs/ 链接，建议增加导航表"
    fi
    
    # 地图声明检查
    if grep -qiE "地图|table.?of.?contents|不是百科全书" "$AGENTS_FILE"; then
        check_pass "AGENTS.md地图声明"
    else
        check_warn "AGENTS.md地图声明" "建议在顶部声明'这个文件是地图，不是百科全书'"
    fi
}

# --- 检查2: docs/ 结构检测 ---

check_docs_structure() {
    log_info "=== docs/ 结构检测 ==="
    
    if [[ ! -d "$DOCS_DIR" ]]; then
        check_fail "docs/目录存在性" "HIGH" "docs/ 目录不存在"
        return 1
    fi
    check_pass "docs/目录存在性"
    
    # 文件数量
    local file_count
    file_count=$(find "$DOCS_DIR" -type f | wc -l | tr -d ' ')
    if [[ $file_count -ge 3 ]]; then
        check_pass "docs/文件数量(≥3)=$file_count"
    else
        check_warn "docs/文件数量" "仅有 $file_count 个文件，建议补充文档"
    fi
    
    # 检查推荐目录结构
    local required_dirs=("design-docs" "exec-plans")
    for dir in "${required_dirs[@]}"; do
        if [[ -d "$DOCS_DIR/$dir" ]]; then
            check_pass "docs/$dir/目录存在"
        else
            check_warn "docs/$dir/目录" "推荐目录 $dir/ 不存在"
        fi
    done
    
    # 检查关键文件
    local required_files=("ARCHITECTURE.md" "QUALITY_SCORE.md")
    for req_file in "${required_files[@]}"; do
        if [[ -f "$DOCS_DIR/$req_file" ]]; then
            check_pass "docs/$req_file存在"
        else
            check_warn "docs/$req_file" "推荐文件 $req_file 不存在"
        fi
    done
    
    # 检查孤立文档（无入链的文档）
    check_orphan_documents
}

check_orphan_documents() {
    local orphan_count=0
    local all_md_files
    all_md_files=$(find "$DOCS_DIR" -name "*.md" -type f 2>/dev/null || true)
    
    [[ -z "$all_md_files" ]] && { check_pass "孤立文档检测(无文档)"; return; }
    
    while IFS= read -r md_file; do
        [[ -z "$md_file" ]] && continue
        local relative_path
        relative_path=$(python3 -c "import os; print(os.path.relpath('$md_file', '$PROJECT_ROOT'))" 2>/dev/null || echo "$md_file")
        
        # 检查该文件是否被其他文件引用
        local ref_count
        ref_count=$(grep -rl "$relative_path" "$DOCS_DIR" "$AGENTS_FILE" 2>/dev/null | wc -l | tr -d ' ')
        
        if [[ $ref_count -eq 0 ]]; then
            ((orphan_count++)) || true
        fi
    done <<< "$all_md_files"
    
    if [[ $orphan_count -eq 0 ]]; then
        check_pass "孤立文档检测"
    else
        check_warn "孤立文档检测" "发现 $orphan_count 个可能的孤立文档"
    fi
}

# --- 检查3: 断链检测 ---

check_broken_links() {
    log_info "=== 断链检测 ==="
    
    local broken_count=0
    local total_links=0
    local broken_details=""
    
    # 扫描所有 .md 文件
    local md_files
    md_files=$(find "$DOCS_DIR" "$AGENTS_FILE" -name "*.md" -type f 2>/dev/null || find "$DOCS_DIR" -name "*.md" -type f)
    
    while IFS= read -r md_file; do
        [[ -z "$md_file" ]] && continue
        
        # 提取 markdown 链接: [text](url)
        local links
        links=$(grep -oE '\]\([^)]+\)' "$md_file" | sed 's/^\](//' | sed 's/)$//' || true)
        
        while IFS= read -r link; do
            [[ -z "$link" ]] && continue
            ((total_links++)) || true
            
            # 跳过外部链接和锚点
            if [[ "$link" =~ ^https?:// || "$link" =~ ^# || "$link" =~ ^mailto: ]]; then
                continue
            fi
            
            # 分离文件路径和锚点
            local file_part anchor_part
            if [[ "$link" =~ ^(.+)#(.+)$ ]]; then
                file_part="${BASH_REMATCH[1]}"
                anchor_part="${BASH_REMATCH[2]}"
            else
                file_part="$link"
                anchor_part=""
            fi
            
            # 解析相对路径
            local dir_of_file
            dir_of_file=$(dirname "$md_file")
            local target_file
            target_file=$(realpath "$dir_of_file/$file_part" 2>/dev/null || echo "")
            
            # 检查文件是否存在
            if [[ -n "$target_file" && -f "$target_file" ]]; then
                # 如果有锚点，检查锚点是否存在
                if [[ -n "$anchor_part" ]]; then
                    local anchor_found
                    anchor_found=$(grep -ciE "(^#+\s+.*${anchor_part}|^<a\s+.*id=\"${anchor_part}\"|^\s*\{#${anchor_part}\})" "$target_file" || echo "0")
                    if [[ $anchor_found -eq 0 ]]; then
                        ((broken_count++)) || true
                        broken_details+="$(basename "$md_file"): $link (锚点 #$anchor_part 不存在); "
                    fi
                fi
            else
                ((broken_count++)) || true
                broken_details+="$(basename "$md_file"): $link (目标文件不存在); "
            fi
        done <<< "$links"
    done <<< "$md_files"
    
    if [[ $broken_count -eq 0 ]]; then
        check_pass "断链检测(共$total_links个链接)"
    else
        check_fail "断链检测" "CRITICAL" "发现 $broken_count/$total_links 个断链: $broken_details"
    fi
}

# --- 检查4: 新鲜度检测 ---

check_freshness() {
    log_info "=== 新鲜度检测 ==="
    
    local stale_count=0
    local stale_files=""
    local current_date
    current_date=$(date +%s)
    local thirty_days_ago=$((current_date - 30 * 86400))
    
    local md_files
    md_files=$(find "$DOCS_DIR" -name "*.md" -type f 2>/dev/null || true)
    
    while IFS= read -r md_file; do
        [[ -z "$md_file" ]] && continue
        
        # 查找 "最后更新" 日期
        local last_updated
        last_updated=$(grep -oE "最后更新:\s*[0-9]{4}-[0-9]{2}-[0-9]{2}" "$md_file" | head -1 | grep -oE "[0-9]{4}-[0-9]{2}-[0-9]{2}" || echo "")
        
        if [[ -n "$last_updated" ]]; then
            local file_date
            file_date=$(date -j -f "%Y-%m-%d" "$last_updated" +%s 2>/dev/null || echo "0")
            
            if [[ $file_date -gt 0 && $file_date -lt $thirty_days_ago ]]; then
                ((stale_count++)) || true
                stale_files+="$(basename "$md_file")($last_updated); "
            fi
        else
            # 没有日期标记，检查文件修改时间
            local mod_time
            mod_time=$(stat -f %m "$md_file" 2>/dev/null || echo "0")
            if [[ $mod_time -lt $thirty_days_ago ]]; then
                ((stale_count++)) || true
                stale_files+="$(basename "$md_file")(无日期标记,修改时间超过30天); "
            fi
        fi
    done <<< "$md_files"
    
    if [[ $stale_count -eq 0 ]]; then
        check_pass "新鲜度检测"
    else
        check_warn "新鲜度检测" "发现 $stale_count 个过期文档: $stale_files"
    fi
}

# --- 检查5: 覆盖率检测 ---

check_coverage() {
    log_info "=== 覆盖率检测 ==="
    
    # 检查 ARCHITECTURE.md 中的领域/包列表是否与代码一致
    local arch_file="$DOCS_DIR/ARCHITECTURE.md"
    if [[ -f "$arch_file" ]]; then
        # 提取 ARCHITECTURE.md 中提到的路径
        local arch_paths
        arch_paths=$(grep -oE '`[a-zA-Z0-9_/-]+/`' "$arch_file" | tr -d '`' || true)
        
        local missing_in_code=0
        local missing_details=""
        
        while IFS= read -r path; do
            [[ -z "$path" ]] && continue
            if [[ ! -e "$PROJECT_ROOT/$path" ]]; then
                ((missing_in_code++)) || true
                missing_details+="$path; "
            fi
        done <<< "$arch_paths"
        
        if [[ $missing_in_code -eq 0 ]]; then
            check_pass "ARCHITECTURE.md代码一致性"
        else
            check_warn "ARCHITECTURE.md代码一致性" "ARCHITECTURE.md 中 $missing_in_code 个路径在代码中不存在: $missing_details"
        fi
    else
        check_warn "ARCHITECTURE.md存在性" "ARCHITECTURE.md 不存在，跳过覆盖率检测"
    fi
    
    # 检查 QUALITY_SCORE.md 是否存在且有内容
    local qs_file="$DOCS_DIR/QUALITY_SCORE.md"
    if [[ -f "$qs_file" ]]; then
        local qs_lines
        qs_lines=$(wc -l < "$qs_file" | tr -d ' ')
        if [[ $qs_lines -ge 10 ]]; then
            check_pass "QUALITY_SCORE.md内容充实度(≥10行)"
        else
            check_warn "QUALITY_SCORE.md内容充实度" "仅有 $qs_lines 行，建议补充"
        fi
    else
        check_warn "QUALITY_SCORE.md存在性" "QUALITY_SCORE.md 不存在"
    fi
}

# --- 检查6: Agent 提示词结构一致性 ---

check_agent_prompt_consistency() {
    log_info "=== Agent 提示词结构一致性 ==="
    
    local skill_files
    skill_files=$(find "$PROJECT_ROOT/skills" -name "SKILL.md" -type f 2>/dev/null || true)
    
    local inconsistent_count=0
    local inconsistent_details=""
    
    while IFS= read -r skill_file; do
        [[ -z "$skill_file" ]] && continue
        
        # 检查 frontmatter agent 字段
        local agent_name
        agent_name=$(grep -E "^agent:\s" "$skill_file" | head -1 | sed 's/^agent:\s*//' || echo "")
        
        if [[ -n "$agent_name" ]]; then
            # 检查是否有对应的 Agent 提示词 section
            if ! grep -qE "^##\s+Agent 提示词" "$skill_file"; then
                ((inconsistent_count++)) || true
                inconsistent_details+="$(basename "$(dirname "$skill_file")"): agent=$agent_name 但无 Agent 提示词 section; "
            fi
        fi
    done <<< "$skill_files"
    
    if [[ $inconsistent_count -eq 0 ]]; then
        check_pass "Agent提示词配对完整性"
    else
        check_warn "Agent提示词配对完整性" "$inconsistent_count 个不一致: $inconsistent_details"
    fi
}

# --- 检查7: 执行计划检查 ---

check_exec_plans() {
    log_info "=== 执行计划检查 ==="
    
    local active_dir="$DOCS_DIR/exec-plans/active"
    local completed_dir="$DOCS_DIR/exec-plans/completed"
    local tracker="$DOCS_DIR/exec-plans/tech-debt-tracker.md"
    
    # 检查 active 目录
    if [[ -d "$active_dir" ]]; then
        local active_count
        active_count=$(find "$active_dir" -name "*.md" -type f | wc -l | tr -d ' ')
        if [[ $active_count -ge 0 ]]; then
            check_pass "exec-plans/active/存在(当前${active_count}个)"
        fi
    else
        check_warn "exec-plans/active/目录" "exec-plans/active/ 目录不存在"
    fi
    
    # 检查 tech-debt-tracker
    if [[ -f "$tracker" ]]; then
        local tracker_lines
        tracker_lines=$(wc -l < "$tracker" | tr -d ' ')
        if [[ $tracker_lines -ge 5 ]]; then
            check_pass "tech-debt-tracker.md内容(≥5行)"
        else
            check_warn "tech-debt-tracker.md内容" "仅有 $tracker_lines 行"
        fi
    else
        check_warn "tech-debt-tracker.md存在性" "tech-debt-tracker.md 不存在"
    fi
}

# --- 主评估函数 ---

main_check() {
    log_info "Repo Map 自动化检查"
    log_info "===================="
    log_info "项目根目录: $PROJECT_ROOT"
    
    # AGENTS.md 检查
    check_agents_md
    
    # docs/ 结构检查
    check_docs_structure
    
    # 断链检测
    check_broken_links
    
    # 新鲜度检测
    check_freshness
    
    # 覆盖率检测
    check_coverage
    
    # Agent 提示词结构一致性
    check_agent_prompt_consistency
    
    # 执行计划检查
    check_exec_plans
    
    # 计算得分
    local auto_score
    if [[ $TOTAL_CHECKS -gt 0 ]]; then
        auto_score=$(echo "scale=2; ($PASSED_CHECKS / $TOTAL_CHECKS) * 10" | bc)
    else
        auto_score="0"
    fi
    
    # 构建 JSON 输出
    local issues_json="["
    local first=true
    for issue in "${ISSUES[@]}"; do
        $first || issues_json+=","
        issues_json+="$issue"
        first=false
    done
    issues_json+="]"
    
    local warnings_json="["
    first=true
    for warn in "${WARNINGS_LIST[@]}"; do
        $first || warnings_json+=","
        warnings_json+="$warn"
        first=false
    done
    warnings_json+="]"
    
    cat <<EOF
{
  "check_date": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "project_root": "$PROJECT_ROOT",
  "auto_check_score": $auto_score,
  "stats": {
    "total_checks": $TOTAL_CHECKS,
    "passed": $PASSED_CHECKS,
    "failed": $FAILED_CHECKS,
    "warnings": $WARNINGS
  },
  "issues": $issues_json,
  "warnings": $warnings_json
}
EOF
}

# --- 入口 ---

main_check
