---
name: make-figures
description: 產出可投稿的圖表與圖說 (publication-quality figures and legends from results tables). Use after Gate G2 when the user wants main/supplementary figures, a graphical abstract, or journal-spec figure formatting, or says「畫圖」「做 figure」「圖說」. Delegates to figure-designer.
argument-hint: "[fig1|figS2|all] [--journal <name>] [--graphical-abstract]"
---

# /make-figures

Follow the orchestration rules in `/team`. Precondition: G2 ☑ (figures of unaudited results are diagnostic only and must stay in `results/diagnostics/`).

## Steps

1. Collect the figure plan from `docs/study-plan.md` §10 and `results/RESULTS-SUMMARY.md`; if a target journal is known (`PROJECT.md` or `--journal`), make sure `submission/checklist-<journal>.md` exists (else ask `submission-strategist` for the figure specs only).
2. Brief **`figure-designer`**: which figures, the exact `results/tables/*` to plot, journal specs (width, dpi, fonts, panel labels), colour mapping per condition to keep across figures, and outputs (`figures/scripts/figN.*`, `figures/output/figN.{pdf,png}`, `figures/legends.md`, `figures/ASSETS.md`). Run independent figures in parallel if there are many.
3. Verify: every script runs from the project root (`make figures` or the listed commands), legends quote numbers that exist in `results/tables/`, palettes are colour-blind safe, each figure has a one-sentence message. Send back anything that recomputed statistics or hard-coded numbers.
4. Update `PROJECT.md` (phase 5 → 6) and the lab notebook; recommend `/draft-paper`.

## Report to the user

List figures with their one-sentence message; any data gaps or journal-spec conflicts; visual issues flagged in the data.
