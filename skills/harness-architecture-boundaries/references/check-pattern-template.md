# Architecture Check Pattern Template

Defines how the `boundary-auditor` agent inline-checks each architecture rule documented in `ARCHITECTURE.md`. Each rule maps to one check pattern — describing "what to check, how to check it, and what a violation looks like."

> This is not an executable script, but a check methodology reference for the agent — the agent uses tool combinations like `Grep`/`Bash`/`list_dir` to inline-execute these checks.
>
> Language portability note: The import search patterns in the examples below are primarily TypeScript-based. In different language stacks, use the corresponding syntax (e.g., Python: `import ... from ...` / `import module`; Go: `"import"`; Java: `import ...;`; Rust: `use ...`).

## Check Pattern Structure

Each rule's check pattern includes the following fields:

```
## Rule: <Rule Name>

- **Constraint Description**: <One sentence describing what this rule restricts>
- **Inspection Method**: <What tool combination the agent uses to check, e.g., Grep searching import statements, Glob enumerating files>
- **Violation Signature**: <What search hit / file existence / structural omission counts as a violation>
- **Fix Direction**: <What is the minimal fix path once a violation is found>
```

## Example 1: Layering Dependency Direction Check

```
## Rule: Service layer must not directly import Runtime internal modules

- **Constraint Description**: Code in the Service layer can only depend forward on the Types/Config/Repo layers, and must not reverse-import internal modules of the Runtime layer.
- **Inspection Method**:
  1. Use Glob to enumerate all source files under `src/**/service/`.
  2. For each file, use Grep to search for patterns like `import.*runtime` and `from.*runtime`.
  3. Exclude legitimate public interface references (if the Runtime layer has a clear public API file, check whether only the public entry point is imported).
- **Violation Signature**: `src/<domain>/service/foo.ts` contains `import { Bar } from '../../runtime/bar'` — a direct reference to a Runtime internal module.
- **Fix Direction**: Change to access via the public interface exposed by the Runtime layer, or move shared logic down to the Types/Config layer.
```

## Example 2: Data Boundary Check

```
## Rule: External data must be parsed into strongly-typed structures when entering the system boundary

- **Constraint Description**: All cross-boundary external data (API responses, user input) must be parsed at the boundary; weak types must not be passed through after mere validation.
- **Inspection Method**:
  1. Use Glob to enumerate boundary layer files (e.g., `src/<domain>/api/`, `src/<domain>/routes/`).
  2. For each file, use Grep to search for patterns like `any` type annotations, `as` type assertions, and direct access to `response.data`.
  3. Check for patterns that "validate field existence then pass the raw object downstream" (e.g., `if (data.field) { return data; }`).
- **Violation Signature**: Boundary layer function return types contain `any` or `unknown`; boundary layer passes unparsed raw response objects directly downstream.
- **Fix Direction**: Use type guards or schema parsing libraries at the boundary to parse external data into explicit types before passing it downstream.
```

## Example 3: Cross-Cutting Concern Entry Point Check

```
## Rule: Cross-cutting concerns (authentication/logging/configuration) must enter each layer through a single Providers entry point

- **Constraint Description**: Cross-cutting concerns such as authentication, connectors, telemetry, and feature flags must not be scattered across arbitrary business layers — they must enter through an explicit Providers interface.
- **Inspection Method**:
  1. Use Glob to enumerate all source files outside the Providers layer.
  2. Use Grep to search for imports of cross-cutting concerns (e.g., `import.*auth`, `import.*logger`, `import.*config`).
  3. Exclude legitimate references from the Providers layer itself and utility function references.
- **Violation Signature**: `src/<domain>/service/foo.ts` directly contains `import { auth } from '@/infra/auth'` — bypassing the Providers entry point.
- **Fix Direction**: Change to injection through Providers, or confirm the dependency is not a cross-cutting concern and update the rule.
```

## Process for Adding a New Check Pattern

1. Extract one rule from ARCHITECTURE.md.
2. Define the check pattern following the template above — key point is to break down "how to check" into Grep/Glob/Bash operation steps executable by the agent.
3. If the check requires project-specific context (e.g., specific layer names, directory paths), explicitly mark them as placeholders in the check pattern — the agent will read actual values from ARCHITECTURE.md at audit time.
4. Make the fix direction concrete — not "follow the rule," but "change X to Y, or move it to Z location."
