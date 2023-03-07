set -eux
cp -v $(realpath $RECIPE_DIR/../pyproject.toml) .
cp -v $(realpath $RECIPE_DIR/../bin/condev-shell) $PREFIX/bin/
python -m pip install . -vv
