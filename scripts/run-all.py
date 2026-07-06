#!/usr/bin/env python3
"""
全量验证流水线：执行 frontmatter 校验 → 关键词回归测试 → agent prompt 存在性检查。

Usage:
    python3 scripts/run-all.py                                # 全量（三阶段依次执行）
    python3 scripts/run-all.py --run-type check               # 仅 frontmatter 校验
    python3 scripts/run-all.py --run-type regression          # 仅关键词回归
    python3 scripts/run-all.py --run-type regression --json   # 回归 JSON 报告
    python3 scripts/run-all.py --run-type prompt              # 仅 agent prompt 检查
    python3 scripts/run-all.py --sync                         # 全量 + 同步到 ~/.claude/skills/
"""

import subprocess
import sys
import os
import argparse

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_DIR = os.path.join(ROOT_DIR, "skills")
HOME_SKILLS = os.path.expanduser("~/.claude/skills")
HOME_SCRIPTS = os.path.join(HOME_SKILLS, "scripts")


def run_script(name, args=None):
    """Run a Python script in scripts/ and return exit code."""
    path = os.path.join(ROOT_DIR, "scripts", name)
    cmd = [sys.executable, path]
    if args:
        cmd.extend(args)
    result = subprocess.run(cmd, cwd=ROOT_DIR, capture_output=not _verbose)
    return result.returncode


# Detect if we're in a pipe (keep verbose when running directly)
_verbose = sys.stdout.isatty()


def sync():
    """Sync skills/ and scripts/ to ~/.claude/skills/."""
    if not os.path.isdir(HOME_SKILLS):
        os.makedirs(HOME_SKILLS, exist_ok=True)
    print(">>> 同步前: 部署 skills 到 ~/.claude/skills/")
    subprocess.run(["rsync", "-av", "--delete", SKILLS_DIR + "/", HOME_SKILLS + "/"],
                   cwd=ROOT_DIR, capture_output=not _verbose)
    print(">>> 同步前: 部署 scripts 到 ~/.claude/skills/scripts/")
    os.makedirs(HOME_SCRIPTS, exist_ok=True)
    subprocess.run(["rsync", "-av", os.path.join(ROOT_DIR, "scripts") + "/", HOME_SCRIPTS + "/"],
                   cwd=ROOT_DIR, capture_output=not _verbose)
    print("✅ 同步完成")


def main():
    parser = argparse.ArgumentParser(description="Harness 全量验证流水线")
    parser.add_argument("--run-type", choices=["check", "regression", "prompt"],
                        help="指定运行阶段: check/regression/prompt")
    parser.add_argument("--json", action="store_true",
                        help="回归测试输出 JSON 报告")
    parser.add_argument("--sync", action="store_true",
                        help="验证完成后同步到 ~/.claude/skills/")
    args = parser.parse_args()

    exit_code = 0

    run_check = not args.run_type or args.run_type == "check"
    run_regression = not args.run_type or args.run_type == "regression"
    run_prompt = not args.run_type or args.run_type == "prompt"
    reg_args = ["--json"] if args.json else []

    print("=" * 60)
    print("Harness 全量验证流水线")
    if args.run_type:
        print(f"运行模式: {args.run_type}")
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

    if args.sync:
        sync()


if __name__ == "__main__":
    main()
