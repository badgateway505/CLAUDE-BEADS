# Claude Beads - Quick Reference

## Single Source of Truth

**`.beads/ledger.md`** is the ONLY source of truth for project state.

- Shows completed beads: `[x]`
- Shows active bead: Listed in "Active Bead" section
- Shows what to do next: Clear instructions when Active Bead is "None"

## Simple Workflow

```
1. Run /clear
2. Run /beads:run
   → If bead exists: executes it
   → If no bead: shows next actions (plan, transition, etc.)
3. Repeat until phase complete
4. Run /beads:close-phase
5. Run /beads:plan for next phase
6. Go to step 1
```

## Key Rules

1. **Beads only exist in ledger AFTER bead files are created**
   - Never list beads before running `/beads:plan`
   - This prevents "bead file not found" errors

2. **Active Bead tells you what to do**
   - `Bead-XX-YY: PENDING` → Execute it immediately
   - `None - [instructions]` → Follow the instructions
   - If unclear, read the "Active Bead" section in ledger

3. **Avoid manual edits to ledger or fsm-state.json**
   - Managed by FSM in normal workflow
   - Exceptions allowed with documented rationale (e.g., emergency architecture pivots)

4. **Run /clear before /beads:run** (recommended)
   - Keeps context clean
   - Prevents token waste

## Bead Types

**Implementation beads** (default) - Production code with verification required
**Spike beads** - Time-boxed exploration (1-3 hours) that produces findings, not code

## Files Explained

| File | Purpose | When it exists |
|------|---------|----------------|
| `ledger.md` | Project history + active bead | Always |
| `fsm-state.json` | Runtime state | Only during bead execution |
| `PROTOCOL.md` | Detailed execution rules | Always |
| `templates/bead.md` | Implementation bead template | Always |
| `templates/spike-bead.md` | Spike bead template | Always |

## Common Issues

**"Bead file not found"**
→ Bead was listed in ledger but file doesn't exist yet
→ Run `/beads:plan` first to create bead files

**"No active bead"**
→ Check "Active Bead" section in ledger for next actions
→ Usually means: plan next phase or transition

**"Context not clear"**
→ Run `/clear` before `/beads:run` (recommended for token efficiency)

## Need Help?

Read `PROTOCOL.md` for detailed execution protocol.
