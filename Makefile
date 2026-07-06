.PHONY: triggers-check triggers-regression triggers-report prompts-sync-check triggers-all

PYTHON = python3

triggers-check:
	$(PYTHON) scripts/validate_skill_triggers.py

triggers-regression:
	$(PYTHON) scripts/run_trigger_regression.py

triggers-report:
	$(PYTHON) scripts/run_trigger_regression.py --json

prompts-sync-check:
	$(PYTHON) scripts/validate_agent_prompt_sync.py

triggers-all: triggers-check triggers-regression prompts-sync-check
