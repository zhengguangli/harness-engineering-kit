#!/usr/bin/env python3
"""
scripts/validate_skill_dependencies.py 的回归测试。

用合成 fixture 验证校验器能真正抓住四类违规，再对真实 skills/ 跑一遍确保当前仓库合规。
不依赖 pytest，仅用标准库 unittest。

Usage:
    python3 tests/dependencies/test_dependency_validation.py
"""

import io
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout

SCRIPTS_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "scripts"))
sys.path.insert(0, SCRIPTS_DIR)

import validate_skill_dependencies as vdd  # noqa: E402

REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
REAL_SKILLS = os.path.join(REPO_ROOT, "skills")

# 复用真实层级表，只替换 skill 名，保证测试与生产规则一致
LAYERS = {
    0: ["harness-alpha"],
    1: ["harness-beta"],
    2: ["harness-gamma", "harness-delta"],
    3: ["harness-epsilon"],
}
META = ["harness-meta"]


def write_skill(root, name, depends_on, extra_body=""):
    d = os.path.join(root, name)
    os.makedirs(os.path.join(d, "references"), exist_ok=True)
    dep_lines = "depends_on: []\n" if not depends_on else \
        "depends_on:\n" + "".join(f"  - {x}\n" for x in depends_on)
    content = (
        "---\n"
        f"name: {name}\n"
        "description: Synthetic fixture skill used only by the dependency validator regression tests.\n"
        "when_to_use: fixture\n"
        "compatibility: claude-code\n"
        f"{dep_lines}"
        "---\n"
        "# Fixture\n\n"
        "## Related Skills\n\n"
        f"{extra_body}"
    )
    with open(os.path.join(d, "SKILL.md"), "w", encoding="utf-8") as f:
        f.write(content)


def run(skills_dir, root_dir, strict=False):
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = vdd.validate(skills_dir, root_dir, layers=LAYERS, meta=META,
                            strict=strict, out=buf)
    return code, buf.getvalue()


class DependencyValidatorTests(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = self.tmp.name
        self.skills = os.path.join(self.root, "skills")
        os.makedirs(self.skills)

    def tearDown(self):
        self.tmp.cleanup()

    def build(self, graph):
        """graph: {skill: [deps]}"""
        for name, deps in graph.items():
            write_skill(self.skills, name, deps)

    # --- 1. 合法 DAG ---
    def test_valid_downward_dag_passes(self):
        self.build({
            "harness-alpha": [],
            "harness-beta": ["harness-alpha"],
            "harness-gamma": ["harness-beta"],
            "harness-delta": ["harness-alpha"],
            "harness-epsilon": ["harness-gamma", "harness-delta"],
        })
        code, out = run(self.skills, self.root)
        self.assertEqual(code, 0, out)

    # --- 2. 环检测 ---
    def test_two_node_cycle_fails(self):
        self.build({
            "harness-beta": ["harness-gamma"],
            "harness-gamma": ["harness-beta"],
        })
        code, out = run(self.skills, self.root)
        self.assertEqual(code, 1)
        self.assertIn("循环依赖", out)

    def test_three_node_cycle_fails(self):
        self.build({
            "harness-beta": ["harness-gamma"],
            "harness-gamma": ["harness-delta"],
            "harness-delta": ["harness-beta"],
        })
        code, out = run(self.skills, self.root)
        self.assertEqual(code, 1)
        self.assertIn("循环依赖", out)

    def test_self_cycle_fails(self):
        self.build({"harness-beta": ["harness-beta"]})
        code, out = run(self.skills, self.root)
        self.assertEqual(code, 1)
        self.assertIn("循环依赖", out)

    # --- 3. 向上依赖 ---
    def test_upward_dependency_fails(self):
        self.build({
            "harness-alpha": ["harness-beta"],  # L0 depends on L1
        })
        code, out = run(self.skills, self.root)
        self.assertEqual(code, 1)
        self.assertIn("向上依赖", out)

    def test_skip_two_layers_upward_fails(self):
        self.build({
            "harness-beta": ["harness-epsilon"],  # L1 depends on L3
        })
        code, out = run(self.skills, self.root)
        self.assertEqual(code, 1)
        self.assertIn("向上依赖", out)

    # --- 4. Meta 层隔离 ---
    def test_non_meta_depending_on_meta_fails(self):
        self.build({"harness-beta": ["harness-meta"]})
        code, out = run(self.skills, self.root)
        self.assertEqual(code, 1)
        self.assertIn("Meta 层", out)

    def test_meta_may_depend_on_anything(self):
        self.build({
            "harness-alpha": [],
            "harness-epsilon": [],
            "harness-meta": ["harness-epsilon", "harness-alpha"],
        })
        code, out = run(self.skills, self.root)
        self.assertEqual(code, 0, out)

    # --- 5. 引用有效性 ---
    def test_unknown_dependency_fails(self):
        self.build({"harness-beta": ["harness-nonexistent"]})
        code, out = run(self.skills, self.root)
        self.assertEqual(code, 1)
        self.assertIn("未登记的 skill", out)

    def test_dependency_not_on_disk_fails(self):
        # 'harness-gamma' is in LAYERS but we never create its directory
        self.build({"harness-epsilon": ["harness-gamma"]})
        code, out = run(self.skills, self.root)
        self.assertEqual(code, 1)
        self.assertIn("不存在", out)

    # --- 6. 同层依赖 WARN ---
    def test_same_layer_dependency_warns_only(self):
        self.build({
            "harness-gamma": [],
            "harness-delta": [],
        })
        # Re-declare the same-layer edge after both skills exist on disk
        write_skill(self.skills, "harness-gamma", ["harness-delta"])
        code, out = run(self.skills, self.root)
        self.assertEqual(code, 0, out)
        self.assertIn("同层", out)
        code_strict, _ = run(self.skills, self.root, strict=True)
        self.assertEqual(code_strict, 1)

    # --- 7. 未登记 skill WARN ---
    def test_unmapped_skill_warns(self):
        self.build({"harness-rogue": []})
        code, out = run(self.skills, self.root)
        self.assertEqual(code, 0, out)
        self.assertIn("未登记在 LAYERS", out)

    # --- 8. 跨 skill 路径引用 ---
    def test_broken_cross_skill_path_fails(self):
        self.build({"harness-beta": []})
        with open(os.path.join(self.skills, "harness-beta", "SKILL.md"), "a",
                  encoding="utf-8") as f:
            f.write("\nSee `../harness-gamma/references/missing.md` for details.\n")
        os.makedirs(os.path.join(self.skills, "harness-gamma", "references"),
                    exist_ok=True)
        code, out = run(self.skills, self.root)
        self.assertEqual(code, 1)
        self.assertIn("跨 skill 路径", out)

    def test_existing_cross_skill_path_passes(self):
        self.build({"harness-beta": [], "harness-gamma": []})
        target = os.path.join(self.skills, "harness-gamma", "references", "real.md")
        with open(target, "w", encoding="utf-8") as f:
            f.write("real\n")
        with open(os.path.join(self.skills, "harness-beta", "SKILL.md"), "a",
                  encoding="utf-8") as f:
            f.write("\nSee `../harness-gamma/references/real.md` for details.\n")
        code, out = run(self.skills, self.root)
        self.assertEqual(code, 0, out)

    def test_self_path_reference_is_not_cross_skill(self):
        self.build({"harness-beta": []})
        with open(os.path.join(self.skills, "harness-beta", "SKILL.md"), "a",
                  encoding="utf-8") as f:
            f.write("\nRun `harness-beta/references/whatever.py` — file need not exist.\n")
        code, out = run(self.skills, self.root)
        self.assertEqual(code, 0, out)

    # --- 9. 标注完整性 WARN ---
    def test_unlabeled_related_skill_warns(self):
        self.build({"harness-beta": [], "harness-gamma": []})
        with open(os.path.join(self.skills, "harness-beta", "SKILL.md"), "a",
                  encoding="utf-8") as f:
            f.write("- **harness-gamma**: some vague mention with no relation label\n")
        code, out = run(self.skills, self.root)
        self.assertEqual(code, 0, out)
        self.assertIn("无关系标注", out)

    def test_labeled_related_skill_no_warn(self):
        self.build({"harness-beta": [], "harness-gamma": []})
        with open(os.path.join(self.skills, "harness-beta", "SKILL.md"), "a",
                  encoding="utf-8") as f:
            f.write("- see-also   **harness-gamma**: related, no data flow\n")
        code, out = run(self.skills, self.root)
        self.assertEqual(code, 0, out)
        self.assertNotIn("无关系标注", out)

    # --- 10. 真实仓库合规 ---
    def test_real_repo_is_compliant(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = vdd.validate(REAL_SKILLS, REPO_ROOT, strict=True, out=buf)
        self.assertEqual(code, 0, buf.getvalue())


if __name__ == "__main__":
    unittest.main(verbosity=2)
