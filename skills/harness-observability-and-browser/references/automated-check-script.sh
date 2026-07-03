#!/bin/bash
# 自动化检查脚本 - 引用共享脚本
# 用法: bash automated-check-script.sh
# 输出: JSON 格式检查结果

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/../../.." && pwd)"
SKILL_NAME="$(basename "$(dirname "$SCRIPT_DIR")")"
SHARED_SCRIPT="$SKILL_DIR/scripts/skill-automated-check.sh"

if [ ! -f "$SHARED_SCRIPT" ]; then
    echo "{\"error\":\"Shared script not found at $SHARED_SCRIPT\"}"
    exit 1
fi

bash "$SHARED_SCRIPT" "$SKILL_DIR/skills" "$SKILL_NAME"
