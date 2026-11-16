# {{PROJECT_NAME}}

**English** | [繁體中文](README.zh-TW.md)

Research project scaffolded with the **bioinfo-research-team** Claude Code plugin.

- `PROJECT.md` — status board and decision log
- `CLAUDE.md` — conventions and quality gates the AI team follows
- `docs/study-plan.md` — pre-specified study plan (created by `/plan-study`)
- `docs/analysis-conventions.md` — analysis conventions every analyst follows
- Reproduce: `make all` (see `Makefile`); environment in `environment.yml`; gate status: `make gates`

## How to reproduce
1. `micromamba create -n {{PROJECT_NAME}} -f environment.yml && micromamba activate {{PROJECT_NAME}}`
2. `make data` (downloads per `data/README.md`), then `make verify-raw`, `make analysis`, `make figures`, `make manuscript`
