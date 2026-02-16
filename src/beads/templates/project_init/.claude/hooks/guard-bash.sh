#!/bin/bash
# PreToolUse hook for Bash — guard framework files from shell manipulation
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# Error lock — hard block after 2 consecutive errors
source "$(dirname "$0")/error-lock.sh"

# Authorized fsm.py commands — SAFE subset only
# These are the ONLY fsm.py subcommands Claude may run
SAFE_FSM="(init|verify|sync-ledger|status|close-phase|check-phase-closed|validate-project)"
if echo "$COMMAND" | grep -qE "^python3?\s+(\./)?\.beads/bin/fsm\.py\s+${SAFE_FSM}(\s|$)"; then
  exit 0
fi

# BLOCKED fsm.py commands — destructive or bypass vectors, user-only
DANGEROUS_FSM="(rollback|transition|reset)"
if echo "$COMMAND" | grep -qE "^python3?\s+(\./)?\.beads/bin/fsm\.py\s+${DANGEROUS_FSM}(\s|$)"; then
  FSM_SUBCMD=$(echo "$COMMAND" | grep -oE "(rollback|transition|reset)")
  echo "BLOCK: 'fsm.py $FSM_SUBCMD' is a destructive command — user-only." >&2
  echo "" >&2
  echo "⛔ STOP. Do not attempt to fix this yourself." >&2
  echo "Report this error to the user exactly as shown." >&2
  echo "" >&2
  echo "Cause: rollback/transition/reset can destroy project state." >&2
  echo "Only the user may run these commands directly in their terminal." >&2
  increment_error_count
  exit 2
fi

# Authorized router.py commands
if echo "$COMMAND" | grep -qE '^python3?\s+(\./)?\.beads/bin/router\.py\s'; then
  exit 0
fi

# Protected path patterns
PROTECTED_PATHS=(
  ".beads/ledger.json"
  ".beads/fsm-state"
  ".beads/PROTOCOL.md"
  ".beads/bin/"
  ".claude/hooks/"
  ".claude/settings.json"
)

for path in "${PROTECTED_PATHS[@]}"; do
  if echo "$COMMAND" | grep -qF "$path"; then
    echo "BLOCK: Command references protected path '$path'." >&2
    echo "" >&2
    echo "⛔ STOP. Do not attempt to fix this yourself." >&2
    echo "Report this error to the user exactly as shown." >&2
    echo "Do NOT rephrase the command, use workarounds, or pipe through other tools." >&2
    echo "" >&2
    echo "Cause: Direct manipulation of BEADS framework files is forbidden." >&2
    echo "Only fsm.py and router.py CLI commands may touch these paths." >&2
    increment_error_count
    exit 2
  fi
done

# Block commands that could modify hook/settings by other means
if echo "$COMMAND" | grep -qE '(>|>>|tee)\s+.*\.(beads|claude)/'; then
  echo "BLOCK: Redirect to .beads/ or .claude/ directory is forbidden." >&2
  echo "" >&2
  echo "⛔ STOP. Do not attempt to fix this yourself." >&2
  echo "Report this error to the user exactly as shown." >&2
  increment_error_count
  exit 2
fi

exit 0
