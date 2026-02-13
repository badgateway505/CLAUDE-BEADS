#!/bin/bash
# PreToolUse hook for Edit|Write — protect framework files
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Protected patterns (substring match on absolute path)
PROTECTED=(
  ".beads/ledger.md"
  ".beads/fsm-state.json"
  ".beads/fsm-state.backup.json"
  ".beads/PROTOCOL.md"
  ".beads/bin/"
  ".claude/hooks/"
  ".claude/settings.json"
  "CLAUDE.md"
)

for pattern in "${PROTECTED[@]}"; do
  if [[ "$FILE_PATH" == *"$pattern"* ]]; then
    echo "BLOCK: Cannot modify '$pattern' directly. This file is managed by the BEADS runtime. All workflow operations must go through FSM commands via /beads:run skill." >&2
    exit 2
  fi
done

exit 0
