# Harness Doctor Example Reports

These examples show the expected report shape. Scores are illustrative; real
scores must come from inspecting durable repository evidence.

## Weak Repository Example

```text
Harness Doctor Report

Score: 48/100
Grade: D

Verdict:
This repository has a few useful project notes, but most agent guidance still
depends on human memory. It has tests and a README, but no durable failure
memory, no agent-specific instruction file, and no structural drift checks.

Breakdown:
- Agent Instructions: 6/20
- Feedback Loops: 14/20
- Durable Memory: 5/20
- Structural Safety: 4/20
- Adoption Clarity: 19/20

Evidence:
- README.md explains the project and includes a quickstart.
- package.json defines a test script and a lint script.
- .github/workflows/ci.yml runs tests.
- No AGENTS.md, CLAUDE.md, Cursor rules, or Copilot instructions were found.
- docs/failures is missing.
- No structure or docs drift check script was found.

Top Risks:
1. New agents may miss project-specific constraints because durable agent
   instructions are missing.
2. Repeated mistakes may recur because failures and rejected approaches are not
   recorded.
3. Temporary files or misplaced generated files may drift into the repository
   because no structural check exists.

Recommended Next Actions:
1. Add AGENTS.md with project overview, exact commands, boundaries, forbidden
   actions, and safety notes.
2. Add docs/failures with at least one real repeated mistake or rejected
   approach.
3. Add lightweight docs and structure drift checks, then wire them into CI or a
   local validation command.
```

## Stronger Repository Example

```text
Harness Doctor Report

Score: 82/100
Grade: B+

Verdict:
This repository has a strong practical harness. A new agent can find project
rules, validation commands, and durable context without relying on chat history.
The main remaining gap is that some architectural boundaries are documented but
not yet enforced automatically.

Breakdown:
- Agent Instructions: 18/20
- Feedback Loops: 18/20
- Durable Memory: 16/20
- Structural Safety: 14/20
- Adoption Clarity: 16/20

Evidence:
- AGENTS.md exists and includes overview, exact commands, forbidden actions, and
  security notes.
- README.md includes a quickstart and explains the harness purpose.
- CI runs tests, linting, typechecking, and docs drift checks.
- docs/decisions contains real ADRs and docs/failures contains one production
  bug write-up.
- scripts/check_structure.py exists, but architecture dependency boundaries are
  only documented in AGENTS.md.
- Known limitations are brief and could be easier for a new maintainer to find.

Top Risks:
1. Agents may violate architecture layering because dependency boundaries are
   not enforced by linting, tests, or CI.
2. Durable failure memory exists but is thin, so repeated mistakes may still be
   under-recorded.
3. Adoption examples are useful but do not show enough before/after contrast.

Recommended Next Actions:
1. Add an import or dependency boundary check for the documented architecture
   layers.
2. Record the next repeated agent error under docs/failures with the durable fix
   that prevents recurrence.
3. Add a before/after adoption example showing the repository before and after
   harness installation.
```
