"""Local dashboard server for Beads projects."""
import json
import re
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path


def _read_bead_title(bead_file: Path) -> str | None:
    """Extract title from '# Bead XX-YY: Title' line."""
    if not bead_file.exists():
        return None
    for line in bead_file.read_text().splitlines():
        match = re.match(r'^#\s+Bead\s+[\w-]+:\s+(.+)', line)
        if match:
            return match.group(1).strip()
    return None


def _build_data(project_root: Path) -> dict:
    """Build dashboard data from ledger.json + planning dirs."""
    ledger_path = project_root / ".beads" / "ledger.json"
    error_count_path = project_root / ".beads" / ".error-count"

    if not ledger_path.exists():
        return {"error": "No ledger.json found — is this a Beads project?"}

    try:
        ledger = json.loads(ledger_path.read_text())
    except json.JSONDecodeError:
        return {"error": "ledger.json is not valid JSON"}

    beads_dict = ledger.get("beads", {})
    roadmap = ledger.get("roadmap", [])
    active_bead = ledger.get("active_bead")

    # Build phase name map from .planning/phases/ directories
    phase_names: dict[str, str] = {}
    planning_dir = project_root / ".planning" / "phases"
    if planning_dir.exists():
        for phase_dir in planning_dir.iterdir():
            if phase_dir.is_dir():
                match = re.match(r'^(\d{2})-(.+)', phase_dir.name)
                if match:
                    num = match.group(1)
                    name = match.group(2).replace("-", " ").title()
                    phase_names[num] = name

    # Build roadmap phase status map
    roadmap_status: dict[str, str] = {}
    for entry in roadmap:
        roadmap_status[entry.get("phase", "")] = entry.get("status", "open")

    # Collect all phase numbers from beads + roadmap + .planning/phases/ dirs
    all_phases: set[str] = set()
    for bid, info in beads_dict.items():
        phase = info.get("phase")
        if phase:
            all_phases.add(phase)
    for entry in roadmap:
        p = entry.get("phase")
        if p:
            all_phases.add(p)
    if planning_dir.exists():
        for phase_dir in planning_dir.iterdir():
            if phase_dir.is_dir():
                m = re.match(r'^(\d{2})-', phase_dir.name)
                if m:
                    all_phases.add(m.group(1))

    # Build phase objects
    phases = []
    for phase_num in sorted(all_phases):
        phase_beads_raw = {
            bid: info for bid, info in beads_dict.items()
            if info.get("phase") == phase_num
        }

        # Find phase dir on disk for title lookups + planned-but-not-started beads
        phase_dir_path: Path | None = None
        if planning_dir.exists():
            for d in planning_dir.iterdir():
                if d.is_dir() and d.name.startswith(f"{phase_num}-"):
                    phase_dir_path = d
                    break

        # Collect bead files on disk (planned beads not yet in ledger)
        disk_beads: dict[str, Path] = {}
        if phase_dir_path:
            beads_dir = phase_dir_path / "beads"
            if beads_dir.exists():
                for bead_file in beads_dir.glob(f"{phase_num}-*.md"):
                    m = re.match(r'^(\d{2}-\d{2})', bead_file.stem)
                    if m:
                        disk_beads[m.group(1)] = bead_file

        # Merge ledger beads + disk beads
        all_bead_ids = sorted(set(list(phase_beads_raw.keys()) + list(disk_beads.keys())))

        phase_beads = []
        for bid in all_bead_ids:
            info = phase_beads_raw.get(bid, {})
            status = info.get("status", "planned")
            title = None
            if bid in disk_beads:
                title = _read_bead_title(disk_beads[bid])
            phase_beads.append({
                "id": bid,
                "title": title or bid,
                "status": status,
                "active": bid == active_bead,
            })

        total = len(phase_beads)
        complete = sum(1 for b in phase_beads if b["status"] == "complete")
        pct = round(complete / total * 100) if total else 0

        phases.append({
            "num": phase_num,
            "name": phase_names.get(phase_num, f"Phase {phase_num}"),
            "status": roadmap_status.get(phase_num, "open"),
            "beads": phase_beads,
            "total": total,
            "complete": complete,
            "pct": pct,
        })

    # Overall completion
    total_beads = len(beads_dict)
    complete_beads = sum(1 for b in beads_dict.values() if b.get("status") == "complete")
    overall_pct = round(complete_beads / total_beads * 100) if total_beads else 0

    # Error lock
    error_locked = False
    if error_count_path.exists():
        try:
            count = int(error_count_path.read_text().strip())
            error_locked = count >= 2
        except (ValueError, OSError):
            pass

    return {
        "project": ledger.get("project", {}),
        "phases": phases,
        "active_bead": active_bead,
        "total_beads": total_beads,
        "complete_beads": complete_beads,
        "overall_pct": overall_pct,
        "error_locked": error_locked,
    }


def make_handler(project_root: Path, html_content: str):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/" or self.path == "/index.html":
                self._serve_html()
            elif self.path == "/api/data":
                self._serve_data()
            else:
                self.send_response(404)
                self.end_headers()

        def _serve_html(self):
            content = html_content.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", len(content))
            self.end_headers()
            self.wfile.write(content)

        def _serve_data(self):
            data = _build_data(project_root)
            content = json.dumps(data).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", len(content))
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            self.wfile.write(content)

        def log_message(self, format, *args):
            pass  # suppress request logs

    return Handler


def start_server(port: int = 3141, open_browser: bool = True):
    """Start the dashboard server."""
    project_root = Path.cwd()

    if not (project_root / ".beads").exists():
        raise RuntimeError("Not a Beads project. Run 'beads init' first.")

    html_path = Path(__file__).parent / "dashboard.html"
    if not html_path.exists():
        raise RuntimeError(f"dashboard.html not found at {html_path}")

    html_content = html_path.read_text()
    handler = make_handler(project_root, html_content)
    server = HTTPServer(("127.0.0.1", port), handler)

    url = f"http://localhost:{port}"
    print(f"  Beads Dashboard → {url}")
    print(f"  Project: {project_root.name}")
    print(f"  Press Ctrl+C to stop\n")

    if open_browser:
        threading.Timer(0.5, lambda: webbrowser.open(url)).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Dashboard stopped.")
