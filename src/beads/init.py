"""Project initialization logic."""
from pathlib import Path
import shutil
from datetime import datetime


def initialize_project(project_root: Path, project_name: str, vision: str, goals: str = ""):
    """Initialize Beads framework in project directory.

    Creates:
    - .beads/ directory with config, docs, templates
    - .claude/ directory with skills
    - .planning/ directory with PROJECT.md
    - Updates CLAUDE.md (or creates it)
    - Updates .gitignore
    - Installs /beads:* commands to ~/.claude/commands/ (global)
    """

    # 1. Copy template directories
    _copy_templates(project_root)

    # 1b. Install global commands for Claude Code autocomplete
    _install_global_commands()

    # 2. Create empty ledger
    _create_ledger(project_root, project_name)

    # 3. Create PROJECT.md
    _create_project_md(project_root, project_name, vision, goals)

    # 4. Update CLAUDE.md
    _update_claude_md(project_root, project_name)

    # 5. Update .gitignore
    _update_gitignore(project_root)

    # 6. Create .github attribution
    _create_github_attribution(project_root)

    # 7. Verify mandatory files — fail loudly if anything is missing
    _verify_init(project_root)


def _install_global_commands():
    """Install /beads:* commands to ~/.claude/commands/ for Claude Code autocomplete."""
    skills_src = Path(__file__).parent / "templates" / "project_init" / ".claude" / "skills"
    commands_dst = Path.home() / ".claude" / "commands"
    commands_dst.mkdir(parents=True, exist_ok=True)

    for skill_file in skills_src.glob("*.md"):
        # beads-plan-project.md → beads:plan-project.md
        command_name = skill_file.name.replace("beads-", "beads:", 1)
        shutil.copy2(skill_file, commands_dst / command_name)

    print(f"  ✓ Installed /beads:* commands to {commands_dst}")


def _copy_templates(project_root: Path):
    """Copy template directories from package to project."""
    template_root = Path(__file__).parent / "templates" / "project_init"

    if not template_root.exists():
        raise RuntimeError(f"Package templates not found at {template_root}. Reinstall claude-beads.")

    # Copy .beads/
    beads_src = template_root / ".beads"
    beads_dst = project_root / ".beads"
    beads_dst.mkdir(exist_ok=True)

    for item in beads_src.iterdir():
        if item.is_file():
            shutil.copy2(item, beads_dst / item.name)
        elif item.is_dir() and item.name in ("templates", "bin"):
            shutil.copytree(item, beads_dst / item.name, dirs_exist_ok=True)

    # Copy .claude/
    claude_src = template_root / ".claude"
    claude_dst = project_root / ".claude"
    claude_dst.mkdir(exist_ok=True)

    shutil.copy2(claude_src / "skills.yaml", claude_dst / "skills.yaml")
    shutil.copytree(claude_src / "skills", claude_dst / "skills", dirs_exist_ok=True)

    # Copy .claude/hooks/ (State Guard) — mandatory, fail loudly if missing
    hooks_src = claude_src / "hooks"
    if not hooks_src.exists():
        raise RuntimeError(f"Hook scripts not found at {hooks_src}. Package may be corrupted — reinstall claude-beads.")
    hooks_dst = claude_dst / "hooks"
    shutil.copytree(hooks_src, hooks_dst, dirs_exist_ok=True)
    for hook in hooks_dst.glob("*.sh"):
        hook.chmod(0o755)

    # Copy .claude/settings.json (hook registration) — mandatory, fail loudly if missing
    settings_src = claude_src / "settings.json"
    if not settings_src.exists():
        raise RuntimeError(f"settings.json not found at {settings_src}. Package may be corrupted — reinstall claude-beads.")
    settings_dst = claude_dst / "settings.json"
    if not settings_dst.exists():
        shutil.copy2(settings_src, settings_dst)
    else:
        print("⚠️  .claude/settings.json already exists — hook config not merged automatically")
        print("    Manually ensure hooks are registered or delete settings.json and re-run beads init")

    # Create .planning/ directory
    planning_dst = project_root / ".planning"
    planning_dst.mkdir(exist_ok=True)


# Mandatory files that MUST exist after beads init
_MANDATORY_FILES = [
    ".beads/bin/fsm.py",
    ".beads/bin/router.py",
    ".beads/PROTOCOL.md",
    ".beads/ledger.json",
    ".beads/config.yaml",
    ".claude/hooks/protect-files.sh",
    ".claude/hooks/guard-bash.sh",
    ".claude/hooks/workflow-guard.sh",
    ".claude/settings.json",
    ".claude/skills.yaml",
    "CLAUDE.md",
]


def _verify_init(project_root: Path):
    """Verify all mandatory files were created. Fail loudly if any are missing."""
    missing = [f for f in _MANDATORY_FILES if not (project_root / f).exists()]
    if missing:
        raise RuntimeError(
            "beads init incomplete — the following mandatory files are missing:\n"
            + "\n".join(f"  ✗ {f}" for f in missing)
            + "\n\nThis may indicate a corrupted package. Try: pipx reinstall claude-beads"
        )


def _create_ledger(project_root: Path, project_name: str):
    """Create empty ledger.json. Skips if already exists (e.g. from /beads:onboard)."""
    ledger_path = project_root / ".beads" / "ledger.json"
    if ledger_path.exists():
        print("  ⏭️  ledger.json already exists — skipping (preserving onboard data)")
        return

    import json
    data = {
        "_warning": "NEVER MANUALLY EDIT — managed by fsm.py only",
        "project": {
            "name": project_name,
            "vision": "",
            "global_context": {}
        },
        "roadmap": [],
        "beads": {},
        "active_bead": None,
        "session_notes": [
            f"{_today()}: Claude Beads initialized"
        ]
    }
    ledger_path.write_text(json.dumps(data, indent=2))


def _create_project_md(project_root: Path, project_name: str, vision: str, goals: str = ""):
    """Create .planning/PROJECT.md. Skips if already exists (e.g. from /beads:onboard)."""
    project_md = project_root / ".planning" / "PROJECT.md"
    project_md.parent.mkdir(parents=True, exist_ok=True)
    if project_md.exists():
        print("  ⏭️  PROJECT.md already exists — skipping (preserving onboard data)")
        return

    content = f"""# Project: {project_name}

## Vision

{vision}

## Goals / MVP Target

{goals}

## Phases

*Run `/beads:plan-project` in Claude Code to generate your phase roadmap.*

---

*Created: {_today()}*
*Methodology: Claude Beads*
*Built with [Claude Beads](https://github.com/badgateway505/CLAUDE-BEADS) - Get it free!*
"""

    project_md.write_text(content)


def _update_claude_md(project_root: Path, project_name: str):
    """Update or create CLAUDE.md with Beads section."""
    claude_md = project_root / "CLAUDE.md"

    beads_section = """
## 🧠 Beads Workflow (Beads v)

**When executing beads, read `.beads/PROTOCOL.md` for the full execution protocol.**

**Quick reference:**
1. Read `.beads/ledger.json` first for project state
2. Suggest next pending bead proactively (Next-In-Line protocol)
3. Run FSM init — validates model, phase boundaries, bead existence
4. Execute tasks atomically, verify, sync ledger
5. Use FSM commands silently (report outcomes only)

**Tip:** Run `/clear` before each bead for optimal token efficiency (not enforced).

**State sources:**
- `.beads/fsm-state.json` — Runtime state (current bead, retries)
- `.beads/ledger.json` — Historical record (outcomes, costs)
- Bead files — Templates (task specs, verification commands)

**Context isolation:**
- Read ONLY: active bead + files in `<context_files>`
- Use `XX-SUMMARY.md` for frozen phases
- Never read `.claudeignore` files

      IMPORTANT: this context may or may not be relevant to your tasks. You should not respond to this context unless it is highly relevant to your task.
"""

    if claude_md.exists():
        # Append to existing CLAUDE.md
        content = claude_md.read_text()
        if "Beads Workflow" not in content:
            content += beads_section
            claude_md.write_text(content)
    else:
        # Create new CLAUDE.md
        content = f"""# Claude Context: {project_name}

## Project Summary

[TODO: Describe your project]

{beads_section}
"""
        claude_md.write_text(content)


def _update_gitignore(project_root: Path):
    """Add Beads entries to .gitignore."""
    gitignore = project_root / ".gitignore"

    beads_entries = [
        "",
        "# Beads framework runtime state",
        ".beads/fsm-state.json",
        ".beads/fsm-state.backup.json",
        ".beads/.plan-ready",
        ".beads/temp.md",
        "",
    ]

    if gitignore.exists():
        content = gitignore.read_text()
        if ".beads/fsm-state.json" not in content:
            content += "\n".join(beads_entries)
            gitignore.write_text(content)
    else:
        gitignore.write_text("\n".join(beads_entries))


def _create_github_attribution(project_root: Path):
    """Create .github directory with Beads attribution."""
    github_dir = project_root / ".github"
    github_dir.mkdir(exist_ok=True)

    # Create BEADS.md file that shows in GitHub insights
    beads_md = github_dir / "BEADS.md"
    content = """# Built with Claude Beads

This project uses [Claude Beads](https://github.com/badgateway505/CLAUDE-BEADS), an atomic task execution framework for AI-assisted development with Claude.

## What is Claude Beads?

Claude Beads helps you build complex software projects with AI assistance by:
- Breaking work into atomic, verifiable tasks (30min-2hr "beads")
- Maintaining a single source of truth (ledger) for context handoff
- Enforcing verification at three tiers (automated, manual checklist, exploratory)
- Preventing context pollution with phase isolation
- Routing tasks to optimal models (Opus/Sonnet/Haiku)

## Get Claude Beads

**Free and open source**: https://github.com/badgateway505/CLAUDE-BEADS

```bash
pipx install claude-beads
cd your-project/
beads init
```

Then use `/beads:plan`, `/beads:run`, and other commands in Claude Code.

---

*If you found Claude Beads helpful, consider starring the repo!*
"""
    beads_md.write_text(content)

    # Create BEADS-BADGE.md with optional badge snippet for user's README
    badge_md = github_dir / "BEADS-BADGE.md"
    badge_content = """# Optional: Add Beads Badge to Your README

You can add this badge to your project's README.md to show it was built with Claude Beads:

## Markdown Badge

```markdown
[![Built with Claude Beads](https://img.shields.io/badge/Built_with-Claude_Beads-blue?logo=anthropic)](https://github.com/badgateway505/CLAUDE-BEADS)
```

## Alternative Text Link

```markdown
*Built with [Claude Beads](https://github.com/badgateway505/CLAUDE-BEADS) - Atomic task execution for AI projects*
```

## HTML Badge (if you prefer)

```html
<a href="https://github.com/badgateway505/CLAUDE-BEADS">
  <img src="https://img.shields.io/badge/Built_with-Claude_Beads-blue?logo=anthropic" alt="Built with Claude Beads">
</a>
```

---

*This is completely optional - only add if you want to share Beads with others!*
"""
    badge_md.write_text(badge_content)


def _today() -> str:
    """Get today's date in YYYY-MM-DD format."""
    return datetime.now().strftime("%Y-%m-%d")
