# Reproduction entry points. Every target must run non-interactively from the project root.
# Any failing step stops the build (pipefail: a failure before `| tee` is not hidden).
SHELL := /bin/bash
.SHELLFLAGS := -eu -o pipefail -c
R      ?= Rscript
PY     ?= python

.PHONY: all dirs data manifest verify-raw analysis figures manuscript test gates clean-derived

all: data analysis figures manuscript

dirs:            ## create output folders that git does not track
	@mkdir -p results/tables results/objects results/diagnostics results/logs results/qc \
	  figures/output data/processed data/reference

data:            ## fetch + verify raw data as documented in data/README.md
	@echo ">> data: implement in workflow/ or data/scripts/ (e.g., snakemake --cores 4 data)"

manifest:        ## add checksums for NEW files in data/raw/ to MANIFEST.sha256 (never rewrites existing lines)
	@bash tools/raw-manifest.sh add

verify-raw:      ## check data/raw/ against MANIFEST.sha256 (the real guarantee that raw data are unchanged)
	@bash tools/raw-manifest.sh verify

analysis: dirs verify-raw   ## run analysis/NN_* scripts (.R, .py, .sh) in numeric order, mixed languages
	@shopt -s nullglob; scripts=(analysis/[0-9][0-9]_*.R analysis/[0-9][0-9]_*.py analysis/[0-9][0-9]_*.sh); \
	if [ $${#scripts[@]} -eq 0 ]; then echo "no analysis scripts yet"; exit 0; fi; \
	for s in $$(printf '%s\n' "$${scripts[@]}" | sort -t/ -k2,2); do \
	  name=$$(basename "$$s"); echo ">> $$s"; \
	  case "$$s" in \
	    *.R)  $(R)  "$$s" 2>&1 | tee "results/logs/$${name%.*}.log" ;; \
	    *.py) $(PY) "$$s" 2>&1 | tee "results/logs/$${name%.*}.log" ;; \
	    *.sh) bash  "$$s" 2>&1 | tee "results/logs/$${name%.*}.log" ;; \
	  esac; \
	done

figures: dirs    ## one script per figure in figures/scripts/
	@shopt -s nullglob; for s in figures/scripts/*.R; do echo ">> $$s"; $(R) "$$s"; done; \
	for s in figures/scripts/*.py; do echo ">> $$s"; $(PY) "$$s"; done

manuscript:      ## build docx from pandoc markdown
	@if [ ! -f manuscript/manuscript.md ]; then echo "no manuscript/manuscript.md yet"; exit 0; fi; \
	pandoc manuscript/manuscript.md --citeproc --bibliography refs/references.bib \
	  $$( [ -f submission/style.csl ] && echo --csl submission/style.csl ) \
	  -o manuscript/manuscript.docx; \
	echo ">> wrote manuscript/manuscript.docx"

test:            ## smoke tests (tiny subset) — any failing test fails the target
	@shopt -s nullglob; tests=(tests/*.sh); \
	if [ $${#tests[@]} -eq 0 ]; then echo "no tests yet"; exit 0; fi; \
	for t in "$${tests[@]}"; do echo ">> $$t"; bash "$$t"; done

gates:           ## recompute G1–G5 from the report files and compare with PROJECT.md
	@bash tools/check-gates.sh

clean-derived:   ## remove regenerable outputs (never touches data/raw)
	rm -rf results/objects/* results/diagnostics/* figures/output/*
