import json
import os
import re
from pathlib import Path

from setuptools import find_packages, setup

# Collect package metadata, etc.

recipe = os.environ.get("RECIPE_DIR", "../recipe")
metasrc = Path(recipe, "meta.json")
meta = json.loads(metasrc.read_text())
name_conda = meta["name"]
name_py = name_conda.replace("-", "_")
src = "." if os.environ.get("CONDA_BUILD") else "src"

# Define basic setup configuration.

kwargs = {
    "entry_points": {"console_scripts": ["condev-meta = %s.meta:main" % name_py]},
    "include_package_data": True,
    "name": name_conda,
    "package_dir": {"": src},
    "packages": find_packages(where=src),
    "scripts": [f"bin/condev-shell"],
    "version": meta["version"],
}

# Define dependency packages for non-devshell installs.

if not os.environ.get("CONDEV_SHELL"):
    kwargs["install_requires"] = [
        pkg.replace(" =", "==")
        for pkg in meta["packages"]["run"]
        if not re.match(r"^python .*$", pkg)
    ]

# Install.

setup(**kwargs)
