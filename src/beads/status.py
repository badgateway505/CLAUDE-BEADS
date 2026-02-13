"""Project status display."""
import json
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

console = Console()


def show_status(project_root: Path):
    """Show project status, active bead, next actions."""
    ledger_path = project_root / ".beads" / "ledger.json"

    if not ledger_path.exists():
        console.print("[red]❌ No ledger found[/red]")
        return

    try:
        data = json.loads(ledger_path.read_text())
    except json.JSONDecodeError as e:
        console.print(f"[red]❌ ledger.json corrupted: {e}[/red]")
        return

    project_name = data.get("project", {}).get("name", "Unknown Project")
    console.print(Panel.fit(
        f"[bold blue]Claude Beads Project Status[/bold blue]\n{project_name}",
        subtitle=str(project_root.name)
    ))

    # Active bead
    active = data.get("active_bead")
    console.print("\n[bold]Active Bead:[/bold]")
    console.print(f"  {active}" if active else "  None")

    # Roadmap summary
    console.print("\n[bold]Roadmap:[/bold]")
    roadmap = data.get("roadmap", [])
    for phase in roadmap[:8]:
        status_icon = {"complete": "✅", "active": "🔄", "pending": "⏳"}.get(phase.get("status"), "?")
        console.print(f"  {status_icon} Phase {phase['phase']}: {phase['name']}")
    if len(roadmap) > 8:
        console.print(f"  ... and {len(roadmap) - 8} more phases")

    # Bead stats
    beads = data.get("beads", {})
    complete = sum(1 for b in beads.values() if b.get("status") == "complete")
    total = len(beads)
    console.print(f"\n[bold]Progress:[/bold] {complete}/{total} beads complete")

    # Next actions
    console.print("\n[bold]Next Actions:[/bold]")
    if active:
        console.print("  • In Claude: [cyan]/clear[/cyan] then [cyan]/beads:run[/cyan]")
    else:
        console.print("  • In Claude: [cyan]/beads:plan <phase-name>[/cyan]")
