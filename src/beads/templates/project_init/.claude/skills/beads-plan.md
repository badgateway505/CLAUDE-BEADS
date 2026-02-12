# Plan Phase Into Beads

Decompose a phase into atomic, model-optimized beads.

**Usage:** `/beads:plan [phase-id]`

**What it does:**
1. Verifies previous phase is CLOSED (if applicable)
2. Reads phase OVERVIEW.md and CONTEXT.md
3. Decomposes work into 3-7 atomic beads
4. Creates bead files in `.planning/phases/XX-*/beads/`
5. Updates ledger with new beads
6. Sets first bead as active

**Output:**
- Bead files (XML-structured) in beads/ directory
- Updated ledger.md with bead list
- First bead ready to execute

**When to use:**
- Starting a new phase
- Before executing beads (they must exist first)

**Related commands:**
- `/beads:research` - Research technical approach before planning
- `/beads:run` - Execute beads after planning
