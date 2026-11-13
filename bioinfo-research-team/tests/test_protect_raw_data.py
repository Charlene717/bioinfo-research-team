#!/usr/bin/env python3
"""Regression tests for hooks/protect-raw-data.sh. Run: python3 tests/test_protect_raw_data.py"""
import json, os, subprocess, sys, tempfile

HOOK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "hooks", "protect-raw-data.sh")
proj = tempfile.mkdtemp()
os.makedirs(f"{proj}/data/raw/geo", exist_ok=True)
os.makedirs(f"{proj}/data/processed", exist_ok=True)
for f in ["a.fastq.gz", "a.fastq", "meta.tsv", "y.gz", "geo/s1.h5"]:
    open(f"{proj}/data/raw/{f}", "w").close()

def run(tool, ti, cwd=proj):
    p = subprocess.run(["bash", HOOK], input=json.dumps({"tool_name": tool, "tool_input": ti, "cwd": cwd}),
                       capture_output=True, text=True)
    return p.returncode

BLOCK, ALLOW = 2, 0
bash_cases = [
    ("rm data/raw/a.fastq.gz", BLOCK),
    ("gunzip data/raw/a.fastq.gz", BLOCK),
    ("gzip data/raw/a.fastq", BLOCK),
    ("cd data/raw && rm a.fastq.gz", BLOCK),
    ("cd data/raw; gunzip *.gz", BLOCK),
    ("find data/raw -name '*.tmp' -delete", BLOCK),
    ("find data/raw -type f -exec rm {} +", BLOCK),
    ("cp new.tsv data/raw/meta.tsv", BLOCK),
    ("cp new.tsv data/raw/", ALLOW),            # new file name, no overwrite
    ("cp meta.tsv data/raw/", BLOCK),           # would overwrite data/raw/meta.tsv
    ("cp -n meta.tsv data/raw/", ALLOW),
    ("chmod u+w data/raw/meta.tsv", BLOCK),
    ("chmod -R 644 data/raw", BLOCK),
    ("find data/raw -type f -exec chmod a-w {} +", ALLOW),
    ("chmod a-w data/raw/meta.tsv", ALLOW),
    ("python3 -c \"open('data/raw/meta.tsv','w')\"", BLOCK),
    ("Rscript -e \"file.remove('data/raw/meta.tsv')\"", BLOCK),
    ("python3 -c \"import pandas as pd; print(pd.read_csv('data/raw/meta.tsv'))\"", ALLOW),
    ("rsync -a --delete src/ data/raw/", BLOCK),
    ("rsync -a --ignore-existing src/ data/raw/", ALLOW),
    ("mv data/raw/meta.tsv data/processed/", BLOCK),
    ("mv dl.tmp data/raw/new.fastq.gz", ALLOW),
    ("curl -L https://x/new.gz > data/raw/new.gz", ALLOW),
    ("curl -L https://x/y.gz > data/raw/y.gz", BLOCK),   # exists -> overwrite
    ("echo x >> data/raw/meta.tsv", BLOCK),
    ("wget -O data/raw/y.gz https://x/y.gz", BLOCK),
    ("wget -c -O data/raw/new2.gz https://x/z.gz", ALLOW),
    ("curl -sSL -o data/raw/new3.tar https://x", ALLOW),
    ("tar -xzf x.tar.gz -C data/raw", BLOCK),
    ("tar -xzf x.tar.gz --skip-old-files -C data/raw", ALLOW),
    ("unzip x.zip -d data/raw", BLOCK),
    ("unzip -n x.zip -d data/raw", ALLOW),
    ("sed -i 's/a/b/' data/raw/meta.tsv", BLOCK),
    ("perl -pi -e 's/a/b/' data/raw/meta.tsv", BLOCK),
    ("sha256sum data/raw/* > data/raw/MANIFEST.sha256", ALLOW),
    ("sha256sum -c data/raw/MANIFEST.sha256", ALLOW),
    ("zcat data/raw/a.fastq.gz | head", ALLOW),
    ("gunzip -c data/raw/a.fastq.gz > data/processed/a.fastq", ALLOW),
    ("gzip -k data/raw/a.fastq", ALLOW),
    ("ls -la data/raw && wc -l data/raw/meta.tsv", ALLOW),
    ("fasterq-dump SRR1 -O data/raw/sra", ALLOW),
    ("rm -rf results/objects/*", ALLOW),
    ("sudo rm -rf data/raw", BLOCK),
    ("echo $(rm data/raw/meta.tsv)", BLOCK),
    ("truncate -s 0 data/raw/meta.tsv", BLOCK),
    ("git status", ALLOW),
]
fails = 0
for cmd, exp in bash_cases:
    got = run("Bash", {"command": cmd})
    ok = got == exp
    fails += not ok
    print(f"{'ok  ' if ok else 'FAIL'} {('BLOCK' if exp == 2 else 'ALLOW'):5} rc={got}  {cmd}")

# cwd inside data/raw
got = run("Bash", {"command": "rm meta.tsv"}, cwd=f"{proj}/data/raw"); fails += got != 2
print(f"{'ok  ' if got == 2 else 'FAIL'} BLOCK rc={got}  (cwd=data/raw) rm meta.tsv")

file_cases = [
    ("Write", {"file_path": "data/raw/meta.tsv", "content": "x"}, BLOCK),
    ("Write", {"file_path": f"{proj}/data/raw/new.tsv", "content": "x" * 300_000}, BLOCK),  # >128 KB payload
    ("Edit", {"file_path": "data/raw/MANIFEST.sha256", "old_string": "a", "new_string": "b"}, ALLOW),
    ("Write", {"file_path": "data/raw/README.md", "content": "x"}, ALLOW),
    ("Write", {"file_path": "data/processed/sample_sheet.tsv", "content": "x" * 300_000}, ALLOW),
    ("NotebookEdit", {"notebook_path": "data/raw/x.ipynb"}, BLOCK),
]
for tool, ti, exp in file_cases:
    got = run(tool, ti); ok = got == exp; fails += not ok
    print(f"{'ok  ' if ok else 'FAIL'} {('BLOCK' if exp == 2 else 'ALLOW'):5} rc={got}  {tool} {ti.get('file_path') or ti.get('notebook_path')}")

print(f"\n{fails} failure(s)")
sys.exit(1 if fails else 0)
