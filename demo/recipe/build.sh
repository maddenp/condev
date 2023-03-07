set -eux
# Copy tool config to support test run during packaging:
cp -v $(realpath $RECIPE_DIR/../pyproject.toml) .
# Install native code:
(cd world && make install)
# Install Python code:
python -m pip install . -vv
