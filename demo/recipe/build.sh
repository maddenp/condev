set -eux
# Install Python code:
python -m pip install -vv .
# Install machine code:
make -C world install
# Copy files needed during test phase:
dst=../test_files
rm -fr $dst
mkdir -pv $dst
mv -v $PKG_NAME $dst/
ln -s $dst/$PKG_NAME
cp -v $SRC_DIR/pyproject.toml $dst/
