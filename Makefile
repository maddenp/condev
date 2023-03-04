CHANNELS    = $(addprefix -c ,$(shell tr '\n' ' ' <$(RECIPE_DIR)/channels))
METAJSON    = recipe/meta.json
PYFILES     = $(shell find . -type f -name "*.py")
RECIPEFILES = $(addprefix $(RECIPE_DIR)/,build.sh conda_build_config.yaml meta.yaml run_test.sh)
TARGETS     = env format meta package test

export RECIPE_DIR := $(shell realpath ./recipe)

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
	conda build $(CHANNELS) --error-overlinking --override-channels $(RECIPE_DIR)

test:
	recipe/run_test.sh

$(METAJSON): $(RECIPEFILES)
	export PYTHONPATH=$(shell realpath ./src)
	python -c "from devconda.meta import *; main()"
