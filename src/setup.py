"""
Basic setuptools configuration
"""

import json
import os

from setuptools import setup  # type: ignore

with open(os.path.join(os.environ["RECIPE_DIR"], "meta.json"), "r", encoding="utf-8") as f:
    meta = json.load(f)

pkgname = meta["name"]

setup(
    entry_points={
        "console_scripts": [
            "condev-meta = %s.meta:main" % pkgname,
        ]
    },
    name=pkgname,
    packages=[pkgname],
    version=meta["version"],
)
