# Close Current Phase

Close current phase, promote issues, and freeze context.

**Usage:** `/beads:close-phase`

**What it does:**
1. Verifies all beads in current phase are complete
2. Creates XX-SUMMARY.md for frozen phase
3. Adds detailed files to `.claudeignore`
4. Marks phase as CLOSED in ledger (enables phase boundary protection)
5. Prepares for next phase

**Output:**
- XX-SUMMARY.md with phase summary
- Updated .claudeignore
- Ledger marked with phase completion

**When to use:**
- After completing all beads in a phase
- Before starting next phase
- To freeze context and prevent re-reading old code

**Related commands:**
- `/beads:plan` - Plan the next phase
- `/beads:new-milestone` - Start a new milestone
