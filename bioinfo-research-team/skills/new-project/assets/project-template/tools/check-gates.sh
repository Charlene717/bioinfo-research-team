#!/usr/bin/env bash
# Recompute quality gates G1–G5 from the report files (not from the ☑ marks an agent typed)
# and compare with the "Gates passed" row of PROJECT.md.
#   tools/check-gates.sh            human-readable table (exit 0)
#   tools/check-gates.sh --strict   exit 1 if PROJECT.md claims a gate the files do not support
#   tools/check-gates.sh --brief    one line (used by the SessionStart hook)
# Run from anywhere inside the project. Requires python3.
set -euo pipefail
ROOT="${CHECK_GATES_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
command -v python3 >/dev/null 2>&1 || { echo "check-gates: python3 not found"; exit 0; }
exec python3 - "$ROOT" "$@" <<'PY'
import glob, os, re, subprocess, sys

root = sys.argv[1]
args = sys.argv[2:]
strict, brief = "--strict" in args, "--brief" in args
os.chdir(root)

def read(p):
    try:
        with open(p, encoding="utf-8") as f:
            return f.read()
    except OSError:
        return None

def field(text, name):
    if not text:
        return None
    m = re.search(rf"^\s*\**{name}\**\s*:\s*\**\s*(.+?)\s*$", text, re.M | re.I)
    return m.group(1).strip().strip("*").strip() if m else None

def rounds(pattern, rx):
    out = []
    for p in glob.glob(pattern):
        m = re.search(rx, os.path.basename(p))
        if m:
            out.append((int(m.group(1)), p))
    return sorted(out)

def git(*a):
    try:
        return subprocess.run(["git", *a], capture_output=True, text=True, check=False)
    except FileNotFoundError:
        return None

project = read("PROJECT.md") or ""
results, notes = {}, []

# ---- G1: plan + latest plan audit + PI approval (git tag) + ethics fields
plan = read("docs/study-plan.md")
plan_rounds = rounds("docs/stats-audit/plan-round-*.md", r"plan-round-(\d+)\.md$")
r0 = read(plan_rounds[-1][1]) if plan_rounds else None
v0 = (field(r0, "Verdict") or "").upper()
g = git("rev-parse", "-q", "--verify", "refs/tags/g1-plan-approved")
tagged = bool(g and g.returncode == 0)
m = re.search(r"\|\s*Data class\s*\|\s*([^|]*)\|", project)
data_class = m.group(1).strip() if m else ""
m = re.search(r"\|\s*IRB / ethics approval\s*\|\s*([^|]*)\|", project)
irb = m.group(1).strip() if m else ""
needs_irb = bool(re.search(r"human|clinical|local|controlled|臨床|人體", data_class, re.I))
irb_missing = needs_irb and (not irb or irb.startswith("_") or irb.lower() in ("tbd", "na", "n/a", "-"))
why = []
if not plan: why.append("no docs/study-plan.md")
if not r0: why.append("no docs/stats-audit/plan-round-N.md (plan audit)")
elif not v0.startswith("APPROVE"): why.append(f"plan audit verdict: {v0 or 'missing'}")
if not tagged: why.append("no git tag g1-plan-approved (created only after the PI approves)")
if not data_class or data_class.startswith("_"): why.append("fill 'Data class' and 'IRB / ethics approval' in PROJECT.md")
elif irb_missing: why.append(f"data class '{data_class}' needs an IRB/ethics number in PROJECT.md")
results["G1"] = (not why, "; ".join(why) or "plan audited, PI-approved (tag g1-plan-approved)")
if tagged and plan:
    d = git("diff", "--stat", "g1-plan-approved", "--", "docs/study-plan.md", "config/")
    if d and d.stdout.strip():
        amend = git("tag", "-l", "g1-plan-amend-*")
        n_amend = len(amend.stdout.split()) if amend else 0
        notes.append(f"study-plan/config changed since g1-plan-approved ({n_amend} amendment tag(s)); "
                     "check the decision log explains every change: git diff g1-plan-approved -- docs/study-plan.md config/")

# ---- G2: latest results audit round >= 1
audits = rounds("docs/stats-audit/round-*.md", r"^round-(\d+)\.md$")
if not audits:
    results["G2"] = (False, "no results audit yet (docs/stats-audit/round-N.md)")
else:
    n, p = audits[-1]
    t = read(p); v = (field(t, "Verdict") or "").upper()
    if v.startswith("APPROVE WITH CHANGES"):
        ok = bool(field(t, "Changes confirmed"))
        results["G2"] = (ok, f"round {n}: APPROVE WITH CHANGES" + ("" if ok else " — 'Changes confirmed:' line missing"))
    else:
        results["G2"] = (v.startswith("APPROVE"), f"round {n}: {v or 'no Verdict line'}")
if os.path.exists("docs/stats-audit.md"):
    notes.append("legacy docs/stats-audit.md found — move it to docs/stats-audit/round-N.md")

# ---- G3: latest internal review
revs = rounds("manuscript/review-round-*.md", r"review-round-(\d+)\.md$")
if not revs:
    results["G3"] = (False, "no manuscript/review-round-N.md")
else:
    n, p = revs[-1]
    t = read(p); v = (field(t, "Recommendation") or "").upper()
    if v.startswith("ACCEPT"):
        results["G3"] = (True, f"round {n}: ACCEPT")
    elif v.startswith("MINOR"):
        ok = bool(field(t, "Minor points addressed"))
        results["G3"] = (ok, f"round {n}: MINOR REVISION" + ("" if ok else " — 'Minor points addressed:' line missing"))
    else:
        results["G3"] = (False, f"round {n}: {v or 'no Recommendation line'}")

# ---- G4: reproducibility
t = read("docs/reproducibility-report.md"); v = (field(t, "Verdict") or "").upper()
if not t:
    results["G4"] = (False, "no docs/reproducibility-report.md")
elif v.startswith("REPRODUCED WITH DISCREPANCIES"):
    ok = bool(field(t, "Discrepancies explained"))
    results["G4"] = (ok, "REPRODUCED WITH DISCREPANCIES" + ("" if ok else " — 'Discrepancies explained:' line missing"))
else:
    results["G4"] = (v == "REPRODUCED", v or "no Verdict line")

# ---- G5: submission checklist + PI approval
cks = glob.glob("submission/checklist-*.md")
if not cks:
    results["G5"] = (False, "no submission/checklist-<journal>.md")
else:
    open_items = []
    for p in cks:
        for line in (read(p) or "").splitlines():
            if re.match(r"^\s*[-*]\s*\[ \]", line) and not re.search(r"PI to supply", line, re.I):
                open_items.append(line.strip())
    approved = bool(re.search(r"\|[^|\n]*\|[^|\n]*G5[^|\n]*approv", project, re.I))
    if open_items:
        results["G5"] = (False, f"{len(open_items)} open checklist item(s)")
    else:
        results["G5"] = (approved, "checklist complete" + ("; PI approval logged" if approved else " — awaiting PI approval row (G5 … approved) in decision log"))

# ---- compare with PROJECT.md
claimed = {}
m = re.search(r"Gates passed\s*\|\s*([^\n]*)", project)
if m:
    for gname, mark in re.findall(r"(G[1-5])\s*([☑☐✓✔xX])", m.group(1)):
        claimed[gname] = mark in "☑✓✔xX"
mismatch = [gname for gname, (ok, _) in results.items() if claimed.get(gname) and not ok]
order = [gname for i, gname in enumerate(["G2", "G3", "G4", "G5"], start=2)
         if results[gname][0] and not results[f"G{i-1}"][0]]

if brief:
    s = " ".join(f"{gname}{'☑' if ok else '☐'}" for gname, (ok, _) in results.items())
    extra = f"  ⚠ PROJECT.md claims {','.join(mismatch)} but the files do not support it" if mismatch else ""
    print(f"Gates (from files): {s}{extra}")
    for n in notes:
        print("  ⚠ " + n)
    sys.exit(0)

print(f"Quality gates recomputed from files — {root}\n")
for gname, (ok, why) in results.items():
    c = claimed.get(gname)
    cl = "" if c is None else ("  [PROJECT.md: ☑]" if c else "  [PROJECT.md: ☐]")
    print(f"  {gname} {'PASS' if ok else '----'}  {why}{cl}")
if mismatch:
    print(f"\n✗ PROJECT.md marks {', '.join(mismatch)} as passed, but the report files do not support it.")
for gname in order:
    print(f"⚠ {gname} passes while an earlier gate does not — check the order of work.")
for n in notes:
    print("⚠ " + n)
sys.exit(1 if (strict and (mismatch or order)) else 0)
PY
