# duty

A simple task runner.

Inspired by [Invoke](https://github.com/pyinvoke/invoke).

## Installation

```
pip install duty
```

With [`uv`](https://docs.astral.sh/uv/):

```
uv tool install duty
```

## Quick start

Create a `duties.py` file at the root of your repository.

```
from duty import duty

@duty
def docs(ctx):
    ctx.run("mkdocs build", title="Building documentation")
```

You can now use the command line tool to run it:

```
duty docs
```

See the [Usage](https://pawamoy.github.io/duty/usage/) section in the documentation for more examples.

Also see ["Why choosing duty over..."](https://pawamoy.github.io/duty/#why-duty-over).

## Sponsors

**Silver sponsors**

**Bronze sponsors**

______________________________________________________________________

*And 7 more private sponsor(s).*

## Why duty over...

### [Invoke](https://www.pyinvoke.org/)?

The main difference is duty's ability to run Python callables, not just (sub)processes. Using Python callables brings three advantages:

- **performance**: creating subprocesses is costly. Running a callable in the current Python process is much cheaper.
- **containment**: running an executable in a subprocess can load various things in the process' environment which you do not have control over. Running a callable in the current Python process ensures that the current process' environment is used, as you configured it.
- **extensibility**: get the full power of Python! You can define functions dynamically in your tasks and run them through duty. We actually provide a set of ready-to-use callables.

Notable differences with Invoke:

- duty captures standard output and error by default. For **interactive commands**, you have to pass the `capture=False` option. See capturing commands output.
- on the CLI, parameters are passed with `param=value`, not `--param=value`. For a boolean parameter: `param=true` instead of `--param`. See passing parameters.

duty provides additional facilities to:

- skip tasks
- create lazy callables
- format the output of commands

The rest is pretty much similar to Invoke. duty has:

- tasks listing
- tasks aliasing
- tasks parameters
- before/after hooks
- working directory management

### [GNU Make](https://www.gnu.org/software/make/)?

Make and duty are not really comparable. However they complement each other well. For example if you are managing your Python project with Poetry or PDM, it can be tedious to type `poetry run duty ...` or `pdm run duty ...` to run tasks. With a makefile you can shorten this to `make ...`:

```
DUTY := $(if $(VIRTUAL_ENV),,pdm run) duty

clean:
    @$(DUTY) clean
```

See [our Makefile](https://github.com/pawamoy/duty/blob/main/Makefile) for inspiration.

### [Task](https://taskfile.dev/)?

Task is based on a Taskfile written in YAML. Declarative languages are nice, but quickly get limited when you have complex things to run.

Also Task is written in Go so you won't be able to specify it in your Python dev-dependencies.
