#!/bin/bash -eu

cli() {
  msg Testing CLI
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
    pytest --cov=condev -n 1 .
  )
  msg OK
}

test "${CONDA_BUILD:-}" = 1 && cd ../test_files || cd $(dirname $0)/../src
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
