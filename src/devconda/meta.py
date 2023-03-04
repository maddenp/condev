"""
Produce a list of build/host/run/test packages, for creation of a development
environment, by rendering and inspecting a conda-build recipe.
"""

import json
import os
import sys
from itertools import chain
from pathlib import Path

from conda_build import api  # type: ignore
from conda_build.metadata import MetaData  # type: ignore


def die(message: str) -> None:
    """Exit with error status."""
    msg(f"ERROR: {message}")
    sys.exit(1)


def main() -> None:
    """Main entry point"""
    recipedir = "RECIPE_DIR"
    try:
        recipedir = Path(os.environ[recipedir]).resolve()
    except KeyError:
        die(f"Export {recipedir} pointing to conda-build recipe")
    if not recipedir.is_dir():
        die(f"Are you in the right place? No '{recipedir.name}/' was found")
    msg("Getting channels")
    channels = []
    channels_file = Path(recipedir, "channels")
    if channels_file.is_file():
        with open(channels_file, "r", encoding="utf-8") as f:
            channels = list(filter(None, f.read().split("\n")))
    else:
        msg("No 'channels' file found in recipe directory, using defaults")
    msg("Rendering recipe")
    solves = api.render(recipedir, channels=channels, override_channels=True)
    if len(solves) > 1:
        msg(f"Using first of {len(solves)} solves found")
    meta = solves[0][0]
    out = json.dumps(
        {
            "name": name(meta),
            "packages": packages(meta),
            "source": source(meta),
            "version": version(meta),
        }
    )
    with open(Path(recipedir, "meta.json"), "w", encoding="utf-8") as f:  # pylint: disable=C0103
        print(out, file=f)
    meta.clean()


def msg(message: str) -> None:
    """Write a message to stderr."""
    print(f"=> {message}", file=sys.stderr)


def name(meta: MetaData) -> str:
    """The package name"""
    return meta.get_section("package")["name"]


def packages(meta: MetaData) -> list:
    """A sorted list of build/host/run/test packages"""
    rrt = meta.get_rendered_recipe_text()
    packages_set = {
        *chain.from_iterable([rrt["requirements"].get(x) or [] for x in ("build", "host", "run")]),
        *rrt["test"]["requires"],
    }
    return sorted(list(packages_set))


def source(meta: MetaData) -> str:
    """The package source directory"""
    try:
        path = meta.get_section("source")["path"]
    except Exception:  # pylint: disable=W0718
        die("Found no single source directory for this package")
    return path


def version(meta: MetaData) -> str:
    """The package version"""
    return meta.get_section("package")["version"]
