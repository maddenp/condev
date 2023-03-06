set -eux
cp -v $(realpath $RECIPE_DIR/../pyproject.toml) .
python setup.py install --single-version-externally-managed --record record.txt
(cd world && make install)
