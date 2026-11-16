---
name: paper-pipeline
description: 一鍵從研究問題做到可投稿論文 (end-to-end research pipeline with checkpoints). Use when the user gives a research question or idea and wants the whole team to run — literature → plan → data → analysis → audit → figures → manuscript → internal review → reproducibility → submission package — or says「把這個題目做成論文」「從頭到尾跑一遍」「開始一個新研究」. Resumes from the phase recorded in PROJECT.md.
argument-hint: "<research question> [--journal <name>] [--data <accession|path>] [--unattended] [--stop-after plan|analysis|figures|draft|repro]"
---

# /paper-pipeline — the whole team, in order

Follow the orchestration rules in `/team`. You are the PI's chief of staff: delegate every specialist task, enforce the gates, and stop at the checkpoints below unless `--unattended` was given (then take the recommended option and write "auto-approved per user instruction" in the decision log). `--unattended` never auto-approves Checkpoint 1 when `PROJECT.md` lists local human / clinical or controlled-access data: those plans always wait for the PI. Never submit, post a preprint, deposit data, or spend money; prepare and hand over.

## Phase 0 — Setup
- Parse `$ARGUMENTS`: question, `--journal`, `--data`, `--unattended`, `--stop-after`.
- If no `PROJECT.md` in the working directory: run `/new-project` (name from the question) and `cd` into it conceptually (all paths below are project-relative). If `PROJECT.md` exists, read its phase and **resume from there**; do not redo completed phases unless their outputs are missing.
- Record the question and options in `PROJECT.md`.

## Phase 1 — Literature (`/lit-review` logic)
`literature-scout` → `refs/`. If the novelty check shows the question is already answered by published work, **stop** and report; propose the nearest open question.

## Phase 2 — Plan (`/plan-study` logic) → Gate G1
`domain-expert` → `docs/domain-brief.md`; `study-designer` → `docs/study-plan.md`; `biostatistician` plan audit (`docs/stats-audit/plan-round-N.md`) and `domain-expert` plan review in parallel; one revision loop; on approval commit + tag `g1-plan-approved`. **Checkpoint 1 (PI)**: approve dataset(s) and plan. `--stop-after plan` ends here.

## Phase 3 — Data
`data-engineer` → raw data with manifest, provenance, sample sheet, QC, environment and workflow files. Access application needed → **stop** and hand the PI the steps.

## Phase 4 — Analysis (`/analyze` logic) → Gate G2
the aim's analyst (`charlene-analyst` or `bioinfo-analyst`, routing in `/team`) per aim (parallel where independent, separate files per aim) → assemble `RESULTS-SUMMARY.md` → `biostatistician` audit → `domain-expert` plausibility review → ≤ 2 fix loops. Unresolved Critical findings → **stop**, report options. `--stop-after analysis` ends here.

## Phase 5 — Figures (`/make-figures` logic)
`figure-designer` from `results/tables/`. `--stop-after figures` ends here.

## Phase 6 — Venue
If `--journal` not given: `submission-strategist` shortlist. **Checkpoint 2 (PI)**: choose the journal (unattended: top recommendation).

## Phase 7 — Manuscript (`/draft-paper` logic) → Gate G3
`manuscript-writer` (claims map → draft) → `literature-scout` for `[CITATION NEEDED]` → `peer-reviewer` → ≤ 2 revision rounds. Still MAJOR REVISION → **stop**, report. `--stop-after draft` ends here.

## Phase 8 — Reproducibility (`/repro-check` logic) → Gate G4
`reproducibility-engineer` full run; discrepancies → the aim's analyst fixes → quick re-check → `manuscript-writer` updates numbers/statements. `--stop-after repro` ends here.

## Phase 9 — Submission package (`/submit` logic) → Gate G5
`submission-strategist` checklist, cover letter, reviewers, paperwork; final consistency check. **Checkpoint 3 (PI)**: approve the final files. Hand over portal steps and the preprint decision.

## Bookkeeping (after every phase)
Update `PROJECT.md` (phase, ≤ 10-line status, open decisions, decision-log row), append the agents' `NOTEBOOK ENTRY` blocks to `notebook/LAB-NOTEBOOK.md`, run `make gates` and set ☑ only for gates it reports as PASS. Commit at each gate with an English message (no data); push only if a remote exists.

## Final report to the user
Outcome first (what the paper claims, with its key effect sizes, CIs and n), the gates passed, what the PI must do next (approve, supply IRB/grant/ORCID info, submit), and the paths of the deliverables (`manuscript/manuscript.docx`, `figures/output/`, `submission/`). State plainly anything that was not reproduced, not verified, or auto-approved.
