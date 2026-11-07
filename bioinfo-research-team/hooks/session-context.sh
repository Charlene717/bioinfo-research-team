#!/usr/bin/env bash
# SessionStart hook: when the working directory is a bioinfo-research-team project
# (has PROJECT.md and CLAUDE.md), print a short team briefing as context. Silent elsewhere.
set -u
INPUT="$(cat 2>/dev/null || true)"
CWD="$(printf '%s' "$INPUT" | python3 -c 'import json,sys
try:
    print(json.load(sys.stdin).get("cwd",""))
except Exception:
    print("")' 2>/dev/null)"
[ -z "$CWD" ] && CWD="${CLAUDE_PROJECT_DIR:-$PWD}"
[ -f "$CWD/PROJECT.md" ] && [ -f "$CWD/CLAUDE.md" ] || exit 0

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cat "$HERE/team-context.md"
echo
echo "## PROJECT.md (current)"
sed -n '1,40p' "$CWD/PROJECT.md"
if [ -f "$CWD/notebook/LAB-NOTEBOOK.md" ]; then
  echo
  echo "## Last lab-notebook entries"
  grep -n '^## ' "$CWD/notebook/LAB-NOTEBOOK.md" | tail -3 | cut -d: -f2-
fi
exit 0
