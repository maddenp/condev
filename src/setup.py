"""
Basic setuptools configuration
"""

import json

from setuptools import setup  # type: ignore

with open("../recipe/meta.json", "r", encoding="utf-8") as f:
    meta = json.load(f)

setup(
    entry_points={
        "console_scripts": [
            "foo = foo.core:main",
        ]
    },
    name=meta["name"],
    version=meta["version"],
)
