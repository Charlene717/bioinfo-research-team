---
name: plan-study
description: 擬定可被審稿人接受的研究計畫 (pre-specified study plan with statistical review). Use when the user has a question or idea and wants hypotheses, aims, dataset choice, analysis plan, power reasoning and go/no-go criteria, or says「設計研究」「怎麼做這個題目」「選資料集」. Runs domain-expert (domain brief) and study-designer, then biostatistician and domain-expert review the plan; ends at Gate G1 with decisions for the PI.
argument-hint: "<research question> [--data <accession|path>] [--deadline <date>] [--venue <journal class>]"
---

# /plan-study — Gate G1

Follow the orchestration rules in `/team`.

## Steps

1. Preconditions: `refs/literature-review.md` exists (else run `/lit-review` first or, if the user insists, tell `study-designer` to proceed with explicitly provisional background). Make sure `PROJECT.md` has `Data class` and `IRB / ethics approval` filled in; ask the PI if not.
1b. **Domain brief**: if `docs/domain-brief.md` is still the empty template, brief **`domain-expert`** to fill it (ask the PI for anything only they know: cohort, tissue handling, clinical definitions).
2. Brief **`study-designer`**: the question (`$ARGUMENTS` + `PROJECT.md`), constraints (data already in hand, deadline, venue class, compute), and the required output `docs/study-plan.md` with the 12 fixed sections. Ask it to list the decisions the PI must make.
3. In parallel: brief **`biostatistician`** to audit the *plan* (not results yet): replication unit, confounding, pre-specification completeness, power argument, double-dipping risk, validation strategy — output `docs/stats-audit/plan-round-1.md` with a verdict; and brief **`domain-expert`** for a *plan review* (biological meaning, clinically coherent groups, positive controls to pre-specify) — appended to `docs/domain-review.md`.
4. If the statistical verdict is REVISE BEFORE PROCEEDING (or the domain verdict is LIKELY ARTEFACT / serious CONCERNS), send the Critical/Major items back to `study-designer` for one revision, then re-audit once as the next plan round (`plan-round-2.md`; earlier rounds are never edited). Do not loop more than twice; escalate to the PI instead.
5. Present the plan to the PI: question → hypotheses → primary dataset(s) with access status → primary analysis → validation → biggest risk → kill criteria. Ask for the explicit decisions (dataset choice, accepted limitations, applications to file). **Gate G1 passes only with the PI's approval**, unless the user asked for an unattended run (then record "auto-approved per user instruction" in the decision log) — never for local human / clinical or controlled-access data.
6. Record the decisions in `docs/study-plan.md` §12 and `PROJECT.md` (phase 2), then **freeze the plan**: `git add docs/study-plan.md docs/domain-brief.md config/ docs/stats-audit/ && git commit -m "G1: study plan approved by PI" && git tag g1-plan-approved` (if the project is not under git, run `git init` first). Run `make gates`; set G1 ☑ only when it shows PASS. Append the agents' notebook entries, and name the next command (`/analyze` or, if data must first be obtained, `/analyze --data-only`).
7. **Later changes to the plan** (pivot, reviewer-requested analysis): edit the plan, add a dated decision-log row with the reason and whether results had been seen, get the PI's approval, then commit and tag `g1-plan-amend-<n>`. Never move or delete `g1-plan-approved`.
