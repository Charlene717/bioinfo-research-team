---
name: new-project
description: 建立新的研究專案骨架 (scaffold a new bioinformatics research project). Use when the user wants to start a new study, says「開新專案」「建立專案」「new project」, or when another workflow (/paper-pipeline) needs a project directory that does not exist yet. Creates the standard directory contract, PROJECT.md status board, CLAUDE.md conventions, config, Makefile, environment file, lab notebook, and initialises git.
argument-hint: "<project-name> [parent-dir]"
---

# /new-project — scaffold a research project

Create a project directory that follows the team's directory contract and quality gates.

## Steps

1. Determine the project name from `$ARGUMENTS` (first token; must be alphanumeric with `._-`). If none was given, propose a short kebab-case name from the research topic and confirm with the user only if the topic is unclear.
2. Run the scaffold script (it refuses to overwrite a non-empty directory):
   ```bash
   bash "${CLAUDE_SKILL_DIR}/scripts/scaffold.sh" <project-name> [parent-dir]
   ```
3. Open `<project>/PROJECT.md` and fill in what is already known: research question, PI name/ORCID if given, target venue class, today's date. Leave unknown fields as placeholders rather than guessing.
4. Append a lab-notebook entry if you added anything beyond the template.
5. Tell the user: the path, the three files that matter (`PROJECT.md`, `CLAUDE.md`, `docs/`), and the recommended next command (`/lit-review <topic>` → `/plan-study`, or `/paper-pipeline <question>` for the full run). Remind them that `data/raw/` is write-protected by design and that `data/`, `results/objects/` are git-ignored.

## Notes

- The template lives in `${CLAUDE_SKILL_DIR}/assets/project-template/`; edit it there to change lab conventions for all future projects.
- If the user already has a project directory with data, do not scaffold on top of it: instead copy only the missing pieces (`CLAUDE.md`, `PROJECT.md`, `config/`, `notebook/`) and describe the mapping of their existing folders to the directory contract in `PROJECT.md`.
