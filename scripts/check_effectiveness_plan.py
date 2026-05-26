#!/usr/bin/env python3
"""Validate adoption-time harness effectiveness measurement reports."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


IGNORED_DIRECTORIES = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "node_modules",
    "dist",
    "build",
    "target",
    "out",
    ".next",
    ".turbo",
    ".gradle",
    "__pycache__",
    "harness-starter-kit",
}

TEMPLATE_PARTS = {
    "templates",
}

ADOPTION_FIELDS = (
    "Baseline available",
    "Comparable tasks to repeat or track",
    "Primary metric",
    "Review window",
    "Results location",
)

EFFECTIVENESS_SECTIONS = (
    "## Target",
    "## Task Set",
    "## Results",
    "## Interpretation",
)

TODO_RE = re.compile(r"\bTODO\b", flags=re.IGNORECASE)


@dataclass(frozen=True)
class Finding:
    path: Path
    message: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Validate that adoption and effectiveness reports contain "
            "measurement details instead of placeholders."
        )
    )
    parser.add_argument(
        "--require-report",
        action="store_true",
        help="Fail when no adoption or effectiveness report is present.",
    )
    return parser.parse_args()


def is_ignored(path: Path) -> bool:
    return any(part in IGNORED_DIRECTORIES for part in path.parts)


def is_template(path: Path) -> bool:
    return any(part in TEMPLATE_PARTS for part in path.parts)


def is_report(path: Path) -> bool:
    name = path.name.lower()
    return (
        name.endswith(".md")
        and ("adoption-report" in name or "effectiveness-report" in name)
    )


def iter_reports(root: Path) -> list[Path]:
    return [
        path
        for path in sorted(root.rglob("*.md"))
        if is_report(path.relative_to(root))
        and not is_ignored(path.relative_to(root))
        and not is_template(path.relative_to(root))
    ]


def field_value(text: str, field: str) -> str | None:
    pattern = re.compile(rf"^\s*-\s*{re.escape(field)}:\s*(.*)$", re.MULTILINE)
    match = pattern.search(text)
    if match is None:
        return None
    return match.group(1).strip()


def is_placeholder(value: str | None) -> bool:
    return value is None or not value or bool(TODO_RE.search(value))


def validate_adoption_report(path: Path, text: str) -> list[Finding]:
    findings: list[Finding] = []
    if "## Effectiveness Measurement Plan" not in text:
        findings.append(
            Finding(path, "missing ## Effectiveness Measurement Plan section")
        )
        return findings

    for field in ADOPTION_FIELDS:
        value = field_value(text, field)
        if is_placeholder(value):
            findings.append(Finding(path, f"incomplete measurement field: {field}"))

    return findings


def validate_effectiveness_report(path: Path, text: str) -> list[Finding]:
    findings: list[Finding] = []
    for section in EFFECTIVENESS_SECTIONS:
        if section not in text:
            findings.append(Finding(path, f"missing required section: {section}"))
    if TODO_RE.search(text):
        findings.append(Finding(path, "effectiveness report still contains TODO"))
    return findings


def check_effectiveness_plan(root: Path, require_report: bool) -> int:
    reports = iter_reports(root)
    findings: list[Finding] = []

    if require_report and not reports:
        print("No adoption or effectiveness report found.")
        return 1

    for path in reports:
        text = path.read_text(encoding="utf-8")
        name = path.name.lower()
        if "adoption-report" in name:
            findings.extend(validate_adoption_report(path, text))
        if "effectiveness-report" in name:
            findings.extend(validate_effectiveness_report(path, text))

    for finding in findings:
        print(f"{finding.path.relative_to(root)}: {finding.message}")

    return 1 if findings else 0


def main() -> int:
    args = parse_args()
    return check_effectiveness_plan(Path.cwd(), args.require_report)


if __name__ == "__main__":
    raise SystemExit(main())
