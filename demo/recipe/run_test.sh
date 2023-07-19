#!/bin/bash -eu

cli() {
  msg Testing CLI programs
  (
    set -eu
    clis=(
      heythere
    )
    for x in ${clis[*]}; do
      which $x
    done
  )
  msg OK
}

lint() {
  msg Running linter
  (
    set -eux
    pylint .
  )
  msg OK
}

msg() {
  echo "=> $@"
}

typecheck() {
  msg Running typechecker
  (
    set -eux
    mypy --install-types --non-interactive .
  )
  msg OK
}

unittest() {
  msg Running unit tests
  (
    set -eux
    coverage run -m pytest -vv .
    coverage report
  )
  msg OK
}

test "${CONDA_BUILD:-}" = 1 && cd ../test_files || cd $(dirname $0)/../src
msg Running in $PWD
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
