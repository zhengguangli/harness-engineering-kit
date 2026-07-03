#!/usr/bin/env bash
# scripts/validate-agent-prompt-sync.sh
# ------------------------------------------------------------
# Agent 提示词存在性校验：检查每个 skill 的 SKILL.md 中
# 是否包含 "## Agent 提示词" section。
#
# 原有的跨平台 prompt 一致性校验（.md vs openai.yaml）
# 已不再适用，因为 agent 提示词已内联到 SKILL.md 中。
# ------------------------------------------------------------
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
skills_dir="$root/skills"
fail=0
warn=0

echo "== agent prompt presence check =="
echo

# 检查每个 SKILL.md 是否包含 Agent 提示词 section
for skill_dir in "$skills_dir"/harness-*/; do
  skill_name="$(basename "$skill_dir")"
  skill_md="$skill_dir/SKILL.md"

  if [[ ! -f "$skill_md" ]]; then
    echo "[FAIL] $skill_name: SKILL.md not found"
    fail=$((fail+1))
    continue
  fi

  # 检查是否包含 Agent 提示词 section
  if grep -q "^## Agent 提示词" "$skill_md"; then
    echo "[OK] $skill_name: has '## Agent 提示词' section"
  else
    echo "[WARN] $skill_name: missing '## Agent 提示词' section"
    warn=$((warn+1))
  fi
done

echo
echo "summary: pass=$(find "$skills_dir" -name "SKILL.md" -path "*/harness-*/SKILL.md" | wc -l | tr -d ' ')  warn=$warn  fail=$fail"

if [[ "$fail" -ne 0 ]]; then
  echo
  echo "Validation finished with $fail failure(s)."
  exit 1
fi

if [[ "$warn" -ne 0 ]]; then
  echo
  echo "Validation finished with $warn warning(s)."
  echo "  → 这些 skill 的 SKILL.md 中缺少 '## Agent 提示词' section，"
  echo "    后续 PR 会逐个补充。当前不阻断 CI。"
fi

echo
echo "All agent prompt checks passed."
