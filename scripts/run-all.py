#!/usr/bin/env python3
"""
全量验证流水线：执行 frontmatter 校验 → 关键词回归测试 → agent prompt 存在性检查。

Usage:
    python3 scripts/run-all.py                     # 全量（无参数，三阶段依次执行）
    python3 scripts/run-all.py --run-type check    # 仅 frontmatter 校验
    python3 scripts/run-all.py --run-type regression   # 仅关键词回归
    python3 scripts/run-all.py --run-type prompt       # 仅 agent prompt 检查
    python3 scripts/run-all.py --run-type regression --json  # 回归 JSON 报告
"""

import subprocess
import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def run_script(name, args=None):
    """Run a Python script in scripts/ and return exit code."""
    path = os.path.join(ROOT_DIR, "scripts", name)
    cmd = [sys.executable, path]
    if args:
        cmd.extend(args)
    result = subprocess.run(cmd, cwd=ROOT_DIR)
    return result.returncode


def main():
    argv = sys.argv[1:]
    exit_code = 0

    # Determine run type
    run_type = ""
    json_mode = "--json" in argv
    for a in argv:
        if a.startswith("--run-type="):
            run_type = a.split("=", 1)[1]
        elif a == "--run-type" and len(argv) > argv.index(a) + 1:
            run_type = argv[argv.index(a) + 1]

    run_check = not run_type or run_type == "check"
    run_regression = not run_type or run_type == "regression"
    run_prompt = not run_type or run_type == "prompt"

    reg_args = ["--json"] if json_mode else []

    print("=" * 60)
    print("Harness 全量验证流水线")
    if run_type:
        print(f"运行模式: {run_type}")
    print("=" * 60)
    print()

    if run_check:
        print(">>> Frontmatter 字段校验")
        if run_script("validate_skill_triggers.py") != 0:
            exit_code = 1
        print()

    if run_regression:
        print(">>> 关键词回归测试 (48 cases)")
        if run_script("run_trigger_regression.py", reg_args) != 0:
            exit_code = 1
        print()

    if run_prompt:
        print(">>> Agent Prompt 存在性检查")
        if run_script("validate_agent_prompt_sync.py") != 0:
            exit_code = 1
        print()

    if exit_code == 0:
        print("✅ 全量验证通过")
    else:
        print("❌ 验证存在失败")
        sys.exit(exit_code)


if __name__ == "__main__":
    main()
