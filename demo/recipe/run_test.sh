#!/bin/bash -eu

lint() {
  (
    set -eux
    pylint ${pyfiles[*]}
  )
}

typecheck() {
  (
    set -eux
    mypy --install-types ${pyfiles[*]}
  )
}

unittest() {
  (
    set -eux
    coverage run -m pytest $srcdir/test
    coverage report --fail-under 100 --show-missing
  )
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
