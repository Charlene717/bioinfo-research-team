---
name: submit
description: 準備完整投稿包並做最終一致性檢查 (final submission package and consistency check). Use when the paper is reviewed and reproduced and the user says「準備投稿」「投稿」「要投 <journal>」「cover letter」. Runs submission-strategist and a final cross-check; ends at Gate G5. Never submits to a portal or posts a preprint — the PI does that.
argument-hint: "[--journal <name>] [--preprint biorxiv|medrxiv|none]"
---

# /submit — Gate G5

Follow the orchestration rules in `/team`. Preconditions: G3 ☑ and G4 ☑ (else run `/draft-paper` / `/repro-check`; if the PI wants to skip a gate, record the risk in the decision log).

## Steps

1. Brief **`submission-strategist`**: the target journal (or ask for the shortlist and let the PI choose), preprint preference, and the outputs: `submission/checklist-<journal>.md` (all items), `submission/cover-letter.md` (with `manuscript-writer`), `submission/reviewers.md`, CRediT/ORCID/ethics/funding statements, preprint plan, and the exact portal steps.
2. **Final cross-check** (brief `peer-reviewer` in consistency mode, or do it with grep if small): abstract numbers = results tables; every figure/table referenced in order; legends match outputs; references all resolve to `.bib` keys with DOIs; word/figure limits met; statements present (ethics/IRB numbers, data/code availability, COI, funding, contributions); reporting checklist filled; supplementary files listed.
3. Produce the final files: `make manuscript` (docx/pdf), figures in the journal's format, supplementary bundle, checklist with every box ticked or an explicit "PI to supply" note.
4. **G5 passes** when the checklist has no open item except those only the PI can supply. Update `PROJECT.md` (phase 9, G5 ☑), lab notebook.
5. Hand over to the PI: the file list with paths, the portal steps, the preprint decision, and what to paste where. Do not upload, post, or e-mail anything.

## Report to the user

Recommended journal and why, the files ready, items the PI must supply (IRB numbers, grants, ORCIDs, COI), and the preprint decision.
