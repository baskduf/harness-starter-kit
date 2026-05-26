# /harness doctor

Run Harness Doctor to evaluate how ready the current repository is for reliable
AI coding agent collaboration.

Harness Doctor is diagnostic only. Do not create, edit, delete, move, format, or
stage files while running this command.

## Goal

Inspect the repository and produce a Harness Score out of 100. The score should
identify weak points where AI coding agents are likely to repeat mistakes across
sessions.

Use this principle when judging the repository:

> Prompting is temporary. Context is session-scoped. A harness is project-scoped.

## Procedure

1. Treat the current working directory as the target repository root.
2. Inspect durable repository files, not chat context.
3. Read likely harness files:
   - `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/*`, `.github/copilot-instructions.md`
   - `README.md`, `CONTRIBUTING.md`, project docs, and CI configs
   - `docs/decisions`, `docs/failures`, `docs/conventions`, and `docs/domain`
   - `scripts/`, package manager config, test config, lint config, and pre-commit config
4. If available, run a baseline scan:

   ```bash
   python scripts/harness_doctor.py --target .
   ```

   Treat this script output as objective baseline evidence only. You must still
   review content quality and enforceability yourself.

5. Score the repository across the five categories below.
6. Produce the required report format.

## Scoring Rules

Be strict.

- Do not give points for intent alone.
- Do not give points for instructions that exist only in chat.
- Award points for durable files, executable checks, clear documentation, and
  validation that a future agent can find without this conversation.
- Partial credit is allowed only when the durable artifact is present but weak.
- If you cannot find evidence for an item, give 0 for that item.
- If a check exists but is not documented or wired into a normal workflow, count
  it only for the item it actually satisfies.

Use the detailed rubric in `docs/scoring/harness-score-rubric.md`.

## Categories

Total score: 100 points.

- Agent Instructions: 20
- Feedback Loops: 20
- Durable Memory: 20
- Structural Safety: 20
- Adoption Clarity: 20

## Required Report Format

```text
Harness Doctor Report

Score: <score>/100
Grade: <grade>

Verdict:
<one short paragraph explaining what the score means>

Breakdown:
- Agent Instructions: <points>/20
- Feedback Loops: <points>/20
- Durable Memory: <points>/20
- Structural Safety: <points>/20
- Adoption Clarity: <points>/20

Evidence:
- <durable evidence found in the repository>
- <durable evidence found in the repository>
- <missing or weak evidence that affected the score>

Top Risks:
1. <highest-impact risk>
2. <next risk>
3. <next risk>

Recommended Next Actions:
1. <concrete durable improvement>
2. <concrete durable improvement>
3. <concrete durable improvement>
```

## Grade Scale

```text
90-100: A / Production-ready harness
80-89: B+ / Strong harness
70-79: B / Useful but incomplete
60-69: C / Basic harness
40-59: D / Mostly ad-hoc
0-39: F / No durable agent harness
```

## Final Check

Before answering, confirm that your report names repository evidence for every
major score decision. The report should help the maintainer decide what durable
harness artifact to add next.
