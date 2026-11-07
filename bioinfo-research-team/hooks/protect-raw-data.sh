#!/usr/bin/env bash
# PreToolUse hook: keep data/raw/ immutable.
# - Write/Edit/NotebookEdit: block any file under data/raw/ except MANIFEST* and README*.
# - Bash: block rm / mv / sed -i / truncate / shred / redirection that target data/raw/.
# Exit 2 = block (stderr is shown to Claude as the reason). Fail-open (exit 0) if input cannot be parsed.
set -u
INPUT="$(cat)"
command -v python3 >/dev/null 2>&1 || exit 0

python3 - "$INPUT" <<'PY'
import json, re, sys
try:
    data = json.loads(sys.argv[1])
except Exception:
    sys.exit(0)

tool = data.get("tool_name", "")
ti = data.get("tool_input", {}) or {}
RAW = re.compile(r"(^|/)data/raw(/|$)")
ALLOWED = re.compile(r"(^|/)data/raw/(MANIFEST[^/]*|README[^/]*)$")

def block(msg):
    sys.stderr.write(
        "BLOCKED by bioinfo-research-team raw-data guard: " + msg +
        "\nRaw data are immutable. Derive into data/processed/ instead; only data/raw/MANIFEST* and data/raw/README* may be written here. "
        "Ask the PI (user) to lift the guard explicitly if a raw-file change is really intended.\n")
    sys.exit(2)

if tool in ("Write", "Edit", "MultiEdit", "NotebookEdit"):
    path = str(ti.get("file_path") or ti.get("notebook_path") or "")
    if RAW.search(path) and not ALLOWED.search(path):
        block(f"{tool} to {path}")

elif tool == "Bash":
    cmd = str(ti.get("command") or "")
    if re.search(r"(^|[\s/\"'=:])data/raw(/|\s|$|[\"'])", cmd):
        destructive = re.compile(
            r"(^|[;&|]\s*|\s)(rm|mv|shred|truncate|unlink|rmdir)\s[^;&|]*data/raw"
            r"|sed\s+(-[a-zA-Z]*i|--in-place)[^;&|]*data/raw"
            r"|(^|[^>])>{1,2}\s*(\S*/)?data/raw/(?!MANIFEST|README)\S+"
            r"|(^|[;&|]\s*|\s)tee\s[^;&|]*data/raw/(?!MANIFEST|README)\S+"
            r"|\bof=(\S*/)?data/raw/\S+"
            r"|perl\s+(?:[^;&|]*\s)?-[a-zA-Z]*i\b[^;&|]*data/raw"
        )
        m = destructive.search(cmd)
        if m:
            block(f"Bash command modifying data/raw: {m.group(0).strip()!r}")
sys.exit(0)
PY
