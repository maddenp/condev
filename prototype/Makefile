CHANNELS    = $(addprefix -c ,$(shell tr '\n' ' ' <$(RECIPE_DIR)/channels))
METAJSON    = recipe/meta.json
PYFILES     = $(shell find . -type f -name "*.py")
RECIPEFILES = $(addprefix $(RECIPE_DIR)/,build.sh conda_build_config.yaml meta.yaml run_test.sh)
TARGETS     = devshell env format lint meta package test typecheck unittest

export RECIPE_DIR := $(shell realpath ./recipe)

.ONESHELL:
.PHONY: $(TARGETS)

all:
	$(error Valid targets are: $(TARGETS))

devshell:
	devconda-shell

env:
	true # conda create ...

format:
	black -l 100 $(PYFILES) && isort --profile black $(PYFILES)

lint:
	recipe/run_test.sh lint

meta: $(METAJSON)

package: meta
	conda build $(CHANNELS) --error-overlinking --override-channels $(RECIPE_DIR)

test:
	recipe/run_test.sh

typecheck:
	recipe/run_test.sh typecheck

unittest:
	recipe/run_test.sh unittest

$(METAJSON): $(RECIPEFILES)
	devconda-meta
