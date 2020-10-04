# Duty

[![ci](https://github.com/pawamoy/duty/workflows/ci/badge.svg)](https://github.com/pawamoy/duty/actions?query=workflow%3Aci)
[![documentation](https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat)](https://pawamoy.github.io/duty/)
[![pypi version](https://img.shields.io/pypi/v/duty.svg)](https://pypi.org/project/duty/)

A simple task runner.

Inspired by [Invoke](https://github.com/pyinvoke/invoke).

![demo](demo.svg)

## Requirements

Duty requires Python 3.6 or above.

<details>
<summary>To install Python 3.6, I recommend using <a href="https://github.com/pyenv/pyenv"><code>pyenv</code></a>.</summary>

```bash
# install pyenv
git clone https://github.com/pyenv/pyenv ~/.pyenv

# setup pyenv (you should also put these three lines in .bashrc or similar)
export PATH="${HOME}/.pyenv/bin:${PATH}"
export PYENV_ROOT="${HOME}/.pyenv"
eval "$(pyenv init -)"

# install Python 3.6
pyenv install 3.6.12

# make it available globally
pyenv global system 3.6.12
```
</details>

## Installation

With `pip`:
```bash
python3.6 -m pip install duty
```

With [`pipx`](https://github.com/pipxproject/pipx):
```bash
python3.6 -m pip install --user pipx

pipx install --python python3.6 duty
```

## Quick start

Proper documentation pages will soon be available.

### Configuration

Create a `duties.py` file at the root of your repository.

Each task is declared as a "duty", using the `duty.duty` decorator.

```python
from duty import duty

@duty
def docs(ctx):
    ctx.run("mkdocs build", title="Building documentation")
```

The `ctx` argument is the "context" of the duty.
It is automatically created and passed to your function.

It has only one purpose: running command with its `run` method.
The `run` method accepts strings, list of strings, or even Python callables.

The above duty can be rewritten as:

```python
from duty import duty

@duty
def docs(ctx):
    ctx.run(["mkdocs", "build"], title="Building documentation")
    # avoid the overhead of an extra shell process
```

Or:

```python
from duty import duty
from mkdocs import build, config

@duty
def docs(ctx):
    ctx.run(build.build, args=[config.load_config()], title="Building documentation")
    # avoid the overhead of an extra Python process
```

The `run` methods accepts various options,
mostly coming from its underlying dependency:
[`failprint`](https://github.com/pawamoy/failprint).

**Arguments of the `run` method:**

Name | Type | Description | Default
---- | ---- | ----------- | -------
cmd | `str`, `list of str`, or Python callable | The command to run. | *required*
args | `list` | Arguments to pass to the callable. | `[]`
kwargs | `dict` | Keyword arguments to pass to the callable. | `{}`
number | `int` | The command number (useful for the `tap` format). | `None`
output_type | `str` | The type of output: `stdout`, `stderr`, `combine` or `nocapture` | `combine`
title | `str` | The command title. | *cmd as a shell command or Python statement*
fmt | `str` | The output format as a Jinja template: `pretty`, `tap` or `custom=...` | `pretty`
pty | `bool` | Whether to run in a PTY. | `False`
progress | `bool` | Whether to show progress. | `True`
nofail | `bool` | Whether to always succeed. | `False`
quiet | `bool` | Don't print the command output, even if it failed. | `False`
silent | `bool` | Don't print anything. | `False`

Example usage of the `silent` option:

```python
@duty
def clean(ctx):
    ctx.run("find . -type d -name __pycache__ | xargs rm -rf", silent=True)
```

Now let's say you have more than one command, and you want to silence all of them:

```python
@duty(silent=True)
def clean(ctx):
    ctx.run("rm -rf .coverage*")
    ctx.run("rm -rf .mypy_cache")
    ctx.run("rm -rf .pytest_cache")
    ctx.run("rm -rf build")
    ctx.run("rm -rf dist")
    ctx.run("rm -rf pip-wheel-metadata")
    ctx.run("rm -rf site")
    ctx.run("find . -type d -name __pycache__ | xargs rm -rf")
    ctx.run("find . -name '*.rej' -delete")
```

### Run

To run a duty, simply use:

```bash
duty clean
```

If you are using [Poetry](https://github.com/python-poetry/poetry):

```bash
poetry run duty clean
```

You can pass multiple duties in one command:

```bash
duty clean docs
```

If one of your duties accept arguments,
you can pass them on the command line as well:

```python
@duty
def docs(ctx, serve=False):
    command = "serve" if serve else "build"
    ctx.run(f"mkdocs {command}")
```

```bash
duty docs serve=1
```

!!! note
    Note that arguments are not type-casted:
    they are always passed as strings to the duties.

## Todo

- Better handling of missing duties arguments.
  Maybe simply print the error without a traceback:
  `release() missing 1 required positional argument: 'version'`
- Arguments type casting, ideally based on type annotations!