#!/usr/bin/env python3
"""Detect temporary or drift-prone files in a repository."""

from __future__ import annotations

import json
import sys
from pathlib import Path


DEFAULT_RULES = {
    "forbidden_patterns": [
        "**/temp_*",
        "**/*_new.*",
        "**/*_old.*",
        "**/*_backup.*",
        "**/*_fix.*",
        "**/*.bak",
    ],
    "ignored_directories": [
        ".git",
        ".hg",
        ".svn",
        ".venv",
        "venv",
        "node_modules",
        "dist",
        "build",
        ".next",
        ".turbo",
        "__pycache__",
    ],
}


def load_rules(root: Path) -> dict[str, list[str]]:
    rules_path = root / ".harness" / "structure-rules.json"
    if not rules_path.exists():
        return DEFAULT_RULES
    return json.loads(rules_path.read_text(encoding="utf-8"))


def is_ignored(path: Path, ignored_directories: set[str]) -> bool:
    return any(part in ignored_directories for part in path.parts)


def check_structure(root: Path) -> int:
    rules = load_rules(root)
    ignored_directories = set(rules.get("ignored_directories", []))
    violations: set[Path] = set()

    for pattern in rules.get("forbidden_patterns", []):
        for path in root.glob(pattern):
            if path.is_file() and not is_ignored(path.relative_to(root), ignored_directories):
                violations.add(path)

    for path in sorted(violations):
        print(f"Forbidden drift-prone file: {path.relative_to(root)}")

    return 1 if violations else 0


def main() -> int:
    return check_structure(Path.cwd())


if __name__ == "__main__":
    raise SystemExit(main())

