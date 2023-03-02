PYFILES = $(shell find . -type f -name "*.py")
TARGETS = format test

.ONESHELL:
.PHONY: format

all:
	$(error Valid targets are: $(TARGETS))

format:
	set -x
	black -l 100 $(PYFILES) && isort --profile black $(PYFILES)

test:
	recipe/run_test.sh
