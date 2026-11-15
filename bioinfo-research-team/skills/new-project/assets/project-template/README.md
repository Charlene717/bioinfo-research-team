# {{PROJECT_NAME}}

Research project scaffolded with the **bioinfo-research-team** Claude Code plugin.

- `PROJECT.md` — status board and decision log
- `CLAUDE.md` — conventions and quality gates the AI team follows
- `docs/study-plan.md` — pre-specified study plan (created by `/plan-study`)
- Reproduce: `make all` (see `Makefile`), environment in `environment.yml`

## How to reproduce
1. `micromamba create -n {{PROJECT_NAME}} -f environment.yml && micromamba activate {{PROJECT_NAME}}`
2. `make data` (downloads per `data/README.md`), `make analysis`, `make figures`, `make manuscript`
