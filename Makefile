METAJSON    = recipe/meta.json
PYFILES     = $(shell find . -type f -name "*.py")
RECIPEFILES = $(addprefix $(RECIPEDIR)/,build.sh conda_build_config.yaml meta.yaml run_test.sh)
SRCDIR      = $(shell realpath ./src)
TARGETS     = env format meta package test

export PYTHONPATH := $(SRCDIR)
export RECIPEDIR  := $(shell realpath ./recipe)

.ONESHELL:
.PHONY: $(TARGETS)

all:
	$(error Valid targets are: $(TARGETS))

env:
	true # conda create ...

format:
	black -l 100 $(PYFILES) && isort --profile black $(PYFILES)

meta: $(METAJSON)

package: meta
	true # conda build ...

test:
	recipe/run_test.sh

$(METAJSON): $(RECIPEFILES)
	python -c "from devenv.meta import *; main()"
