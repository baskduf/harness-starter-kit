from __future__ import annotations

import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LOCALIZED_READMES = (
    "README.ko.md",
    "README.ja.md",
    "README.zh-CN.md",
)
PROMPT_MARKERS = (
    "Ask an agent:",
    "Read ./harness-starter-kit",
    "Requirements:",
)


def agent_prompt_blocks(readme: Path) -> list[str]:
    text = readme.read_text(encoding="utf-8")
    blocks = re.findall(r"```text\n(.*?)\n```", text, flags=re.DOTALL)
    return [
        block
        for block in blocks
        if any(marker in block for marker in PROMPT_MARKERS)
    ]


class ReadmePromptDriftTests(unittest.TestCase):
    def test_localized_readme_agent_prompts_match_english_readme(self) -> None:
        expected = agent_prompt_blocks(REPO_ROOT / "README.md")

        self.assertGreaterEqual(len(expected), 1)
        for filename in LOCALIZED_READMES:
            with self.subTest(readme=filename):
                actual = agent_prompt_blocks(REPO_ROOT / filename)
                self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
