#!/bin/sh
# Notion sync reminder for Claude Code.
#
#   mark  (PostToolUse on Write/Edit)  -> project file changed: set the pending flag
#   clear (PostToolUse on Notion writes) -> Notion was updated: remove the flag
#   stop  (Stop)                        -> flag still set: ask Claude once to update Notion
#
# The flag is a plain file, so state survives between hook runs.

FLAG="$CLAUDE_PROJECT_DIR/.claude/.notion-pending"
INPUT=$(cat)

case "$1" in
  mark)
    f=$(printf '%s' "$INPUT" | jq -r '.tool_input.file_path // empty')
    case "$f" in
      "" | "$CLAUDE_PROJECT_DIR"/.claude/*) ;;              # ignore Claude's own config
      "$CLAUDE_PROJECT_DIR"/*) touch "$FLAG" ;;             # a real project file changed
    esac
    ;;
  clear)
    rm -f "$FLAG"
    ;;
  stop)
    [ -f "$FLAG" ] || exit 0
    active=$(printf '%s' "$INPUT" | jq -r '.stop_hook_active // false')
    if [ "$active" = "true" ]; then
      # Already reminded once this turn: let Claude stop, and reset for next time.
      rm -f "$FLAG"
      exit 0
    fi
    jq -n '{decision: "block", reason: "Project files changed this turn but Notion was not updated. Per CLAUDE.md, if this change is meaningful (task done, decision, problem solved, new concept), update Notion now following docs/NOTION.md. If it is trivial, stop and say briefly why Notion was skipped."}'
    ;;
esac
exit 0
