---
framework_version: 1.0.0
---

# Agent Guidelines: AI Job Search

This workspace is structured to manage job search activities, scraper tools, CVs, cover letters, and interview preparation.

## Thin-Pointer Design (Single Source of Truth)

To prevent duplication and configuration drift across different AI agent frameworks, this workspace uses a unified thin-pointer design. The canonical specifications and candidate profile live in the files and directories below; agent-specific entry points should point to them rather than copy their rules.

1. **Personal Candidate Profile:**
   - The candidate profile, contact details, education, and target preferences are defined in [CLAUDE.md](CLAUDE.md) and the individual profile methodology files under [.claude/skills/job-application-assistant/](.claude/skills/job-application-assistant/) (specifically `01-*.md` etc.).
2. **Canonical Workflow Specifications:**
   - The step-by-step instructions and triggers for tasks (setup, scrape, rank, apply, upskill, interview) are defined in the [.claude/](.claude/) directory (specifically under `.claude/skills/` and `.claude/commands/`).
   - Do not duplicate these rules or specifications. Treat `.claude/` files as the single source of truth.
   - VS Code Copilot discovers the pointer skills under [.github/skills/](.github/skills/) and project-wide guidance in [.github/copilot-instructions.md](.github/copilot-instructions.md). Each skill points to its canonical `.claude/` workflow.
3. **Portal Search Skills:**
   - Job-portal search CLIs and their canonical skill instructions live under [.agents/skills/](.agents/skills/) (with a `SKILL.md` per portal). Copilot's native skill pointers are under `.github/skills/`; the canonical `/scrape` workflow in [.claude/skills/job-scraper/](.claude/skills/job-scraper/) orchestrates the portal CLIs.
