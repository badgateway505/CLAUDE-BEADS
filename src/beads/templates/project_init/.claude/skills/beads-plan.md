# Plan Phase Into Beads

Decompose a phase into atomic, model-optimized beads.

**Usage:** `/beads:plan [phase-id]`

**What it does:**
1. Reads phase OVERVIEW.md and CONTEXT.md
2. Decomposes work into 3-7 atomic beads
3. Creates bead files in `.planning/phases/XX-*/beads/`
4. Updates ledger with new beads
5. Sets first bead as active

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
