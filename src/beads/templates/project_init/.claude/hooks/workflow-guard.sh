#!/bin/bash
# PreToolUse hook for Edit|Write|NotebookEdit — enforce active bead requirement
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Error lock — hard block after 2 consecutive errors
source "$(dirname "$0")/error-lock.sh"

# Phase planning guard: writing phase OVERVIEW files requires .plan-ready flag
# Exempt: bead files under /beads/ (created by /beads:plan-phase)
# Exempt: files that already exist (updates to OVERVIEWs during /beads:plan-phase are legitimate)
if [[ "$FILE_PATH" == *".planning/phases/"* ]] && [[ "$FILE_PATH" != *"/beads/"* ]]; then
  if [[ -f "$FILE_PATH" ]]; then
    exit 0  # updating existing file — always allowed
  fi
  if [[ ! -f ".beads/.plan-ready" ]]; then
    echo "BLOCK: Cannot create new phase files without project validation." >&2
    echo "" >&2
    echo "⛔ STOP. Do not attempt to fix this yourself." >&2
    echo "Report this error to the user exactly as shown." >&2
    echo "Do NOT run rollback, transition, or any FSM command to work around this." >&2
    echo "" >&2
    echo "Cause: .beads/.plan-ready flag not set." >&2
    echo "The user needs to run: python3 .beads/bin/fsm.py validate-project" >&2
    increment_error_count
    exit 2
  fi
  exit 0
fi

# Skip if editing framework files (protected by protect-files.sh)
if [[ "$FILE_PATH" == *".beads/"* ]] || [[ "$FILE_PATH" == *".claude/"* ]] || [[ "$FILE_PATH" == *".planning/"* ]]; then
  exit 0
fi

# Skip if editing documentation/config files that don't require active bead
if [[ "$FILE_PATH" == *"README"* ]] || [[ "$FILE_PATH" == *"LICENSE"* ]] || [[ "$FILE_PATH" == *".gitignore"* ]] || [[ "$FILE_PATH" == *".claudeignore"* ]]; then
  exit 0
fi

# For project source files, require active bead in EXECUTE state
if [[ ! -f ".beads/fsm-state.json" ]]; then
  echo "BLOCK: No active bead. Cannot edit project files without an initialized bead." >&2
  echo "" >&2
  echo "⛔ STOP. Do not attempt to fix this yourself." >&2
  echo "Report this error to the user exactly as shown." >&2
  echo "Do NOT run rollback, transition, or any FSM command to work around this." >&2
  echo "" >&2
  echo "Cause: .beads/fsm-state.json not found — no bead is active." >&2
  echo "The user needs to run /beads:run or /beads:plan-phase to set up a bead." >&2
  increment_error_count
  exit 2
fi

# Validate fsm-state.json is in EXECUTE state (not stale from a previous bead)
FSM_STATE=$(jq -r '.current_state // empty' .beads/fsm-state.json 2>/dev/null)
if [[ "$FSM_STATE" != "execute" ]]; then
  echo "BLOCK: FSM state is '$FSM_STATE', not 'execute'. Stale or invalid state detected." >&2
  echo "" >&2
  echo "⛔ STOP. Do not attempt to fix this yourself." >&2
  echo "Report this error to the user exactly as shown." >&2
  echo "Do NOT run rollback, transition, or any FSM command to work around this." >&2
  echo "" >&2
  echo "Cause: .beads/fsm-state.json exists but is in '$FSM_STATE' state." >&2
  echo "This usually means a previous bead completed but state wasn't cleaned up." >&2
  increment_error_count
  exit 2
fi

exit 0
