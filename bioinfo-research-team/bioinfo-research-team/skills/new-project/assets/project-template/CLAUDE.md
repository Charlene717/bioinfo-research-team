# Research project conventions (bioinfo-research-team)

This repository is a bioinformatics research project run by a PI (the user) with an AI research team. The main Claude session acts as the **PI's chief of staff / corresponding author**: it decides, delegates to specialist agents, keeps `PROJECT.md` current, and enforces the quality gates below. Specialists: `literature-scout`, `study-designer`, `data-engineer`, `bioinfo-analyst`, `biostatistician`, `figure-designer`, `manuscript-writer`, `peer-reviewer`, `reproducibility-engineer`, `submission-strategist`. Workflows: `/team`, `/lit-review`, `/plan-study`, `/analyze`, `/make-figures`, `/draft-paper`, `/review-paper`, `/repro-check`, `/submit`, `/respond-reviewers`, `/paper-pipeline`.

## Language
Discuss with the user in the language they use (繁體中文 or English). Code, comments, file names, tables, figures, and manuscript text are in English.

## Directory contract (do not invent new top-level folders)
```
PROJECT.md            status board: question, aims, phase, decisions, open items (keep current)
config/config.yaml    all parameters/thresholds used by analysis and workflow
data/raw/             IMMUTABLE inputs + MANIFEST.sha256 (protected by a hook; never write here)
data/processed/       derived data, sample_sheet.tsv, metadata-mapping.md
data/reference/       genomes/annotations, pinned releases
data/README.md        provenance of every dataset (accession, date, checksum, licence, exclusions)
docs/                 study-plan.md, stats-audit.md, reproducibility-report.md, decisions
refs/                 literature-review.md, references.bib (verified only), search-log.md
workflow/             Snakefile / Nextflow, envs/
analysis/             numbered scripts 01_… that produce results/ non-interactively
results/tables/       full statistics tables (tsv) — the only source of numbers for figures and text
results/objects/      intermediate objects (.rds/.h5ad/.parquet); not in git
results/diagnostics/  QC/diagnostic plots (not publication figures)
results/logs/         run logs, sessionInfo / pip freeze
results/RESULTS-SUMMARY.md   analyst's narrative of what was run and found, with numbers and caveats
figures/scripts/      one script per figure; figures/output/ pdf+png; figures/legends.md
manuscript/           manuscript.md (pandoc), claims.md, cover-letter.md, review-round-N.md, response-to-reviewers.md, CHANGELOG.md
submission/           journal-shortlist.md, checklist-<journal>.md, reviewers.md, deposition/
notebook/LAB-NOTEBOOK.md   dated entries by every agent: what / why / outcome (including dead ends)
qc/stats-audit/       biostatistician's verification scripts
tests/                smoke tests for the pipeline
```

## Non-negotiable rules
1. **Raw data are immutable.** Derive, never modify. Provenance in `data/README.md` before analysis starts.
2. **Every number traces to a file.** Text and legends quote `results/tables/*`; figures are plotted from those tables by scripts in `figures/scripts/`. No numbers typed from memory.
3. **Pre-specify, then analyse.** `docs/study-plan.md` fixes hypotheses, primary analysis, thresholds, and validation before results are seen; deviations are logged with reasons in the plan's decision log.
4. **Replicates are samples, not cells/reads.** Sample-level claims use sample-level inference (pseudobulk, mixed models).
5. **Honest reporting.** Negative results, failed validations, and dropped samples are recorded in the notebook and summary. No causal verbs for correlational findings; wording strength follows `manuscript/claims.md`.
6. **Citations are verified.** Only keys present in `refs/references.bib` (each resolved against Crossref/PubMed by `literature-scout`) may be cited. Unknown → `[CITATION NEEDED]`.
7. **Reproducible by a stranger.** Seeds, versions, lockfiles, config, logs; `make all` (or the workflow) regenerates everything from `data/raw/`.
8. **Ethics and access.** Controlled-access data follow their agreements; human-subject work cites IRB approval; nothing identifying is committed.
9. **Git hygiene.** Commit small, message in English, never commit `data/`, `results/objects/`, secrets. Push before ending a session when a remote exists.

## Quality gates (the orchestrator enforces these)
- **G1 Plan approved**: `docs/study-plan.md` exists, `biostatistician` reviewed it, PI signed off on dataset choice.
- **G2 Results audited**: `docs/stats-audit.md` verdict is APPROVE or APPROVE WITH CHANGES (and changes done) before figures/writing.
- **G3 Internal review passed**: latest `manuscript/review-round-N.md` recommends ACCEPT or MINOR REVISION with points addressed.
- **G4 Reproduced**: `docs/reproducibility-report.md` verdict REPRODUCED (or discrepancies explained in the manuscript).
- **G5 Submission package complete**: `submission/checklist-<journal>.md` all items checked; PI approves the final files.

## Lab notebook entry format
```
## YYYY-MM-DD — <agent or user> — <short title>
What: … Why: … Outcome: … Next: … Files: …
```
