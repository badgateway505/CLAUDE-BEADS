#!/bin/bash
# PreToolUse hook for Edit|Write — protect framework files
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Error lock — hard block after 2 consecutive errors
source "$(dirname "$0")/error-lock.sh"

# Protected patterns (substring match on absolute path)
PROTECTED=(
  ".beads/ledger.json"
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
    echo "BLOCK: Cannot modify '$pattern' — managed by BEADS runtime." >&2
    echo "" >&2
    echo "⛔ STOP. Do not attempt to fix this yourself." >&2
    echo "Report this error to the user exactly as shown." >&2
    echo "Do NOT try alternative paths, tools, or workarounds to edit this file." >&2
    increment_error_count
    exit 2
  fi
done

exit 0
