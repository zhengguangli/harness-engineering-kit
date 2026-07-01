#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
cases_file="$root/tests/triggers/cases.json"
skills_dir="$root/skills"
report_file="$root/tests/triggers/report.json"
json_mode=0

if [[ "${1:-}" == "--json" ]]; then
  json_mode=1
  mkdir -p "$(dirname "$report_file")"
fi

if [[ ! -f "$cases_file" ]]; then
  echo "cases file not found: $cases_file"
  exit 2
fi

declare -A SKILL_KW
SKILL_KW[harness-architecture-boundaries]="分层架构 循环依赖 层间越界 lint 规则 依赖方向 架构腐化"
SKILL_KW[harness-authoring]="怎么写一个好的 SKILL.md 给 harness 添新能力 skill 还是 subagent 瘦身"
SKILL_KW[harness-bootstrap]="init harness 为这个项目初始化 harness AGENTS.md docs/ 骨架 CI 模板"
SKILL_KW[harness-commit-gate]="提交代码 commit git commit 修复，提交代码 代码提交"
SKILL_KW[harness-exec-plans]="先做个计划 改动比较大 落盘 跨多个会话 跨多窗口 接力 上一轮试过什么"
SKILL_KW[harness-golden-principles]="周期性扫描 模式漂移 黄金原则 品味编码 重复模式"
SKILL_KW[harness-observability-and-browser]="复现 UI bug P99 截图 浏览器 验证"
SKILL_KW[harness-orchestration]="我该用哪些 skill 多 skill 协作 不确定先后顺序 不确定先做什么后做什么 路由"
SKILL_KW[harness-project-intake]="分析当前项目 项目概览 README 这个项目是做什么的 项目卡片"
SKILL_KW[harness-prompt-optimizer]="优化这个 prompt prompt 效果不好 system prompt"
SKILL_KW[harness-repo-map]="AGENTS.md 瘦身 断链 过期 从零搭建 docs 渐进式披露"
SKILL_KW[harness-verification-loop]="可合并 自验证循环 测试失败 循环迭代 实现→自检→测试→评审→修复 迭代"

match_count() {
  local skill="$1" text="$2" count=0
  local words="${SKILL_KW[$skill]:-}"
  [[ -z "$words" ]] && { echo 0; return; }
  for w in $words; do
    if echo "$text" | grep -F -q "$w"; then
      count=$((count+1))
    fi
  done
  echo "$count"
}

pass=0; warn=0; fail=0
json_items=()
while IFS= read -r row; do
  [[ -z "$row" ]] && continue
  id=$(echo "$row" | jq -r '.id')
  input=$(echo "$row" | jq -r '.input')
  primary=$(echo "$row" | jq -r '.expected_primary_skill')
  candidates=$(echo "$row" | jq -r '.expected_candidates[]')

  primary_count=$(match_count "$primary" "$input")
  best_skill="$primary"
  best_count=$primary_count
  matched_candidates=()

  for c in $candidates; do
    c_count=$(match_count "$c" "$input")
    if [[ $c_count -gt 0 ]]; then
      matched_candidates+=("$c")
      if [[ $c_count -gt $best_count ]]; then
        best_count=$c_count
        best_skill="$c"
      fi
    fi
  done

  result="FAIL"; reason=""
  if [[ $primary_count -gt 0 ]]; then
    if [[ "$best_skill" == "$primary" ]]; then
      result="PASS"; reason="primary matched with strongest signal"
    else
      result="WARN"; reason="primary matched but not strongest signal"
    fi
  else
    result="FAIL"; reason="primary not matched"
  fi

  [[ "$result" == "PASS" ]] && ((pass++)) || true
  [[ "$result" == "WARN" ]] && ((warn++)) || true
  [[ "$result" == "FAIL" ]] && ((fail++)) || true
  printf "[%s] %s -> %s (%s)\n" "$result" "$id" "$primary" "$reason"

  if [[ "$json_mode" -eq 1 ]]; then
    json_items+=("{\"id\":\"$id\",\"input\":\"$input\",\"primary\":\"$primary\",\"result\":\"$result\",\"reason\":\"$reason\",\"matched_candidates\":\"${matched_candidates[*]:-}\"}")
  fi
done < <(jq -c '.[]' "$cases_file")

printf "\nSummary: PASS=%s WARN=%s FAIL=%s\n" "$pass" "$warn" "$fail"

if [[ "$json_mode" -eq 1 ]]; then
  printf '[' > "$report_file"
  first=1
  for item in "${json_items[@]}"; do
    if [[ $first -eq 1 ]]; then first=0; else printf ',' >> "$report_file"; fi
    printf '%s' "$item" >> "$report_file"
  done
  printf ']' >> "$report_file"
  echo "Report written to $report_file"
fi

if [[ "$fail" -gt 0 ]]; then exit 1; fi
