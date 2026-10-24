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
      (set -x && which $x)
    done
  )
  msg OK
}

lint() {
  msg Running linter
  (
    set -eux
    ruff check --exclude demo/ .
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
    mypy --exclude demo/ .
  )
  msg OK
}

unittest() {
  msg Running unit tests
  (
    set -eux
    pytest --cov=condev tests/
  )
  msg OK
}

test -v CONDA_BUILD && cd ../test_files

if [[ -v 1 ]]; then # run single specified code-quality tool.
  $1
else # run all code-quality tools.
  lint
  typecheck
  unittest
  cli
fi
