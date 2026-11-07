---
name: draft-paper
description: 撰寫並內審論文草稿 (draft the manuscript and pass internal peer review). Use after figures exist when the user wants the paper written or revised, says「寫論文」「寫 paper」「改稿」, or wants a cover letter. Runs submission-strategist (journal choice if unknown) → manuscript-writer → peer-reviewer → revision loop; ends at Gate G3.
argument-hint: "[--journal <name>] [--sections abstract,intro,...] [--rounds 2]"
---

# /draft-paper — Gate G3

Follow the orchestration rules in `/team`. Preconditions: G2 ☑, `figures/legends.md` present (else `/make-figures`).

## Steps

1. **Venue**: if no target journal is recorded in `PROJECT.md` and none is given, brief **`submission-strategist`** for `submission/journal-shortlist.md` and the top candidate's `checklist-<journal>.md`; ask the PI to choose (unattended runs take the recommendation and log it). Word/figure limits from the checklist constrain the draft.
2. **Draft**: brief **`manuscript-writer`** with every input path (plan, results summary, tables, legends, audit, data README, literature review, `.bib`, checklist) and outputs (`manuscript/claims.md` first, then `manuscript/manuscript.md`, `manuscript/CHANGELOG.md`). Insist on: cite only `.bib` keys, `[CITATION NEEDED]` otherwise; numbers copied from tables; wording strength per `claims.md`; reporting guideline named.
3. **Citations**: if the writer lists `[CITATION NEEDED]` items, brief **`literature-scout`** to find and verify them (append to `.bib`), then have the writer insert them.
4. **Review**: brief **`peer-reviewer`** (round N) with the manuscript, figures, tables, code, audit; output `manuscript/review-round-N.md` with a recommendation.
5. **Revise loop** (default max 2 rounds, `--rounds` to change): Major points → the responsible agent (`manuscript-writer` for text; `bioinfo-analyst` + `biostatistician` for analyses; `figure-designer` for figures; `literature-scout` for novelty/citations); then `manuscript-writer` updates the draft and `CHANGELOG.md`; then `peer-reviewer` re-reviews. **G3 passes** at ACCEPT or MINOR REVISION with the minor points addressed. If still MAJOR after the allowed rounds, stop and give the PI the unresolved points with options (more analysis, reframe, different venue).
6. Build `manuscript/manuscript.docx` via `make manuscript` if pandoc is available (fetch the journal CSL into `submission/style.csl`). Update `PROJECT.md` (phase 6 → 7 → 8, G3 ☑), lab notebook; recommend `/repro-check`.

## Report to the user

Title options, abstract, word counts vs. limits, reviewer recommendation and the Major points that were resolved or remain, claims that were downgraded and why, and the decisions needed (framing, title, which limitation to foreground).
