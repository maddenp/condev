# condev

Creates conda development environments and provides related convenience tooling.

## Getting Started

The `condev` tools expect to run in a conda environment providing these programs:

- `conda` itself
- `conda-build` and `conda-verify` for building conda packages and interpreting their metadata
- `jq` for extracting select metadata values from conda-package metadata
- A late-model `make` for using the convenient targets defined by the `condev` `Makefile`s

`conda` itself may be provided by a [Miniconda](https://docs.conda.io/en/latest/miniconda.html), [Miniforge](https://github.com/conda-forge/miniforge#miniforge3), [Mambaforge](https://github.com/conda-forge/miniforge#mambaforge), or [Anaconda](https://www.anaconda.com/) installation. Prefer one of the first three for a lightweight installation providing only what you need. Miniconda is the official distribution from Anaconda, Inc., and defaults to using their package collection. Miniforge is equivalent to Miniconda except that it defaults to using the [conda-forge](https://conda-forge.org/) package collection: A community-curated collection of high-quality packages for which all recipes are available for public inspection. Mambaforge is identical to Miniforge except that includes the [mamba](https://github.com/mamba-org/mamba) tools. If you are unsure, use Miniforge, as shown below.

The bootstrap procedure below downloads the latest Miniforge installer, installs it to a `conda` subdirectory in your `condev` clone, activates the base environment in your (Bourne-family) shell, installs additional tools required by `condev`, builds the `condev` conda package, installs that package into the base environment, then verifies that the expected `condev` programs are available.

``` bash
cd condev # your condev git clone
wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh
bash Miniforge3-Linux-x86_64.sh -bfp ./conda
source ./conda/etc/profile.d/conda.sh
conda activate
conda install -y conda-build conda-verify jq make
make package
conda install -y -c local condev=$(jq -r .version recipe/meta.json)=$(jq -r .buildnum recipe/meta.json)
which condev-meta condev-shell
```

After executing this procedure, you should have a `condev`-equipped conda installation that you can activate in the future with the command `source /path/to/condev/conda/etc/profile.d/conda.sh && conda activate`.

## General Use

If you adhere to a few conventions in the layout and configuration of your project, you can use your `condev`-equipped conda installation to:

- Obtain a development shell in which you can edit and test your code interactively, in an isolated environment with all dependency libraries available
- Build a conda package based on your project's recipe with the `make package` command
- Create a conda environment based on your project's recipe with the `make env` command
- Execute your project's defined code-quality tests with the `make test` command (or the more granular `make lint`, `make typecheck`, and `make unittest` commands)
- Auto-format your Python code with the `make format` command

## Demo

The `demo` subdirectory of this repo offers a prototype project (i.e. files/directories that would appear in the root of a separate git repository) that leverages `condev` to demonstrate the use of the various convenience `make` targets. It also demonstrates one way in which hybrid Python/C projects might be handled.

### `make devshell`

Use `make devshell` to create and actiate a conda environment in which all dependency packages are available, and package's Python code is live-linked for a fast edit/test loop. After executing the the _Getting Started_ procedure above, try the following:

``` bash
cd demo
make devshell
```

This will create a conda environment with your project's build, host, run, and test packages all installed and ready to use. The Python code under `src/hello` is live-linked into the environment via a `setuptools` [editable install](https://setuptools.pypa.io/en/latest/userguide/development_mode.html), so any changes you make can be immediately executed, tested, etc. You will see your Bash prompt prefixed with the name of the development environment, `(DEV-hello)`.

If this were a pure-Python codebase, you could now run the `heythere` entry-point console script (defined by `src/setup.py`). Try that and see how it fails. Since this project's Python code relies on a C function (which also lives in the project, so cannot be satisfied by installing a dependency package), that needs to be build first:

``` bash
(cd src/world && make install)
```

Now run `heythere` and it should succeed.

The `demo` project provides auto-formatting via [black](https://github.com/psf/black) and [isort](https://pycqa.github.io/isort/). Run `make format` to auto-format all Python code in the project. This _should_ do nothing if you haven't changed the code since you cloned the repo, but feel free to edit e.g. `src/hello/core.py`, then run `make format` to see the tools in action.

You can run code-quality tools -- linter, type checker, and unit tests with a coverage report -- by running `make test`. These tests rely on [pylint](https://pypi.org/project/pylint/), [mypy](https://github.com/python/mypy), [pytest](https://docs.pytest.org), and [coverage](https://coverage.readthedocs.io), primarily configured via the `pyproject.toml` file in the project's root directory. You can also run tools individually with `make lint`, `make typecheck`, and `make unittest`. Again, these tools should all pass if you have not changed the code (provided you have build the C code as described above), but you can tweak the code to see how the tools respond to code-quality issues.

When you are finished with development work, you can simply exit the development shell with `exit` or CTRL-D. If you later type `make devshell` again, the existing environment will be activated nearly instantaneously.

*NB*: As a rule of thumb, you should manually remove your development environment (e.g. `conda env remove -n DEV-demo`) if you change the contents of `recipe/`, and especially if you change the `meta.yaml` file, which defines required dependency packages. Likewise, the file `recipe/meta.json` is generated by several `make` targets, but only if certain other files under `recipe/` change. There could be other circumstances under which this file should be regenerated, however, so manually remove it and re-run your `make` command if in doubt.

### `make package`

While *not* in a development shell (`exit` from `DEV-hello` if necessary), run `make package` to invoke `conda-build` to build the `demo` code as a conda package. (Note that the same tests run by `make test` will be run by `conda-build`, and must succeed for the final package to be built -- so to save time, ensure that `make test` in a development shell succeeds before attempting `make package`.) When the package has been built, you can verify its availability with

``` bash
conda search -c local --override-channels hello
```

Depending on your needs, you could upload this package to a public Anaconda channel, to a private conda-package server, or simply access it from local disk, creating conda environments that include it.

### `make env`

Use `make env` to create a conda package based on the current directory's recipe, then create a conda environment based on that package -- pulling in any run-time dependency packages it declares in its `recipe/meta.yaml` file -- named based on the package name, version number, and build number. Try:

``` bash
make env
version=$(jq -r .version recipe/meta.json)
buildnum=$(jq -r .buildnum recipe/meta.json)
conda activate hello-$version-$buildnum
heythere
```

## Notes

- There is *a lot* about `conda-build` that all this glosses over. It is a powerful tool for building, packaging, and versioning code from nearly any language, and covers countless complex use cases. So, the [the documentation](https://docs.conda.io/projects/conda-build/en/stable/) is invaluable. The [Defining metadata (meta.yaml)](https://docs.conda.io/projects/conda-build/en/latest/resources/define-metadata.html) page is especially handy. There's no way to avoid complexity in some cases, though using these `condev` tools and their associated conventions can often hide a lot of it.
- You might like to create a single conda (e.g. Miniforge) installation that multiple users of a multi-tennant system can share. Beware: Many conda packages contain files that are group-writable, and if your shared conda installation is `chgrp`ed to a group that your users are also members of, they may be able to, even if by accident, overrwrite files that should be read-only to them. To work around this: 1. Make sure that the conda installation's files are `chgrp`ed to a group that _only_ contains the appropriate user(s); and 2. Have each user `export CONDA_PKGS_DIR=$HOME/.conda/pkgs` or similar. The first step ensures that arbitrary users cannot modify any part of the conda installation but, by itself, would also lead to errors when users ran commands like `conda create`, as they would not have permissions to download package files into the conda directory, as conda requires. The second steps mitigates that issue, by letting each user download and cache packages in a directory they own -- at the unfortunate potential expense of added disk use. Used together, these steps support group use of a shared conda installation; but, if you can spare the disk space, consider having users maintain their own e.g. Miniconda installations, to avoid coordination headaches.
- It may sometimes be useful to create multiple development environments concurrently from the "same" code, perhaps based on different git branches. This would normally cause a conflict, as the same development environment name (e.g. `DEV-hello`) would be oversubscribed. You may set the `DEV_ENV_PREFIX` environment variable to change the `DEV` prefix to something else; for example, `DEV_ENV_PREFIX=FOO make devshell` would create development environment `FOO-hello` in the `demo` project.
- Note that some of the techniques used in the `Makefile`, `recipe/` directory, etc., of the top-level `condev` project are not meant for duplication in projects that would _use_ the `condev` tools, but are required for bootstrapping in environments where `condev` tools are not yet available. The techniques used in the `demo` project are better examples to follow.
