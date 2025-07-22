---
hide:
- navigation
---

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

The above duty runs the command in a shell process.
To avoid using a shell, pass a list of strings instead:

```python
from duty import duty


@duty
def docs(ctx):
    ctx.run(["mkdocs", "build"], title="Building documentation")
    # avoid the overhead of an extra shell process
```

And to avoid using a subprocess completely, pass a Python callable:

```python
from duty import duty
from mkdocs import build, config


@duty
def docs(ctx):
    ctx.run(build.build, args=[config.load_config()], title="Building documentation")
    # avoid the overhead of an extra Python process
```

For convenience, `duty` provides callables (called "tools") for many popular Python tools,
so that you don't have to read their source and learn how to call them.
For example, the `mkdocs build` command can be called like this:

```python
from duty import duty, tools


@duty
def docs(ctx):
    ctx.run(tool.mkdocs.build, kwargs={"strict": True}, title="Building documentation")
```

### Lazy callables

> TIP: **Our callables are lazy!**

Not only imports to third-party modules are deferred when our callables run,
but the callables themselves are lazy, meaning you can call them directly,
without passing arguments and keyword arguments
with the `args` and `kwargs` parameters of `ctx.run()`:

```python
from duty import duty, tools


@duty
def docs(ctx):
    ctx.run(tools.mkdocs.build(strict=True), title="Building documentation")
```

The main benefit is that it enables IDE features like help tooltips and auto-completion,
as well as improving readability and writability.

**[See all our tools in the Code reference][duty.tools].**

You can also create your own lazy callables with [`duty.Tool`][]
and [`duty.lazy`][].
Check out our tools to see how to create your own.

The `lazy` function/decorator is a quicker way
to create a lazy callable:

```python
from duty import duty, tools

from griffe.cli import check


@duty
def check_api(ctx):
    griffe_check = tools.lazy(check, name="griffe.check")
    ctx.run(griffe_check("pkg"))
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
stdin | `str` | Pass text to a command as standard input. | `None`
workdir | `str` | Change the working directory. | `None`
command | `str` | The shell command equivalent to `cmd`, to show how to run it without duty (useful when passing Python callables). | stringified `cmd`
allow_overrides | `bool` | Allow options overrides via CLI arguments. | `True`

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

### Saving the output of a command

In *duty* 0.7 (thanks to *failprint* 0.8),
the `run` method of the context objects always returns
the captured output of the command
(even when it also prints it on the standard output).
If nothing was captured, the returned output will be empty.

You can therefore use `ctx.run` as a shortcut to get
the output of a command.

Before *duty* 0.7:

```python
import subprocess

from duty import duty


@duty
def action(ctx):
    requirements = subprocess.run(
        ["pip", "freeze"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    ).output
    ...
```

With *duty* 0.7:

```python
from duty import duty


@duty
def action(ctx):
    requirements = ctx.run(["pip", "freeze"])
    ...
```

### Passing standard input to a command

*failprint* 0.8 introduced the ability to pass text as standard input to a command.
*duty* 0.7 takes advantage of this new *failprint* version,
and therefore allows you to do the same in your duties.

Before *duty* 0.7, to pass standard input to a command,
you had to write a shell command, for example:

```python
@duty
def check_dependencies(ctx):
    ctx.run(
        "pdm export -f requirements --without-hashes | safety check --stdin --full-report",
        title="Checking dependencies",
    )
```

This had a few issues:

- you had to use a shell command, which brings its lot of platform-and-shell-dependent issues, such as:
    - shell might not be the same everywhere
    - on Windows, there were high chances the `safety` executable would not be found

To fix the latter, you had to compute the absolute paths of all exectuables in the command before-hand
(except the first one, which *failprint* handles itself):

```python
@duty
def check_dependencies(ctx):
    safety = which("safety") or "safety"  # hope for the best
    ctx.run(
        f"pdm export -f requirements --without-hashes | {safety} check --stdin --full-report",
        title="Checking dependencies",
        pty=PTY,
    )
```

With *duty* 0.7, everything is easier and more robust
since you can save the output of a command in a variable,
and then pass this variable as standard input to another command!
This allows to write commands as lists of strings
(better cross-platform support, less resource-consuming),
and reuse the output of one command as input of several others:

```python
@duty
def check_dependencies(ctx):
    requirements = ctx.run(
        ["pdm", "export", "-f", "requirements", "--without-hashes"],
        title="Exporting dependencies as requirements",
        allow_overrides=False,
        # this is a preparation command that must not be altered
        # by CLI options targetted at the next commands,
        # see "Preventing options overrides"
    )
    ctx.run(
        ["safety", "check", "--stdin", "--full-report"],
        title="Checking dependencies",
        stdin=requirements,
    )
    ctx.run(
        ["other", "command", "using", "requirements"],
        title="Checking one more thing",
        stdin=requirements,
    )
```

### Pre/post duties

Each duty can be configured to run other duties before or after itself,
with the `pre` and `post` decorator options.

The `pre` and `post` options accept a list of other duties to run.
These other duties can be passed directly, or can be looked up
using their names. You can also pass any callable that accepts
a context argument, just like any duty.

For example, you can create a composite duty `check` that calls other,
more specific checking duties:

```python
# looking up duties thanks to their names, allowing to reference duties
# that have not yet been declared in the collection
@duty(pre=["check_quality", "check_types", "check_docs", "check_dependencies"])
def check(ctx):
    """Check it all!"""
```

Or you can make sure to always run the `clean` duty before running your tests,
and print a coverage report after running them:

```python
@duty
def clean(ctx):
    ctx.run("rm -rf tests/tmp")


@duty
def coverage(ctx):
    ctx.run("coverage combine", nofail=True)
    ctx.run("coverage report", capture=False)


@duty(pre=[clean], post=[coverage])
def test(ctx):
    ctx.run("pytest tests")
```

> IMPORTANT: The pre/post duties will be passed the context of the running duty.
> This allows to alter the behavior in both the running duties, as well as its pre/post duties.
> If you wish to run the pre/post duties with unaltered context, you can pass a lambda
> that calls their `run` method:
>
> ```python
> @duty(nofail=True, capture=False)
> def coverage(ctx):
>     ctx.run("coverage combine")
>     ctx.run("coverage report")
>
>
> @duty(post=[lambda ctx: coverage.run()])
> def test(ctx):
>     ctx.run("pytest tests")
> ```

### Defining aliases

Duties can have aliases. By default, duty will create an alias
for each duty by replacing underscores with dashes.
It means that, even if you duty is called `check_docs`,
you can call it with `duty check-docs` on the command line,
or reference it using `check-docs` in pre/post duties.

If you wish to add more aliases to a duty (for example to provide shorter names),
use the decorator `aliases` option:

```python
@duty(aliases=["start", "up"])
def start_backend(ctx):
    ctx.run("docker-compose up")
```

With this example, you'll be able to start the backend with
any of the four equivalent commands:

```bash
duty start_backend
duty start-backend
duty start
duty up
```

### Skipping duties

You can tell duty to always skip a duty if a certain condition is met.
This feature is inspired by pytest's `skip_if` marker.

```python
@duty(
    skip_if=sys.version_info < (3, 8),
    skip_reason="Building docs is not supported on Python 3.7",
)
def docs(ctx):
    ctx.run("mkdocs build")
```

By default, `skip_reason` will be "duty: skipped" where "duty" is replaced
by the name of the duty.

## Listing duties

Once you have defined some duties, you can list them from the CLI
with the `-l`, `--list` option. Example:

```console
$ duty --list
  changelog             Update the changelog in-place with latest commits.
  check                 Check it all!
  check-api             Check for API breaking changes.
  check-dependencies    Check for vulnerabilities in dependencies.
  check-docs            Check if the documentation builds correctly.
  check-quality         Check the code quality.
  check-types           Check that the code is correctly typed.
  clean                 Delete temporary files.
  cov                   Report coverage as text and HTML.
  docs                  Serve the documentation (localhost:8000).
  docs-deploy           Deploy the documentation on GitHub pages.
  format                Run formatting tools on the code.
  release               Release a new Python package.
  test                  Run the test suite.
```

You can also show help for given duties with the `-h`, `--help` option:

```console
$ duty --help release
usage: duty release [-c {stdout,stderr,both,none}] [-f {pretty,tap}] [-y | -Y] [-p | -P] [-q | -Q] [-s | -S] [-z | -Z]

Release a new Python package.

Parameters:
    ctx: The context instance (passed automatically).
    version: The new version number to use.

options:
  -c {stdout,stderr,both,none}, --capture {stdout,stderr,both,none}
                        Which output to capture. Colors are supported with 'both' only, unless the command has a 'force color' option.
  -f {pretty,tap}, --fmt {pretty,tap}, --format {pretty,tap}
                        Output format. Pass your own Jinja2 template as a string with '-f custom=TEMPLATE'. Available variables: command, title (command or title passed with -t), code (exit
                        status), success (boolean), failure (boolean), number (command number passed with -n), output (command output), nofail (boolean), quiet (boolean), silent (boolean).
                        Available filters: indent (textwrap.indent).
  -y, --pty             Enable the use of a pseudo-terminal. PTY doesn't allow programs to use standard input.
  -Y, --no-pty          Disable the use of a pseudo-terminal. PTY doesn't allow programs to use standard input.
  -p, --progress        Print progress while running a command.
  -P, --no-progress     Don't print progress while running a command.
  -q, --quiet           Don't print the command output, even if it failed.
  -Q, --no-quiet        Print the command output when it fails.
  -s, --silent          Don't print anything.
  -S, --no-silent       Print output as usual.
  -z, --zero, --nofail  Don't fail. Always return a success (0) exit code.
  -Z, --no-zero, --strict
                        Return the original exit code.
```

It prints the docstring of the corresponding function
as well as all the duty options you can use (same options for every duties).

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
in the duty's signature. If there is no annotation
but a default value, it will be type-casted using
the type of the default value.

We support any type that is callable and accepts
one positional argument (a string), as well as
optional types (`Optional[...]`, `... | None`)
and union types (`Union[..., ...]`, `... | ...`).

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

WARNING: **Limitation with positional arguments.**
When passing positional arguments,
make sure there is no overlap between other duties' names
and the argument value, otherwise `duty` will not be able
to parse the command correctly.

If your duty accepts variadic positional arguments,
those can be passed too from the command line:

```python
@duty
def shout(ctx, *names):
    ctx.run(print, args=[f"{name.upper()}!" for name in names])
```

```bash
duty shout herbert marvin
```

This can also be used to pass additional CLI flags
to commands or duty tools. If the flags clash with
duty's own options, add `--` first:

```python
from duty import duty, tools

@duty
def docs(ctx, *cli_args) -> None:
    ctx.run(tools.mkdocs.serve().add_args(*cli_args), capture=False)
```

```bash
duty docs -- -vs -f mkdocs.yml
```

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

WARNING: **Windows quirks.** On Windows you might need to set the following environment variables to allow proper output capture: `PYTHONLEGACYWINDOWSSTDIO=1`, `PYTHONUTF8=1`, `PYTHONIOENCODING=UTF8`. If the `✓` and `✗` characters are mangled, try changing them by [customizing the output format](#formatting-duty-output).

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

### Shell completions

You can enable auto-completion in Bash with these commands:

```bash
completions_dir="${BASH_COMPLETION_USER_DIR:-${XDG_DATA_HOME:-$HOME/.local/share}/bash-completion}/completions"
mkdir -p "${completions_dir}"
duty --completion > "${completions_dir}/duty"
```

Only Bash is supported for now.
