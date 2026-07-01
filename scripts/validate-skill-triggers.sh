#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
skills_dir="$root/skills"
fail=0

for skill_md in "$skills_dir"/harness-*/SKILL.md; do
  skill_dir="$(dirname "$skill_md")"
  skill_name="$(basename "$skill_dir")"
  missing=()

  # Check frontmatter fields
  if ! awk '/^---$/{c++} c==1' "$skill_md" | grep -q "^description:"; then
    missing+=("missing_field:description")
  fi

  if ! awk '/^---$/{c++} c==1' "$skill_md" | grep -q "^when_to_use:"; then
    missing+=("missing_field:when_to_use")
  fi

  if ! awk '/^---$/{c++} c==1' "$skill_md" | grep -q "^compatibility:"; then
    missing+=("missing_field:compatibility")
  fi

  # Check description length (should be > 20 chars)
  desc_len=$(awk '/^---$/{c++} c==1 && /^description:/{sub(/^description:[[:space:]]*/,""); print length; exit}' "$skill_md")
  if [[ "${desc_len:-0}" -lt 20 ]]; then
    missing+=("description_too_short:${desc_len:-0}")
  fi

  # Verify no legacy 触发信号 section remains
  if rg -q "^## 触发信号$" "$skill_md"; then
    missing+=("legacy_section:## 触发信号 still present")
  fi

  # Verify no version field
  if awk '/^---$/{c++} c==1' "$skill_md" | grep -q "^version:"; then
    missing+=("legacy_field:version still present")
  fi

  if [[ ${#missing[@]} -gt 0 ]]; then
    fail=1
    echo "[WARN] $skill_name: ${missing[*]}"
  else
    echo "[OK] $skill_name"
  fi
done

echo ""
echo "--- Cross-reference check ---"
cross_ref_fail=0
cross_ref_total=0
for skill_md in "$skills_dir"/harness-*/SKILL.md; do
  skill_name="$(basename "$(dirname "$skill_md")")"
  # Only check references in "配合的 agent" section (actual skill cross-refs)
  refs=$(awk '/^## 配合的 agent$/{found=1;next} found && /^## /{exit} found' "$skill_md" | { grep -oE 'harness-[a-z]+-[a-z-]+' || true; } | sort -u)
  for r in $refs; do
    if [[ "$r" == "$skill_name" ]]; then continue; fi
    cross_ref_total=$((cross_ref_total + 1))
    if [[ ! -d "$skills_dir/$r" ]]; then
      echo "[WARN] $skill_name references non-existent skill: $r"
      cross_ref_fail=1
    fi
  done
done
if [[ "$cross_ref_fail" -ne 0 ]]; then
  fail=1
  echo "Cross-reference check failed."
else
  echo "[OK] $cross_ref_total cross-references validated"
fi

if [[ "$fail" -ne 0 ]]; then
  echo ""
  echo "Validation finished with failures."
  exit 1
fi

echo ""
echo "All skill frontmatter validated."
