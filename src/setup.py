"""
Basic setuptools configuration
"""

import json
import os

from setuptools import setup  # type: ignore

with open(os.path.join(os.environ["RECIPE_DIR"], "meta.json"), "r", encoding="utf-8") as f:
    meta = json.load(f)

setup(
    entry_points={
        "console_scripts": [
            "devconda-meta = %s.meta:main" % meta["name"],
        ]
    },
    name=meta["name"],
    packages=[
        meta["name"],
    ],
    version=meta["version"],
)
