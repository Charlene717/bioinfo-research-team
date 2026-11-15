#!/usr/bin/env bash
# Checksum manifest for data/raw/ (paths relative to data/raw/).
#   tools/raw-manifest.sh add      append sha256 lines for files not yet listed (existing lines are never rewritten)
#   tools/raw-manifest.sh verify   check every listed file; report missing, changed, and unlisted files
# Exit status of verify: 0 = all good, 1 = mismatch/missing/unlisted.
set -euo pipefail
SELF="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/$(basename "${BASH_SOURCE[0]}")"
cd "$(dirname "$SELF")/.."
RAW=data/raw
MAN=MANIFEST.sha256
if command -v sha256sum >/dev/null 2>&1; then SHA=(sha256sum); else SHA=(shasum -a 256); fi
[ -d "$RAW" ] || { echo "no $RAW/ yet"; exit 0; }
cd "$RAW"

list_files() { find . -type f ! -name 'MANIFEST*' ! -name 'README*' ! -name '.gitkeep' | sed 's|^\./||' | LC_ALL=C sort; }
listed()     { [ -f "$MAN" ] && awk '{ $1=""; sub(/^ +\*?/, ""); print }' "$MAN" | LC_ALL=C sort || true; }

case "${1:-}" in
  add)
    new=$(comm -23 <(list_files) <(listed))
    if [ -z "$new" ]; then echo "manifest up to date ($(listed | wc -l | tr -d ' ') files)"; exit 0; fi
    n=0
    while IFS= read -r f; do "${SHA[@]}" -- "$f" >> "$MAN"; n=$((n+1)); done <<< "$new"
    echo "added $n file(s) to $RAW/$MAN"
    echo "next: find $RAW -type f ! -name 'MANIFEST*' ! -name 'README*' -exec chmod a-w {} +"
    ;;
  verify)
    if [ ! -f "$MAN" ]; then
      if [ -z "$(list_files)" ]; then echo "verify-raw: data/raw is empty — nothing to verify"; exit 0; fi
      echo "verify-raw: FAIL — data/raw has files but no $MAN (run: make manifest)"; exit 1
    fi
    status=0
    if ! "${SHA[@]}" -c --quiet "$MAN"; then status=1; echo "verify-raw: FAIL — checksum mismatch or missing file (see above)"; fi
    unlisted=$(comm -23 <(list_files) <(listed))
    if [ -n "$unlisted" ]; then status=1; echo "verify-raw: FAIL — files not in manifest:"; echo "$unlisted" | sed 's/^/  /'; echo "  (if they are new downloads, run: make manifest)"; fi
    [ $status -eq 0 ] && echo "verify-raw: OK ($(listed | wc -l | tr -d ' ') files match $MAN)"
    exit $status
    ;;
  *) sed -n "2,5p" "$SELF"; exit 2;;
esac
