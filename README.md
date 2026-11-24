# bioinfo-research-team


**English** | [繁體中文](README.zh-TW.md)

A Claude Code plugin that turns Claude into a bioinformatics research and publication team. Twelve specialist agents work from a research question to a submittable paper through twelve slash-command workflows, under five quality gates that a script recomputes from the report files. A guard keeps raw data immutable.

> Every number traces back to a file, every citation is verified, every figure has a script, and no conclusion goes beyond the evidence.

## What is inside

- **12 agents.** Literature scout, domain biologist, study designer, data engineer, a lead analyst built on the author's own single-cell / multi-omics experience, a supporting analyst, statistical auditor, figure designer, manuscript writer, internal peer reviewer, reproducibility engineer, and submission strategist.
- **12 workflows**: `/new-project`, `/lit-review`, `/plan-study`, `/analyze`, `/make-figures`, `/draft-paper`, `/review-paper`, `/repro-check`, `/submit`, `/respond-reviewers`, `/paper-pipeline`, `/team`.
- **Quality gates G1–G5.** These cover plan approval, statistical audit, internal review, reproducibility and submission checklist. `make gates` checks them against the reports instead of ticked boxes.
- **Raw-data guard and checksum manifest.** Files can be added to `data/raw/` but never changed, and `make verify-raw` checks them before every analysis.

Full documentation: [`bioinfo-research-team/README.md`](bioinfo-research-team/README.md) · Changes: [`CHANGELOG.md`](bioinfo-research-team/CHANGELOG.md)

## Install

In Claude Code:
```
/plugin marketplace add Charlene717/bioinfo-research-team
/plugin install bioinfo-research-team@bioinfo-research-team
```
Then open a project folder and type `/team`.

Other options, such as loading with `--plugin-dir` or copying into `~/.claude` with `scripts/install.sh`, are described in the [full documentation](bioinfo-research-team/README.md#installation).

## Repository layout

```
.
├── .claude-plugin/marketplace.json   marketplace entry (points to ./bioinfo-research-team)
├── bioinfo-research-team/            the plugin: agents/, skills/, hooks/, scripts/, tests/
├── README.md · README.zh-TW.md       this page
└── .gitignore                        keeps private/ and local R files out of the repository
```

## License

MIT, © Chia-Jung (Charlene) Chang. See [`LICENSE`](bioinfo-research-team/LICENSE).
