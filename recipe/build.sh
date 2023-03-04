python setup.py install --single-version-externally-managed --record record.txt
cp -v $(realpath $RECIPEDIR/../bin/devconda-shell) $PREFIX/bin/
