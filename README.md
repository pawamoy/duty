# duty

[![ci](https://github.com/pawamoy/duty/workflows/ci/badge.svg)](https://github.com/pawamoy/duty/actions?query=workflow%3Aci)
[![documentation](https://img.shields.io/badge/docs-mkdocs-708FCC.svg?style=flat)](https://pawamoy.github.io/duty/)
[![pypi version](https://img.shields.io/pypi/v/duty.svg)](https://pypi.org/project/duty/)
[![gitter](https://img.shields.io/badge/matrix-chat-4DB798.svg?style=flat)](https://app.gitter.im/#/room/#duty:gitter.im)

A simple task runner.

Inspired by [Invoke](https://github.com/pyinvoke/invoke).

![demo](demo.svg)

## Installation

```bash
pip install duty
```

With [`uv`](https://docs.astral.sh/uv/):

```bash
uv tool install duty
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

Also see ["Why choosing duty over..."](https://pawamoy.github.io/duty/#why-duty-over).

## Sponsors

<!-- sponsors-start -->
<!-- sponsors-end -->
