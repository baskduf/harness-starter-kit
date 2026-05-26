# AGENTS.md

## Purpose

This repository is a reusable harness engineering starter kit. Its job is to
teach agents how to add durable project rules, constraints, feedback loops,
knowledge storage, and drift checks to another repository.

When applying this kit to a target repository, treat the target repository as
the source of truth. Preserve its existing architecture and tools.

## How To Apply This Kit To A Target Repository

1. Inspect the target repository before editing.
   - Identify language, framework, package manager, test command, linter, CI,
     directory layout, and existing agent instruction files.
   - Read existing `README`, `AGENTS.md`, `CLAUDE.md`, contribution docs, and CI
     configs if present.

2. Install only the missing harness pieces.
   - Add `AGENTS.md` if there is no durable agent instruction file.
   - Add `docs/decisions`, `docs/failures`, `docs/conventions`, and
     `docs/domain` if the target has no equivalent knowledge store.
   - Add drift checks under `scripts/` when no equivalent checks exist.
   - Add CI or pre-commit wiring only when it fits the existing tooling.

3. Prefer local conventions over starter-kit defaults.
   - Use the target repo's naming, formatting, package manager, and test runner.
   - Do not introduce a new framework to enforce a rule that existing tooling
     can already enforce.

4. Make rules enforceable where practical.
   - If `AGENTS.md` says "no direct database access from routes", add a lint,
     import, test, or review check that can catch violations.
   - If an automated check is not practical, document the manual review point.

5. Avoid overwriting existing files.
   - If a file exists, patch it carefully or create a clearly named snippet for
     the maintainer to merge.
   - Never delete target project files unless the user explicitly asks.

6. Finish with an adoption report.
   - List files added or changed.
   - List checks the agent can run.
   - List remaining manual steps.
   - Name any assumptions made about the target stack.

## Harness Components

### Instruction Document

Use `AGENTS.md` for agent-facing rules. Keep it concise, structured, and
specific. Include project overview, directory rules, commands, forbidden
changes, testing expectations, and PR behavior.

### Architecture Constraints

Use tools that block invalid code before it is merged: linters, formatters,
type checks, dependency boundaries, import rules, schema validation, and
pre-commit hooks.

### Feedback Loops

Provide guides and sensors.

- Guides: examples, tests, fixtures, API contracts, golden files
- Sensors: lint failures, type failures, test failures, CI failures, runtime
  checks, observability checks

### Knowledge Store

Store durable context in `docs/`:

- `docs/decisions/` for Architecture Decision Records
- `docs/failures/` for approaches already tried and rejected
- `docs/conventions/` for project-specific coding rules
- `docs/domain/` for business language, workflows, and invariants

### Garbage Collection

Add checks for drift:

- code drift: unused code, dead imports, duplicate helpers
- document drift: `AGENTS.md` references missing files or stale commands
- structure drift: temporary files or paths outside the agreed architecture

## Starter Kit Editing Rules

- Keep templates generic and conservative.
- Do not bake in a single product architecture.
- Add profile-specific guidance under `templates/profiles/<profile>/`.
- Scripts should be safe by default and avoid overwriting user files.
- Favor clear Markdown and small Python scripts over heavyweight generators.

