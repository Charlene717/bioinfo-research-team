---
name: analyze
description: 執行分析並通過統計審核 (acquire data, run the pre-specified analysis, audit statistics). Use when the plan is approved and the user wants results, says「開始分析」「跑分析」「處理資料」, or when reviewers request additional analyses. Runs data-engineer → the aim's analyst (charlene-analyst for single-cell/bulk/multi-omics, bioinfo-analyst otherwise) → biostatistician → domain-expert until the audit verdict is APPROVE; ends at Gate G2.
argument-hint: "[aim-1|aim-2|all] [--data-only] [--extra \"<analysis requested by reviewer>\"]"
---

# /analyze — Gate G2

Follow the orchestration rules in `/team`. Precondition: `make gates` shows G1 PASS (plan exists, plan audit approved, tag `g1-plan-approved`, ethics fields filled) (else run `/plan-study`; for `--extra` reviewer analyses the precondition is a decision letter triage in `submission/`).

## Steps

1. **Data** (skip if `data/README.md` already documents the needed datasets with checksums): brief **`data-engineer`** with the datasets from the plan (§5), the data class from `PROJECT.md` (local human data → follow the agent's clinical-intake section), the required outputs (`data/raw/` + `MANIFEST.sha256` via `make manifest`, a passing `make verify-raw`, `data/README.md`, `data/processed/sample_sheet.tsv`, `results/qc/qc-summary.md`, environment/workflow files). If a dataset needs an access application, stop and report to the PI. With `--data-only`, stop after this step.
2. **Analysis**: brief **the aim's analyst** per aim (routing in `/team`: `charlene-analyst` for scRNA/snRNA/bulk/deconvolution/methylation+RNA/multi-omics, else `bioinfo-analyst`; if `docs/analysis-conventions.md` is still the template, `charlene-analyst` fills it first) (parallel across independent aims) with the plan section, the shared config (read-only) and its own `config/aim-<k>.yaml`, the QC summary, a distinct script-number block (aim 1 → `10–19`, aim 2 → `20–29`, …; shared preprocessing `01–09` runs first, alone), and the required outputs (`analysis/NN_aim<k>_*`, `results/tables/aim<k>_*.tsv` with full statistics, `results/summary/aim-<k>.md`, logs with versions). When all aims return, assemble `results/RESULTS-SUMMARY.md` as an index (one short section per aim, linking its summary) and apply any proposed shared-config changes yourself after checking them against the plan. Insist on: pre-specified thresholds from `config/config.yaml`, seeds, sample-level inference, and that deviations are written down.
3. **Audit**: brief **`biostatistician`** with the files to audit, the previous rounds, and the instruction to use its two-pass protocol and the `g1-plan-approved` diff; output `docs/stats-audit/round-<N>.md` (next number) with verdict.
3b. **Biology**: brief **`domain-expert`** for an annotation + results review against `docs/domain-brief.md` (positive controls recovered? implausible findings? artefacts?). A LIKELY ARTEFACT verdict goes back to the analyst and the statistician like a Major finding.
4. **Loop**: if REVISE BEFORE PROCEEDING, send the Critical/Major items to the aim's analyst (one round), then re-audit. Maximum two loops; afterwards report the unresolved items to the PI with options (change method, drop claim, collect more data). APPROVE WITH CHANGES → have the aim's analyst apply the changes, then have `biostatistician` do a short re-check and append `Changes confirmed: <date> — …` to that round's file (not a full re-audit).
5. **Gate G2** passes when `make gates` shows G2 PASS (latest verdict APPROVE, or APPROVE WITH CHANGES with the `Changes confirmed:` line). Update `PROJECT.md` (phase 4 → 5, G2 ☑, headline results in ≤ 5 lines), append the agents' notebook entries, commit (`git commit -m "G2: results audited"`), and recommend `/make-figures`.

## Report to the user

Headline results with effect sizes, CIs and n (from the summary), the audit verdict and what was fixed, the domain verdict (positive controls), deviations from the plan, negative results, and open decisions. Never present a result the audit rejected as a finding.
