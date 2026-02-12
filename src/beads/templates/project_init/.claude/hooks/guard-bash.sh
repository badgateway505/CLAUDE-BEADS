#!/bin/bash
# PreToolUse hook for Bash — guard framework files from shell manipulation
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# Authorized commands: fsm.py and router.py via their proper CLI
# These are the ONLY commands allowed to touch framework state
if echo "$COMMAND" | grep -qE '^python3?\s+(\./)?\.beads/bin/fsm\.py\s'; then
  exit 0
fi
if echo "$COMMAND" | grep -qE '^python3?\s+(\./)?\.beads/bin/router\.py\s'; then
  exit 0
fi

# Protected path patterns
PROTECTED_PATHS=(
  ".beads/ledger.md"
  ".beads/fsm-state"
  ".beads/PROTOCOL.md"
  ".beads/bin/"
  ".claude/hooks/"
  ".claude/settings.json"
)

for path in "${PROTECTED_PATHS[@]}"; do
  if echo "$COMMAND" | grep -qF "$path"; then
    echo "BLOCK: Command references protected path '$path'. Direct manipulation of BEADS framework files is forbidden. Use the authorized FSM commands: python3 .beads/bin/fsm.py <command>" >&2
    exit 2
  fi
done

# Block commands that could modify hook/settings by other means
# (e.g., using variables, wildcards targeting .claude/ or .beads/bin/)
if echo "$COMMAND" | grep -qE '(>|>>|tee)\s+.*\.(beads|claude)/'; then
  echo "BLOCK: Redirect to .beads/ or .claude/ directory is forbidden." >&2
  exit 2
fi

exit 0
