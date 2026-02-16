#!/bin/bash
# PostToolUse hook for Bash — track command failures
# Increments .beads/.error-count on non-zero exit code
# PreToolUse hooks check this counter and hard-lock after 2 errors
INPUT=$(cat)

# Try multiple possible paths for exit code (Claude Code format may vary)
EXIT_CODE=$(echo "$INPUT" | jq -r '
  .tool_response.exitCode //
  .tool_response.exit_code //
  .tool_result.exitCode //
  .tool_result.exit_code //
  0
' 2>/dev/null)

# Only count actual failures (non-zero exit)
if [[ "$EXIT_CODE" != "0" ]] && [[ "$EXIT_CODE" != "null" ]] && [[ -n "$EXIT_CODE" ]]; then
  COUNT_FILE=".beads/.error-count"
  if [[ -d ".beads" ]]; then
    CURRENT=$(cat "$COUNT_FILE" 2>/dev/null || echo "0")
    echo $((CURRENT + 1)) > "$COUNT_FILE"
  fi
fi

exit 0
