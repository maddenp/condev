FILES = devmeta src/setup.py src/foo/core.py

.ONESHELL:
.PHONY: qc

qc:
	set -x
	black -l 100 $(FILES) && isort --profile black $(FILES) && pylint $(FILES) && mypy --install-types $(FILES)
