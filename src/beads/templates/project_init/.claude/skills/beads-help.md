# Beads Framework Help

Show available Claude Beads commands and workflow.

**Usage:** `/beads:help`

**Available Commands:**

| Command | Purpose |
|---------|---------|
| `/beads:plan-project` | Evaluate idea, create phase roadmap |
| `/beads:plan-phase` | Decompose phase into beads |
| `/beads:run` | Execute active bead |
| `/beads:close-phase` | Close phase (Phase 01: evaluate idea) |
| `/beads:research` | Research before planning |
| `/beads:resume` | Restore project context |
| `/beads:new-milestone` | Create new milestone |
| `/beads:help` | Show this help |

**Quick Workflow:**

```
1. /beads:plan-project        (evaluate idea, create roadmap)
2. /beads:plan-phase 01       (decompose proof-of-concept)
3. /beads:run                  (execute beads, /clear between each)
4. /beads:close-phase          (evaluate: continue, pivot, or kill?)
5. /beads:plan-phase 02+       (if validated — proceed with features)
6. Repeat 3-5 for each phase
```

**Key Files:**
- `.beads/ledger.json` — Project state (single source of truth)
- `.beads/PROTOCOL.md` — Execution protocol
- `.beads/fsm-state.json` — Runtime state (during bead execution)
- `.planning/PROJECT.md` — Project vision, core function, tech stack
- `.planning/DECISIONS.md` — Architectural decisions + Phase 01 evaluation

**Documentation:**
- Read `.beads/README.md` for quick reference
- Read `.beads/PROTOCOL.md` for detailed protocol
