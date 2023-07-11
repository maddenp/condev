"""
Basic setuptools configuration.
"""

import json
import os

from setuptools import find_packages, setup  # type: ignore

with open(os.path.join(os.environ["RECIPE_DIR"], "meta.json"), "r", encoding="utf-8") as f:
    meta = json.load(f)

name_conda = meta["name"]
name_py = name_conda.replace("-", "_")

setup(
    entry_points={
        "console_scripts": [
            "heythere = %s.core:main" % name_py,
        ]
    },
    name=name_conda,
    packages=find_packages(
        exclude=["%s.tests" % name_py],
        include=[name_py, "%s.*" % name_py],
    ),
    version=meta["version"],
)
