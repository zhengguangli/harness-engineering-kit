#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
skills_dir="$root/skills"
fail=0

for skill_md in "$skills_dir"/harness-*/SKILL.md; do
  skill_dir="$(dirname "$skill_md")"
  skill_name="$(basename "$skill_dir")"
  missing=()

  if ! rg -q "^## 触发信号$" "$skill_md"; then
    missing+=("missing_section:## 触发信号")
  fi

  for block in "显式触发（explicit）" "语义意图（intent）" "证据触发（artifacts）" "避免触发（avoid_when）"; do
    if ! rg -q "^### $block$" "$skill_md"; then
      missing+=("missing_block:$block")
    fi
  done

  explicit_count=$(awk "/^### 显式触发（explicit）\$/{f=1;next} /^### /{f=0} f && /^- /{c++} END{print c+0}" "$skill_md")
  intent_count=$(awk "/^### 语义意图（intent）\$/{f=1;next} /^### /{f=0} f && /^- /{c++} END{print c+0}" "$skill_md")
  avoid_count=$(awk "/^### 避免触发（avoid_when）\$/{f=1;next} /^###{1,2} /{f=0} f && /^- /{c++} END{print c+0}" "$skill_md")

  [[ "$explicit_count" -lt 3 ]] && missing+=("explicit_count=$explicit_count<3")
  [[ "$intent_count" -lt 3 ]] && missing+=("intent_count=$intent_count<3")
  [[ "$avoid_count" -lt 2 ]] && missing+=("avoid_count=$avoid_count<2")

  if [[ ${#missing[@]} -gt 0 ]]; then
    fail=1
    echo "[WARN] $skill_name: ${missing[*]}"
  else
    echo "[OK] $skill_name"
  fi
done

if [[ "$fail" -ne 0 ]]; then
  echo "\nValidation finished with warnings."
  exit 1
fi

echo "\n--- Cross-reference check ---"
cross_ref_fail=0
cross_ref_total=0
for skill_md in "$skills_dir"/harness-*/SKILL.md; do
  skill_name="$(basename "$(dirname "$skill_md")")"
  refs=$(awk '/^### 避免触发（avoid_when）$/{f=1;next} /^### /{f=0} f' "$skill_md" | { grep -oE 'harness-[a-z-]+' || true; } | sort -u)
  for r in $refs; do
    cross_ref_total=$((cross_ref_total + 1))
    if [[ ! -d "$skills_dir/$r" ]]; then
      echo "[FAIL] $skill_name references non-existent skill: $r"
      cross_ref_fail=1
    fi
  done
done
if [[ "$cross_ref_fail" -ne 0 ]]; then
  fail=1
  echo "Cross-reference check failed."
else
  echo "[OK] 12 skills cross-referenced ($cross_ref_total refs valid)"
fi

if [[ "$fail" -ne 0 ]]; then
  echo "\nValidation finished with failures."
  exit 1
fi

echo "\nAll skill trigger sections validated."
