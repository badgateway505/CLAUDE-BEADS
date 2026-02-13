#!/usr/bin/env python3
"""
Claude Beads CLI

Commands:
  beads init    Initialize Beads in current project
  beads status  Show project status
  beads help    Show help and workflow guide
"""

import click
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()


@click.group()
@click.version_option(version="1.1.0", prog_name="beads")
def cli():
    """Claude Beads - Atomic task execution for AI projects."""
    pass


@cli.command()
@click.option('--project-name', prompt='Project name', help='Name of your project')
@click.option('--vision', prompt='What is this project? (describe it fully — what it does, who it\'s for, why it matters)', help='Full project description')
@click.option('--goals', prompt='What does "done" look like? (end goal / MVP target)', help='Success criteria and deliverables')
@click.option('--yes', '-y', is_flag=True, default=False, help='Skip confirmation prompts (for non-interactive use)')
def init(project_name: str, vision: str, goals: str, yes: bool):
    """Initialize Beads framework in current directory."""
    from beads.init import initialize_project

    project_root = Path.cwd()

    # Check if already initialized
    if (project_root / ".beads").exists():
        console.print("[yellow]⚠️  Beads already initialized in this directory[/yellow]")
        if not yes and not click.confirm("Reinitialize?"):
            raise click.Abort()

    console.print(Panel.fit(
        "[bold blue]Claude Beads Initialization[/bold blue]",
        subtitle="Setting up framework..."
    ))

    try:
        initialize_project(project_root, project_name, vision, goals)
        console.print("\n[green]✅ Beads initialized successfully![/green]")
        console.print("\n[bold]Next steps:[/bold]")
        console.print("  1. Run [cyan]claude[/cyan] to open Claude Code in this directory")
        console.print("  2. [bold]New project[/bold]      → [cyan]/beads:plan-project[/cyan]")
        console.print("     [bold]Existing project[/bold] → [cyan]/beads:onboard[/cyan] → [cyan]/beads:plan-project[/cyan]")
        console.print("\n[dim]Documentation: .beads/README.md[/dim]")
    except Exception as e:
        console.print(f"[red]❌ Initialization failed: {e}[/red]")
        raise click.Abort()


@cli.command()
def status():
    """Show project status and next actions."""
    from beads.status import show_status

    project_root = Path.cwd()
    _verify_initialized(project_root)

    show_status(project_root)


@cli.command(name='help')
def show_help():
    """Show available commands and workflow guide."""
    help_text = """
# Claude Beads - Quick Reference

## Workflow

### New Project
1. **Initialize**: `beads init` (in terminal)
2. **Plan roadmap**: `/beads:plan-project` (in Claude Code — creates all phases)
3. **Plan phase**: `/beads:plan phase-01` (decomposes phase into beads)
4. **Execute beads**: `/clear` then `/beads:run` (in Claude Code)
5. **Close phase**: `/beads:close-phase` (in Claude Code)
6. Repeat 3-5 until project complete

### Existing Project
1. **Initialize**: `beads init` (in terminal — scaffolds framework + skills)
2. **Onboard**: `/beads:onboard` (in Claude Code — scans codebase, enriches PROJECT.md)
3. **Plan roadmap**: `/beads:plan-project` (creates phases based on analysis)
4. Continue from step 3 above

## CLI Commands (Terminal)

- `beads init` - Initialize framework in current project
- `beads status` - Show project status and active bead
- `beads help` - Show this help

## Claude Commands (in Claude Code)

After `beads init`, use these in Claude:

- `/beads:plan-project` - Generate full phase roadmap for the project
- `/beads:plan phase-XX` - Decompose a phase into atomic beads
- `/beads:run` - Execute active bead (recommended: `/clear` first)
- `/beads:research` - Research technical approach before planning
- `/beads:resume` - Restore project context after break
- `/beads:close-phase` - Close and freeze current phase
- `/beads:onboard` - Analyze existing codebase before init
- `/beads:help` - Show framework help

## Key Concepts

**Bead**: Atomic unit of work (30min-2 hours)
- Clear success criteria
- Verifiable (tests, checklist, or none for spikes)
- All-or-nothing commit

**Ledger**: Single source of truth (`.beads/ledger.json`)
- Tracks all completed work
- Shows active bead
- Enables context handoff between beads

**Phase**: Collection of related beads
- Frozen when complete (context isolation)
- Summarized in XX-SUMMARY.md

## Documentation

- `.beads/README.md` - Quick reference
- `.beads/PROTOCOL.md` - Execution protocol
- `.beads/VERIFICATION-TIERS.md` - Testing guide
- `.beads/templates/` - Bead templates

## Support

- GitHub: https://github.com/badgateway505/CLAUDE-BEADS
- Issues: https://github.com/badgateway505/CLAUDE-BEADS/issues
"""
    console.print(Markdown(help_text))


def _verify_initialized(project_root: Path):
    """Check if Beads is initialized in this project."""
    if not (project_root / ".beads").exists():
        console.print("[red]❌ Beads not initialized in this directory[/red]")
        console.print("\nRun: [cyan]beads init[/cyan]")
        raise click.Abort()


if __name__ == "__main__":
    cli()
