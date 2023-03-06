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

The `demo` subdirectory of this repo offers a prototype project (i.e. files/directories that would appear in the root of a separate git repository) that leverages `condev`. It also demonstrates one way in which hybrid Python/C projects might be handled.

After executing the the _Getting Started_ procedure above, try the following:

``` bash
cd demo
make devshell
```

This will create a conda environment with your project's build, host, run, and test packages all installed and ready to use. The Python code under `src/hello` is live-linked into the environment via a `setuptools` [editable install](https://setuptools.pypa.io/en/latest/userguide/development_mode.html), so any changes you make can be immediately executed, tested, etc. You will see your Bash prompt prefixed with the name of the development environment, `(DEV-hello)`.

In a pure-Python codebase, you could now run the Python code-quality tests with `make test`, or run the `heythere` entry-point console script (defined by `src/setup.py`) successfully. Try those commands now and note how they fail.

Since this project's Python code relies on a C function (which also lives in the project, so cannot be satisfied by installing a dependency package), that needs to be build first:

``` bash
(cd src/world && make install)
```

Now try running `make test` and `heythere` again. They should both succeed.

When you are finished with development work, you can simply exit the development environment with `exit` or CTRL-D. If you later type `make devshell` again, the existing environment will be activated nearly instantaneously.

*NB*: As a rule of thumb, you should manually remove your development environment (e.g. `conda env remove -n DEV-demo`) if you change the contents of `recipe/`, and especially if you change the `meta.yaml` file, which defines required dependency packages. Likewise, the file `recipe/meta.json` is generated by several `make` targets, but only if certain other files under `recipe/` change. There could be other circumstances under which this file should be regenerated, however, so manually remove it and re-run your `make` command if in doubt.


# READ MORE ABOUT CONDA_BUILD ETC WARNING
# SHARED INSTALL WARNING
# DEV_ENV_PREFIX note
