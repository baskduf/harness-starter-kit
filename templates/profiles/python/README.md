# Python Harness Profile

Use these snippets when the target project is Python.

## Recommended Checks

- Ruff for linting and formatting
- mypy or pyright for type checking
- pytest for tests
- vulture for unused code detection
- pre-commit when the project already uses commit hooks

## Integration Notes

Do not replace an existing `pyproject.toml` blindly. Merge the relevant sections
from `pyproject.harness.toml` into the target project's existing config.

Prefer the target project's existing test command if it already has one.

