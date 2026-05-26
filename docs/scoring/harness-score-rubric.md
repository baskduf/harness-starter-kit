# Harness Score Rubric

Harness Score measures how ready a repository is for reliable AI coding agent
collaboration.

The goal is not to gamify documentation. The goal is to find weak points where
AI coding agents are likely to repeat mistakes because guidance, constraints,
memory, or validation loops are missing from the repository.

## Scoring Principles

- Score durable repository artifacts, not chat instructions.
- Prefer executable checks over requests for discipline.
- Prefer project-specific rules over generic advice.
- Award partial credit for weak but real evidence.
- Give 0 when evidence is absent, only implied, or known only from conversation.
- Record missing evidence in the report so the maintainer knows what to improve.

## 1. Agent Instructions / 20

Evaluate whether the repository has durable instructions for AI coding agents.

```text
Agent instruction file exists: 5
Project overview is clear: 3
Exact build/test/lint commands exist: 4
Architecture boundaries are documented: 4
Forbidden actions are documented: 2
Security/safety notes exist: 2
```

What counts:

- `AGENTS.md`, `CLAUDE.md`, Cursor rules, Copilot instructions, or equivalent.
- A concise project overview that helps an agent understand what the repository
  is for.
- Exact commands such as `python -m unittest discover -s tests`, `npm test`, or
  `mvn test`.
- Boundaries such as directory ownership, dependency rules, generated file
  rules, API layering, or framework-specific constraints.
- Explicit forbidden actions such as "do not edit generated files" or "never
  commit secrets".
- Safety notes about credentials, production data, destructive commands, or
  privacy-sensitive files.

What does not count:

- A chat message that was never committed to the repository.
- A vague instruction like "run the tests" without a command, when the project
  has no obvious standard command.
- Generic advice that does not mention this repository's tools or constraints.

## 2. Feedback Loops / 20

Evaluate whether validation mechanisms catch bad agent changes.

```text
Test command exists: 4
Lint command exists: 4
Typecheck command exists: 3
CI workflow exists: 5
Pre-commit or local validation script exists: 2
Validation instructions are documented: 2
```

What counts:

- Tests with a durable command in docs, package scripts, Makefile, CI, or
  equivalent.
- Linting and typechecking wired through the repository's normal toolchain.
- CI workflows such as GitHub Actions, GitLab CI, Buildkite, CircleCI, or
  equivalent.
- Pre-commit hooks, `make check`, `npm run validate`, or a project-specific
  local validation script.
- Documentation that tells a new agent which checks to run before finishing.

What does not count:

- Tests that exist but have no discoverable command and are not run by CI.
- A linter dependency that is installed but not wired into a command.
- CI that only deploys and does not validate code.

## 3. Durable Memory / 20

Evaluate whether the repository stores long-term project memory.

```text
docs/decisions exists: 5
docs/failures exists: 5
docs/conventions exists: 4
docs/domain exists: 3
At least one real decision or failure record exists: 3
```

What counts:

- Architecture Decision Records under `docs/decisions`.
- Failure records under `docs/failures` that describe rejected approaches,
  repeated agent mistakes, incidents, or fixes that should not be forgotten.
- Conventions that explain local coding, naming, testing, or review rules.
- Domain notes that define business language, workflows, invariants, or user
  expectations.
- At least one non-template decision or failure record with concrete context.

What does not count:

- Empty directories.
- Placeholder templates only.
- Historical knowledge that lives only in issue comments, chat, or a person's
  memory.

## 4. Structural Safety / 20

Evaluate whether the repository has safeguards against structural drift.

```text
Structure check script exists: 5
Docs drift check exists: 4
Generated file protection exists: 3
Forbidden path checks exist: 3
Architecture/dependency boundary checks exist: 3
CI runs at least one structural check: 2
```

What counts:

- A script that detects drift-prone paths, temporary files, duplicate generated
  files, or files outside approved locations.
- A docs drift check that catches broken local Markdown links or stale file
  references.
- `.gitignore`, lint rules, or scripts that protect generated files from
  accidental edits or commits.
- Forbidden path checks backed by code, lint rules, or explicit CI validation.
- Architecture boundary checks such as import restrictions, dependency rules, or
  layer enforcement.
- CI that runs at least one structural or drift check.

What does not count:

- A documented boundary that no check can catch and no reviewer checklist names.
- A drift script that exists but is broken or unrelated to the repository.
- Generated file guidance with no ignore rule, check, or review point.

## 5. Adoption Clarity / 20

Evaluate whether a new user or agent can understand and adopt the harness.

```text
README explains harness purpose: 4
Quickstart exists: 4
Before/after example exists: 4
Adoption report template exists: 3
Profiles/examples exist: 3
Known limitations are documented: 2
```

What counts:

- A README that explains what the harness is for in practical terms.
- A quickstart that tells a user or agent how to begin.
- Before/after examples, adoption reports, or realistic examples showing what
  adoption looks like.
- A report template for summarizing adoption changes, checks, assumptions, and
  remaining work.
- Profiles, examples, or templates for common stacks.
- Known limitations such as "this is not a full automatic installer" or
  "scripts provide a baseline and require agent review."

What does not count:

- Marketing copy with no adoption path.
- Examples that are unrelated to the actual workflow.
- Templates that overwrite target project conventions without explanation.

## Grade Scale

```text
90-100: A / Production-ready harness
80-89: B+ / Strong harness
70-79: B / Useful but incomplete
60-69: C / Basic harness
40-59: D / Mostly ad-hoc
0-39: F / No durable agent harness
```

## Interpreting Results

A high score does not mean the project has perfect documentation. It means the
repository has enough durable instructions, constraints, memory, and validation
loops that a new coding agent can work without depending on session-scoped
context.

A low score is not a failure. It is a map of where to add the next durable
harness artifact.
