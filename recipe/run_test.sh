PYFILES=( $(find $(dirname $(basename $0)) -type f -name "*.py") )

lint() {
  pylint ${PYFILES[*]}
}

typecheck() {
  mypy --install-types ${PYFILES[*]}  
}

unittest() {
  true
}

fn=${1:-} # optional single test function to run
if [[ -n "$fn" ]]; then
  $fn
else
  lint
  typecheck
  unittest
fi
