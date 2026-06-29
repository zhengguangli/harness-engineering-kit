#!/usr/bin/env bash
# scripts/check-skills-quality.sh
# 统一执行 9 项 skill 质量检查,任何失败返回 FAIL=1
# 用法: bash scripts/check-skills-quality.sh
set -euo pipefail

FAIL=0

# ──────────────────────────────────────────────
# 1. check-skill-structure — 三件套完整性
# ──────────────────────────────────────────────
echo "=== [1/9] check-skill-structure ==="
for d in skills/harness-*/; do
  [ ! -d "$d" ] && continue
  missing=""
  [ ! -f "${d}SKILL.md" ] && missing="$missing SKILL.md"
  [ ! -d "${d}agents" ] && missing="$missing agents/"
  [ ! -d "${d}references" ] && missing="$missing references/"
  if [ -n "$missing" ]; then
    echo "FAIL: ${d} missing:${missing}"
    echo "FIX:  Create missing files/dirs under ${d}. Reference skills/harness-repo-map/ structure."
    FAIL=1
  fi
done

# ──────────────────────────────────────────────
# 2. check-frontmatter — Agent 定义文件 6 字段完整性
# ──────────────────────────────────────────────
echo "=== [2/9] check-frontmatter ==="
required_fields="name description type tools model skills"
for f in skills/*/agents/*.md; do
  [ ! -f "$f" ] && continue
  frontmatter=$(sed -n '/^---$/,/^---$/p' "$f")
  missing=""
  for field in $required_fields; do
    echo "$frontmatter" | grep -q "^${field}:" || missing="$missing $field"
  done
  if [ -n "$missing" ]; then
    echo "FAIL: ${f} frontmatter missing:${missing}"
    echo "FIX:  Add missing fields to ${f} YAML frontmatter."
    FAIL=1
  fi
done

# ──────────────────────────────────────────────
# 3. check-naming — 目录命名规范 (harness- + kebab-case)
# ──────────────────────────────────────────────
echo "=== [3/9] check-naming ==="
for d in skills/*/; do
  [ ! -d "$d" ] && continue
  name=$(basename "$d")
  [ "$name" = "references" ] && continue
  if ! echo "$name" | grep -qE '^harness-[a-z0-9]+(-[a-z0-9]+)*$'; then
    echo "FAIL: skills/${name}/ naming violation"
    echo "FIX:  Directory name must start with harness- and use kebab-case (lowercase + digits + hyphens)."
    FAIL=1
  fi
done

# ──────────────────────────────────────────────
# 4. check-dates — docs/ 文件"最后更新"标记
# ──────────────────────────────────────────────
echo "=== [4/9] check-dates ==="
while IFS= read -r f; do
  if ! grep -q "最后更新" "$f"; then
    echo "FAIL: ${f} missing '最后更新' date"
    echo "FIX:  Append: ---\n最后更新: $(date +%Y-%m-%d)"
    FAIL=1
  fi
done < <(find docs/ -name '*.md' -type f 2>/dev/null)

# ──────────────────────────────────────────────
# 5. check-three-blocks — openai.yaml 三区块完整性
# ──────────────────────────────────────────────
echo "=== [5/9] check-three-blocks ==="
for f in skills/*/agents/openai.yaml; do
  [ ! -f "$f" ] && continue
  blocks=$(grep -cE '^(metadata|tools|system_prompt):' "$f" || true)
  if [ "$blocks" -lt 3 ]; then
    echo "FAIL: ${f} has only ${blocks}/3 required blocks (metadata/tools/system_prompt)"
    echo "FIX:  Reference skills/harness-repo-map/agents/openai.yaml format."
    FAIL=1
  fi
  # system_prompt 行数检查 (排除末尾空行)
  if grep -q '^system_prompt:' "$f"; then
    lines=$(sed -n '/^system_prompt:/,$ p' "$f" | sed '/^[[:space:]]*$/d' | wc -l)
    lines=$((lines + 0))  # trim whitespace from wc
    if [ "$lines" -lt 10 ]; then
      echo "FAIL: ${f} system_prompt too short (${lines} lines, min 10)"
      echo "FIX:  Expand system_prompt content in ${f}."
      FAIL=1
    fi
  fi
done

# ──────────────────────────────────────────────
# 6. check-cross-platform-sync — .md ↔ openai.yaml 对应关系
# ──────────────────────────────────────────────
echo "=== [6/9] check-cross-platform-sync ==="
for skill_dir in skills/harness-*/; do
  [ ! -d "$skill_dir" ] && continue
  skill=$(basename "$skill_dir")
  md_count=0
  for f in "${skill_dir}agents/"*.md; do
    [ -f "$f" ] && md_count=$((md_count + 1))
  done
  yaml="${skill_dir}agents/openai.yaml"
  if [ "$md_count" -gt 0 ] && [ ! -f "$yaml" ]; then
    echo "FAIL: ${skill} has ${md_count} agent .md but no openai.yaml"
    echo "FIX:  Create ${yaml} with metadata/tools/system_prompt blocks."
    FAIL=1
  fi
done

# ──────────────────────────────────────────────
# 7. check-template-drift — 同名模板跨 skill 一致性
# ──────────────────────────────────────────────
echo "=== [7/9] check-template-drift ==="
declare -A template_files
for f in skills/*/references/*.md; do
  [ ! -f "$f" ] && continue
  fname=$(basename "$f")
  # Skip prompt files (they are per-agent, not shared templates)
  [[ "$fname" == *-prompt.md ]] && continue
  if [[ -n "${template_files[$fname]+x}" ]]; then
    template_files[$fname]="${template_files[$fname]}|$f"
  else
    template_files[$fname]="$f"
  fi
done
for fname in "${!template_files[@]}"; do
  files="${template_files[$fname]}"
  IFS='|' read -ra file_list <<< "$files"
  if [ "${#file_list[@]}" -gt 1 ]; then
    # Compare all files against the first one (skip line 3 which has ownership comment)
    base="${file_list[0]}"
    for other in "${file_list[@]:1}"; do
      if ! diff <(sed '3d' "$base") <(sed '3d' "$other") > /dev/null 2>&1; then
        echo "FAIL: Template drift detected: $fname"
        echo "  Files: $base vs $other"
        echo "FIX:  Sync the canonical owner's version to the derived copy."
        FAIL=1
      fi
    done
  fi
done

# ──────────────────────────────────────────────
# 8. check-skill-size — GP-05 SKILL.md ≤ 200 行
# ──────────────────────────────────────────────
echo "=== [8/9] check-skill-size ==="
for f in skills/*/SKILL.md; do
  [ ! -f "$f" ] && continue
  lines=$(wc -l < "$f")
  if [ "$lines" -gt 200 ]; then
    echo "FAIL: ${f} is ${lines} lines (max 200 per GP-05)"
    echo "FIX:  Move verbose sections to references/ files, keep SKILL.md focused on core methodology."
    FAIL=1
  fi
done

# ──────────────────────────────────────────────
# 9. check-prompt-sync — agent .md 与 prompt 文件一致性
# ──────────────────────────────────────────────
echo "=== [9/9] check-prompt-sync ==="
if ! python3 scripts/check-prompt-sync.py; then
  FAIL=1
fi

# ──────────────────────────────────────────────
# Summary
# ──────────────────────────────────────────────
echo ""
if [ "$FAIL" -eq 0 ]; then
  echo "ALL CHECKS PASSED"
else
  echo "CHECKS FAILED (see above)"
  exit 1
fi
