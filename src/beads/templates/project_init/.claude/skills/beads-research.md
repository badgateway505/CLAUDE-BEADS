# Research Phase

Research technical approach before planning implementation.

**Usage:** `/beads:research [phase-id]`

**Why This Matters:** Research prevents building the wrong thing. Technical unknowns discovered late — wrong API choice, missing capability, incompatible dependency — cost 10x more to fix after code is written than before.

**What it does:**
1. Explores technical options for the phase
2. Creates XX-RESEARCH.md with XML-structured findings
3. Documents patterns, alternatives, tradeoffs
4. Provides verification commands proving findings

**Output:**
- XX-RESEARCH.md with technical analysis
- Recommended approach + alternatives
- Verification commands for testing

**When to use:**
- Before planning a phase with unclear technical approach
- When evaluating multiple implementation strategies
- To avoid building the wrong thing
- **Before Phase 01:** to validate whether the core idea is even feasible — not just "which library" but "can this actually work?" Research can kill a bad idea before any code is written, saving significant time and tokens

**Related commands:**
- `/beads:plan` - Plan phase after research is complete
