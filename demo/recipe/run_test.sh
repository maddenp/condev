#!/bin/bash -eu

cli() {
  echo Testing CLI programs...
  (
    set -eu
    clis=(
      heythere
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
    coverage run -m pytest -vv .
    coverage report --omit="*/tests/*"
  )
  echo OK
}

test "${CONDA_BUILD:-}" = 1 && cd ../test_files || cd $(realpath $(dirname $0)/../src)
pyfiles=( $(find . -type f -name "*.py") )
if [[ -n "${1:-}" ]]; then
  # Run single specified code-quality tool.
  $1
else
  # Run all code-quality tools.
  lint
  typecheck
  unittest
  cli
fi
