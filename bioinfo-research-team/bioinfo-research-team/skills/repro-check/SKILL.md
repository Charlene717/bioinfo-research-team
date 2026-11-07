---
name: repro-check
description: 乾淨環境重跑全流程並準備程式碼／資料釋出 (clean-room reproduction, repository hardening, deposition plan). Use before submission or after major revisions, or when the user says「檢查可重現性」「重跑一次」「準備公開程式碼」「資料要放哪」. Delegates to reproducibility-engineer; ends at Gate G4.
argument-hint: "[--full | --quick] [--license MIT|BSD-3|Apache-2.0] [--deposit GEO,Zenodo,...]"
---

# /repro-check — Gate G4

Follow the orchestration rules in `/team`. Precondition: G3 ☑ (or the user explicitly wants an early check).

## Steps

1. Brief **`reproducibility-engineer`**: mode (`--full` rebuilds the environment and re-runs everything; `--quick` re-runs `make analysis figures` in the existing environment and cross-checks numbers), licence preference, repositories for deposition, and outputs (`docs/reproducibility-report.md`, hardened repo files, `submission/deposition/`, availability statements).
2. If the verdict is NOT REPRODUCED or discrepancies touch a reported number: brief **`bioinfo-analyst`** to fix the cause (seed, version, hidden step), then re-run the quick check; if a number changes, route it to `manuscript-writer` (text/legends) and `biostatistician` (does the conclusion hold?).
3. Have `manuscript-writer` paste the final Data and Code Availability statements into the manuscript.
4. **G4 passes** at REPRODUCED (or REPRODUCED WITH DISCREPANCIES fully explained in the report and manuscript). Update `PROJECT.md` (phase 8 → 9, G4 ☑), lab notebook; recommend `/submit`.
5. Do not create public releases, Zenodo records, or repository deposits yourself; prepare them and give the PI the exact steps.

## Report to the user

Verdict, discrepancies and causes, blocking issues, and the decisions (licence, repositories, embargo, release tag).
