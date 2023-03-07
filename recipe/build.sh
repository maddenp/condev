set -eux
cp -v $(realpath $RECIPE_DIR/../pyproject.toml) .
python -m pip install . -vv
