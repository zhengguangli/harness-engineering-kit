### plan-architect ↔ verification-loop-runner Collaboration

The exec-plan lifecycle is completed by two agents in phased handoffs:

1. **plan-architect creates**: Decompose high-level goals into an exec-plan file (goals, steps, acceptance criteria, risks), written to `docs/exec-plans/active/`. plan-architect does not write implementation code.
2. **verification-loop-runner executes**: Implement each step from the exec-plan one by one. Each step goes through the self-verification loop (implement → self-check → test → review → fix), then mark the step as complete in the exec-plan and add decision logs.
3. **Handoff point**: After plan-architect completes the plan, tell the main conversation "Suggest delegating to verification-loop-runner to execute according to this plan"; verification-loop-runner reads the exec-plan before starting to confirm the definition of done.
4. **Write-back convention**: Only verification-loop-runner can modify step check status and decision logs in the exec-plan; plan-architect only modifies goals/scope/steps when the user requests plan adjustments.

---
Last updated: 2026-06-29
