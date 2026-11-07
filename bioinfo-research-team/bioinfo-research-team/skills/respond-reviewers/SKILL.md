---
name: respond-reviewers
description: 處理審稿意見與修稿 (triage a decision letter, run requested analyses, revise, and write the point-by-point response). Use when the user receives reviewer comments or a decision letter, says「審稿意見回來了」「回覆 reviewer」「修稿」, or pastes referee reports. Runs submission-strategist (triage) → bioinfo-analyst/biostatistician (new analyses) → manuscript-writer (response + revision) → peer-reviewer (sanity check).
argument-hint: "<path/to/decision-letter.(txt|md|pdf)> [--deadline <date>]"
---

# /respond-reviewers

Follow the orchestration rules in `/team`.

## Steps

1. Save the decision letter verbatim under `submission/decision-<date>.md` (convert PDF with `pdftotext` if needed; never edit the reviewers' words).
2. Brief **`submission-strategist`** to triage: number every comment, classify must-do / should-do / can-rebut, estimate effort, assign an agent, propose a timeline against `--deadline`; output `submission/decision-<date>-triage.md`. Present the triage to the PI and confirm the plan (especially any comment the team proposes to rebut rather than follow).
3. **New analyses**: brief **`bioinfo-analyst`** per assigned comment (pre-specify the analysis in a short addendum to `docs/study-plan.md` §12 first), then **`biostatistician`** to audit the additions (`docs/stats-audit.md` new round). Figures via **`figure-designer`**; citations via **`literature-scout`**.
4. **Response and revision**: brief **`manuscript-writer`** to write `manuscript/response-to-reviewers.md` (quote → response → exact change with location → new text) and to revise `manuscript/manuscript.md` with a tracked `CHANGELOG.md` entry; a marked-up copy if the journal requires (e.g., `pandoc --track-changes` from a diff, or highlighted docx).
5. **Sanity check**: brief **`peer-reviewer`** to verify every reviewer point is answered honestly, every claimed change exists, and no new over-claims were introduced. Fix and re-check once.
6. Rebuild documents (`make manuscript`), update `submission/checklist-<journal>.md` for resubmission, `PROJECT.md` (phase 10), lab notebook. Hand the PI the files and portal steps; do not submit.

## Report to the user

Comments resolved vs. rebutted vs. outstanding, new results (with numbers if they changed a conclusion), what changed in the manuscript, and the decisions needed before resubmission.
