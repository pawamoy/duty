# Duty

[![ci](https://github.com/pawamoy/duty/workflows/ci/badge.svg)](https://github.com/pawamoy/duty/actions?query=workflow%3Aci)
[![documentation](https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat)](https://pawamoy.github.io/duty/)
[![pypi version](https://img.shields.io/pypi/v/duty.svg)](https://pypi.org/project/duty/)
[![gitpod](https://img.shields.io/badge/gitpod-workspace-blue.svg?style=flat)](https://gitpod.io/#https://github.com/pawamoy/duty)
[![gitter](https://badges.gitter.im/join%20chat.svg)](https://gitter.im/duty/community)

A simple task runner.

Inspired by [Invoke](https://github.com/pyinvoke/invoke).

![demo](demo.svg)

## Installation

With `pip`:
```bash
pip install duty
```

With [`pipx`](https://github.com/pipxproject/pipx):
```bash
python3.7 -m pip install --user pipx
pipx install duty
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
