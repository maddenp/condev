#!/bin/bash -eu

lint() {
  (set -x && pylint ${pyfiles[*]})
}

typecheck() {
  (set -x && mypy --install-types ${pyfiles[*]})
}

unittest() {
  (set -x && true that unittests shoudl be written) # TODO FIXME
}

test "${CONDA_BUILD:-}" = 1 && srcdir=$PWD || srcdir=$(realpath $(dirname $0)/../src)
pyfiles=( $(find $srcdir -type f -name "*.py") )
if [[ -n "${1:-}" ]]; then
  $1 # run single specified code-quality tool
else
  lint
  typecheck
  unittest
fi
