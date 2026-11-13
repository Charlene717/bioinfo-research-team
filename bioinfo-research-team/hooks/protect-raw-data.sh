#!/usr/bin/env bash
# PreToolUse hook wrapper: the guard logic lives in protect_raw_data.py.
# The hook JSON is passed on stdin (not argv), so large Write/Edit payloads
# cannot hit the kernel's per-argument size limit.
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if ! command -v python3 >/dev/null 2>&1; then
  echo "bioinfo-research-team: python3 not found — raw-data guard inactive; rely on 'make verify-raw'." >&2
  exit 1   # non-blocking warning
fi
exec python3 "$HERE/protect_raw_data.py"
