# 版本紀錄

[English](CHANGELOG.md) | **繁體中文**

## 0.3.1 — 2026-11-15

### 變更
- **說明文件雙語化。** 所有介紹頁預設英文，另有繁體中文版（`*.zh-TW.md`），頁首有「English | 繁體中文」切換連結。範圍包括 repo 首頁、plugin README、本版本紀錄、`private/README`，以及 `/new-project` 建立的每個新專案的 README。
- **marketplace 設定移到 repo 根目錄**（`.claude-plugin/marketplace.json`，`source: ./bioinfo-research-team`），`/plugin marketplace add Charlene717/bioinfo-research-team` 才能正常運作。
- 根目錄 `.gitignore` 也擋住 `**/private/*`（README 與範本除外），從 repo 根目錄 commit 時不會誤上傳私檔。
- 移除巢狀的 v0.1 舊 skills 副本（`bioinfo-research-team/bioinfo-research-team/skills/`）。
- README 修正：指令表補上 `/paper-pipeline`；門檻表和後面段落分開；安裝指令改用實際的 repo 名稱。

## 0.3.0 — 2026-11-13

### 新增
- **新成員 `charlene-analyst`（專屬生資分析師，主力）。** 依 Charlene 本人的分析經驗工作，是 scRNA-seq／snRNA-seq、bulk RNA-seq、deconvolution、甲基化＋RNA、多體學整合的預設分析師。涵蓋：
  - 數字－理由－紀錄，以及決策紀錄；
  - 每個 capture lane 先做 ambient 校正，再用兩種 doublet 方法；
  - pseudobulk 設每個樣本的最少細胞數，並把變化拆成族群比例位移和族群內變化；
  - 文獻挑選的候選基因要透明交代；新亞群要和既有命名比對；
  - 檢查解離壓力假象；
  - 平行的敏感度情境，包括純度情境和可疑樣本；
  - 先跑一版完全照計畫書的分析；
  - 假說帳本（支持／矛盾／原因／怎麼區分）；
  - 事先估算記憶體、改檔前先備份、新版本不覆蓋舊版。
- **專案範本新增 `docs/analysis-conventions.md`**：由 `charlene-analyst` 維護，所有分析師都要遵守。
- **`private/`**：只在本機、被 git 忽略的背景資料。`charlene-profile.md` 存放進行中的專案、合作者偏好、未發表結果、本機路徑與運算資源。`install.sh` 會把它複製到 `~/.claude/bioinfo-research-team/private/`；分析師每次開工會先讀，但不會複製進專案檔案或網路搜尋。

### 變更
- `bioinfo-analyst` 改為支援角色，負責其他資料類型（變異／GWAS、以空間為主、只做存活、只做 ML），並遵守 `docs/analysis-conventions.md`。
- `/team` 新增分析師分派規則。`/analyze`、`/respond-reviewers`、`/draft-paper`、`/repro-check`、`/paper-pipeline` 改為交給「該 aim 的分析師」。

## 0.2.0 — 2026-11-12

### 修正
- **原始資料保護 hook 重寫**（`hooks/protect_raw_data.py`）。現在會擋：原地執行的 `gzip`／`gunzip`／`bgzip`／`xz`、`find -delete`／`-exec rm`、會覆蓋檔案的 `cp`／`mv`／`rsync`／`tar`／`unzip`、`rsync --delete`、讓檔案變可寫的 `chmod`、含寫入的 `python -c`／`Rscript -e`，以及 `cd data/raw && rm …`（hook 會追蹤 `cd`）。下載新檔到 `data/raw/` 仍然允許，包括 `curl … > 新檔`（舊版會擋這個，卻放行 `wget -O`）。指令提到 `data/raw` 但無法解析時一律阻擋。
- **大檔寫入不再讓 hook 失效。** 舊版把 JSON 當成命令列參數傳入，超過 128 KB 就會出現 `Argument list too long`（exit 126），寫入直接通過、沒被檢查。現在改由 stdin 傳入。
- **`.gitignore` 改為 commit 驗證資料所需的檔案**：`data/raw/MANIFEST*`、`data/raw/README*`、`data/processed/sample_sheet.tsv`、`metadata-mapping.md`，以及被忽略資料夾的 `.gitkeep`。
- **Makefile**：
  - 使用 `pipefail`，`| tee` 前面的腳本失敗會中斷 build。
  - `analysis/NN_*` 依編號順序執行，R、Python、shell 腳本混在一起排序。舊版會先跑完所有 R 再跑所有 Python。
  - 測試失敗時 `make test` 會報錯。
  - 新增 `dirs` 目標，建立 git 不追蹤的輸出資料夾。
- **`biostatistician` 與 `peer-reviewer` 有了 Write 工具**，但只能寫自己的報告檔。舊版只能透過 Bash heredoc 寫檔。
- **平行執行的成員不再寫同一個檔案。**
  - 每位分析師只負責一個 aim：`results/summary/aim-<k>.md`、`config/aim-<k>.yaml`，以及自己的腳本編號區段。
  - 文獻偵察員寫到 `refs/partial/`，最後由一位負責合併。
  - `PROJECT.md`、lab notebook、`RESULTS-SUMMARY.md` 和共用 config 只由主對話寫入；成員改為回傳 `NOTEBOOK ENTRY` 區塊，不直接改 notebook。
- **統計審核逐輪保存**：`docs/stats-audit/plan-round-N.md` 與 `docs/stats-audit/round-N.md`，舊輪不會被修改。
- README 和 manifest 的數量改成和 plugin 實際內容一致。

### 新增
- **`make gates`／`tools/check-gates.sh`**：從報告檔重新判定 G1–G5，並和 `PROJECT.md` 的 ☑ 比對；`--strict` 在不一致時 exit 1。SessionStart hook 會顯示重新判定的門檻狀態。
- **`make manifest`／`make verify-raw`（`tools/raw-manifest.sh`）。** `make manifest` 只為還沒列入的新檔加 checksum；`make verify-raw` 會列出被改動、遺失或未列入的檔案。`make analysis` 一開始就先跑 `verify-raw`。
- **可驗證的預先註冊。**
  - PI 在 G1 核可計畫時，commit 並打 tag `g1-plan-approved`。
  - 之後的修訂打 tag `g1-plan-amend-<n>`。
  - 統計審核員每次審結果，都會拿計畫和 config 跟 tag 比對；主要分析若有未記錄的修改，列為 Critical。
- **機器可讀的門檻行**：`Changes confirmed:`、`Minor points addressed:`、`Discrepancies explained:`；G5 則是 decision log 中的 `G5 final files approved`。
- **兩段式（先盲讀）審查**：`biostatistician` 與 `peer-reviewer` 先只看表格和程式碼，再讀敘事，並指出敘事超出證據的地方。
- **新成員 `domain-expert`（領域生物學專家）。**
  - 撰寫 `docs/domain-brief.md`：預期細胞類型、marker、positive controls、組織特有假象。
  - 在 `docs/domain-review.md` 審查計畫、annotation 與結果、Discussion。
  - 已接進 `/plan-study`、`/analyze`、`/draft-paper`、`/respond-reviewers`、`/review-paper`、`/paper-pipeline`。
- **本地臨床資料的處理。**
  - `PROJECT.md` 新增 `Data class` 與 `IRB / ethics approval` 欄位，G1 要求必填。
  - `data-engineer` 新增資料接收流程：去識別化檢查、編碼過的樣本 ID、依計畫書規定存放。
  - 樣本層級的資料不會送到網路搜尋。
  - `--unattended` 不會自動核可人體或受控存取資料的 G1。
- `tests/test_protect_raw_data.py`：hook 的 53 個回歸測試情境。
- `install.sh --uninstall` 會在備份後，從 `settings.json` 移除 hook 設定。
