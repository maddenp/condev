# condev

[![ci](https://github.com/maddenp/condev/actions/workflows/ci.yml/badge.svg)](https://github.com/maddenp/condev/actions/workflows/ci.yml)

Creates conda development shells and provides related convenience tooling.

## Getting Started

The following subsection provides instructions on obtaining, installing, and activating conda. The two remaining subsections describe two methods for installing `condev` and its required tools into a conda installation: 1. Using a prebuilt package, or 2. Bootstrapping.

### Installing conda

`conda` itself may be provided by a [Miniforge](https://github.com/conda-forge/miniforge#miniforge3), [Miniconda](https://docs.conda.io/en/latest/miniconda.html), or [Anaconda](https://www.anaconda.com/) installation. Prefer Miniforge to Miniconda to Anaconda. Miniforge is equivalent to Miniconda except that it defaults to using the [conda-forge](https://conda-forge.org/) package collection: A community-curated collection of high-quality packages for which all recipes are available for public inspection. Miniconda is the official lightweight distribution from Anaconda, Inc., and defaults to using their package collection.

``` bash
wget https://github.com/conda-forge/miniforge/releases/download/24.11.0-0/Miniforge3-Linux-x86_64.sh
bash Miniforge3-Linux-x86_64.sh -bfp /desired/path/to/conda
source /desired/path/to/conda/etc/profile.d/conda.sh
conda activate
```

### Using a Prebuilt Package

With conda activated, the following command installs the latest available `condev` package:

``` bash
conda install -y -c maddenp condev
```

This also installs dependency packages providing:

- `conda-build` for building conda packages and interpreting their metadata
- `jq` for extracting select metadata values from conda-package metadata
- `make` for using the convenient targets defined by the `condev` `Makefile`s

The `maddenp` channel can be searched for available versions with `conda search -c maddenp --override-channels condev`, and a specific version installed by replacing `condev` with `condev=<version>[=build]` in the preceding `conda install` command.

### Bootstrapping

With conda activated, the following steps install required dependency packages, builds the `condev` conda package, installs that package into the base environment, then verifies that the expected `condev` programs are available:

``` bash
conda install -y conda-build jq make
make package
conda install -y -c local condev=$(jq -r .version src/condev/resources/meta.json)=*_$(jq -r .buildnum src/condev/resources/meta.json)
which condev-meta condev-shell
```

In the future, after executing this procedure, the `condev`-equipped conda installation can be activated with `source /path/to/condev/conda/etc/profile.d/conda.sh && conda activate`.

## General Use

By adhering to a few conventions in the layout and configuration of the project, a `condev`-equipped conda installation can:

- Obtain a development shell in which to can edit and test code interactively, in an isolated environment with all dependency libraries available, with `make devshell`
- Build a conda package based on the project's recipe with the `make package` command
- Create a conda environment based on the project's recipe with the `make env` command
- Execute the project's defined code-quality tests with the `make test` command (or the more granular `make lint`, `make typecheck`, and `make unittest` commands)
- Auto-format the project's Python code with the `make format` command

The Bash shell created by `make devshell` may start with only a subset of the host shell's environment. If a `~/.condevrc` file exists, it will be sourced to do any required environment setup. For example, `~/.condevrc` might simply contain `. ~/.bashrc`.

## Demo

The `demo` subdirectory of this repo offers a prototype project (i.e. files/directories that would appear in the root of a separate git repository) that leverages `condev` to demonstrate the use of the various convenience `make` targets. It also demonstrates one way in which hybrid Python/C projects might be handled.

**NB** Prior to `condev` `v0.7.0`, conventions involved a fleshed-out `recipe/meta.yaml` file and a `make meta` targed that called the `condev` utility `condev-meta` to render the conda recipe, extract selected metadata, and write it to `recipe/meta.json` for use my other `make` targets, tests defined in `recipe/run_test.sh`, etc. The new conventions rely on the existince of a version-contolled `meta.json` file in a project's `src/<package>/resources/` directory, which is then loaded by `recipe/meta.yaml` to augment its own minimal content. The `v0.7.0` `condev` is meant to be backward compatible with projects that continue to use the old conventions, but an update to the new conventions is recommended. See pre-`v0.7.0` versions of this file for detailed information on the old conventions.

### `make devshell`

Use `make devshell` to create and activate a conda environment in which all dependency packages are available, and package's Python code is live-linked for a fast edit/test loop. After executing the the _Getting Started_ procedure above, try the following:

``` bash
cd demo
make devshell
```

This will create a conda environment with the project's build, host, run, and test packages all installed and ready to use. The Python code under `src/hello` is live-linked into the environment via a `setuptools` [editable install](https://setuptools.pypa.io/en/latest/userguide/development_mode.html), so any changes can be immediately executed, tested, etc. The Bash prompt will be prefixed with the name of the development environment, `(DEV-hello)`.

If this were a pure-Python codebase, the `heythere` entry-point console script (defined in `src/setup.py`) could now be run. Try, and see how it fails. Since this project's Python code relies on a C function (which also lives in the project, so cannot be satisfied by installing a dependency package), that needs to be built first:

``` bash
(cd src/world && make install)
```

Running `heythere` now should succeed.

The `demo` project provides auto-formatting via [black](https://github.com/psf/black), [docformatter](https://pypi.org/project/docformatter/), and [isort](https://pycqa.github.io/isort/). Run `make format` to auto-format all Python code in the project. This _should_ do nothing if the code hasn't been changed since the repo was cloned, but feel free to edit e.g. `src/hello/core.py`, then run `make format` to see the tools in action.

The code-quality tools -- linter, type checker, and unit tests with a coverage report -- can be run with `make test`. These tests rely on [pylint](https://pypi.org/project/pylint/), [mypy](https://github.com/python/mypy), and [pytest](https://docs.pytest.org) (with some plugins), primarily configured via `src/pyproject.toml`. The tools can be run individually with `make lint`, `make typecheck`, and `make unittest`. Again, these tools should all pass if the code has not been changed (provided the C code was also built, as described above).

When finished with development work, exit the development shell with `exit` or CTRL-D. Typing `make devshell` again later, the existing environment will be activated nearly instantaneously.

**NB**: As a rule of thumb, manually remove a development environment (e.g. `conda env remove -y -n DEV-demo`) and recreate it with `make devshell` the contents of `recipe/` or the `src/<package>/resources/info.json` file change.

#### Run a single command in a development shell

Exporting environment variable `CONDEV_SHELL_CMD` then running `make devshell` (or its underlying `condev-shell` script directly), will result in the variable's value being executed as a command in the devlopment shell, followed by the development shell exiting and returning control to the caller. This may be useful for automation, e.g. in CI environments.

### `make package`

While *not* in a development shell (`exit` from `DEV-hello` if necessary), run `make package` to invoke `conda-build` to build the `demo` code as a conda package. The same tests run by `make test` will be run by `conda-build`, and must succeed for the final package to be built -- so to save time, ensure that `make test` in a development shell succeeds before attempting `make package`. When the package has been built, verify its availability with

``` bash
conda search -c local --override-channels hello
```

Depending on requirements, the package could be uploaded to a public Anaconda channelor to a private conda-package server, or simply accessed from local disk, to create conda environments that include it.

### `make env`

Use `make env` to create a conda package based on the `demo` code, then create a conda environment based on the built package and any run dependencies it declares. The environment will be named based on the package name, version number, and build number. Try:

``` bash
make env
version=$(jq -r .version src/demo/resources/meta.json)
buildnum=$(jq -r .buildnum src/demo/resources//meta.json)
conda activate hello-$version-$buildnum
heythere
```

## Conventions and Advice

The `demo` project demonstrates a number of conventions (or in some case requirements) that might be helpful when working with `condev` and/or with `conda` and/or with Python projects in general:

- `recipe/build.sh` is a standard `conda-build` file and is executed to build code and install it into the `conda-build`-supplied `$PREFIX` tree for packaging. Simple build recipes can be provided directly in `meta.yaml` as an alternative, but `build.sh` allows maximum flexibility. (See the link in the `recipe/meta.yaml` bullet below for detailed information on that file's contents.)
- `recipe/channels` specifies a list of channels conda is allowed to use to obtain packages. Via `make` targets, calls to `conda create`, `conda install`, etc., include these channels, translated into `-c` (aka `--channel`) options. Channels are consulted in priority order; packages satisfying requirements are taken from the highest-priority channel. The `local` channel (i.e. packages built by and contained in the local conda installation) is always implicitly added as the lowest-priority channel. This file is required by the `condev` tools, but is not a standard file from the perspective of `conda-build`.
- `recipe/meta.yaml` is [well described](https://docs.conda.io/projects/conda-build/en/latest/resources/define-metadata.html).
- `recipe/run_test.sh` is a standard `conda-build` file, is executed late in the package-build process, and must run successfully for the build to complete. Normally, the tests executed in this script are meant to test the built and packaged code in its run-time environment; however, the `demo` project also arranges for everything available in a development shell to also be available at `conda-build` test time, such that the same code-quality tests executed by `make test` at development time can be exercised one last time before the final package is built. (In fact, `make test` works by executing `run_test.sh` in the development shell, to avoid build-time surprises.)
- `src/pyproject.toml` specifies most configuration options for the code-quality tools listed in the `test` `requires` section of `meta.json` and exercised by `make test` / `recipe/run_test.sh`.
- `src/setup.py` is used both to install Python code (and potentially non-Python scripts) at package build time, and to create an "editable install" into the development shell. It relies on metadata supplied by `src/<package>/resources/meta.json`. `make devshell` (or `condev-shell`) expect to be run from the repo root directory where `src/setup.py` is available. `src/setup.py` also defines so-called entry-point console scripts: The command-line programs that the package provides users. Prefer writing Python code as a _library_ (i.e. do not include `#!` at the top of, or `if __name__ == "__main__"` at the bottom of, `.py` files) and rely on `setuptools` (via `setup.py`) to create and install entry-point scripts that load and call the appropriate package, module, and function.
- Use `importlib.resources` to provide configuration files, etc., to code. Python will always know where to find resources so configured, regardless of whether the code is running in a development shell or a final, deployed conda environment, eliminating any headaches about paths. Update `src/MANIFEST.in` in combination with setting `"include_package_data": True` in `setup.py` for support run-time loading of files in a repo's `src/<package>/resources` directory.
- If these conventions are followed, `demo/Makefile` should be usable for most any Python project.

## Notes

- There is *a lot* about `conda-build` that all this glosses over. It is a powerful tool for building, packaging, and versioning code from nearly any language, and covers countless complex use cases. So, the [the documentation](https://docs.conda.io/projects/conda-build/en/stable/) is invaluable. The [Defining metadata (meta.yaml)](https://docs.conda.io/projects/conda-build/en/latest/resources/define-metadata.html) page is especially handy. There's no way to avoid complexity in some cases, though using these `condev` tools and their associated conventions can often hide a lot of it.
- When creating a single conda (e.g. Miniforge) installation that multiple users of a multi-tenant system can share, beware: Many conda packages contain files that are group-writable, and if the shared conda installation is `chgrp`ed to a group that users are also members of, they may be able to, even if by accident, overwrite files that should be read-only to them. To work around this: 1. Make sure that the conda installation's files are `chgrp`ed to a group that _only_ contains the appropriate user(s); and 2. Have each user `export CONDA_PKGS_DIR=$HOME/.conda/pkgs` or similar. The first step ensures that arbitrary users cannot modify any part of the conda installation but, by itself, would also lead to errors when users ran commands like `conda create`, as they would not have permissions to download package files into the conda directory, as conda requires. The second steps mitigates that issue, by letting each user download and cache packages in a directory they own -- though at the unfortunate potential expense of added disk use. Used together, these steps support group use of a shared conda installation; but, if the disk space can be spared, consider having users maintain their own e.g. Miniconda installations, to avoid coordination headaches.
- It may sometimes be useful to create multiple development environments concurrently from the "same" code, perhaps based on different git branches. This would normally cause a conflict, as the same development environment name (e.g. `DEV-hello`) would be oversubscribed. Set the `DEV_ENV_PREFIX` environment variable to change the `DEV` prefix to something else; for example, `DEV_ENV_PREFIX=FOO make devshell` would create development environment `FOO-hello` in the `demo` project.
- Some of the techniques used in the `Makefile`, `recipe/` directory, etc., of the top-level `condev` project are not meant for duplication in projects that would _use_ the `condev` tools, but are required for bootstrapping in environments where `condev` tools are not yet available. The techniques used in the `demo` project are better examples to follow.
