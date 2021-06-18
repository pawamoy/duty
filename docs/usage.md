# Usage

## Writing duties

Your tasks, or duties, are defined in a Python module.
By default, `duty` will load these tasks
from a `duties.py` file at the root of your repository.

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

### `ctx.run()` options

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
capture | `str` | The type of output: `"stdout"`, `"stderr"`, `"both"` (or `True`) and `"none"` (or `False`) | `True`
title | `str` | The command title. | *cmd as a shell command or Python statement*
fmt | `str` | The output format as a Jinja template: `"pretty"`, `"tap"` or `"custom=..."` | `"pretty"`
pty | `bool` | Whether to run in a PTY. | `False`
progress | `bool` | Whether to show progress. | `True`
nofail | `bool` | Whether to always succeed. | `False`
quiet | `bool` | Don't print the command output, even if it failed. | `False`
silent | `bool` | Don't print anything. | `False`
workdir | `str` | Change the working directory. | `None`
allow_overrides | `bool` | Allow options overrides via CLI arguments. | `True`.

Example usage of the `silent` option:

```python
@duty
def clean(ctx):
    ctx.run("find . -type d -name __pycache__ | xargs rm -rf", silent=True)
```

### Default options

Let's say you have more than one command, and you want to silence all of them.
Instead of passing `silent=True` to all `ctx.run()` calls,
you can set this option as default in the decorator itself:

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

You can of course override the default options
in the `ctx.run()` calls:

```python
@duty(capture=True)
def run_scripts(ctx):
    ctx.run("bash script1.sh")
    ctx.run("bash script2.sh")
    ctx.run("bash script3.sh", capture=False)
```

### Options as a context manager

You can temporarily change options for several `run` calls with `ctx.options()`:

```python
@duty
def run_scripts(ctx):
    with ctx.options(nofail=True):
        ctx.run("bash script1.sh")
        ctx.run("bash script2.sh")
    ctx.run("bash script3.sh")
```

Such temporary changes will stack above the previous ones
each time you enter the `with` clause,
and unstack each time you leave it:

```python
@duty
def run_scripts(ctx):
    ctx.run("bash script0.sh")  # defaults

    with ctx.options(nofail=True):
        ctx.run("bash script1.sh")  # nofail=True

        with ctx.options(quiet=True):
            ctx.run("bash script2.sh")  # nofail=True, quiet=True

            with ctx.options(silent=True, nofail=False):
                ctx.run("bash script3.sh")  # nofail=False, quiet=True, silent=True

            ctx.run("bash script4.sh")  # nofail=True, quiet=True

        ctx.run("bash script5.sh")  # nofail=True

    ctx.run("bash script6.sh")  # defaults
```

### Changing the working directory

You can change the working directory for a specific `run`:

```python
@duty
def run_scripts(ctx):
    ctx.run("bash script3.sh", workdir="subfolder")
```

Or for a group of `run` calls, using the `options` context manager:

```python
@duty
def run_scripts(ctx):
    ctx.run("echo in .")
    ctx.run("ls")
    with ctx.options(workdir="subfolder"):
        ctx.run("echo in subfolder")
        ctx.run("ls")
```

!!! warning "The change of directory is not immediate."
    When using the `workdir` option through the context manager,
    the actual change of directory is deferred to each of the `run` calls
    within that context.

    A nesting of `ctx.options(workdir=...)` will each time override the previous one:

    ```python
    @duty
    def run_scripts(ctx):
        ctx.run("echo in .")  # run in ./
        with ctx.options(workdir="A"):
            ctx.run("echo in A")  # run in ./A
            with ctx.options(workdir="B"):
                ctx.run("echo in...")  # run in ./B, not ./A/B!
    ```

    It also means instructions other than `ctx.run` still run in the original directory!

    ```python
    @duty
    def run_scripts(ctx):
        ctx.run("echo in .")  # run in ./
        with ctx.options(workdir="A"):
            ctx.run("echo in A")  # run in ./A
            l = os.listdir()  # run in ./, not ./A!
    ```

    If you want to immediately enter the directory,
    or to nest multiple directory changes, use the `cd` context manager.

Another way to change the working directory
is to use the `ctx.cd(directory)` context manager:

```python
@duty
def run_scripts(ctx):
    ctx.run("echo in .")  # run in ./

    with ctx.cd("A"):
        ctx.run("echo in A")  # run in ./A
        l = os.listdir()  # run in ./A as well

        with ctx.cd("B"):
            ctx.run("echo in A/B")  # run in ./A/B
            ctx.run("echo in A/B/C", workdir="C")  # run in ./A/B/C

        ctx.run("echo in A")  # back to ./A

    ctx.run("echo in .")  # back to ./
```

## Running duties

To run a duty, simply use:

```bash
duty clean
```

If you are using [Poetry](https://github.com/python-poetry/poetry)
or [PDM](https://github.com/frostming/pdm):

```bash
poetry run duty clean
pdm run duty clean
```

You can pass multiple duties in one command:

```bash
duty clean docs
```

### Passing parameters

Duties can accept arguments (or parameters):

```python
@duty
def docs(ctx, serve: bool = False):
    command = "serve" if serve else "build"
    ctx.run(f"mkdocs {command}")
```

When passing the argument from the command line,
it will be type-casted using the parameter annotation
in the duty's signature.

We only support types that are callable and accept
one positional argument: a string.
Examples of supported builtin types: `int`, `str`, `float`, `bool`, `list`, etc.

The `bool` type uses a special conversion table:

Value (case-insensitive) | Result
----- | ------
`""` (empty string) | `False`
`"0"` | `False`
`"off"` | `False`
`"n"` | `False`
`"no"` | `False`
`"false"` | `False`
anything else (including `"-1"`) | `True`

To pass a parameter as a keyword argument,
use the `name=value` form:

```bash
duty docs serve=yes  # --> serve = True
```

You can use your own custom types as well:

```python
class Point:
    def __init__(self, xy: str):
        self.x, self.y = xy.split(",")

@duty
def shoot(ctx, point: Point):
    ctx.run(f"shoot -x {point.x} -y {point.y}")
```

Then, when running the duty:

```bash
duty shoot point=5,15
```

You can also pass parameters as positional arguments:

```bash
duty shoot 5,15
```

!!! warning "Limitation with positional arguments"
    When passing positional arguments,
    make sure there is no overlap between other duties' names
    and the argument value, otherwise `duty` will not be able
    to parse the command correctly.

### Passing options

Usage summary:

```
duty [GLOBAL_OPTS...] [DUTY [DUTY_OPTS...] [DUTY_PARAMS...]...]
```

#### Global options

The `duty` command line tool accepts global options
that will affect all the duties selected to run.
These options are the same you can use in `ctx.run()` calls,
except for `number` and `title` (because it wouldn't make sense).

The specified global options will *override* the default options
of duties, as well as the options passed in `ctx.run()` calls!

For example, with a duty declaring these options:

```python
@duty(capture="both")
def play(ctx, file):
    ctx.run(f"play {file}", nofail=True)
```

...you can override both the `capture` and `nofail` options like this:

```bash
duty --capture=none --strict play this-file.mp4
# or with the short options
duty -Zc none play this-file.mp4 
```

#### Local options

Local options are the same as global options.
Instead of passing them to `duty` directly,
you can pass them to a specific duty on the command line.
If we use the previous example again:

```bash
duty play -Zc none this-file.mp4 
```

It allows to use different options for different duties
selected on the command line.
In the following example, the `format` and `check` duties
will have their output captured,
while the `test` duty will not:

```bash
duty -cboth format check test -cnone
```

#### Preventing options overrides from the CLI

If for some reason you would like to prevent the ability
to override an option with the command line global or local options,
pass `allow_overrides=False` to your `ctx.run()` call,
or even to your `ctx.options()` context manager:

```python
@duty
def run_scripts(ctx):
    # no option can be changed from the CLI for the following run
    ctx.run("bash script1.sh", quiet=False, allow_overrides=False)

    # not for these runs either
    with ctx.options(nofail=True, allow_overrides=False):
        ctx.run("bash script2.sh")
        ctx.run("bash script3.sh")
```

### Capturing commands output

When running a command through `ctx.run()`,
you can choose to capture its standard output,
its standard error, both, or none.

Captured output is then available as an `output`
variable when [formatting duty's output](#formatting-duty-ouput).

- `capture=stdout` will capture *both* stdout and stderr,
  but will only make *stdout* available while formatting
- `capture=stderr` will capture *both* stdout and stderr,
  but will only make *stderr* available while formatting
- `capture=both` will capture both stdout and stderr as one single stream,
  and will make it available while formatting
- `capture=none` will not capture anything, and both stdout and stderr
  *will be printed in real-time to the console*

It is not possible to capture only stdout, or only stderr,
and let the other one be printed to the console.
Capturing one is capturing both, but discarding the other.

### Formatting duty output

Thanks to its underlying [`failprint`](https://github.com/pawamoy/failprint) dependency,
it is possible to change the output of command runs.
The output of a command is rendered using a Jinja template string.
For example, the two builtin `failprint` formats are:

- `pretty` (default)
  ```jinja
  {% if success %}<green>✓</green>
  {% elif nofail %}<yellow>✗</yellow>
  {% else %}<red>✗</red>{% endif %} 
  <bold>{{ title or command }}</bold>
  {% if failure %} ({{ code }}){% endif %}
  {% if failure and output and not quiet %}\n
  {{ ('  > ' + command + '\n') if title else '' }}
  {{ output|indent(2 * ' ') }}{% endif %}
  ```
  Its "progress" template is `> {{ title or command }}`.

- `tap`
  ```jinja
  {% if failure %}not {% endif %}ok {{ number }} - {{ title or command }}
  {% if failure and output %}\n  ---
  \n  {{ ('command: ' + command + '\n  ') if title else '' }}
  output: |\n{{ output|indent(4 * ' ') }}\n  ...{% endif %}
  ```

As you can see there are variables
you can use in your format template:

Variable | Description
-------- | -----------
`command` | A stringified version of the command.
`title` | The title passed with the `title` option.
`code` | The command exit status.
`success` | A boolean indicating if the command succeeded.
`failure` | A boolean indicating if the command failed.
`number` | The command number passed with the `number` option.
`output` | The command output (stdout, stderr, both or none, depending on the `capture` option).
`nofail` | A boolean indicating if the command was allowed to fail.
`quiet` | A boolean instructing to be quiet, i.e. don't print the command output even if it failed.
`silent` | A boolean indicating to be silent, i.e. don't print anything.


There is also one Jinja filter available

Filter | Description
------ | -----------
`indent` | The [`textwrap.indent`](https://docs.python.org/3/library/textwrap.html#textwrap.indent) function

To select a different format than the default one,
or to provide your own, you can use the `fmt` option
of `ctx.run()`, the `--format` CLI option (global and local),
and the `FAILPRINT_FORMAT` environment variable.

For example, here is how to use the `tap` format:

```python
# in the ctx.run() call
@duty
def task1(ctx):
    ctx.run("echo failed && false", fmt="tap")


# or as a default duty option
@duty(fmt="tap")
def task2(ctx):
    ctx.run("echo failed && false")
    ctx.run("echo failed && false")
```

```bash
# or with the CLI global option
duty --format tap task1 task2

# or with a CLI local option
duty task1 -ftap task2

# or with an environment variable
FAILPRINT_FORMAT=tap duty task1 task2
```

To use your own format template,
just make the value of the `fmt` option
start with `custom=`. For example,
with an environment variable:

```bash
export FAILPRINT_FORMAT="custom={{output}}"
# always print the captured output, nothing else

duty task1 task2
```