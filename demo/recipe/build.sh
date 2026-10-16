set -eux
root=$(readlink -f $RECIPE_DIR/..)
# Install Python code:
cp -v $root/setup.py .
python -m pip install -vv .
# Install machine code:
make -C world install
# Stage files needed during test phase:
dst=../test_files
rm -fr $dst
mkdir -pv $dst
mv -v $PKG_NAME $dst/
ln -sv $dst/$PKG_NAME
cp -v $root/pyproject.toml $dst/
