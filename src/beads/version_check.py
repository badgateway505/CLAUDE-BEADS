"""Version check against PyPI with 24h cache."""
import json
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

PYPI_URL = "https://pypi.org/pypi/claude-beads/json"
CACHE_FILE = Path.home() / ".claude" / "cache" / "beads-version.json"
CACHE_TTL_HOURS = 24


def get_latest_version() -> str | None:
    """Fetch latest version from PyPI. Returns None on any failure."""
    try:
        with urllib.request.urlopen(PYPI_URL, timeout=3) as resp:
            data = json.loads(resp.read())
            return data["info"]["version"]
    except Exception:
        return None


def check_for_update(current_version: str) -> str | None:
    """
    Return latest version string if newer than current, else None.
    Result is cached for 24h to avoid a network call on every command.
    """
    latest = _read_cache()

    if latest is None:
        latest = get_latest_version()
        if latest:
            _write_cache(latest)

    if latest and _is_newer(latest, current_version):
        return latest
    return None


def _read_cache() -> str | None:
    try:
        data = json.loads(CACHE_FILE.read_text())
        cached_at = datetime.fromisoformat(data["cached_at"])
        age_hours = (datetime.now(timezone.utc) - cached_at).total_seconds() / 3600
        if age_hours < CACHE_TTL_HOURS:
            return data["version"]
    except Exception:
        pass
    return None


def _write_cache(version: str):
    try:
        CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
        CACHE_FILE.write_text(json.dumps({
            "version": version,
            "cached_at": datetime.now(timezone.utc).isoformat(),
        }))
    except Exception:
        pass


def _is_newer(latest: str, current: str) -> bool:
    try:
        def parse(v):
            return tuple(int(x) for x in v.split("."))
        return parse(latest) > parse(current)
    except Exception:
        return False
