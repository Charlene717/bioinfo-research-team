---
name: analyze
description: 執行分析並通過統計審核 (acquire data, run the pre-specified analysis, audit statistics). Use when the plan is approved and the user wants results, says「開始分析」「跑分析」「處理資料」, or when reviewers request additional analyses. Runs data-engineer → bioinfo-analyst → biostatistician until the audit verdict is APPROVE; ends at Gate G2.
argument-hint: "[aim-1|aim-2|all] [--data-only] [--extra \"<analysis requested by reviewer>\"]"
---

# /analyze — Gate G2

Follow the orchestration rules in `/team`. Precondition: `docs/study-plan.md` exists and G1 is ☑ in `PROJECT.md` (else run `/plan-study`; for `--extra` reviewer analyses the precondition is a decision letter triage in `submission/`).

## Steps

1. **Data** (skip if `data/README.md` already documents the needed datasets with checksums): brief **`data-engineer`** with the datasets from the plan (§5), the required outputs (`data/raw/` + `MANIFEST.sha256`, `data/README.md`, `data/processed/sample_sheet.tsv`, `results/qc/qc-summary.md`, environment/workflow files). If a dataset needs an access application, stop and report to the PI. With `--data-only`, stop after this step.
2. **Analysis**: brief **`bioinfo-analyst`** per aim (parallel across independent aims) with the plan section, config path, QC summary, and the required outputs (`analysis/NN_*`, `results/tables/*.tsv` with full statistics, `results/RESULTS-SUMMARY.md`, logs with versions). Insist on: pre-specified thresholds from `config/config.yaml`, seeds, sample-level inference, and that deviations are written down.
3. **Audit**: brief **`biostatistician`** with the files to audit and the previous audit round; output `docs/stats-audit.md` round N with verdict.
4. **Loop**: if REVISE BEFORE PROCEEDING, send the Critical/Major items to `bioinfo-analyst` (one round), then re-audit. Maximum two loops; afterwards report the unresolved items to the PI with options (change method, drop claim, collect more data). APPROVE WITH CHANGES → have the analyst apply the changes and confirm with a short re-check, not a full re-audit.
5. **Gate G2** passes when the latest verdict is APPROVE (or APPROVE WITH CHANGES with changes confirmed). Update `PROJECT.md` (phase 4 → 5, G2 ☑, headline results in ≤ 5 lines), lab notebook, and recommend `/make-figures`.

## Report to the user

Headline results with effect sizes, CIs and n (from the summary), the audit verdict and what was fixed, deviations from the plan, negative results, and open decisions. Never present a result the audit rejected as a finding.
