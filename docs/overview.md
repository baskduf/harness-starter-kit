# Harness Engineering Overview

Harness engineering is the practice of designing a repository environment so
coding agents can do reliable work inside durable rules.

It is different from prompt engineering. Prompts improve one interaction.
Harnesses improve the project environment.

## The Shift

Software agents can read files, edit code, run tests, and open pull requests.
That autonomy creates a new problem: agents do not automatically know a team's
implicit architecture, taste, history, or rejected approaches.

A harness turns that implicit context into repository artifacts.

## The Four Core Components

| Component | Role | Typical Files |
| --- | --- | --- |
| Instruction document | Tells the agent how to behave | `AGENTS.md`, `CLAUDE.md` |
| Architecture constraints | Blocks invalid structure | linters, type checks, import rules |
| Feedback loops | Corrects behavior quickly | tests, CI, pre-commit, examples |
| Knowledge store | Preserves decisions and context | `docs/decisions`, `docs/failures` |

This starter kit also includes garbage collection, which keeps the harness from
drifting over time.

## Operating Principle

When an agent repeats a mistake, add a durable harness improvement:

- add a specific instruction
- add a test
- add a linter or type check
- add an ADR or failure record
- add a drift check

The goal is not to make agents perfect. The goal is to make the project easier
for agents to understand and harder for them to damage.

