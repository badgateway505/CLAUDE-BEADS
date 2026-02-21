# Beads: Context and State Rules

Applies to all sessions in this project. Rules for FSM state, context isolation, and error handling.

## State Sources

- `.beads/fsm-state.json` — Runtime state (current bead, retries). Written by FSM only.
- `.beads/ledger.json` — Historical record (outcomes, costs). Single source of truth.
- Bead files in `.planning/phases/` — Task specs, verification commands, context file lists.

## Context Isolation

- Read ONLY the active bead file + files listed in its `<context_files>` block.
- For closed phases, read `XX-SUMMARY.md` — never the raw bead files.
- Never read files listed in `.claudeignore` — they are excluded for a reason.
- Do not carry context between beads. Each bead starts fresh from the ledger.

## Architectural Decisions

- `.planning/DECISIONS.md` records WHY technical choices were made. Persists across all phases.
- Before proposing an alternative to a recorded decision, read the rationale first.
- New decisions made during planning or execution must be appended to this file.

## Error Handling

- The error-lock activates after 2 consecutive Bash failures.
- When locked: no file writes or Bash commands are permitted.
- To reset: run `fsm.py init` (starts a new bead) or achieve a passing `fsm.py verify`.
- On lock, report the error to the user and stop — do not attempt workarounds.

## FSM Commands

- Use `fsm.py` silently — report outcomes, not commands.
- `rollback`, `transition`, `reset` are user-only commands — never call them.
- Only call `fsm.py init` for the first bead of a phase. Remaining beads queue automatically.
