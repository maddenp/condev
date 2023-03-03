PYFILES		= $(shell find . -type f -name "*.py")
RECIPEDIR = $(shell realpath ./recipe)
TARGETS		= env format meta package test

.ONESHELL:
.PHONY: $(TARGETS)

all:
	$(error Valid targets are: $(TARGETS))

env:
	true # conda create ...

format:
	black -l 100 $(PYFILES) && isort --profile black $(PYFILES)

meta:
	RECIPEDIR=$(RECIPEDIR) src/devenv/devmeta.py

package:
	true # conda build ...

test:
	recipe/run_test.sh
