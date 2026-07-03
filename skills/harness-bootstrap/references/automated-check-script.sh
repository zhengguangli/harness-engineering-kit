#!/bin/bash
# Automated check script for harness-bootstrap
# Includes shared checks + skill-specific checks

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../../.." && pwd)"
SKILL_NAME="$(basename "$SKILL_DIR")"

# Run shared checks first
shared_result=$(bash "$ROOT_DIR/scripts/skill-automated-check.sh" "$ROOT_DIR/skills" "$SKILL_NAME")
echo "$shared_result"

# Skill-specific checks
TOTAL_EXTRA=0
PASSED_EXTRA=0

# Check mandatory reference files
for ref_file in "claude-md-template.md" "claude-md-examples.md" "docs-skeleton-template.md" "docs-skeleton-by-stack.md" "gitignore-templates.md" "init-workflows.md"; do
  ((++TOTAL_EXTRA))
  if [ -f "$SKILL_DIR/references/$ref_file" ]; then
    ((++PASSED_EXTRA))
  else
    echo "  [FAIL] Missing reference: $ref_file"
  fi
done

# Check SKILL.md contains "Minimum Viable" in Core Principles section
((++TOTAL_EXTRA))
if grep -qE "^## Core Principles" "$SKILL_DIR/SKILL.md"; then
  if sed -n '/^## Core Principles/,/^## /p' "$SKILL_DIR/SKILL.md" | grep -q "Minimum Viable"; then
    ((++PASSED_EXTRA))
  else
    echo "  [FAIL] Core Principles section missing 'Minimum Viable'"
  fi
else
  echo "  [FAIL] Missing Core Principles section"
fi

# Check Project Type Tailoring Guide section exists (new content)
((++TOTAL_EXTRA))
if grep -qE "Project Type Tailoring Guide" "$SKILL_DIR/SKILL.md"; then
  ((++PASSED_EXTRA))
else
  echo "  [FAIL] Missing Project Type Tailoring Guide section"
fi

# Check Three-Layer Structure section
((++TOTAL_EXTRA))
if grep -qE "Three-Layer Structure" "$SKILL_DIR/SKILL.md"; then
  ((++PASSED_EXTRA))
else
  echo "  [FAIL] Missing Three-Layer Structure section in methodology"
fi

# Check Post-Initialization Checklist
((++TOTAL_EXTRA))
if grep -qE "Post-Initialization Checklist" "$SKILL_DIR/SKILL.md"; then
  ((++PASSED_EXTRA))
else
  echo "  [FAIL] Missing Post-Initialization Checklist section"
fi

echo "---"
echo "Extra checks: $PASSED_EXTRA/$TOTAL_EXTRA passed"
