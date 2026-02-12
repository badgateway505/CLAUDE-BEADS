# Beads Framework Help

Show available Claude Beads commands and workflow.

**Usage:** `/beads:help`

**Available Commands:**

| Command | Purpose |
|---------|---------|
| `/beads:run` | Execute active bead |
| `/beads:plan` | Plan phase into beads |
| `/beads:research` | Research before planning |
| `/beads:resume` | Restore project context |
| `/beads:close-phase` | Close phase and freeze |
| `/beads:new-milestone` | Create new milestone |
| `/beads:help` | Show this help |

**Quick Workflow:**

```
1. /clear
2. /beads:resume (if needed)
3. /beads:plan (if phase not planned)
4. /beads:run (execute active bead)
5. Repeat 1-4 until phase done
6. /beads:close-phase
7. Go to step 3 for next phase
```

**Key Files:**
- `.beads/ledger.md` - Project state (single source of truth)
- `.beads/PROTOCOL.md` - Execution protocol
- `.beads/fsm-state.json` - Runtime state (during bead execution)

**Documentation:**
- Read `.beads/README.md` for quick reference
- Read `.beads/PROTOCOL.md` for detailed protocol
