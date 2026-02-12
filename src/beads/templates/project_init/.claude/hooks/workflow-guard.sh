#!/bin/bash
# PreToolUse hook for Edit|Write — enforce active bead requirement
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Skip if editing framework files (protected by protect-files.sh)
if [[ "$FILE_PATH" == *".beads/"* ]] || [[ "$FILE_PATH" == *".claude/"* ]] || [[ "$FILE_PATH" == *".planning/"* ]]; then
  exit 0
fi

# Skip if editing documentation/config files that don't require active bead
if [[ "$FILE_PATH" == *"README"* ]] || [[ "$FILE_PATH" == *"LICENSE"* ]] || [[ "$FILE_PATH" == *".gitignore"* ]] || [[ "$FILE_PATH" == *"CLAUDE.md"* ]]; then
  exit 0
fi

# For project source files, require active bead
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

exit 0
