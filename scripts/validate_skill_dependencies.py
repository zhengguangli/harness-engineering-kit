#!/usr/bin/env python3
"""
Skill 依赖方向与循环依赖校验（TD-001 的机械强制实现）。

权威来源（single source of truth）：
  - 层级定义  → docs/ARCHITECTURE.md "Skill Layering & Dependency Direction"（固化为下方 LAYERS）
  - 依赖声明  → 各 SKILL.md frontmatter 的 `depends_on` 数组

`depends_on` 只表达**真实数据/产出传递**。路由、参见、模板出处指针一律不入此字段，
它们属于 `## Related Skills` 的人读说明，不参与依赖图构建。

校验规则：
  1. 环检测        — depends_on 图中不得存在环路（FAIL）
  2. 向下流动      — Layer N 只可依赖 Layer <= N；依赖更高层属向上引用（FAIL）
  3. Meta 层隔离   — 非 Meta skill 不得依赖 Meta 层 skill（FAIL）
  4. 引用有效性    — depends_on 中的 skill 必须存在于 skills/ 且登记在层级表中（FAIL）
  5. 同层依赖      — 同层 skill 之间的依赖（WARN，同层应为并行关系）
  6. 标注完整性    — Related Skills 中引用其他 skill 但无任何关系标注的条目（WARN）
  7. 跨 skill 路径 — SKILL.md/references 中 `../harness-*/references/*` 引用必须存在（FAIL）

Usage:
    python3 scripts/validate_skill_dependencies.py            # 校验
    python3 scripts/validate_skill_dependencies.py --strict   # WARN 也视为失败
    python3 scripts/validate_skill_dependencies.py --graph    # 打印依赖图
    python3 scripts/validate_skill_dependencies.py --paths    # 只打印跨 skill 路径引用
"""

import os
import re
import sys
import argparse

ROOT_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
SKILLS_DIR = os.path.join(ROOT_DIR, "skills")

# ---------------------------------------------------------------------------
# 层级定义 — 与 docs/ARCHITECTURE.md "Skill Layering & Dependency Direction" 保持一致
# 修改 ARCHITECTURE.md 的层级时必须同步此处
# ---------------------------------------------------------------------------
LAYERS = {
    0: ["harness-project-intake"],
    1: ["harness-bootstrap"],
    2: [
        "harness-repo-map",
        "harness-architecture-boundaries",
        "harness-golden-principles",
        "harness-prompt-optimizer",
    ],
    3: ["harness-exec-plans"],
    4: ["harness-verification-loop", "harness-observability-and-browser"],
    5: ["harness-commit-gate"],
}

# Meta 层：可被任意层调用；其自身依赖也豁免层级方向校验
META_LAYER = ["harness-orchestration", "harness-authoring", "harness-skill-quality-assessor"]

# 人读说明章节（不参与依赖图，仅做标注完整性 WARN 检查）
DESCRIPTION_SECTIONS = [
    "Related Skills",
    "Cross-Skill Handoff Points",
    "相关 Skill",
    "配合的 agent",
]

SKILL_NAME_RE = re.compile(r"harness-[a-z]+(?:-[a-z]+)*")
CROSS_SKILL_PATH_RE = re.compile(r"(?:\.\./)?harness-[a-z0-9-]+/references/[A-Za-z0-9._-]+")
RELATION_KEYWORDS = (
    "input", "output", "routes-to", "see-also",
    "upstream", "downstream", "peer", "cross-reference",
)


def skill_layer(skill_name, layers=None, meta=None):
    """Return (layer_number, is_meta). layer_number is None when unknown or meta."""
    layers = LAYERS if layers is None else layers
    meta = META_LAYER if meta is None else meta
    for layer, names in layers.items():
        if skill_name in names:
            return layer, False
    if skill_name in meta:
        return None, True
    return None, False


def all_known_skills(layers=None, meta=None):
    layers = LAYERS if layers is None else layers
    meta = META_LAYER if meta is None else meta
    names = set()
    for names_list in layers.values():
        names.update(names_list)
    names.update(meta)
    return names


def read_lines(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.readlines()
    except (OSError, UnicodeDecodeError):
        return []


def parse_frontmatter(lines):
    """Parse frontmatter blocks. Supports scalar fields and simple YAML lists.

    Handles multiple consecutive ---...--- blocks (slug block + harness block).
    """
    fm = {}
    if not lines or lines[0].strip() != "---":
        return fm

    i = 1
    current_key = None
    while i < len(lines):
        stripped = lines[i].strip()
        if stripped == "---":
            if i + 1 < len(lines) and lines[i + 1].strip() == "---":
                i += 2
                current_key = None
                continue
            break
        if stripped.startswith("- ") and current_key:
            fm.setdefault(current_key, [])
            if isinstance(fm[current_key], list):
                fm[current_key].append(stripped[2:].strip().strip("\"'"))
        else:
            m = re.match(r"^([A-Za-z_][\w-]*)\s*:\s*(.*)$", stripped)
            if m:
                current_key = m.group(1)
                value = m.group(2).strip().strip("\"'")
                fm[current_key] = value if value else []
            else:
                current_key = None
        i += 1
    return fm


def get_depends_on(fm):
    """Normalise the depends_on frontmatter field into a list of skill names."""
    raw = fm.get("depends_on")
    if raw is None:
        return []
    if isinstance(raw, list):
        items = raw
    else:
        # Inline form: depends_on: [a, b]  or  depends_on: a
        items = re.split(r"[,\[\]\s]+", str(raw))
    out = []
    for item in items:
        name = str(item).strip().strip("\"'[]")
        if name:
            out.append(name)
    return out


def get_section_content(lines, section_title):
    """Get body lines of a '## <title>' section (exact title match)."""
    start = -1
    for i, line in enumerate(lines):
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m and m.group(1).strip() == section_title:
            start = i + 1
            break
    if start == -1:
        return []
    content = []
    for line in lines[start:]:
        if re.match(r"^##\s+", line.strip()):
            break
        content.append(line)
    return content


def collect_skills(skills_dir):
    """Return {skill_name: {'lines': [...], 'files': [...]}} for every skill on disk."""
    skills = {}
    if not os.path.isdir(skills_dir):
        return skills
    for entry in sorted(os.listdir(skills_dir)):
        d = os.path.join(skills_dir, entry)
        if not os.path.isdir(d) or not entry.startswith("harness-"):
            continue
        skill_md = os.path.join(d, "SKILL.md")
        if not os.path.isfile(skill_md):
            continue
        files = []
        refs_dir = os.path.join(d, "references")
        if os.path.isdir(refs_dir):
            for root, _dirs, names in os.walk(refs_dir):
                for n in names:
                    files.append(os.path.join(root, n))
        skills[entry] = {"lines": read_lines(skill_md), "files": files}
    return skills


def find_cycles(edges):
    """Return list of cycles (each a list of nodes, first node repeated at end)."""
    cycles = []
    seen = set()
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {n: WHITE for n in edges}
    stack = []

    def dfs(node):
        color[node] = GRAY
        stack.append(node)
        for dep in sorted(edges.get(node, ())):
            if dep not in color:
                continue
            if color[dep] == GRAY:
                idx = stack.index(dep)
                cycle = stack[idx:] + [dep]
                key = tuple(cycle)
                if key not in seen:
                    seen.add(key)
                    cycles.append(cycle)
            elif color[dep] == WHITE:
                dfs(dep)
        stack.pop()
        color[node] = BLACK

    for node in sorted(edges):
        if color[node] == WHITE:
            dfs(node)
    return cycles


def describe_layer(skill_name, layers=None, meta=None):
    layer, is_meta = skill_layer(skill_name, layers, meta)
    if is_meta:
        return "Meta"
    if layer is None:
        return "????"
    return f"L{layer}"


def validate(skills_dir, root_dir, layers=None, meta=None, strict=False,
             show_graph=False, show_paths=False, out=None):
    """Run all dependency checks. Returns process exit code."""
    layers = LAYERS if layers is None else layers
    meta = META_LAYER if meta is None else meta
    known = all_known_skills(layers, meta)
    out = out if out is not None else sys.stdout

    def say(msg=""):
        print(msg, file=out)

    skills = collect_skills(skills_dir)
    on_disk = set(skills)

    say("== skill dependency validation ==")
    say()

    # --- 0. 层级表自检 ---
    for s in sorted(on_disk - known):
        say(f"[WARN] {s}: 未登记在 LAYERS 层级表中，跳过其层级校验")
    for name in sorted(known - on_disk):
        say(f"[WARN] LAYERS 中的 {name} 在 skills/ 下不存在")

    # --- 0b. 跨 skill 路径引用存在性 ---
    path_fail = 0
    path_total = 0
    cross_paths = []
    for skill, data in sorted(skills.items()):
        skill_dir = os.path.join(skills_dir, skill)
        texts = ["\n".join(data["lines"])]
        for f in data["files"]:
            texts.append("\n".join(read_lines(f)))
        seen = set()
        for text in texts:
            for rel in CROSS_SKILL_PATH_RE.findall(text):
                if rel in seen:
                    continue
                seen.add(rel)
                # Self-references (a skill pointing at its own references/) are
                # not cross-skill references and are validated elsewhere.
                if rel.lstrip("./").split("/")[0] == skill:
                    continue
                path_total += 1
                # Resolve: '../'-prefixed paths are relative to the skill dir;
                # bare 'harness-*/...' mentions are ambiguous, so accept any of
                # skill-dir-relative, repo-root-relative or skills/-relative.
                candidates = [os.path.normpath(os.path.join(skill_dir, rel))]
                if rel.startswith("../"):
                    candidates.append(os.path.normpath(
                        os.path.join(root_dir, "skills", rel[3:])))
                else:
                    candidates.append(os.path.normpath(os.path.join(root_dir, rel)))
                    candidates.append(os.path.normpath(
                        os.path.join(root_dir, "skills", rel)))
                exists = any(os.path.isfile(c) for c in candidates)
                cross_paths.append((skill, rel, exists))
                if not exists:
                    say(f"[FAIL] {skill} 引用不存在的跨 skill 路径: {rel}")
                    path_fail = 1

    if show_paths:
        say("--- cross-skill path references ---")
        for skill, rel, ok in cross_paths:
            say(f"  [{'OK' if ok else 'MISSING'}] {skill} -> {rel}")
        return 0

    if not path_fail:
        say(f"[OK] {path_total} 个跨 skill 路径引用全部存在")

    # --- 1. 构建 depends_on 图 ---
    edges = {}
    declared = {}
    for skill, data in skills.items():
        fm = parse_frontmatter(data["lines"])
        deps = get_depends_on(fm)
        declared[skill] = deps
        edges[skill] = set(deps)

    if show_graph:
        say("--- dependency graph (S -> dep means S depends on dep) ---")
        for skill in sorted(edges):
            deps = sorted(edges[skill])
            say(f"{describe_layer(skill, layers, meta):6} {skill} -> "
                f"{', '.join(deps) if deps else '(none)'}")
        say()

    # --- 2. 引用有效性 ---
    bad_ref_fail = 0
    for skill, deps in sorted(declared.items()):
        for dep in deps:
            if dep not in known:
                say(f"[FAIL] {skill} 的 depends_on 引用未登记的 skill: {dep}")
                bad_ref_fail = 1
            elif dep not in on_disk:
                say(f"[FAIL] {skill} 的 depends_on 引用 skills/ 下不存在的 skill: {dep}")
                bad_ref_fail = 1
    if not bad_ref_fail:
        total_deps = sum(len(v) for v in declared.values())
        say(f"[OK] {total_deps} 条 depends_on 声明全部有效")

    # --- 3. 环检测 ---
    cycles = find_cycles(edges)
    for cycle in cycles:
        say(f"[FAIL] 循环依赖: {' -> '.join(cycle)}")
    if not cycles:
        say("[OK] 无循环依赖")

    # --- 4. 方向校验 ---
    direction_fail = 0
    same_layer_warn = 0
    for skill in sorted(edges):
        layer, is_meta = skill_layer(skill, layers, meta)
        if is_meta or layer is None:
            continue
        for dep in sorted(edges[skill]):
            dep_layer, dep_is_meta = skill_layer(dep, layers, meta)
            if dep_is_meta:
                say(f"[FAIL] {skill} (L{layer}) 依赖 Meta 层 skill {dep} — Meta 层只能被调用，不得被依赖")
                direction_fail = 1
                continue
            if dep_layer is None:
                continue  # already reported as bad ref
            if dep_layer > layer:
                say(f"[FAIL] {skill} (L{layer}) 向上依赖 {dep} (L{dep_layer}) — 违反向下流动规则")
                direction_fail = 1
            elif dep_layer == layer:
                say(f"[WARN] {skill} (L{layer}) 依赖同层 skill {dep} — 同层应为并行关系")
                same_layer_warn += 1

    if not direction_fail and not same_layer_warn:
        say("[OK] 依赖方向全部向下")

    # --- 5. Related Skills 标注完整性（WARN 级，不建边） ---
    unlabeled_warn = 0
    for skill, data in sorted(skills.items()):
        for title in DESCRIPTION_SECTIONS:
            for raw in get_section_content(data["lines"], title):
                line = raw.strip()
                if not line.startswith(("-", "*", "|")):
                    continue
                refs = set(SKILL_NAME_RE.findall(line)) - {skill}
                if not refs:
                    continue
                lowered = line.lower()
                if not any(kw in lowered for kw in RELATION_KEYWORDS):
                    say(f"[WARN] {skill} 在 '{title}' 中引用 "
                        f"{', '.join(sorted(refs))} 但无关系标注"
                        f"（input/output/routes-to/see-also）")
                    unlabeled_warn += 1

    # --- 汇总 ---
    total_deps = sum(len(v) for v in declared.values())
    warns = len(on_disk - known) + len(known - on_disk) + same_layer_warn + unlabeled_warn
    say()
    say(f"summary: skills={len(skills)}  dep_edges={total_deps}  "
        f"cycles={len(cycles)}  direction_fail={direction_fail}  "
        f"bad_ref={bad_ref_fail}  cross_path_fail={path_fail}  warn={warns}")

    if cycles or direction_fail or bad_ref_fail or path_fail:
        say()
        say("Dependency validation FAILED.")
        return 1

    if strict and warns:
        say()
        say("Dependency validation FAILED (strict mode).")
        return 1

    say()
    say("All skill dependency checks passed.")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Skill 依赖方向与循环依赖校验")
    parser.add_argument("--strict", action="store_true", help="将 WARN 级问题也视为失败")
    parser.add_argument("--graph", action="store_true", help="打印依赖图")
    parser.add_argument("--paths", action="store_true", help="只打印跨 skill 路径引用")
    args = parser.parse_args()

    return validate(SKILLS_DIR, ROOT_DIR, strict=args.strict,
                    show_graph=args.graph, show_paths=args.paths)


if __name__ == "__main__":
    sys.exit(main())
