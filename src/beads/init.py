"""Project initialization logic."""
from pathlib import Path
import shutil
from importlib import resources
from datetime import datetime


def initialize_project(project_root: Path, project_name: str, vision: str):
    """Initialize Beads framework in project directory.

    Creates:
    - .beads/ directory with config, docs, templates
    - .claude/ directory with skills
    - .planning/ directory with PROJECT.md
    - Updates CLAUDE.md (or creates it)
    - Updates .gitignore
    """

    # 1. Copy template directories
    _copy_templates(project_root)

    # 2. Create empty ledger
    _create_ledger(project_root, project_name)

    # 3. Create PROJECT.md
    _create_project_md(project_root, project_name, vision)

    # 4. Update CLAUDE.md
    _update_claude_md(project_root, project_name)

    # 5. Update .gitignore
    _update_gitignore(project_root)

    # 6. Create .github attribution
    _create_github_attribution(project_root)


def _copy_templates(project_root: Path):
    """Copy template directories from package to project."""
    # Get package template directory
    try:
        template_root = resources.files("beads") / "templates" / "project_init"
    except AttributeError:
        # Fallback for Python < 3.9
        import importlib_resources
        template_root = importlib_resources.files("beads") / "templates" / "project_init"

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

    # Copy .claude/hooks/ (State Guard)
    hooks_src = claude_src / "hooks"
    hooks_dst = claude_dst / "hooks"
    if hooks_src.exists():
        shutil.copytree(hooks_src, hooks_dst, dirs_exist_ok=True)
        # Make hook scripts executable
        for hook in hooks_dst.glob("*.sh"):
            hook.chmod(0o755)

    # Copy .claude/settings.json (hook registration)
    settings_src = claude_src / "settings.json"
    settings_dst = claude_dst / "settings.json"
    if settings_src.exists():
        if not settings_dst.exists():
            shutil.copy2(settings_src, settings_dst)
        else:
            # Settings already exists - user should manually merge hook config
            print("⚠️  .claude/settings.json already exists - hook config not merged automatically")
            print("    Copy hook registration from template if needed")

    # Create .planning/ directory (empty for now)
    planning_dst = project_root / ".planning"
    planning_dst.mkdir(exist_ok=True)


def _create_ledger(project_root: Path, project_name: str):
    """Create empty ledger.md."""
    ledger_path = project_root / ".beads" / "ledger.md"

    content = f"""# Ledger: {project_name}

<!-- ⚠️ WARNING: NEVER MANUALLY EDIT THIS FILE -->
<!-- Managed by fsm.py sync-ledger command only -->
<!-- Manual edits will break Beads workflow and cause state desync -->

## Project Vision

[TODO: Add vision from PROJECT.md]

## Global Context
- **Stack**: [TODO]
- **Constraints**: [TODO]
- **Methodology**: Claude Beads (atomic execution, model-optimized)

## Roadmap Overview

| Phase | Name | Goal | Status |
|-------|------|------|--------|
| 1 | [TODO] | [TODO] | ⏳ Pending |

**Progress**: Phase 0 of 0 (0% complete)

---

## Ledger History

[Beads will be added here after planning]

---

## Active Bead

**None** — Run `/beads:plan` in Claude to create first phase

---

## Session Notes

- Claude Beads initialized: {_today()}
- Ledger is the SOLE source of truth
- Run `/beads:help` in Claude for available commands

---

*This project was built using [Claude Beads](https://github.com/badgateway505/CLAUDE-BEADS) - An atomic task execution framework for AI-assisted development.*
"""

    ledger_path.write_text(content)


def _create_project_md(project_root: Path, project_name: str, vision: str):
    """Create .planning/PROJECT.md."""
    project_md = project_root / ".planning" / "PROJECT.md"
    project_md.parent.mkdir(parents=True, exist_ok=True)

    content = f"""# Project: {project_name}

## Vision

{vision}

## Goals

1. [TODO]
2. [TODO]
3. [TODO]

## Constraints

- **Technical**: [TODO]
- **Timeline**: [TODO]
- **Resources**: [TODO]

## Success Criteria

- [ ] [TODO]
- [ ] [TODO]
- [ ] [TODO]

## Phases

### Phase 1: [Name]
**Goal**: [TODO]

**Deliverables**:
- [TODO]

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
## 🧠 Beads Workflow (Beads v2.0)

**When executing beads, read `.beads/PROTOCOL.md` for the full execution protocol.**

**Quick reference:**
1. Read `.beads/ledger.md` first for project state
2. Suggest next pending bead proactively (Next-In-Line protocol)
3. Run FSM init — validates model, phase boundaries, bead existence
4. Execute tasks atomically, verify, sync ledger
5. Use FSM commands silently (report outcomes only)

**Tip:** Run `/clear` before each bead for optimal token efficiency (not enforced).

**State sources:**
- `.beads/fsm-state.json` — Runtime state (current bead, retries)
- `.beads/ledger.md` — Historical record (outcomes, costs)
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
