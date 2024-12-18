set -eux
# Install Python code:
python -m pip install -vv .
# Install machine code:
(cd world && make install)
# Copy files needed during test phase:
dst=../test_files
rm -fr $dst
mkdir -pv $dst
mv -v $PKG_NAME $dst/
ln -s $dst/$PKG_NAME
cp -v $SRC_DIR/pyproject.toml $dst/
