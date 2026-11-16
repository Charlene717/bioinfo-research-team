# private/ — 只留在本機的背景資料（git 忽略）

[English](README.md) | **繁體中文**

這裡的檔案**不會**被 commit（見 `.gitignore`），只有兩份 README 和範本是公開的。

`charlene-profile.md` 提供 `charlene-analyst` 專案層級的背景：進行中的專案與現況、合作者偏好、本機資料夾慣例、運算資源。檔案裡可能有未發表結果，所以一定不能進公開的 repo。

## 分析師從哪裡讀

`~/.claude/bioinfo-research-team/private/charlene-profile.md`

- 用 `scripts/install.sh` 安裝時，如果 `private/charlene-profile.md` 存在，會自動複製到上面的位置。
- 若改用 marketplace 安裝，要自己複製一次：
  `mkdir -p ~/.claude/bioinfo-research-team/private && cp private/charlene-profile.md ~/.claude/bioinfo-research-team/private/`

專案有變動時就更新這個檔案，分析師每次開工都會重新讀。想從頭開始寫，可以把 `charlene-profile.template.md` 複製成 `charlene-profile.md`。
