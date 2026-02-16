#!/bin/bash
# Shared error-lock check — sourced by all PreToolUse hooks
# Hard-locks Claude after 2 consecutive errors (hook blocks + command failures)
#
# Usage: source this at the TOP of every PreToolUse hook
#   source "$(dirname "$0")/error-lock.sh"
#
# To increment on block: call increment_error_count before exit 2
#   increment_error_count
#   exit 2

COUNT_FILE=".beads/.error-count"

check_error_lock() {
  local count
  count=$(cat "$COUNT_FILE" 2>/dev/null || echo "0")
  if [[ "$count" -ge 2 ]]; then
    echo "🔒 SESSION LOCKED — 2 consecutive errors detected." >&2
    echo "" >&2
    echo "⛔ STOP. Do not attempt ANY more tool calls." >&2
    echo "Report this lock to the user exactly as shown." >&2
    echo "" >&2
    echo "The user must intervene. Recovery options:" >&2
    echo "  rm .beads/.error-count    (unlock and retry)" >&2
    echo "  python3 .beads/bin/fsm.py status  (inspect state)" >&2
    exit 2
  fi
}

increment_error_count() {
  local current
  current=$(cat "$COUNT_FILE" 2>/dev/null || echo "0")
  echo $((current + 1)) > "$COUNT_FILE"
}

# Auto-check on source
check_error_lock
