# private/ — local-only context (git-ignored)

**English** | [繁體中文](README.zh-TW.md)

Files here are **not** committed (see `.gitignore`); only the READMEs and the template are public.

`charlene-profile.md` gives `charlene-analyst` project-specific context: ongoing projects and their status, collaborators' preferences, local folder conventions, computing resources. It may contain unpublished results, so it must stay out of the public repository.

## Where the agent reads it

`~/.claude/bioinfo-research-team/private/charlene-profile.md`

- `scripts/install.sh` copies `private/charlene-profile.md` there (if it exists) when you install.
- If you install from the marketplace instead, copy it yourself:
  `mkdir -p ~/.claude/bioinfo-research-team/private && cp private/charlene-profile.md ~/.claude/bioinfo-research-team/private/`

Update the file whenever a project changes; the agent re-reads it at the start of every task. To start fresh, copy `charlene-profile.template.md` to `charlene-profile.md`.
