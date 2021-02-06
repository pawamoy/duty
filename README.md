# Duty

[![ci](https://github.com/pawamoy/duty/workflows/ci/badge.svg)](https://github.com/pawamoy/duty/actions?query=workflow%3Aci)
[![documentation](https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat)](https://pawamoy.github.io/duty/)
[![pypi version](https://img.shields.io/pypi/v/duty.svg)](https://pypi.org/project/duty/)
[![gitter](https://badges.gitter.im/join%20chat.svg)](https://gitter.im/duty/community)

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

Create a `duties.py` file at the root of your repository.

```python
from duty import duty

@duty
def docs(ctx):
    ctx.run("mkdocs build", title="Building documentation")
```

You can now use the command line tool to run it:

```bash
duty docs
```

See the [Usage](https://pawamoy.github.io/duty/usage/)
section in the documentation for more examples.
