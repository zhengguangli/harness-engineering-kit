#!/usr/bin/env python3
"""
Output-specification executability audit.

A skill's Output Specification is a promise. This audit checks whether each
promise is mechanically actionable — does the spec name a concrete path, a
format template, or a field list, or does it just say "output the results"?

This is specification conformance testing, NOT outcome effectiveness. It
catches "the spec is incomplete or vague", which is a prerequisite for any
later A/B experiment to mean anything: if the spec cannot say what success
looks like, no experiment can measure it.

Checks per skill:
  1. Output Specification section exists
  2. If it promises a persisted file, a concrete path is named
  3. If it promises a structured format, a template or field list is given
  4. No unbounded vagueness ("output the results", "as appropriate")
  5. If it says "conversation only", that is stated explicitly
"""
import os
import re
import sys
import glob

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
SKILLS_DIR = os.path.join(ROOT, "skills")

VAGUE = [
    r"output the results?",
    r"as appropriate",
    r"if necessary",
    r"etc\.?$",
    r"and so on",
]
PATH_RE = re.compile(r"`[A-Za-z0-9_./-]+\.[a-z]+`")
TEMPLATE_RE = re.compile(r"```")


def agent_block(lines):
    s = next((i for i, l in enumerate(lines)
              if l.startswith("## ") and l[3:].strip() == "Agent 提示词"), None)
    if s is None:
        return []
    e, seen = len(lines), False
    for j in range(s + 1, len(lines)):
        if lines[j].startswith("## "):
            if not seen:
                seen = True
                continue
            e = j
            break
    return lines[s + 1:e]


def section(lines, title, level=3):
    pre = "#" * level + " "
    s = next((i for i, l in enumerate(lines)
              if l.startswith(pre) and l[len(pre):].strip() == title), None)
    if s is None:
        return []
    e = next((j for j in range(s + 1, len(lines)) if lines[j].startswith(pre)), len(lines))
    return lines[s + 1:e]


def audit(skill):
    path = os.path.join(SKILLS_DIR, skill, "SKILL.md")
    lines = open(path, encoding="utf-8").readlines()
    ab = agent_block(lines)
    spec = section(ab, "Output Specification", level=3)
    text = "".join(spec)
    issues = []

    if not spec:
        return [("CRITICAL", "no Output Specification section in the agent prompt")]

    # 1. promises a persisted file but names no path.
    #    Negation must be handled: "not persisted to file" is the opposite claim.
    persist_claim = re.search(
        r"output path|persist|archive|overwrit|save to|write.*file", text, re.I)
    negated = re.search(
        r"not persisted|do not create|no file|conversation only|output in conversation|"
        r"retract file writes|output primarily in conversation", text, re.I)
    if persist_claim and not negated and not PATH_RE.search(text):
        issues.append(("HIGH", "promises a persisted file but names no concrete path"))

    # 2. promises a structured format but gives no template or field list.
    #    A field list may appear inline in parentheses, as a bullet, in a table,
    #    or as a quoted format pattern.
    if re.search(r"structured|format|template|report", text, re.I):
        has_template = bool(TEMPLATE_RE.search(text)) or \
                       bool(re.search(r"references/[\w.-]+\.md", text))
        has_fields = (bool(re.search(r"^-\s+\*\*[A-Z]", text, re.M)) or
                      bool(re.search(r"\|\s*\w+.*\|", text)) or
                      bool(re.search(r"\([A-Z][^)]{10,}\)", text)) or
                      bool(re.search(r'"[^"]*\+[^"]*"', text)))
        if not (has_template or has_fields):
            issues.append(("MEDIUM", "claims a structured format but gives neither a "
                                     "template nor a field list"))

    # 3. unbounded vagueness
    for pat in VAGUE:
        for m in re.finditer(pat, text, re.I):
            frag = text[max(0, m.start()-40):m.end()+20].replace("\n", " ").strip()
            issues.append(("LOW", f"vague phrasing: ...{frag}..."))

    # 4. conversation-only must be stated explicitly if no path is named
    if (not PATH_RE.search(text) and not negated
            and not re.search(r"conversation|chat|no file", text, re.I)):
        issues.append(("MEDIUM", "no output path named and does not say output is "
                                 "conversation-only — the destination is unspecified"))

    return issues


def main():
    print("== output specification executability audit ==")
    print()
    total = 0
    for d in sorted(glob.glob(os.path.join(SKILLS_DIR, "harness-*"))):
        skill = os.path.basename(d)
        issues = audit(skill)
        if not issues:
            print(f"[OK] {skill}")
            continue
        total += len(issues)
        print(f"[{len(issues)} issue(s)] {skill}")
        for sev, msg in issues:
            print(f"    [{sev}] {msg}")
    print()
    print(f"summary: {total} issue(s) across 13 skills")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
