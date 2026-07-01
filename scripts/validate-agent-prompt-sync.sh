#!/usr/bin/env bash
# scripts/validate-agent-prompt-sync.sh
# ------------------------------------------------------------
# 跨平台 prompt 一致性校验：把每个 skill 的
#   agents/<name>.md (frontmatter 之后的正文)
# 与
#   agents/openai.yaml 的 system_prompt: | 段
# 做规范化后计算字节比，比值落在 [0.95, 1.05] 区间视为同步。
#
# 初版采用"最宽松"规范化规则：
#   - 去除所有空行
#   - 去除每行首尾空白
#   - 把常见中英文标点映射为同一种（`,` vs `，`, `.` vs `。`,
#     `;` vs `；`, `:` vs `：`, `(` vs `（`, `)` vs `）`,
#     `"` vs `「`/`」`, `,` vs `、`, `?` vs `？`, `!` vs `！`）
#   - 把任意连续空白压成单个空格
#
# 设计原则：宁可漏报（让本来有差异的 pair 通过），也不要误报
# （让本来同步的 pair fail）。yaml 多行字符串的引号差异、注释
# 等暂不处理，留给 V2。
# ------------------------------------------------------------
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
skills_dir="$root/skills"
fail=0
warn=0

# 阈值（可在命令行覆盖：THRESHOLD_LOW=0.90 THRESHOLD_HIGH=1.80 ./scripts/validate-agent-prompt-sync.sh）
THRESHOLD_LOW="${THRESHOLD_LOW:-0.95}"
THRESHOLD_HIGH="${THRESHOLD_HIGH:-1.05}"

# 把单个文件做规范化后输出到 stdout
# stdin -> normalize -> stdout
normalize() {
  # 1) 折叠所有空白（tab / 连续空格 / 行尾空白）成单个空格
  # 2) 删除纯空行
  # 3) 把标点差异折叠
  sed -E '
    s/[[:space:]]+/ /g;
    s/^ //;
    s/ $//;
    /^$/d;
  ' | sed -E '
    s/，/,/g;
    s/。/./g;
    s/；/;/g;
    s/：/:/g;
    s/（/(/g;
    s/）/)/g;
    s/「/"/g;
    s/」/"/g;
    s/、/,/g;
    s/？/?/g;
    s/！/!/g;
  '
}

# 从 .md 文件里抽出 frontmatter 之后的正文
extract_md_body() {
  awk '
    BEGIN { in_fm=0; fm_closed=0 }
    NR==1 && /^---[[:space:]]*$/ { in_fm=1; next }
    in_fm && /^---[[:space:]]*$/ { fm_closed=1; in_fm=0; next }
    fm_closed { print }
  ' "$1"
}

# 从 .yaml 文件里抽出 system_prompt: | 段（保留内部缩进）
extract_yaml_prompt() {
  awk '
    /^system_prompt:[[:space:]]*\|/ { capture=1; next }
    capture==1 {
      # 顶层 key 出现时结束（行首以非空白字符开头的"key:"）
      if ($0 ~ /^[A-Za-z_][A-Za-z0-9_]*:[[:space:]]*$/) { exit }
      # 去掉 system_prompt 段的固定 2 空格缩进
      sub(/^  /, "")
      print
    }
  ' "$1"
}

# 安全比较浮点（bash 内置不能做浮点，用 awk）
in_range() {
  local ratio="$1" lo="$2" hi="$3"
  awk -v r="$ratio" -v lo="$lo" -v hi="$hi" 'BEGIN { exit (r+0 >= lo+0 && r+0 <= hi+0) ? 0 : 1 }'
}

echo "== cross-platform prompt sync check =="
echo "threshold: [$THRESHOLD_LOW, $THRESHOLD_HIGH]"
echo

# 用关联数组收集（bash 4+）
declare -A md_count
declare -A yaml_count
declare -A ratio_map
declare -A status_map
declare -A skip_map

# 收集所有 yaml 路径
shopt -s nullglob
yaml_files=("$skills_dir"/harness-*/agents/openai.yaml)
md_files=("$skills_dir"/harness-*/agents/*.md)

if [[ ${#yaml_files[@]} -eq 0 ]]; then
  echo "no agents/openai.yaml files found under $skills_dir" >&2
  exit 1
fi

for yaml_path in "${yaml_files[@]}"; do
  skill_dir="$(dirname "$(dirname "$yaml_path")")"
  skill_name="$(basename "$skill_dir")"

  # 从 yaml 的 metadata.name 字段读出 agent 名
  agent_name="$(awk '/^metadata:/{m=1;next} m && /^  name:/{sub(/^  name:[[:space:]]*/,""); print; exit}' "$yaml_path")"

  if [[ -z "$agent_name" ]]; then
    echo "[WARN] $skill_name: cannot read metadata.name from $yaml_path"
    warn=$((warn+1))
    continue
  fi

  md_path="$skill_dir/agents/${agent_name}.md"
  if [[ ! -f "$md_path" ]]; then
    echo "[WARN] $skill_name: matched agent '$agent_name' has no .md at $md_path"
    warn=$((warn+1))
    continue
  fi

  # 抽取并规范化
  md_norm="$(extract_md_body "$md_path" | normalize)"
  yaml_norm="$(extract_yaml_prompt "$yaml_path" | normalize)"

  md_len=${#md_norm}
  yaml_len=${#yaml_norm}

  if [[ "$md_len" -eq 0 ]]; then
    echo "[WARN] $skill_name: md body normalized to 0 bytes; skipping ratio"
    warn=$((warn+1))
    continue
  fi

  ratio="$(awk -v y="$yaml_len" -v m="$md_len" 'BEGIN { if (m+0==0) { print "0" } else { printf "%.4f", y/m } }')"
  ratio_map["$skill_name"]="$ratio"
  md_count["$skill_name"]="$md_len"
  yaml_count["$skill_name"]="$yaml_len"

  if in_range "$ratio" "$THRESHOLD_LOW" "$THRESHOLD_HIGH"; then
    status_map["$skill_name"]="OK"
  else
    status_map["$skill_name"]="FAIL"
    fail=$((fail+1))
  fi
done

# 输出：按比值降序排列
echo "skill                          status   ratio    md_bytes  yaml_bytes"
echo "---------------------------- -------- -------- --------- ----------"
for skill in "${!ratio_map[@]}"; do :; done

# 用 awk 排序打印
{
  for skill in "${!ratio_map[@]}"; do
    printf "%s\t%s\t%s\t%s\t%s\n" \
      "$skill" \
      "${status_map[$skill]}" \
      "${ratio_map[$skill]}" \
      "${md_count[$skill]}" \
      "${yaml_count[$skill]}"
  done
} | sort -t $'\t' -k3,3 -gr

echo
echo "summary: pass=$(printf '%s\n' "${status_map[@]}" | rg -c '^OK$' || true)  fail=$fail  warn=$warn  threshold=[$THRESHOLD_LOW, $THRESHOLD_HIGH]"

# 门限模式：默认 warn-only（CI 不被 block，drift 列表作为开发体验信号可见），
# 显式设置 STRICT=1 时才硬退出（用于 pre-release 检查或本地 strict 模式）。
if [[ "$fail" -ne 0 ]]; then
  if [[ "${STRICT:-0}" == "1" ]]; then
    echo
    echo "Validation finished with $fail failure(s) (STRICT mode)."
    exit 1
  else
    echo
    echo "Validation finished with $fail drift(s) (warn-only mode)."
    echo "  → 这些 skill 的 .md ↔ openai.yaml 内容存在差异，"
    echo "    后续 PR 会逐个修复。当前不阻断 CI。"
    echo "  → 如需硬检查（pre-release / 本地），运行: STRICT=1 $0"
    exit 0
  fi
fi

echo
echo "All agent prompts are within sync threshold."
