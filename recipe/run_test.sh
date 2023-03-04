lint() {
  pylint ${pyfiles[*]}
}

typecheck() {
  mypy --install-types ${pyfiles[*]}  
}

unittest() {
  true
}

test $CONDA_BUILD == 1 && srcdir=$PWD || srcdir=$(realpath ../src)
pyfiles=( $(find $srcdir -type f -name "*.py") )
fn=${1:-} # optional single test function to run
if [[ -n "$fn" ]]; then
  $fn
else
  lint
  typecheck
  unittest
fi
