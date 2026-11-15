#!/usr/bin/env bash
# Scaffold a bioinfo-research-team project.
# Usage: scaffold.sh <project-name> [parent-dir]   (default parent: current directory)
set -euo pipefail
NAME="${1:?usage: scaffold.sh <project-name> [parent-dir]}"
PARENT="${2:-.}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE="$HERE/../assets/project-template"
DEST="$PARENT/$NAME"
DATE="$(date -u +%Y-%m-%d)"

if [[ ! "$NAME" =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]]; then
  echo "error: project name must be alphanumeric with . _ - only" >&2; exit 1
fi
if [ -e "$DEST" ] && [ -n "$(ls -A "$DEST" 2>/dev/null)" ]; then
  echo "error: $DEST exists and is not empty — refusing to overwrite" >&2; exit 1
fi

mkdir -p "$DEST"
cp -R "$TEMPLATE"/. "$DEST"/
# substitute placeholders in text files only
grep -rl --exclude-dir=.git -e '{{PROJECT_NAME}}' -e '{{DATE}}' "$DEST" | while read -r f; do
  sed -i.bak -e "s/{{PROJECT_NAME}}/$NAME/g" -e "s/{{DATE}}/$DATE/g" "$f" && rm -f "$f.bak"
done
# files placed in data/raw are made read-only by data-engineer after download (directory stays writable)

if command -v git >/dev/null 2>&1 && [ ! -d "$DEST/.git" ]; then
  ( cd "$DEST" && git init -q && git add -A && git commit -qm "Scaffold research project $NAME" ) || true
fi

echo "Created $DEST"
echo "Next: cd $DEST && claude   # then /lit-review <topic> or /paper-pipeline <question>"
