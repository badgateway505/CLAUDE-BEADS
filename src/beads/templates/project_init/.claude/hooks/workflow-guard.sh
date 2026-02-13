#!/bin/bash
# PreToolUse hook for Edit|Write|NotebookEdit — enforce active bead requirement
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Phase planning guard: writing phase OVERVIEW files requires .plan-ready flag
# Bead files (.planning/phases/XX/beads/*.md) are exempt — they are created by /beads:plan phase-XX
if [[ "$FILE_PATH" == *".planning/phases/"* ]] && [[ "$FILE_PATH" != *"/beads/"* ]]; then
  if [[ ! -f ".beads/.plan-ready" ]]; then
    echo "BLOCK: Cannot write to .planning/phases/ without project validation." >&2
    echo "" >&2
    echo "Run first: python3 .beads/bin/fsm.py validate-project" >&2
    echo "" >&2
    echo "This ensures PROJECT.md has real content (vision, goals) before" >&2
    echo "generating phases. No hallucinated roadmaps." >&2
    exit 2
  fi
  exit 0
fi

# Skip if editing framework files (protected by protect-files.sh)
if [[ "$FILE_PATH" == *".beads/"* ]] || [[ "$FILE_PATH" == *".claude/"* ]] || [[ "$FILE_PATH" == *".planning/"* ]]; then
  exit 0
fi

# Skip if editing documentation/config files that don't require active bead
if [[ "$FILE_PATH" == *"README"* ]] || [[ "$FILE_PATH" == *"LICENSE"* ]] || [[ "$FILE_PATH" == *".gitignore"* ]]; then
  exit 0
fi

# For project source files, require active bead in EXECUTE state
if [[ ! -f ".beads/fsm-state.json" ]]; then
  echo "BLOCK: No active bead. You must initialize a bead before editing project files." >&2
  echo "" >&2
  echo "Run: python3 .beads/bin/fsm.py init <bead-id> --active-model <model> --bead <path>" >&2
  echo "" >&2
  echo "This ensures:" >&2
  echo "  - Phase boundaries are respected (previous phase closed)" >&2
  echo "  - Model guard is enforced (correct model for task)" >&2
  echo "  - Work is tracked in ledger" >&2
  exit 2
fi

# Validate fsm-state.json is in EXECUTE state (not stale from a previous bead)
FSM_STATE=$(jq -r '.current_state // empty' .beads/fsm-state.json 2>/dev/null)
if [[ "$FSM_STATE" != "execute" ]]; then
  echo "BLOCK: FSM state is '$FSM_STATE', not 'execute'. Stale or invalid state detected." >&2
  echo "" >&2
  echo "If a bead completed, the state file should have been removed." >&2
  echo "Run: python3 .beads/bin/fsm.py status  (to inspect)" >&2
  echo "Run: python3 .beads/bin/fsm.py rollback (to reset)" >&2
  exit 2
fi

exit 0
