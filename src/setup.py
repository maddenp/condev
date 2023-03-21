"""
Basic setuptools configuration
"""

import json
import os

from setuptools import setup  # type: ignore

with open(os.path.join(os.environ["RECIPE_DIR"], "meta.json"), "r", encoding="utf-8") as f:
    meta = json.load(f)

name_conda = meta["name"]
name_py = name_conda.replace("-", "_")

setup(
    entry_points={
        "console_scripts": [
            "condev-meta = %s.meta:main" % name_py,
        ]
    },
    name=name_conda,
    packages=[name_py],
    scripts=["bash/condev-shell"],
    version=meta["version"],
)
