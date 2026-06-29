#!/usr/bin/env python3
"""Check that agent .md body matches references/*-prompt.md body."""
import os, re, glob, sys

fail = 0
for skill_dir in sorted(glob.glob("skills/harness-*/")):
    skill = os.path.basename(skill_dir.rstrip("/"))
    for agent_md_path in sorted(glob.glob(os.path.join(skill_dir, "agents", "*.md"))):
        agent_name = os.path.splitext(os.path.basename(agent_md_path))[0]
        prompt_path = os.path.join(skill_dir, "references", f"{agent_name}-prompt.md")
        if not os.path.exists(prompt_path):
            continue
        with open(agent_md_path) as f:
            agent = f.read()
        with open(prompt_path) as f:
            prompt = f.read()
        # Extract agent body (after second ---)
        parts = agent.split("---", 2)
        agent_body = parts[2].strip() if len(parts) >= 3 else ""
        # Extract prompt body (before trailing ---\n最后更新)
        prompt_body = re.sub(r"\n---\n最后更新:.*$", "", prompt.rstrip()).strip()
        if agent_body != prompt_body:
            print(f"FAIL: {skill}/{agent_name} — agent .md body differs from references/{agent_name}-prompt.md")
            print(f"FIX:  Sync content between {agent_md_path} and {prompt_path}.")
            fail += 1
sys.exit(1 if fail > 0 else 0)
