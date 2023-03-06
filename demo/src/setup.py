"""
Basic setuptools configuration
"""

import json
import os

from setuptools import setup  # type: ignore

with open(os.path.join(os.environ["RECIPE_DIR"], "meta.json"), "r", encoding="utf-8") as f:
    meta = json.load(f)

name = meta["name"]

setup(
    entry_points={
        "console_scripts": [
            "hello-world = %s.core:main" % name,
        ]
    },
    name=name,
    packages=[
        name,
    ],
    version=meta["version"],
)
