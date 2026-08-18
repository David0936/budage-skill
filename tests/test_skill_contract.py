from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


class SkillContractTests(unittest.TestCase):
    def test_version_is_consistent(self):
        version = (ROOT / "VERSION").read_text().strip()
        readme = (ROOT / "README.md").read_text()
        changelog = (ROOT / "CHANGELOG.md").read_text()

        self.assertIn(f"version-v{version}", readme)
        self.assertIn(f"当前版本：`v{version}`", readme)
        self.assertIn(f"`v{version}`", changelog)

    def test_access_code_is_only_in_internal_config(self):
        config_path = ROOT / "references/internal/.deep-mode-access.md"
        config = config_path.read_text()
        match = re.search(r"access_code:\s*(\S+)", config)
        self.assertIsNotNone(match)
        access_code = match.group(1)

        for path in ROOT.rglob("*"):
            if not path.is_file() or ".git" in path.parts or path == config_path:
                continue
            try:
                content = path.read_text()
            except UnicodeDecodeError:
                continue
            self.assertNotIn(access_code, content, str(path))

    def test_required_experience_protocols_exist(self):
        skill = (ROOT / "SKILL.md").read_text()
        required = [
            "references/阿星智能体_IP定位提问题库.md",
            "references/p16-PDF设计交付.md",
            "references/p17-访谈进度与续聊.md",
        ]
        for relative_path in required:
            self.assertIn(relative_path, skill)
            self.assertTrue((ROOT / relative_path).is_file())

    def test_guided_mode_supports_progress_and_resume(self):
        skill = (ROOT / "SKILL.md").read_text()
        progress = (ROOT / "references/p17-访谈进度与续聊.md").read_text()

        self.assertIn("显示轻量进度并支持暂停、续聊和小白选项", skill)
        self.assertIn("【不答哥续聊卡 v1】", progress)
        self.assertIn("都不是，我自己说", progress)

    def test_formal_deliverables_require_pdf_preview(self):
        skill = (ROOT / "SKILL.md").read_text()
        protocol = (ROOT / "references/p16-PDF设计交付.md").read_text()

        self.assertIn("报告预览卡", skill)
        self.assertIn("确认生成", protocol)
        self.assertIn("藏红力量版", protocol)
        self.assertIn("女性温暖版", protocol)
        self.assertIn("商务专业版", protocol)


if __name__ == "__main__":
    unittest.main()
