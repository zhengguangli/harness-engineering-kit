.PHONY: triggers-check triggers-regression triggers-report prompts-sync-check triggers-all

triggers-check:
	./scripts/validate-skill-triggers.sh

triggers-regression:
	./scripts/run-trigger-regression.sh

triggers-report:
	./scripts/run-trigger-regression.sh --json

prompts-sync-check:
	./scripts/validate-agent-prompt-sync.sh

triggers-all: triggers-check triggers-regression prompts-sync-check
