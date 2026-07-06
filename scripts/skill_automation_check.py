#!/usr/bin/env python3
"""
[已废弃] 通用 SKILL.md 自动化检查脚本（中文版）。

⚠️ 此脚本检查中文章节名（核心原则、何时使用等），但 SKILL.md 已全
   部翻译为英文，运行结果全部显示缺失，不具备实际检查价值。
   保留仅用于参考完整的逻辑结构，不再推荐调用。

替代 scripts/skill-automation-check.sh
"""

import os
import re
import sys
from datetime import datetime

ROOT_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
SKILLS_DIR = os.path.join(ROOT_DIR, "skills")


def read_lines(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.readlines()
    except (OSError, UnicodeDecodeError):
        return []


def has_field(lines, field):
    """Check if frontmatter contains a field."""
    in_fm = False
    for line in lines:
        stripped = line.strip()
        if stripped == "---":
            if not in_fm:
                in_fm = True
                continue
            else:
                break
        if in_fm and re.match(rf"^{re.escape(field)}:", stripped):
            return True
    return False


def has_section(lines, section_name):
    for line in lines:
        m = re.match(r"^##\s+(.+)$", line.strip())
        if m and section_name in m.group(1):
            return True
    return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/skill_automation_check.py <skill-name>")
        sys.exit(1)

    skill_name = sys.argv[1]
    report_file = os.path.join(ROOT_DIR, "docs/quality-reports", f"{skill_name}-check.md")
    skill_file = os.path.join(SKILLS_DIR, skill_name, "SKILL.md")

    os.makedirs(os.path.join(ROOT_DIR, "docs/quality-reports"), exist_ok=True)

    lines = []
    report_lines = []

    def report(text):
        report_lines.append(text)

    report(f"# {skill_name} 自动化检查报告")
    report("")
    report(f"检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report("")

    if not os.path.isfile(skill_file):
        report("## 错误")
        report(f"SKILL.md 文件不存在: {skill_file}")
        print("检查完成，报告已保存到 " + report_file)
        with open(report_file, "w", encoding="utf-8") as f:
            f.write("\n".join(report_lines) + "\n")
        sys.exit(1)

    lines = read_lines(skill_file)

    report("## 检查结果")
    report("")

    # Frontmatter
    report("### Frontmatter检查")
    for field in ("name", "description", "when_to_use", "compatibility"):
        if has_field(lines, field):
            report(f"- [x] {field} 字段存在")
        else:
            report(f"- [ ] {field} 字段缺失")

    # Standard sections
    report("### 章节结构检查")
    for section in ("核心原则", "何时使用", "方法论", "硬约束", "关键要点"):
        if has_section(lines, section):
            report(f"- [x] {section} 章节存在")
        else:
            report(f"- [ ] {section} 章节缺失")

    # Agent prompt section
    if has_section(lines, "Agent 提示词"):
        report("- [x] Agent 提示词章节存在")
    else:
        report("- [ ] Agent 提示词章节缺失")

    # Optional sections
    report("### 可选章节检查")
    for section in ("常见陷阱", "边界情况处理", "最佳实践", "跨skill交接点", "自动化检查", "相关模板"):
        if has_section(lines, section):
            report(f"- [x] {section} 章节存在")

    # Example counts
    example_count = sum(1 for line in lines if re.match(r"^#{2,4}\s+示例", line.strip()))
    report("### 示例统计")
    report(f"- 示例数量: {example_count}")

    report("")
    report("## 检查完成")

    with open(report_file, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")

    print(f"检查完成，报告已保存到 {report_file}")


if __name__ == "__main__":
    main()
