# Claude Beads Changelog

## 2026-02-12 - Rebranding from GSD Beads

**Major rebrand: GSD Claude Beads → Claude Beads**

The framework has been renamed to "Beads" to reflect custom innovations and signature features not present in the original GSD methodology.

### Breaking Changes

#### Directory Structure
- `.gsd/` → `.beads/` (all framework files)
- All references to `.gsd/` paths updated throughout codebase

#### Command Names
Old commands (deprecated):
- `/gsd:execute-bead`
- `/gsd:plan-phase`
- `/gsd:research-phase`
- `/gsd:resume-project`
- `/gsd:transition`

New commands (active):
- `/beads:run` - Execute active bead
- `/beads:plan` - Plan phase into beads
- `/beads:research` - Research technical approach
- `/beads:resume` - Restore project context
- `/beads:close-phase` - Close and freeze phase

#### Framework References
- "GSD Claude Beads" → "Claude Beads" throughout documentation
- Python files updated: `fsm.py`, `router.py`
- Protocol documentation updated: `PROTOCOL.md`, `README.md`
- Project files updated: `CLAUDE.md`, ledger

### New Features

#### Skill System
Created `.claude/skills/` with proper skill definitions:
- `beads-run.md` - Execute bead workflow
- `beads-plan.md` - Phase planning
- `beads-research.md` - Technical research
- `beads-resume.md` - Context restoration
- `beads-close-phase.md` - Phase completion
- `beads-help.md` - Framework help

Registered in `.claude/skills.yaml` with command aliases.

### Migration Guide

**For existing projects:**

1. Rename `.gsd/` to `.beads/`:
   ```bash
   git mv .gsd .beads
   ```

2. Update references in project files:
   ```bash
   find . -type f -exec sed -i '' 's/\.gsd\//\.beads\//g' {} +
   find . -type f -exec sed -i '' 's/GSD Beads/Beads/g' {} +
   ```

3. Update permissions in `.claude/settings.local.json`:
   ```json
   "Bash(python .beads/bin/fsm.py:*)"
   ```

4. Update workflow:
   - Use `/beads:run` instead of `/gsd:execute-bead`
   - Use `/beads:plan` instead of `/gsd:plan-phase`
   - etc.

### Why Rebrand?

The original GSD methodology provided the foundation, but this framework includes custom innovations:

1. **State Guard** - Hook-based physical enforcement of framework file integrity
2. **IRON LOCK** - Model guard enforcement via FSM
3. **Next-In-Line Protocol** - Auto-queue next pending bead
4. **XML-structured beads** - Machine-readable templates
5. **FSM automation** - 1232-line state machine
6. **Ledger-based handoff** - 70-85% token reduction
7. **Context isolation** - Phase freezing via `.claudeignore`
8. **Circuit breaker** - 3-attempt retry strategy

These signature features warrant distinct branding as "Claude Beads".

### Documentation

- Read `.beads/README.md` for quick reference
- Read `.beads/PROTOCOL.md` for execution protocol
- Run `/beads:help` for available commands
