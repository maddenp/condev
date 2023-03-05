"""
Produce a list of build/host/run/test packages, for creation of a development
environment, by rendering and inspecting a conda-build recipe.
"""

import json
import os
import re
import sys
from itertools import chain
from pathlib import Path
from typing import List

from conda_build import api  # type: ignore
from conda_build.metadata import MetaData  # type: ignore


def die(message: str) -> None:
    """Exit with error status."""
    msg(f"ERROR: {message}")
    sys.exit(1)


def get_channels(recipedir: Path) -> List[str]:
    """The list of channels from which packages can be used"""
    msg("Getting channels")
    channels = []
    channels_file = Path(recipedir, "channels")
    if channels_file.is_file():
        with open(channels_file, "r", encoding="utf-8") as f:
            channels = list(filter(None, f.read().split("\n")))
    else:
        msg("No 'channels' file found in recipe directory, using defaults")
    channels.append("local")
    return channels


def get_meta_json(recipedir: Path, channels: List[str]) -> str:
    """A dict version of select package metadata"""
    msg("Rendering recipe")
    solves = api.render(recipedir, channels=channels, override_channels=True)
    if len(solves) > 1:
        msg(f"Using first of {len(solves)} solves found")
    meta = solves[0][0]
    meta_json = json.dumps(
        {
            "name": get_name(meta),
            "packages": get_packages(meta),
            "source": get_source(meta),
            "version": get_version(meta),
        }
    )
    meta.clean()
    return meta_json


def get_name(meta: MetaData) -> str:
    """The package name"""
    return meta.get_section("package")["name"]


def get_packages(meta: MetaData) -> list:
    """A sorted list of build/host/run/test packages"""
    rrt = meta.get_rendered_recipe_text()
    pkglist = []
    for pkg in {
        *chain.from_iterable([rrt["requirements"].get(x) or [] for x in ("build", "host", "run")]),
        *rrt["test"]["requires"],
    }:
        if " " in pkg and not any(x in pkg for x in ["<", "=", ">"]):
            pkg = re.sub(r"  *", " =", pkg)
        pkglist.append(pkg)
    return sorted(pkglist)


def get_recipedir() -> Path:
    """The directory containing meta.yaml"""
    rdname = "RECIPE_DIR"
    try:
        recipedir = Path(os.environ[rdname]).resolve()
    except KeyError:
        die(f"Export {rdname} pointing to conda-build recipe")
    if not recipedir.is_dir():
        die(f"Recipe directory '{recipedir}/' was not found")
    return recipedir


def get_source(meta: MetaData) -> str:
    """The package source directory"""
    try:
        path = meta.get_section("source")["path"]
    except Exception:  # pylint: disable=W0718
        die("Found no single source directory for this package")
    return path


def get_version(meta: MetaData) -> str:
    """The package version"""
    return meta.get_section("package")["version"]


def main() -> None:
    """Main entry point"""
    recipedir = get_recipedir()
    channels = get_channels(recipedir)
    meta_json = get_meta_json(recipedir, channels)
    with open(Path(recipedir, "meta.json"), "w", encoding="utf-8") as f:
        print(meta_json, file=f)


def msg(message: str) -> None:
    """Write a message to stderr."""
    print(f"=> {message}", file=sys.stderr)
