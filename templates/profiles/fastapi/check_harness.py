#!/usr/bin/env python3
"""Run local harness checks for a FastAPI project."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def repo_root() -> Path:
    current = Path(__file__).resolve()
    if current.parent.name == "scripts":
        return current.parents[1]

    cwd = Path.cwd()
    if (cwd / "scripts" / "check_docs_drift.py").exists():
        return cwd

    for candidate in (current.parent, *current.parents):
        if any((candidate / marker).exists() for marker in ("pyproject.toml", "README.md")):
            return candidate
    return cwd


ROOT = repo_root()
WINDOWS_VENV_PYTHON = ROOT / ".venv" / "Scripts" / "python.exe"
POSIX_VENV_PYTHON = ROOT / ".venv" / "bin" / "python"


def project_python() -> str:
    if WINDOWS_VENV_PYTHON.exists():
        return str(WINDOWS_VENV_PYTHON)
    if POSIX_VENV_PYTHON.exists():
        return str(POSIX_VENV_PYTHON)
    return sys.executable


def run(command: list[str]) -> None:
    subprocess.run(command, cwd=ROOT, check=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run FastAPI harness checks.")
    parser.add_argument(
        "--tests",
        default="tests",
        help="Test directory for pytest discovery.",
    )
    parser.add_argument(
        "--skip-mypy",
        action="store_true",
        help="Skip mypy type check (useful before mypy is fully configured).",
    )
    parser.add_argument(
        "--mypy-target",
        default=".",
        help="Path passed to mypy when type checking is enabled.",
    )
    parser.add_argument(
        "--mypy-exclude",
        default=r"(^|[\\/])(docs[\\/]harness|\.venv|venv)([\\/]|$)",
        help="Regex of generated or local paths excluded from mypy.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    python = project_python()
    run([python, "-m", "pytest", args.tests, "-v"])
    if not args.skip_mypy:
        run([python, "-m", "mypy", "--exclude", args.mypy_exclude, args.mypy_target])
    run([python, "scripts/check_docs_drift.py"])
    run([python, "scripts/check_structure.py"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
