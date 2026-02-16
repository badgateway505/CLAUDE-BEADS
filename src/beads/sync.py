"""Sync framework files from installed package to current project."""
import filecmp
import shutil
from pathlib import Path


# Files that get synced — framework internals only, never user content
_SYNC_FILES = [
    # Hooks (enforcement layer)
    (".claude/hooks/guard-bash.sh", 0o755),
    (".claude/hooks/workflow-guard.sh", 0o755),
    (".claude/hooks/protect-files.sh", 0o755),
    (".claude/hooks/error-lock.sh", 0o755),
    (".claude/hooks/error-tracker.sh", 0o755),
    # Hook config
    (".claude/settings.json", None),
    # FSM engine
    (".beads/bin/fsm.py", 0o755),
    (".beads/bin/router.py", 0o755),
    # Protocol docs
    (".beads/PROTOCOL.md", None),
    # Skills
    (".claude/skills.yaml", None),
]

# Skills directory — sync all .md files
_SYNC_SKILL_DIR = ".claude/skills"


def sync_project(project_root: Path) -> list[str]:
    """Sync framework files from package templates to project.

    Only overwrites files that differ from the template.
    Returns list of updated file paths.
    """
    template_root = Path(__file__).parent / "templates" / "project_init"
    if not template_root.exists():
        raise RuntimeError("Package templates not found. Reinstall claude-beads.")

    updated = []

    # Sync individual files
    for rel_path, mode in _SYNC_FILES:
        src = template_root / rel_path
        dst = project_root / rel_path
        if not src.exists():
            continue
        if _needs_update(src, dst):
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            if mode:
                dst.chmod(mode)
            updated.append(rel_path)

    # Sync skills directory
    skills_src = template_root / _SYNC_SKILL_DIR
    skills_dst = project_root / _SYNC_SKILL_DIR
    if skills_src.exists():
        skills_dst.mkdir(parents=True, exist_ok=True)
        for skill_file in skills_src.glob("*.md"):
            dst = skills_dst / skill_file.name
            if _needs_update(skill_file, dst):
                shutil.copy2(skill_file, dst)
                updated.append(f"{_SYNC_SKILL_DIR}/{skill_file.name}")

    return updated


def _needs_update(src: Path, dst: Path) -> bool:
    """Check if dst needs to be updated from src."""
    if not dst.exists():
        return True
    return not filecmp.cmp(src, dst, shallow=False)
