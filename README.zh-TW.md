# bioinfo-research-team

[English](README.md) | **繁體中文**

一個 Claude Code plugin，讓 Claude 變成一支生物資訊研究與論文發表團隊。12 位專職 AI 成員透過 12 個斜線指令工作流，從研究問題一路走到可投稿的論文。途中必須通過五道品質門檻，門檻由腳本從報告檔重新判定；原始資料則有保護機制，不會被改動。

> 每個數字都能追溯到檔案、每個引用都經過驗證、每張圖都有腳本、每個結論不超過證據。

## 內容

- **12 位成員**：文獻偵察員、領域生物學專家、研究設計師、資料工程師、以作者本人單細胞／多體學經驗打造的主力分析師、支援分析師、生物統計審核員、圖表設計師、論文撰寫者、內部審稿人、可重現性工程師、投稿策略師。
- **12 個工作流**：`/new-project`、`/lit-review`、`/plan-study`、`/analyze`、`/make-figures`、`/draft-paper`、`/review-paper`、`/repro-check`、`/submit`、`/respond-reviewers`、`/paper-pipeline`、`/team`。
- **品質門檻 G1–G5**：涵蓋計畫核可、統計審核、內部審稿、可重現、投稿清單。`make gates` 直接比對各報告檔，不靠勾選。
- **原始資料保護與 checksum 清單**：`data/raw/` 只能新增、不能改動；每次分析前都會先跑 `make verify-raw` 檢查。

完整說明：[`bioinfo-research-team/README.zh-TW.md`](bioinfo-research-team/README.zh-TW.md) · 版本紀錄：[`CHANGELOG.zh-TW.md`](bioinfo-research-team/CHANGELOG.zh-TW.md)

## 安裝

在 Claude Code 中：
```
/plugin marketplace add Charlene717/bioinfo-research-team
/plugin install bioinfo-research-team@bioinfo-research-team
```
接著打開專案資料夾，輸入 `/team` 即可開始。

其他安裝方式（用 `--plugin-dir` 直接載入，或用 `scripts/install.sh` 複製到 `~/.claude`）見[完整說明](bioinfo-research-team/README.zh-TW.md#安裝)。

## Repo 結構

```
.
├── .claude-plugin/marketplace.json   marketplace 設定（指向 ./bioinfo-research-team）
├── bioinfo-research-team/            plugin 本體：agents/、skills/、hooks/、scripts/、tests/
├── README.md · README.zh-TW.md       本頁（英文／中文）
└── .gitignore                        擋住 private/ 與本機 R 檔案，不讓它們進 repo
```

## 授權

MIT，© 張嘉容（Chia-Jung "Charlene" Chang）。見 [`LICENSE`](bioinfo-research-team/LICENSE)。
