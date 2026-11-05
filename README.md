# bioinfo-research-team — 生物資訊研究與論文發表團隊

一個 Claude Code plugin，把「從研究問題到可投稿論文」拆成 10 位各有專長的 AI 成員與 11 個工作流，由主對話（你的 PI 幕僚）統籌、強制通過五道品質門檻，並保護原始資料不被改動。

> 設計原則：**每個數字都能追溯到檔案、每個引用都經過驗證、每張圖都有腳本、每個結論不超過證據。**

---

## 團隊成員（`agents/`）

| 成員 | 角色 | 主要產出 | 預設模型 |
|---|---|---|---|
| `literature-scout` | 文獻偵察員：搜尋、篩選、**逐筆驗證 DOI/PMID**、新穎性查核 | `refs/literature-review.md`、`refs/references.bib`、`refs/search-log.md` | sonnet |
| `study-designer` | 研究設計師：假說、Aims、資料集選擇、分析預先註冊、樣本數、停損條件 | `docs/study-plan.md` | opus |
| `data-engineer` | 資料工程師：下載／驗證／不可變原始資料、metadata 整理、技術 QC、環境與 workflow | `data/`、`workflow/`、`environment.yml` | sonnet |
| `bioinfo-analyst` | 生資分析師：依計畫實作分析（bulk／scRNA-seq／空間／enrichment／變異／存活／ML） | `analysis/`、`results/tables/`、`results/RESULTS-SUMMARY.md` | opus |
| `biostatistician` | 生物統計審核員：pseudoreplication、混淆、多重檢定、double-dipping、效果量與 CI | `docs/stats-audit.md`（含 verdict） | opus |
| `figure-designer` | 圖表設計師：期刊規格、色盲友善、一圖一腳本、圖說 | `figures/` | sonnet |
| `manuscript-writer` | 論文撰寫者：claim–evidence 對照表、IMRaD、可重現 Methods、cover letter、回覆審稿 | `manuscript/` | opus |
| `peer-reviewer` | 同儕審稿人（嚴格但公正的 Reviewer 2）：新穎性、嚴謹度、圖文一致、過度宣稱 | `manuscript/review-round-N.md` | opus |
| `reproducibility-engineer` | 可重現性工程師：乾淨環境重跑、版本鎖定、程式碼釋出、資料存放 | `docs/reproducibility-report.md` | sonnet |
| `submission-strategist` | 投稿策略師：選刊、掠奪性期刊篩檢、投稿清單、推薦審稿人、決定信分流 | `submission/` | sonnet |

成員之間透過**專案檔案**交接（不是互相對話），所以每一步都留下可稽核的紀錄。

## 工作流（`skills/`，以斜線指令呼叫）

```
/new-project ─▶ /lit-review ─▶ /plan-study ─[G1]─▶ /analyze ─[G2]─▶ /make-figures ─▶ /draft-paper ─[G3]─▶ /repro-check ─[G4]─▶ /submit ─[G5]
                                                                                           ▲                                   │
                                                                                           └────────── /respond-reviewers ◀────┘ （審稿意見回來）
/paper-pipeline <研究問題>   一鍵跑完整條鏈（有三個需要你拍板的 checkpoint）        /review-paper   隨時以審稿人角度審任何稿子
/team [status|roster]        看團隊名單、流程圖、目前進度與下一步
```

| 指令 | 用途 | 結束於 |
|---|---|---|
| `/team` | 總覽、現況、下一步建議 | — |
| `/new-project <name>` | 建立標準專案骨架（`PROJECT.md`、`CLAUDE.md`、`config/`、`Makefile`、lab notebook、git init） | — |
| `/lit-review <topic>` | 文獻回顧／新穎性查核／驗證 .bib | — |
| `/plan-study <question>` | 研究設計 + 統計審核計畫 | **G1 計畫核可** |
| `/analyze [aim]` | 取得資料 → 分析 → 統計審核循環 | **G2 統計審核通過** |
| `/make-figures` | 從 results/tables 產出投稿圖與圖說 | — |
| `/draft-paper [--journal]` | 選刊 → 撰寫 → 內部審稿 → 修改循環 | **G3 內審通過** |
| `/review-paper [path]` | 獨立審稿（自己的或你要審的稿子） | — |
| `/repro-check` | 乾淨環境重跑、程式碼／資料釋出準備 | **G4 可重現** |
| `/submit [--journal]` | 投稿包、最終一致性檢查、portal 步驟 | **G5 投稿清單完成** |
| `/respond-reviewers <letter>` | 分流審稿意見 → 補分析 → 回覆信與修稿 → 內部核對 | — |

五道門檻的定義寫在每個專案的 `CLAUDE.md`（由 `/new-project` 產生），主對話負責檢查，**不會默默跳過**。需要花錢、申請資料、送出投稿、上傳 preprint 的動作一律停下來交給你決定；團隊不會替你送出任何東西。

## 安裝

### 方式一：直接以 plugin 載入（最快，適合先試用）
```bash
claude --plugin-dir /path/to/bioinfo-research-team
```

### 方式二：推到 GitHub 後當 marketplace 安裝（適合長期使用、跨電腦）
本 repo 同時是 plugin 與 marketplace（見 `.claude-plugin/marketplace.json`）。推上 GitHub 後，在 Claude Code 中：
```
/plugin marketplace add <你的帳號>/bioinfo-research-team
/plugin install bioinfo-research-team@bioinfo-research-team
```

### 方式三：不用 plugin 系統，直接複製到 `.claude/`
```bash
scripts/install.sh --user                    # 安裝到 ~/.claude（所有專案可用）
scripts/install.sh --project /path/to/proj   # 只安裝到某個專案的 .claude/
scripts/install.sh --uninstall --user        # 移除
```
安裝腳本會先備份 `settings.json` 再合併 hooks。

## 快速開始

```bash
mkdir ~/research && cd ~/research
claude --plugin-dir /path/to/bioinfo-research-team
```
在 Claude Code 中：
```
/new-project tcell-exhaustion-scrna
/paper-pipeline 「在抗 PD-1 治療無反應者的腫瘤浸潤 T 細胞中，耗竭相關轉錄程式是否與臨床反應有關？」 --data GSEXXXXX
```
或分步進行：`/lit-review …` → `/plan-study …` → `/analyze` → `/make-figures` → `/draft-paper --journal "Genome Medicine"` → `/repro-check` → `/submit`。

## 專案目錄契約（由 `/new-project` 建立）

```
PROJECT.md   狀態板：問題、Aims、目前階段、門檻、決策紀錄、待你決定的事
CLAUDE.md    團隊慣例與五道門檻（主對話與所有成員都會讀）
config/      所有參數與閾值（分析腳本只從這裡讀）
data/raw/    不可變原始資料 + MANIFEST.sha256（hook 保護）   data/processed/  衍生資料、sample_sheet.tsv
docs/        study-plan.md、stats-audit.md、reproducibility-report.md
refs/        literature-review.md、references.bib（只放驗證過的）
analysis/    01_…、02_… 編號腳本    results/tables/  完整統計表（圖與文字唯一的數字來源）
figures/     scripts/ 一圖一腳本、output/、legends.md
manuscript/  manuscript.md（pandoc）、claims.md、review-round-N.md、response-to-reviewers.md
submission/  journal-shortlist.md、checklist-<journal>.md、reviewers.md、deposition/
notebook/LAB-NOTEBOOK.md   所有成員的日誌（含失敗與死路）
```

## Hooks

- **`protect-raw-data.sh`（PreToolUse）**：攔截任何對 `data/raw/` 的 Write／Edit，以及 Bash 中的 `rm`／`mv`／`sed -i`／重導向等破壞性操作；只允許 `MANIFEST*` 與 `README*`。下載（`curl -o`、`wget`）、讀取、`chmod a-w` 不受影響。解析失敗時放行（fail-open），不會卡住一般工作。
- **`session-context.sh`（SessionStart）**：只有在目前目錄是團隊專案（同時有 `PROJECT.md` 與 `CLAUDE.md`）時，才注入團隊簡報與 `PROJECT.md` 現況；其他目錄完全靜默。

## 自訂

- **換模型／力度**：編輯 `agents/<name>.md` 的 `model:`（`sonnet`／`opus`／`haiku`／`inherit`／完整 model ID）；可加 `effort: high`。審核類成員（`biostatistician`、`peer-reviewer`）建議維持較強模型。
- **改實驗室慣例**：編輯 `skills/new-project/assets/project-template/CLAUDE.md`，之後新專案都會套用。
- **改方法預設**：`agents/bioinfo-analyst.md` 的「Method defaults」段落；`agents/biostatistician.md` 的檢查清單。
- **加成員**：在 `agents/` 新增一個 `.md`（frontmatter：`name`、`description`、`tools`、`model`、`color`），並在 `skills/team/SKILL.md` 的名單加一列。
- 修改後執行 `claude plugin validate . --strict` 檢查格式。

## 注意事項

- **成本**：`/paper-pipeline` 會依序呼叫多位成員（部分為 opus），一個完整專案可能消耗可觀的 token；分步執行並善用 `--stop-after` 可控制花費。
- **網路**：`literature-scout`、`study-designer`、`submission-strategist` 需要能連到 PubMed／Europe PMC／Crossref／期刊網站。
- **不是作者**：團隊能寫出草稿、審核與重跑，但研究設計的最終責任、資料使用授權（IRB／DUA）、作者資格與投稿行為都屬於你（PI）。所有引用請在投稿前再抽查一次。
- **執行環境**：分析腳本需要本機有 R／Python 與相關套件（`environment.yml` 提供起點）；團隊不會替你安裝系統層級軟體。

## 檔案結構

```
bioinfo-research-team/
├── .claude-plugin/plugin.json · marketplace.json
├── agents/            10 位成員
├── skills/            11 個工作流（new-project 內含專案範本 assets/project-template/ 與 scripts/scaffold.sh）
├── hooks/             hooks.json · protect-raw-data.sh · session-context.sh · team-context.md
├── scripts/install.sh 非 plugin 安裝方式
├── LICENSE            MIT
└── README.md
```
