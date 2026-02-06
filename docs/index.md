---
title: Overview
hide:
- feedback
---

--8<-- "README.md"

## Why duty over...

### [Invoke](https://www.pyinvoke.org/)?

The main difference is duty's ability to run Python callables,
not just (sub)processes. Using Python callables brings three advantages:

- **performance**: creating subprocesses is costly. Running a callable
    in the current Python process is much cheaper.
- **containment**: running an executable in a subprocess can load
    various things in the process' environment which you do not
    have control over. Running a callable in the current Python
    process ensures that the current process' environment is used,
    as you configured it.
- **extensibility**: get the full power of Python! You can define
    functions dynamically in your tasks and run them through duty.
    We actually provide a set of [ready-to-use callables][duty.tools].

Notable differences with Invoke:

- duty captures standard output and error by default.
    For **interactive commands**, you have to pass the `capture=False` option.
    See [capturing commands output][capturing-commands-output].
- on the CLI, parameters are passed with `param=value`, not `--param=value`.
    For a boolean parameter: `param=true` instead of `--param`.
    See [passing parameters][passing-parameters].

duty provides additional facilities to:

- [skip tasks][skipping-duties]
- [create lazy callables][lazy-callables]
- [format the output of commands][formatting-duty-output]

The rest is pretty much similar to Invoke. duty has:

- [tasks listing][listing-duties]
- [tasks aliasing][defining-aliases]
- [tasks parameters][passing-parameters]
- [before/after hooks][prepost-duties]
- [working directory management][changing-the-working-directory]

### [GNU Make](https://www.gnu.org/software/make/)?

Make and duty are not really comparable.
However they complement each other well.
For example if you are managing your Python project
with Poetry or PDM, it can be tedious to type
`poetry run duty ...` or `pdm run duty ...` to run tasks.
With a makefile you can shorten this to `make ...`:

```makefile
DUTY := $(if $(VIRTUAL_ENV),,pdm run) duty

clean:
	@$(DUTY) clean
```

See [our Makefile](https://github.com/pawamoy/duty/blob/main/Makefile)
for inspiration.

### [Task](https://taskfile.dev/)?

Task is based on a Taskfile written in YAML.
Declarative languages are nice, but quickly get limited
when you have complex things to run.

Also Task is written in Go so you won't be able to specify
it in your Python dev-dependencies.

### [Poe the Poet](https://github.com/nat-n/poethepoet)

Poe the Poet, or `poe`, lets you declare tasks in pyproject.toml.
The comparison is similar to [Task's](#task): declarative language only gets you so far.
duty is fully based on Python, and provides you with batteries to control
the output, the exit code, etc. While Poe the Poet lets you call Python functions,
the user would have to re-implement these batteries themselves.

Poe the Poet and duty can be used together though, with Poe tasks calling duty.
But that feels like an additional complexity layer for the single benefit
of declaring your task directly in pyproject.toml.

```toml
[tool.poe.tasks]
test = "duty test"
docs = "duty docs"
```
