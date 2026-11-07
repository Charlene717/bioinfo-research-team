#!/usr/bin/env bash
# Install bioinfo-research-team WITHOUT the plugin system, by copying agents/ and skills/
# into ~/.claude (user-wide) or <project>/.claude (one project), and wiring the hooks
# into the matching settings.json (backed up first).
#
# Usage:
#   scripts/install.sh --user                 # ~/.claude/agents, ~/.claude/skills, ~/.claude/settings.json
#   scripts/install.sh --project /path/to/dir # <dir>/.claude/...
#   scripts/install.sh --uninstall --user|--project <dir>
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MODE=""; TARGET=""; UNINSTALL=0
while [ $# -gt 0 ]; do
  case "$1" in
    --user) MODE=user; TARGET="$HOME/.claude"; shift;;
    --project) MODE=project; TARGET="${2:?--project needs a directory}/.claude"; shift 2;;
    --uninstall) UNINSTALL=1; shift;;
    -h|--help) sed -n '2,10p' "$0"; exit 0;;
    *) echo "unknown option $1" >&2; exit 1;;
  esac
done
[ -n "$MODE" ] || { echo "choose --user or --project <dir>" >&2; exit 1; }
AGENTS=(literature-scout study-designer data-engineer bioinfo-analyst biostatistician figure-designer manuscript-writer peer-reviewer reproducibility-engineer submission-strategist)
SKILLS=(team new-project lit-review plan-study analyze make-figures draft-paper review-paper repro-check submit respond-reviewers paper-pipeline)
HOOKDIR="$TARGET/hooks/bioinfo-research-team"
SETTINGS="$TARGET/settings.json"

if [ "$UNINSTALL" = 1 ]; then
  for a in "${AGENTS[@]}"; do rm -f "$TARGET/agents/$a.md"; done
  for s in "${SKILLS[@]}"; do rm -rf "$TARGET/skills/$s"; done
  rm -rf "$HOOKDIR"
  echo "Removed agents, skills and hook scripts from $TARGET."
  echo "Hooks entries in $SETTINGS were left in place; remove the two entries whose command contains 'bioinfo-research-team' if you no longer want them."
  exit 0
fi

mkdir -p "$TARGET/agents" "$TARGET/skills" "$HOOKDIR"
for a in "${AGENTS[@]}"; do cp "$HERE/agents/$a.md" "$TARGET/agents/"; done
for s in "${SKILLS[@]}"; do rm -rf "$TARGET/skills/$s"; cp -R "$HERE/skills/$s" "$TARGET/skills/"; done
cp "$HERE/hooks/protect-raw-data.sh" "$HERE/hooks/session-context.sh" "$HERE/hooks/team-context.md" "$HOOKDIR/"
chmod +x "$HOOKDIR"/*.sh

# merge hooks into settings.json (python for a safe JSON merge; backup first)
if command -v python3 >/dev/null 2>&1; then
  [ -f "$SETTINGS" ] && cp "$SETTINGS" "$SETTINGS.bak.$(date +%Y%m%d%H%M%S)"
  python3 - "$SETTINGS" "$HOOKDIR" <<'PY'
import json, os, sys
settings_path, hookdir = sys.argv[1], sys.argv[2]
s = {}
if os.path.exists(settings_path):
    with open(settings_path) as f:
        s = json.load(f)
hooks = s.setdefault("hooks", {})
def entry(matcher, script):
    return {"matcher": matcher, "hooks": [{"type": "command", "command": f'"{hookdir}/{script}"', "timeout": 10}]}
def add(event, matcher, script):
    lst = hooks.setdefault(event, [])
    if not any("bioinfo-research-team" in json.dumps(e) and (e.get("matcher","") == matcher) for e in lst):
        lst.append(entry(matcher, script))
add("PreToolUse", "Write|Edit|MultiEdit|NotebookEdit", "protect-raw-data.sh")
add("PreToolUse", "Bash", "protect-raw-data.sh")
add("SessionStart", "", "session-context.sh")
with open(settings_path, "w") as f:
    json.dump(s, f, indent=2, ensure_ascii=False); f.write("\n")
print(f"hooks merged into {settings_path}")
PY
else
  echo "python3 not found: hooks not merged. Add the entries from $HERE/hooks/hooks.json to $SETTINGS manually (replace \${CLAUDE_PLUGIN_ROOT}/hooks with $HOOKDIR)."
fi

echo "Installed ${#AGENTS[@]} agents and ${#SKILLS[@]} skills into $TARGET. Restart Claude Code; type /team to begin."
