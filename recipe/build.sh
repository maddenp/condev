set -eux
root=$(readlink -f $RECIPE_DIR/..)
# Install Python code:
python -m pip install -vv .
# Stage files needed during test phase:
dst=../test_files
rm -fr $dst
mkdir -pv $dst
mv -v $PKG_NAME $dst/
ln -s $dst/$PKG_NAME
cp -v $root/pyproject.toml $dst/
