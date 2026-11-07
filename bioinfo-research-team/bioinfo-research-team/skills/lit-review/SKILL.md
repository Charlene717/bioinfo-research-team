---
name: lit-review
description: 文獻回顧與新穎性查核 (literature review / novelty check). Use when the user wants to know what is already published on a topic, needs related work for a manuscript, asks「這個做過了嗎」「幫我查文獻」「找 reference」, or wants references verified. Delegates to literature-scout and writes refs/.
argument-hint: "<topic or question> [--novelty \"<claim>\"] [--for-section intro|discussion] [--verify-bib]"
---

# /lit-review

Delegate to **`literature-scout`** (may appear as `bioinfo-research-team:literature-scout`). Follow the orchestration rules in `/team`.

## Steps

1. Read `PROJECT.md` (if present) for the research question and constraints; combine with `$ARGUMENTS`.
2. Brief `literature-scout` with: the question; the mode (`background scan`, `related work for <section>`, `novelty check for "<claim>"`, or `verify refs/references.bib`); the time window if the user set one; output paths `refs/literature-review.md`, `refs/references.bib`, `refs/search-log.md`; the requirement that every reference is resolved via Crossref/PubMed/Europe PMC and preprints/retractions are flagged.
3. For a broad topic, split into 2–3 sub-questions and run scouts in parallel, then ask one scout to merge and deduplicate the `.bib`.
4. Read the returned `refs/literature-review.md`. Check: PRISMA-style counts present, gap statement explicit, must-cite list ≤ 10, verification status stated. Send it back if any are missing.
5. Update `PROJECT.md` (phase 1, key gap statement, open questions) and the lab notebook.

## Report to the user

One-paragraph answer; the must-cite papers (first author, year, one-line relevance); the gap/novelty verdict; anything that could not be verified; recommended next step (`/plan-study` if the gap is real; rethink the question if it is not).
