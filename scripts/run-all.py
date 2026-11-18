#!/usr/bin/env python3
"""
全量验证流水线：frontmatter 校验 → 关键词回归测试 → agent prompt 存在性检查 → 依赖方向校验 → 单元测试 → 输出规格与任务集覆盖审计。

Usage:
    python3 scripts/run-all.py                                # 全量（六阶段依次执行）
    python3 scripts/run-all.py --run-type check               # 仅 frontmatter 校验
    python3 scripts/run-all.py --run-type regression          # 仅关键词回归
    python3 scripts/run-all.py --run-type regression --json   # 回归 JSON 报告
    python3 scripts/run-all.py --run-type prompt              # 仅 agent prompt 检查
    python3 scripts/run-all.py --run-type deps                # 仅依赖方向/循环依赖校验
    python3 scripts/run-all.py --run-type tests               # 仅单元测试（tests/ 下全部）
    python3 scripts/run-all.py --run-type audit               # 仅输出规格可执行性审计
    python3 scripts/run-all.py --sync                         # 全量 + 同步到 ~/.agents/skills/ (并维护 ~/.claude/skills 软链接)
"""

import argparse
import json
import os
import shutil
import subprocess
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_DIR = os.path.join(ROOT_DIR, "skills")
HOME_SKILLS = os.path.expanduser("~/.agents/skills")
CLAUDE_SKILLS = os.path.expanduser("~/.claude/skills")


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


def _remove_entry(path):
    """Remove a file, symlink, or directory cleanly."""
    if os.path.islink(path) or os.path.isfile(path):
        os.unlink(path)
    elif os.path.isdir(path):
        shutil.rmtree(path)


def sync(skills_dir=SKILLS_DIR, home_skills=HOME_SKILLS, claude_skills=CLAUDE_SKILLS):
    """Safely sync harness-* skills to ~/.agents/skills/ without deleting unrelated skills."""
    print(f">>> 部署 harness-* skills 到 {home_skills}/")
    os.makedirs(home_skills, exist_ok=True)

    active = sorted(
        name for name in os.listdir(skills_dir)
        if name.startswith("harness-") and os.path.isdir(os.path.join(skills_dir, name))
    )
    active_set = set(active)

    # Prune only stale harness-* entries; preserve third-party skills (e.g. context7-mcp)
    for entry in sorted(os.listdir(home_skills)):
        if entry.startswith("harness-") and entry not in active_set:
            _remove_entry(os.path.join(home_skills, entry))
            print(f"  [PRUNE] {os.path.join(home_skills, entry)}")

    for name in active:
        src = os.path.join(skills_dir, name)
        dst = os.path.join(home_skills, name)
        if os.path.lexists(dst):
            _remove_entry(dst)
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        print(f"  [SYNC] {name}")

    # Maintain ~/.claude/skills: directory-level symlink if empty/absent, else per-skill symlinks
    if os.path.islink(claude_skills):
        if os.readlink(claude_skills) == home_skills:
            print("  ~/.claude/skills -> ~/.agents/skills 软链接已存在，跳过")
        else:
            os.unlink(claude_skills)
            os.symlink(home_skills, claude_skills)
            print("  ~/.claude/skills 软链接已更新")
    elif os.path.isdir(claude_skills):
        # Preserve existing non-harness skills inside ~/.claude/skills/
        for entry in sorted(os.listdir(claude_skills)):
            if entry.startswith("harness-") and entry not in active_set:
                _remove_entry(os.path.join(claude_skills, entry))
        for name in active:
            link_path = os.path.join(claude_skills, name)
            target = os.path.join(home_skills, name)
            if os.path.lexists(link_path):
                if os.path.islink(link_path) and os.readlink(link_path) == target:
                    continue
                _remove_entry(link_path)
            os.symlink(target, link_path)
        print("  ~/.claude/skills 中 harness-* 软链接已更新（保留非 harness 技能）")
    else:
        os.makedirs(os.path.dirname(claude_skills), exist_ok=True)
        os.symlink(home_skills, claude_skills)
        print("  ~/.claude/skills 软链接已创建")

    print("✅ 同步完成")


def main():
    parser = argparse.ArgumentParser(description="Harness 全量验证流水线")
    parser.add_argument("--run-type", choices=["check", "regression", "prompt", "deps", "tests", "audit"],
                        help="指定运行阶段: check/regression/prompt/deps/tests/audit")
    parser.add_argument("--json", action="store_true",
                        help="回归测试输出 JSON 报告")
    parser.add_argument("--sync", action="store_true",
                        help="验证完成后同步到 ~/.agents/skills/ (并维护 ~/.claude/skills 软链接)")
    args = parser.parse_args()

    exit_code = 0

    run_check = not args.run_type or args.run_type == "check"
    run_regression = not args.run_type or args.run_type == "regression"
    run_prompt = not args.run_type or args.run_type == "prompt"
    run_deps = not args.run_type or args.run_type == "deps"
    run_tests = not args.run_type or args.run_type == "tests"
    run_audit = not args.run_type or args.run_type == "audit"
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
        n_cases = 0
        try:
            with open(os.path.join(ROOT_DIR, "tests", "triggers", "cases.json"),
                      encoding="utf-8") as f:
                n_cases = len(json.load(f))
        except (OSError, ValueError):
            pass
        print(f">>> 关键词回归测试 ({n_cases} cases)")
        if run_script("run_trigger_regression.py", reg_args) != 0:
            exit_code = 1
        print()

    if run_prompt:
        print(">>> Agent Prompt 存在性检查")
        if run_script("validate_agent_prompt_sync.py") != 0:
            exit_code = 1
        print()

    if run_deps:
        print(">>> Skill 依赖方向与循环依赖校验")
        if run_script("validate_skill_dependencies.py") != 0:
            exit_code = 1
        print()

    if run_tests:
        print(">>> 单元测试 (tests/)")
        import glob as _glob
        test_files = sorted(_glob.glob(os.path.join(ROOT_DIR, "tests", "**", "test_*.py"),
                                       recursive=True))
        if not test_files:
            print("  (no test files found)")
        for tf in test_files:
            rel = os.path.relpath(tf, ROOT_DIR)
            r = subprocess.run([sys.executable, tf], cwd=ROOT_DIR,
                               capture_output=not _verbose)
            if r.returncode != 0:
                print(f"  [FAIL] {rel}")
                exit_code = 1
            else:
                print(f"  [OK] {rel}")
        print()

    if run_audit:
        print(">>> 输出规格可执行性审计")
        if run_script("audit_output_specs.py") != 0:
            exit_code = 1
        print()
        print(">>> 任务集覆盖审计")
        if run_script("audit_task_coverage.py") != 0:
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
