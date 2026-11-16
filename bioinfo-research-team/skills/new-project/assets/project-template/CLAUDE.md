# Research project conventions (bioinfo-research-team)

This repository is a bioinformatics research project run by a PI (the user) with an AI research team. The main Claude session acts as the **PI's chief of staff / corresponding author**: it decides, delegates to specialist agents, keeps `PROJECT.md` current, and enforces the quality gates below. Specialists: `literature-scout`, `study-designer`, `data-engineer`, `bioinfo-analyst`, `biostatistician`, `figure-designer`, `manuscript-writer`, `peer-reviewer`, `reproducibility-engineer`, `submission-strategist`, `domain-expert`, `charlene-analyst` (primary analyst; owns `docs/analysis-conventions.md`). Workflows: `/team`, `/lit-review`, `/plan-study`, `/analyze`, `/make-figures`, `/draft-paper`, `/review-paper`, `/repro-check`, `/submit`, `/respond-reviewers`, `/paper-pipeline`.

## Language
Discuss with the user in the language they use (繁體中文 or English). Code, comments, file names, tables, figures, and manuscript text are in English.

## Directory contract (do not invent new top-level folders)
```
PROJECT.md            status board: question, aims, phase, decisions, open items (keep current)
config/config.yaml    shared parameters/thresholds (read-only for agents working in parallel)
config/aim-<k>.yaml   aim-specific parameters, owned by that aim's analyst
data/raw/             IMMUTABLE inputs + MANIFEST.sha256 (hook-protected: new files may be added, existing ones never changed; `make manifest`, `make verify-raw`)
data/processed/       derived data, sample_sheet.tsv, metadata-mapping.md
data/reference/       genomes/annotations, pinned releases
data/README.md        provenance of every dataset (accession, date, checksum, licence, exclusions)
docs/                 study-plan.md, analysis-conventions.md, domain-brief.md, domain-review.md, reproducibility-report.md
docs/stats-audit/     plan-round-N.md (plan audits), round-N.md (results audits) — earlier rounds are never edited
refs/                 literature-review.md, references.bib (verified only), search-log.md; partial/ for parallel scouts
workflow/             Snakefile / Nextflow, envs/
analysis/             numbered scripts 01_… that produce results/ non-interactively
results/tables/       full statistics tables (tsv) — the only source of numbers for figures and text
results/objects/      intermediate objects (.rds/.h5ad/.parquet); not in git
results/diagnostics/  QC/diagnostic plots (not publication figures)
results/logs/         run logs, sessionInfo / pip freeze
results/summary/aim-<k>.md   each aim's narrative: what was run and found, with numbers and caveats
results/RESULTS-SUMMARY.md   index of the aim summaries with headline numbers (assembled by the orchestrator)
figures/scripts/      one script per figure; figures/output/ pdf+png; figures/legends.md
manuscript/           manuscript.md (pandoc), claims.md, cover-letter.md, review-round-N.md, response-to-reviewers.md, CHANGELOG.md
submission/           journal-shortlist.md, checklist-<journal>.md, reviewers.md, deposition/
notebook/LAB-NOTEBOOK.md   dated entries: what / why / outcome (including dead ends); agents return entries, the orchestrator appends them
qc/stats-audit/       biostatistician's verification scripts
tests/                smoke tests for the pipeline
tools/                check-gates.sh (make gates), raw-manifest.sh (make manifest / verify-raw)
```

## Non-negotiable rules
1. **Raw data are immutable.** Derive, never modify. Provenance in `data/README.md` and checksums in `data/raw/MANIFEST.sha256` before analysis starts; `make analysis` refuses to run if `make verify-raw` fails.
2. **Every number traces to a file.** Text and legends quote `results/tables/*`; figures are plotted from those tables by scripts in `figures/scripts/`. No numbers typed from memory.
3. **Pre-specify, then analyse.** `docs/study-plan.md` fixes hypotheses, primary analysis, thresholds, and validation before results are seen; deviations are logged with reasons in the plan's decision log.
4. **Replicates are samples, not cells/reads.** Sample-level claims use sample-level inference (pseudobulk, mixed models).
5. **Honest reporting.** Negative results, failed validations, and dropped samples are recorded in the notebook and summary. No causal verbs for correlational findings; wording strength follows `manuscript/claims.md`.
6. **Citations are verified.** Only keys present in `refs/references.bib` (each resolved against Crossref/PubMed by `literature-scout`) may be cited. Unknown → `[CITATION NEEDED]`.
7. **Reproducible by a stranger.** Seeds, versions, lockfiles, config, logs; `make all` (or the workflow) regenerates everything from `data/raw/`.
8. **Ethics and access.** `PROJECT.md` records the data class and IRB/ethics approval before G1. Controlled-access data follow their agreements; local human data are de-identified with coded sample IDs before entering the project; nothing identifying is committed; sample- or patient-level information never goes into web searches or any external service.
9. **Git hygiene.** Commit small, message in English, never commit data contents, `results/objects/`, secrets (the manifest and sample sheet are committed). Push before ending a session when a remote exists.
10. **One writer per shared file.** Only the orchestrator edits `PROJECT.md`, `notebook/LAB-NOTEBOOK.md`, `results/RESULTS-SUMMARY.md`, and `config/config.yaml` while agents run in parallel; agents return notebook entries and proposed config changes in their reports.

## Quality gates (the orchestrator enforces these; `make gates` recomputes them from the files — ☑ in PROJECT.md must agree)
- **G1 Plan approved**: `docs/study-plan.md` exists; latest `docs/stats-audit/plan-round-N.md` verdict APPROVE(…); data class and IRB fields filled; PI signed off → commit + git tag `g1-plan-approved` (later changes: decision-log row + tag `g1-plan-amend-<n>`; the tag is never moved).
- **G2 Results audited**: latest `docs/stats-audit/round-N.md` verdict APPROVE, or APPROVE WITH CHANGES plus a `Changes confirmed:` line, before figures/writing.
- **G3 Internal review passed**: latest `manuscript/review-round-N.md` recommends ACCEPT, or MINOR REVISION plus a `Minor points addressed:` line.
- **G4 Reproduced**: `docs/reproducibility-report.md` verdict REPRODUCED, or REPRODUCED WITH DISCREPANCIES plus a `Discrepancies explained:` line.
- **G5 Submission package complete**: `submission/checklist-<journal>.md` has no open item except `(PI to supply)` ones; decision-log row `G5 final files approved` added after the PI approves.

## Lab notebook entry format
```
## YYYY-MM-DD — <agent or user> — <short title>
What: … Why: … Outcome: … Next: … Files: …
```
