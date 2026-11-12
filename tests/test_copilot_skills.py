import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


class CopilotSkillPointerTests(unittest.TestCase):
    def assert_skill_frontmatter(self, skill_file, skill_name):
        content = skill_file.read_text(encoding="utf-8")
        self.assertTrue(content.startswith("---\n"), f"Missing frontmatter in {skill_file}")
        frontmatter = content.split("---", 2)[1]
        self.assertIn(f"name: {skill_name}\n", frontmatter)
        self.assertRegex(frontmatter, r"(?m)^description: .+\S$")
        for line in frontmatter.splitlines():
            if line.startswith("argument-hint:"):
                self.assertRegex(line, r"argument-hint: [\"'].*[\"']$")

    def test_every_canonical_command_has_a_copilot_skill_pointer(self):
        commands = REPO_ROOT / ".claude" / "commands"
        skills = REPO_ROOT / ".github" / "skills"

        for command in sorted(commands.glob("*.md")):
            with self.subTest(command=command.stem):
                skill_file = skills / command.stem / "SKILL.md"
                self.assertTrue(skill_file.is_file(), f"Missing {skill_file.relative_to(REPO_ROOT)}")
                self.assert_skill_frontmatter(skill_file, command.stem)
                self.assertTrue((REPO_ROOT / ".claude" / "commands" / command.name).is_file())
                self.assertIn(
                    f"../../../.claude/commands/{command.name}",
                    skill_file.read_text(encoding="utf-8"),
                )

    def test_application_and_portal_skills_have_copilot_pointers(self):
        pointers = {
            "job-application-assistant": ".claude/skills/job-application-assistant/SKILL.md",
            "job-scraper": ".claude/skills/job-scraper/SKILL.md",
            "upskill": ".claude/skills/upskill/SKILL.md",
            **{
                portal.name: f".agents/skills/{portal.name}/SKILL.md"
                for portal in sorted((REPO_ROOT / ".agents" / "skills").iterdir())
                if (portal / "SKILL.md").is_file()
            },
        }

        for skill_name, target in pointers.items():
            with self.subTest(skill=skill_name):
                skill_file = REPO_ROOT / ".github" / "skills" / skill_name / "SKILL.md"
                self.assertTrue(skill_file.is_file(), f"Missing {skill_file.relative_to(REPO_ROOT)}")
                self.assert_skill_frontmatter(skill_file, skill_name)
                self.assertTrue((REPO_ROOT / target).is_file())
                self.assertIn(
                    f"../../../{target}",
                    skill_file.read_text(encoding="utf-8"),
                )


if __name__ == "__main__":
    unittest.main()