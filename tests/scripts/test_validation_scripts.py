#!/usr/bin/env python3
"""
Regression tests for the repo-level validation scripts.

Covers the three scripts that previously had zero test coverage:
  - scripts/validate_skill_triggers.py     (frontmatter + cross-reference)
  - scripts/validate_agent_prompt_sync.py  (Agent 提示词 section presence)
  - scripts/run_trigger_regression.py      (keyword matching logic)

scripts/validate_skill_dependencies.py is covered separately in
tests/dependencies/test_dependency_validation.py.

Uses synthetic fixtures; only stdlib unittest.
"""

import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout

SCRIPTS_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "scripts"))
REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
REAL_SKILLS = os.path.join(REPO_ROOT, "skills")

sys.path.insert(0, SCRIPTS_DIR)
import run_trigger_regression as rtr  # noqa: E402
import validate_skill_dependencies as vdd  # noqa: E402


def write_skill(root, name, body, frontmatter=None):
    d = os.path.join(root, name)
    os.makedirs(d, exist_ok=True)
    fm = frontmatter if frontmatter is not None else (
        "---\n"
        f"name: {name}\n"
        "description: Synthetic fixture skill used only by the validation script regression tests.\n"
        "when_to_use: fixture\n"
        "compatibility: claude-code\n"
        "---\n"
    )
    with open(os.path.join(d, "SKILL.md"), "w", encoding="utf-8") as f:
        f.write(fm + body)


def run_in_fake_repo(script_name, skills_dir, tmp):
    """Copy a script into a fake repo root containing `skills_dir` and run it."""
    fake = os.path.join(tmp, "repo")
    os.makedirs(os.path.join(fake, "scripts"), exist_ok=True)
    shutil.copy(os.path.join(SCRIPTS_DIR, script_name),
                os.path.join(fake, "scripts", script_name))
    os.rename(skills_dir, os.path.join(fake, "skills"))
    r = subprocess.run([sys.executable, os.path.join(fake, "scripts", script_name)],
                       capture_output=True, text=True, cwd=REPO_ROOT)
    return r.stdout + r.stderr


def run_real(script_name):
    r = subprocess.run([sys.executable, os.path.join(SCRIPTS_DIR, script_name)],
                       capture_output=True, text=True, cwd=REPO_ROOT)
    return r.returncode, r.stdout + r.stderr


class TriggerRegressionLogicTests(unittest.TestCase):
    """Pure-logic tests for the keyword matcher — no fixtures needed."""

    def test_match_count_counts_substring_hits(self):
        self.assertEqual(rtr.match_count("harness-commit-gate", "帮我提交代码"), 1)

    def test_match_count_zero_when_no_keyword_present(self):
        self.assertEqual(rtr.match_count("harness-commit-gate", "今天天气不错"), 0)

    def test_match_count_counts_each_keyword_once(self):
        self.assertGreaterEqual(
            rtr.match_count("harness-commit-gate", "git commit 提交代码"), 2)

    def test_every_skill_has_keywords(self):
        for skill in rtr.SKILL_KW:
            self.assertTrue(rtr.SKILL_KW[skill].strip(), f"{skill} has empty keywords")

    def test_no_duplicate_keywords_within_a_skill(self):
        for skill, kw in rtr.SKILL_KW.items():
            words = kw.split()
            dupes = {w for w in words if words.count(w) > 1}
            self.assertEqual(dupes, set(), f"{skill} has duplicate keywords: {dupes}")

    def test_negative_case_passes_when_nothing_matches(self):
        case = {"id": "x", "input": "今天天气不错", "expected_primary_skill": "none",
                "expected_candidates": ["harness-commit-gate"]}
        buf = io.StringIO()
        with redirect_stdout(buf):
            result, _reason, _cands = rtr.process_case(case, json_mode=False)
        self.assertEqual(result, "PASS")

    def test_positive_case_fails_when_primary_absent(self):
        case = {"id": "x", "input": "今天天气不错",
                "expected_primary_skill": "harness-commit-gate",
                "expected_candidates": ["harness-commit-gate"]}
        buf = io.StringIO()
        with redirect_stdout(buf):
            result, _reason, _cands = rtr.process_case(case, json_mode=False)
        self.assertEqual(result, "FAIL")

    def test_real_cases_file_is_valid_and_complete(self):
        with open(os.path.join(REPO_ROOT, "tests", "triggers", "cases.json"),
                  encoding="utf-8") as f:
            cases = json.load(f)
        self.assertGreater(len(cases), 0)
        for c in cases:
            for field in ("id", "input", "expected_primary_skill"):
                self.assertIn(field, c, f"case missing {field}: {c}")

    def test_every_skill_has_at_least_one_case(self):
        """The assessor had keywords but zero cases for a long time."""
        with open(os.path.join(REPO_ROOT, "tests", "triggers", "cases.json"),
                  encoding="utf-8") as f:
            cases = json.load(f)
        covered = {c["expected_primary_skill"] for c in cases}
        for skill in rtr.SKILL_KW:
            self.assertIn(skill, covered, f"{skill} has keywords but no regression case")


class ValidateSkillTriggersTests(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.skills = os.path.join(self.tmp.name, "skills")
        os.makedirs(self.skills)

    def tearDown(self):
        self.tmp.cleanup()

    def _run(self):
        return run_in_fake_repo("validate_skill_triggers.py", self.skills, self.tmp.name)

    def test_valid_skill_passes(self):
        write_skill(self.skills, "harness-alpha",
                    "## Core Principles\n\n- a\n\n## Methodology\n\n- b\n")
        out = self._run()
        self.assertIn("[OK] harness-alpha", out)
        self.assertNotIn("[WARN]", out)

    def test_missing_required_field_warns(self):
        write_skill(self.skills, "harness-alpha", "## Core Principles\n\n- a\n",
                    frontmatter="---\nname: harness-alpha\ndescription: too short\n---\n")
        self.assertIn("missing_field:when_to_use", self._run())

    def test_short_description_warns(self):
        write_skill(self.skills, "harness-alpha", "## Core Principles\n\n- a\n",
                    frontmatter="---\nname: harness-alpha\ndescription: short\n"
                                "when_to_use: fixture\ncompatibility: claude-code\n---\n")
        self.assertIn("description_too_short", self._run())

    def test_dangling_cross_reference_warns(self):
        write_skill(self.skills, "harness-alpha",
                    "## Core Principles\n\n- a\n\n## Related Skills\n\n"
                    "- see-also **harness-does-not-exist**: broken pointer\n")
        self.assertIn("references non-existent skill", self._run())


class ValidateAgentPromptSyncTests(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.skills = os.path.join(self.tmp.name, "skills")
        os.makedirs(self.skills)

    def tearDown(self):
        self.tmp.cleanup()

    def _run(self):
        return run_in_fake_repo("validate_agent_prompt_sync.py", self.skills, self.tmp.name)

    def test_present_agent_section_passes(self):
        write_skill(self.skills, "harness-alpha",
                    "## Agent 提示词\n\n## alpha-runner\n\n### Role Definition\n\nx\n")
        self.assertIn("[OK] harness-alpha", self._run())

    def test_missing_agent_section_warns(self):
        write_skill(self.skills, "harness-alpha", "## Core Principles\n\n- a\n")
        self.assertIn("missing '## Agent 提示词' section", self._run())


class RealRepoGuards(unittest.TestCase):
    """Cheap end-to-end guards over the real repository."""

    def test_frontmatter_validation_passes(self):
        code, out = run_real("validate_skill_triggers.py")
        self.assertEqual(code, 0, out)

    def test_agent_prompt_validation_passes(self):
        code, out = run_real("validate_agent_prompt_sync.py")
        self.assertEqual(code, 0, out)

    def test_dependency_validation_passes_strict(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = vdd.validate(REAL_SKILLS, REPO_ROOT, strict=True, out=buf)
        self.assertEqual(code, 0, buf.getvalue())


class TriggerContractConsistencyTests(unittest.TestCase):
    """SKILL_KW and when_to_use are two representations of the same intent.

    They are maintained by hand in different files and nothing kept them in
    sync, so they drifted. Measured on 2026-09-24: 9 skills had keywords absent
    from their own when_to_use, and golden-principles had 5 of 6 explicit
    trigger phrases with no keyword coverage at all.

    These tests act as a ratchet: they record the current drift as a baseline
    and fail if it gets worse. Tightening the baseline is a deliberate act.
    """
    BASELINE_ORPHAN_KEYWORDS = 19   # keywords with no basis in when_to_use
    BASELINE_UNCOVERED_PHRASES = 13  # explicit trigger phrases with no keyword

    @staticmethod
    def _when_to_use(skill):
        import re
        txt = open(os.path.join(REAL_SKILLS, skill, "SKILL.md"), encoding="utf-8").read()
        m = re.search(r"^when_to_use:\s*\|\s*$(.*?)^(?:\w[\w-]*:|---)",
                      txt, re.M | re.S)
        return m.group(1) if m else ""

    def _orphan_keywords(self):
        out = []
        for skill, kw in rtr.SKILL_KW.items():
            wt = self._when_to_use(skill)
            for w in kw.split():
                if not any(p in wt for p in w.split("+")):
                    out.append((skill, w))
        return out

    def _uncovered_phrases(self):
        import re
        out = []
        for skill in rtr.SKILL_KW:
            wt = self._when_to_use(skill)
            m = re.search(r"显式触发：([^\n]*)", wt)
            if not m:
                continue
            phrases = [p.strip().strip("\"'") for p in re.split(r"[、，,]", m.group(1))
                       if p.strip()]
            for p in phrases:
                if not any(all(x in p for x in w.split("+"))
                           for w in rtr.SKILL_KW[skill].split()):
                    out.append((skill, p))
        return out

    def test_orphan_keywords_do_not_increase(self):
        found = self._orphan_keywords()
        self.assertLessEqual(
            len(found), self.BASELINE_ORPHAN_KEYWORDS,
            f"{len(found)} keywords have no basis in when_to_use "
            f"(baseline {self.BASELINE_ORPHAN_KEYWORDS}): {found}")

    def test_uncovered_trigger_phrases_do_not_increase(self):
        found = self._uncovered_phrases()
        self.assertLessEqual(
            len(found), self.BASELINE_UNCOVERED_PHRASES,
            f"{len(found)} explicit trigger phrases have no keyword "
            f"(baseline {self.BASELINE_UNCOVERED_PHRASES}): {found}")

    def test_reports_current_drift(self):
        """Informational: prints the drift so it is visible in test output."""
        o = self._orphan_keywords()
        u = self._uncovered_phrases()
        print(f"\n    orphan keywords: {len(o)}  "
              f"uncovered trigger phrases: {len(u)}")
        for skill, w in o:
            print(f"      orphan keyword  {skill}: '{w}'")
        for skill, p in u:
            print(f"      uncovered phrase {skill}: '{p}'")


class TaskCoverageMappingTests(unittest.TestCase):
    """REQUIRES in scripts/audit_task_coverage.py is a THIRD representation of
    trigger intent (after when_to_use and SKILL_KW), so it needs the same
    anti-drift guard the other two got.

    Two failure modes are checked:
      - dead patterns: keys no acceptance criterion ever references
      - orphan criteria: criteria no pattern can match, which silently pass
        through the checker's only remaining guard
    """
    BASELINE_DEAD_PATTERNS = 0
    BASELINE_UNMAPPED_CRITERIA = 0

    def _load(self):
        sys.path.insert(0, SCRIPTS_DIR)
        import audit_task_coverage as atc
        import json
        tasks = json.load(open(os.path.join(REPO_ROOT, "tests", "tasks", "tasks.json"),
                               encoding="utf-8"))
        crits = [c for t in tasks for c in t["acceptance_criteria"]]
        return atc, crits

    def test_no_dead_patterns(self):
        atc, crits = self._load()
        blob = " ".join(crits).lower()
        dead = [k for k in atc.REQUIRES if k.lower() not in blob]
        self.assertEqual(dead, [],
                         f"{len(dead)} REQUIRES patterns are never referenced by any "
                         f"acceptance criterion: {dead}")

    def test_every_criterion_maps_to_a_pattern(self):
        """A criterion that matches no REQUIRES key falls through to the
        checker's only remaining logic. If that logic is ever removed the
        criterion would be silently reported as covered."""
        atc, crits = self._load()
        unmapped = []
        for c in crits:
            if not any(k.lower() in c.lower() for k in atc.REQUIRES):
                unmapped.append(c)
        self.assertEqual(unmapped, [],
                         f"{len(unmapped)} criteria match no REQUIRES key and rely on "
                         f"fallback logic: {unmapped}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
