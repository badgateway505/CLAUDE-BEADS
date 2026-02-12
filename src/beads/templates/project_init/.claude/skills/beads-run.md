# Run Active Bead

Execute the currently active bead from the ledger.

**Usage:** `/beads:run`

**Prerequisites:**
- Must run `/clear` first (HARD LOCK requirement)
- Active bead must be set in `.beads/ledger.md`

**What it does:**
1. Checks that `/clear` was run (HARD LOCK)
2. Reads `.beads/ledger.md` for active bead
3. Executes bead via simplified FSM protocol (init → work → verify)
4. Auto-queues next pending bead when verification passes

**When to use:**
- After `/clear`, to execute the next bead in the workflow
- When continuing work on a phase

**Related commands:**
- `/beads:plan` - Plan a phase into beads (before running)
- `/beads:resume` - Restore project context after break
