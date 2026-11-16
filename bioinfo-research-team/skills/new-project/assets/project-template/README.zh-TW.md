# {{PROJECT_NAME}}

[English](README.md) | **繁體中文**

以 **bioinfo-research-team** Claude Code plugin 建立的研究專案。

- `PROJECT.md`：狀態板與決策紀錄
- `CLAUDE.md`：AI 團隊遵守的慣例與品質門檻
- `docs/study-plan.md`：預先註冊的研究計畫（由 `/plan-study` 產生）
- `docs/analysis-conventions.md`：所有分析師都要遵守的分析慣例
- 重現：`make all`（見 `Makefile`）；環境設定在 `environment.yml`；門檻狀態：`make gates`

## 如何重現
1. `micromamba create -n {{PROJECT_NAME}} -f environment.yml && micromamba activate {{PROJECT_NAME}}`
2. `make data`（依 `data/README.md` 下載），接著 `make verify-raw`、`make analysis`、`make figures`、`make manuscript`
