# bioinfo-research-team — a bioinformatics research & publication team

**English** | [繁體中文](README.zh-TW.md)

A Claude Code plugin that splits the path from a research question to a submittable paper across 12 specialist AI agents and 12 workflows (slash commands). The main session acts as the PI's chief of staff and coordinates the team. Work must pass five quality gates, which a script recomputes from the report files instead of trusting ticked boxes, and the raw data are protected from modification.

> Design principle: **every number traces back to a file, every citation is verified, every figure has a script, and no conclusion goes beyond the evidence.**

---

## Team members (`agents/`)

| Agent | Role | Main outputs | Default model |
|---|---|---|---|
| `literature-scout` | Literature scout: searching, screening, **verifying every DOI/PMID**, novelty checks | `refs/literature-review.md`, `refs/references.bib`, `refs/search-log.md` | sonnet |
| `domain-expert` | Domain biologist: domain brief (expected cell types, markers, positive controls, tissue-specific artefacts), plan sense-check, biological plausibility of annotation and results, Discussion | `docs/domain-brief.md`, `docs/domain-review.md` | opus |
| `study-designer` | Study designer: hypotheses, aims, dataset choice, pre-registered analysis, sample size, stopping rules | `docs/study-plan.md` | opus |
| `data-engineer` | Data engineer: download / verify / immutable raw data, metadata curation, technical QC, environment and workflow | `data/`, `workflow/`, `environment.yml` | sonnet |
| `charlene-analyst` | **Lead analyst, built on Charlene's own analysis experience**: scRNA-seq / snRNA-seq, bulk, deconvolution, methylation + RNA, multi-omics integration. Rules include number–reason–record; ambient correction then two doublet methods per lane; pseudobulk with proportion vs within-population decomposition; parallel scenarios; an "as in the proposal" baseline; a hypothesis ledger | `analysis/`, `results/summary/aim-N.md` (decision log + hypothesis ledger), `docs/analysis-conventions.md` | opus |
| `bioinfo-analyst` | Supporting analyst: other data types (variants/GWAS, spatial-first, survival, ML), following `docs/analysis-conventions.md` | `analysis/`, `results/tables/`, `results/summary/aim-N.md` | opus |
| `biostatistician` | Statistical auditor: pseudoreplication, confounding, multiple testing, double-dipping, effect sizes and CIs | `docs/stats-audit/plan-round-N.md`, `round-N.md` (with verdict; every round kept) | opus |
| `figure-designer` | Figure designer: journal specs, colour-blind safe, one script per figure, legends | `figures/` | sonnet |
| `manuscript-writer` | Manuscript writer: claim–evidence table, IMRaD, reproducible Methods, cover letter, response to reviewers | `manuscript/` | opus |
| `peer-reviewer` | Internal peer reviewer (a strict but fair Reviewer 2): novelty, rigour, text–figure consistency, over-claiming | `manuscript/review-round-N.md` | opus |
| `reproducibility-engineer` | Reproducibility engineer: clean-environment rerun, version pinning, code release, data deposition | `docs/reproducibility-report.md` | sonnet |
| `submission-strategist` | Submission strategist: journal selection, predatory-journal screening, submission checklist, suggested reviewers, decision-letter triage | `submission/` | sonnet |

Agents hand work to each other through **project files** rather than by talking to each other, so every step leaves an auditable record. Shared files (`PROJECT.md`, the lab notebook, `RESULTS-SUMMARY.md`, `config/config.yaml`) are written only by the main session. Agents running in parallel each write their own files (`results/summary/aim-N.md`, `config/aim-N.yaml`, `refs/partial/`), so they cannot overwrite each other.

The biostatistician and the peer reviewer read in two passes. First they form a judgement from the tables and code alone; only then do they read the analyst's narrative. This limits anchoring on the story.

## Workflows (`skills/`, invoked as slash commands; when installed as a plugin they may appear as `/bioinfo-research-team:<command>`)

```
/new-project ─▶ /lit-review ─▶ /plan-study ─[G1]─▶ /analyze ─[G2]─▶ /make-figures ─▶ /draft-paper ─[G3]─▶ /repro-check ─[G4]─▶ /submit ─[G5]
                                                                                           ▲                                   │
                                                                                           └────────── /respond-reviewers ◀────┘ (reviews come back)
/paper-pipeline <question>   run the whole chain (three checkpoints wait for your decision)   /review-paper   review any manuscript as a referee
/team [status|roster]        team roster, flow chart, current progress and next step
```

| Command | Purpose | Ends at |
|---|---|---|
| `/team` | Overview, current status, suggested next step | — |
| `/new-project <name>` | Create the standard project scaffold (`PROJECT.md`, `CLAUDE.md`, `config/`, `Makefile`, lab notebook, git init) | — |
| `/lit-review <topic>` | Literature review / novelty check / `.bib` verification | — |
| `/plan-study <question>` | Study design + statistical audit of the plan | **G1 plan approved** |
| `/analyze [aim]` | Data acquisition → analysis → statistical-audit loop | **G2 results audited** |
| `/make-figures` | Publication figures and legends from `results/tables` | — |
| `/draft-paper [--journal]` | Journal choice → drafting → internal review → revision loop | **G3 internal review passed** |
| `/review-paper [path]` | Independent review (of your own manuscript or one you are refereeing) | — |
| `/repro-check` | Clean-environment rerun, code / data release preparation | **G4 reproduced** |
| `/submit [--journal]` | Submission package, final consistency checks, portal steps | **G5 submission checklist complete** |
| `/respond-reviewers <letter>` | Triage reviewer comments → extra analyses → response letter and revision → internal check | — |
| `/paper-pipeline <question>` | The whole chain in one command, stopping at three checkpoints (`--stop-after`, `--unattended`) | per `--stop-after` |

Each project's `CLAUDE.md` (created by `/new-project`) defines the five gates, and the main session enforces them; **gates are never skipped silently**. `make gates` (`tools/check-gates.sh`) recomputes G1–G5 from the `Verdict:` / `Recommendation:` lines of the reports and compares the result with the ☑ marks in `PROJECT.md`. The SessionStart hook also shows this line every time the project is opened.

| Gate | When the script reports PASS |
|---|---|
| G1 | `docs/study-plan.md` exists; the latest `plan-round-N.md` is APPROVE; `PROJECT.md` has the data class and IRB filled in; the git tag `g1-plan-approved` was created after PI approval (later changes to the plan or config trigger a reminder to check the decision log) |
| G2 | The latest `docs/stats-audit/round-N.md` is APPROVE, or APPROVE WITH CHANGES with a `Changes confirmed:` line |
| G3 | The latest `manuscript/review-round-N.md` is ACCEPT, or MINOR REVISION with a `Minor points addressed:` line |
| G4 | `docs/reproducibility-report.md` is REPRODUCED, or WITH DISCREPANCIES with a `Discrepancies explained:` line |
| G5 | Every checklist item is ticked except `(PI to supply)` ones, and the decision log has `G5 final files approved` |

Anything that costs money, requests data access, submits a manuscript, or posts a preprint stops and waits for your decision. The team never submits anything on your behalf.

## Installation

### Option 1: load as a plugin directly (fastest; good for trying it out)
```bash
claude --plugin-dir /path/to/bioinfo-research-team/bioinfo-research-team   # the folder that contains .claude-plugin/plugin.json
```

### Option 2: install from the GitHub marketplace (for long-term use across computers)
The repository root has `.claude-plugin/marketplace.json`, which points to this folder. In Claude Code:
```
/plugin marketplace add Charlene717/bioinfo-research-team
/plugin install bioinfo-research-team@bioinfo-research-team
```

### Option 3: copy into `.claude/` without the plugin system
```bash
scripts/install.sh --user                    # install into ~/.claude (available in every project)
scripts/install.sh --project /path/to/proj   # install into one project's .claude/
scripts/install.sh --uninstall --user        # remove
```
The installer backs up `settings.json` before merging the hooks.

## Quick start

```bash
mkdir ~/research && cd ~/research
claude --plugin-dir /path/to/bioinfo-research-team/bioinfo-research-team   # or just run claude after Option 2
```
In Claude Code:
```
/new-project tcell-exhaustion-scrna
/paper-pipeline "In tumour-infiltrating T cells of anti-PD-1 non-responders, is the exhaustion transcriptional programme associated with clinical response?" --data GSEXXXXX
```
Or step by step: `/lit-review …` → `/plan-study …` → `/analyze` → `/make-figures` → `/draft-paper --journal "Genome Medicine"` → `/repro-check` → `/submit`.

## Project directory contract (created by `/new-project`)

```
PROJECT.md   status board: question, aims, current phase, gates, decision log, decisions awaiting you
CLAUDE.md    team conventions and the five gates (read by the main session and every agent)
config/      all parameters and thresholds (analysis scripts read only from here)
data/raw/    immutable raw data + MANIFEST.sha256 (hook-protected; make manifest / make verify-raw)   data/processed/  derived data, sample_sheet.tsv (these two small files are committed)
docs/        study-plan.md, analysis-conventions.md, domain-brief.md, domain-review.md, reproducibility-report.md
docs/stats-audit/  plan-round-N.md (plan audits), round-N.md (results audits); earlier rounds never overwritten
refs/        literature-review.md, references.bib (verified entries only)
analysis/    numbered scripts 01_…, 02_… (R and Python run together in numeric order)    results/tables/  full statistics tables (the only source of numbers for figures and text)
results/summary/aim-N.md  per-aim results narrative; RESULTS-SUMMARY.md is the index assembled by the main session
tools/       check-gates.sh, raw-manifest.sh
figures/     scripts/ one script per figure, output/, legends.md
manuscript/  manuscript.md (pandoc), claims.md, review-round-N.md, response-to-reviewers.md
submission/  journal-shortlist.md, checklist-<journal>.md, reviewers.md, deposition/
notebook/LAB-NOTEBOOK.md   everyone's log, dead ends included (agents return entries; the main session writes them)
```

## Hooks

- **`protect-raw-data.sh` → `protect_raw_data.py` (PreToolUse)**: files can be *added* to `data/raw/` but never *changed*.
  - Blocked:
    - Write / Edit into `data/raw/` (except `MANIFEST*` and `README*`).
    - `rm`; `gzip` / `gunzip` without `-c` / `-k`; `sed -i`; `perl -i`; `truncate`; `find -delete` / `-exec rm`.
    - `mv` out of `data/raw`; `rsync --delete`; `chmod` that makes files writable.
    - `cp`, `>`, `>>`, `tee`, `wget -O` or `curl -o` that would overwrite an existing file.
    - `tar -x` without `--skip-old-files`; `unzip` without `-n`.
    - `python -c` / `Rscript -e` containing write or delete calls.
  - It tracks `cd`, so `cd data/raw && rm x` is blocked too.
  - Allowed: downloads to new files (`curl -o`, `wget -O`, `> new-file`), `cp -n`, `rsync --ignore-existing`, `zcat`, `gunzip -c … > data/processed/…`, `chmod a-w`, and all reads.
  - The JSON payload arrives on stdin, so large writes cannot disable the hook. A command that mentions `data/raw` but cannot be parsed is blocked (fail-closed); everything else fails open.
  - Limitation: scripts run from files (`python foo.py`) are not inspected. The real guarantee is `make verify-raw` (`sha256sum -c`), which `make analysis` runs first.
  - Regression tests: `python3 tests/test_protect_raw_data.py` (53 cases).
- **`session-context.sh` (SessionStart)**: when, and only when, the current directory is a team project (it has both `PROJECT.md` and `CLAUDE.md`), it injects the team briefing, the current `PROJECT.md`, and **the gate status recomputed from the files**. It stays silent everywhere else.

## Customisation

- **Models / effort**: edit `model:` in `agents/<name>.md` (`sonnet` / `opus` / `haiku` / `inherit` / a full model ID); you can add `effort: high`. Keep a strong model for the auditors (`biostatistician`, `peer-reviewer`).
- **Lab conventions**: edit `skills/new-project/assets/project-template/CLAUDE.md`; every new project picks them up.
- **Method defaults**:
  - `agents/charlene-analyst.md` holds the lead analyst's practices.
  - The project template's `docs/analysis-conventions.md` is shared by both analysts.
  - `agents/bioinfo-analyst.md` has a "Method defaults" section.
  - `agents/biostatistician.md` has the audit checklist.
- **The lead analyst's private context**: ongoing projects, collaborators' preferences, unpublished results, local paths and computer specs live in `private/charlene-profile.md`.
  - The file is git-ignored and never reaches GitHub.
  - `scripts/install.sh` copies it to `~/.claude/bioinfo-research-team/private/`, and `charlene-analyst` reads it at the start of every task.
  - With a marketplace install, copy it once by hand (see [`private/README.md`](private/README.md)).
- **Adding an agent**: add a `.md` file to `agents/` (frontmatter: `name`, `description`, `tools`, `model`, `color`), add a row to the roster in `skills/team/SKILL.md`, and update both language versions of this README.
- **Auditors on a different model**: for more diverse viewpoints, set the `model:` of `peer-reviewer` or `biostatistician` to a model different from `bioinfo-analyst` / `manuscript-writer`.
- **Local clinical data**: set Data class to `local human` in `PROJECT.md`. G1 then requires an IRB number, `data-engineer` follows its "Local / clinical data intake" procedure (de-identification check), and no agent sends sample-level data to web searches.
- After changes, run `claude plugin validate . --strict` to check the format and `python3 tests/test_protect_raw_data.py` to check the hook.

## Notes

- **Cost**: `/paper-pipeline` calls many agents in turn (some on opus), so a full project can use a substantial number of tokens. Running step by step and using `--stop-after` keeps spending under control.
- **Network**: `literature-scout`, `study-designer` and `submission-strategist` need access to PubMed / Europe PMC / Crossref / journal websites.
- **Not an author**: the team drafts, audits and reruns, but final responsibility for the study design, data-use authorisation (IRB / DUA), authorship and submission belongs to you (the PI). Spot-check every citation again before submitting.
- **Runtime**: analysis scripts need R / Python and the relevant packages on your machine (`environment.yml` is a starting point). The team does not install system-level software for you.

## File layout

```
bioinfo-research-team/
├── .claude-plugin/plugin.json      (marketplace.json is at the repository root)
├── agents/            12 agents
├── skills/            12 workflows (new-project contains the project template assets/project-template/ and scripts/scaffold.sh)
├── hooks/             hooks.json · protect-raw-data.sh · protect_raw_data.py · session-context.sh · team-context.md
├── tests/             test_protect_raw_data.py (hook regression tests)
├── private/           local-only files (git-ignored; only the READMEs and the template are public)
├── scripts/install.sh install without the plugin system
├── CHANGELOG.md · CHANGELOG.zh-TW.md
├── LICENSE            MIT
└── README.md (English) · README.zh-TW.md (Chinese)
```
