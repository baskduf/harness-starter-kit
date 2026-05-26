from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CHECKER = REPO_ROOT / "scripts" / "check_effectiveness_plan.py"


COMPLETE_ADOPTION_REPORT = """# Adoption Report

## Effectiveness Measurement Plan

- Baseline available: No historical agent PR data available.
- Comparable tasks to repeat or track: next 5 route, docs, and test changes.
- Primary metric: wrong-file edits and first-pass verification success.
- Review window: next 5 comparable agent changes.
- Results location: `docs/effectiveness/harness.md`.
"""


COMPLETE_EFFECTIVENESS_REPORT = """# Harness Effectiveness Report

## Target

- Repository: sample

## Task Set

| Task ID | Scenario | Expected boundary | Common failure |
| --- | --- | --- | --- |
| T1 | Add route | routes and tests | direct database import |

## Results

| Metric | Baseline | Harnessed | Delta |
| --- | ---: | ---: | ---: |
| Wrong-file edits | 3 | 1 | -2 |

## Interpretation

- What improved: fewer wrong-file edits.
"""


class CheckEffectivenessPlanTests(unittest.TestCase):
    def run_checker(
        self, root: Path, *args: str
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(CHECKER), *args],
            cwd=root,
            capture_output=True,
            text=True,
        )

    def test_no_report_passes_unless_report_is_required(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            result = self.run_checker(root)
            required = self.run_checker(root, "--require-report")

            self.assertEqual(0, result.returncode)
            self.assertEqual(1, required.returncode)
            self.assertIn("No adoption or effectiveness report found", required.stdout)

    def test_complete_adoption_report_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs").mkdir()
            (root / "docs" / "adoption-report.md").write_text(
                COMPLETE_ADOPTION_REPORT,
                encoding="utf-8",
            )

            result = self.run_checker(root, "--require-report")

            self.assertEqual("", result.stdout)
            self.assertEqual(0, result.returncode)

    def test_missing_measurement_plan_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "adoption-report.md").write_text(
                "# Adoption Report\n\n## Checks Run\n\nPassed.\n",
                encoding="utf-8",
            )

            result = self.run_checker(root)

            self.assertIn("missing ## Effectiveness Measurement Plan", result.stdout)
            self.assertEqual(1, result.returncode)

    def test_todo_measurement_field_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "adoption-report.md").write_text(
                COMPLETE_ADOPTION_REPORT.replace(
                    "wrong-file edits and first-pass verification success.",
                    "TODO",
                ),
                encoding="utf-8",
            )

            result = self.run_checker(root)

            self.assertIn("incomplete measurement field: Primary metric", result.stdout)
            self.assertEqual(1, result.returncode)

    def test_templates_are_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            template_dir = root / "docs" / "templates"
            template_dir.mkdir(parents=True)
            (template_dir / "adoption-report.md").write_text(
                "# Adoption Report\n\n## Effectiveness Measurement Plan\n\n"
                "- Baseline available: TODO\n",
                encoding="utf-8",
            )

            result = self.run_checker(root)

            self.assertEqual("", result.stdout)
            self.assertEqual(0, result.returncode)

    def test_complete_effectiveness_report_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "node-effectiveness-report.md").write_text(
                COMPLETE_EFFECTIVENESS_REPORT,
                encoding="utf-8",
            )

            result = self.run_checker(root, "--require-report")

            self.assertEqual("", result.stdout)
            self.assertEqual(0, result.returncode)

    def test_effectiveness_report_with_todo_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "node-effectiveness-report.md").write_text(
                COMPLETE_EFFECTIVENESS_REPORT + "\n- Follow-up: TODO\n",
                encoding="utf-8",
            )

            result = self.run_checker(root)

            self.assertIn("effectiveness report still contains TODO", result.stdout)
            self.assertEqual(1, result.returncode)


if __name__ == "__main__":
    unittest.main()
