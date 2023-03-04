#!/bin/bash

lint() {
  pylint ${pyfiles[*]}
}

typecheck() {
  mypy --install-types ${pyfiles[*]}  
}

unittest() {
  true
}

test "$CONDA_BUILD" = 1 && srcdir=$PWD || srcdir=$(realpath $(dirname $0)/../src)
pyfiles=( $(find $srcdir -type f -name "*.py") )
if [[ -n "$1" ]]; then
  $1 # run single specified code-quality tool
else
  lint
  typecheck
  unittest
fi
