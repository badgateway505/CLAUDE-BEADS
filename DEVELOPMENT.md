# Development Guide

## Building the Package

### Prerequisites
- Python 3.11+
- `uv` or `pip` package manager

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/badgateway505/CLAUDE-BEADS.git
cd claude-beads
```

2. Install in development mode:
```bash
pip install -e .
```

Or with uv:
```bash
uv pip install -e .
```

3. Test the CLI:
```bash
beads --version
beads help
```

### Testing Initialization

To test the `beads init` command:

1. Create a test project directory:
```bash
mkdir /tmp/test-project
cd /tmp/test-project
git init
```

2. Run initialization:
```bash
beads init
```

3. Verify created files:
```bash
ls -la .beads/
ls -la .claude/
ls -la .planning/
cat CLAUDE.md
```

## Package Structure

```
CLAUDE-BEADS/
├── src/beads/              # Main package source
│   ├── __init__.py         # Package exports
│   ├── fsm.py              # Finite state machine (also in templates)
│   ├── cli/                # CLI commands
│   │   ├── main.py         # click commands: init, status, help
│   │   └── __init__.py
│   ├── init.py             # Project initialization logic
│   ├── status.py           # Status display logic
│   └── templates/          # Templates copied to user projects
│       └── project_init/   # Files for `beads init`
│           ├── .beads/     # Framework configuration
│           │   ├── bin/    # FSM and router scripts
│           │   ├── templates/  # Bead templates
│           │   └── *.md    # Documentation
│           └── .claude/    # Claude Code skills
│               └── skills/ # Skill definitions
├── pyproject.toml          # Package metadata and dependencies
├── README.md               # User documentation
├── LICENSE                 # MIT license
└── DEVELOPMENT.md          # This file
```

## Building Distribution

To build the package for distribution:

```bash
pip install build
python -m build
```

This creates:
- `dist/claude_beads-1.0.0-py3-none-any.whl` (wheel)
- `dist/claude-beads-1.0.0.tar.gz` (source distribution)

## Publishing to PyPI

```bash
pip install twine
twine upload dist/*
```

## Code Quality

### Linting with Ruff
```bash
pip install ruff
ruff check src/
ruff format src/
```

### Type Checking with mypy
```bash
pip install mypy
mypy src/beads/
```

## Versioning

Update version in `pyproject.toml` and `src/beads/__init__.py` before releasing.

## Common Issues

### Templates not included in package
- Ensure `[tool.hatch.build.targets.wheel.shared-data]` is correctly configured in `pyproject.toml`
- Verify templates exist in `src/beads/templates/project_init/`

### CLI command not found after install
- Reinstall with `pip install -e .`
- Check `[project.scripts]` in `pyproject.toml`

### Import errors in development
- Ensure you're in the package root directory
- Check Python path with `python -c "import sys; print(sys.path)"`
