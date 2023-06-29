#!/bin/bash -eu

cli() {
  echo Testing CLI programs...
  (
    set -eu
    clis=(
      condev-meta
      condev-shell
    )
    for x in ${clis[*]}; do
      which $x
    done
  )
  echo OK
}

lint() {
  echo Running linter...
  (
    set -eu
    pylint ${pyfiles[*]}
  )
  echo OK
}

typecheck() {
  echo Running typechecker...
  (
    set -eu
    mypy --install-types --non-interactive ${pyfiles[*]}
  )
  echo OK
}

unittest() {
  echo Running unit tests...
  (
    set -eu
    testdir=$srcdir/tests
    export PYTHONPATH=$testdir
    coverage run -m pytest -v $testdir
    coverage report --omit="$testdir/*"
  )
  echo OK
}

test "${CONDA_BUILD:-}" = 1 && srcdir=$PWD || srcdir=$(realpath $(dirname $0)/../src)
pyfiles=( $(find $srcdir -type f -name "*.py") )
if [[ -n "${1:-}" ]]; then
  $1 # run single specified code-quality tool
else
  lint
  typecheck
  unittest
  cli
fi
