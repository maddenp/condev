CHANNELS    = $(addprefix -c ,$(shell tr '\n' ' ' <$(RECIPE_DIR)/channels)) -c local
METAJSON    = $(RECIPE_DIR)/meta.json
PYFILES     = $(shell find src -type f -name "*.py")
RECIPEFILES = $(addprefix $(RECIPE_DIR)/,conda_build_config.yaml meta.yaml)
TARGETS     = devshell env format lint meta package test typecheck unittest

export RECIPE_DIR := $(shell realpath ./recipe)

spec = $(call val,name)$(1)$(call val,version)$(1)$(call val,buildnum)
val  = $(shell jq -r .$(1) $(METAJSON))

.ONESHELL:
.PHONY: $(TARGETS)

all:
	$(error Valid targets are: $(TARGETS))

devshell:
	condev-shell || true

env: meta package
	conda create -y -n $(call spec,-) $(CHANNELS) $(call spec,=)

format:
	black $(PYFILES) && isort --profile black $(PYFILES)

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
	condev-meta
