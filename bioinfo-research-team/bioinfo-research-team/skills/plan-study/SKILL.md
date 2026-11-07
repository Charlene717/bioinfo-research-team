---
name: plan-study
description: 擬定可被審稿人接受的研究計畫 (pre-specified study plan with statistical review). Use when the user has a question or idea and wants hypotheses, aims, dataset choice, analysis plan, power reasoning and go/no-go criteria, or says「設計研究」「怎麼做這個題目」「選資料集」. Runs study-designer, then biostatistician reviews the plan; ends at Gate G1 with decisions for the PI.
argument-hint: "<research question> [--data <accession|path>] [--deadline <date>] [--venue <journal class>]"
---

# /plan-study — Gate G1

Follow the orchestration rules in `/team`.

## Steps

1. Preconditions: `refs/literature-review.md` exists (else run `/lit-review` first or, if the user insists, tell `study-designer` to proceed with explicitly provisional background).
2. Brief **`study-designer`**: the question (`$ARGUMENTS` + `PROJECT.md`), constraints (data already in hand, deadline, venue class, compute), and the required output `docs/study-plan.md` with the 12 fixed sections. Ask it to list the decisions the PI must make.
3. Brief **`biostatistician`** to audit the *plan* (not results yet): replication unit, confounding, pre-specification completeness, power argument, double-dipping risk, validation strategy. Output `docs/stats-audit.md` (round 0 — plan audit) with a verdict.
4. If the verdict is REVISE BEFORE PROCEEDING, send the Critical/Major items back to `study-designer` for one revision, then re-audit once. Do not loop more than twice; escalate to the PI instead.
5. Present the plan to the PI: question → hypotheses → primary dataset(s) with access status → primary analysis → validation → biggest risk → kill criteria. Ask for the explicit decisions (dataset choice, accepted limitations, applications to file). **Gate G1 passes only with the PI's approval**, unless the user asked for an unattended run (then record "auto-approved per user instruction" in the decision log).
6. Record the decisions in `docs/study-plan.md` §12 and `PROJECT.md` (phase 2, G1 ☑), append the lab notebook, and name the next command (`/analyze` or, if data must first be obtained, `/analyze --data-only`).
