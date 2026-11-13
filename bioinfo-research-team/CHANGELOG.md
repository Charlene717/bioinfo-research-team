# Changelog

## 0.2.0 — 2026-11-12

### Fixed
- **Raw-data hook rewritten** (`hooks/protect_raw_data.py`). It now blocks in-place `gzip`/`gunzip`/`bgzip`/`xz`, `find -delete` / `-exec rm`, overwriting `cp`/`mv`/`rsync`/`tar`/`unzip`, `rsync --delete`, `chmod` that grants write, inline `python -c` / `Rscript -e` writes, and `cd data/raw && rm …` (the hook tracks `cd`). New downloads into `data/raw/` are still allowed, including `curl … > new-file` (the old hook blocked this, while `wget -O` was allowed). Commands that mention `data/raw` but cannot be parsed are blocked.
- **The hook no longer fails open on large writes.** The JSON payload used to be passed as a command-line argument, so writes over 128 KB hit `Argument list too long`, exited with 126, and went through unchecked. The payload now goes through stdin.
- **`.gitignore` now commits the files needed to verify the data**: `data/raw/MANIFEST*`, `data/raw/README*`, `data/processed/sample_sheet.tsv`, `metadata-mapping.md`, and the `.gitkeep` files for ignored folders.
- **Makefile**:
  - Uses `pipefail`, so a failing script before `| tee` now stops the build.
  - Runs `analysis/NN_*` scripts in numeric order with R, Python and shell scripts mixed together. Before, all R scripts ran first and then all Python scripts.
  - `make test` now fails when a test fails.
  - New `dirs` target creates the output folders that git does not track.
- **`biostatistician` and `peer-reviewer` have the Write tool**, limited to their own report files. Before, they had to write files through Bash heredocs.
- **Agents running in parallel no longer write to the same files.**
  - Each analyst works on one aim: `results/summary/aim-<k>.md`, `config/aim-<k>.yaml`, and its own script-number block.
  - Scouts write to `refs/partial/`, and a final scout merges the results.
  - The orchestrator is the only writer of `PROJECT.md`, the lab notebook, `RESULTS-SUMMARY.md` and the shared config. Agents return a `NOTEBOOK ENTRY` block instead of editing the notebook.
- **Statistical audits are kept per round**: `docs/stats-audit/plan-round-N.md` and `docs/stats-audit/round-N.md`. Earlier rounds are never edited.
- README and manifest counts now match the plugin contents.

### Added
- **`make gates` / `tools/check-gates.sh`** recomputes G1–G5 from the report files and compares them with the ☑ marks in `PROJECT.md`. The `--strict` flag makes it exit 1 on a mismatch. The SessionStart hook shows the recomputed gate line.
- **`make manifest` / `make verify-raw` (`tools/raw-manifest.sh`).** `make manifest` adds checksums only for files not yet listed. `make verify-raw` reports files that are changed, missing or not listed. `make analysis` runs `verify-raw` first.
- **Enforceable pre-registration.**
  - When the PI approves the plan at G1, it is committed and tagged `g1-plan-approved`.
  - Later amendments get a tag `g1-plan-amend-<n>`.
  - The statistician diffs the plan and config against the tag in every results audit; an undocumented change to the primary analysis is a Critical finding.
- **Machine-readable gate lines**: `Changes confirmed:`, `Minor points addressed:` and `Discrepancies explained:`. For G5, a decision-log row `G5 final files approved`.
- **Two-pass (blind-first) protocol** for `biostatistician` and `peer-reviewer`. They read the tables and code first, then the narrative, and report any place where the narrative goes beyond the evidence.
- **New agent `domain-expert`** (領域生物學專家).
  - Writes `docs/domain-brief.md`: expected cell types, markers, positive controls and tissue artefacts.
  - Reviews the plan, the annotation and results, and the Discussion, in `docs/domain-review.md`.
  - Wired into `/plan-study`, `/analyze`, `/draft-paper`, `/respond-reviewers`, `/review-paper` and `/paper-pipeline`.
- **Handling local clinical data.**
  - `PROJECT.md` has new `Data class` and `IRB / ethics approval` fields, and G1 requires them.
  - `data-engineer` has a new intake section: de-identification check, coded sample IDs, storage per protocol.
  - No sample-level data goes into web searches.
  - `--unattended` never auto-approves G1 for human or controlled-access data.
- `tests/test_protect_raw_data.py`: 53 regression cases for the hook.
- `install.sh --uninstall` now also removes the hook entries from `settings.json` (after making a backup).
