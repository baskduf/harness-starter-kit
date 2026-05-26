# Prompt: Apply harness-starter-kit To A Target Repository

Use this prompt from inside the target repository.

```text
Read ../harness-starter-kit first. Apply the harness engineering starter kit to this
repository.

Goal:
Make this repository easier and safer for coding agents to work in by adding
durable instructions, architecture constraints, feedback loops, knowledge
storage, and drift checks.

Rules:
- Inspect this repository before editing.
- Preserve existing architecture, tools, naming, package managers, and test
  commands.
- Add the smallest useful harness rather than a large generic framework.
- Prefer updating existing docs/configs over duplicating them.
- Do not overwrite existing files without explaining why.
- Do not delete existing files unless I explicitly ask.

Expected work:
- Add or update AGENTS.md with project-specific agent instructions.
- Add docs/decisions, docs/failures, docs/conventions, and docs/domain if no
  equivalent structure exists.
- Add lightweight drift checks under scripts/.
- Add CI or pre-commit integration only when it fits the existing project.
- Add stack-specific lint/type/test recommendations based on the detected
  language.

Finish by reporting:
- files added or changed
- checks I can run locally
- assumptions you made
- remaining manual steps
```
