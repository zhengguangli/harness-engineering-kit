.PHONY: triggers-check triggers-regression keyword-consistency triggers-report triggers-all

triggers-check:
	./scripts/validate-skill-triggers.sh

triggers-regression:
	./scripts/run-trigger-regression.sh

keyword-consistency:
	./scripts/validate-keyword-consistency.sh

triggers-report:
	./scripts/run-trigger-regression.sh --json

triggers-all: triggers-check keyword-consistency triggers-regression triggers-report
