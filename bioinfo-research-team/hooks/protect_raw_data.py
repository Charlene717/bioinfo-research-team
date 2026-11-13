#!/usr/bin/env python3
"""PreToolUse guard that keeps data/raw/ immutable.

Reads the hook JSON from stdin (never from argv, so large Write payloads cannot
overflow the argument limit). Exit 2 = block (stderr goes to Claude as the reason);
exit 0 = allow.

Policy
- Write / Edit / MultiEdit / NotebookEdit: any path under a data/raw/ directory is
  blocked, except data/raw/MANIFEST* and data/raw/README*.
- Bash: commands are split into segments; `cd` is tracked so relative paths are
  resolved correctly (e.g. `cd data/raw && rm x`). Within data/raw/ the guard:
    * blocks deleting, truncating, re-compressing or editing in place
      (rm, rmdir, unlink, shred, truncate, gzip/gunzip/bgzip/xz/zstd/bzip2 without
      -c/-k, sed -i, perl -i, find -delete / -exec <destructive>);
    * blocks moving anything out of / within data/raw and rsync --delete;
    * allows ADDING new files: downloads (curl -o, wget -O, `> file`, tee, dd of=)
      and cp/mv/rsync/tar/unzip into data/raw are allowed only when they cannot
      overwrite an existing file (target absent, or a no-clobber flag is given);
    * blocks chmod that grants write permission;
    * blocks inline interpreter code (python -c, Rscript -e, perl -e, node -e)
      that mentions data/raw together with a write/delete call.
- If a command mentions data/raw but cannot be parsed, it is blocked (fail-closed
  for raw data, fail-open for everything else).

Limitations (documented, by design): scripts executed from files (python foo.py)
are not inspected. The real integrity guarantee is `make verify-raw`
(sha256sum -c data/raw/MANIFEST.sha256), which `make analysis` runs first.
"""
import json
import os
import re
import shlex
import sys

RAW_COMPONENT = re.compile(r"(^|/)data/raw(/|$)")
ALLOWED_NAME = re.compile(r"^(MANIFEST|README)[^/]*$")


def block(msg):
    sys.stderr.write(
        "BLOCKED by bioinfo-research-team raw-data guard: " + msg + "\n"
        "Raw data are immutable. Derive into data/processed/ instead; only "
        "data/raw/MANIFEST* and data/raw/README* may be written. New files may be "
        "added to data/raw/ only without overwriting (e.g. `cp -n`, `rsync "
        "--ignore-existing`, `tar --skip-old-files`, `unzip -n`, `gunzip -c a.gz > "
        "data/processed/a`). Ask the PI (user) to lift the guard explicitly if a "
        "raw-file change is really intended.\n"
    )
    sys.exit(2)


def norm(path, cwd):
    path = os.path.expanduser(path)
    if not os.path.isabs(path):
        path = os.path.join(cwd, path)
    return os.path.normpath(path)


def in_raw(abspath):
    """True if abspath is data/raw itself or inside it (and not an allowed meta file)."""
    if not RAW_COMPONENT.search(abspath):
        return False
    if ALLOWED_NAME.match(os.path.basename(abspath)) and RAW_COMPONENT.search(os.path.dirname(abspath)):
        return False
    return True


def is_raw_root_or_inside(abspath):
    return bool(RAW_COMPONENT.search(abspath))


# ---------------------------------------------------------------- tool checks

def check_file_tool(tool, ti, cwd):
    path = str(ti.get("file_path") or ti.get("notebook_path") or "")
    if path and in_raw(norm(path, cwd)):
        block(f"{tool} to {path}")


# ---------------------------------------------------------------- bash parsing

SEPARATORS = {";", "&&", "||", "|", "&", "\n", "|&"}
WRAPPERS = {"sudo", "env", "nohup", "time", "nice", "ionice", "command", "builtin", "exec", "xargs"}
DELETERS = {"rm", "rmdir", "unlink", "shred", "truncate", "srm"}
COMPRESSORS = {"gzip", "gunzip", "bgzip", "pigz", "unpigz", "xz", "unxz", "bzip2",
               "bunzip2", "zstd", "unzstd", "lz4", "pbzip2"}
INTERPRETERS = {"python", "python3", "Rscript", "R", "perl", "node", "ruby"}
INLINE_FLAGS = {"-c", "-e", "--eval", "-E"}
WRITE_CALLS = re.compile(
    r"""open\([^)]*['"](w|a|r\+|wb|ab|x)['"]|\.write|to_csv|to_parquet|write_h5ad|"""
    r"""os\.remove|os\.unlink|os\.rename|shutil\.(move|rmtree)|unlink\(|rmtree|Path\([^)]*\)\.(unlink|write_)|"""
    r"""file\.remove|file\.rename|unlink\(|write\.(csv|table|tsv)|writeLines|saveRDS|fwrite|write_tsv|"""
    r"""write_csv|sink\(|system\(|\bunlink\b"""
)


def tokenize(cmd):
    lex = shlex.shlex(cmd, posix=True, punctuation_chars=";&|<>")
    lex.whitespace_split = True
    lex.commenters = ""
    toks = []
    for t in lex:
        toks.append(t)
    return toks


def split_segments(tokens):
    seg, segs = [], []
    for t in tokens:
        if t in SEPARATORS or (set(t) <= set(";&|") and t):
            if seg:
                segs.append(seg)
            seg = []
        else:
            seg.append(t)
    if seg:
        segs.append(seg)
    return segs


def strip_wrappers(seg):
    i = 0
    while i < len(seg):
        t = seg[i]
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", t):
            i += 1
            continue
        if t in WRAPPERS:
            i += 1
            # skip wrapper options like `nice -n 10`, `xargs -0`
            while i < len(seg) and seg[i].startswith("-"):
                i += 1
                if i < len(seg) and seg[i - 1] in ("-n", "-u", "-I", "-P") and not seg[i].startswith("-"):
                    i += 1
            continue
        break
    return seg[i:]


def split_redirections(seg):
    """Return (args_without_redirs, [(op, target)])."""
    args, redirs = [], []
    i = 0
    while i < len(seg):
        t = seg[i]
        if t in (">", ">>", ">|", "&>", "&>>") or re.fullmatch(r"\d?>{1,2}\|?", t):
            if i + 1 < len(seg):
                redirs.append((t, seg[i + 1]))
            i += 2
            continue
        if t in ("<", "<<", "<<<"):
            i += 2
            continue
        m = re.fullmatch(r"(\d?>{1,2})(\S+)", t)
        if m and not t.startswith("-"):
            redirs.append((m.group(1), m.group(2)))
            i += 1
            continue
        args.append(t)
        i += 1
    return args, redirs


def positional(args):
    out, end_of_opts = [], False
    for a in args:
        if a == "--":
            end_of_opts = True
            continue
        if not end_of_opts and a.startswith("-") and a != "-":
            continue
        out.append(a)
    return out


def has_flag(args, shorts="", longs=()):
    for a in args:
        if a.startswith("--"):
            name = a.split("=", 1)[0]
            if name in longs:
                return True
        elif a.startswith("-") and len(a) > 1 and shorts:
            if any(c in a[1:] for c in shorts):
                return True
    return False


def option_value(args, names):
    """Values of options like -o FILE, -O FILE, --output FILE, --output=FILE, -oFILE."""
    vals = []
    for i, a in enumerate(args):
        for n in names:
            if a == n and i + 1 < len(args):
                vals.append(args[i + 1])
            elif n.startswith("--") and a.startswith(n + "="):
                vals.append(a.split("=", 1)[1])
            elif not n.startswith("--") and a.startswith(n) and len(a) > len(n) and len(n) == 2:
                vals.append(a[len(n):])
    return vals


def would_overwrite(target_abs, sources=()):
    """True if writing to target would replace an existing raw file."""
    if not in_raw(target_abs):
        return False
    if os.path.isdir(target_abs):
        return any(os.path.exists(os.path.join(target_abs, os.path.basename(s.rstrip("/")))) for s in sources)
    return os.path.exists(target_abs)


def check_segment(seg, cwd, original):
    seg = strip_wrappers(seg)
    if not seg:
        return cwd
    args, redirs = split_redirections(seg)
    if not args:
        args = [""]
    cmd = os.path.basename(args[0])
    rest = args[1:]
    pos = positional(rest)
    absp = [norm(p, cwd) for p in pos]

    # output redirections
    for op, target in redirs:
        if target.startswith("&") or target == "/dev/null":
            continue
        t = norm(target, cwd)
        if in_raw(t) and (os.path.exists(t) or ">>" in op):
            block(f"redirection {op} {target} would overwrite/append an existing raw file")

    if cmd == "cd":
        dest = pos[0] if pos else os.path.expanduser("~")
        return norm(dest, cwd)
    if cmd in ("pushd",) and pos:
        return norm(pos[0], cwd)

    raw_args = [p for p in absp if in_raw(p)]
    raw_any = [p for p in absp if is_raw_root_or_inside(p)]

    if cmd in DELETERS and raw_args:
        block(f"{cmd} on {raw_args[0]}")

    if cmd in COMPRESSORS and raw_args:
        if not has_flag(rest, "ck", ("--stdout", "--to-stdout", "--keep", "--test", "--list")) \
                and not has_flag(rest, "tl"):
            block(f"{cmd} would replace {raw_args[0]} in place (use -c > data/processed/… or -k)")

    if cmd == "sed" and raw_args and has_flag(rest, "i", ("--in-place",)):
        block(f"sed -i on {raw_args[0]}")
    if cmd == "perl" and raw_args and any(re.match(r"^-[a-zA-Z]*i", a) for a in rest):
        block(f"perl -i on {raw_args[0]}")

    if cmd == "find" and raw_any:
        if "-delete" in rest:
            block("find … -delete inside data/raw")
        for i, a in enumerate(rest):
            if a in ("-exec", "-execdir", "-ok", "-okdir") and i + 1 < len(rest):
                inner = os.path.basename(rest[i + 1])
                if inner in DELETERS | COMPRESSORS | {"mv", "sed", "perl", "chmod", "truncate", "dd"}:
                    if inner not in ("chmod",) or any("w" in x and ("+" in x or "=" in x) for x in rest[i + 2:]):
                        block(f"find -exec {inner} inside data/raw")

    if cmd == "chmod" and raw_any:
        mode = pos[0] if pos else ""
        grants_w = ("+" in mode or "=" in mode) and "w" in mode
        if re.fullmatch(r"[0-7]{3,4}", mode or ""):
            grants_w = any(int(d) & 2 for d in mode[-3:])
        if grants_w:
            block(f"chmod {mode} would make raw files writable")

    if cmd == "mv" and raw_any:
        srcs, dest = absp[:-1], (absp[-1] if absp else "")
        tdir = option_value(rest, ["-t", "--target-directory"])
        if tdir:
            srcs, dest = absp, norm(tdir[0], cwd)
        if any(is_raw_root_or_inside(s) and not (ALLOWED_NAME.match(os.path.basename(s))) for s in srcs):
            block("mv of a file that is in data/raw")
        if dest and in_raw(dest) and would_overwrite(dest, srcs) and not has_flag(rest, "n", ("--no-clobber",)):
            block(f"mv would overwrite {dest}")

    if cmd in ("cp", "install", "ln") and pos:
        tdir = option_value(rest, ["-t", "--target-directory"])
        if tdir:
            srcs, dest = absp, norm(tdir[0], cwd)
        else:
            srcs, dest = absp[:-1], absp[-1]
        noclobber = has_flag(rest, "n", ("--no-clobber", "--update")) or "--update=none" in rest
        if is_raw_root_or_inside(dest):
            if would_overwrite(dest, srcs) and not noclobber:
                block(f"{cmd} would overwrite an existing file in {dest} (use {cmd} -n)")
            if cmd == "ln" and has_flag(rest, "f", ("--force",)):
                block("ln -f into data/raw")

    if cmd == "rsync" and raw_any:
        if any(a.startswith("--delete") or a == "--remove-source-files" for a in rest):
            src_raw = any(is_raw_root_or_inside(p) for p in absp[:-1])
            if any(a.startswith("--delete") for a in rest) and absp and is_raw_root_or_inside(absp[-1]):
                block("rsync --delete into data/raw")
            if "--remove-source-files" in rest and src_raw:
                block("rsync --remove-source-files from data/raw")
        if absp and is_raw_root_or_inside(absp[-1]) and "--ignore-existing" not in rest:
            if would_overwrite(absp[-1], absp[:-1]) or os.path.isdir(absp[-1]):
                block("rsync into data/raw without --ignore-existing")

    if cmd in ("tar", "bsdtar"):
        tdir = option_value(rest, ["-C", "--directory"])
        extracting = any(re.match(r"^-?[a-zA-Z]*x", a) for a in rest[:1]) or "--extract" in rest or "-x" in rest \
            or any(a.startswith("-") and not a.startswith("--") and "x" in a for a in rest)
        dest = norm(tdir[0], cwd) if tdir else cwd
        if extracting and is_raw_root_or_inside(dest):
            if not any(a in rest for a in ("--skip-old-files", "--keep-old-files", "-k")) and \
                    not any(a.startswith("-") and not a.startswith("--") and "k" in a for a in rest):
                block("tar extraction into data/raw without --skip-old-files")
    if cmd == "unzip":
        tdir = option_value(rest, ["-d"])
        dest = norm(tdir[0], cwd) if tdir else cwd
        if is_raw_root_or_inside(dest) and "-n" not in rest and not any(a in rest for a in ("-l", "-t", "-p")):
            block("unzip into data/raw without -n")

    if cmd in ("curl", "wget", "aria2c", "dd", "tee"):
        targets = []
        if cmd == "curl":
            targets = option_value(rest, ["-o", "--output"])
        elif cmd == "wget":
            targets = option_value(rest, ["-O", "--output-document"])
        elif cmd == "aria2c":
            d = option_value(rest, ["-d", "--dir"])
            o = option_value(rest, ["-o", "--out"])
            if o:
                targets = [os.path.join(d[0] if d else ".", o[0])]
            if "--allow-overwrite=true" in rest:
                if (d and is_raw_root_or_inside(norm(d[0], cwd))) or any(is_raw_root_or_inside(norm(t, cwd)) for t in targets):
                    block("aria2c --allow-overwrite=true into data/raw")
        elif cmd == "dd":
            targets = [a[3:] for a in rest if a.startswith("of=")]
        elif cmd == "tee":
            targets = pos
            if has_flag(rest, "a", ("--append",)) and any(in_raw(norm(t, cwd)) for t in targets):
                block("tee -a into an existing raw file")
        for t in targets:
            ta = norm(t, cwd)
            if in_raw(ta) and os.path.exists(ta):
                block(f"{cmd} would overwrite existing raw file {t}")

    if cmd in INTERPRETERS or re.match(r"^python3?(\.\d+)?$", cmd):
        for i, a in enumerate(rest):
            if a in INLINE_FLAGS and i + 1 < len(rest):
                code = rest[i + 1]
                inline_cwd_raw = is_raw_root_or_inside(cwd)
                if ("data/raw" in code or inline_cwd_raw) and WRITE_CALLS.search(code):
                    block(f"inline {cmd} code that writes/deletes and references data/raw")

    return cwd


def check_bash(cmd, cwd):
    mentions_raw = "data/raw" in cmd or is_raw_root_or_inside(cwd) or re.search(r"\bcd\s+raw\b", cmd)
    if not mentions_raw:
        return
    # here-docs: drop their bodies, they are data not commands
    cmd_clean = re.sub(r"<<-?\s*'?\"?(\w+)'?\"?\n.*?\n\1\b", "", cmd, flags=re.S)
    try:
        tokens = tokenize(cmd_clean.replace("\n", " ; "))
    except ValueError:
        block("command touches data/raw but could not be parsed safely; split it into simpler commands")
    # $(...) / backticks: inspect their contents too
    for inner in re.findall(r"\$\(([^()]*)\)|`([^`]*)`", cmd_clean):
        sub = inner[0] or inner[1]
        if sub.strip():
            check_bash(sub, cwd)
    for seg in split_segments(tokens):
        cwd = check_segment(seg, cwd, cmd)


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)
    tool = data.get("tool_name", "")
    ti = data.get("tool_input", {}) or {}
    cwd = data.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    if tool in ("Write", "Edit", "MultiEdit", "NotebookEdit"):
        check_file_tool(tool, ti, cwd)
    elif tool == "Bash":
        check_bash(str(ti.get("command") or ""), cwd)
    sys.exit(0)


if __name__ == "__main__":
    main()
