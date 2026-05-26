# Adoption Workflow

Use this workflow when applying `harness-starter-kit` to another repository.

## 1. Read The Target Repository

Collect the current shape before changing anything:

- language and framework
- package manager
- test commands
- lint and format commands
- CI provider
- directory layout
- existing docs and agent instruction files

## 2. Identify Existing Harness Pieces

Many projects already have part of a harness:

- `README.md` or contribution docs
- tests
- CI
- lint configuration
- architecture docs
- decision records

Reuse these instead of duplicating them.

## 3. Add Or Update `AGENTS.md`

The first useful harness artifact is usually a short `AGENTS.md`.

It should answer:

- What is this project?
- Which commands should agents run?
- Which directories have special rules?
- What should agents avoid?
- What must be true before a change is complete?

## 4. Add A Knowledge Store

Create these directories if the target has no equivalent:

```text
docs/
├── decisions/
├── failures/
├── conventions/
└── domain/
```

Start small. Empty directories are less useful than one real decision or failure
record.

## 5. Add Constraints

Match constraints to the stack:

- Python: Ruff, mypy, import-linter, vulture, pre-commit
- TypeScript: ESLint, TypeScript strictness, dependency boundary rules,
  unused-export checks
- Any stack: CI checks, formatting checks, forbidden-file scans

Prefer existing tools when possible.

## 6. Add Feedback Loops

Make the common path fast:

- local check command
- pre-commit checks when the project already uses them
- CI workflow
- clear test names and error messages

Agents improve fastest when feedback is quick and concrete.

## 7. Add Garbage Collection

Install lightweight drift checks:

- missing files referenced by docs
- forbidden temporary filenames
- stale commands in `AGENTS.md`
- unused code checks for the chosen stack

Run them manually at first, then wire them into CI once they are stable.
