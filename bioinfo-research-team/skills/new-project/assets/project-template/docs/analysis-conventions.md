# Analysis conventions — {{PROJECT_NAME}}

Owned by `charlene-analyst`; every analyst follows it (`bioinfo-analyst` included). Project-specific additions go at the end with a date.

## Parameters and records
- Every chosen parameter has a **number, a reason, and a record** (`config/*.yaml` + the decision log in `results/summary/aim-<k>.md`).
- Decision log columns: date · finding · options · choice · reason. It is the Methods draft.
- Seeds: `set.seed(1234)` / `np.random.seed(1234)`; parallel back-ends seeded too (`RNGseed = 1234`).
- renv / conda lock files committed; paths relative to the project root; no `setwd()`.

## Versions
- Results that were shown to anyone are frozen. Changed reruns go to a new dated location (`results/versions/YYYYMMDD_<label>/` or new script numbers) and never overwrite or mix with the originals.
- "New version" = a new file next to the old one.
- Edit an existing file only after backing it up to `_backup/YYYYMMDD-HHMM_<reason>/` (relative paths kept, logged in `_backup/INDEX.md`).
- A run that follows the proposal / published method exactly comes first and is labelled as such; implementation choices it needed are listed.
- Uncertain choices are run as parallel scenarios with identical downstream steps; the primary scenario is pre-specified.

## Single-cell QC order (per capture lane, before integration)
1. Ambient correction (CellBender on the raw matrix, or SoupX / decontX).
2. Per-sample MAD-based cell QC, cells removed per step recorded.
3. Doublets by two methods with different principles (default scDblFinder + DoubletFinder or scds), label first, remove consensus, inspect single-method calls; genotype demultiplexing when donors were pooled.
4. Normalise → HVG → PCA → integration only if needed, with mixing and biology-preservation diagnostics.

## Inference
- Condition effects: pseudobulk per sample × cell type, minimum cells per sample (default ≥ 10, recorded), n per group reported.
- Differential abundance at the sample level.
- Aggregate changes are decomposed into proportion shift vs within-population change.
- Candidate genes chosen from literature are declared as hypothesis-driven, with their rank in the full table and family members' effects.
- Communication analyses export sender × receiver × pair tables; reported as hypotheses.
- Single-dataset findings are labelled; independent validation is sought and reported either way.

## Figures and reporting
- Figure labels in English. Every figure has a note: method, thresholds, key parameters, groups, n.
- Each aim summary ends with a Hypothesis ledger: supports / contradicts / inconclusive, likely reason, discriminating next step.
- Deck and document formats follow the PI's requirements recorded in `PROJECT.md` (e.g. bilingual zh/en, Word for write-ups).

## Project-specific additions
<!-- YYYY-MM-DD — rule — reason -->
