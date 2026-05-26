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


if __name__ == "__main__":
    unittest.main()
