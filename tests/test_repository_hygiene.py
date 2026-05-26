from __future__ import annotations

import shutil
import subprocess
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class RepositoryHygieneTests(unittest.TestCase):
    def test_python_cache_files_are_not_tracked(self) -> None:
        if shutil.which("git") is None or not (REPO_ROOT / ".git").exists():
            self.skipTest("git repository is not available")

        result = subprocess.run(
            ["git", "ls-files"],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        tracked_cache_files = [
            path
            for path in result.stdout.splitlines()
            if "__pycache__/" in path.replace("\\", "/") or path.endswith(".pyc")
        ]

        self.assertEqual([], tracked_cache_files)

    def test_fastapi_check_harness_excludes_generated_profile_snippets(self) -> None:
        check_harness = (
            REPO_ROOT / "templates" / "profiles" / "fastapi" / "check_harness.py"
        )
        text = check_harness.read_text(encoding="utf-8")

        self.assertIn("--exclude", text)
        self.assertIn("docs", text)
        self.assertIn("harness", text)

    def test_effectiveness_measurement_is_wired_into_adoption_flow(self) -> None:
        adoption_report = (
            REPO_ROOT / "docs" / "templates" / "adoption-report.md"
        ).read_text(encoding="utf-8")
        agent_template = (REPO_ROOT / "templates" / "generic" / "AGENTS.md").read_text(
            encoding="utf-8"
        )
        adoption_prompt = (
            REPO_ROOT / "docs" / "prompts" / "apply-to-target-repo.md"
        ).read_text(encoding="utf-8")
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("## Effectiveness Measurement Plan", adoption_report)
        self.assertIn("Do not leave this section as TODO", adoption_report)
        self.assertIn("Baseline available", adoption_report)
        self.assertIn("Primary metric", adoption_report)
        self.assertIn("Results location", adoption_report)
        self.assertIn("effectiveness measurement plan", agent_template)
        self.assertIn("Effectiveness Measurement Plan", adoption_prompt)
        self.assertIn("They do not prove", readme)
        self.assertIn("docs/evaluation.md", readme)


if __name__ == "__main__":
    unittest.main()
