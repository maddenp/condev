META				= recipe/meta.json
PYFILES			= $(shell find . -type f -name "*.py")
RECIPEDIR		= $(shell realpath ./recipe)
RECIPEFILES = $(addprefix $(RECIPEDIR)/,build.sh conda_build_config.yaml meta.yaml run_test.sh)
TARGETS			= env format meta package test

.ONESHELL:
.PHONY: $(TARGETS)

all:
	$(error Valid targets are: $(TARGETS))

env:
	true # conda create ...

format:
	black -l 100 $(PYFILES) && isort --profile black $(PYFILES)

meta: $(META)

package: meta
	true # conda build ...

test:
	recipe/run_test.sh

$(META): $(RECIPEFILES)
	RECIPEDIR=$(RECIPEDIR) src/devenv/devmeta.py
