#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
script="$root/scripts/run-trigger-regression.sh"
skills_dir="$root/skills"
fail=0

while IFS= read -r line; do
  if [[ "$line" =~ ^SKILL_KW\[([^\]]+)\]=\"(.*)\"$ ]]; then
    skill="${BASH_REMATCH[1]}"
    words="${BASH_REMATCH[2]}"
    skill_file="$skills_dir/$skill/SKILL.md"
    if [[ ! -f "$skill_file" ]]; then
      echo "[FAIL] $skill: SKILL.md not found"
      fail=1
      continue
    fi
    missing=()
    for w in $words; do
      if ! rg -q "$w" "$skill_file"; then
        missing+=("$w")
      fi
    done
    if [[ ${#missing[@]} -gt 0 ]]; then
      fail=1
      echo "[FAIL] $skill missing in SKILL.md: ${missing[*]}"
    else
      echo "[OK] $skill"
    fi
  fi
done < "$script"

if [[ "$fail" -ne 0 ]]; then
  echo "\nKeyword consistency check failed."
  exit 1
fi

echo "\nAll regression keywords exist in corresponding SKILL.md files."
