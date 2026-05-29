# Changelog

Notable project changes should be recorded here before release tags are cut.

## v0.1.0 - 2026-05-29

Initial early release of `harness-starter-kit`.

This release is for maintainers who want to make repositories safer for AI
coding agents through durable instructions, project memory, feedback loops, and
drift checks. The kit is prompt-first by design; the installer is a conservative
bootstrap helper, not a full automatic migration tool.

### Added

- Prompt-first adoption workflow for applying the kit from a target repository.
- Generic harness templates for `AGENTS.md`, knowledge storage, and drift
  checks.
- Stack profile snippets for Python, TypeScript, Node.js, Next.js, React, Vue,
  Django, Flask, FastAPI, Spring Boot, and Android.
- `/harness doctor`, `/harness update`, and `/harness refresh` command
  workflows.
- Drift checks for documentation references, structure hygiene, encoding
  hygiene, and effectiveness measurement plans.
- Harness Doctor baseline scoring across agent instructions, feedback loops,
  durable memory, structural safety, and adoption clarity.
- Fixture smoke tests and an opt-in FastAPI profile E2E test.
- Adoption report and effectiveness report templates.
- Lifecycle pilot notes, launch essay link, and Django dogfood repository link.
