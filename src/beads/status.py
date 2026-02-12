"""Project status display."""
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

console = Console()


def show_status(project_root: Path):
    """Show project status, active bead, next actions."""
    ledger_path = project_root / ".beads" / "ledger.md"

    if not ledger_path.exists():
        console.print("[red]❌ No ledger found[/red]")
        return

    content = ledger_path.read_text()

    # Display project info
    project_name = _extract_project_name(content)
    console.print(Panel.fit(
        f"[bold blue]Claude Beads Project Status[/bold blue]\n{project_name}",
        subtitle=str(project_root.name)
    ))

    # Show active bead
    active_section = _extract_section(content, "## Active Bead")
    console.print("\n[bold]Active Bead:[/bold]")
    console.print(active_section if active_section else "  None")

    # Show roadmap
    console.print("\n[bold]Roadmap:[/bold]")
    roadmap_section = _extract_section(content, "## Roadmap Overview")
    if roadmap_section:
        # Just show first few lines (the table)
        roadmap_lines = roadmap_section.split("\n")[:6]
        console.print("\n".join(roadmap_lines))

    # Next actions
    console.print("\n[bold]Next Actions:[/bold]")
    if active_section and "PENDING" in active_section:
        console.print("  • In Claude: [cyan]/clear[/cyan] then [cyan]/beads:run[/cyan]")
    elif active_section and "None" in active_section:
        console.print("  • In Claude: [cyan]/beads:plan <phase-name>[/cyan]")
    else:
        console.print("  • Check [cyan].beads/ledger.md[/cyan] for details")


def _extract_project_name(content: str) -> str:
    """Extract project name from ledger."""
    first_line = content.split("\n")[0]
    if first_line.startswith("# Ledger:"):
        return first_line.replace("# Ledger:", "").strip()
    return "Unknown Project"


def _extract_section(content: str, heading: str) -> str:
    """Extract content between heading and next ##."""
    lines = content.split("\n")
    in_section = False
    section_lines = []

    for line in lines:
        if line.startswith(heading):
            in_section = True
            continue
        if in_section:
            if line.startswith("##") or line.startswith("---"):
                break
            section_lines.append(line)

    return "\n".join(section_lines).strip()
