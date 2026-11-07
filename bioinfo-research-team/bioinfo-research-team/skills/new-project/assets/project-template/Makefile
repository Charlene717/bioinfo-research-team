# Reproduction entry points. Every target must run non-interactively from the project root.
SHELL := /bin/bash
R      ?= Rscript
PY     ?= python

.PHONY: all data analysis figures manuscript test clean-derived

all: data analysis figures manuscript

data:            ## fetch + verify raw data as documented in data/README.md
	@echo ">> data: implement in workflow/ or data/scripts/ (e.g., snakemake --cores 4 data)"

analysis:        ## run numbered scripts in analysis/ in order
	@set -e; for s in $$(ls analysis/[0-9][0-9]_*.R 2>/dev/null); do echo ">> $$s"; $(R) $$s 2>&1 | tee results/logs/$$(basename $$s .R).log; done
	@set -e; for s in $$(ls analysis/[0-9][0-9]_*.py 2>/dev/null); do echo ">> $$s"; $(PY) $$s 2>&1 | tee results/logs/$$(basename $$s .py).log; done

figures:         ## one script per figure in figures/scripts/
	@set -e; for s in $$(ls figures/scripts/*.R 2>/dev/null); do echo ">> $$s"; $(R) $$s; done
	@set -e; for s in $$(ls figures/scripts/*.py 2>/dev/null); do echo ">> $$s"; $(PY) $$s; done

manuscript:      ## build docx (and pdf if a LaTeX engine exists) from pandoc markdown
	@test -f manuscript/manuscript.md || { echo "no manuscript/manuscript.md yet"; exit 0; }
	pandoc manuscript/manuscript.md --citeproc --bibliography refs/references.bib \
	  $$( [ -f submission/style.csl ] && echo --csl submission/style.csl ) \
	  -o manuscript/manuscript.docx
	@echo ">> wrote manuscript/manuscript.docx"

test:            ## smoke tests (tiny subset) — see tests/
	@ls tests/*.sh >/dev/null 2>&1 && for t in tests/*.sh; do bash $$t; done || echo "no tests yet"

clean-derived:   ## remove regenerable outputs (never touches data/raw)
	rm -rf results/objects/* results/diagnostics/* figures/output/*
