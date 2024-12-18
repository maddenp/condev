"""
Extract select metadata from a conda recipe to meta.json in the recipe directory.
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
    """
    Exit with error status.
    """
    msg(f"ERROR: {message}")
    sys.exit(1)


def get_build(meta: MetaData) -> str:
    """
    The package build, possibly including hash component.
    """
    return str(meta.info_index()["build"])


def get_buildnum(meta: MetaData) -> int:
    """
    The package build number.
    """
    return int(meta.get_section("build")["number"])


def get_channels(recipedir: Path) -> List[str]:
    """
    The list of channels from which packages can be used.
    """
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
    """
    A dict version of select package metadata.
    """
    msg("Rendering recipe")
    variants = api.render(recipedir, channels=channels, override_channels=True)
    if len(variants) > 1:
        msg(f"Using first of {len(variants)} variants found")
    meta = variants[0][0]
    meta_json = json.dumps(
        {
            "build": get_build(meta),
            "buildnum": get_buildnum(meta),
            "name": get_name(meta),
            "packages": {
                "dev": get_packages(meta, ["build", "host", "run", "test"]),
                "run": get_packages(meta, ["run"]),
            },
            "version": get_version(meta),
        },
        indent=2,
    )
    meta.clean()
    return meta_json


def get_name(meta: MetaData) -> str:
    """
    The package name.
    """
    return str(meta.get_section("package")["name"])


def get_packages(meta: MetaData, sections: list) -> list:
    """
    A sorted list of build/host/run/test packages.
    """
    rrt = meta.get_rendered_recipe_text()
    pkgs = [
        *chain.from_iterable(
            [
                rrt.get("requirements", {}).get(x, [])
                for x in sections
                if x in ("build", "host", "run")
            ]
        ),
        *(rrt.get("test", {}).get("requires", []) if "test" in sections else []),
    ]
    pkglist = []
    for pkg in pkgs:
        if " " in pkg and not any(x in pkg for x in ["<", "=", ">"]):
            pkg = re.sub(r"  *", " =", pkg)
        pkglist.append(pkg)
    return sorted(pkglist)


def get_recipedir() -> Path:
    """
    The directory containing meta.yaml.
    """
    rdname = "RECIPE_DIR"
    try:
        recipedir = Path(os.environ[rdname]).resolve()
    except KeyError:
        die(f"Export {rdname} pointing to conda-build recipe")
    if not recipedir.is_dir():
        die(f"Recipe directory '{recipedir}/' was not found")
    return recipedir


def get_version(meta: MetaData) -> str:
    """
    The package version.
    """
    return str(meta.get_section("package")["version"])


def main() -> None:
    """
    Main entry point.
    """
    recipedir = get_recipedir()
    channels = get_channels(recipedir)
    meta_json = get_meta_json(recipedir, channels)
    with open(Path(recipedir, "meta.json"), "w", encoding="utf-8") as f:
        print(meta_json, file=f)


def msg(message: str) -> None:
    """
    Write a message to stderr.
    """
    print(f"=> {message}", file=sys.stderr)


if __name__ == "__main__":
    main()  # pragma: no cover
