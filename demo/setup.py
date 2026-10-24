import json
import os
import re
from pathlib import Path

from setuptools import find_packages, setup

# Collect package metadata, etc.

recipe = os.environ.get("RECIPE_DIR", "recipe")
metasrc = Path(recipe, "meta.json")
meta = json.loads(metasrc.read_text())
name_conda = meta["name"]
name_py = name_conda.replace("-", "_")
src = "." if os.environ.get("CONDA_BUILD") else "src"

# Define basic setup configuration.

kwargs = {
    "entry_points": {"console_scripts": ["heythere = %s.core:main" % name_py]},
    "include_package_data": True,
    "name": name_conda,
    "package_dir": {"": src},
    "packages": find_packages(where=src),
    "version": meta["version"],
}

# Define dependency packages for non-devshell installs.

do_not_install = ["python"]

if not os.environ.get("CONDEV_SHELL"):
    kwargs["install_requires"] = [
        pkg.replace(" ==", "==")
        for pkg in meta["packages"]["run"]
        if not any(re.match(rf"^{x}.*$", pkg) for x in do_not_install)
    ]

# Install.

setup(**kwargs)
