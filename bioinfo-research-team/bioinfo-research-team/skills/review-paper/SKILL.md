---
name: review-paper
description: 以嚴格審稿人的角度審查任何論文草稿 (independent peer review of a manuscript draft — ours or one the user is refereeing). Use when the user says「幫我審這篇」「review 這個稿子」「當 reviewer 2」, pastes or points to a manuscript/PDF, or wants a pre-submission check. Delegates to peer-reviewer; read-only on the manuscript.
argument-hint: "[path/to/manuscript.(md|docx|pdf)] [--venue <journal>] [--focus stats|repro|novelty|all]"
---

# /review-paper

Follow the orchestration rules in `/team`.

## Steps

1. Locate the manuscript: `$ARGUMENTS` path, else `manuscript/manuscript.md`. For `.docx`/`.pdf`, convert to text first (`pandoc -t plain` / `pdftotext`) into the scratchpad and pass that path; do not modify the original.
2. Decide scope: our own paper (full access to `results/`, `analysis/`, audit) vs. an external manuscript the user is refereeing (text, figures, and supplementary only; no code expectations beyond what the paper claims).
3. Brief **`peer-reviewer`** with the paths, the venue, the focus, and the output path (`manuscript/review-round-N.md` for ours; `reviews/<slug>-review.md` for external). For external reviews, add: be confidential, do not search for author identities, do not upload the text anywhere, and phrase for the authors (constructive, specific).
4. If `--focus stats` or the review raises statistical doubts, also brief **`biostatistician`** on the same text and merge the verdicts.
5. Return the review. For our paper, update `PROJECT.md` and the notebook; for external, remind the user that the final judgement and wording are theirs and that journal confidentiality rules apply.
