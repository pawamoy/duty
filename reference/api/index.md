# duty

duty package.

A simple task runner.

Modules:

- **`callables`** – Module containing callables for many tools.
- **`cli`** – Deprecated. Import from duty directly.
- **`collection`** – Deprecated. Import from duty directly.
- **`context`** – Deprecated. Import from duty directly.
- **`decorator`** – Deprecated. Import from duty directly.
- **`exceptions`** – Deprecated. Import from duty directly.
- **`lazy`** – Deprecated. Import from failprint directly.
- **`tools`** – Our collection of tools.
- **`validation`** – Deprecated. Import from duty directly.

Classes:

- **`Collection`** – A collection of duties.
- **`Context`** – A simple context class.
- **`Duty`** – The main duty class.
- **`DutyFailure`** – An exception raised when a duty fails.
- **`LazyStderr`** – Lazy stderr buffer.
- **`LazyStdout`** – Lazy stdout buffer.
- **`ParamsCaster`** – A helper class to cast parameters based on a function's signature annotations.
- **`Tool`** – Base class for tools.

Functions:

- **`cast_arg`** – Cast an argument using a type annotation.
- **`create_duty`** – Register a duty in the collection.
- **`duty`** – Decorate a callable to transform it and register it as a duty.
- **`get_duty_parser`** – Get a duty-specific options parser.
- **`get_parser`** – Return the CLI argument parser.
- **`main`** – Run the main program.
- **`parse_args`** – Parse the positional and keyword arguments of a duty.
- **`parse_commands`** – Parse argument lists into ready-to-run duties.
- **`parse_options`** – Parse options for a duty.
- **`print_help`** – Print general help or duties help.
- **`specified_options`** – Cast an argparse Namespace into a dictionary of options.
- **`split_args`** – Split command line arguments into duty commands.
- **`to_bool`** – Convert a string to a boolean.
- **`validate`** – Validate positional and keyword arguments against a function.

Attributes:

- **`CmdType`** – Type of a command that can be run in a subprocess or as a Python callable.
- **`DutyListType`** – Type of a list of duties, which can be a list of strings, callables, or Duty instances.
- **`default_duties_file`** – Default path to the duties file, relative to the current working directory.
- **`empty`** – Empty value for a parameter's default value.

## CmdType

```
CmdType = Union[str, list[str], Callable]

```

Type of a command that can be run in a subprocess or as a Python callable.

## DutyListType

```
DutyListType = list[Union[str, Callable, 'Duty']]

```

Type of a list of duties, which can be a list of strings, callables, or Duty instances.

## default_duties_file

```
default_duties_file = 'duties.py'

```

Default path to the duties file, relative to the current working directory.

## empty

```
empty = empty

```

Empty value for a parameter's default value.

## Collection

```
Collection(path: str = default_duties_file)

```

A collection of duties.

Attributes:

- **`path`** – The path to the duties file.
- **`duties`** (`dict[str, Duty]`) – The list of duties.
- **`aliases`** (`dict[str, Duty]`) – A dictionary of aliases pointing to their respective duties.

Parameters:

- **`path`** (`str`, default: `default_duties_file` ) – The path to the duties file.

Methods:

- **`add`** – Add a duty to the collection.
- **`clear`** – Clear the collection.
- **`completion_candidates`** – Find shell completion candidates within this collection.
- **`format_help`** – Format a message listing the duties.
- **`get`** – Get a duty by its name or alias.
- **`load`** – Load duties from a Python file.
- **`names`** – Return the list of duties names and aliases.

Source code in `src/duty/_internal/collection.py`

```
def __init__(self, path: str = default_duties_file) -> None:
    """Initialize the collection.

    Parameters:
        path: The path to the duties file.
    """
    self.path = path
    """The path to the duties file."""
    self.duties: dict[str, Duty] = {}
    """The list of duties."""
    self.aliases: dict[str, Duty] = {}
    """A dictionary of aliases pointing to their respective duties."""

```

### aliases

```
aliases: dict[str, Duty] = {}

```

A dictionary of aliases pointing to their respective duties.

### duties

```
duties: dict[str, Duty] = {}

```

The list of duties.

### path

```
path = path

```

The path to the duties file.

### add

```
add(duty: Duty) -> None

```

Add a duty to the collection.

Parameters:

- **`duty`** (`Duty`) – The duty to add.

Source code in `src/duty/_internal/collection.py`

```
def add(self, duty: Duty) -> None:
    """Add a duty to the collection.

    Parameters:
        duty: The duty to add.
    """
    if duty.collection is not None:
        # we must copy the duty to be able to add it
        # in multiple collections
        duty = deepcopy(duty)
    duty.collection = self
    self.duties[duty.name] = duty
    for alias in duty.aliases:
        self.aliases[alias] = duty

```

### clear

```
clear() -> None

```

Clear the collection.

Source code in `src/duty/_internal/collection.py`

```
def clear(self) -> None:
    """Clear the collection."""
    self.duties.clear()
    self.aliases.clear()

```

### completion_candidates

```
completion_candidates(args: tuple[str, ...]) -> list[str]

```

Find shell completion candidates within this collection.

Returns:

- `list[str]` – The list of shell completion candidates, sorted alphabetically.

Source code in `src/duty/_internal/collection.py`

```
def completion_candidates(self, args: tuple[str, ...]) -> list[str]:
    """Find shell completion candidates within this collection.

    Returns:
        The list of shell completion candidates, sorted alphabetically.
    """
    # Find last duty name in args.
    name = None
    names = set(self.names())
    for arg in reversed(args):
        if arg in names:
            name = arg
            break

    completion_names = sorted(names)

    # If no duty found, return names.
    if name is None:
        return completion_names

    params = [
        f"{param.name}="
        for param in inspect.signature(self.get(name).function).parameters.values()
        if param.kind is not param.VAR_POSITIONAL
    ][1:]

    # If duty found, return names *and* duty parameters.
    return completion_names + sorted(params)

```

### format_help

```
format_help() -> str

```

Format a message listing the duties.

Returns:

- `str` – A string listing the duties and their summary.

Source code in `src/duty/_internal/collection.py`

```
def format_help(self) -> str:
    """Format a message listing the duties.

    Returns:
        A string listing the duties and their summary.
    """
    lines = []
    # 20 makes the summary aligned with options description
    longest_name = max(*(len(name) for name in self.duties), 20)
    for name, duty in self.duties.items():
        description = duty.description.split("\n")[0]
        lines.append(f"{name:{longest_name}}  {description}")
    return "\n".join(lines)

```

### get

```
get(name_or_alias: str) -> Duty

```

Get a duty by its name or alias.

Parameters:

- **`name_or_alias`** (`str`) – The name or alias of the duty.

Returns:

- `Duty` – A duty.

Source code in `src/duty/_internal/collection.py`

```
def get(self, name_or_alias: str) -> Duty:
    """Get a duty by its name or alias.

    Parameters:
        name_or_alias: The name or alias of the duty.

    Returns:
        A duty.
    """
    try:
        return self.duties[name_or_alias]
    except KeyError:
        return self.aliases[name_or_alias]

```

### load

```
load(path: str | None = None) -> None

```

Load duties from a Python file.

Parameters:

- **`path`** (`str | None`, default: `None` ) – The path to the Python file to load. Uses the collection's path by default.

Source code in `src/duty/_internal/collection.py`

```
def load(self, path: str | None = None) -> None:
    """Load duties from a Python file.

    Parameters:
        path: The path to the Python file to load.
            Uses the collection's path by default.
    """
    path = path or self.path
    spec = importlib_util.spec_from_file_location("duty.duties", path)
    if spec:
        duties = importlib_util.module_from_spec(spec)
        sys.modules["duty.duties"] = duties
        spec.loader.exec_module(duties)  # type: ignore[union-attr]
        declared_duties = inspect.getmembers(duties, lambda member: isinstance(member, Duty))
        for _, duty in declared_duties:
            self.add(duty)

```

### names

```
names() -> list[str]

```

Return the list of duties names and aliases.

Returns:

- `list[str]` – The list of duties names and aliases.

Source code in `src/duty/_internal/collection.py`

```
def names(self) -> list[str]:
    """Return the list of duties names and aliases.

    Returns:
        The list of duties names and aliases.
    """
    return list(self.duties.keys()) + list(self.aliases.keys())

```

## Context

```
Context(
    options: dict[str, Any],
    options_override: dict[str, Any] | None = None,
)

```

A simple context class.

Context instances are passed to functions decorated with `duty`.

Parameters:

- **`options`** (`dict[str, Any]`) – Base options specified in @duty(\*\*options).
- **`options_override`** (`dict[str, Any] | None`, default: `None` ) – Options that override run and @duty options. This argument is used to allow users to override options from the CLI or environment.

Methods:

- **`cd`** – Change working directory as a context manager.
- **`options`** – Change options as a context manager.
- **`run`** – Run a command in a subprocess or a Python callable.

Source code in `src/duty/_internal/context.py`

```
def __init__(self, options: dict[str, Any], options_override: dict[str, Any] | None = None) -> None:
    """Initialize the context.

    Parameters:
        options: Base options specified in `@duty(**options)`.
        options_override: Options that override `run` and `@duty` options.
            This argument is used to allow users to override options from the CLI or environment.
    """
    self._options = options
    self._option_stack: list[dict[str, Any]] = []
    self._options_override = options_override or {}

```

### cd

```
cd(directory: str) -> Iterator

```

Change working directory as a context manager.

Parameters:

- **`directory`** (`str`) – The directory to go into.

Yields:

- `Iterator` – Nothing.

Source code in `src/duty/_internal/context.py`

```
@contextmanager
def cd(self, directory: str) -> Iterator:
    """Change working directory as a context manager.

    Parameters:
        directory: The directory to go into.

    Yields:
        Nothing.
    """
    if not directory:
        yield
        return
    old_wd = os.getcwd()
    os.chdir(directory)
    try:
        yield
    finally:
        os.chdir(old_wd)

```

### options

```
options(**opts: Any) -> Iterator

```

Change options as a context manager.

Can be nested as will, previous options will pop once out of the with clause.

Parameters:

- **`**opts`** (`Any`, default: `{}` ) – Options used in run.

Yields:

- `Iterator` – Nothing.

Source code in `src/duty/_internal/context.py`

```
@contextmanager
def options(self, **opts: Any) -> Iterator:
    """Change options as a context manager.

    Can be nested as will, previous options will pop once out of the with clause.

    Parameters:
        **opts: Options used in `run`.

    Yields:
        Nothing.
    """
    self._option_stack.append(self._options)
    self._options = {**self._options, **opts}
    try:
        yield
    finally:
        self._options = self._option_stack.pop()

```

### run

```
run(cmd: CmdType, **options: Any) -> str

```

Run a command in a subprocess or a Python callable.

Parameters:

- **`cmd`** (`CmdType`) – A command or a Python callable.
- **`options`** (`Any`, default: `{}` ) – Options passed to failprint functions.

Raises:

- `DutyFailure` – When the exit code / function result is greather than 0.

Returns:

- `str` – The output of the command.

Source code in `src/duty/_internal/context.py`

```
def run(self, cmd: CmdType, **options: Any) -> str:
    """Run a command in a subprocess or a Python callable.

    Parameters:
        cmd: A command or a Python callable.
        options: Options passed to `failprint` functions.

    Raises:
        DutyFailure: When the exit code / function result is greather than 0.

    Returns:
        The output of the command.
    """
    final_options = dict(self._options)
    final_options.update(options)

    if "command" not in final_options and isinstance(cmd, Tool):
        with suppress(ValueError):
            final_options["command"] = cmd.cli_command

    allow_overrides = final_options.pop("allow_overrides", True)
    workdir = final_options.pop("workdir", None)

    if allow_overrides:
        final_options.update(self._options_override)

    with self.cd(workdir):
        try:
            result = failprint_run(cmd, **final_options)
        except KeyboardInterrupt as ki:
            raise DutyFailure(130) from ki

    if result.code:
        raise DutyFailure(result.code)

    return result.output

```

## Duty

```
Duty(
    name: str,
    description: str,
    function: Callable,
    collection: Collection | None = None,
    aliases: set | None = None,
    pre: DutyListType | None = None,
    post: DutyListType | None = None,
    opts: dict[str, Any] | None = None,
)

```

The main duty class.

Parameters:

- **`name`** (`str`) – The duty name.
- **`description`** (`str`) – The duty description.
- **`function`** (`Callable`) – The duty function.
- **`collection`** (`Collection | None`, default: `None` ) – The collection on which to attach this duty.
- **`aliases`** (`set | None`, default: `None` ) – A list of aliases for this duty.
- **`pre`** (`DutyListType | None`, default: `None` ) – A list of duties to run before this one.
- **`post`** (`DutyListType | None`, default: `None` ) – A list of duties to run after this one.
- **`opts`** (`dict[str, Any] | None`, default: `None` ) – Options used to create the context instance.

Methods:

- **`__call__`** – Run the duty function.
- **`run`** – Run the duty.
- **`run_duties`** – Run a list of duties.

Attributes:

- **`aliases`** – A set of aliases for this duty.
- **`collection`** (`Collection | None`) – The collection on which this duty is attached.
- **`context`** (`Context`) – Return a new context instance.
- **`default_options`** (`dict[str, Any]`) – Default options used to create the context instance.
- **`description`** – The duty description.
- **`function`** – The duty function.
- **`name`** – The duty name.
- **`options`** – Options used to create the context instance.
- **`options_override`** (`dict`) – Options that override run and @duty options.
- **`post`** – A list of duties to run after this one.
- **`pre`** – A list of duties to run before this one.

Source code in `src/duty/_internal/collection.py`

```
def __init__(
    self,
    name: str,
    description: str,
    function: Callable,
    collection: Collection | None = None,
    aliases: set | None = None,
    pre: DutyListType | None = None,
    post: DutyListType | None = None,
    opts: dict[str, Any] | None = None,
) -> None:
    """Initialize the duty.

    Parameters:
        name: The duty name.
        description: The duty description.
        function: The duty function.
        collection: The collection on which to attach this duty.
        aliases: A list of aliases for this duty.
        pre: A list of duties to run before this one.
        post: A list of duties to run after this one.
        opts: Options used to create the context instance.
    """
    self.name = name
    """The duty name."""
    self.description = description
    """The duty description."""
    self.function = function
    """The duty function."""
    self.aliases = aliases or set()
    """A set of aliases for this duty."""
    self.pre = pre or []
    """A list of duties to run before this one."""
    self.post = post or []
    """A list of duties to run after this one."""
    self.options = opts or self.default_options
    """Options used to create the context instance."""
    self.options_override: dict = {}
    """Options that override `run` and `@duty` options."""

    self.collection: Collection | None = None
    """The collection on which this duty is attached."""
    if collection:
        collection.add(self)

```

### aliases

```
aliases = aliases or set()

```

A set of aliases for this duty.

### collection

```
collection: Collection | None = None

```

The collection on which this duty is attached.

### context

```
context: Context

```

Return a new context instance.

Returns:

- `Context` – A new context instance.

### default_options

```
default_options: dict[str, Any] = {}

```

Default options used to create the context instance.

### description

```
description = description

```

The duty description.

### function

```
function = function

```

The duty function.

### name

```
name = name

```

The duty name.

### options

```
options = opts or default_options

```

Options used to create the context instance.

### options_override

```
options_override: dict = {}

```

Options that override `run` and `@duty` options.

### post

```
post = post or []

```

A list of duties to run after this one.

### pre

```
pre = pre or []

```

A list of duties to run before this one.

### __call__

```
__call__(
    context: Context, *args: Any, **kwargs: Any
) -> None

```

Run the duty function.

Parameters:

- **`context`** (`Context`) – The context to use.
- **`args`** (`Any`, default: `()` ) – Positional arguments passed to the function.
- **`kwargs`** (`Any`, default: `{}` ) – Keyword arguments passed to the function.

Source code in `src/duty/_internal/collection.py`

```
def __call__(self, context: Context, *args: Any, **kwargs: Any) -> None:
    """Run the duty function.

    Parameters:
        context: The context to use.
        args: Positional arguments passed to the function.
        kwargs: Keyword arguments passed to the function.
    """
    self.run_duties(context, self.pre)
    self.function(context, *args, **kwargs)
    self.run_duties(context, self.post)

```

### run

```
run(*args: Any, **kwargs: Any) -> None

```

Run the duty.

This is just a shortcut for `duty(duty.context, *args, **kwargs)`.

Parameters:

- **`args`** (`Any`, default: `()` ) – Positional arguments passed to the function.
- **`kwargs`** (`Any`, default: `{}` ) – Keyword arguments passed to the function.

Source code in `src/duty/_internal/collection.py`

```
def run(self, *args: Any, **kwargs: Any) -> None:
    """Run the duty.

    This is just a shortcut for `duty(duty.context, *args, **kwargs)`.

    Parameters:
        args: Positional arguments passed to the function.
        kwargs: Keyword arguments passed to the function.
    """
    self(self.context, *args, **kwargs)

```

### run_duties

```
run_duties(
    context: Context, duties_list: DutyListType
) -> None

```

Run a list of duties.

Parameters:

- **`context`** (`Context`) – The context to use.
- **`duties_list`** (`DutyListType`) – The list of duties to run.

Raises:

- `RuntimeError` – When a duty name is given to pre or post duties. Indeed, without a parent collection, it is impossible to find another duty by its name.

Source code in `src/duty/_internal/collection.py`

```
def run_duties(self, context: Context, duties_list: DutyListType) -> None:
    """Run a list of duties.

    Parameters:
        context: The context to use.
        duties_list: The list of duties to run.

    Raises:
        RuntimeError: When a duty name is given to pre or post duties.
            Indeed, without a parent collection, it is impossible
            to find another duty by its name.
    """
    for duty_item in duties_list:
        if callable(duty_item):
            # Item is a proper duty, or a callable: run it.
            duty_item(context)
        elif isinstance(duty_item, str):
            # Item is a reference to a duty.
            if self.collection is None:
                raise RuntimeError(f"Can't find duty by name without a collection ({duty_item})")
            # Get the duty and run it.
            self.collection.get(duty_item)(context)

```

## DutyFailure

```
DutyFailure(code: int)

```

Bases: `Exception`

An exception raised when a duty fails.

Parameters:

- **`code`** (`int`) – The exit code of a command.

Attributes:

- **`code`** – The exit code of the command that failed.

Source code in `src/duty/_internal/exceptions.py`

```
def __init__(self, code: int) -> None:
    """Initialize the object.

    Parameters:
        code: The exit code of a command.
    """
    super().__init__(self)
    self.code = code
    """The exit code of the command that failed."""

```

### code

```
code = code

```

The exit code of the command that failed.

## LazyStderr

Bases: `StringIO`

Lazy stderr buffer.

Can be used when tools' main entry-points expect a file-like object for stderr.

Methods:

- **`write`** – Write a string to the stderr buffer.

### write

```
write(value: str) -> int

```

Write a string to the stderr buffer.

Source code in `src/duty/_internal/tools/_base.py`

```
def write(self, value: str) -> int:
    """Write a string to the stderr buffer."""
    return sys.stderr.write(value)

```

## LazyStdout

Bases: `StringIO`

Lazy stdout buffer.

Can be used when tools' main entry-points expect a file-like object for stdout.

Methods:

- **`write`** – Write a string to the stdout buffer.

### write

```
write(value: str) -> int

```

Write a string to the stdout buffer.

Source code in `src/duty/_internal/tools/_base.py`

```
def write(self, value: str) -> int:
    """Write a string to the stdout buffer."""
    return sys.stdout.write(value)

```

## ParamsCaster

```
ParamsCaster(signature: Signature)

```

A helper class to cast parameters based on a function's signature annotations.

Parameters:

- **`signature`** (`Signature`) – The signature to use to cast arguments.

Methods:

- **`annotation_at_pos`** – Give the annotation for the parameter at the given position.
- **`cast`** – Cast all positional and keyword arguments.
- **`cast_kwarg`** – Cast a keyword argument.
- **`cast_posarg`** – Cast a positional argument.
- **`eaten_by_var_positional`** – Tell if the parameter at this position is eaten by a variable positional parameter.

Attributes:

- **`has_var_positional`** (`bool`) – Tell if there is a variable positional parameter.
- **`params_dict`** – A dictionary of parameters, indexed by their name.
- **`params_list`** – A list of parameters, in the order they appear in the signature.
- **`var_keyword_annotation`** (`Any`) – Give the variable keyword parameter (\*\*kwargs) annotation if any.
- **`var_positional_annotation`** (`Any`) – Give the variable positional parameter (\*args) annotation if any.
- **`var_positional_position`** (`int`) – Give the position of the variable positional parameter in the signature.

Source code in `src/duty/_internal/validation.py`

```
def __init__(self, signature: Signature) -> None:
    """Initialize the object.

    Parameters:
        signature: The signature to use to cast arguments.
    """
    self.params_dict = signature.parameters
    """A dictionary of parameters, indexed by their name."""
    self.params_list = list(self.params_dict.values())
    """A list of parameters, in the order they appear in the signature."""

```

### has_var_positional

```
has_var_positional: bool

```

Tell if there is a variable positional parameter.

Returns:

- `bool` – True or False.

### params_dict

```
params_dict = parameters

```

A dictionary of parameters, indexed by their name.

### params_list

```
params_list = list(values())

```

A list of parameters, in the order they appear in the signature.

### var_keyword_annotation

```
var_keyword_annotation: Any

```

Give the variable keyword parameter (`**kwargs`) annotation if any.

Returns:

- `Any` – The variable keyword parameter annotation.

### var_positional_annotation

```
var_positional_annotation: Any

```

Give the variable positional parameter (`*args`) annotation if any.

Returns:

- `Any` – The variable positional parameter annotation.

### var_positional_position

```
var_positional_position: int

```

Give the position of the variable positional parameter in the signature.

Returns:

- `int` – The position of the variable positional parameter.

### annotation_at_pos

```
annotation_at_pos(pos: int) -> Any

```

Give the annotation for the parameter at the given position.

Parameters:

- **`pos`** (`int`) – The position of the parameter.

Returns:

- `Any` – The positional parameter annotation.

Source code in `src/duty/_internal/validation.py`

```
def annotation_at_pos(self, pos: int) -> Any:
    """Give the annotation for the parameter at the given position.

    Parameters:
        pos: The position of the parameter.

    Returns:
        The positional parameter annotation.
    """
    return self.params_list[pos].annotation

```

### cast

```
cast(
    *args: Any, **kwargs: Any
) -> tuple[Sequence, dict[str, Any]]

```

Cast all positional and keyword arguments.

Parameters:

- **`*args`** (`Any`, default: `()` ) – The positional arguments.
- **`**kwargs`** (`Any`, default: `{}` ) – The keyword arguments.

Returns:

- `tuple[Sequence, dict[str, Any]]` – The cast arguments.

Source code in `src/duty/_internal/validation.py`

```
def cast(self, *args: Any, **kwargs: Any) -> tuple[Sequence, dict[str, Any]]:
    """Cast all positional and keyword arguments.

    Parameters:
        *args: The positional arguments.
        **kwargs: The keyword arguments.

    Returns:
        The cast arguments.
    """
    positional = tuple(self.cast_posarg(pos, arg) for pos, arg in enumerate(args))
    keyword = {name: self.cast_kwarg(name, value) for name, value in kwargs.items()}
    return positional, keyword

```

### cast_kwarg

```
cast_kwarg(name: str, value: Any) -> Any

```

Cast a keyword argument.

Parameters:

- **`name`** (`str`) – The name of the argument in the signature.
- **`value`** (`Any`) – The argument value.

Returns:

- `Any` – The cast value.

Source code in `src/duty/_internal/validation.py`

```
def cast_kwarg(self, name: str, value: Any) -> Any:
    """Cast a keyword argument.

    Parameters:
        name: The name of the argument in the signature.
        value: The argument value.

    Returns:
        The cast value.
    """
    if name in self.params_dict:
        return cast_arg(value, self.params_dict[name].annotation)
    return cast_arg(value, self.var_keyword_annotation)

```

### cast_posarg

```
cast_posarg(pos: int, arg: Any) -> Any

```

Cast a positional argument.

Parameters:

- **`pos`** (`int`) – The position of the argument in the signature.
- **`arg`** (`Any`) – The argument value.

Returns:

- `Any` – The cast value.

Source code in `src/duty/_internal/validation.py`

```
def cast_posarg(self, pos: int, arg: Any) -> Any:
    """Cast a positional argument.

    Parameters:
        pos: The position of the argument in the signature.
        arg: The argument value.

    Returns:
        The cast value.
    """
    if self.eaten_by_var_positional(pos):
        return cast_arg(arg, self.var_positional_annotation)
    return cast_arg(arg, self.annotation_at_pos(pos))

```

### eaten_by_var_positional

```
eaten_by_var_positional(pos: int) -> bool

```

Tell if the parameter at this position is eaten by a variable positional parameter.

Parameters:

- **`pos`** (`int`) – The position of the parameter.

Returns:

- `bool` – Whether the parameter is eaten.

Source code in `src/duty/_internal/validation.py`

```
def eaten_by_var_positional(self, pos: int) -> bool:
    """Tell if the parameter at this position is eaten by a variable positional parameter.

    Parameters:
        pos: The position of the parameter.

    Returns:
        Whether the parameter is eaten.
    """
    return self.has_var_positional and pos >= self.var_positional_position

```

## Tool

```
Tool(
    cli_args: list[str] | None = None,
    py_args: dict[str, Any] | None = None,
)

```

Base class for tools.

Parameters:

- **`cli_args`** (`list[str] | None`, default: `None` ) – Initial command-line arguments. Use add_args() to add more.
- **`py_args`** (`dict[str, Any] | None`, default: `None` ) – Python arguments. Your __call__ method will be able to access these arguments as self.py_args.

Methods:

- **`add_args`** – Append CLI arguments.

Attributes:

- **`cli_args`** (`list[str]`) – Registered command-line arguments.
- **`cli_command`** (`str`) – The equivalent CLI command.
- **`cli_name`** (`str`) – The name of the executable on PATH.
- **`py_args`** (`dict[str, Any]`) – Registered Python arguments.

Source code in `src/duty/_internal/tools/_base.py`

```
def __init__(
    self,
    cli_args: list[str] | None = None,
    py_args: dict[str, Any] | None = None,
) -> None:
    """Initialize the tool.

    Parameters:
        cli_args: Initial command-line arguments. Use `add_args()` to add more.
        py_args: Python arguments. Your `__call__` method will be able to access
            these arguments as `self.py_args`.
    """
    self.cli_args: list[str] = cli_args or []
    """Registered command-line arguments."""
    self.py_args: dict[str, Any] = py_args or {}
    """Registered Python arguments."""

```

### cli_args

```
cli_args: list[str] = cli_args or []

```

Registered command-line arguments.

### cli_command

```
cli_command: str

```

The equivalent CLI command.

### cli_name

```
cli_name: str = ''

```

The name of the executable on PATH.

### py_args

```
py_args: dict[str, Any] = py_args or {}

```

Registered Python arguments.

### add_args

```
add_args(*args: str) -> Self

```

Append CLI arguments.

Source code in `src/duty/_internal/tools/_base.py`

```
def add_args(self, *args: str) -> Self:
    """Append CLI arguments."""
    self.cli_args.extend(args)
    return self

```

## cast_arg

```
cast_arg(arg: Any, annotation: Any) -> Any

```

Cast an argument using a type annotation.

Parameters:

- **`arg`** (`Any`) – The argument value.
- **`annotation`** (`Any`) – A type annotation.

Returns:

- `Any` – The cast value.

Source code in `src/duty/_internal/validation.py`

```
def cast_arg(arg: Any, annotation: Any) -> Any:
    """Cast an argument using a type annotation.

    Parameters:
        arg: The argument value.
        annotation: A type annotation.

    Returns:
        The cast value.
    """
    if annotation is Parameter.empty:
        return arg
    if annotation is bool:
        annotation = to_bool
    if get_origin(annotation) in _union_types:
        for sub_annotation in get_args(annotation):
            if sub_annotation is type(None):
                continue
            with suppress(Exception):
                return cast_arg(arg, sub_annotation)
    try:
        return annotation(arg)
    except Exception:  # noqa: BLE001
        return arg

```

## create_duty

```
create_duty(
    func: Callable,
    *,
    name: str | None = None,
    aliases: Iterable[str] | None = None,
    pre: DutyListType | None = None,
    post: DutyListType | None = None,
    skip_if: bool = False,
    skip_reason: str | None = None,
    **opts: Any,
) -> Duty

```

Register a duty in the collection.

Parameters:

- **`func`** (`Callable`) – The callable to register as a duty.
- **`name`** (`str | None`, default: `None` ) – The duty name.
- **`aliases`** (`Iterable[str] | None`, default: `None` ) – A set of aliases for this duty.
- **`pre`** (`DutyListType | None`, default: `None` ) – Pre-duties.
- **`post`** (`DutyListType | None`, default: `None` ) – Post-duties.
- **`skip_if`** (`bool`, default: `False` ) – Skip running the duty if the given condition is met.
- **`skip_reason`** (`str | None`, default: `None` ) – Custom message when skipping.
- **`opts`** (`Any`, default: `{}` ) – Options passed to the context.

Returns:

- `Duty` – The registered duty.

Source code in `src/duty/_internal/decorator.py`

```
def create_duty(
    func: Callable,
    *,
    name: str | None = None,
    aliases: Iterable[str] | None = None,
    pre: DutyListType | None = None,
    post: DutyListType | None = None,
    skip_if: bool = False,
    skip_reason: str | None = None,
    **opts: Any,
) -> Duty:
    """Register a duty in the collection.

    Parameters:
        func: The callable to register as a duty.
        name: The duty name.
        aliases: A set of aliases for this duty.
        pre: Pre-duties.
        post: Post-duties.
        skip_if: Skip running the duty if the given condition is met.
        skip_reason: Custom message when skipping.
        opts: Options passed to the context.

    Returns:
        The registered duty.
    """
    aliases = set(aliases) if aliases else set()
    name = name or func.__name__
    dash_name = name.replace("_", "-")
    if name != dash_name:
        aliases.add(name)
        name = dash_name
    description = inspect.getdoc(func) or ""
    if skip_if:
        func = _skip(func, skip_reason or f"{dash_name}: skipped")
    duty = Duty(name, description, func, aliases=aliases, pre=pre, post=post, opts=opts)
    duty.__name__ = name  # type: ignore[attr-defined]
    duty.__doc__ = description
    duty.__wrapped__ = func  # type: ignore[attr-defined]
    return duty

```

## duty

```
duty(**kwargs: Any) -> Callable[[Callable], Duty]

```

```
duty(func: Callable) -> Duty

```

```
duty(*args: Any, **kwargs: Any) -> Callable | Duty

```

Decorate a callable to transform it and register it as a duty.

Parameters:

- **`args`** (`Any`, default: `()` ) – One callable.
- **`kwargs`** (`Any`, default: `{}` ) – Context options.

Raises:

- `ValueError` – When the decorator is misused.

Examples:

Decorate a function:

```
@duty
def clean(ctx):
    ctx.run("rm -rf build", silent=True)

```

Pass options to the context:

```
@duty(silent=True)
def clean(ctx):
    ctx.run("rm -rf build")  # silent=True is implied

```

Returns:

- `Callable | Duty` – A duty when used without parentheses, a decorator otherwise.

Source code in `src/duty/_internal/decorator.py`

````
def duty(*args: Any, **kwargs: Any) -> Callable | Duty:
    """Decorate a callable to transform it and register it as a duty.

    Parameters:
        args: One callable.
        kwargs: Context options.

    Raises:
        ValueError: When the decorator is misused.

    Examples:
        Decorate a function:

        ```python
        @duty
        def clean(ctx):
            ctx.run("rm -rf build", silent=True)
        ```

        Pass options to the context:

        ```python
        @duty(silent=True)
        def clean(ctx):
            ctx.run("rm -rf build")  # silent=True is implied
        ```

    Returns:
        A duty when used without parentheses, a decorator otherwise.
    """
    if args:
        if len(args) > 1:
            raise ValueError("The duty decorator accepts only one positional argument")
        return create_duty(args[0], **kwargs)

    def decorator(func: Callable) -> Duty:
        return create_duty(func, **kwargs)

    return decorator

````

## get_duty_parser

```
get_duty_parser(duty: Duty) -> ArgParser

```

Get a duty-specific options parser.

Parameters:

- **`duty`** (`Duty`) – The duty to parse for.

Returns:

- `ArgParser` – A duty-specific parser.

Source code in `src/duty/_internal/cli.py`

```
def get_duty_parser(duty: Duty) -> ArgParser:
    """Get a duty-specific options parser.

    Parameters:
        duty: The duty to parse for.

    Returns:
        A duty-specific parser.
    """
    parser = ArgParser(
        prog=f"duty {duty.name}",
        add_help=False,
        description=duty.description,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    add_flags(parser, set_defaults=False)
    return parser

```

## get_parser

```
get_parser() -> ArgParser

```

Return the CLI argument parser.

Returns:

- `ArgParser` – An argparse parser.

Source code in `src/duty/_internal/cli.py`

```
def get_parser() -> ArgParser:
    """Return the CLI argument parser.

    Returns:
        An argparse parser.
    """
    usage = "duty [GLOBAL_OPTS...] [DUTY [DUTY_OPTS...] [DUTY_PARAMS...]...]"
    description = "A simple task runner."
    parser = ArgParser(add_help=False, usage=usage, description=description)

    parser.add_argument(
        "-d",
        "--duties-file",
        default="duties.py",
        help="Python file where the duties are defined.",
    )
    parser.add_argument(
        "-l",
        "--list",
        action="store_true",
        dest="list",
        help="List the available duties.",
    )
    parser.add_argument(
        "-h",
        "--help",
        dest="help",
        nargs="*",
        metavar="DUTY",
        help="Show this help message and exit. Pass duties names to print their help.",
    )
    parser.add_argument(
        "--completion",
        dest="completion",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--complete",
        dest="complete",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    parser.add_argument("-V", "--version", action="version", version=f"%(prog)s {debug._get_version()}")
    parser.add_argument("--debug-info", action=_DebugInfo, help="Print debug information.")

    add_flags(parser, set_defaults=False)
    parser.add_argument("remainder", nargs=argparse.REMAINDER)

    parser._optionals.title = "Global options"

    return parser

```

## main

```
main(args: list[str] | None = None) -> int

```

Run the main program.

This function is executed when you type `duty` or `python -m duty`.

Parameters:

- **`args`** (`list[str] | None`, default: `None` ) – Arguments passed from the command line.

Returns:

- `int` – An exit code.

Source code in `src/duty/_internal/cli.py`

```
def main(args: list[str] | None = None) -> int:
    """Run the main program.

    This function is executed when you type `duty` or `python -m duty`.

    Parameters:
        args: Arguments passed from the command line.

    Returns:
        An exit code.
    """
    parser = get_parser()
    opts = parser.parse_args(args=args)
    remainder = opts.remainder

    collection = Collection(opts.duties_file)
    collection.load()

    if opts.completion:
        print(Path(__file__).parent.joinpath("completions.bash").read_text())
        return 0

    if opts.complete:
        words = collection.completion_candidates(remainder)
        words += sorted(
            opt for opt, action in parser._option_string_actions.items() if action.help != argparse.SUPPRESS
        )
        print(*words, sep="\n")
        return 0

    if opts.help is not None:
        print_help(parser, opts, collection)
        return 0

    if opts.list:
        print(textwrap.indent(collection.format_help(), prefix="  "))
        return 0

    try:
        arg_lists = split_args(remainder, collection.names())
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1

    if not arg_lists:
        print_help(parser, opts, collection)
        return 1

    global_opts = specified_options(
        opts,
        exclude={"duties_file", "list", "help", "remainder", "complete", "completion"},
    )
    try:
        commands = parse_commands(arg_lists, global_opts, collection)
    except TypeError as error:
        print(f"> {error}", file=sys.stderr)
        return 1

    for duty, posargs, kwargs in commands:
        try:
            duty.run(*posargs, **kwargs)
        except DutyFailure as failure:
            return failure.code

    return 0

```

## parse_args

```
parse_args(duty: Duty, args: list[str]) -> tuple

```

Parse the positional and keyword arguments of a duty.

Parameters:

- **`duty`** (`Duty`) – The duty to parse for.
- **`args`** (`list[str]`) – The list of arguments.

Returns:

- `tuple` – The positional and keyword arguments.

Source code in `src/duty/_internal/cli.py`

```
def parse_args(duty: Duty, args: list[str]) -> tuple:
    """Parse the positional and keyword arguments of a duty.

    Parameters:
        duty: The duty to parse for.
        args: The list of arguments.

    Returns:
        The positional and keyword arguments.
    """
    posargs = []
    kwargs = {}

    for arg in args:
        if "=" in arg:
            # we found a keyword argument
            arg_name, arg_value = arg.split("=", 1)
            kwargs[arg_name] = arg_value
        else:
            # we found a positional argument
            posargs.append(arg)

    return validate(duty.function, *posargs, **kwargs)

```

## parse_commands

```
parse_commands(
    arg_lists: list[list[str]],
    global_opts: dict[str, Any],
    collection: Collection,
) -> list[tuple]

```

Parse argument lists into ready-to-run duties.

Parameters:

- **`arg_lists`** (`list[list[str]]`) – Lists of arguments lists.
- **`global_opts`** (`dict[str, Any]`) – The global options.
- **`collection`** (`Collection`) – The duties collection.

Returns:

- `list[tuple]` – A list of tuples composed of: a duty its positional arguments its keyword arguments

Source code in `src/duty/_internal/cli.py`

```
def parse_commands(arg_lists: list[list[str]], global_opts: dict[str, Any], collection: Collection) -> list[tuple]:
    """Parse argument lists into ready-to-run duties.

    Parameters:
        arg_lists: Lists of arguments lists.
        global_opts: The global options.
        collection: The duties collection.

    Returns:
        A list of tuples composed of:

            - a duty
            - its positional arguments
            - its keyword arguments
    """
    commands = []
    for arg_list in arg_lists:
        duty = collection.get(arg_list[0])
        opts, remainder = parse_options(duty, arg_list[1:])
        if remainder and remainder[0] == "--":
            remainder = remainder[1:]
        duty.options_override = {**global_opts, **opts}
        commands.append((duty, *parse_args(duty, remainder)))
    return commands

```

## parse_options

```
parse_options(
    duty: Duty, args: list[str]
) -> tuple[dict, list[str]]

```

Parse options for a duty.

Parameters:

- **`duty`** (`Duty`) – The duty to parse for.
- **`args`** (`list[str]`) – The CLI args passed for this duty.

Returns:

- `tuple[dict, list[str]]` – The parsed opts, and the remaining arguments.

Source code in `src/duty/_internal/cli.py`

```
def parse_options(duty: Duty, args: list[str]) -> tuple[dict, list[str]]:
    """Parse options for a duty.

    Parameters:
        duty: The duty to parse for.
        args: The CLI args passed for this duty.

    Returns:
        The parsed opts, and the remaining arguments.
    """
    parser = get_duty_parser(duty)
    opts, remainder = parser.parse_known_args(args)
    return specified_options(opts), remainder

```

## print_help

```
print_help(
    parser: ArgParser,
    opts: Namespace,
    collection: Collection,
) -> None

```

Print general help or duties help.

Parameters:

- **`parser`** (`ArgParser`) – The main parser.
- **`opts`** (`Namespace`) – The main parsed options.
- **`collection`** (`Collection`) – A collection of duties.

Source code in `src/duty/_internal/cli.py`

```
def print_help(parser: ArgParser, opts: argparse.Namespace, collection: Collection) -> None:
    """Print general help or duties help.

    Parameters:
        parser: The main parser.
        opts: The main parsed options.
        collection: A collection of duties.
    """
    if opts.help:
        for duty_name in opts.help:
            try:
                duty = collection.get(duty_name)
            except KeyError:
                print(f"> Unknown duty '{duty_name}'")
            else:
                print(get_duty_parser(duty).format_help())
    else:
        print(parser.format_help())
        print("Available duties:")
        print(textwrap.indent(collection.format_help(), prefix="  "))

```

## specified_options

```
specified_options(
    opts: Namespace, exclude: set[str] | None = None
) -> dict

```

Cast an argparse Namespace into a dictionary of options.

Remove all options that were not specified (equal to None).

Parameters:

- **`opts`** (`Namespace`) – The namespace to cast.
- **`exclude`** (`set[str] | None`, default: `None` ) – Names of options to exclude from the result.

Returns:

- `dict` – A dictionary of specified-only options.

Source code in `src/duty/_internal/cli.py`

```
def specified_options(opts: argparse.Namespace, exclude: set[str] | None = None) -> dict:
    """Cast an argparse Namespace into a dictionary of options.

    Remove all options that were not specified (equal to None).

    Parameters:
        opts: The namespace to cast.
        exclude: Names of options to exclude from the result.

    Returns:
        A dictionary of specified-only options.
    """
    exclude = exclude or set()
    options = opts.__dict__.items()
    return {opt: value for opt, value in options if value is not None and opt not in exclude}

```

## split_args

```
split_args(
    args: list[str], names: list[str]
) -> list[list[str]]

```

Split command line arguments into duty commands.

Parameters:

- **`args`** (`list[str]`) – The CLI arguments.
- **`names`** (`list[str]`) – The known duty names.

Raises:

- `ValueError` – When a duty name is missing before an argument, or when the duty name is unknown.

Returns:

- `list[list[str]]` – The split commands.

Source code in `src/duty/_internal/cli.py`

```
def split_args(args: list[str], names: list[str]) -> list[list[str]]:
    """Split command line arguments into duty commands.

    Parameters:
        args: The CLI arguments.
        names: The known duty names.

    Raises:
        ValueError: When a duty name is missing before an argument,
            or when the duty name is unknown.

    Returns:
        The split commands.
    """
    arg_lists = []
    current_arg_list: list[str] = []

    for arg in args:
        if arg in names:
            # We found a duty name.
            if current_arg_list:
                # Append the previous arg list to the result and reset it.
                arg_lists.append(current_arg_list)
                current_arg_list = []
            current_arg_list.append(arg)
        elif current_arg_list:
            # We found an argument.
            current_arg_list.append(arg)
        else:
            # We found an argument but no duty name.
            raise ValueError(f"> Missing duty name before argument '{arg}', or unknown duty name")

    # Don't forget the last arg list.
    if current_arg_list:
        arg_lists.append(current_arg_list)

    return arg_lists

```

## to_bool

```
to_bool(value: str) -> bool

```

Convert a string to a boolean.

Parameters:

- **`value`** (`str`) – The string to convert.

Returns:

- `bool` – True or False.

Source code in `src/duty/_internal/validation.py`

```
def to_bool(value: str) -> bool:
    """Convert a string to a boolean.

    Parameters:
        value: The string to convert.

    Returns:
        True or False.
    """
    return value.lower() not in {"", "0", "no", "n", "false", "off"}

```

## validate

```
validate(
    func: Callable, *args: Any, **kwargs: Any
) -> tuple[Sequence, dict[str, Any]]

```

Validate positional and keyword arguments against a function.

First we clone the function, removing the first parameter (the context) and the body, to fail early with a `TypeError` if the arguments are incorrect: not enough, too much, in the wrong order, etc.

Then we cast all the arguments using the function's signature and we return them.

Parameters:

- **`func`** (`Callable`) – The function to copy.
- **`*args`** (`Any`, default: `()` ) – The positional arguments.
- **`**kwargs`** (`Any`, default: `{}` ) – The keyword arguments.

Returns:

- `tuple[Sequence, dict[str, Any]]` – The casted arguments.

Source code in `src/duty/_internal/validation.py`

```
def validate(
    func: Callable,
    *args: Any,
    **kwargs: Any,
) -> tuple[Sequence, dict[str, Any]]:
    """Validate positional and keyword arguments against a function.

    First we clone the function, removing the first parameter (the context)
    and the body, to fail early with a `TypeError` if the arguments
    are incorrect: not enough, too much, in the wrong order, etc.

    Then we cast all the arguments using the function's signature
    and we return them.

    Parameters:
        func: The function to copy.
        *args: The positional arguments.
        **kwargs: The keyword arguments.

    Returns:
        The casted arguments.
    """
    return _get_params_caster(func, *args, **kwargs).cast(*args, **kwargs)

```

## callables

Module containing callables for many tools.

These callables are **deprecated** in favor of our new tools.

Modules:

- **`autoflake`** – Deprecated. Use duty.tools.autoflake instead.
- **`black`** – Deprecated. Use duty.tools.black instead.
- **`blacken_docs`** – Deprecated. Use duty.tools.blacken_docs instead.
- **`build`** – Deprecated. Use duty.tools.build instead.
- **`coverage`** – Deprecated. Use duty.tools.coverage instead.
- **`flake8`** – Deprecated. Use duty.tools.flake8 instead.
- **`git_changelog`** – Deprecated. Use duty.tools.git_changelog instead.
- **`griffe`** – Deprecated. Use duty.tools.griffe instead.
- **`interrogate`** – Deprecated. Use duty.tools.interrogate instead.
- **`isort`** – Deprecated. Use duty.tools.isort instead.
- **`mkdocs`** – Deprecated. Use duty.tools.mkdocs instead.
- **`mypy`** – Deprecated. Use duty.tools.mypy instead.
- **`pytest`** – Deprecated. Use duty.tools.pytest instead.
- **`ruff`** – Deprecated. Use duty.tools.ruff instead.
- **`safety`** – Deprecated. Use duty.tools.safety instead.
- **`ssort`** – Deprecated. Use duty.tools.ssort instead.
- **`twine`** – Deprecated. Use duty.tools.twine instead.

### autoflake

Deprecated. Use duty.tools.autoflake instead.

### black

Deprecated. Use duty.tools.black instead.

### blacken_docs

Deprecated. Use duty.tools.blacken_docs instead.

### build

Deprecated. Use duty.tools.build instead.

### coverage

Deprecated. Use duty.tools.coverage instead.

### flake8

Deprecated. Use duty.tools.flake8 instead.

### git_changelog

Deprecated. Use duty.tools.git_changelog instead.

### griffe

Deprecated. Use duty.tools.griffe instead.

### interrogate

Deprecated. Use duty.tools.interrogate instead.

### isort

Deprecated. Use duty.tools.isort instead.

### mkdocs

Deprecated. Use duty.tools.mkdocs instead.

### mypy

Deprecated. Use duty.tools.mypy instead.

### pytest

Deprecated. Use duty.tools.pytest instead.

### ruff

Deprecated. Use duty.tools.ruff instead.

### safety

Deprecated. Use duty.tools.safety instead.

### ssort

Deprecated. Use duty.tools.ssort instead.

### twine

Deprecated. Use duty.tools.twine instead.

## cli

Deprecated. Import from `duty` directly.

## collection

Deprecated. Import from `duty` directly.

## context

Deprecated. Import from `duty` directly.

## decorator

Deprecated. Import from `duty` directly.

## exceptions

Deprecated. Import from `duty` directly.

## lazy

Deprecated. Import from `failprint` directly.

## tools

Our collection of tools.

Classes:

- **`autoflake`** – Call autoflake.
- **`black`** – Call Black.
- **`blacken_docs`** – Call blacken-docs.
- **`build`** – Call build.
- **`coverage`** – Call Coverage.py.
- **`flake8`** – Call Flake8.
- **`git_changelog`** – Call git-changelog.
- **`griffe`** – Call Griffe.
- **`interrogate`** – Call Interrogate.
- **`isort`** – Call isort.
- **`mkdocs`** – Call MkDocs.
- **`mypy`** – Call Mypy.
- **`pytest`** – Call pytest.
- **`ruff`** – Call Ruff.
- **`safety`** – Call Safety.
- **`ssort`** – Call ssort.
- **`twine`** – Call Twine.
- **`yore`** – Call Yore.

### autoflake

```
autoflake(
    *files: str,
    config: str | None = None,
    check: bool | None = None,
    check_diff: bool | None = None,
    imports: list[str] | None = None,
    remove_all_unused_imports: bool | None = None,
    recursive: bool | None = None,
    jobs: int | None = None,
    exclude: list[str] | None = None,
    expand_star_imports: bool | None = None,
    ignore_init_module_imports: bool | None = None,
    remove_duplicate_keys: bool | None = None,
    remove_unused_variables: bool | None = None,
    remove_rhs_for_unused_variables: bool | None = None,
    ignore_pass_statements: bool | None = None,
    ignore_pass_after_docstring: bool | None = None,
    quiet: bool | None = None,
    verbose: bool | None = None,
    stdin_display_name: str | None = None,
    in_place: bool | None = None,
    stdout: bool | None = None,
)

```

Bases: `Tool`

Call [autoflake](https://github.com/PyCQA/autoflake).

Parameters:

- **`*files`** (`str`, default: `()` ) – Files to format.
- **`config`** (`str | None`, default: `None` ) – Explicitly set the config file instead of auto determining based on file location.
- **`check`** (`bool | None`, default: `None` ) – Return error code if changes are needed.
- **`check_diff`** (`bool | None`, default: `None` ) – Return error code if changes are needed, also display file diffs.
- **`imports`** (`list[str] | None`, default: `None` ) – By default, only unused standard library imports are removed; specify a comma-separated list of additional modules/packages.
- **`remove_all_unused_imports`** (`bool | None`, default: `None` ) – Remove all unused imports (not just those from the standard library).
- **`recursive`** (`bool | None`, default: `None` ) – Drill down directories recursively.
- **`jobs`** (`int | None`, default: `None` ) – Number of parallel jobs; match CPU count if value is 0 (default: 0).
- **`exclude`** (`list[str] | None`, default: `None` ) – Exclude file/directory names that match these comma-separated globs.
- **`expand_star_imports`** (`bool | None`, default: `None` ) – Expand wildcard star imports with undefined names; this only triggers if there is only one star import in the file; this is skipped if there are any uses of __all__ or del in the file.
- **`ignore_init_module_imports`** (`bool | None`, default: `None` ) – Exclude __init__.py when removing unused imports.
- **`remove_duplicate_keys`** (`bool | None`, default: `None` ) – Remove all duplicate keys in objects.
- **`remove_unused_variables`** (`bool | None`, default: `None` ) – Remove unused variables.
- **`remove_rhs_for_unused_variables`** (`bool | None`, default: `None` ) – Remove RHS of statements when removing unused variables (unsafe).
- **`ignore_pass_statements`** (`bool | None`, default: `None` ) – Ignore all pass statements.
- **`ignore_pass_after_docstring`** (`bool | None`, default: `None` ) – Ignore pass statements after a newline ending on """.
- **`quiet`** (`bool | None`, default: `None` ) – Suppress output if there are no issues.
- **`verbose`** (`bool | None`, default: `None` ) – Print more verbose logs (you can repeat -v to make it more verbose).
- **`stdin_display_name`** (`str | None`, default: `None` ) – The name used when processing input from stdin.
- **`in_place`** (`bool | None`, default: `None` ) – Make changes to files instead of printing diffs.
- **`stdout`** (`bool | None`, default: `None` ) – Print changed text to stdout. defaults to true when formatting stdin, or to false otherwise.

Methods:

- **`__call__`** – Run the command.
- **`add_args`** – Append CLI arguments.

Attributes:

- **`cli_args`** (`list[str]`) – Registered command-line arguments.
- **`cli_command`** (`str`) – The equivalent CLI command.
- **`cli_name`** – The name of the executable on PATH.
- **`py_args`** (`dict[str, Any]`) – Registered Python arguments.

Source code in `src/duty/_internal/tools/_autoflake.py`

```
def __init__(
    self,
    *files: str,
    config: str | None = None,
    check: bool | None = None,
    check_diff: bool | None = None,
    imports: list[str] | None = None,
    remove_all_unused_imports: bool | None = None,
    recursive: bool | None = None,
    jobs: int | None = None,
    exclude: list[str] | None = None,
    expand_star_imports: bool | None = None,
    ignore_init_module_imports: bool | None = None,
    remove_duplicate_keys: bool | None = None,
    remove_unused_variables: bool | None = None,
    remove_rhs_for_unused_variables: bool | None = None,
    ignore_pass_statements: bool | None = None,
    ignore_pass_after_docstring: bool | None = None,
    quiet: bool | None = None,
    verbose: bool | None = None,
    stdin_display_name: str | None = None,
    in_place: bool | None = None,
    stdout: bool | None = None,
) -> None:
    r"""Run `autoflake`.

    Parameters:
        *files: Files to format.
        config: Explicitly set the config file instead of auto determining based on file location.
        check: Return error code if changes are needed.
        check_diff: Return error code if changes are needed, also display file diffs.
        imports: By default, only unused standard library imports are removed; specify a comma-separated list of additional modules/packages.
        remove_all_unused_imports: Remove all unused imports (not just those from the standard library).
        recursive: Drill down directories recursively.
        jobs: Number of parallel jobs; match CPU count if value is 0 (default: 0).
        exclude: Exclude file/directory names that match these comma-separated globs.
        expand_star_imports: Expand wildcard star imports with undefined names; this only triggers if there is only one star import in the file; this is skipped if there are any uses of `__all__` or `del` in the file.
        ignore_init_module_imports: Exclude `__init__.py` when removing unused imports.
        remove_duplicate_keys: Remove all duplicate keys in objects.
        remove_unused_variables: Remove unused variables.
        remove_rhs_for_unused_variables: Remove RHS of statements when removing unused variables (unsafe).
        ignore_pass_statements: Ignore all pass statements.
        ignore_pass_after_docstring: Ignore pass statements after a newline ending on `\"\"\"`.
        quiet: Suppress output if there are no issues.
        verbose: Print more verbose logs (you can repeat `-v` to make it more verbose).
        stdin_display_name: The name used when processing input from stdin.
        in_place: Make changes to files instead of printing diffs.
        stdout: Print changed text to stdout. defaults to true when formatting stdin, or to false otherwise.
    """
    cli_args = list(files)

    if check:
        cli_args.append("--check")

    if check_diff:
        cli_args.append("--check-diff")

    if imports:
        cli_args.append("--imports")
        cli_args.append(",".join(imports))

    if remove_all_unused_imports:
        cli_args.append("--remove-all-unused-imports")

    if recursive:
        cli_args.append("--recursive")

    if jobs:
        cli_args.append("--jobs")
        cli_args.append(str(jobs))

    if exclude:
        cli_args.append("--exclude")
        cli_args.append(",".join(exclude))

    if expand_star_imports:
        cli_args.append("--expand-star-imports")

    if ignore_init_module_imports:
        cli_args.append("--ignore-init-module-imports")

    if remove_duplicate_keys:
        cli_args.append("--remove-duplicate-keys")

    if remove_unused_variables:
        cli_args.append("--remove-unused-variables")

    if remove_rhs_for_unused_variables:
        cli_args.append("remove-rhs-for-unused-variables")

    if ignore_pass_statements:
        cli_args.append("--ignore-pass-statements")

    if ignore_pass_after_docstring:
        cli_args.append("--ignore-pass-after-docstring")

    if quiet:
        cli_args.append("--quiet")

    if verbose:
        cli_args.append("--verbose")

    if stdin_display_name:
        cli_args.append("--stdin-display-name")
        cli_args.append(stdin_display_name)

    if config:
        cli_args.append("--config")
        cli_args.append(config)

    if in_place:
        cli_args.append("--in-place")

    if stdout:
        cli_args.append("--stdout")

    super().__init__(cli_args)

```

#### cli_args

```
cli_args: list[str] = cli_args or []

```

Registered command-line arguments.

#### cli_command

```
cli_command: str

```

The equivalent CLI command.

#### cli_name

```
cli_name = 'autoflake'

```

The name of the executable on PATH.

#### py_args

```
py_args: dict[str, Any] = py_args or {}

```

Registered Python arguments.

#### __call__

```
__call__() -> int

```

Run the command.

Returns:

- `int` – The exit code of the command.

Source code in `src/duty/_internal/tools/_autoflake.py`

```
def __call__(self) -> int:
    """Run the command.

    Returns:
        The exit code of the command.
    """
    from autoflake import _main as run_autoflake  # noqa: PLC0415

    return run_autoflake(
        self.cli_args,
        standard_out=LazyStdout(),
        standard_error=LazyStderr(),
    )

```

#### add_args

```
add_args(*args: str) -> Self

```

Append CLI arguments.

Source code in `src/duty/_internal/tools/_base.py`

```
def add_args(self, *args: str) -> Self:
    """Append CLI arguments."""
    self.cli_args.extend(args)
    return self

```

### black

```
black(
    *src: str,
    config: str | None = None,
    code: str | None = None,
    line_length: int | None = None,
    target_version: str | None = None,
    check: bool | None = None,
    diff: bool | None = None,
    color: bool | None = None,
    fast: bool | None = None,
    pyi: bool | None = None,
    ipynb: bool | None = None,
    python_cell_magics: str | None = None,
    skip_source_first_line: bool | None = None,
    skip_string_normalization: bool | None = None,
    skip_magic_trailing_comma: bool | None = None,
    experimental_string_processing: bool | None = None,
    preview: bool | None = None,
    quiet: bool | None = None,
    verbose: bool | None = None,
    required_version: str | None = None,
    include: str | None = None,
    exclude: str | None = None,
    extend_exclude: str | None = None,
    force_exclude: str | None = None,
    stdin_filename: str | None = None,
    workers: int | None = None,
)

```

Bases: `Tool`

Call [Black](https://github.com/psf/black).

Parameters:

- **`src`** (`str`, default: `()` ) – Format the directories and file paths.
- **`config`** (`str | None`, default: `None` ) – Read configuration from this file path.
- **`code`** (`str | None`, default: `None` ) – Format the code passed in as a string.
- **`line_length`** (`int | None`, default: `None` ) – How many characters per line to allow [default: 120].
- **`target_version`** (`str | None`, default: `None` ) – Python versions that should be supported by Black's output. By default, Black will try to infer this from the project metadata in pyproject.toml. If this does not yield conclusive results, Black will use per-file auto-detection.
- **`check`** (`bool | None`, default: `None` ) – Don't write the files back, just return the status. Return code 0 means nothing would change. Return code 1 means some files would be reformatted. Return code 123 means there was an internal error.
- **`diff`** (`bool | None`, default: `None` ) – Don't write the files back, just output a diff for each file on stdout.
- **`color`** (`bool | None`, default: `None` ) – Show colored diff. Only applies when --diff is given.
- **`fast`** (`bool | None`, default: `None` ) – If --fast given, skip temporary sanity checks. [default: --safe]
- **`pyi`** (`bool | None`, default: `None` ) – Format all input files like typing stubs regardless of file extension (useful when piping source on standard input).
- **`ipynb`** (`bool | None`, default: `None` ) – Format all input files like Jupyter Notebooks regardless of file extension (useful when piping source on standard input).
- **`python_cell_magics`** (`str | None`, default: `None` ) – When processing Jupyter Notebooks, add the given magic to the list of known python-magics (capture, prun, pypy, python, python3, time, timeit). Useful for formatting cells with custom python magics.
- **`skip_source_first_line`** (`bool | None`, default: `None` ) – Skip the first line of the source code.
- **`skip_string_normalization`** (`bool | None`, default: `None` ) – Don't normalize string quotes or prefixes.
- **`skip_magic_trailing_comma`** (`bool | None`, default: `None` ) – Don't use trailing commas as a reason to split lines.
- **`preview`** (`bool | None`, default: `None` ) – Enable potentially disruptive style changes that may be added to Black's main functionality in the next major release.
- **`quiet`** (`bool | None`, default: `None` ) – Don't emit non-error messages to stderr. Errors are still emitted; silence those with 2>/dev/null.
- **`verbose`** (`bool | None`, default: `None` ) – Also emit messages to stderr about files that were not changed or were ignored due to exclusion patterns.
- **`required_version`** (`str | None`, default: `None` ) – Require a specific version of Black to be running (useful for unifying results across many environments e.g. with a pyproject.toml file). It can be either a major version number or an exact version.
- **`include`** (`str | None`, default: `None` ) – A regular expression that matches files and directories that should be included on recursive searches. An empty value means all files are included regardless of the name. Use forward slashes for directories on all platforms (Windows, too). Exclusions are calculated first, inclusions later [default: (.pyi?|.ipynb)$].
- **`exclude`** (`str | None`, default: `None` ) – A regular expression that matches files and directories that should be excluded on recursive searches. An empty value means no paths are excluded. Use forward slashes for directories on all platforms (Windows, too). Exclusions are calculated first, inclusions later [default: /(.direnv|.eggs|.git|.hg|.mypy_cache|.nox| .tox|.venv|venv|.svn|.ipynb_checkpoints|\_build|buck-out|build|dist|pypackages)/].
- **`extend_exclude`** (`str | None`, default: `None` ) – Like --exclude, but adds additional files and directories on top of the excluded ones (useful if you simply want to add to the default).
- **`force_exclude`** (`str | None`, default: `None` ) – Like --exclude, but files and directories matching this regex will be excluded even when they are passed explicitly as arguments.
- **`stdin_filename`** (`str | None`, default: `None` ) – The name of the file when passing it through stdin. Useful to make sure Black will respect --force-exclude option on some editors that rely on using stdin.
- **`workers`** (`int | None`, default: `None` ) – Number of parallel workers [default: number CPUs in the system].

Methods:

- **`__call__`** – Run the command.
- **`add_args`** – Append CLI arguments.

Attributes:

- **`cli_args`** (`list[str]`) – Registered command-line arguments.
- **`cli_command`** (`str`) – The equivalent CLI command.
- **`cli_name`** – The name of the executable on PATH.
- **`py_args`** (`dict[str, Any]`) – Registered Python arguments.

Source code in `src/duty/_internal/tools/_black.py`

```
def __init__(
    self,
    *src: str,
    config: str | None = None,
    code: str | None = None,
    line_length: int | None = None,
    target_version: str | None = None,
    check: bool | None = None,
    diff: bool | None = None,
    color: bool | None = None,
    fast: bool | None = None,
    pyi: bool | None = None,
    ipynb: bool | None = None,
    python_cell_magics: str | None = None,
    skip_source_first_line: bool | None = None,
    skip_string_normalization: bool | None = None,
    skip_magic_trailing_comma: bool | None = None,
    experimental_string_processing: bool | None = None,
    preview: bool | None = None,
    quiet: bool | None = None,
    verbose: bool | None = None,
    required_version: str | None = None,
    include: str | None = None,
    exclude: str | None = None,
    extend_exclude: str | None = None,
    force_exclude: str | None = None,
    stdin_filename: str | None = None,
    workers: int | None = None,
) -> None:
    r"""Run `black`.

    Parameters:
        src: Format the directories and file paths.
        config: Read configuration from this file path.
        code: Format the code passed in as a string.
        line_length: How many characters per line to allow [default: 120].
        target_version: Python versions that should be supported by Black's output.
            By default, Black will try to infer this from the project metadata in pyproject.toml.
            If this does not yield conclusive results, Black will use per-file auto-detection.
        check: Don't write the files back, just return the status. Return code 0 means nothing would change.
            Return code 1 means some files would be reformatted. Return code 123 means there was an internal error.
        diff: Don't write the files back, just output a diff for each file on stdout.
        color: Show colored diff. Only applies when `--diff` is given.
        fast: If --fast given, skip temporary sanity checks. [default: --safe]
        pyi: Format all input files like typing stubs regardless of file extension
            (useful when piping source on standard input).
        ipynb: Format all input files like Jupyter Notebooks regardless of file extension
            (useful when piping source on standard input).
        python_cell_magics: When processing Jupyter Notebooks, add the given magic to the list of known python-magics
            (capture, prun, pypy, python, python3, time, timeit). Useful for formatting cells with custom python magics.
        skip_source_first_line: Skip the first line of the source code.
        skip_string_normalization: Don't normalize string quotes or prefixes.
        skip_magic_trailing_comma: Don't use trailing commas as a reason to split lines.
        preview: Enable potentially disruptive style changes that may be added
            to Black's main functionality in the next major release.
        quiet: Don't emit non-error messages to stderr. Errors are still emitted; silence those with 2>/dev/null.
        verbose: Also emit messages to stderr about files that were not changed or were ignored due to exclusion patterns.
        required_version: Require a specific version of Black to be running (useful for unifying results
            across many environments e.g. with a pyproject.toml file).
            It can be either a major version number or an exact version.
        include: A regular expression that matches files and directories that should be included on recursive searches.
            An empty value means all files are included regardless of the name. Use forward slashes for directories
            on all platforms (Windows, too). Exclusions are calculated first, inclusions later [default: (\.pyi?|\.ipynb)$].
        exclude: A regular expression that matches files and directories that should be excluded on recursive searches.
            An empty value means no paths are excluded. Use forward slashes for directories on all platforms (Windows, too).
            Exclusions are calculated first, inclusions later [default: /(\.direnv|\.eggs|\.git|\.hg|\.mypy_cache|\.nox|
            \.tox|\.venv|venv|\.svn|\.ipynb_checkpoints|_build|buck-out|build|dist|__pypackages__)/].
        extend_exclude: Like --exclude, but adds additional files and directories on top of the excluded ones
            (useful if you simply want to add to the default).
        force_exclude: Like --exclude, but files and directories matching this regex will be excluded
            even when they are passed explicitly as arguments.
        stdin_filename: The name of the file when passing it through stdin. Useful to make sure Black will respect
            --force-exclude option on some editors that rely on using stdin.
        workers: Number of parallel workers [default: number CPUs in the system].
    """
    cli_args = list(src)

    if config:
        cli_args.append("--config")
        cli_args.append(config)

    if code:
        cli_args.append("--code")
        cli_args.append(code)

    if line_length:
        cli_args.append("--line-length")
        cli_args.append(str(line_length))

    if target_version:
        cli_args.append("--target-version")
        cli_args.append(target_version)

    if check:
        cli_args.append("--check")

    if diff:
        cli_args.append("--diff")

    if color is True:
        cli_args.append("--color")
    elif color is False:
        cli_args.append("--no-color")

    if fast:
        cli_args.append("--fast")

    if pyi:
        cli_args.append("--pyi")

    if ipynb:
        cli_args.append("--ipynb")

    if python_cell_magics:
        cli_args.append("--python-cell-magics")
        cli_args.append(python_cell_magics)

    if skip_source_first_line:
        cli_args.append("--skip_source_first_line")

    if skip_string_normalization:
        cli_args.append("--skip_string_normalization")

    if skip_magic_trailing_comma:
        cli_args.append("--skip_magic_trailing_comma")

    if experimental_string_processing:
        cli_args.append("--experimental_string_processing")

    if preview:
        cli_args.append("--preview")

    if quiet:
        cli_args.append("--quiet")

    if verbose:
        cli_args.append("--verbose")

    if required_version:
        cli_args.append("--required-version")
        cli_args.append(required_version)

    if include:
        cli_args.append("--include")
        cli_args.append(include)

    if exclude:
        cli_args.append("--exclude")
        cli_args.append(exclude)

    if extend_exclude:
        cli_args.append("--extend-exclude")
        cli_args.append(extend_exclude)

    if force_exclude:
        cli_args.append("--force-exclude")
        cli_args.append(force_exclude)

    if stdin_filename:
        cli_args.append("--stdin-filename")
        cli_args.append(stdin_filename)

    if workers:
        cli_args.append("--workers")
        cli_args.append(str(workers))

    super().__init__(cli_args)

```

#### cli_args

```
cli_args: list[str] = cli_args or []

```

Registered command-line arguments.

#### cli_command

```
cli_command: str

```

The equivalent CLI command.

#### cli_name

```
cli_name = 'black'

```

The name of the executable on PATH.

#### py_args

```
py_args: dict[str, Any] = py_args or {}

```

Registered Python arguments.

#### __call__

```
__call__() -> None

```

Run the command.

Source code in `src/duty/_internal/tools/_black.py`

```
def __call__(self) -> None:
    """Run the command."""
    from black import main as run_black  # noqa: PLC0415

    run_black(self.cli_args, prog_name="black")

```

#### add_args

```
add_args(*args: str) -> Self

```

Append CLI arguments.

Source code in `src/duty/_internal/tools/_base.py`

```
def add_args(self, *args: str) -> Self:
    """Append CLI arguments."""
    self.cli_args.extend(args)
    return self

```

### blacken_docs

```
blacken_docs(
    *paths: str | Path,
    exts: Sequence[str] | None = None,
    exclude: Sequence[str | Pattern] | None = None,
    skip_errors: bool = False,
    rst_literal_blocks: bool = False,
    line_length: int | None = None,
    string_normalization: bool = True,
    is_pyi: bool = False,
    is_ipynb: bool = False,
    skip_source_first_line: bool = False,
    magic_trailing_comma: bool = True,
    python_cell_magics: set[str] | None = None,
    preview: bool = False,
    check_only: bool = False,
)

```

Bases: `Tool`

Call [blacken-docs](https://github.com/adamchainz/blacken-docs).

Parameters:

- **`*paths`** (`str | Path`, default: `()` ) – Directories and files to format.
- **`exts`** (`Sequence[str] | None`, default: `None` ) – List of extensions to select files with.
- **`exclude`** (`Sequence[str | Pattern] | None`, default: `None` ) – List of regular expressions to exclude files.
- **`skip_errors`** (`bool`, default: `False` ) – Don't exit non-zero for errors from Black (normally syntax errors).
- **`rst_literal_blocks`** (`bool`, default: `False` ) – Also format literal blocks in reStructuredText files (more below).
- **`line_length`** (`int | None`, default: `None` ) – How many characters per line to allow.
- **`string_normalization`** (`bool`, default: `True` ) – Normalize string quotes or prefixes.
- **`is_pyi`** (`bool`, default: `False` ) – Format all input files like typing stubs regardless of file extension.
- **`is_ipynb`** (`bool`, default: `False` ) – Format all input files like Jupyter Notebooks regardless of file extension.
- **`skip_source_first_line`** (`bool`, default: `False` ) – Skip the first line of the source code.
- **`magic_trailing_comma`** (`bool`, default: `True` ) – Use trailing commas as a reason to split lines.
- **`python_cell_magics`** (`set[str] | None`, default: `None` ) – When processing Jupyter Notebooks, add the given magic to the list of known python-magics (capture, prun, pypy, python, python3, time, timeit). Useful for formatting cells with custom python magics.
- **`preview`** (`bool`, default: `False` ) – Enable potentially disruptive style changes that may be added to Black's main functionality in the next major release.
- **`check_only`** (`bool`, default: `False` ) – Don't modify files but indicate when changes are necessary with a message and non-zero return code.

Returns:

- `None` – Success/failure.

Methods:

- **`__call__`** – Run the command.
- **`add_args`** – Append CLI arguments.

Attributes:

- **`cli_args`** (`list[str]`) – Registered command-line arguments.
- **`cli_command`** (`str`) – The equivalent CLI command.
- **`cli_name`** – The name of the executable on PATH.
- **`py_args`** (`dict[str, Any]`) – Registered Python arguments.

Source code in `src/duty/_internal/tools/_blacken_docs.py`

```
def __init__(
    self,
    *paths: str | Path,
    exts: Sequence[str] | None = None,
    exclude: Sequence[str | Pattern] | None = None,
    skip_errors: bool = False,
    rst_literal_blocks: bool = False,
    line_length: int | None = None,
    string_normalization: bool = True,
    is_pyi: bool = False,
    is_ipynb: bool = False,
    skip_source_first_line: bool = False,
    magic_trailing_comma: bool = True,
    python_cell_magics: set[str] | None = None,
    preview: bool = False,
    check_only: bool = False,
) -> None:
    """Run `blacken-docs`.

    Parameters:
        *paths: Directories and files to format.
        exts: List of extensions to select files with.
        exclude: List of regular expressions to exclude files.
        skip_errors: Don't exit non-zero for errors from Black (normally syntax errors).
        rst_literal_blocks: Also format literal blocks in reStructuredText files (more below).
        line_length: How many characters per line to allow.
        string_normalization: Normalize string quotes or prefixes.
        is_pyi: Format all input files like typing stubs regardless of file extension.
        is_ipynb: Format all input files like Jupyter Notebooks regardless of file extension.
        skip_source_first_line: Skip the first line of the source code.
        magic_trailing_comma: Use trailing commas as a reason to split lines.
        python_cell_magics: When processing Jupyter Notebooks, add the given magic to the list
            of known python-magics (capture, prun, pypy, python, python3, time, timeit).
            Useful for formatting cells with custom python magics.
        preview: Enable potentially disruptive style changes that may be added
            to Black's main functionality in the next major release.
        check_only: Don't modify files but indicate when changes are necessary
            with a message and non-zero return code.

    Returns:
        Success/failure.
    """
    super().__init__(py_args=dict(locals()))

```

#### cli_args

```
cli_args: list[str] = cli_args or []

```

Registered command-line arguments.

#### cli_command

```
cli_command: str

```

The equivalent CLI command.

#### cli_name

```
cli_name = 'blacken-docs'

```

The name of the executable on PATH.

#### py_args

```
py_args: dict[str, Any] = py_args or {}

```

Registered Python arguments.

#### __call__

```
__call__() -> int

```

Run the command.

Returns:

- `int` – The exit code of the command.

Source code in `src/duty/_internal/tools/_blacken_docs.py`

```
def __call__(self) -> int:
    """Run the command.

    Returns:
        The exit code of the command.
    """
    import black  # noqa: PLC0415
    from blacken_docs import format_file  # noqa: PLC0415

    # Restore locals.
    exts = self.py_args["exts"]
    exclude = self.py_args["exclude"]
    paths = self.py_args["paths"]
    line_length = self.py_args["line_length"]
    string_normalization = self.py_args["string_normalization"]
    is_pyi = self.py_args["is_pyi"]
    is_ipynb = self.py_args["is_ipynb"]
    skip_source_first_line = self.py_args["skip_source_first_line"]
    magic_trailing_comma = self.py_args["magic_trailing_comma"]
    python_cell_magics = self.py_args["python_cell_magics"]
    preview = self.py_args["preview"]
    skip_errors = self.py_args["skip_errors"]
    rst_literal_blocks = self.py_args["rst_literal_blocks"]
    check_only = self.py_args["check_only"]

    # Build filepaths.
    exts = ("md", "py") if exts is None else tuple(ext.lstrip(".") for ext in exts)
    if exclude:
        exclude = tuple(re.compile(regex, re.I) if isinstance(regex, str) else regex for regex in exclude)
    filepaths = set()
    for path in paths:
        path = Path(path)  # noqa: PLW2901
        if path.is_file():
            filepaths.add(path.as_posix())
        else:
            for ext in exts:
                filepaths |= {filepath.as_posix() for filepath in path.rglob(f"*.{ext}")}

    # Initiate black.
    black_mode = black.Mode(
        line_length=line_length or black.DEFAULT_LINE_LENGTH,
        string_normalization=string_normalization,
        is_pyi=is_pyi,
        is_ipynb=is_ipynb,
        skip_source_first_line=skip_source_first_line,
        magic_trailing_comma=magic_trailing_comma,
        python_cell_magics=python_cell_magics or set(),
        preview=preview,
    )

    # Run blacken-docs.
    retv = 0
    for filepath in sorted(filepaths):
        retv |= format_file(
            filepath,
            black_mode,
            skip_errors=skip_errors,
            rst_literal_blocks=rst_literal_blocks,
            check_only=check_only,
        )
    return retv

```

#### add_args

```
add_args(*args: str) -> Self

```

Append CLI arguments.

Source code in `src/duty/_internal/tools/_base.py`

```
def add_args(self, *args: str) -> Self:
    """Append CLI arguments."""
    self.cli_args.extend(args)
    return self

```

### build

```
build(
    srcdir: str | None = None,
    *,
    version: bool = False,
    verbose: bool = False,
    sdist: bool = False,
    wheel: bool = False,
    outdir: str | None = None,
    skip_dependency_check: bool = False,
    no_isolation: bool = False,
    installer: Literal["pip", "uv"] | None = None,
    config_setting: list[str] | None = None,
)

```

Bases: `Tool`

Call [build](https://github.com/pypa/build).

Parameters:

- **`srcdir`** (`str | None`, default: `None` ) – Source directory (defaults to current directory).
- **`version`** (`bool`, default: `False` ) – Show program's version number and exit.
- **`verbose`** (`bool`, default: `False` ) – Increase verbosity
- **`sdist`** (`bool`, default: `False` ) – Build a source distribution (disables the default behavior).
- **`wheel`** (`bool`, default: `False` ) – Build a wheel (disables the default behavior).
- **`outdir`** (`str | None`, default: `None` ) – Output directory (defaults to {srcdir}/dist).
- **`skip_dependency_check`** (`bool`, default: `False` ) – Do not check that build dependencies are installed.
- **`no_isolation`** (`bool`, default: `False` ) – Disable building the project in an isolated virtual environment. Build dependencies must be installed separately when this option is used.
- **`installer`** (`Literal['pip', 'uv'] | None`, default: `None` ) – Python package installer to use (defaults to pip).
- **`config_setting`** (`list[str] | None`, default: `None` ) – Settings to pass to the backend. Multiple settings can be provided.

Methods:

- **`__call__`** – Run the command.
- **`add_args`** – Append CLI arguments.

Attributes:

- **`cli_args`** (`list[str]`) – Registered command-line arguments.
- **`cli_command`** (`str`) – The equivalent CLI command.
- **`cli_name`** – The name of the executable on PATH.
- **`py_args`** (`dict[str, Any]`) – Registered Python arguments.

Source code in `src/duty/_internal/tools/_build.py`

```
def __init__(
    self,
    srcdir: str | None = None,
    *,
    version: bool = False,
    verbose: bool = False,
    sdist: bool = False,
    wheel: bool = False,
    outdir: str | None = None,
    skip_dependency_check: bool = False,
    no_isolation: bool = False,
    installer: Literal["pip", "uv"] | None = None,
    config_setting: list[str] | None = None,
) -> None:
    """Run `build`.

    Parameters:
        srcdir: Source directory (defaults to current directory).
        version: Show program's version number and exit.
        verbose: Increase verbosity
        sdist: Build a source distribution (disables the default behavior).
        wheel: Build a wheel (disables the default behavior).
        outdir: Output directory (defaults to `{srcdir}/dist`).
        skip_dependency_check: Do not check that build dependencies are installed.
        no_isolation: Disable building the project in an isolated virtual environment.
            Build dependencies must be installed separately when this option is used.
        installer: Python package installer to use (defaults to pip).
        config_setting: Settings to pass to the backend. Multiple settings can be provided.
    """
    cli_args = []

    if srcdir:
        cli_args.append(srcdir)

    if version:
        cli_args.append("--version")

    if verbose:
        cli_args.append("--verbose")

    if sdist:
        cli_args.append("--sdist")

    if wheel:
        cli_args.append("--wheel")

    if outdir:
        cli_args.append("--outdir")
        cli_args.append(outdir)

    if skip_dependency_check:
        cli_args.append("--skip-dependency-check")

    if no_isolation:
        cli_args.append("--no-isolation")

    if installer:
        cli_args.append("--installer")
        cli_args.append(installer)

    if config_setting:
        for setting in config_setting:
            cli_args.append(f"--config-setting={setting}")

    super().__init__(cli_args)

```

#### cli_args

```
cli_args: list[str] = cli_args or []

```

Registered command-line arguments.

#### cli_command

```
cli_command: str

```

The equivalent CLI command.

#### cli_name

```
cli_name = 'pyproject-build'

```

The name of the executable on PATH.

#### py_args

```
py_args: dict[str, Any] = py_args or {}

```

Registered Python arguments.

#### __call__

```
__call__() -> None

```

Run the command.

Source code in `src/duty/_internal/tools/_build.py`

```
def __call__(self) -> None:
    """Run the command."""
    from build.__main__ import main as run_build  # noqa: PLC0415

    run_build(self.cli_args)

```

#### add_args

```
add_args(*args: str) -> Self

```

Append CLI arguments.

Source code in `src/duty/_internal/tools/_base.py`

```
def add_args(self, *args: str) -> Self:
    """Append CLI arguments."""
    self.cli_args.extend(args)
    return self

```

### coverage

```
coverage(
    cli_args: list[str] | None = None,
    py_args: dict[str, Any] | None = None,
)

```

Bases: `Tool`

Call [Coverage.py](https://github.com/nedbat/coveragepy).

Parameters:

- **`cli_args`** (`list[str] | None`, default: `None` ) – Initial command-line arguments. Use add_args() to add more.
- **`py_args`** (`dict[str, Any] | None`, default: `None` ) – Python arguments. Your __call__ method will be able to access these arguments as self.py_args.

Methods:

- **`__call__`** – Run the command.
- **`add_args`** – Append CLI arguments.
- **`annotate`** – Annotate source files with execution information.
- **`combine`** – Combine a number of data files.
- **`debug`** – Display information about the internals of coverage.py.
- **`erase`** – Erase previously collected coverage data.
- **`html`** – Create an HTML report.
- **`json`** – Create a JSON report of coverage results.
- **`lcov`** – Create an LCOV report of coverage results.
- **`report`** – Report coverage statistics on modules.
- **`run`** – Run a Python program and measure code execution.
- **`xml`** – Create an XML report of coverage results.

Attributes:

- **`cli_args`** (`list[str]`) – Registered command-line arguments.
- **`cli_command`** (`str`) – The equivalent CLI command.
- **`cli_name`** – The name of the executable on PATH.
- **`py_args`** (`dict[str, Any]`) – Registered Python arguments.

Source code in `src/duty/_internal/tools/_base.py`

```
def __init__(
    self,
    cli_args: list[str] | None = None,
    py_args: dict[str, Any] | None = None,
) -> None:
    """Initialize the tool.

    Parameters:
        cli_args: Initial command-line arguments. Use `add_args()` to add more.
        py_args: Python arguments. Your `__call__` method will be able to access
            these arguments as `self.py_args`.
    """
    self.cli_args: list[str] = cli_args or []
    """Registered command-line arguments."""
    self.py_args: dict[str, Any] = py_args or {}
    """Registered Python arguments."""

```

#### cli_args

```
cli_args: list[str] = cli_args or []

```

Registered command-line arguments.

#### cli_command

```
cli_command: str

```

The equivalent CLI command.

#### cli_name

```
cli_name = 'coverage'

```

The name of the executable on PATH.

#### py_args

```
py_args: dict[str, Any] = py_args or {}

```

Registered Python arguments.

#### __call__

```
__call__() -> int | None

```

Run the command.

Returns:

- `int | None` – The exit code of the command.

Source code in `src/duty/_internal/tools/_coverage.py`

```
def __call__(self) -> int | None:
    """Run the command.

    Returns:
        The exit code of the command.
    """
    from coverage.cmdline import main as run_coverage  # noqa: PLC0415

    return run_coverage(self.cli_args)

```

#### add_args

```
add_args(*args: str) -> Self

```

Append CLI arguments.

Source code in `src/duty/_internal/tools/_base.py`

```
def add_args(self, *args: str) -> Self:
    """Append CLI arguments."""
    self.cli_args.extend(args)
    return self

```

#### annotate

```
annotate(
    *,
    rcfile: str | None = None,
    directory: str | None = None,
    data_file: str | None = None,
    ignore_errors: bool | None = None,
    include: list[str] | None = None,
    omit: list[str] | None = None,
    debug_opts: list[str] | None = None,
) -> coverage

```

Annotate source files with execution information.

Make annotated copies of the given files, marking statements that are executed with `>` and statements that are missed with `!`.

Parameters:

- **`rcfile`** (`str | None`, default: `None` ) – Specify configuration file. By default .coveragerc, setup.cfg, tox.ini, and pyproject.toml are tried [env: COVERAGE_RCFILE].
- **`directory`** (`str | None`, default: `None` ) – Write the output files to this directory.
- **`data_file`** (`str | None`, default: `None` ) – Read coverage data for report generation from this file. Defaults to .coverage [env: COVERAGE_FILE].
- **`ignore_errors`** (`bool | None`, default: `None` ) – Ignore errors while reading source files.
- **`include`** (`list[str] | None`, default: `None` ) – Include only files whose paths match one of these patterns. Accepts shell-style wildcards, which must be quoted.
- **`omit`** (`list[str] | None`, default: `None` ) – Omit files whose paths match one of these patterns. Accepts shell-style wildcards, which must be quoted.
- **`debug_opts`** (`list[str] | None`, default: `None` ) – Debug options, separated by commas [env: COVERAGE_DEBUG].

Source code in `src/duty/_internal/tools/_coverage.py`

```
@classmethod
def annotate(
    cls,
    *,
    rcfile: str | None = None,
    directory: str | None = None,
    data_file: str | None = None,
    ignore_errors: bool | None = None,
    include: list[str] | None = None,
    omit: list[str] | None = None,
    debug_opts: list[str] | None = None,
) -> coverage:
    """Annotate source files with execution information.

    Make annotated copies of the given files, marking statements that are executed
    with `>` and statements that are missed with `!`.

    Parameters:
        rcfile: Specify configuration file. By default `.coveragerc`, `setup.cfg`, `tox.ini`,
            and `pyproject.toml` are tried [env: `COVERAGE_RCFILE`].
        directory: Write the output files to this directory.
        data_file: Read coverage data for report generation from this file.
            Defaults to `.coverage` [env: `COVERAGE_FILE`].
        ignore_errors: Ignore errors while reading source files.
        include: Include only files whose paths match one of these patterns. Accepts shell-style wildcards, which must be quoted.
        omit: Omit files whose paths match one of these patterns. Accepts shell-style wildcards, which must be quoted.
        debug_opts: Debug options, separated by commas [env: `COVERAGE_DEBUG`].
    """
    cli_args = ["annotate"]

    if directory:
        cli_args.append("--directory")
        cli_args.append(directory)

    if data_file:
        cli_args.append("--data-file")
        cli_args.append(data_file)

    if ignore_errors:
        cli_args.append("--ignore-errors")

    if include:
        cli_args.append("--include")
        cli_args.append(",".join(include))

    if omit:
        cli_args.append("--omit")
        cli_args.append(",".join(omit))

    if debug_opts:
        cli_args.append("--debug")
        cli_args.append(",".join(debug_opts))

    if rcfile:
        cli_args.append("--rcfile")
        cli_args.append(rcfile)

    return cls(cli_args)

```

#### combine

```
combine(
    *paths: str,
    rcfile: str | None = None,
    append: bool | None = None,
    data_file: str | None = None,
    keep: bool | None = None,
    quiet: bool | None = None,
    debug_opts: list[str] | None = None,
) -> coverage

```

Combine a number of data files.

Combine data from multiple coverage files. The combined results are written to a single file representing the union of the data. The positional arguments are data files or directories containing data files. If no paths are provided, data files in the default data file's directory are combined.

Parameters:

- **`paths`** (`str`, default: `()` ) – Paths to combine.
- **`rcfile`** (`str | None`, default: `None` ) – Specify configuration file. By default .coveragerc, setup.cfg, tox.ini, and pyproject.toml are tried [env: COVERAGE_RCFILE].
- **`append`** (`bool | None`, default: `None` ) – Append coverage data to .coverage, otherwise it starts clean each time.
- **`data_file`** (`str | None`, default: `None` ) – Read coverage data for report generation from this file. Defaults to .coverage [env: COVERAGE_FILE].
- **`keep`** (`bool | None`, default: `None` ) – Keep original coverage files, otherwise they are deleted.
- **`quiet`** (`bool | None`, default: `None` ) – Don't print messages about what is happening.
- **`debug_opts`** (`list[str] | None`, default: `None` ) – Debug options, separated by commas [env: COVERAGE_DEBUG].

Source code in `src/duty/_internal/tools/_coverage.py`

```
@classmethod
def combine(
    cls,
    *paths: str,
    rcfile: str | None = None,
    append: bool | None = None,
    data_file: str | None = None,
    keep: bool | None = None,
    quiet: bool | None = None,
    debug_opts: list[str] | None = None,
) -> coverage:
    """Combine a number of data files.

    Combine data from multiple coverage files. The combined results are written to
    a single file representing the union of the data. The positional arguments are
    data files or directories containing data files. If no paths are provided,
    data files in the default data file's directory are combined.

    Parameters:
        paths: Paths to combine.
        rcfile: Specify configuration file. By default `.coveragerc`, `setup.cfg`, `tox.ini`,
            and `pyproject.toml` are tried [env: `COVERAGE_RCFILE`].
        append: Append coverage data to .coverage, otherwise it starts clean each time.
        data_file: Read coverage data for report generation from this file.
            Defaults to `.coverage` [env: `COVERAGE_FILE`].
        keep: Keep original coverage files, otherwise they are deleted.
        quiet: Don't print messages about what is happening.
        debug_opts: Debug options, separated by commas [env: `COVERAGE_DEBUG`].
    """
    cli_args = ["combine", *paths]

    if append:
        cli_args.append("--append")

    if data_file:
        cli_args.append("--data-file")
        cli_args.append(data_file)

    if keep:
        cli_args.append("--keep")

    if quiet:
        cli_args.append("--quiet")

    if debug_opts:
        cli_args.append("--debug")
        cli_args.append(",".join(debug_opts))

    if rcfile:
        cli_args.append("--rcfile")
        cli_args.append(rcfile)

    return cls(cli_args)

```

#### debug

```
debug(
    topic: Literal[
        "data", "sys", "config", "premain", "pybehave"
    ],
    *,
    rcfile: str | None = None,
    debug_opts: list[str] | None = None,
) -> coverage

```

Display information about the internals of coverage.py.

Display information about the internals of coverage.py, for diagnosing problems. Topics are: `data` to show a summary of the collected data; `sys` to show installation information; `config` to show the configuration; `premain` to show what is calling coverage; `pybehave` to show internal flags describing Python behavior.

Parameters:

- **`topic`** (`Literal['data', 'sys', 'config', 'premain', 'pybehave']`) – Topic to display.
- **`rcfile`** (`str | None`, default: `None` ) – Specify configuration file. By default .coveragerc, setup.cfg, tox.ini, and pyproject.toml are tried [env: COVERAGE_RCFILE].
- **`debug_opts`** (`list[str] | None`, default: `None` ) – Debug options, separated by commas [env: COVERAGE_DEBUG].

Source code in `src/duty/_internal/tools/_coverage.py`

```
@classmethod
def debug(
    cls,
    topic: Literal["data", "sys", "config", "premain", "pybehave"],
    *,
    rcfile: str | None = None,
    debug_opts: list[str] | None = None,
) -> coverage:
    """Display information about the internals of coverage.py.

    Display information about the internals of coverage.py, for diagnosing
    problems. Topics are: `data` to show a summary of the collected data; `sys` to
    show installation information; `config` to show the configuration; `premain`
    to show what is calling coverage; `pybehave` to show internal flags describing
    Python behavior.

    Parameters:
        topic: Topic to display.
        rcfile: Specify configuration file. By default `.coveragerc`, `setup.cfg`, `tox.ini`,
            and `pyproject.toml` are tried [env: `COVERAGE_RCFILE`].
        debug_opts: Debug options, separated by commas [env: `COVERAGE_DEBUG`].
    """
    cli_args: list[str] = ["debug", topic]

    if debug_opts:
        cli_args.append("--debug")
        cli_args.append(",".join(debug_opts))

    if rcfile:
        cli_args.append("--rcfile")
        cli_args.append(rcfile)

    return cls(cli_args)

```

#### erase

```
erase(
    *,
    rcfile: str | None = None,
    data_file: str | None = None,
    debug_opts: list[str] | None = None,
) -> coverage

```

Erase previously collected coverage data.

Parameters:

- **`rcfile`** (`str | None`, default: `None` ) – Specify configuration file. By default .coveragerc, setup.cfg, tox.ini, and pyproject.toml are tried [env: COVERAGE_RCFILE].
- **`data_file`** (`str | None`, default: `None` ) – Read coverage data for report generation from this file. Defaults to .coverage [env: COVERAGE_FILE].
- **`debug_opts`** (`list[str] | None`, default: `None` ) – Debug options, separated by commas [env: COVERAGE_DEBUG].

Source code in `src/duty/_internal/tools/_coverage.py`

```
@classmethod
def erase(
    cls,
    *,
    rcfile: str | None = None,
    data_file: str | None = None,
    debug_opts: list[str] | None = None,
) -> coverage:
    """Erase previously collected coverage data.

    Parameters:
        rcfile: Specify configuration file. By default `.coveragerc`, `setup.cfg`, `tox.ini`,
            and `pyproject.toml` are tried [env: `COVERAGE_RCFILE`].
        data_file: Read coverage data for report generation from this file.
            Defaults to `.coverage` [env: `COVERAGE_FILE`].
        debug_opts: Debug options, separated by commas [env: `COVERAGE_DEBUG`].
    """
    cli_args = ["erase"]

    if data_file:
        cli_args.append("--data-file")
        cli_args.append(data_file)

    if debug_opts:
        cli_args.append("--debug")
        cli_args.append(",".join(debug_opts))

    if rcfile:
        cli_args.append("--rcfile")
        cli_args.append(rcfile)

    return cls(cli_args)

```

#### html

```
html(
    *,
    rcfile: str | None = None,
    contexts: list[str] | None = None,
    directory: str | None = None,
    data_file: str | None = None,
    fail_under: int | None = None,
    ignore_errors: bool | None = None,
    include: list[str] | None = None,
    omit: list[str] | None = None,
    precision: int | None = None,
    quiet: bool | None = None,
    show_contexts: bool | None = None,
    skip_covered: bool | None = None,
    skip_empty: bool | None = None,
    title: str | None = None,
    debug_opts: list[str] | None = None,
) -> coverage

```

Create an HTML report.

Create an HTML report of the coverage of the files. Each file gets its own page, with the source decorated to show executed, excluded, and missed lines.

Parameters:

- **`rcfile`** (`str | None`, default: `None` ) – Specify configuration file. By default .coveragerc, setup.cfg, tox.ini, and pyproject.toml are tried [env: COVERAGE_RCFILE].
- **`contexts`** (`list[str] | None`, default: `None` ) – Only display data from lines covered in the given contexts. Accepts Python regexes, which must be quoted.
- **`directory`** (`str | None`, default: `None` ) – Write the output files to this directory.
- **`data_file`** (`str | None`, default: `None` ) – Read coverage data for report generation from this file. Defaults to .coverage [env: COVERAGE_FILE].
- **`fail_under`** (`int | None`, default: `None` ) – Exit with a status of 2 if the total coverage is less than the given number.
- **`ignore_errors`** (`bool | None`, default: `None` ) – Ignore errors while reading source files.
- **`include`** (`list[str] | None`, default: `None` ) – Include only files whose paths match one of these patterns. Accepts shell-style wildcards, which must be quoted.
- **`omit`** (`list[str] | None`, default: `None` ) – Omit files whose paths match one of these patterns. Accepts shell-style wildcards, which must be quoted.
- **`precision`** (`int | None`, default: `None` ) – Number of digits after the decimal point to display for reported coverage percentages.
- **`quiet`** (`bool | None`, default: `None` ) – Don't print messages about what is happening.
- **`show_contexts`** (`bool | None`, default: `None` ) – Show contexts for covered lines.
- **`skip_covered`** (`bool | None`, default: `None` ) – Skip files with 100% coverage.
- **`skip_empty`** (`bool | None`, default: `None` ) – Skip files with no code.
- **`title`** (`str | None`, default: `None` ) – A text string to use as the title on the HTML.
- **`debug_opts`** (`list[str] | None`, default: `None` ) – Debug options, separated by commas [env: COVERAGE_DEBUG].

Source code in `src/duty/_internal/tools/_coverage.py`

```
@classmethod
def html(
    cls,
    *,
    rcfile: str | None = None,
    contexts: list[str] | None = None,
    directory: str | None = None,
    data_file: str | None = None,
    fail_under: int | None = None,
    ignore_errors: bool | None = None,
    include: list[str] | None = None,
    omit: list[str] | None = None,
    precision: int | None = None,
    quiet: bool | None = None,
    show_contexts: bool | None = None,
    skip_covered: bool | None = None,
    skip_empty: bool | None = None,
    title: str | None = None,
    debug_opts: list[str] | None = None,
) -> coverage:
    """Create an HTML report.

    Create an HTML report of the coverage of the files.  Each file gets its own
    page, with the source decorated to show executed, excluded, and missed lines.

    Parameters:
        rcfile: Specify configuration file. By default `.coveragerc`, `setup.cfg`, `tox.ini`,
            and `pyproject.toml` are tried [env: `COVERAGE_RCFILE`].
        contexts: Only display data from lines covered in the given contexts.
            Accepts Python regexes, which must be quoted.
        directory: Write the output files to this directory.
        data_file: Read coverage data for report generation from this file.
            Defaults to `.coverage` [env: `COVERAGE_FILE`].
        fail_under: Exit with a status of 2 if the total coverage is less than the given number.
        ignore_errors: Ignore errors while reading source files.
        include: Include only files whose paths match one of these patterns. Accepts shell-style wildcards, which must be quoted.
        omit: Omit files whose paths match one of these patterns. Accepts shell-style wildcards, which must be quoted.
        precision: Number of digits after the decimal point to display for reported coverage percentages.
        quiet: Don't print messages about what is happening.
        show_contexts: Show contexts for covered lines.
        skip_covered: Skip files with 100% coverage.
        skip_empty: Skip files with no code.
        title: A text string to use as the title on the HTML.
        debug_opts: Debug options, separated by commas [env: `COVERAGE_DEBUG`].
    """
    cli_args = ["html"]

    if contexts:
        cli_args.append("--contexts")
        cli_args.append(",".join(contexts))

    if directory:
        cli_args.append("--directory")
        cli_args.append(directory)

    if data_file:
        cli_args.append("--data-file")
        cli_args.append(data_file)

    if fail_under is not None:
        cli_args.append("--fail-under")
        cli_args.append(str(fail_under))

    if ignore_errors:
        cli_args.append("--ignore-errors")

    if include:
        cli_args.append("--include")
        cli_args.append(",".join(include))

    if omit:
        cli_args.append("--omit")
        cli_args.append(",".join(omit))

    if precision is not None:
        cli_args.append("--precision")
        cli_args.append(str(precision))

    if quiet:
        cli_args.append("--quiet")

    if show_contexts:
        cli_args.append("--show-contexts")

    if skip_covered is True:
        cli_args.append("--skip-covered")
    elif skip_covered is False:
        cli_args.append("--no-skip-covered")

    if skip_empty:
        cli_args.append("--skip-empty")

    if title:
        cli_args.append("--title")
        cli_args.append(title)

    if debug_opts:
        cli_args.append("--debug")
        cli_args.append(",".join(debug_opts))

    if rcfile:
        cli_args.append("--rcfile")
        cli_args.append(rcfile)

    return cls(cli_args)

```

#### json

```
json(
    *,
    rcfile: str | None = None,
    contexts: list[str] | None = None,
    data_file: str | None = None,
    fail_under: int | None = None,
    ignore_errors: bool | None = None,
    include: list[str] | None = None,
    omit: list[str] | None = None,
    output: str | None = None,
    pretty_print: bool | None = None,
    quiet: bool | None = None,
    show_contexts: bool | None = None,
    debug_opts: list[str] | None = None,
) -> coverage

```

Create a JSON report of coverage results.

Parameters:

- **`rcfile`** (`str | None`, default: `None` ) – Specify configuration file. By default .coveragerc, setup.cfg, tox.ini, and pyproject.toml are tried [env: COVERAGE_RCFILE].
- **`contexts`** (`list[str] | None`, default: `None` ) – Only display data from lines covered in the given contexts. Accepts Python regexes, which must be quoted.
- **`data_file`** (`str | None`, default: `None` ) – Read coverage data for report generation from this file. Defaults to .coverage [env: COVERAGE_FILE].
- **`fail_under`** (`int | None`, default: `None` ) – Exit with a status of 2 if the total coverage is less than the given number.
- **`ignore_errors`** (`bool | None`, default: `None` ) – Ignore errors while reading source files.
- **`include`** (`list[str] | None`, default: `None` ) – Include only files whose paths match one of these patterns. Accepts shell-style wildcards, which must be quoted.
- **`omit`** (`list[str] | None`, default: `None` ) – Omit files whose paths match one of these patterns. Accepts shell-style wildcards, which must be quoted.
- **`output`** (`str | None`, default: `None` ) – Write the JSON report to this file. Defaults to coverage.json.
- **`pretty_print`** (`bool | None`, default: `None` ) – Format the JSON for human readers.
- **`quiet`** (`bool | None`, default: `None` ) – Don't print messages about what is happening.
- **`show_contexts`** (`bool | None`, default: `None` ) – Show contexts for covered lines.
- **`debug_opts`** (`list[str] | None`, default: `None` ) – Debug options, separated by commas [env: COVERAGE_DEBUG].

Source code in `src/duty/_internal/tools/_coverage.py`

```
@classmethod
def json(
    cls,
    *,
    rcfile: str | None = None,
    contexts: list[str] | None = None,
    data_file: str | None = None,
    fail_under: int | None = None,
    ignore_errors: bool | None = None,
    include: list[str] | None = None,
    omit: list[str] | None = None,
    output: str | None = None,
    pretty_print: bool | None = None,
    quiet: bool | None = None,
    show_contexts: bool | None = None,
    debug_opts: list[str] | None = None,
) -> coverage:
    """Create a JSON report of coverage results.

    Parameters:
        rcfile: Specify configuration file. By default `.coveragerc`, `setup.cfg`, `tox.ini`,
            and `pyproject.toml` are tried [env: `COVERAGE_RCFILE`].
        contexts: Only display data from lines covered in the given contexts.
            Accepts Python regexes, which must be quoted.
        data_file: Read coverage data for report generation from this file.
            Defaults to `.coverage` [env: `COVERAGE_FILE`].
        fail_under: Exit with a status of 2 if the total coverage is less than the given number.
        ignore_errors: Ignore errors while reading source files.
        include: Include only files whose paths match one of these patterns. Accepts shell-style wildcards, which must be quoted.
        omit: Omit files whose paths match one of these patterns. Accepts shell-style wildcards, which must be quoted.
        output: Write the JSON report to this file. Defaults to `coverage.json`.
        pretty_print: Format the JSON for human readers.
        quiet: Don't print messages about what is happening.
        show_contexts: Show contexts for covered lines.
        debug_opts: Debug options, separated by commas [env: `COVERAGE_DEBUG`].
    """
    cli_args = ["json"]

    if contexts:
        cli_args.append("--contexts")
        cli_args.append(",".join(contexts))

    if data_file:
        cli_args.append("--data-file")
        cli_args.append(data_file)

    if fail_under is not None:
        cli_args.append("--fail-under")
        cli_args.append(str(fail_under))

    if ignore_errors:
        cli_args.append("--ignore-errors")

    if include:
        cli_args.append("--include")
        cli_args.append(",".join(include))

    if omit:
        cli_args.append("--omit")
        cli_args.append(",".join(omit))

    if output:
        cli_args.append("-o")
        cli_args.append(output)

    if pretty_print:
        cli_args.append("--pretty-print")

    if quiet:
        cli_args.append("--quiet")

    if show_contexts:
        cli_args.append("--show-contexts")

    if debug_opts:
        cli_args.append("--debug")
        cli_args.append(",".join(debug_opts))

    if rcfile:
        cli_args.append("--rcfile")
        cli_args.append(rcfile)

    return cls(cli_args)

```

#### lcov

```
lcov(
    *,
    rcfile: str | None = None,
    data_file: str | None = None,
    fail_under: int | None = None,
    ignore_errors: bool | None = None,
    include: list[str] | None = None,
    omit: list[str] | None = None,
    output: str | None = None,
    quiet: bool | None = None,
    debug_opts: list[str] | None = None,
) -> coverage

```

Create an LCOV report of coverage results.

Parameters:

- **`rcfile`** (`str | None`, default: `None` ) – Specify configuration file. By default .coveragerc, setup.cfg, tox.ini, and pyproject.toml are tried [env: COVERAGE_RCFILE].
- **`data_file`** (`str | None`, default: `None` ) – Read coverage data for report generation from this file. Defaults to .coverage [env: COVERAGE_FILE].
- **`fail_under`** (`int | None`, default: `None` ) – Exit with a status of 2 if the total coverage is less than the given number.
- **`ignore_errors`** (`bool | None`, default: `None` ) – Ignore errors while reading source files.
- **`include`** (`list[str] | None`, default: `None` ) – Include only files whose paths match one of these patterns. Accepts shell-style wildcards, which must be quoted.
- **`omit`** (`list[str] | None`, default: `None` ) – Omit files whose paths match one of these patterns. Accepts shell-style wildcards, which must be quoted.
- **`output`** (`str | None`, default: `None` ) – Write the JSON report to this file. Defaults to coverage.json.
- **`quiet`** (`bool | None`, default: `None` ) – Don't print messages about what is happening.
- **`debug_opts`** (`list[str] | None`, default: `None` ) – Debug options, separated by commas [env: COVERAGE_DEBUG].

Source code in `src/duty/_internal/tools/_coverage.py`

```
@classmethod
def lcov(
    cls,
    *,
    rcfile: str | None = None,
    data_file: str | None = None,
    fail_under: int | None = None,
    ignore_errors: bool | None = None,
    include: list[str] | None = None,
    omit: list[str] | None = None,
    output: str | None = None,
    quiet: bool | None = None,
    debug_opts: list[str] | None = None,
) -> coverage:
    """Create an LCOV report of coverage results.

    Parameters:
        rcfile: Specify configuration file. By default `.coveragerc`, `setup.cfg`, `tox.ini`,
            and `pyproject.toml` are tried [env: `COVERAGE_RCFILE`].
        data_file: Read coverage data for report generation from this file.
            Defaults to `.coverage` [env: `COVERAGE_FILE`].
        fail_under: Exit with a status of 2 if the total coverage is less than the given number.
        ignore_errors: Ignore errors while reading source files.
        include: Include only files whose paths match one of these patterns. Accepts shell-style wildcards, which must be quoted.
        omit: Omit files whose paths match one of these patterns. Accepts shell-style wildcards, which must be quoted.
        output: Write the JSON report to this file. Defaults to `coverage.json`.
        quiet: Don't print messages about what is happening.
        debug_opts: Debug options, separated by commas [env: `COVERAGE_DEBUG`].
    """
    cli_args = ["lcov"]

    if data_file:
        cli_args.append("--data-file")
        cli_args.append(data_file)

    if fail_under is not None:
        cli_args.append("--fail-under")
        cli_args.append(str(fail_under))

    if ignore_errors:
        cli_args.append("--ignore-errors")

    if include:
        cli_args.append("--include")
        cli_args.append(",".join(include))

    if omit:
        cli_args.append("--omit")
        cli_args.append(",".join(omit))

    if output:
        cli_args.append("-o")
        cli_args.append(output)

    if quiet:
        cli_args.append("--quiet")

    if debug_opts:
        cli_args.append("--debug")
        cli_args.append(",".join(debug_opts))

    if rcfile:
        cli_args.append("--rcfile")
        cli_args.append(rcfile)

    return cls(cli_args)

```

#### report

```
report(
    *,
    rcfile: str | None = None,
    contexts: list[str] | None = None,
    data_file: str | None = None,
    fail_under: int | None = None,
    output_format: Literal["text", "markdown", "total"]
    | None = None,
    ignore_errors: bool | None = None,
    include: list[str] | None = None,
    omit: list[str] | None = None,
    precision: int | None = None,
    sort: Literal[
        "name", "stmts", "miss", "branch", "brpart", "cover"
    ]
    | None = None,
    show_missing: bool | None = None,
    skip_covered: bool | None = None,
    skip_empty: bool | None = None,
    debug_opts: list[str] | None = None,
) -> coverage

```

Report coverage statistics on modules.

Parameters:

- **`rcfile`** (`str | None`, default: `None` ) – Specify configuration file. By default .coveragerc, setup.cfg, tox.ini, and pyproject.toml are tried [env: COVERAGE_RCFILE].
- **`contexts`** (`list[str] | None`, default: `None` ) – Only display data from lines covered in the given contexts.
- **`data_file`** (`str | None`, default: `None` ) – Read coverage data for report generation from this file. Defaults to .coverage [env: COVERAGE_FILE].
- **`fail_under`** (`int | None`, default: `None` ) – Exit with a status of 2 if the total coverage is less than the given number.
- **`output_format`** (`Literal['text', 'markdown', 'total'] | None`, default: `None` ) – Output format, either text (default), markdown, or total.
- **`ignore_errors`** (`bool | None`, default: `None` ) – Ignore errors while reading source files.
- **`include`** (`list[str] | None`, default: `None` ) – Include only files whose paths match one of these patterns. Accepts shell-style wildcards, which must be quoted.
- **`omit`** (`list[str] | None`, default: `None` ) – Omit files whose paths match one of these patterns. Accepts shell-style wildcards, which must be quoted.
- **`precision`** (`int | None`, default: `None` ) – Number of digits after the decimal point to display for reported coverage percentages.
- **`sort`** (`Literal['name', 'stmts', 'miss', 'branch', 'brpart', 'cover'] | None`, default: `None` ) – Sort the report by the named column: name, stmts, miss, branch, brpart, or cover. Default is name.
- **`show_missing`** (`bool | None`, default: `None` ) – Show line numbers of statements in each module that weren't executed.
- **`skip_covered`** (`bool | None`, default: `None` ) – Skip files with 100% coverage.
- **`skip_empty`** (`bool | None`, default: `None` ) – Skip files with no code.
- **`debug_opts`** (`list[str] | None`, default: `None` ) – Debug options, separated by commas [env: COVERAGE_DEBUG].

Source code in `src/duty/_internal/tools/_coverage.py`

```
@classmethod
def report(
    cls,
    *,
    rcfile: str | None = None,
    contexts: list[str] | None = None,
    data_file: str | None = None,
    fail_under: int | None = None,
    output_format: Literal["text", "markdown", "total"] | None = None,
    ignore_errors: bool | None = None,
    include: list[str] | None = None,
    omit: list[str] | None = None,
    precision: int | None = None,
    sort: Literal["name", "stmts", "miss", "branch", "brpart", "cover"] | None = None,
    show_missing: bool | None = None,
    skip_covered: bool | None = None,
    skip_empty: bool | None = None,
    debug_opts: list[str] | None = None,
) -> coverage:
    """Report coverage statistics on modules.

    Parameters:
        rcfile: Specify configuration file. By default `.coveragerc`, `setup.cfg`, `tox.ini`,
            and `pyproject.toml` are tried [env: `COVERAGE_RCFILE`].
        contexts: Only display data from lines covered in the given contexts.
        data_file: Read coverage data for report generation from this file.
            Defaults to `.coverage` [env: `COVERAGE_FILE`].
        fail_under: Exit with a status of 2 if the total coverage is less than the given number.
        output_format: Output format, either text (default), markdown, or total.
        ignore_errors: Ignore errors while reading source files.
        include: Include only files whose paths match one of these patterns. Accepts shell-style wildcards, which must be quoted.
        omit: Omit files whose paths match one of these patterns. Accepts shell-style wildcards, which must be quoted.
        precision: Number of digits after the decimal point to display for reported coverage percentages.
        sort: Sort the report by the named column: name, stmts, miss, branch, brpart, or cover. Default is name.
        show_missing: Show line numbers of statements in each module that weren't executed.
        skip_covered: Skip files with 100% coverage.
        skip_empty: Skip files with no code.
        debug_opts: Debug options, separated by commas [env: `COVERAGE_DEBUG`].
    """
    cli_args = ["report"]

    if contexts:
        cli_args.append("--contexts")
        cli_args.append(",".join(contexts))

    if data_file:
        cli_args.append("--data-file")
        cli_args.append(data_file)

    if fail_under is not None:
        cli_args.append("--fail-under")
        cli_args.append(str(fail_under))

    if output_format:
        cli_args.append("--format")
        cli_args.append(output_format)

    if ignore_errors:
        cli_args.append("--ignore-errors")

    if include:
        cli_args.append("--include")
        cli_args.append(",".join(include))

    if omit:
        cli_args.append("--omit")
        cli_args.append(",".join(omit))

    if precision is not None:
        cli_args.append("--precision")
        cli_args.append(str(precision))

    if sort:
        cli_args.append("--sort")
        cli_args.append(sort)

    if show_missing:
        cli_args.append("--show-missing")

    if skip_covered is True:
        cli_args.append("--skip-covered")
    elif skip_covered is False:
        cli_args.append("--no-skip-covered")

    if skip_empty:
        cli_args.append("--skip-empty")

    if debug_opts:
        cli_args.append("--debug")
        cli_args.append(",".join(debug_opts))

    if rcfile:
        cli_args.append("--rcfile")
        cli_args.append(rcfile)

    return cls(cli_args)

```

#### run

```
run(
    pyfile: str,
    *,
    rcfile: str | None = None,
    append: bool | None = None,
    branch: bool | None = None,
    concurrency: list[str] | None = None,
    context: str | None = None,
    data_file: str | None = None,
    include: list[str] | None = None,
    omit: list[str] | None = None,
    module: bool | None = None,
    pylib: bool | None = None,
    parallel_mode: bool | None = None,
    source: list[str] | None = None,
    timid: bool | None = None,
    debug_opts: list[str] | None = None,
) -> coverage

```

Run a Python program and measure code execution.

Parameters:

- **`pyfile`** (`str`) – Python script or module to run.
- **`rcfile`** (`str | None`, default: `None` ) – Specify configuration file. By default .coveragerc, setup.cfg, tox.ini, and pyproject.toml are tried [env: COVERAGE_RCFILE].
- **`append`** (`bool | None`, default: `None` ) – Append coverage data to .coverage, otherwise it starts clean each time.
- **`branch`** (`bool | None`, default: `None` ) – Measure branch coverage in addition to statement coverage.
- **`concurrency`** (`list[str] | None`, default: `None` ) – Properly measure code using a concurrency library. Valid values are: eventlet, gevent, greenlet, multiprocessing, thread, or a comma-list of them.
- **`context`** (`str | None`, default: `None` ) – The context label to record for this coverage run.
- **`data_file`** (`str | None`, default: `None` ) – Read coverage data for report generation from this file. Defaults to .coverage [env: COVERAGE_FILE].
- **`include`** (`list[str] | None`, default: `None` ) – Include only files whose paths match one of these patterns. Accepts shell-style wildcards, which must be quoted.
- **`omit`** (`list[str] | None`, default: `None` ) – Omit files whose paths match one of these patterns. Accepts shell-style wildcards, which must be quoted.
- **`module`** (`bool | None`, default: `None` ) – The given file is an importable Python module, not a script path, to be run as python -m would run it.
- **`pylib`** (`bool | None`, default: `None` ) – Measure coverage even inside the Python installed library, which isn't done by default.
- **`parallel_mode`** (`bool | None`, default: `None` ) – Append the machine name, process id and random number to the data file name to simplify collecting data from many processes.
- **`source`** (`list[str] | None`, default: `None` ) – A list of directories or importable names of code to measure.
- **`timid`** (`bool | None`, default: `None` ) – Use a simpler but slower trace method. Try this if you get seemingly impossible results!
- **`debug_opts`** (`list[str] | None`, default: `None` ) – Debug options, separated by commas [env: COVERAGE_DEBUG].

Source code in `src/duty/_internal/tools/_coverage.py`

```
@classmethod
def run(
    cls,
    pyfile: str,
    *,
    rcfile: str | None = None,
    append: bool | None = None,
    branch: bool | None = None,
    concurrency: list[str] | None = None,
    context: str | None = None,
    data_file: str | None = None,
    include: list[str] | None = None,
    omit: list[str] | None = None,
    module: bool | None = None,
    pylib: bool | None = None,
    parallel_mode: bool | None = None,
    source: list[str] | None = None,
    timid: bool | None = None,
    debug_opts: list[str] | None = None,
) -> coverage:
    """Run a Python program and measure code execution.

    Parameters:
        pyfile: Python script or module to run.
        rcfile: Specify configuration file. By default `.coveragerc`, `setup.cfg`, `tox.ini`,
            and `pyproject.toml` are tried [env: `COVERAGE_RCFILE`].
        append: Append coverage data to .coverage, otherwise it starts clean each time.
        branch: Measure branch coverage in addition to statement coverage.
        concurrency: Properly measure code using a concurrency library. Valid values are:
            eventlet, gevent, greenlet, multiprocessing, thread, or a comma-list of them.
        context: The context label to record for this coverage run.
        data_file: Read coverage data for report generation from this file.
            Defaults to `.coverage` [env: `COVERAGE_FILE`].
        include: Include only files whose paths match one of these patterns. Accepts shell-style wildcards, which must be quoted.
        omit: Omit files whose paths match one of these patterns. Accepts shell-style wildcards, which must be quoted.
        module: The given file is an importable Python module, not a script path, to be run as `python -m` would run it.
        pylib: Measure coverage even inside the Python installed library, which isn't done by default.
        parallel_mode: Append the machine name, process id and random number to the data file name
            to simplify collecting data from many processes.
        source: A list of directories or importable names of code to measure.
        timid: Use a simpler but slower trace method. Try this if you get seemingly impossible results!
        debug_opts: Debug options, separated by commas [env: `COVERAGE_DEBUG`].
    """
    cli_args = ["run", pyfile]

    if append:
        cli_args.append("--append")

    if branch:
        cli_args.append("--branch")

    if concurrency:
        cli_args.append("--concurrency")
        cli_args.append(",".join(concurrency))

    if context:
        cli_args.append("--context")
        cli_args.append(context)

    if data_file:
        cli_args.append("--data-file")
        cli_args.append(data_file)

    if include:
        cli_args.append("--include")
        cli_args.append(",".join(include))

    if omit:
        cli_args.append("--omit")
        cli_args.append(",".join(omit))

    if module:
        cli_args.append("--module")

    if pylib:
        cli_args.append("--pylib")

    if parallel_mode:
        cli_args.append("--parallel-mode")

    if source:
        cli_args.append("--source")
        cli_args.append(",".join(source))

    if timid:
        cli_args.append("--timid")

    if debug_opts:
        cli_args.append("--debug")
        cli_args.append(",".join(debug_opts))

    if rcfile:
        cli_args.append("--rcfile")
        cli_args.append(rcfile)

    return cls(cli_args)

```

#### xml

```
xml(
    *,
    rcfile: str | None = None,
    data_file: str | None = None,
    fail_under: int | None = None,
    ignore_errors: bool | None = None,
    include: list[str] | None = None,
    omit: list[str] | None = None,
    output: str | None = None,
    quiet: bool | None = None,
    skip_empty: bool | None = None,
    debug_opts: list[str] | None = None,
) -> coverage

```

Create an XML report of coverage results.

Parameters:

- **`rcfile`** (`str | None`, default: `None` ) – Specify configuration file. By default .coveragerc, setup.cfg, tox.ini, and pyproject.toml are tried [env: COVERAGE_RCFILE].
- **`data_file`** (`str | None`, default: `None` ) – Read coverage data for report generation from this file. Defaults to .coverage [env: COVERAGE_FILE].
- **`fail_under`** (`int | None`, default: `None` ) – Exit with a status of 2 if the total coverage is less than the given number.
- **`ignore_errors`** (`bool | None`, default: `None` ) – Ignore errors while reading source files.
- **`include`** (`list[str] | None`, default: `None` ) – Include only files whose paths match one of these patterns. Accepts shell-style wildcards, which must be quoted.
- **`omit`** (`list[str] | None`, default: `None` ) – Omit files whose paths match one of these patterns. Accepts shell-style wildcards, which must be quoted.
- **`output`** (`str | None`, default: `None` ) – Write the JSON report to this file. Defaults to coverage.json.
- **`quiet`** (`bool | None`, default: `None` ) – Don't print messages about what is happening.
- **`skip_empty`** (`bool | None`, default: `None` ) – Skip files with no code.
- **`debug_opts`** (`list[str] | None`, default: `None` ) – Debug options, separated by commas [env: COVERAGE_DEBUG].

Source code in `src/duty/_internal/tools/_coverage.py`

```
@classmethod
def xml(
    cls,
    *,
    rcfile: str | None = None,
    data_file: str | None = None,
    fail_under: int | None = None,
    ignore_errors: bool | None = None,
    include: list[str] | None = None,
    omit: list[str] | None = None,
    output: str | None = None,
    quiet: bool | None = None,
    skip_empty: bool | None = None,
    debug_opts: list[str] | None = None,
) -> coverage:
    """Create an XML report of coverage results.

    Parameters:
        rcfile: Specify configuration file. By default `.coveragerc`, `setup.cfg`, `tox.ini`,
            and `pyproject.toml` are tried [env: `COVERAGE_RCFILE`].
        data_file: Read coverage data for report generation from this file.
            Defaults to `.coverage` [env: `COVERAGE_FILE`].
        fail_under: Exit with a status of 2 if the total coverage is less than the given number.
        ignore_errors: Ignore errors while reading source files.
        include: Include only files whose paths match one of these patterns. Accepts shell-style wildcards, which must be quoted.
        omit: Omit files whose paths match one of these patterns. Accepts shell-style wildcards, which must be quoted.
        output: Write the JSON report to this file. Defaults to `coverage.json`.
        quiet: Don't print messages about what is happening.
        skip_empty: Skip files with no code.
        debug_opts: Debug options, separated by commas [env: `COVERAGE_DEBUG`].
    """
    cli_args = ["xml"]

    if data_file:
        cli_args.append("--data-file")
        cli_args.append(data_file)

    if fail_under is not None:
        cli_args.append("--fail-under")
        cli_args.append(str(fail_under))

    if ignore_errors:
        cli_args.append("--ignore-errors")

    if include:
        cli_args.append("--include")
        cli_args.append(",".join(include))

    if omit:
        cli_args.append("--omit")
        cli_args.append(",".join(omit))

    if output:
        cli_args.append("-o")
        cli_args.append(output)

    if quiet:
        cli_args.append("--quiet")

    if skip_empty:
        cli_args.append("--skip-empty")

    if debug_opts:
        cli_args.append("--debug")
        cli_args.append(",".join(debug_opts))

    if rcfile:
        cli_args.append("--rcfile")
        cli_args.append(rcfile)

    return cls(cli_args)

```

### flake8

```
flake8(
    *paths: str,
    config: str | None = None,
    verbose: bool | None = None,
    output_file: str | None = None,
    append_config: str | None = None,
    isolated: bool | None = None,
    enable_extensions: list[str] | None = None,
    require_plugins: list[str] | None = None,
    quiet: bool | None = None,
    color: Literal["auto", "always", "never"] | None = None,
    count: bool | None = None,
    exclude: list[str] | None = None,
    extend_exclude: list[str] | None = None,
    filename: list[str] | None = None,
    stdin_display_name: str | None = None,
    error_format: str | None = None,
    hang_closing: bool | None = None,
    ignore: list[str] | None = None,
    extend_ignore: list[str] | None = None,
    per_file_ignores: dict[str, list[str]] | None = None,
    max_line_length: int | None = None,
    max_doc_length: int | None = None,
    indent_size: int | None = None,
    select: list[str] | None = None,
    extend_select: list[str] | None = None,
    disable_noqa: bool | None = None,
    show_source: bool | None = None,
    no_show_source: bool | None = None,
    statistics: bool | None = None,
    exit_zero: bool | None = None,
    jobs: int | None = None,
    tee: bool | None = None,
    benchmark: bool | None = None,
    bug_report: bool | None = None,
)

```

Bases: `Tool`

Call [Flake8](https://github.com/PyCQA/flake8).

Parameters:

- **`*paths`** (`str`, default: `()` ) – Paths to check.
- **`config`** (`str | None`, default: `None` ) – Path to the config file that will be the authoritative config source. This will cause Flake8 to ignore all other configuration files.
- **`verbose`** (`bool | None`, default: `None` ) – Print more information about what is happening in flake8. This option is repeatable and will increase verbosity each time it is repeated.
- **`output_file`** (`str | None`, default: `None` ) – Redirect report to a file.
- **`append_config`** (`str | None`, default: `None` ) – Provide extra config files to parse in addition to the files found by Flake8 by default. These files are the last ones read and so they take the highest precedence when multiple files provide the same option.
- **`isolated`** (`bool | None`, default: `None` ) – Ignore all configuration files.
- **`enable_extensions`** (`list[str] | None`, default: `None` ) – Enable plugins and extensions that are otherwise disabled by default.
- **`require_plugins`** (`list[str] | None`, default: `None` ) – Require specific plugins to be installed before running.
- **`quiet`** (`bool | None`, default: `None` ) – Report only file names, or nothing. This option is repeatable.
- **`color`** (`Literal['auto', 'always', 'never'] | None`, default: `None` ) – Whether to use color in output. Defaults to auto.
- **`count`** (`bool | None`, default: `None` ) – Print total number of errors to standard output and set the exit code to 1 if total is not empty.
- **`exclude`** (`list[str] | None`, default: `None` ) – Comma-separated list of files or directories to exclude (default: ['.svn', 'CVS', '.bzr', '.hg', '.git', 'pycache', '.tox', '.nox', '.eggs', '\*.egg']).
- **`extend_exclude`** (`list[str] | None`, default: `None` ) – Comma-separated list of files or directories to add to the list of excluded ones.
- **`filename`** (`list[str] | None`, default: `None` ) – Only check for filenames matching the patterns in this comma-separated list (default: ['\*.py']).
- **`stdin_display_name`** (`str | None`, default: `None` ) – The name used when reporting errors from code passed via stdin. This is useful for editors piping the file contents to flake8 (default: stdin).
- **`error_format`** (`str | None`, default: `None` ) – Format errors according to the chosen formatter.
- **`hang_closing`** (`bool | None`, default: `None` ) – Hang closing bracket instead of matching indentation of opening bracket's line.
- **`ignore`** (`list[str] | None`, default: `None` ) – Comma-separated list of error codes to ignore (or skip). For example, --ignore=E4,E51,W234 (default: E121,E123,E126,E226,E24,E704,W503,W504).
- **`extend_ignore`** (`list[str] | None`, default: `None` ) – Comma-separated list of error codes to add to the list of ignored ones. For example, --extend-ignore=E4,E51,W234.
- **`per_file_ignores`** (`dict[str, list[str]] | None`, default: `None` ) – A pairing of filenames and violation codes that defines which violations to ignore in a particular file. The filenames can be specified in a manner similar to the --exclude option and the violations work similarly to the --ignore and --select options.
- **`max_line_length`** (`int | None`, default: `None` ) – Maximum allowed line length for the entirety of this run (default: 79).
- **`max_doc_length`** (`int | None`, default: `None` ) – Maximum allowed doc line length for the entirety of this run (default: None).
- **`indent_size`** (`int | None`, default: `None` ) – Number of spaces used for indentation (default: 4).
- **`select`** (`list[str] | None`, default: `None` ) – Comma-separated list of error codes to enable. For example, --select=E4,E51,W234 (default: E,F,W,C90).
- **`extend_select`** (`list[str] | None`, default: `None` ) – Comma-separated list of error codes to add to the list of selected ones. For example, --extend-select=E4,E51,W234.
- **`disable_noqa`** (`bool | None`, default: `None` ) – Disable the effect of "# noqa". This will report errors on lines with "# noqa" at the end.
- **`show_source`** (`bool | None`, default: `None` ) – Show the source generate each error or warning.
- **`no_show_source`** (`bool | None`, default: `None` ) – Negate --show-source.
- **`statistics`** (`bool | None`, default: `None` ) – Count errors.
- **`exit_zero`** (`bool | None`, default: `None` ) – Exit with status code "0" even if there are errors.
- **`jobs`** (`int | None`, default: `None` ) – Number of subprocesses to use to run checks in parallel. This is ignored on Windows. The default, "auto", will auto-detect the number of processors available to use (default: auto).
- **`tee`** (`bool | None`, default: `None` ) – Write to stdout and output-file.
- **`benchmark`** (`bool | None`, default: `None` ) – Print benchmark information about this run of Flake8.
- **`bug_report`** (`bool | None`, default: `None` ) – Print information necessary when preparing a bug report.

Returns:

- `None` – Success/failure.

Methods:

- **`__call__`** – Run the command.
- **`add_args`** – Append CLI arguments.

Attributes:

- **`cli_args`** (`list[str]`) – Registered command-line arguments.
- **`cli_command`** (`str`) – The equivalent CLI command.
- **`cli_name`** – The name of the executable on PATH.
- **`py_args`** (`dict[str, Any]`) – Registered Python arguments.

Source code in `src/duty/_internal/tools/_flake8.py`

```
def __init__(
    self,
    *paths: str,
    config: str | None = None,
    verbose: bool | None = None,
    output_file: str | None = None,
    append_config: str | None = None,
    isolated: bool | None = None,
    enable_extensions: list[str] | None = None,
    require_plugins: list[str] | None = None,
    quiet: bool | None = None,
    color: Literal["auto", "always", "never"] | None = None,
    count: bool | None = None,
    exclude: list[str] | None = None,
    extend_exclude: list[str] | None = None,
    filename: list[str] | None = None,
    stdin_display_name: str | None = None,
    error_format: str | None = None,
    hang_closing: bool | None = None,
    ignore: list[str] | None = None,
    extend_ignore: list[str] | None = None,
    per_file_ignores: dict[str, list[str]] | None = None,
    max_line_length: int | None = None,
    max_doc_length: int | None = None,
    indent_size: int | None = None,
    select: list[str] | None = None,
    extend_select: list[str] | None = None,
    disable_noqa: bool | None = None,
    show_source: bool | None = None,
    no_show_source: bool | None = None,
    statistics: bool | None = None,
    exit_zero: bool | None = None,
    jobs: int | None = None,
    tee: bool | None = None,
    benchmark: bool | None = None,
    bug_report: bool | None = None,
) -> None:
    """Run `flake8`.

    Parameters:
        *paths: Paths to check.
        config: Path to the config file that will be the authoritative config source.
            This will cause Flake8 to ignore all other configuration files.
        verbose: Print more information about what is happening in flake8.
            This option is repeatable and will increase verbosity each time it is repeated.
        output_file: Redirect report to a file.
        append_config: Provide extra config files to parse in addition to the files found by Flake8 by default.
            These files are the last ones read and so they take the highest precedence when multiple files provide the same option.
        isolated: Ignore all configuration files.
        enable_extensions: Enable plugins and extensions that are otherwise disabled by default.
        require_plugins: Require specific plugins to be installed before running.
        quiet: Report only file names, or nothing. This option is repeatable.
        color: Whether to use color in output. Defaults to `auto`.
        count: Print total number of errors to standard output and set the exit code to 1 if total is not empty.
        exclude: Comma-separated list of files or directories to exclude (default: ['.svn', 'CVS', '.bzr', '.hg', '.git', '__pycache__', '.tox', '.nox', '.eggs', '*.egg']).
        extend_exclude: Comma-separated list of files or directories to add to the list of excluded ones.
        filename: Only check for filenames matching the patterns in this comma-separated list (default: ['*.py']).
        stdin_display_name: The name used when reporting errors from code passed via stdin. This is useful for editors piping the file contents to flake8 (default: stdin).
        error_format: Format errors according to the chosen formatter.
        hang_closing: Hang closing bracket instead of matching indentation of opening bracket's line.
        ignore: Comma-separated list of error codes to ignore (or skip). For example, ``--ignore=E4,E51,W234`` (default: E121,E123,E126,E226,E24,E704,W503,W504).
        extend_ignore: Comma-separated list of error codes to add to the list of ignored ones. For example, ``--extend-ignore=E4,E51,W234``.
        per_file_ignores: A pairing of filenames and violation codes that defines which violations to ignore in a particular file. The filenames can be specified in a manner similar to the ``--exclude`` option and the violations work similarly to the ``--ignore`` and ``--select`` options.
        max_line_length: Maximum allowed line length for the entirety of this run (default: 79).
        max_doc_length: Maximum allowed doc line length for the entirety of this run (default: None).
        indent_size: Number of spaces used for indentation (default: 4).
        select: Comma-separated list of error codes to enable. For example, ``--select=E4,E51,W234`` (default: E,F,W,C90).
        extend_select: Comma-separated list of error codes to add to the list of selected ones. For example, ``--extend-select=E4,E51,W234``.
        disable_noqa: Disable the effect of "# noqa". This will report errors on lines with "# noqa" at the end.
        show_source: Show the source generate each error or warning.
        no_show_source: Negate --show-source.
        statistics: Count errors.
        exit_zero: Exit with status code "0" even if there are errors.
        jobs: Number of subprocesses to use to run checks in parallel. This is ignored on Windows. The default, "auto", will auto-detect the number of processors available to use (default: auto).
        tee: Write to stdout and output-file.
        benchmark: Print benchmark information about this run of Flake8.
        bug_report: Print information necessary when preparing a bug report.

    Returns:
        Success/failure.
    """
    cli_args = list(paths)

    if verbose:
        cli_args.append("--verbose")

    if output_file:
        cli_args.append("--output-file")
        cli_args.append(output_file)

    if append_config:
        cli_args.append("--append-config")
        cli_args.append(append_config)

    if config:
        cli_args.append("--config")
        cli_args.append(config)

    if isolated:
        cli_args.append("--isolated")

    if enable_extensions:
        cli_args.append("--enable-extensions")
        cli_args.append(",".join(enable_extensions))

    if require_plugins:
        cli_args.append("--require-plugins")
        cli_args.append(",".join(require_plugins))

    if quiet:
        cli_args.append("--quiet")

    if color:
        cli_args.append("--color")
        cli_args.append(color)

    if count:
        cli_args.append("--count")

    if exclude:
        cli_args.append("--exclude")
        cli_args.append(",".join(exclude))

    if extend_exclude:
        cli_args.append("--extend-exclude")
        cli_args.append(",".join(extend_exclude))

    if filename:
        cli_args.append("--filename")
        cli_args.append(",".join(filename))

    if stdin_display_name:
        cli_args.append("--stdin-display-name")
        cli_args.append(stdin_display_name)

    if error_format:
        cli_args.append("--format")
        cli_args.append(error_format)

    if hang_closing:
        cli_args.append("--hang-closing")

    if ignore:
        cli_args.append("--ignore")
        cli_args.append(",".join(ignore))

    if extend_ignore:
        cli_args.append("--extend-ignore")
        cli_args.append(",".join(extend_ignore))

    if per_file_ignores:
        cli_args.append("--per-file-ignores")
        cli_args.append(
            " ".join(f"{path}:{','.join(codes)}" for path, codes in per_file_ignores.items()),
        )

    if max_line_length:
        cli_args.append("--max-line-length")
        cli_args.append(str(max_line_length))

    if max_doc_length:
        cli_args.append("--max-doc-length")
        cli_args.append(str(max_doc_length))

    if indent_size:
        cli_args.append("--indent-size")
        cli_args.append(str(indent_size))

    if select:
        cli_args.append("--select")
        cli_args.append(",".join(select))

    if extend_select:
        cli_args.append("--extend-select")
        cli_args.append(",".join(extend_select))

    if disable_noqa:
        cli_args.append("--disable-noqa")

    if show_source:
        cli_args.append("--show-source")

    if no_show_source:
        cli_args.append("--no-show-source")

    if statistics:
        cli_args.append("--statistics")

    if exit_zero:
        cli_args.append("--exit-zero")

    if jobs:
        cli_args.append("--jobs")
        cli_args.append(str(jobs))

    if tee:
        cli_args.append("--tee")

    if benchmark:
        cli_args.append("--benchmark")

    if bug_report:
        cli_args.append("--bug-report")

    super().__init__(cli_args)

```

#### cli_args

```
cli_args: list[str] = cli_args or []

```

Registered command-line arguments.

#### cli_command

```
cli_command: str

```

The equivalent CLI command.

#### cli_name

```
cli_name = 'flake8'

```

The name of the executable on PATH.

#### py_args

```
py_args: dict[str, Any] = py_args or {}

```

Registered Python arguments.

#### __call__

```
__call__() -> int

```

Run the command.

Returns:

- `int` – The exit code of the command.

Source code in `src/duty/_internal/tools/_flake8.py`

```
def __call__(self) -> int:
    """Run the command.

    Returns:
        The exit code of the command.
    """
    from flake8.main.cli import main as run_flake8  # noqa: PLC0415

    return run_flake8(self.cli_args)

```

#### add_args

```
add_args(*args: str) -> Self

```

Append CLI arguments.

Source code in `src/duty/_internal/tools/_base.py`

```
def add_args(self, *args: str) -> Self:
    """Append CLI arguments."""
    self.cli_args.extend(args)
    return self

```

### git_changelog

```
git_changelog(
    repository: str | None = None,
    *,
    config_file: str | None = None,
    bump: str | None = None,
    versioning: Literal["semver", "pep440"] | None = None,
    in_place: bool = False,
    version_regex: str | None = None,
    marker_line: str | None = None,
    output: str | None = None,
    provider: Literal["github", "gitlab", "bitbucket"]
    | None = None,
    parse_refs: bool = False,
    release_notes: bool = False,
    input: str | None = None,
    convention: Literal["basic", "angular", "conventional"]
    | None = None,
    sections: list[str] | None = None,
    template: str | None = None,
    git_trailers: bool = False,
    omit_empty_versions: bool = False,
    no_zerover: bool = False,
    filter_commits: str | None = None,
    jinja_context: list[str] | None = None,
    version: bool = False,
    debug_info: bool = False,
)

```

Bases: `Tool`

Call [git-changelog](https://github.com/pawamoy/git-changelog).

Parameters:

- **`repository`** (`str | None`, default: `None` ) – The repository path, relative or absolute. Default: current working directory.
- **`config_file`** (`str | None`, default: `None` ) – Configuration file(s).
- **`bump`** (`str | None`, default: `None` ) – Specify the bump from latest version for the set of unreleased commits. Can be one of auto, major, minor, patch or a valid SemVer version (eg. 1.2.3). For both SemVer and PEP 440 versioning schemes (see -n), auto will bump the major number if a commit contains breaking changes (or the minor number for 0.x versions, see -Z), else the minor number if there are new features, else the patch number. Default: unset (false).
- **`versioning`** (`Literal['semver', 'pep440'] | None`, default: `None` ) – Versioning scheme to use when bumping and comparing versions. The selected scheme will impact the values accepted by the --bump option. Supported: pep440, semver. PEP 440 provides the following bump strategies: auto, epoch, release, major, minor, micro, patch, pre, alpha, beta, candidate, post, dev. Values auto, major, minor, micro can be suffixed with one of +alpha, +beta, +candidate, and/or +dev. Values alpha, beta and candidate can be suffixed with +dev. Examples: auto+alpha, major+beta+dev, micro+dev, candidate+dev, etc.. SemVer provides the following bump strategies: auto, major, minor, patch, release. See the docs for more information. Default: unset (semver).
- **`in_place`** (`bool`, default: `False` ) – Insert new entries (versions missing from changelog) in-place. An output file must be specified. With custom templates, you can pass two additional arguments: --version-regex and --marker-line. When writing in-place, an in_place variable will be injected in the Jinja context, allowing to adapt the generated contents (for example to skip changelog headers or footers). Default: unset (false).
- **`version_regex`** (`str | None`, default: `None` ) – A regular expression to match versions in the existing changelog (used to find the latest release) when writing in-place. The regular expression must be a Python regex with a version named group. Default: ^## \[(?P<version>v?[^]\]+).
- **`marker_line`** (`str | None`, default: `None` ) – A marker line at which to insert new entries (versions missing from changelog). If two marker lines are present in the changelog, the contents between those two lines will be overwritten (useful to update an 'Unreleased' entry for example). Default: <!-- insertion marker -->.
- **`output`** (`str | None`, default: `None` ) – Output to given file. Default: standard output.
- **`provider`** (`Literal['github', 'gitlab', 'bitbucket'] | None`, default: `None` ) – Explicitly specify the repository provider. Default: unset.
- **`parse_refs`** (`bool`, default: `False` ) – Parse provider-specific references in commit messages (GitHub/GitLab/Bitbucket issues, PRs, etc.). Default: unset (false).
- **`release_notes`** (`bool`, default: `False` ) – Output release notes to stdout based on the last entry in the changelog. Default: unset (false).
- **`input`** (`str | None`, default: `None` ) – Read from given file when creating release notes. Default: CHANGELOG.md.
- **`convention`** (`Literal['basic', 'angular', 'conventional'] | None`, default: `None` ) – The commit convention to match against. Default: basic.
- **`sections`** (`list[str] | None`, default: `None` ) – A comma-separated list of sections to render. See the available sections for each supported convention in the description. Default: unset (None).
- **`template`** (`str | None`, default: `None` ) – The Jinja2 template to use. Prefix it with path: to specify the path to a Jinja templated file. Default: keepachangelog.
- **`git_trailers`** (`bool`, default: `False` ) – Parse Git trailers in the commit message. See https://git-scm.com/docs/git-interpret-trailers. Default: unset (false).
- **`omit_empty_versions`** (`bool`, default: `False` ) – Omit empty versions from the output. Default: unset (false).
- **`no_zerover`** (`bool`, default: `False` ) – By default, breaking changes on a 0.x don't bump the major version, maintaining it at 0. With this option, a breaking change will bump a 0.x version to 1.0.
- **`filter_commits`** (`str | None`, default: `None` ) – The Git revision-range filter to use (e.g. v1.2.0..). Default: no filter.
- **`jinja_context`** (`list[str] | None`, default: `None` ) – Pass additional key/value pairs to the template. Option can be used multiple times. The key/value pairs are accessible as 'jinja_context' in the template.
- **`version`** (`bool`, default: `False` ) – Show the current version of the program and exit.
- **`debug_info`** (`bool`, default: `False` ) – Print debug information.

Methods:

- **`__call__`** – Run the command.
- **`add_args`** – Append CLI arguments.

Attributes:

- **`cli_args`** (`list[str]`) – Registered command-line arguments.
- **`cli_command`** (`str`) – The equivalent CLI command.
- **`cli_name`** – The name of the executable on PATH.
- **`py_args`** (`dict[str, Any]`) – Registered Python arguments.

Source code in `src/duty/_internal/tools/_git_changelog.py`

```
def __init__(
    self,
    repository: str | None = None,
    *,
    config_file: str | None = None,
    bump: str | None = None,
    versioning: Literal["semver", "pep440"] | None = None,
    in_place: bool = False,
    version_regex: str | None = None,
    marker_line: str | None = None,
    output: str | None = None,
    provider: Literal["github", "gitlab", "bitbucket"] | None = None,
    parse_refs: bool = False,
    release_notes: bool = False,
    input: str | None = None,  # noqa: A002
    convention: Literal["basic", "angular", "conventional"] | None = None,
    sections: list[str] | None = None,
    template: str | None = None,
    git_trailers: bool = False,
    omit_empty_versions: bool = False,
    no_zerover: bool = False,
    filter_commits: str | None = None,
    jinja_context: list[str] | None = None,
    version: bool = False,
    debug_info: bool = False,
) -> None:
    r"""Run `git-changelog`.

    Parameters:
        repository: The repository path, relative or absolute. Default: current working directory.
        config_file: Configuration file(s).
        bump: Specify the bump from latest version for the set of unreleased commits.
            Can be one of `auto`, `major`, `minor`, `patch` or a valid SemVer version (eg. 1.2.3).
            For both SemVer and PEP 440 versioning schemes (see -n), `auto` will bump the major number
            if a commit contains breaking changes (or the minor number for 0.x versions, see -Z),
            else the minor number if there are new features, else the patch number. Default: unset (false).
        versioning: Versioning scheme to use when bumping and comparing versions.
            The selected scheme will impact the values accepted by the `--bump` option.
            Supported: `pep440`, `semver`.

            PEP 440 provides the following bump strategies: `auto`, `epoch`, `release`, `major`, `minor`, `micro`, `patch`,
            `pre`, `alpha`, `beta`, `candidate`, `post`, `dev`.
            Values `auto`, `major`, `minor`, `micro` can be suffixed with one of `+alpha`, `+beta`, `+candidate`, and/or `+dev`.
            Values `alpha`, `beta` and `candidate` can be suffixed with `+dev`.
            Examples: `auto+alpha`, `major+beta+dev`, `micro+dev`, `candidate+dev`, etc..

            SemVer provides the following bump strategies: `auto`, `major`, `minor`, `patch`, `release`.
            See the docs for more information. Default: unset (`semver`).
        in_place: Insert new entries (versions missing from changelog) in-place.
            An output file must be specified. With custom templates, you can pass two additional
            arguments: `--version-regex` and `--marker-line`.
            When writing in-place, an `in_place` variable will be injected in the Jinja context,
            allowing to adapt the generated contents (for example to skip changelog headers or footers).
            Default: unset (false).
        version_regex: A regular expression to match versions in the existing changelog
            (used to find the latest release) when writing in-place.
            The regular expression must be a Python regex with a `version` named group.
            Default: `^## \[(?P<version>v?[^\]]+)`.
        marker_line: A marker line at which to insert new entries (versions missing from changelog).
            If two marker lines are present in the changelog, the contents between those two lines
            will be overwritten (useful to update an 'Unreleased' entry for example). Default: `<!-- insertion marker -->`.
        output: Output to given file. Default: standard output.
        provider: Explicitly specify the repository provider. Default: unset.
        parse_refs: Parse provider-specific references in commit messages (GitHub/GitLab/Bitbucket issues, PRs, etc.).
            Default: unset (false).
        release_notes: Output release notes to stdout based on the last entry in the changelog. Default: unset (false).
        input: Read from given file when creating release notes. Default: `CHANGELOG.md`.
        convention: The commit convention to match against. Default: `basic`.
        sections: A comma-separated list of sections to render.
            See the available sections for each supported convention in the description. Default: unset (None).
        template: The Jinja2 template to use.
            Prefix it with `path:` to specify the path to a Jinja templated file. Default: `keepachangelog`.
        git_trailers: Parse Git trailers in the commit message.
            See https://git-scm.com/docs/git-interpret-trailers. Default: unset (false).
        omit_empty_versions: Omit empty versions from the output. Default: unset (false).
        no_zerover: By default, breaking changes on a 0.x don't bump the major version, maintaining it at 0.
            With this option, a breaking change will bump a 0.x version to 1.0.
        filter_commits: The Git revision-range filter to use (e.g. `v1.2.0..`). Default: no filter.
        jinja_context: Pass additional key/value pairs to the template.
            Option can be used multiple times.
            The key/value pairs are accessible as 'jinja_context' in the template.
        version: Show the current version of the program and exit.
        debug_info: Print debug information.
    """
    cli_args = []

    if repository:
        cli_args.append(repository)

    if config_file:
        cli_args.append("--config-file")
        cli_args.append(config_file)

    if bump:
        cli_args.append("--bump")
        cli_args.append(bump)

    if versioning:
        cli_args.append("--versioning")
        cli_args.append(versioning)

    if in_place:
        cli_args.append("--in-place")

    if version_regex:
        cli_args.append("--version-regex")
        cli_args.append(version_regex)

    if marker_line:
        cli_args.append("--marker-line")
        cli_args.append(marker_line)

    if output:
        cli_args.append("--output")
        cli_args.append(output)

    if provider:
        cli_args.append("--provider")
        cli_args.append(provider)

    if parse_refs:
        cli_args.append("--parse-refs")

    if release_notes:
        cli_args.append("--release-notes")

    if input:
        cli_args.append("--input")
        cli_args.append(input)

    if convention:
        cli_args.append("--convention")
        cli_args.append(convention)

    if sections:
        cli_args.append("--sections")
        cli_args.append(",".join(sections))

    if template:
        cli_args.append("--template")
        cli_args.append(template)

    if git_trailers:
        cli_args.append("--git-trailers")

    if omit_empty_versions:
        cli_args.append("--omit-empty-versions")

    if no_zerover:
        cli_args.append("--no-zerover")

    if filter_commits:
        cli_args.append("--filter-commits")
        cli_args.append(filter_commits)

    if jinja_context:
        for key_value in jinja_context:
            cli_args.append("--jinja-context")
            cli_args.append(key_value)

    if version:
        cli_args.append("--version")

    if debug_info:
        cli_args.append("--debug-info")

    super().__init__(cli_args)

```

#### cli_args

```
cli_args: list[str] = cli_args or []

```

Registered command-line arguments.

#### cli_command

```
cli_command: str

```

The equivalent CLI command.

#### cli_name

```
cli_name = 'git-changelog'

```

The name of the executable on PATH.

#### py_args

```
py_args: dict[str, Any] = py_args or {}

```

Registered Python arguments.

#### __call__

```
__call__() -> int

```

Run the command.

Returns:

- `int` – The exit code of the command.

Source code in `src/duty/_internal/tools/_git_changelog.py`

```
def __call__(self) -> int:
    """Run the command.

    Returns:
        The exit code of the command.
    """
    from git_changelog.cli import main as run_git_changelog  # noqa: PLC0415

    return run_git_changelog(self.cli_args)

```

#### add_args

```
add_args(*args: str) -> Self

```

Append CLI arguments.

Source code in `src/duty/_internal/tools/_base.py`

```
def add_args(self, *args: str) -> Self:
    """Append CLI arguments."""
    self.cli_args.extend(args)
    return self

```

### griffe

```
griffe(
    cli_args: list[str] | None = None,
    py_args: dict[str, Any] | None = None,
)

```

Bases: `Tool`

Call [Griffe](https://github.com/mkdocstrings/griffe).

Parameters:

- **`cli_args`** (`list[str] | None`, default: `None` ) – Initial command-line arguments. Use add_args() to add more.
- **`py_args`** (`dict[str, Any] | None`, default: `None` ) – Python arguments. Your __call__ method will be able to access these arguments as self.py_args.

Methods:

- **`__call__`** – Run the command.
- **`add_args`** – Append CLI arguments.
- **`check`** – Check for API breakages or possible improvements.
- **`dump`** – Load package-signatures and dump them as JSON.

Attributes:

- **`cli_args`** (`list[str]`) – Registered command-line arguments.
- **`cli_command`** (`str`) – The equivalent CLI command.
- **`cli_name`** – The name of the executable on PATH.
- **`py_args`** (`dict[str, Any]`) – Registered Python arguments.

Source code in `src/duty/_internal/tools/_base.py`

```
def __init__(
    self,
    cli_args: list[str] | None = None,
    py_args: dict[str, Any] | None = None,
) -> None:
    """Initialize the tool.

    Parameters:
        cli_args: Initial command-line arguments. Use `add_args()` to add more.
        py_args: Python arguments. Your `__call__` method will be able to access
            these arguments as `self.py_args`.
    """
    self.cli_args: list[str] = cli_args or []
    """Registered command-line arguments."""
    self.py_args: dict[str, Any] = py_args or {}
    """Registered Python arguments."""

```

#### cli_args

```
cli_args: list[str] = cli_args or []

```

Registered command-line arguments.

#### cli_command

```
cli_command: str

```

The equivalent CLI command.

#### cli_name

```
cli_name = 'griffe'

```

The name of the executable on PATH.

#### py_args

```
py_args: dict[str, Any] = py_args or {}

```

Registered Python arguments.

#### __call__

```
__call__() -> int

```

Run the command.

Returns:

- `int` – The exit code of the command.

Source code in `src/duty/_internal/tools/_griffe.py`

```
def __call__(self) -> int:
    """Run the command.

    Returns:
        The exit code of the command.
    """
    from griffe import main as run_griffe  # noqa: PLC0415

    return run_griffe(self.cli_args)

```

#### add_args

```
add_args(*args: str) -> Self

```

Append CLI arguments.

Source code in `src/duty/_internal/tools/_base.py`

```
def add_args(self, *args: str) -> Self:
    """Append CLI arguments."""
    self.cli_args.extend(args)
    return self

```

#### check

```
check(
    package: str,
    *,
    against: str | None = None,
    base_ref: str | None = None,
    color: bool = False,
    verbose: bool = False,
    format: Literal[
        "oneline", "verbose", "markdown", "github"
    ]
    | None = None,
    search: list[str] | None = None,
    sys_path: bool = False,
    find_stubs_packages: bool = False,
    extensions: str | list[str] | None = None,
    inspection: bool | None = None,
    log_level: Literal[
        "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
    ]
    | None = None,
    version: bool = False,
    debug_info: bool = False,
) -> griffe

```

Check for API breakages or possible improvements.

Parameters:

- **`package`** (`str`) – Package to find, load and check, as path.
- **`against`** (`str | None`, default: `None` ) – Older Git reference (commit, branch, tag) to check against. Default: load latest tag.
- **`base_ref`** (`str | None`, default: `None` ) – Git reference (commit, branch, tag) to check. Default: load current code.
- **`color`** (`bool`, default: `False` ) – Force enable/disable colors in the output.
- **`verbose`** (`bool`, default: `False` ) – Verbose output.
- **`format`** (`Literal['oneline', 'verbose', 'markdown', 'github'] | None`, default: `None` ) – Output format.
- **`search`** (`list[str] | None`, default: `None` ) – Paths to search packages into.
- **`sys_path`** (`bool`, default: `False` ) – Whether to append sys.path to search paths specified with -s.
- **`find_stubs_packages`** (`bool`, default: `False` ) – Whether to look for stubs-only packages and merge them with concrete ones.
- **`extensions`** (`str | list[str] | None`, default: `None` ) – A comma-separated list or a JSON list of extensions to load.
- **`inspection`** (`bool | None`, default: `None` ) – Whether to disallow or force inspection (dynamic analysis). By default, Griffe tries to use static analysis and falls back to dynamic analysis when it can't.
- **`log_level`** (`Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'] | None`, default: `None` ) – Set the log level: DEBUG, INFO, WARNING, ERROR, CRITICAL.
- **`version`** (`bool`, default: `False` ) – Show program's version number and exit.
- **`debug_info`** (`bool`, default: `False` ) – Print debug information.

Source code in `src/duty/_internal/tools/_griffe.py`

```
@classmethod
def check(
    cls,
    package: str,
    *,
    against: str | None = None,
    base_ref: str | None = None,
    color: bool = False,
    verbose: bool = False,
    format: Literal["oneline", "verbose", "markdown", "github"] | None = None,  # noqa: A002
    search: list[str] | None = None,
    sys_path: bool = False,
    find_stubs_packages: bool = False,
    extensions: str | list[str] | None = None,
    inspection: bool | None = None,
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] | None = None,
    version: bool = False,
    debug_info: bool = False,
) -> griffe:
    """Check for API breakages or possible improvements.

    Parameters:
        package: Package to find, load and check, as path.
        against: Older Git reference (commit, branch, tag) to check against. Default: load latest tag.
        base_ref: Git reference (commit, branch, tag) to check. Default: load current code.
        color: Force enable/disable colors in the output.
        verbose: Verbose output.
        format: Output format.
        search: Paths to search packages into.
        sys_path: Whether to append `sys.path` to search paths specified with `-s`.
        find_stubs_packages: Whether to look for stubs-only packages and merge them with concrete ones.
        extensions: A comma-separated list or a JSON list of extensions to load.
        inspection: Whether to disallow or force inspection (dynamic analysis).
            By default, Griffe tries to use static analysis and falls back to dynamic analysis when it can't.
        log_level: Set the log level: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`.
        version: Show program's version number and exit.
        debug_info: Print debug information.
    """
    cli_args = ["check"]

    if version:
        cli_args.append("--version")

    if debug_info:
        cli_args.append("--debug-info")

    if package:
        cli_args.append(package)

    if against:
        cli_args.append("--against")
        cli_args.append(against)

    if base_ref:
        cli_args.append("--base-ref")
        cli_args.append(base_ref)

    if color is True:
        cli_args.append("--color")
    elif color is False:
        cli_args.append("--no-color")

    if verbose:
        cli_args.append("--verbose")

    if format:
        cli_args.append("--format")
        cli_args.append(format)

    if search:
        for path in search:
            cli_args.append("--search")
            cli_args.append(path)

    if sys_path:
        cli_args.append("--sys-path")

    if find_stubs_packages:
        cli_args.append("--find-stubs-packages")

    if extensions:
        cli_args.append("--extensions")
        if isinstance(extensions, str):
            cli_args.append(extensions)
        else:
            cli_args.append(",".join(extensions))

    if inspection is True:
        cli_args.append("--force-inspection")
    elif inspection is False:
        cli_args.append("--no-inspection")

    if log_level:
        cli_args.append("--log-level")
        cli_args.append(log_level)

    return cls(cli_args)

```

#### dump

```
dump(
    *packages: str,
    full: bool = False,
    output: str | None = None,
    docstyle: str | None = None,
    docopts: str | None = None,
    resolve_aliases: bool = False,
    resolve_implicit: bool = False,
    resolve_external: bool | None = None,
    stats: bool = False,
    search: list[str] | None = None,
    sys_path: bool = False,
    find_stubs_packages: bool = False,
    extensions: str | list[str] | None = None,
    inspection: bool | None = None,
    log_level: Literal[
        "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
    ]
    | None = None,
    version: bool = False,
    debug_info: bool = False,
) -> griffe

```

Load package-signatures and dump them as JSON.

Parameters:

- **`packages`** (`str`, default: `()` ) – Packages to find, load and dump.
- **`full`** (`bool`, default: `False` ) – Whether to dump full data in JSON.
- **`output`** (`str | None`, default: `None` ) – Output file. Supports templating to output each package in its own file, with {package}.
- **`docstyle`** (`str | None`, default: `None` ) – The docstring style to parse.
- **`docopts`** (`str | None`, default: `None` ) – The options for the docstring parser.
- **`resolve_aliases`** (`bool`, default: `False` ) – Whether to resolve aliases.
- **`resolve_implicit`** (`bool`, default: `False` ) – Whether to resolve implicitely exported aliases as well. Aliases are explicitely exported when defined in __all__.
- **`resolve_external`** (`bool | None`, default: `None` ) – Whether to resolve aliases pointing to external/unknown modules (not loaded directly). Default is to resolve only from one module to its private sibling (ast -> \_ast).
- **`stats`** (`bool`, default: `False` ) – Show statistics at the end.
- **`search`** (`list[str] | None`, default: `None` ) – Paths to search packages into.
- **`sys_path`** (`bool`, default: `False` ) – Whether to append sys.path to search paths specified with -s.
- **`find_stubs_packages`** (`bool`, default: `False` ) – Whether to look for stubs-only packages and merge them with concrete ones.
- **`extensions`** (`str | list[str] | None`, default: `None` ) – A comma-separated list or a JSON list of extensions to load.
- **`inspection`** (`bool | None`, default: `None` ) – Whether to disallow or force inspection (dynamic analysis). By default, Griffe tries to use static analysis and falls back to dynamic analysis when it can't.
- **`log_level`** (`Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'] | None`, default: `None` ) – Set the log level: DEBUG, INFO, WARNING, ERROR, CRITICAL.
- **`version`** (`bool`, default: `False` ) – Show program's version number and exit.
- **`debug_info`** (`bool`, default: `False` ) – Print debug information.

Source code in `src/duty/_internal/tools/_griffe.py`

```
@classmethod
def dump(
    cls,
    *packages: str,
    full: bool = False,
    output: str | None = None,
    docstyle: str | None = None,
    docopts: str | None = None,
    resolve_aliases: bool = False,
    resolve_implicit: bool = False,
    resolve_external: bool | None = None,
    stats: bool = False,
    search: list[str] | None = None,
    sys_path: bool = False,
    find_stubs_packages: bool = False,
    extensions: str | list[str] | None = None,
    inspection: bool | None = None,
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] | None = None,
    version: bool = False,
    debug_info: bool = False,
) -> griffe:
    """Load package-signatures and dump them as JSON.

    Parameters:
        packages: Packages to find, load and dump.
        full: Whether to dump full data in JSON.
        output: Output file. Supports templating to output each package in its own file, with `{package}`.
        docstyle: The docstring style to parse.
        docopts: The options for the docstring parser.
        resolve_aliases: Whether to resolve aliases.
        resolve_implicit: Whether to resolve implicitely exported aliases as well. Aliases are explicitely exported when defined in `__all__`.
        resolve_external: Whether to resolve aliases pointing to external/unknown modules (not loaded directly).
            Default is to resolve only from one module to its private sibling (`ast` -> `_ast`).
        stats: Show statistics at the end.
        search: Paths to search packages into.
        sys_path: Whether to append `sys.path` to search paths specified with `-s`.
        find_stubs_packages: Whether to look for stubs-only packages and merge them with concrete ones.
        extensions: A comma-separated list or a JSON list of extensions to load.
        inspection: Whether to disallow or force inspection (dynamic analysis).
            By default, Griffe tries to use static analysis and falls back to dynamic analysis when it can't.
        log_level: Set the log level: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`.
        version: Show program's version number and exit.
        debug_info: Print debug information.
    """
    cli_args = ["dump", *packages]

    if version:
        cli_args.append("--version")

    if debug_info:
        cli_args.append("--debug-info")

    if full:
        cli_args.append("--full")

    if output:
        cli_args.append("--output")
        cli_args.append(output)

    if docstyle:
        cli_args.append("--docstyle")
        cli_args.append(docstyle)

    if docopts:
        cli_args.append("--docopts")
        cli_args.append(docopts)

    if resolve_aliases:
        cli_args.append("--resolve-aliases")

    if resolve_implicit:
        cli_args.append("--resolve-implicit")

    if resolve_external is True:
        cli_args.append("--resolve-external")
    elif resolve_external is False:
        cli_args.append("--no-resolve-external")

    if stats:
        cli_args.append("--stats")

    if search:
        for path in search:
            cli_args.append("--search")
            cli_args.append(path)

    if sys_path:
        cli_args.append("--sys-path")

    if find_stubs_packages:
        cli_args.append("--find-stubs-packages")

    if extensions:
        cli_args.append("--extensions")
        if isinstance(extensions, str):
            cli_args.append(extensions)
        else:
            cli_args.append(",".join(extensions))

    if inspection is True:
        cli_args.append("--force-inspection")
    elif inspection is False:
        cli_args.append("--no-inspection")

    if log_level:
        cli_args.append("--log-level")
        cli_args.append(log_level)

    return cls(cli_args)

```

### interrogate

```
interrogate(
    *src: str,
    verbose: int | None = None,
    quiet: bool | None = None,
    fail_under: float | None = None,
    exclude: str | None = None,
    ignore_init_method: bool | None = None,
    ignore_init_module: bool | None = None,
    ignore_magic: bool | None = None,
    ignore_module: bool | None = None,
    ignore_nested_functions: bool | None = None,
    ignore_nested_classes: bool | None = None,
    ignore_private: bool | None = None,
    ignore_property_decorators: bool | None = None,
    ignore_setters: bool | None = None,
    ignore_semiprivate: bool | None = None,
    ignore_regex: str | None = None,
    whitelist_regex: str | None = None,
    output: str | None = None,
    config: str | None = None,
    color: bool | None = None,
    omit_covered_files: bool | None = None,
    generate_badge: str | None = None,
    badge_format: Literal["png", "svg"] | None = None,
    badge_style: _BADGE_STYLE | None = None,
)

```

Bases: `Tool`

Call [Interrogate](https://github.com/econchick/interrogate).

Parameters:

- **`src`** (`str`, default: `()` ) – Format the directories and file paths.
- **`verbose`** (`int | None`, default: `None` ) – Level of verbosity.
- **`quiet`** (`bool | None`, default: `None` ) – Do not print output.
- **`fail_under`** (`float | None`, default: `None` ) – Fail when coverage % is less than a given amount.
- **`exclude`** (`str | None`, default: `None` ) – Exclude PATHs of files and/or directories.
- **`ignore_init_method`** (`bool | None`, default: `None` ) – Ignore __init__ method of classes.
- **`ignore_init_module`** (`bool | None`, default: `None` ) – Ignore __init__.py modules.
- **`ignore_magic`** (`bool | None`, default: `None` ) – Ignore all magic methods of classes.
- **`ignore_module`** (`bool | None`, default: `None` ) – Ignore module-level docstrings.
- **`ignore_nested_functions`** (`bool | None`, default: `None` ) – Ignore nested functions and methods.
- **`ignore_nested_classes`** (`bool | None`, default: `None` ) – Ignore nested classes.
- **`ignore_private`** (`bool | None`, default: `None` ) – Ignore private classes, methods, and functions starting with two underscores.
- **`ignore_property_decorators`** (`bool | None`, default: `None` ) – Ignore methods with property setter/getter decorators.
- **`ignore_setters`** (`bool | None`, default: `None` ) – Ignore methods with property setter decorators.
- **`ignore_semiprivate`** (`bool | None`, default: `None` ) – Ignore semiprivate classes, methods, and functions starting with a single underscore.
- **`ignore_regex`** (`str | None`, default: `None` ) – Regex identifying class, method, and function names to ignore.
- **`whitelist_regex`** (`str | None`, default: `None` ) – Regex identifying class, method, and function names to include.
- **`output`** (`str | None`, default: `None` ) – Write output to a given FILE.
- **`config`** (`str | None`, default: `None` ) – Read configuration from pyproject.toml or setup.cfg.
- **`color`** (`bool | None`, default: `None` ) – Toggle color output on/off when printing to stdout.
- **`omit_covered_files`** (`bool | None`, default: `None` ) – Omit reporting files that have 100% documentation coverage.
- **`generate_badge`** (`str | None`, default: `None` ) – Generate a shields.io status badge (an SVG image) in at a given file or directory.
- **`badge_format`** (`Literal['png', 'svg'] | None`, default: `None` ) – File format for the generated badge.
- **`badge_style`** (`_BADGE_STYLE | None`, default: `None` ) – Desired style of shields.io badge.

Methods:

- **`__call__`** – Run the command.
- **`add_args`** – Append CLI arguments.

Attributes:

- **`cli_args`** (`list[str]`) – Registered command-line arguments.
- **`cli_command`** (`str`) – The equivalent CLI command.
- **`cli_name`** – The name of the executable on PATH.
- **`py_args`** (`dict[str, Any]`) – Registered Python arguments.

Source code in `src/duty/_internal/tools/_interrogate.py`

```
def __init__(
    self,
    *src: str,
    verbose: int | None = None,
    quiet: bool | None = None,
    fail_under: float | None = None,
    exclude: str | None = None,
    ignore_init_method: bool | None = None,
    ignore_init_module: bool | None = None,
    ignore_magic: bool | None = None,
    ignore_module: bool | None = None,
    ignore_nested_functions: bool | None = None,
    ignore_nested_classes: bool | None = None,
    ignore_private: bool | None = None,
    ignore_property_decorators: bool | None = None,
    ignore_setters: bool | None = None,
    ignore_semiprivate: bool | None = None,
    ignore_regex: str | None = None,
    whitelist_regex: str | None = None,
    output: str | None = None,
    config: str | None = None,
    color: bool | None = None,
    omit_covered_files: bool | None = None,
    generate_badge: str | None = None,
    badge_format: Literal["png", "svg"] | None = None,
    badge_style: _BADGE_STYLE | None = None,
) -> None:
    """Run `interrogate`.

    Args:
        src: Format the directories and file paths.
        verbose: Level of verbosity.
        quiet: Do not print output.
        fail_under: Fail when coverage % is less than a given amount.
        exclude: Exclude PATHs of files and/or directories.
        ignore_init_method: Ignore `__init__` method of classes.
        ignore_init_module: Ignore `__init__.py` modules.
        ignore_magic: Ignore all magic methods of classes.
        ignore_module: Ignore module-level docstrings.
        ignore_nested_functions: Ignore nested functions and methods.
        ignore_nested_classes: Ignore nested classes.
        ignore_private: Ignore private classes, methods, and functions starting with two underscores.
        ignore_property_decorators: Ignore methods with property setter/getter decorators.
        ignore_setters: Ignore methods with property setter decorators.
        ignore_semiprivate: Ignore semiprivate classes, methods, and functions starting with a single underscore.
        ignore_regex: Regex identifying class, method, and function names to ignore.
        whitelist_regex: Regex identifying class, method, and function names to include.
        output: Write output to a given FILE.
        config: Read configuration from pyproject.toml or setup.cfg.
        color: Toggle color output on/off when printing to stdout.
        omit_covered_files: Omit reporting files that have 100% documentation coverage.
        generate_badge: Generate a shields.io status badge (an SVG image) in at a given file or directory.
        badge_format: File format for the generated badge.
        badge_style: Desired style of shields.io badge.
    """
    cli_args = list(src)

    if verbose:
        cli_args.append("--verbose")
        cli_args.append(str(verbose))

    if quiet:
        cli_args.append("--quiet")

    if fail_under:
        cli_args.append("--fail-under")
        cli_args.append(str(fail_under))

    if exclude:
        cli_args.append("--exclude")
        cli_args.append(exclude)

    if ignore_init_method:
        cli_args.append("--ignore-init-method")

    if ignore_init_module:
        cli_args.append("--ignore-init-module")

    if ignore_magic:
        cli_args.append("--ignore-magic")

    if ignore_module:
        cli_args.append("--ignore-module")

    if ignore_nested_functions:
        cli_args.append("--ignore-nested-functions")

    if ignore_nested_classes:
        cli_args.append("--ignore-nested-classes")

    if ignore_private:
        cli_args.append("--ignore-private")

    if ignore_property_decorators:
        cli_args.append("--ignore-property-decorators")

    if ignore_setters:
        cli_args.append("--ignore-setters")

    if ignore_semiprivate:
        cli_args.append("--ignore-semiprivate")

    if ignore_regex:
        cli_args.append("--ignore-regex")
        cli_args.append(ignore_regex)

    if whitelist_regex:
        cli_args.append("--whitelist-regex")
        cli_args.append(whitelist_regex)

    if output:
        cli_args.append("--output")
        cli_args.append(output)

    if omit_covered_files:
        cli_args.append("--omit-covered-files")

    if generate_badge:
        cli_args.append("--generate-badge")
        cli_args.append(generate_badge)

    if badge_format:
        cli_args.append("--badge-format")
        cli_args.append(badge_format)

    if badge_style:
        cli_args.append("--badge-style")
        cli_args.append(badge_style)

    if config:
        cli_args.append("--config")
        cli_args.append(config)

    if color is True:
        cli_args.append("--color")
    elif color is False:
        cli_args.append("--no-color")

    super().__init__(cli_args)

```

#### cli_args

```
cli_args: list[str] = cli_args or []

```

Registered command-line arguments.

#### cli_command

```
cli_command: str

```

The equivalent CLI command.

#### cli_name

```
cli_name = 'interrogate'

```

The name of the executable on PATH.

#### py_args

```
py_args: dict[str, Any] = py_args or {}

```

Registered Python arguments.

#### __call__

```
__call__() -> None

```

Run the command.

Source code in `src/duty/_internal/tools/_interrogate.py`

```
def __call__(self) -> None:
    """Run the command."""
    from interrogate.cli import main as run_interrogate  # noqa: PLC0415

    return run_interrogate(self.cli_args)

```

#### add_args

```
add_args(*args: str) -> Self

```

Append CLI arguments.

Source code in `src/duty/_internal/tools/_base.py`

```
def add_args(self, *args: str) -> Self:
    """Append CLI arguments."""
    self.cli_args.extend(args)
    return self

```

### isort

```
isort(
    *files: str,
    settings: str | None = None,
    verbose: bool | None = None,
    only_modified: bool | None = None,
    dedup_headings: bool | None = None,
    quiet: bool | None = None,
    stdout: bool | None = None,
    overwrite_in_place: bool | None = None,
    show_config: bool | None = None,
    show_files: bool | None = None,
    diff: bool | None = None,
    check: bool | None = None,
    ignore_whitespace: bool | None = None,
    config_root: str | None = None,
    resolve_all_configs: bool | None = None,
    profile: str | None = None,
    jobs: int | None = None,
    atomic: bool | None = None,
    interactive: bool | None = None,
    format_error: str | None = None,
    format_success: str | None = None,
    sort_reexports: bool | None = None,
    filter_files: bool | None = None,
    skip: list[str] | None = None,
    extend_skip: list[str] | None = None,
    skip_glob: list[str] | None = None,
    extend_skip_glob: list[str] | None = None,
    skip_gitignore: bool | None = None,
    supported_extension: list[str] | None = None,
    blocked_extension: list[str] | None = None,
    dont_follow_links: bool | None = None,
    filename: str | None = None,
    allow_root: bool | None = None,
    add_import: str | None = None,
    append_only: bool | None = None,
    force_adds: bool | None = None,
    remove_import: str | None = None,
    float_to_top: bool | None = None,
    dont_float_to_top: bool | None = None,
    combine_as: bool | None = None,
    combine_star: bool | None = None,
    balanced: bool | None = None,
    from_first: bool | None = None,
    force_grid_wrap: int | None = None,
    indent: str | None = None,
    lines_before_imports: int | None = None,
    lines_after_imports: int | None = None,
    lines_between_types: int | None = None,
    line_ending: str | None = None,
    length_sort: bool | None = None,
    length_sort_straight: bool | None = None,
    multi_line: Multiline | None = None,
    ensure_newline_before_comments: bool | None = None,
    no_inline_sort: bool | None = None,
    order_by_type: bool | None = None,
    dont_order_by_type: bool | None = None,
    reverse_relative: bool | None = None,
    reverse_sort: bool | None = None,
    sort_order: Literal["natural", "native"] | None = None,
    force_single_line_imports: bool | None = None,
    single_line_exclusions: list[str] | None = None,
    trailing_comma: bool | None = None,
    use_parentheses: bool | None = None,
    line_length: int | None = None,
    wrap_length: int | None = None,
    case_sensitive: bool | None = None,
    remove_redundant_aliases: bool | None = None,
    honor_noqa: bool | None = None,
    treat_comment_as_code: str | None = None,
    treat_all_comment_as_code: bool | None = None,
    formatter: str | None = None,
    color: bool | None = None,
    ext_format: str | None = None,
    star_first: bool | None = None,
    split_on_trailing_comma: bool | None = None,
    section_default: Literal[
        "FUTURE",
        "STDLIB",
        "THIRDPARTY",
        "FIRSTPARTY",
        "LOCALFOLDER",
    ]
    | None = None,
    only_sections: bool | None = None,
    no_sections: bool | None = None,
    force_alphabetical_sort: bool | None = None,
    force_sort_within_sections: bool | None = None,
    honor_case_in_force_sorted_sections: bool | None = None,
    sort_relative_in_force_sorted_sections: bool
    | None = None,
    force_alphabetical_sort_within_sections: bool
    | None = None,
    top: str | None = None,
    combine_straight_imports: bool | None = None,
    no_lines_before: list[str] | None = None,
    src_path: list[str] | None = None,
    builtin: str | None = None,
    extra_builtin: str | None = None,
    future: str | None = None,
    thirdparty: str | None = None,
    project: str | None = None,
    known_local_folder: str | None = None,
    virtual_env: str | None = None,
    conda_env: str | None = None,
    python_version: Literal[
        "all",
        "2",
        "27",
        "3",
        "36",
        "37",
        "38",
        "39",
        "310",
        "311",
        "auto",
    ]
    | None = None,
)

```

Bases: `Tool`

Call [isort](https://github.com/PyCQA/isort).

Sort Python import definitions alphabetically within logical sections. Run with no arguments to see a quick start guide, otherwise, one or more files/directories/stdin must be provided. Use `-` as the first argument to represent stdin. Use --interactive to use the pre 5.0.0 interactive behavior. If you've used isort 4 but are new to isort 5, see the upgrading guide: <https://pycqa.github.io/isort/docs/upgrade_guides/5.0.0.html>.

Parameters:

- **`*files`** (`str`, default: `()` ) – One or more Python source files that need their imports sorted.
- **`settings`** (`str | None`, default: `None` ) – Explicitly set the settings path or file instead of auto determining based on file location.
- **`verbose`** (`bool | None`, default: `None` ) – Shows verbose output, such as when files are skipped or when a check is successful.
- **`only_modified`** (`bool | None`, default: `None` ) – Suppresses verbose output for non-modified files.
- **`dedup_headings`** (`bool | None`, default: `None` ) – Tells isort to only show an identical custom import heading comment once, even if there are multiple sections with the comment set.
- **`quiet`** (`bool | None`, default: `None` ) – Shows extra quiet output, only errors are outputted.
- **`stdout`** (`bool | None`, default: `None` ) – Force resulting output to stdout, instead of in-place.
- **`overwrite_in_place`** (`bool | None`, default: `None` ) – Tells isort to overwrite in place using the same file handle. Comes at a performance and memory usage penalty over its standard approach but ensures all file flags and modes stay unchanged.
- **`show_config`** (`bool | None`, default: `None` ) – See isort's determined config, as well as sources of config options.
- **`show_files`** (`bool | None`, default: `None` ) – See the files isort will be run against with the current config options.
- **`diff`** (`bool | None`, default: `None` ) – Prints a diff of all the changes isort would make to a file, instead of changing it in place
- **`check`** (`bool | None`, default: `None` ) – Checks the file for unsorted / unformatted imports and prints them to the command line without modifying the file. Returns 0 when nothing would change and returns 1 when the file would be reformatted.
- **`ignore_whitespace`** (`bool | None`, default: `None` ) – Tells isort to ignore whitespace differences when --check-only is being used.
- **`config_root`** (`str | None`, default: `None` ) – Explicitly set the config root for resolving all configs. When used with the --resolve-all-configs flag, isort will look at all sub-folders in this config root to resolve config files and sort files based on the closest available config(if any)
- **`resolve_all_configs`** (`bool | None`, default: `None` ) – Tells isort to resolve the configs for all sub-directories and sort files in terms of its closest config files.
- **`profile`** (`str | None`, default: `None` ) – Base profile type to use for configuration. Profiles include: black, django, pycharm, google, open_stack, plone, attrs, hug, wemake, appnexus. As well as any shared profiles.
- **`jobs`** (`int | None`, default: `None` ) – Number of files to process in parallel. Negative value means use number of CPUs.
- **`atomic`** (`bool | None`, default: `None` ) – Ensures the output doesn't save if the resulting file contains syntax errors.
- **`interactive`** (`bool | None`, default: `None` ) – Tells isort to apply changes interactively.
- **`format_error`** (`str | None`, default: `None` ) – Override the format used to print errors.
- **`format_success`** (`str | None`, default: `None` ) – Override the format used to print success.
- **`sort_reexports`** (`bool | None`, default: `None` ) – Automatically sort all re-exports (module level all collections)
- **`filter_files`** (`bool | None`, default: `None` ) – Tells isort to filter files even when they are explicitly passed in as part of the CLI command.
- **`skip`** (`list[str] | None`, default: `None` ) – Files that isort should skip over. If you want to skip multiple files you should specify twice: --skip file1 --skip file2. Values can be file names, directory names or file paths. To skip all files in a nested path use --skip-glob.
- **`extend_skip`** (`list[str] | None`, default: `None` ) – Extends --skip to add additional files that isort should skip over. If you want to skip multiple files you should specify twice: --skip file1 --skip file2. Values can be file names, directory names or file paths. To skip all files in a nested path use --skip-glob.
- **`skip_glob`** (`list[str] | None`, default: `None` ) – Files that isort should skip over.
- **`extend_skip_glob`** (`list[str] | None`, default: `None` ) – Additional files that isort should skip over (extending --skip-glob).
- **`skip_gitignore`** (`bool | None`, default: `None` ) – Treat project as a git repository and ignore files listed in .gitignore. NOTE: This requires git to be installed and accessible from the same shell as isort.
- **`supported_extension`** (`list[str] | None`, default: `None` ) – Specifies what extensions isort can be run against.
- **`blocked_extension`** (`list[str] | None`, default: `None` ) – Specifies what extensions isort can never be run against.
- **`dont_follow_links`** (`bool | None`, default: `None` ) – Tells isort not to follow symlinks that are encountered when running recursively.
- **`filename`** (`str | None`, default: `None` ) – Provide the filename associated with a stream.
- **`allow_root`** (`bool | None`, default: `None` ) – Tells isort not to treat / specially, allowing it to be run against the root dir.
- **`add_import`** (`str | None`, default: `None` ) – Adds the specified import line to all files, automatically determining correct placement.
- **`append_only`** (`bool | None`, default: `None` ) – Only adds the imports specified in --add-import if the file contains existing imports.
- **`force_adds`** (`bool | None`, default: `None` ) – Forces import adds even if the original file is empty.
- **`remove_import`** (`str | None`, default: `None` ) – Removes the specified import from all files.
- **`float_to_top`** (`bool | None`, default: `None` ) – Causes all non-indented imports to float to the top of the file having its imports sorted (immediately below the top of file comment). This can be an excellent shortcut for collecting imports every once in a while when you place them in the middle of a file to avoid context switching. NOTE: It currently doesn't work with cimports and introduces some extra over-head and a performance penalty.
- **`dont_float_to_top`** (`bool | None`, default: `None` ) – Forces --float-to-top setting off. See --float-to-top for more information.
- **`combine_as`** (`bool | None`, default: `None` ) – Combines as imports on the same line.
- **`combine_star`** (`bool | None`, default: `None` ) – Ensures that if a star import is present, nothing else is imported from that namespace.
- **`balanced`** (`bool | None`, default: `None` ) – Balances wrapping to produce the most consistent line length possible
- **`from_first`** (`bool | None`, default: `None` ) – Switches the typical ordering preference, showing from imports first then straight ones.
- **`force_grid_wrap`** (`int | None`, default: `None` ) – Force number of from imports (defaults to 2 when passed as CLI flag without value) to be grid wrapped regardless of line length. If 0 is passed in (the global default) only line length is considered.
- **`indent`** (`str | None`, default: `None` ) – String to place for indents defaults to " " (4 spaces).
- **`lines_before_imports`** (`int | None`, default: `None` ) – Number of lines to insert before imports.
- **`lines_after_imports`** (`int | None`, default: `None` ) – Number of lines to insert after imports.
- **`lines_between_types`** (`int | None`, default: `None` ) – Number of lines to insert between imports.
- **`line_ending`** (`str | None`, default: `None` ) – Forces line endings to the specified value. If not set, values will be guessed per-file.
- **`length_sort`** (`bool | None`, default: `None` ) – Sort imports by their string length.
- **`length_sort_straight`** (`bool | None`, default: `None` ) – Sort straight imports by their string length. Similar to length_sort but applies only to straight imports and doesn't affect from imports.
- **`multi_line`** (`Multiline | None`, default: `None` ) – Multi line output (0-grid, 1-vertical, 2-hanging, 3-vert-hanging, 4-vert-grid, 5-vert-grid-grouped, 6-deprecated-alias-for-5, 7-noqa, 8-vertical-hanging-indent-bracket, 9-vertical-prefix-from- module-import, 10-hanging-indent-with-parentheses).
- **`ensure_newline_before_comments`** (`bool | None`, default: `None` ) – Inserts a blank line before a comment following an import.
- **`no_inline_sort`** (`bool | None`, default: `None` ) – Leaves from imports with multiple imports 'as-is' (e.g. from foo import a, c ,b).
- **`order_by_type`** (`bool | None`, default: `None` ) – Order imports by type, which is determined by case, in addition to alphabetically. NOTE: type here refers to the implied type from the import name capitalization. isort does not do type introspection for the imports. These "types" are simply: CONSTANT_VARIABLE, CamelCaseClass, variable_or_function. If your project follows PEP8 or a related coding standard and has many imports this is a good default, otherwise you likely will want to turn it off. From the CLI the --dont-order-by-type option will turn this off.
- **`dont_order_by_type`** (`bool | None`, default: `None` ) – Don't order imports by type, which is determined by case, in addition to alphabetically. NOTE: type here refers to the implied type from the import name capitalization. isort does not do type introspection for the imports. These "types" are simply: CONSTANT_VARIABLE, CamelCaseClass, variable_or_function. If your project follows PEP8 or a related coding standard and has many imports this is a good default. You can turn this on from the CLI using --order-by-type.
- **`reverse_relative`** (`bool | None`, default: `None` ) – Reverse order of relative imports.
- **`reverse_sort`** (`bool | None`, default: `None` ) – Reverses the ordering of imports.
- **`sort_order`** (`Literal['natural', 'native'] | None`, default: `None` ) – Specify sorting function. Can be built in (natural[default] = force numbers to be sequential, native = Python's built-in sorted function) or an installable plugin.
- **`force_single_line_imports`** (`bool | None`, default: `None` ) – Forces all from imports to appear on their own line
- **`single_line_exclusions`** (`list[str] | None`, default: `None` ) – One or more modules to exclude from the single line rule.
- **`trailing_comma`** (`bool | None`, default: `None` ) – Includes a trailing comma on multi line imports that include parentheses.
- **`use_parentheses`** (`bool | None`, default: `None` ) – Use parentheses for line continuation on length limit instead of slashes. NOTE: This is separate from wrap modes, and only affects how individual lines that are too long get continued, not sections of multiple imports.
- **`line_length`** (`int | None`, default: `None` ) – The max length of an import line (used for wrapping long imports).
- **`wrap_length`** (`int | None`, default: `None` ) – Specifies how long lines that are wrapped should be, if not set line_length is used. NOTE: wrap_length must be LOWER than or equal to line_length.
- **`case_sensitive`** (`bool | None`, default: `None` ) – Tells isort to include casing when sorting module names
- **`remove_redundant_aliases`** (`bool | None`, default: `None` ) – Tells isort to remove redundant aliases from imports, such as import os as os. This defaults to False simply because some projects use these seemingly useless aliases to signify intent and change behaviour.
- **`honor_noqa`** (`bool | None`, default: `None` ) – Tells isort to honor noqa comments to enforce skipping those comments.
- **`treat_comment_as_code`** (`str | None`, default: `None` ) – Tells isort to treat the specified single line comment(s) as if they are code.
- **`treat_all_comment_as_code`** (`bool | None`, default: `None` ) – Tells isort to treat all single line comments as if they are code.
- **`formatter`** (`str | None`, default: `None` ) – Specifies the name of a formatting plugin to use when producing output.
- **`color`** (`bool | None`, default: `None` ) – Tells isort to use color in terminal output.
- **`ext_format`** (`str | None`, default: `None` ) – Tells isort to format the given files according to an extensions formatting rules.
- **`star_first`** (`bool | None`, default: `None` ) – Forces star imports above others to avoid overriding directly imported variables.
- **`split_on_trailing_comma`** (`bool | None`, default: `None` ) – Split imports list followed by a trailing comma into VERTICAL_HANGING_INDENT mode
- **`section_default`** (`Literal['FUTURE', 'STDLIB', 'THIRDPARTY', 'FIRSTPARTY', 'LOCALFOLDER'] | None`, default: `None` ) – Sets the default section for import options: ('FUTURE', 'STDLIB', 'THIRDPARTY', 'FIRSTPARTY', 'LOCALFOLDER')
- **`only_sections`** (`bool | None`, default: `None` ) – Causes imports to be sorted based on their sections like STDLIB, THIRDPARTY, etc. Within sections, the imports are ordered by their import style and the imports with the same style maintain their relative positions.
- **`no_sections`** (`bool | None`, default: `None` ) – Put all imports into the same section bucket
- **`force_alphabetical_sort`** (`bool | None`, default: `None` ) – Force all imports to be sorted as a single section
- **`force_sort_within_sections`** (`bool | None`, default: `None` ) – Don't sort straight-style imports (like import sys) before from-style imports (like from itertools import groupby). Instead, sort the imports by module, independent of import style.
- **`honor_case_in_force_sorted_sections`** (`bool | None`, default: `None` ) – Honor --case-sensitive when --force-sort-within-sections is being used. Without this option set, --order-by-type decides module name ordering too.
- **`sort_relative_in_force_sorted_sections`** (`bool | None`, default: `None` ) – When using --force-sort-within-sections, sort relative imports the same way as they are sorted when not using that setting.
- **`force_alphabetical_sort_within_sections`** (`bool | None`, default: `None` ) – Force all imports to be sorted alphabetically within a section
- **`top`** (`str | None`, default: `None` ) – Force specific imports to the top of their appropriate section.
- **`combine_straight_imports`** (`bool | None`, default: `None` ) – Combines all the bare straight imports of the same section in a single line. Won't work with sections which have 'as' imports
- **`no_lines_before`** (`list[str] | None`, default: `None` ) – Sections which should not be split with previous by empty lines
- **`src_path`** (`list[str] | None`, default: `None` ) – Add an explicitly defined source path (modules within src paths have their imports automatically categorized as first_party). Glob expansion (\* and \*\*) is supported for this option.
- **`builtin`** (`str | None`, default: `None` ) – Force isort to recognize a module as part of Python's standard library.
- **`extra_builtin`** (`str | None`, default: `None` ) – Extra modules to be included in the list of ones in Python's standard library.
- **`future`** (`str | None`, default: `None` ) – Force isort to recognize a module as part of Python's internal future compatibility libraries. WARNING: this overrides the behavior of future handling and therefore can result in code that can't execute. If you're looking to add dependencies such as six, a better option is to create another section below --future using custom sections. See: https://github.com/PyCQA/isort#custom- sections-and-ordering and the discussion here: https://github.com/PyCQA/isort/issues/1463.
- **`thirdparty`** (`str | None`, default: `None` ) – Force isort to recognize a module as being part of a third party library.
- **`project`** (`str | None`, default: `None` ) – Force isort to recognize a module as being part of the current python project.
- **`known_local_folder`** (`str | None`, default: `None` ) – Force isort to recognize a module as being a local folder. Generally, this is reserved for relative imports (from . import module).
- **`virtual_env`** (`str | None`, default: `None` ) – Virtual environment to use for determining whether a package is third-party
- **`conda_env`** (`str | None`, default: `None` ) – Conda environment to use for determining whether a package is third-party
- **`python_version`** (`Literal['all', '2', '27', '3', '36', '37', '38', '39', '310', '311', 'auto'] | None`, default: `None` ) – Tells isort to set the known standard library based on the specified Python version. Default is to assume any Python 3 version could be the target, and use a union of all stdlib modules across versions. If auto is specified, the version of the interpreter used to run isort (currently: 311) will be used.

Methods:

- **`__call__`** – Run the command.
- **`add_args`** – Append CLI arguments.

Attributes:

- **`cli_args`** (`list[str]`) – Registered command-line arguments.
- **`cli_command`** (`str`) – The equivalent CLI command.
- **`cli_name`** – The name of the executable on PATH.
- **`py_args`** (`dict[str, Any]`) – Registered Python arguments.

Source code in `src/duty/_internal/tools/_isort.py`

```
def __init__(
    self,
    *files: str,
    settings: str | None = None,
    verbose: bool | None = None,
    only_modified: bool | None = None,
    dedup_headings: bool | None = None,
    quiet: bool | None = None,
    stdout: bool | None = None,
    overwrite_in_place: bool | None = None,
    show_config: bool | None = None,
    show_files: bool | None = None,
    diff: bool | None = None,
    check: bool | None = None,
    ignore_whitespace: bool | None = None,
    config_root: str | None = None,
    resolve_all_configs: bool | None = None,
    profile: str | None = None,
    jobs: int | None = None,
    atomic: bool | None = None,
    interactive: bool | None = None,
    format_error: str | None = None,
    format_success: str | None = None,
    sort_reexports: bool | None = None,
    filter_files: bool | None = None,
    skip: list[str] | None = None,
    extend_skip: list[str] | None = None,
    skip_glob: list[str] | None = None,
    extend_skip_glob: list[str] | None = None,
    skip_gitignore: bool | None = None,
    supported_extension: list[str] | None = None,
    blocked_extension: list[str] | None = None,
    dont_follow_links: bool | None = None,
    filename: str | None = None,
    allow_root: bool | None = None,
    add_import: str | None = None,
    append_only: bool | None = None,
    force_adds: bool | None = None,
    remove_import: str | None = None,
    float_to_top: bool | None = None,
    dont_float_to_top: bool | None = None,
    combine_as: bool | None = None,
    combine_star: bool | None = None,
    balanced: bool | None = None,
    from_first: bool | None = None,
    force_grid_wrap: int | None = None,
    indent: str | None = None,
    lines_before_imports: int | None = None,
    lines_after_imports: int | None = None,
    lines_between_types: int | None = None,
    line_ending: str | None = None,
    length_sort: bool | None = None,
    length_sort_straight: bool | None = None,
    multi_line: Multiline | None = None,
    ensure_newline_before_comments: bool | None = None,
    no_inline_sort: bool | None = None,
    order_by_type: bool | None = None,
    dont_order_by_type: bool | None = None,
    reverse_relative: bool | None = None,
    reverse_sort: bool | None = None,
    sort_order: Literal["natural", "native"] | None = None,
    force_single_line_imports: bool | None = None,
    single_line_exclusions: list[str] | None = None,
    trailing_comma: bool | None = None,
    use_parentheses: bool | None = None,
    line_length: int | None = None,
    wrap_length: int | None = None,
    case_sensitive: bool | None = None,
    remove_redundant_aliases: bool | None = None,
    honor_noqa: bool | None = None,
    treat_comment_as_code: str | None = None,
    treat_all_comment_as_code: bool | None = None,
    formatter: str | None = None,
    color: bool | None = None,
    ext_format: str | None = None,
    star_first: bool | None = None,
    split_on_trailing_comma: bool | None = None,
    section_default: Literal["FUTURE", "STDLIB", "THIRDPARTY", "FIRSTPARTY", "LOCALFOLDER"] | None = None,
    only_sections: bool | None = None,
    no_sections: bool | None = None,
    force_alphabetical_sort: bool | None = None,
    force_sort_within_sections: bool | None = None,
    honor_case_in_force_sorted_sections: bool | None = None,
    sort_relative_in_force_sorted_sections: bool | None = None,
    force_alphabetical_sort_within_sections: bool | None = None,
    top: str | None = None,
    combine_straight_imports: bool | None = None,
    no_lines_before: list[str] | None = None,
    src_path: list[str] | None = None,
    builtin: str | None = None,
    extra_builtin: str | None = None,
    future: str | None = None,
    thirdparty: str | None = None,
    project: str | None = None,
    known_local_folder: str | None = None,
    virtual_env: str | None = None,
    conda_env: str | None = None,
    python_version: Literal["all", "2", "27", "3", "36", "37", "38", "39", "310", "311", "auto"] | None = None,
) -> None:
    """Run `isort`.

    Sort Python import definitions alphabetically within logical sections.
    Run with no arguments to see a quick start guide, otherwise, one or more files/directories/stdin must be provided.
    Use `-` as the first argument to represent stdin. Use --interactive to use the pre 5.0.0 interactive behavior.
    If you've used isort 4 but are new to isort 5, see the upgrading guide:
    https://pycqa.github.io/isort/docs/upgrade_guides/5.0.0.html.

    Parameters:
        *files: One or more Python source files that need their imports sorted.
        settings: Explicitly set the settings path or file instead of auto determining based on file location.
        verbose: Shows verbose output, such as when files are skipped or when a check is successful.
        only_modified: Suppresses verbose output for non-modified files.
        dedup_headings: Tells isort to only show an identical custom import heading comment once, even if there are multiple sections with the comment set.
        quiet: Shows extra quiet output, only errors are outputted.
        stdout: Force resulting output to stdout, instead of in-place.
        overwrite_in_place: Tells isort to overwrite in place using the same file handle. Comes at a performance and memory usage penalty over its standard approach but ensures all file flags and modes stay unchanged.
        show_config: See isort's determined config, as well as sources of config options.
        show_files: See the files isort will be run against with the current config options.
        diff: Prints a diff of all the changes isort would make to a file, instead of changing it in place
        check: Checks the file for unsorted / unformatted imports and prints them to the command line without modifying the file. Returns 0 when nothing would change and returns 1 when the file would be reformatted.
        ignore_whitespace: Tells isort to ignore whitespace differences when --check-only is being used.
        config_root: Explicitly set the config root for resolving all configs. When used with the --resolve-all-configs flag, isort will look at all sub-folders in this config root to resolve config files and sort files based on the closest available config(if any)
        resolve_all_configs: Tells isort to resolve the configs for all sub-directories and sort files in terms of its closest config files.
        profile: Base profile type to use for configuration. Profiles include: black, django, pycharm, google, open_stack, plone, attrs, hug, wemake, appnexus. As well as any shared profiles.
        jobs: Number of files to process in parallel. Negative value means use number of CPUs.
        atomic: Ensures the output doesn't save if the resulting file contains syntax errors.
        interactive: Tells isort to apply changes interactively.
        format_error: Override the format used to print errors.
        format_success: Override the format used to print success.
        sort_reexports: Automatically sort all re-exports (module level __all__ collections)
        filter_files: Tells isort to filter files even when they are explicitly passed in as part of the CLI command.
        skip: Files that isort should skip over. If you want to skip multiple files you should specify twice: --skip file1 --skip file2. Values can be file names, directory names or file paths. To skip all files in a nested path use --skip-glob.
        extend_skip: Extends --skip to add additional files that isort should skip over. If you want to skip multiple files you should specify twice: --skip file1 --skip file2. Values can be file names, directory names or file paths. To skip all files in a nested path use --skip-glob.
        skip_glob: Files that isort should skip over.
        extend_skip_glob: Additional files that isort should skip over (extending --skip-glob).
        skip_gitignore: Treat project as a git repository and ignore files listed in .gitignore. NOTE: This requires git to be installed and accessible from the same shell as isort.
        supported_extension: Specifies what extensions isort can be run against.
        blocked_extension: Specifies what extensions isort can never be run against.
        dont_follow_links: Tells isort not to follow symlinks that are encountered when running recursively.
        filename: Provide the filename associated with a stream.
        allow_root: Tells isort not to treat / specially, allowing it to be run against the root dir.
        add_import: Adds the specified import line to all files, automatically determining correct placement.
        append_only: Only adds the imports specified in --add-import if the file contains existing imports.
        force_adds: Forces import adds even if the original file is empty.
        remove_import: Removes the specified import from all files.
        float_to_top: Causes all non-indented imports to float to the top of the file having its imports sorted (immediately below the top of file comment). This can be an excellent shortcut for collecting imports every once in a while when you place them in the middle of a file to avoid context switching. *NOTE*: It currently doesn't work with cimports and introduces some extra over-head and a performance penalty.
        dont_float_to_top: Forces --float-to-top setting off. See --float-to-top for more information.
        combine_as: Combines as imports on the same line.
        combine_star: Ensures that if a star import is present, nothing else is imported from that namespace.
        balanced: Balances wrapping to produce the most consistent line length possible
        from_first: Switches the typical ordering preference, showing from imports first then straight ones.
        force_grid_wrap: Force number of from imports (defaults to 2 when passed as CLI flag without value) to be grid wrapped regardless of line length. If 0 is passed in (the global default) only line length is considered.
        indent: String to place for indents defaults to " " (4 spaces).
        lines_before_imports: Number of lines to insert before imports.
        lines_after_imports: Number of lines to insert after imports.
        lines_between_types: Number of lines to insert between imports.
        line_ending: Forces line endings to the specified value. If not set, values will be guessed per-file.
        length_sort: Sort imports by their string length.
        length_sort_straight: Sort straight imports by their string length. Similar to `length_sort` but applies only to straight imports and doesn't affect from imports.
        multi_line: Multi line output (0-grid, 1-vertical, 2-hanging, 3-vert-hanging, 4-vert-grid, 5-vert-grid-grouped, 6-deprecated-alias-for-5, 7-noqa, 8-vertical-hanging-indent-bracket, 9-vertical-prefix-from- module-import, 10-hanging-indent-with-parentheses).
        ensure_newline_before_comments: Inserts a blank line before a comment following an import.
        no_inline_sort: Leaves `from` imports with multiple imports 'as-is' (e.g. `from foo import a, c ,b`).
        order_by_type: Order imports by type, which is determined by case, in addition to alphabetically. **NOTE**: type here refers to the implied type from the import name capitalization. isort does not do type introspection for the imports. These "types" are simply: CONSTANT_VARIABLE, CamelCaseClass, variable_or_function. If your project follows PEP8 or a related coding standard and has many imports this is a good default, otherwise you likely will want to turn it off. From the CLI the `--dont-order-by-type` option will turn this off.
        dont_order_by_type: Don't order imports by type, which is determined by case, in addition to alphabetically. **NOTE**: type here refers to the implied type from the import name capitalization. isort does not do type introspection for the imports. These "types" are simply: CONSTANT_VARIABLE, CamelCaseClass, variable_or_function. If your project follows PEP8 or a related coding standard and has many imports this is a good default. You can turn this on from the CLI using `--order-by-type`.
        reverse_relative: Reverse order of relative imports.
        reverse_sort: Reverses the ordering of imports.
        sort_order: Specify sorting function. Can be built in (natural[default] = force numbers to be sequential, native = Python's built-in sorted function) or an installable plugin.
        force_single_line_imports: Forces all from imports to appear on their own line
        single_line_exclusions: One or more modules to exclude from the single line rule.
        trailing_comma: Includes a trailing comma on multi line imports that include parentheses.
        use_parentheses: Use parentheses for line continuation on length limit instead of slashes. **NOTE**: This is separate from wrap modes, and only affects how individual lines that are too long get continued, not sections of multiple imports.
        line_length: The max length of an import line (used for wrapping long imports).
        wrap_length: Specifies how long lines that are wrapped should be, if not set line_length is used. NOTE: wrap_length must be LOWER than or equal to line_length.
        case_sensitive: Tells isort to include casing when sorting module names
        remove_redundant_aliases: Tells isort to remove redundant aliases from imports, such as `import os as os`. This defaults to `False` simply because some projects use these seemingly useless aliases to signify intent and change behaviour.
        honor_noqa: Tells isort to honor noqa comments to enforce skipping those comments.
        treat_comment_as_code: Tells isort to treat the specified single line comment(s) as if they are code.
        treat_all_comment_as_code: Tells isort to treat all single line comments as if they are code.
        formatter: Specifies the name of a formatting plugin to use when producing output.
        color: Tells isort to use color in terminal output.
        ext_format: Tells isort to format the given files according to an extensions formatting rules.
        star_first: Forces star imports above others to avoid overriding directly imported variables.
        split_on_trailing_comma: Split imports list followed by a trailing comma into VERTICAL_HANGING_INDENT mode
        section_default: Sets the default section for import options: ('FUTURE', 'STDLIB', 'THIRDPARTY', 'FIRSTPARTY', 'LOCALFOLDER')
        only_sections: Causes imports to be sorted based on their sections like STDLIB, THIRDPARTY, etc. Within sections, the imports are ordered by their import style and the imports with the same style maintain their relative positions.
        no_sections: Put all imports into the same section bucket
        force_alphabetical_sort: Force all imports to be sorted as a single section
        force_sort_within_sections: Don't sort straight-style imports (like import sys) before from-style imports (like from itertools import groupby). Instead, sort the imports by module, independent of import style.
        honor_case_in_force_sorted_sections: Honor `--case-sensitive` when `--force-sort-within-sections` is being used. Without this option set, `--order-by-type` decides module name ordering too.
        sort_relative_in_force_sorted_sections: When using `--force-sort-within-sections`, sort relative imports the same way as they are sorted when not using that setting.
        force_alphabetical_sort_within_sections: Force all imports to be sorted alphabetically within a section
        top: Force specific imports to the top of their appropriate section.
        combine_straight_imports: Combines all the bare straight imports of the same section in a single line. Won't work with sections which have 'as' imports
        no_lines_before: Sections which should not be split with previous by empty lines
        src_path: Add an explicitly defined source path (modules within src paths have their imports automatically categorized as first_party). Glob expansion (`*` and `**`) is supported for this option.
        builtin: Force isort to recognize a module as part of Python's standard library.
        extra_builtin: Extra modules to be included in the list of ones in Python's standard library.
        future: Force isort to recognize a module as part of Python's internal future compatibility libraries. WARNING: this overrides the behavior of __future__ handling and therefore can result in code that can't execute. If you're looking to add dependencies such as six, a better option is to create another section below --future using custom sections. See: https://github.com/PyCQA/isort#custom- sections-and-ordering and the discussion here: https://github.com/PyCQA/isort/issues/1463.
        thirdparty: Force isort to recognize a module as being part of a third party library.
        project: Force isort to recognize a module as being part of the current python project.
        known_local_folder: Force isort to recognize a module as being a local folder. Generally, this is reserved for relative imports (from . import module).
        virtual_env: Virtual environment to use for determining whether a package is third-party
        conda_env: Conda environment to use for determining whether a package is third-party
        python_version: Tells isort to set the known standard library based on the specified Python version. Default is to assume any Python 3 version could be the target, and use a union of all stdlib modules across versions. If auto is specified, the version of the interpreter used to run isort (currently: 311) will be used.
    """
    cli_args = list(files)

    if verbose:
        cli_args.append("--verbose")

    if only_modified:
        cli_args.append("--only-modified")

    if dedup_headings:
        cli_args.append("--dedup-headings")

    if quiet:
        cli_args.append("--quiet")

    if stdout:
        cli_args.append("--stdout")

    if overwrite_in_place:
        cli_args.append("--overwrite-in-place")

    if show_config:
        cli_args.append("--show-config")

    if show_files:
        cli_args.append("--show-files")

    if diff:
        cli_args.append("--diff")

    if check:
        cli_args.append("--check")

    if ignore_whitespace:
        cli_args.append("--ignore-whitespace")

    if settings:
        cli_args.append("--settings")
        cli_args.append(settings)

    if config_root:
        cli_args.append("--config-root")
        cli_args.append(config_root)

    if resolve_all_configs:
        cli_args.append("--resolve-all-configs")

    if profile:
        cli_args.append("--profile")
        cli_args.append(profile)

    if jobs:
        cli_args.append("--jobs")
        cli_args.append(str(jobs))

    if atomic:
        cli_args.append("--atomic")

    if interactive:
        cli_args.append("--interactive")

    if format_error:
        cli_args.append("--format-error")
        cli_args.append(format_error)

    if format_success:
        cli_args.append("--format-success")
        cli_args.append(format_success)

    if sort_reexports:
        cli_args.append("--sort-reexports")

    if filter_files:
        cli_args.append("--filter-files")

    if skip:
        cli_args.append("--skip")
        cli_args.append(",".join(skip))

    if extend_skip:
        cli_args.append("--extend-skip")
        cli_args.append(",".join(extend_skip))

    if skip_glob:
        cli_args.append("--skip-glob")
        cli_args.append(",".join(skip_glob))

    if extend_skip_glob:
        cli_args.append("--extend-skip-glob")
        cli_args.append(",".join(extend_skip_glob))

    if skip_gitignore:
        cli_args.append("--skip-gitignore")

    if supported_extension:
        cli_args.append("--supported-extension")
        cli_args.append(",".join(supported_extension))

    if blocked_extension:
        cli_args.append("--blocked-extension")
        cli_args.append(",".join(blocked_extension))

    if dont_follow_links:
        cli_args.append("--dont-follow-links")

    if filename:
        cli_args.append("--filename")
        cli_args.append(filename)

    if allow_root:
        cli_args.append("--allow-root")

    if add_import:
        cli_args.append("--add-import")
        cli_args.append(add_import)

    if append_only:
        cli_args.append("--append-only")

    if force_adds:
        cli_args.append("--force-adds")

    if remove_import:
        cli_args.append("--remove-import")
        cli_args.append(remove_import)

    if float_to_top:
        cli_args.append("--float-to-top")

    if dont_float_to_top:
        cli_args.append("--dont-float-to-top")

    if combine_as:
        cli_args.append("--combine-as")

    if combine_star:
        cli_args.append("--combine-star")

    if balanced:
        cli_args.append("--balanced")

    if from_first:
        cli_args.append("--from-first")

    if force_grid_wrap:
        cli_args.append("--force-grid-wrap")
        cli_args.append(str(force_grid_wrap))

    if indent:
        cli_args.append("--indent")
        cli_args.append(indent)

    if lines_before_imports:
        cli_args.append("--lines-before-imports")
        cli_args.append(str(lines_before_imports))

    if lines_after_imports:
        cli_args.append("--lines-after-imports")
        cli_args.append(str(lines_after_imports))

    if lines_between_types:
        cli_args.append("--lines-between-types")
        cli_args.append(str(lines_between_types))

    if line_ending:
        cli_args.append("--line-ending")
        cli_args.append(line_ending)

    if length_sort:
        cli_args.append("--length-sort")

    if length_sort_straight:
        cli_args.append("--length-sort-straight")

    if multi_line:
        cli_args.append("--multi-line")
        cli_args.append(multi_line)

    if ensure_newline_before_comments:
        cli_args.append("--ensure-newline-before-comments")

    if no_inline_sort:
        cli_args.append("--no-inline-sort")

    if order_by_type:
        cli_args.append("--order-by-type")

    if dont_order_by_type:
        cli_args.append("--dont-order-by-type")

    if reverse_relative:
        cli_args.append("--reverse-relative")

    if reverse_sort:
        cli_args.append("--reverse-sort")

    if sort_order:
        cli_args.append("--sort-order")
        cli_args.append(sort_order)

    if force_single_line_imports:
        cli_args.append("--force-single-line-imports")

    if single_line_exclusions:
        cli_args.append("--single-line-exclusions")
        cli_args.append(",".join(single_line_exclusions))

    if trailing_comma:
        cli_args.append("--trailing-comma")

    if use_parentheses:
        cli_args.append("--use-parentheses")

    if line_length:
        cli_args.append("--line-length")
        cli_args.append(str(line_length))

    if wrap_length:
        cli_args.append("--wrap-length")
        cli_args.append(str(wrap_length))

    if case_sensitive:
        cli_args.append("--case-sensitive")

    if remove_redundant_aliases:
        cli_args.append("--remove-redundant-aliases")

    if honor_noqa:
        cli_args.append("--honor-noqa")

    if treat_comment_as_code:
        cli_args.append("--treat-comment-as-code")
        cli_args.append(treat_comment_as_code)

    if treat_all_comment_as_code:
        cli_args.append("--treat-all-comment-as-code")

    if formatter:
        cli_args.append("--formatter")
        cli_args.append(formatter)

    if color:
        cli_args.append("--color")

    if ext_format:
        cli_args.append("--ext-format")
        cli_args.append(ext_format)

    if star_first:
        cli_args.append("--star-first")

    if split_on_trailing_comma:
        cli_args.append("--split-on-trailing-comma")

    if section_default:
        cli_args.append("--section-default")
        cli_args.append(section_default)

    if only_sections:
        cli_args.append("--only-sections")

    if no_sections:
        cli_args.append("--no-sections")

    if force_alphabetical_sort:
        cli_args.append("--force-alphabetical-sort")

    if force_sort_within_sections:
        cli_args.append("--force-sort-within-sections")

    if honor_case_in_force_sorted_sections:
        cli_args.append("--honor-case-in-force-sorted-sections")

    if sort_relative_in_force_sorted_sections:
        cli_args.append("--sort-relative-in-force-sorted-sections")

    if force_alphabetical_sort_within_sections:
        cli_args.append("force-alphabetical-sort-within-sections")

    if top:
        cli_args.append("--top")
        cli_args.append(top)

    if combine_straight_imports:
        cli_args.append("--combine-straight-imports")

    if no_lines_before:
        cli_args.append("--no-lines-before")
        cli_args.append(",".join(no_lines_before))

    if src_path:
        cli_args.append("--src-path")
        cli_args.append(",".join(src_path))

    if builtin:
        cli_args.append("--builtin")
        cli_args.append(builtin)

    if extra_builtin:
        cli_args.append("--extra-builtin")
        cli_args.append(extra_builtin)

    if future:
        cli_args.append("--future")
        cli_args.append(future)

    if thirdparty:
        cli_args.append("--thirdparty")
        cli_args.append(thirdparty)

    if project:
        cli_args.append("--project")
        cli_args.append(project)

    if known_local_folder:
        cli_args.append("--known-local-folder")
        cli_args.append(known_local_folder)

    if virtual_env:
        cli_args.append("--virtual-env")
        cli_args.append(virtual_env)

    if conda_env:
        cli_args.append("--conda-env")
        cli_args.append(conda_env)

    if python_version:
        cli_args.append("--python-version")
        cli_args.append(python_version)

    super().__init__(cli_args)

```

#### cli_args

```
cli_args: list[str] = cli_args or []

```

Registered command-line arguments.

#### cli_command

```
cli_command: str

```

The equivalent CLI command.

#### cli_name

```
cli_name = 'isort'

```

The name of the executable on PATH.

#### py_args

```
py_args: dict[str, Any] = py_args or {}

```

Registered Python arguments.

#### __call__

```
__call__() -> None

```

Run the command.

Source code in `src/duty/_internal/tools/_isort.py`

```
def __call__(self) -> None:
    """Run the command."""
    from isort.main import main as run_isort  # noqa: PLC0415

    run_isort(self.cli_args)

```

#### add_args

```
add_args(*args: str) -> Self

```

Append CLI arguments.

Source code in `src/duty/_internal/tools/_base.py`

```
def add_args(self, *args: str) -> Self:
    """Append CLI arguments."""
    self.cli_args.extend(args)
    return self

```

### mkdocs

```
mkdocs(
    cli_args: list[str] | None = None,
    py_args: dict[str, Any] | None = None,
)

```

Bases: `Tool`

Call [MkDocs](https://github.com/mkdocs/mkdocs).

Parameters:

- **`cli_args`** (`list[str] | None`, default: `None` ) – Initial command-line arguments. Use add_args() to add more.
- **`py_args`** (`dict[str, Any] | None`, default: `None` ) – Python arguments. Your __call__ method will be able to access these arguments as self.py_args.

Methods:

- **`__call__`** – Run the command.
- **`add_args`** – Append CLI arguments.
- **`build`** – Build the MkDocs documentation.
- **`gh_deploy`** – Deploy your documentation to GitHub Pages.
- **`new`** – Create a new MkDocs project.
- **`serve`** – Run the builtin development server.

Attributes:

- **`cli_args`** (`list[str]`) – Registered command-line arguments.
- **`cli_command`** (`str`) – The equivalent CLI command.
- **`cli_name`** – The name of the executable on PATH.
- **`py_args`** (`dict[str, Any]`) – Registered Python arguments.

Source code in `src/duty/_internal/tools/_base.py`

```
def __init__(
    self,
    cli_args: list[str] | None = None,
    py_args: dict[str, Any] | None = None,
) -> None:
    """Initialize the tool.

    Parameters:
        cli_args: Initial command-line arguments. Use `add_args()` to add more.
        py_args: Python arguments. Your `__call__` method will be able to access
            these arguments as `self.py_args`.
    """
    self.cli_args: list[str] = cli_args or []
    """Registered command-line arguments."""
    self.py_args: dict[str, Any] = py_args or {}
    """Registered Python arguments."""

```

#### cli_args

```
cli_args: list[str] = cli_args or []

```

Registered command-line arguments.

#### cli_command

```
cli_command: str

```

The equivalent CLI command.

#### cli_name

```
cli_name = 'mkdocs'

```

The name of the executable on PATH.

#### py_args

```
py_args: dict[str, Any] = py_args or {}

```

Registered Python arguments.

#### __call__

```
__call__() -> int

```

Run the command.

Returns:

- `int` – The exit code of the command.

Source code in `src/duty/_internal/tools/_mkdocs.py`

```
def __call__(self) -> int:
    """Run the command.

    Returns:
        The exit code of the command.
    """
    from mkdocs.__main__ import cli as run_mkdocs  # noqa: PLC0415

    return run_mkdocs(self.cli_args)

```

#### add_args

```
add_args(*args: str) -> Self

```

Append CLI arguments.

Source code in `src/duty/_internal/tools/_base.py`

```
def add_args(self, *args: str) -> Self:
    """Append CLI arguments."""
    self.cli_args.extend(args)
    return self

```

#### build

```
build(
    *,
    config_file: str | None = None,
    clean: bool | None = None,
    strict: bool | None = None,
    theme: str | None = None,
    directory_urls: bool | None = None,
    site_dir: str | None = None,
    quiet: bool = False,
    verbose: bool = False,
) -> mkdocs

```

Build the MkDocs documentation.

Parameters:

- **`config_file`** (`str | None`, default: `None` ) – Provide a specific MkDocs config.
- **`clean`** (`bool | None`, default: `None` ) – Remove old files from the site_dir before building (the default).
- **`strict`** (`bool | None`, default: `None` ) – Enable strict mode. This will cause MkDocs to abort the build on any warnings.
- **`theme`** (`str | None`, default: `None` ) – The theme to use when building your documentation.
- **`directory_urls`** (`bool | None`, default: `None` ) – Use directory URLs when building pages (the default).
- **`site_dir`** (`str | None`, default: `None` ) – The directory to output the result of the documentation build.
- **`quiet`** (`bool`, default: `False` ) – Silence warnings.
- **`verbose`** (`bool`, default: `False` ) – Enable verbose output.

Source code in `src/duty/_internal/tools/_mkdocs.py`

```
@classmethod
def build(
    cls,
    *,
    config_file: str | None = None,
    clean: bool | None = None,
    strict: bool | None = None,
    theme: str | None = None,
    directory_urls: bool | None = None,
    site_dir: str | None = None,
    quiet: bool = False,
    verbose: bool = False,
) -> mkdocs:
    """Build the MkDocs documentation.

    Parameters:
        config_file: Provide a specific MkDocs config.
        clean: Remove old files from the site_dir before building (the default).
        strict: Enable strict mode. This will cause MkDocs to abort the build on any warnings.
        theme: The theme to use when building your documentation.
        directory_urls: Use directory URLs when building pages (the default).
        site_dir: The directory to output the result of the documentation build.
        quiet: Silence warnings.
        verbose: Enable verbose output.
    """
    cli_args = ["build"]

    if clean is True:
        cli_args.append("--clean")
    elif clean is False:
        cli_args.append("--dirty")

    if config_file:
        cli_args.append("--config-file")
        cli_args.append(config_file)

    if strict is True:
        cli_args.append("--strict")

    if theme:
        cli_args.append("--theme")
        cli_args.append(theme)

    if directory_urls is True:
        cli_args.append("--use-directory-urls")
    elif directory_urls is False:
        cli_args.append("--no-directory-urls")

    if site_dir:
        cli_args.append("--site_dir")
        cli_args.append(site_dir)

    if quiet and "-q" not in cli_args:
        cli_args.append("--quiet")

    if verbose and "-v" not in cli_args:
        cli_args.append("--verbose")

    return cls(cli_args)

```

#### gh_deploy

```
gh_deploy(
    *,
    config_file: str | None = None,
    clean: bool | None = None,
    message: str | None = None,
    remote_branch: str | None = None,
    remote_name: str | None = None,
    force: bool | None = None,
    no_history: bool | None = None,
    ignore_version: bool | None = None,
    shell: bool | None = None,
    strict: bool | None = None,
    theme: str | None = None,
    directory_urls: bool | None = None,
    site_dir: str | None = None,
    quiet: bool = False,
    verbose: bool = False,
) -> mkdocs

```

Deploy your documentation to GitHub Pages.

Parameters:

- **`config_file`** (`str | None`, default: `None` ) – Provide a specific MkDocs config.
- **`clean`** (`bool | None`, default: `None` ) – Remove old files from the site_dir before building (the default).
- **`message`** (`str | None`, default: `None` ) – A commit message to use when committing to the GitHub Pages remote branch. Commit {sha} and MkDocs {version} are available as expansions.
- **`remote_branch`** (`str | None`, default: `None` ) – The remote branch to commit to for GitHub Pages. This overrides the value specified in config.
- **`remote_name`** (`str | None`, default: `None` ) – The remote name to commit to for GitHub Pages. This overrides the value specified in config
- **`force`** (`bool | None`, default: `None` ) – Force the push to the repository.
- **`no_history`** (`bool | None`, default: `None` ) – Replace the whole Git history with one new commit.
- **`ignore_version`** (`bool | None`, default: `None` ) – Ignore check that build is not being deployed with an older version of MkDocs.
- **`shell`** (`bool | None`, default: `None` ) – Use the shell when invoking Git.
- **`strict`** (`bool | None`, default: `None` ) – Enable strict mode. This will cause MkDocs to abort the build on any warnings.
- **`theme`** (`str | None`, default: `None` ) – The theme to use when building your documentation.
- **`directory_urls`** (`bool | None`, default: `None` ) – Use directory URLs when building pages (the default).
- **`site_dir`** (`str | None`, default: `None` ) – The directory to output the result of the documentation build.
- **`quiet`** (`bool`, default: `False` ) – Silence warnings.
- **`verbose`** (`bool`, default: `False` ) – Enable verbose output.

Source code in `src/duty/_internal/tools/_mkdocs.py`

```
@classmethod
def gh_deploy(
    cls,
    *,
    config_file: str | None = None,
    clean: bool | None = None,
    message: str | None = None,
    remote_branch: str | None = None,
    remote_name: str | None = None,
    force: bool | None = None,
    no_history: bool | None = None,
    ignore_version: bool | None = None,
    shell: bool | None = None,
    strict: bool | None = None,
    theme: str | None = None,
    directory_urls: bool | None = None,
    site_dir: str | None = None,
    quiet: bool = False,
    verbose: bool = False,
) -> mkdocs:
    """Deploy your documentation to GitHub Pages.

    Parameters:
        config_file: Provide a specific MkDocs config.
        clean: Remove old files from the site_dir before building (the default).
        message: A commit message to use when committing to the GitHub Pages remote branch.
            Commit {sha} and MkDocs {version} are available as expansions.
        remote_branch: The remote branch to commit to for GitHub Pages. This overrides the value specified in config.
        remote_name: The remote name to commit to for GitHub Pages. This overrides the value specified in config
        force: Force the push to the repository.
        no_history: Replace the whole Git history with one new commit.
        ignore_version: Ignore check that build is not being deployed with an older version of MkDocs.
        shell: Use the shell when invoking Git.
        strict: Enable strict mode. This will cause MkDocs to abort the build on any warnings.
        theme: The theme to use when building your documentation.
        directory_urls: Use directory URLs when building pages (the default).
        site_dir: The directory to output the result of the documentation build.
        quiet: Silence warnings.
        verbose: Enable verbose output.
    """
    cli_args = ["gh-deploy"]

    if clean is True:
        cli_args.append("--clean")
    elif clean is False:
        cli_args.append("--dirty")

    if message:
        cli_args.append("--message")
        cli_args.append(message)

    if remote_branch:
        cli_args.append("--remote-branch")
        cli_args.append(remote_branch)

    if remote_name:
        cli_args.append("--remote-name")
        cli_args.append(remote_name)

    if force:
        cli_args.append("--force")

    if no_history:
        cli_args.append("--no-history")

    if ignore_version:
        cli_args.append("--ignore-version")

    if shell:
        cli_args.append("--shell")

    if config_file:
        cli_args.append("--config-file")
        cli_args.append(config_file)

    if strict is True:
        cli_args.append("--strict")

    if theme:
        cli_args.append("--theme")
        cli_args.append(theme)

    if directory_urls is True:
        cli_args.append("--use-directory-urls")
    elif directory_urls is False:
        cli_args.append("--no-directory-urls")

    if site_dir:
        cli_args.append("--site_dir")
        cli_args.append(site_dir)

    if quiet and "-q" not in cli_args:
        cli_args.append("--quiet")

    if verbose and "-v" not in cli_args:
        cli_args.append("--verbose")

    return cls(cli_args)

```

#### new

```
new(
    project_directory: str,
    *,
    quiet: bool = False,
    verbose: bool = False,
) -> mkdocs

```

Create a new MkDocs project.

Parameters:

- **`project_directory`** (`str`) – Where to create the project.
- **`quiet`** (`bool`, default: `False` ) – Silence warnings.
- **`verbose`** (`bool`, default: `False` ) – Enable verbose output.

Source code in `src/duty/_internal/tools/_mkdocs.py`

```
@classmethod
def new(cls, project_directory: str, *, quiet: bool = False, verbose: bool = False) -> mkdocs:
    """Create a new MkDocs project.

    Parameters:
        project_directory: Where to create the project.
        quiet: Silence warnings.
        verbose: Enable verbose output.
    """
    cli_args = ["new", project_directory]

    if quiet and "-q" not in cli_args:
        cli_args.append("--quiet")

    if verbose and "-v" not in cli_args:
        cli_args.append("--verbose")

    return cls(cli_args)

```

#### serve

```
serve(
    *,
    config_file: str | None = None,
    dev_addr: str | None = None,
    livereload: bool | None = None,
    dirtyreload: bool | None = None,
    watch_theme: bool | None = None,
    watch: list[str] | None = None,
    strict: bool | None = None,
    theme: str | None = None,
    directory_urls: bool | None = None,
    quiet: bool = False,
    verbose: bool = False,
) -> mkdocs

```

Run the builtin development server.

Parameters:

- **`config_file`** (`str | None`, default: `None` ) – Provide a specific MkDocs config.
- **`dev_addr`** (`str | None`, default: `None` ) – IP address and port to serve documentation locally (default: localhost:8000).
- **`livereload`** (`bool | None`, default: `None` ) – Enable/disable the live reloading in the development server.
- **`dirtyreload`** (`bool | None`, default: `None` ) – nable the live reloading in the development server, but only re-build files that have changed.
- **`watch_theme`** (`bool | None`, default: `None` ) – Include the theme in list of files to watch for live reloading. Ignored when live reload is not used.
- **`watch`** (`list[str] | None`, default: `None` ) – Directories or files to watch for live reloading.
- **`strict`** (`bool | None`, default: `None` ) – Enable strict mode. This will cause MkDocs to abort the build on any warnings.
- **`theme`** (`str | None`, default: `None` ) – The theme to use when building your documentation.
- **`directory_urls`** (`bool | None`, default: `None` ) – Use directory URLs when building pages (the default).
- **`quiet`** (`bool`, default: `False` ) – Silence warnings.
- **`verbose`** (`bool`, default: `False` ) – Enable verbose output.

Source code in `src/duty/_internal/tools/_mkdocs.py`

```
@classmethod
def serve(
    cls,
    *,
    config_file: str | None = None,
    dev_addr: str | None = None,
    livereload: bool | None = None,
    dirtyreload: bool | None = None,
    watch_theme: bool | None = None,
    watch: list[str] | None = None,
    strict: bool | None = None,
    theme: str | None = None,
    directory_urls: bool | None = None,
    quiet: bool = False,
    verbose: bool = False,
) -> mkdocs:
    """Run the builtin development server.

    Parameters:
        config_file: Provide a specific MkDocs config.
        dev_addr: IP address and port to serve documentation locally (default: localhost:8000).
        livereload: Enable/disable the live reloading in the development server.
        dirtyreload: nable the live reloading in the development server, but only re-build files that have changed.
        watch_theme: Include the theme in list of files to watch for live reloading. Ignored when live reload is not used.
        watch: Directories or files to watch for live reloading.
        strict: Enable strict mode. This will cause MkDocs to abort the build on any warnings.
        theme: The theme to use when building your documentation.
        directory_urls: Use directory URLs when building pages (the default).
        quiet: Silence warnings.
        verbose: Enable verbose output.
    """
    cli_args = ["serve"]

    if dev_addr:
        cli_args.append("--dev-addr")
        cli_args.append(dev_addr)

    if livereload is True:
        cli_args.append("--livereload")
    elif livereload is False:
        cli_args.append("--no-livereload")

    if dirtyreload:
        cli_args.append("--dirtyreload")

    if watch_theme:
        cli_args.append("--watch-theme")

    if watch:
        for path in watch:
            cli_args.append("--watch")
            cli_args.append(path)

    if config_file:
        cli_args.append("--config-file")
        cli_args.append(config_file)

    if strict is True:
        cli_args.append("--strict")

    if theme:
        cli_args.append("--theme")
        cli_args.append(theme)

    if directory_urls is True:
        cli_args.append("--use-directory-urls")
    elif directory_urls is False:
        cli_args.append("--no-directory-urls")

    if quiet and "-q" not in cli_args:
        cli_args.append("--quiet")

    if verbose and "-v" not in cli_args:
        cli_args.append("--verbose")

    return cls(cli_args)

```

### mypy

```
mypy(
    *paths: str,
    config_file: str | None = None,
    enable_incomplete_feature: bool | None = None,
    verbose: bool | None = None,
    warn_unused_configs: bool | None = None,
    no_namespace_packages: bool | None = None,
    ignore_missing_imports: bool | None = None,
    follow_imports: Literal[
        "normal", "silent", "skip", "error"
    ]
    | None = None,
    python_executable: str | None = None,
    no_site_packages: bool | None = None,
    no_silence_site_packages: bool | None = None,
    python_version: str | None = None,
    py2: bool | None = None,
    platform: str | None = None,
    always_true: list[str] | None = None,
    always_false: list[str] | None = None,
    disallow_any_unimported: bool | None = None,
    disallow_any_expr: bool | None = None,
    disallow_any_decorated: bool | None = None,
    disallow_any_explicit: bool | None = None,
    disallow_any_generics: bool | None = None,
    disallow_subclassing_any: bool | None = None,
    disallow_untyped_calls: bool | None = None,
    disallow_untyped_defs: bool | None = None,
    disallow_incomplete_defs: bool | None = None,
    check_untyped_defs: bool | None = None,
    disallow_untyped_decorators: bool | None = None,
    implicit_optional: bool | None = None,
    no_strict_optional: bool | None = None,
    warn_redundant_casts: bool | None = None,
    warn_unused_ignores: bool | None = None,
    no_warn_no_return: bool | None = None,
    warn_return_any: bool | None = None,
    warn_unreachable: bool | None = None,
    allow_untyped_globals: bool | None = None,
    allow_redefinition: bool | None = None,
    no_implicit_reexport: bool | None = None,
    strict_equality: bool | None = None,
    strict_concatenate: bool | None = None,
    strict: bool | None = None,
    disable_error_code: str | None = None,
    enable_error_code: str | None = None,
    show_error_context: bool | None = None,
    show_column_numbers: bool | None = None,
    show_error_end: bool | None = None,
    hide_error_codes: bool | None = None,
    pretty: bool | None = None,
    no_color_output: bool | None = None,
    no_error_summary: bool | None = None,
    show_absolute_path: bool | None = None,
    no_incremental: bool | None = None,
    cache_dir: str | None = None,
    sqlite_cache: bool | None = None,
    cache_fine_grained: bool | None = None,
    skip_version_check: bool | None = None,
    skip_cache_mtime_checks: bool | None = None,
    pdb: bool | None = None,
    show_traceback: bool | None = None,
    raise_exceptions: bool | None = None,
    custom_typing_module: str | None = None,
    disable_recursive_aliases: bool | None = None,
    custom_typeshed_dir: str | None = None,
    warn_incomplete_stub: bool | None = None,
    shadow_file: tuple[str, str] | None = None,
    any_exprs_report: str | None = None,
    cobertura_xml_report: str | None = None,
    html_report: str | None = None,
    linecount_report: str | None = None,
    linecoverage_report: str | None = None,
    lineprecision_report: str | None = None,
    txt_report: str | None = None,
    xml_report: str | None = None,
    xslt_html_report: str | None = None,
    xslt_txt_report: str | None = None,
    junit_xml: str | None = None,
    find_occurrences: str | None = None,
    scripts_are_modules: bool | None = None,
    install_types: bool | None = None,
    non_interactive: bool | None = None,
    explicit_package_bases: bool | None = None,
    exclude: str | None = None,
    module: str | None = None,
    package: str | None = None,
    command: str | None = None,
)

```

Bases: `Tool`

Call [Mypy](https://github.com/python/mypy).

Parameters:

- **`*paths`** (`str`, default: `()` ) – Path to scan.
- **`config_file`** (`str | None`, default: `None` ) – Configuration file, must have a [mypy] section (defaults to mypy.ini, .mypy.ini,
- **`enable_incomplete_feature`** (`bool | None`, default: `None` ) – Enable support of incomplete/experimental features for early preview.
- **`verbose`** (`bool | None`, default: `None` ) – More verbose messages. pyproject.toml, setup.cfg, /home/pawamoy/.config/mypy/config, ~/.config/mypy/config, ~/.mypy.ini).
- **`warn_unused_configs`** (`bool | None`, default: `None` ) – Warn about unused '[mypy-]' or '\[[tool.mypy.overrides]\]' config sections (inverse: --no-warn-unused-configs).
- **`no_namespace_packages`** (`bool | None`, default: `None` ) – Support namespace packages (PEP 420, init.py-less) (inverse: --namespace-packages).
- **`ignore_missing_imports`** (`bool | None`, default: `None` ) – Silently ignore imports of missing modules.
- **`follow_imports`** (`Literal['normal', 'silent', 'skip', 'error'] | None`, default: `None` ) – How to treat imports (default normal).
- **`python_executable`** (`str | None`, default: `None` ) – Python executable used for finding PEP 561 compliant installed packages and stubs.
- **`no_site_packages`** (`bool | None`, default: `None` ) – Do not search for installed PEP 561 compliant packages.
- **`no_silence_site_packages`** (`bool | None`, default: `None` ) – Do not silence errors in PEP 561 compliant installed packages.
- **`python_version`** (`str | None`, default: `None` ) – Type check code assuming it will be running on Python x.y.
- **`py2`** (`bool | None`, default: `None` ) – Use Python 2 mode (same as --python-version 2.7).
- **`platform`** (`str | None`, default: `None` ) – Type check special-cased code for the given OS platform (defaults to sys.platform).
- **`always_true`** (`list[str] | None`, default: `None` ) – Additional variable to be considered True (may be repeated).
- **`always_false`** (`list[str] | None`, default: `None` ) – Additional variable to be considered False (may be repeated).
- **`disallow_any_unimported`** (`bool | None`, default: `None` ) – Disallow Any types resulting from unfollowed imports.
- **`disallow_any_expr`** (`bool | None`, default: `None` ) – Disallow all expressions that have type Any.
- **`disallow_any_decorated`** (`bool | None`, default: `None` ) – Disallow functions that have Any in their signature after decorator transformation.
- **`disallow_any_explicit`** (`bool | None`, default: `None` ) – Disallow explicit Any in type positions.
- **`disallow_any_generics`** (`bool | None`, default: `None` ) – Disallow usage of generic types that do not specify explicit type parameters (inverse: --allow-any-generics).
- **`disallow_subclassing_any`** (`bool | None`, default: `None` ) – Disallow subclassing values of type 'Any' when defining classes (inverse: --allow-subclassing-any).
- **`disallow_untyped_calls`** (`bool | None`, default: `None` ) – Disallow calling functions without type annotations from functions with type annotations (inverse: --allow-untyped-calls).
- **`disallow_untyped_defs`** (`bool | None`, default: `None` ) – Disallow defining functions without type annotations or with incomplete type annotations (inverse: --allow-untyped-defs).
- **`disallow_incomplete_defs`** (`bool | None`, default: `None` ) – Disallow defining functions with incomplete type annotations (inverse: --allow-incomplete-defs).
- **`check_untyped_defs`** (`bool | None`, default: `None` ) – Type check the interior of functions without type annotations (inverse: --no-check-untyped-defs).
- **`disallow_untyped_decorators`** (`bool | None`, default: `None` ) – Disallow decorating typed functions with untyped decorators (inverse: --allow-untyped-decorators).
- **`implicit_optional`** (`bool | None`, default: `None` ) – Assume arguments with default values of None are Optional(inverse: --no-implicit-optional).
- **`no_strict_optional`** (`bool | None`, default: `None` ) – Disable strict Optional checks (inverse: --strict-optional).
- **`warn_redundant_casts`** (`bool | None`, default: `None` ) – Warn about casting an expression to its inferred type (inverse: --no-warn-redundant-casts).
- **`warn_unused_ignores`** (`bool | None`, default: `None` ) – Warn about unneeded '# type: ignore' comments (inverse: --no-warn-unused-ignores).
- **`no_warn_no_return`** (`bool | None`, default: `None` ) – Do not warn about functions that end without returning (inverse: --warn-no-return).
- **`warn_return_any`** (`bool | None`, default: `None` ) – Warn about returning values of type Any from non-Any typed functions (inverse: --no-warn-return-any).
- **`warn_unreachable`** (`bool | None`, default: `None` ) – Warn about statements or expressions inferred to be unreachable (inverse: --no-warn-unreachable).
- **`allow_untyped_globals`** (`bool | None`, default: `None` ) – Suppress toplevel errors caused by missing annotations (inverse: --disallow-untyped-globals).
- **`allow_redefinition`** (`bool | None`, default: `None` ) – Allow unconditional variable redefinition with a new type (inverse: --disallow-redefinition).
- **`no_implicit_reexport`** (`bool | None`, default: `None` ) – Treat imports as private unless aliased (inverse: --implicit-reexport).
- **`strict_equality`** (`bool | None`, default: `None` ) – Prohibit equality, identity, and container checks for non-overlapping types (inverse: --no-strict-equality).
- **`strict_concatenate`** (`bool | None`, default: `None` ) – Make arguments prepended via Concatenate be truly positional-only (inverse: --no-strict-concatenate).
- **`strict`** (`bool | None`, default: `None` ) – Strict mode; enables the following flags: --warn-unused-configs, --disallow-any-generics, --disallow-subclassing-any, --disallow-untyped-calls, --disallow-untyped-defs, --disallow-incomplete-defs, --check-untyped-defs, --disallow-untyped-decorators, --warn-redundant-casts, --warn-unused-ignores, --warn-return-any, --no-implicit-reexport, --strict-equality, --strict-concatenate.
- **`disable_error_code`** (`str | None`, default: `None` ) – Disable a specific error code.
- **`enable_error_code`** (`str | None`, default: `None` ) – Enable a specific error code.
- **`show_error_context`** (`bool | None`, default: `None` ) – Precede errors with "note:" messages explaining context (inverse: --hide-error-context).
- **`show_column_numbers`** (`bool | None`, default: `None` ) – Show column numbers in error messages (inverse: --hide-column-numbers).
- **`show_error_end`** (`bool | None`, default: `None` ) – Show end line/end column numbers in error messages. This implies --show-column-numbers (inverse: --hide-error-end).
- **`hide_error_codes`** (`bool | None`, default: `None` ) – Hide error codes in error messages (inverse: --show-error-codes).
- **`pretty`** (`bool | None`, default: `None` ) – Use visually nicer output in error messages: Use soft word wrap, show source code snippets, and show error location markers (inverse: --no-pretty).
- **`no_color_output`** (`bool | None`, default: `None` ) – Do not colorize error messages (inverse: --color-output).
- **`no_error_summary`** (`bool | None`, default: `None` ) – Do not show error stats summary (inverse: --error-summary).
- **`show_absolute_path`** (`bool | None`, default: `None` ) – Show absolute paths to files (inverse: --hide-absolute-path).
- **`no_incremental`** (`bool | None`, default: `None` ) – Disable module cache (inverse: --incremental).
- **`cache_dir`** (`str | None`, default: `None` ) – Store module cache info in the given folder in incremental mode (defaults to '.mypy_cache').
- **`sqlite_cache`** (`bool | None`, default: `None` ) – Use a sqlite database to store the cache (inverse: --no-sqlite-cache).
- **`cache_fine_grained`** (`bool | None`, default: `None` ) – Include fine-grained dependency information in the cache for the mypy daemon.
- **`skip_version_check`** (`bool | None`, default: `None` ) – Allow using cache written by older mypy version.
- **`skip_cache_mtime_checks`** (`bool | None`, default: `None` ) – Skip cache internal consistency checks based on mtime.
- **`pdb`** (`bool | None`, default: `None` ) – Invoke pdb on fatal error.
- **`show_traceback`** (`bool | None`, default: `None` ) – Show traceback on fatal error.
- **`raise_exceptions`** (`bool | None`, default: `None` ) – Raise exception on fatal error.
- **`custom_typing_module`** (`str | None`, default: `None` ) – Use a custom typing module.
- **`disable_recursive_aliases`** (`bool | None`, default: `None` ) – Disable experimental support for recursive type aliases.
- **`custom_typeshed_dir`** (`str | None`, default: `None` ) – Use the custom typeshed in DIR.
- **`warn_incomplete_stub`** (`bool | None`, default: `None` ) – Warn if missing type annotation in typeshed, only relevant with --disallow-untyped-defs or --disallow-incomplete-defs enabled (inverse: --no-warn-incomplete-stub).
- **`shadow_file`** (`tuple[str, str] | None`, default: `None` ) – When encountering SOURCE_FILE, read and type check the contents of SHADOW_FILE instead..
- **`any_exprs_report`** (`str | None`, default: `None` ) – Report any expression.
- **`cobertura_xml_report`** (`str | None`, default: `None` ) – Report Cobertura.
- **`html_report`** (`str | None`, default: `None` ) – Report HTML.
- **`linecount_report`** (`str | None`, default: `None` ) – Report line count.
- **`linecoverage_report`** (`str | None`, default: `None` ) – Report line coverage.
- **`lineprecision_report`** (`str | None`, default: `None` ) – Report line precision.
- **`txt_report`** (`str | None`, default: `None` ) – Report text.
- **`xml_report`** (`str | None`, default: `None` ) – Report XML.
- **`xslt_html_report`** (`str | None`, default: `None` ) – Report XLST HTML.
- **`xslt_txt_report`** (`str | None`, default: `None` ) – Report XLST text.
- **`junit_xml`** (`str | None`, default: `None` ) – Write junit.xml to the given file.
- **`find_occurrences`** (`str | None`, default: `None` ) – Print out all usages of a class member (experimental).
- **`scripts_are_modules`** (`bool | None`, default: `None` ) – Script x becomes module x instead of main.
- **`install_types`** (`bool | None`, default: `None` ) – Install detected missing library stub packages using pip (inverse: --no-install-types).
- **`non_interactive`** (`bool | None`, default: `None` ) – Install stubs without asking for confirmation and hide errors, with --install-types (inverse: --interactive).
- **`explicit_package_bases`** (`bool | None`, default: `None` ) – Use current directory and MYPYPATH to determine module names of files passed (inverse: --no-explicit-package-bases).
- **`exclude`** (`str | None`, default: `None` ) – Regular expression to match file names, directory names or paths which mypy should ignore while recursively discovering files to check, e.g. --exclude '/setup.py$'. May be specified more than once, eg. --exclude a --exclude b.
- **`module`** (`str | None`, default: `None` ) – Type-check module; can repeat for more modules.
- **`package`** (`str | None`, default: `None` ) – Type-check package recursively; can be repeated.
- **`command`** (`str | None`, default: `None` ) – Type-check program passed in as string.

Methods:

- **`__call__`** – Run the command.
- **`add_args`** – Append CLI arguments.

Attributes:

- **`cli_args`** (`list[str]`) – Registered command-line arguments.
- **`cli_command`** (`str`) – The equivalent CLI command.
- **`cli_name`** – The name of the executable on PATH.
- **`py_args`** (`dict[str, Any]`) – Registered Python arguments.

Source code in `src/duty/_internal/tools/_mypy.py`

```
def __init__(
    self,
    *paths: str,
    config_file: str | None = None,
    enable_incomplete_feature: bool | None = None,
    verbose: bool | None = None,
    warn_unused_configs: bool | None = None,
    no_namespace_packages: bool | None = None,
    ignore_missing_imports: bool | None = None,
    follow_imports: Literal["normal", "silent", "skip", "error"] | None = None,
    python_executable: str | None = None,
    no_site_packages: bool | None = None,
    no_silence_site_packages: bool | None = None,
    python_version: str | None = None,
    py2: bool | None = None,
    platform: str | None = None,
    always_true: list[str] | None = None,
    always_false: list[str] | None = None,
    disallow_any_unimported: bool | None = None,
    disallow_any_expr: bool | None = None,
    disallow_any_decorated: bool | None = None,
    disallow_any_explicit: bool | None = None,
    disallow_any_generics: bool | None = None,
    disallow_subclassing_any: bool | None = None,
    disallow_untyped_calls: bool | None = None,
    disallow_untyped_defs: bool | None = None,
    disallow_incomplete_defs: bool | None = None,
    check_untyped_defs: bool | None = None,
    disallow_untyped_decorators: bool | None = None,
    implicit_optional: bool | None = None,
    no_strict_optional: bool | None = None,
    warn_redundant_casts: bool | None = None,
    warn_unused_ignores: bool | None = None,
    no_warn_no_return: bool | None = None,
    warn_return_any: bool | None = None,
    warn_unreachable: bool | None = None,
    allow_untyped_globals: bool | None = None,
    allow_redefinition: bool | None = None,
    no_implicit_reexport: bool | None = None,
    strict_equality: bool | None = None,
    strict_concatenate: bool | None = None,
    strict: bool | None = None,
    disable_error_code: str | None = None,
    enable_error_code: str | None = None,
    show_error_context: bool | None = None,
    show_column_numbers: bool | None = None,
    show_error_end: bool | None = None,
    hide_error_codes: bool | None = None,
    pretty: bool | None = None,
    no_color_output: bool | None = None,
    no_error_summary: bool | None = None,
    show_absolute_path: bool | None = None,
    no_incremental: bool | None = None,
    cache_dir: str | None = None,
    sqlite_cache: bool | None = None,
    cache_fine_grained: bool | None = None,
    skip_version_check: bool | None = None,
    skip_cache_mtime_checks: bool | None = None,
    pdb: bool | None = None,
    show_traceback: bool | None = None,
    raise_exceptions: bool | None = None,
    custom_typing_module: str | None = None,
    disable_recursive_aliases: bool | None = None,
    custom_typeshed_dir: str | None = None,
    warn_incomplete_stub: bool | None = None,
    shadow_file: tuple[str, str] | None = None,
    any_exprs_report: str | None = None,
    cobertura_xml_report: str | None = None,
    html_report: str | None = None,
    linecount_report: str | None = None,
    linecoverage_report: str | None = None,
    lineprecision_report: str | None = None,
    txt_report: str | None = None,
    xml_report: str | None = None,
    xslt_html_report: str | None = None,
    xslt_txt_report: str | None = None,
    junit_xml: str | None = None,
    find_occurrences: str | None = None,
    scripts_are_modules: bool | None = None,
    install_types: bool | None = None,
    non_interactive: bool | None = None,
    explicit_package_bases: bool | None = None,
    exclude: str | None = None,
    module: str | None = None,
    package: str | None = None,
    command: str | None = None,
) -> None:
    """Run mypy.

    Parameters:
        *paths: Path to scan.
        config_file: Configuration file, must have a [mypy] section (defaults to mypy.ini, .mypy.ini,
        enable_incomplete_feature: Enable support of incomplete/experimental features for early preview.
        verbose: More verbose messages.
            pyproject.toml, setup.cfg, /home/pawamoy/.config/mypy/config, ~/.config/mypy/config, ~/.mypy.ini).
        warn_unused_configs: Warn about unused '[mypy-<pattern>]' or '[[tool.mypy.overrides]]' config sections
            (inverse: --no-warn-unused-configs).
        no_namespace_packages: Support namespace packages (PEP 420, __init__.py-less) (inverse: --namespace-packages).
        ignore_missing_imports: Silently ignore imports of missing modules.
        follow_imports: How to treat imports (default normal).
        python_executable: Python executable used for finding PEP 561 compliant installed packages and stubs.
        no_site_packages: Do not search for installed PEP 561 compliant packages.
        no_silence_site_packages: Do not silence errors in PEP 561 compliant installed packages.
        python_version: Type check code assuming it will be running on Python x.y.
        py2: Use Python 2 mode (same as --python-version 2.7).
        platform: Type check special-cased code for the given OS platform (defaults to sys.platform).
        always_true: Additional variable to be considered True (may be repeated).
        always_false: Additional variable to be considered False (may be repeated).
        disallow_any_unimported: Disallow Any types resulting from unfollowed imports.
        disallow_any_expr: Disallow all expressions that have type Any.
        disallow_any_decorated: Disallow functions that have Any in their signature after decorator transformation.
        disallow_any_explicit: Disallow explicit Any in type positions.
        disallow_any_generics: Disallow usage of generic types that do not specify explicit type parameters
            (inverse: --allow-any-generics).
        disallow_subclassing_any: Disallow subclassing values of type 'Any' when defining classes
            (inverse: --allow-subclassing-any).
        disallow_untyped_calls: Disallow calling functions without type annotations from functions with type annotations
            (inverse: --allow-untyped-calls).
        disallow_untyped_defs: Disallow defining functions without type annotations or with incomplete type annotations
            (inverse: --allow-untyped-defs).
        disallow_incomplete_defs: Disallow defining functions with incomplete type annotations
            (inverse: --allow-incomplete-defs).
        check_untyped_defs: Type check the interior of functions without type annotations
            (inverse: --no-check-untyped-defs).
        disallow_untyped_decorators: Disallow decorating typed functions with untyped decorators
            (inverse: --allow-untyped-decorators).
        implicit_optional: Assume arguments with default values of None are Optional(inverse: --no-implicit-optional).
        no_strict_optional: Disable strict Optional checks (inverse: --strict-optional).
        warn_redundant_casts: Warn about casting an expression to its inferred type (inverse: --no-warn-redundant-casts).
        warn_unused_ignores: Warn about unneeded '# type: ignore' comments (inverse: --no-warn-unused-ignores).
        no_warn_no_return: Do not warn about functions that end without returning (inverse: --warn-no-return).
        warn_return_any: Warn about returning values of type Any from non-Any typed functions (inverse: --no-warn-return-any).
        warn_unreachable: Warn about statements or expressions inferred to be unreachable (inverse: --no-warn-unreachable).
        allow_untyped_globals: Suppress toplevel errors caused by missing annotations (inverse: --disallow-untyped-globals).
        allow_redefinition: Allow unconditional variable redefinition with a new type (inverse: --disallow-redefinition).
        no_implicit_reexport: Treat imports as private unless aliased (inverse: --implicit-reexport).
        strict_equality: Prohibit equality, identity, and container checks for non-overlapping types
            (inverse: --no-strict-equality).
        strict_concatenate: Make arguments prepended via Concatenate be truly positional-only (inverse: --no-strict-concatenate).
        strict: Strict mode; enables the following flags: --warn-unused-configs, --disallow-any-generics,
            --disallow-subclassing-any, --disallow-untyped-calls, --disallow-untyped-defs, --disallow-incomplete-defs,
            --check-untyped-defs, --disallow-untyped-decorators, --warn-redundant-casts, --warn-unused-ignores,
            --warn-return-any, --no-implicit-reexport, --strict-equality, --strict-concatenate.
        disable_error_code: Disable a specific error code.
        enable_error_code: Enable a specific error code.
        show_error_context: Precede errors with "note:" messages explaining context (inverse: --hide-error-context).
        show_column_numbers: Show column numbers in error messages (inverse: --hide-column-numbers).
        show_error_end: Show end line/end column numbers in error messages. This implies --show-column-numbers
            (inverse: --hide-error-end).
        hide_error_codes: Hide error codes in error messages (inverse: --show-error-codes).
        pretty: Use visually nicer output in error messages: Use soft word wrap, show source code snippets,
            and show error location markers (inverse: --no-pretty).
        no_color_output: Do not colorize error messages (inverse: --color-output).
        no_error_summary: Do not show error stats summary (inverse: --error-summary).
        show_absolute_path: Show absolute paths to files (inverse: --hide-absolute-path).
        no_incremental: Disable module cache (inverse: --incremental).
        cache_dir: Store module cache info in the given folder in incremental mode (defaults to '.mypy_cache').
        sqlite_cache: Use a sqlite database to store the cache (inverse: --no-sqlite-cache).
        cache_fine_grained: Include fine-grained dependency information in the cache for the mypy daemon.
        skip_version_check: Allow using cache written by older mypy version.
        skip_cache_mtime_checks: Skip cache internal consistency checks based on mtime.
        pdb: Invoke pdb on fatal error.
        show_traceback: Show traceback on fatal error.
        raise_exceptions: Raise exception on fatal error.
        custom_typing_module: Use a custom typing module.
        disable_recursive_aliases: Disable experimental support for recursive type aliases.
        custom_typeshed_dir: Use the custom typeshed in DIR.
        warn_incomplete_stub: Warn if missing type annotation in typeshed, only relevant with --disallow-untyped-defs
            or --disallow-incomplete-defs enabled (inverse: --no-warn-incomplete-stub).
        shadow_file: When encountering SOURCE_FILE, read and type check the contents of SHADOW_FILE instead..
        any_exprs_report: Report any expression.
        cobertura_xml_report: Report Cobertura.
        html_report: Report HTML.
        linecount_report: Report line count.
        linecoverage_report: Report line coverage.
        lineprecision_report: Report line precision.
        txt_report: Report text.
        xml_report: Report XML.
        xslt_html_report: Report XLST HTML.
        xslt_txt_report: Report XLST text.
        junit_xml: Write junit.xml to the given file.
        find_occurrences: Print out all usages of a class member (experimental).
        scripts_are_modules: Script x becomes module x instead of __main__.
        install_types: Install detected missing library stub packages using pip (inverse: --no-install-types).
        non_interactive: Install stubs without asking for confirmation and hide errors, with --install-types
            (inverse: --interactive).
        explicit_package_bases: Use current directory and MYPYPATH to determine module names of files passed
            (inverse: --no-explicit-package-bases).
        exclude: Regular expression to match file names, directory names or paths which mypy should ignore while
            recursively discovering files to check, e.g. --exclude '/setup\\.py$'.
            May be specified more than once, eg. --exclude a --exclude b.
        module: Type-check module; can repeat for more modules.
        package: Type-check package recursively; can be repeated.
        command: Type-check program passed in as string.
    """  # noqa: D301
    cli_args = list(paths)

    if enable_incomplete_feature:
        cli_args.append("--enable-incomplete-feature")

    if verbose:
        cli_args.append("--verbose")

    if config_file:
        cli_args.append("--config-file")
        cli_args.append(config_file)

    if warn_unused_configs:
        cli_args.append("--warn-unused-configs")

    if no_namespace_packages:
        cli_args.append("--no-namespace-packages")

    if ignore_missing_imports:
        cli_args.append("--ignore-missing-imports")

    if follow_imports:
        cli_args.append("--follow-imports")
        cli_args.append(follow_imports)

    if python_executable:
        cli_args.append("--python-executable")
        cli_args.append(python_executable)

    if no_site_packages:
        cli_args.append("--no-site-packages")

    if no_silence_site_packages:
        cli_args.append("--no-silence-site-packages")

    if python_version:
        cli_args.append("--python-version")
        cli_args.append(python_version)

    if py2:
        cli_args.append("--py2")

    if platform:
        cli_args.append("--platform")
        cli_args.append(platform)

    if always_true:
        for posarg in always_true:
            cli_args.append("--always-true")
            cli_args.append(posarg)

    if always_false:
        for posarg in always_false:
            cli_args.append("--always-false")
            cli_args.append(posarg)

    if disallow_any_unimported:
        cli_args.append("--disallow-any-unimported")

    if disallow_any_expr:
        cli_args.append("--disallow-any-expr")

    if disallow_any_decorated:
        cli_args.append("--disallow-any-decorated")

    if disallow_any_explicit:
        cli_args.append("--disallow-any-explicit")

    if disallow_any_generics:
        cli_args.append("--disallow-any-generics")

    if disallow_subclassing_any:
        cli_args.append("--disallow-subclassing-any")

    if disallow_untyped_calls:
        cli_args.append("--disallow-untyped-calls")

    if disallow_untyped_defs:
        cli_args.append("--disallow-untyped-defs")

    if disallow_incomplete_defs:
        cli_args.append("--disallow-incomplete-defs")

    if check_untyped_defs:
        cli_args.append("--check-untyped-defs")

    if disallow_untyped_decorators:
        cli_args.append("--disallow-untyped-decorators")

    if implicit_optional:
        cli_args.append("--implicit-optional")

    if no_strict_optional:
        cli_args.append("--no-strict-optional")

    if warn_redundant_casts:
        cli_args.append("--warn-redundant-casts")

    if warn_unused_ignores:
        cli_args.append("--warn-unused-ignores")

    if no_warn_no_return:
        cli_args.append("--no-warn-no-return")

    if warn_return_any:
        cli_args.append("--warn-return-any")

    if warn_unreachable:
        cli_args.append("--warn-unreachable")

    if allow_untyped_globals:
        cli_args.append("--allow-untyped-globals")

    if allow_redefinition:
        cli_args.append("--allow-redefinition")

    if no_implicit_reexport:
        cli_args.append("--no-implicit-reexport")

    if strict_equality:
        cli_args.append("--strict-equality")

    if strict_concatenate:
        cli_args.append("--strict-concatenate")

    if strict:
        cli_args.append("--strict")

    if disable_error_code:
        cli_args.append("--disable-error-code")
        cli_args.append(disable_error_code)

    if enable_error_code:
        cli_args.append("--enable-error-code")
        cli_args.append(enable_error_code)

    if show_error_context:
        cli_args.append("--show-error-context")

    if show_column_numbers:
        cli_args.append("--show-column-numbers")

    if show_error_end:
        cli_args.append("--show-error-end")

    if hide_error_codes:
        cli_args.append("--hide-error-codes")

    if pretty:
        cli_args.append("--pretty")

    if no_color_output:
        cli_args.append("--no-color-output")

    if no_error_summary:
        cli_args.append("--no-error-summary")

    if show_absolute_path:
        cli_args.append("--show-absolute-path")

    if no_incremental:
        cli_args.append("--no-incremental")

    if cache_dir:
        cli_args.append("--cache-dir")
        cli_args.append(cache_dir)

    if sqlite_cache:
        cli_args.append("--sqlite-cache")

    if cache_fine_grained:
        cli_args.append("--cache-fine-grained")

    if skip_version_check:
        cli_args.append("--skip-version-check")

    if skip_cache_mtime_checks:
        cli_args.append("--skip-cache-mtime-checks")

    if pdb:
        cli_args.append("--pdb")

    if show_traceback:
        cli_args.append("--show-traceback")

    if raise_exceptions:
        cli_args.append("--raise-exceptions")

    if custom_typing_module:
        cli_args.append("--custom-typing-module")
        cli_args.append(custom_typing_module)

    if disable_recursive_aliases:
        cli_args.append("--disable-recursive-aliases")

    if custom_typeshed_dir:
        cli_args.append("--custom-typeshed-dir")
        cli_args.append(custom_typeshed_dir)

    if warn_incomplete_stub:
        cli_args.append("--warn-incomplete-stub")

    if shadow_file:
        cli_args.append("--shadow-file")
        cli_args.extend(shadow_file)

    if any_exprs_report:
        cli_args.append("--any-exprs-report")
        cli_args.append(any_exprs_report)

    if cobertura_xml_report:
        cli_args.append("--cobertura-xml-report")
        cli_args.append(cobertura_xml_report)

    if html_report:
        cli_args.append("--html-report")
        cli_args.append(html_report)

    if linecount_report:
        cli_args.append("--linecount-report")
        cli_args.append(linecount_report)

    if linecoverage_report:
        cli_args.append("--linecoverage-report")
        cli_args.append(linecoverage_report)

    if lineprecision_report:
        cli_args.append("--lineprecision-report")
        cli_args.append(lineprecision_report)

    if txt_report:
        cli_args.append("--txt-report")
        cli_args.append(txt_report)

    if xml_report:
        cli_args.append("--xml-report")
        cli_args.append(xml_report)

    if xslt_html_report:
        cli_args.append("--xslt-html-report")
        cli_args.append(xslt_html_report)

    if xslt_txt_report:
        cli_args.append("--xslt-txt-report")
        cli_args.append(xslt_txt_report)

    if junit_xml:
        cli_args.append("--junit-xml")
        cli_args.append(junit_xml)

    if find_occurrences:
        cli_args.append("--find-occurrences")
        cli_args.append(find_occurrences)

    if scripts_are_modules:
        cli_args.append("--scripts-are-modules")

    if install_types:
        cli_args.append("--install-types")

    if non_interactive:
        cli_args.append("--non-interactive")

    if explicit_package_bases:
        cli_args.append("--explicit-package-bases")

    if exclude:
        cli_args.append("--exclude")
        cli_args.append(exclude)

    if module:
        cli_args.append("--module")
        cli_args.append(module)

    if package:
        cli_args.append("--package")
        cli_args.append(package)

    if command:
        cli_args.append("--command")
        cli_args.append(command)

    super().__init__(cli_args)

```

#### cli_args

```
cli_args: list[str] = cli_args or []

```

Registered command-line arguments.

#### cli_command

```
cli_command: str

```

The equivalent CLI command.

#### cli_name

```
cli_name = 'mypy'

```

The name of the executable on PATH.

#### py_args

```
py_args: dict[str, Any] = py_args or {}

```

Registered Python arguments.

#### __call__

```
__call__() -> None

```

Run the command.

Source code in `src/duty/_internal/tools/_mypy.py`

```
def __call__(self) -> None:
    """Run the command."""
    from mypy.main import main as run_mypy  # noqa: PLC0415

    run_mypy(
        args=self.cli_args,
        stdout=LazyStdout(),
        stderr=LazyStderr(),
        clean_exit=True,
    )

```

#### add_args

```
add_args(*args: str) -> Self

```

Append CLI arguments.

Source code in `src/duty/_internal/tools/_base.py`

```
def add_args(self, *args: str) -> Self:
    """Append CLI arguments."""
    self.cli_args.extend(args)
    return self

```

### pytest

```
pytest(
    *paths: str,
    config_file: str | None = None,
    select: str | None = None,
    select_markers: str | None = None,
    markers: bool | None = None,
    exitfirst: bool | None = None,
    fixtures: bool | None = None,
    fixtures_per_test: bool | None = None,
    pdb: bool | None = None,
    pdbcls: str | None = None,
    trace: bool | None = None,
    capture: str | None = None,
    runxfail: bool | None = None,
    last_failed: bool | None = None,
    failed_first: bool | None = None,
    new_first: bool | None = None,
    cache_show: str | None = None,
    cache_clear: bool | None = None,
    last_failed_no_failures: Literal["all", "none"]
    | None = None,
    stepwise: bool | None = None,
    stepwise_skip: bool | None = None,
    durations: int | None = None,
    durations_min: int | None = None,
    verbose: bool | None = None,
    no_header: bool | None = None,
    no_summary: bool | None = None,
    quiet: bool | None = None,
    verbosity: int | None = None,
    show_extra_summary: str | None = None,
    disable_pytest_warnings: bool | None = None,
    showlocals: bool | None = None,
    no_showlocals: bool | None = None,
    traceback: Literal[
        "auto", "long", "short", "line", "native", "no"
    ]
    | None = None,
    show_capture: Literal[
        "no", "stdout", "stderr", "log", "all"
    ]
    | None = None,
    full_trace: bool | None = None,
    color: str | None = None,
    code_highlight: bool | None = None,
    pastebin: str | None = None,
    junit_xml: str | None = None,
    junit_prefix: str | None = None,
    pythonwarnings: str | None = None,
    maxfail: int | None = None,
    strict_config: bool | None = None,
    strict_markers: bool | None = None,
    continue_on_collection_errors: bool | None = None,
    rootdir: str | None = None,
    collect_only: bool | None = None,
    pyargs: bool | None = None,
    ignore: list[str] | None = None,
    ignore_glob: list[str] | None = None,
    deselect: str | None = None,
    confcutdir: str | None = None,
    noconftest: bool | None = None,
    keep_duplicates: bool | None = None,
    collect_in_virtualenv: bool | None = None,
    import_mode: Literal["prepend", "append", "importlib"]
    | None = None,
    doctest_modules: bool | None = None,
    doctest_report: Literal[
        "none",
        "cdiff",
        "ndiff",
        "udiff",
        "only_first_failure",
    ]
    | None = None,
    doctest_glob: str | None = None,
    doctest_ignore_import_errors: bool | None = None,
    doctest_continue_on_failure: bool | None = None,
    basetemp: str | None = None,
    plugins: list[str] | None = None,
    no_plugins: list[str] | None = None,
    trace_config: bool | None = None,
    debug: str | None = None,
    override_ini: str | None = None,
    assert_mode: str | None = None,
    setup_only: bool | None = None,
    setup_show: bool | None = None,
    setup_plan: bool | None = None,
    log_level: str | None = None,
    log_format: str | None = None,
    log_date_format: str | None = None,
    log_cli_level: tuple[str, str] | None = None,
    log_cli_format: str | None = None,
    log_cli_date_format: str | None = None,
    log_file: str | None = None,
    log_file_level: str | None = None,
    log_file_format: str | None = None,
    log_file_date_format: str | None = None,
    log_auto_indent: str | None = None,
)

```

Bases: `Tool`

Call [pytest](https://github.com/pytest-dev/pytest).

Parameters:

- **`*paths`** (`str`, default: `()` ) – Files or directories to select tests from.
- **`select`** (`str | None`, default: `None` ) – Only run tests which match the given substring expression. An expression is a Python evaluatable expression where all names are substring-matched against test names and their parent classes. Example: -k 'test_method or test_other' matches all test functions and classes whose name contains 'test_method' or 'test_other', while -k 'not test_method' matches those that don't contain 'test_method' in their names. -k 'not test_method and not test_other' will eliminate the matches. Additionally keywords are matched to classes and functions containing extra names in their 'extra_keyword_matches' set, as well as functions which have names assigned directly to them. The matching is case-insensitive.
- **`select_markers`** (`str | None`, default: `None` ) – Only run tests matching given mark expression. For example: -m 'mark1 and not mark2'.
- **`markers`** (`bool | None`, default: `None` ) – show markers (builtin, plugin and per-project ones).
- **`exitfirst`** (`bool | None`, default: `None` ) – Exit instantly on first error or failed test
- **`fixtures`** (`bool | None`, default: `None` ) – Show available fixtures, sorted by plugin appearance (fixtures with leading '\_' are only shown with '-v')
- **`fixtures_per_test`** (`bool | None`, default: `None` ) – Show fixtures per test
- **`pdb`** (`bool | None`, default: `None` ) – Start the interactive Python debugger on errors or KeyboardInterrupt
- **`pdbcls`** (`str | None`, default: `None` ) – Specify a custom interactive Python debugger for use with --pdb.For example: --pdbcls IPython.terminal.debugger:TerminalPdb
- **`trace`** (`bool | None`, default: `None` ) – Immediately break when running each test
- **`capture`** (`str | None`, default: `None` ) – Per-test capturing method: one of fd|sys|no|tee-sys
- **`runxfail`** (`bool | None`, default: `None` ) – Report the results of xfail tests as if they were not marked
- **`last_failed`** (`bool | None`, default: `None` ) – Rerun only the tests that failed at the last run (or all if none failed)
- **`failed_first`** (`bool | None`, default: `None` ) – Run all tests, but run the last failures first. This may re-order tests and thus lead to repeated fixture setup/teardown.
- **`new_first`** (`bool | None`, default: `None` ) – Run tests from new files first, then the rest of the tests sorted by file mtime
- **`cache_show`** (`str | None`, default: `None` ) – Show cache contents, don't perform collection or tests. Optional argument: glob (default: '\*').
- **`cache_clear`** (`bool | None`, default: `None` ) – Remove all cache contents at start of test run
- **`last_failed_no_failures`** (`Literal['all', 'none'] | None`, default: `None` ) – Which tests to run with no previously (known) failures
- **`stepwise`** (`bool | None`, default: `None` ) – Exit on test failure and continue from last failing test next time
- **`stepwise_skip`** (`bool | None`, default: `None` ) – Ignore the first failing test but stop on the next failing test. Implicitly enables --stepwise.
- **`durations`** (`int | None`, default: `None` ) – Show N slowest setup/test durations (N 0 for all)
- **`durations_min`** (`int | None`, default: `None` ) – Minimal duration in seconds for inclusion in slowest list. Default: 0.005.
- **`verbose`** (`bool | None`, default: `None` ) – Increase verbosity
- **`no_header`** (`bool | None`, default: `None` ) – Disable header
- **`no_summary`** (`bool | None`, default: `None` ) – Disable summary
- **`quiet`** (`bool | None`, default: `None` ) – Decrease verbosity
- **`verbosity`** (`int | None`, default: `None` ) – Set verbosity. Default: 0.
- **`show_extra_summary`** (`str | None`, default: `None` ) – Show extra test summary info as specified by chars: (f)ailed, (E)rror, (s)kipped, (x)failed, (X)passed, (p)assed, (P)assed with output, (a)ll except passed (p/P), or (A)ll. (w)arnings are enabled by default (see --disable-warnings), 'N' can be used to reset the list. (default: 'fE').
- **`disable_pytest_warnings`** (`bool | None`, default: `None` ) – Disable warnings summary
- **`showlocals`** (`bool | None`, default: `None` ) – Show locals in tracebacks (disabled by default)
- **`no_showlocals`** (`bool | None`, default: `None` ) – Hide locals in tracebacks (negate --showlocals passed through addopts)
- **`traceback`** (`Literal['auto', 'long', 'short', 'line', 'native', 'no'] | None`, default: `None` ) – Traceback print mode (auto/long/short/line/native/no)
- **`show_capture`** (`Literal['no', 'stdout', 'stderr', 'log', 'all'] | None`, default: `None` ) – Controls how captured stdout/stderr/log is shown on failed tests. Default: all.
- **`full_trace`** (`bool | None`, default: `None` ) – Don't cut any tracebacks (default is to cut)
- **`color`** (`str | None`, default: `None` ) – Color terminal output (yes/no/auto)
- **`code_highlight`** (`bool | None`, default: `None` ) – {yes,no} Whether code should be highlighted (only if --color is also enabled). Default: yes.
- **`pastebin`** (`str | None`, default: `None` ) – Send failed|all info to bpaste.net pastebin service
- **`junit_xml`** (`str | None`, default: `None` ) – Create junit-xml style report file at given path
- **`junit_prefix`** (`str | None`, default: `None` ) – Prepend prefix to classnames in junit-xml output
- **`pythonwarnings`** (`str | None`, default: `None` ) – Set which warnings to report, see -W option of Python itself
- **`maxfail`** (`int | None`, default: `None` ) – Exit after first num failures or errors
- **`strict_config`** (`bool | None`, default: `None` ) – Any warnings encountered while parsing the pytest section of the configuration file raise errors
- **`strict_markers`** (`bool | None`, default: `None` ) – Markers not registered in the markers section of the configuration file raise errors
- **`config_file`** (`str | None`, default: `None` ) – Load configuration from file instead of trying to locate one of the implicit configuration files
- **`continue_on_collection_errors`** (`bool | None`, default: `None` ) – Force test execution even if collection errors occur
- **`rootdir`** (`str | None`, default: `None` ) – Define root directory for tests. Can be relative path: 'root_dir', './root_dir', 'root_dir/another_dir/'; absolute path: '/home/user/root_dir'; path with variables: '$HOME/root_dir'.
- **`collect_only`** (`bool | None`, default: `None` ) – Only collect tests, don't execute them
- **`pyargs`** (`bool | None`, default: `None` ) – Try to interpret all arguments as Python packages
- **`ignore`** (`list[str] | None`, default: `None` ) – Ignore path during collection (multi-allowed)
- **`ignore_glob`** (`list[str] | None`, default: `None` ) – Ignore path pattern during collection (multi-allowed)
- **`deselect`** (`str | None`, default: `None` ) – Deselect item (via node id prefix) during collection (multi-allowed)
- **`confcutdir`** (`str | None`, default: `None` ) – Only load conftest.py's relative to specified dir
- **`noconftest`** (`bool | None`, default: `None` ) – Don't load any conftest.py files
- **`keep_duplicates`** (`bool | None`, default: `None` ) – Keep duplicate tests
- **`collect_in_virtualenv`** (`bool | None`, default: `None` ) – Don't ignore tests in a local virtualenv directory
- **`import_mode`** (`Literal['prepend', 'append', 'importlib'] | None`, default: `None` ) – Prepend/append to sys.path when importing test modules and conftest files. Default: prepend.
- **`doctest_modules`** (`bool | None`, default: `None` ) – Run doctests in all .py modules
- **`doctest_report`** (`Literal['none', 'cdiff', 'ndiff', 'udiff', 'only_first_failure'] | None`, default: `None` ) – Choose another output format for diffs on doctest failure
- **`doctest_glob`** (`str | None`, default: `None` ) – Doctests file matching pattern, default: test\*.txt
- **`doctest_ignore_import_errors`** (`bool | None`, default: `None` ) – Ignore doctest ImportErrors
- **`doctest_continue_on_failure`** (`bool | None`, default: `None` ) – For a given doctest, continue to run after the first failure
- **`basetemp`** (`str | None`, default: `None` ) – Base temporary directory for this test run. (Warning: this directory is removed if it exists.)
- **`plugins`** (`list[str] | None`, default: `None` ) – Early-load given plugin module name or entry point (multi-allowed). To avoid loading of plugins, use the no: prefix, e.g. no:doctest.
- **`no_plugins`** (`list[str] | None`, default: `None` ) – Early-load given plugin module name or entry point (multi-allowed). To avoid loading of plugins, use the no: prefix, e.g. no:doctest.
- **`trace_config`** (`bool | None`, default: `None` ) – Trace considerations of conftest.py files
- **`debug`** (`str | None`, default: `None` ) – Store internal tracing debug information in this log file. This file is opened with 'w' and truncated as a result, care advised. Default: pytestdebug.log.
- **`override_ini`** (`str | None`, default: `None` ) – Override ini option with "option value" style, e.g. -o xfail_strict True -o cache_dir cache.
- **`assert_mode`** (`str | None`, default: `None` ) – Control assertion debugging tools. 'plain' performs no assertion debugging. 'rewrite' (the default) rewrites assert statements in test modules on import to provide assert expression information.
- **`setup_only`** (`bool | None`, default: `None` ) – Only setup fixtures, do not execute tests
- **`setup_show`** (`bool | None`, default: `None` ) – Show setup of fixtures while executing tests
- **`setup_plan`** (`bool | None`, default: `None` ) – Show what fixtures and tests would be executed but don't execute anything
- **`log_level`** (`str | None`, default: `None` ) – Level of messages to catch/display. Not set by default, so it depends on the root/parent log handler's effective level, where it is "WARNING" by default.
- **`log_format`** (`str | None`, default: `None` ) – Log format used by the logging module.
- **`log_date_format`** (`str | None`, default: `None` ) – Log date format used by the logging module.
- **`log_cli_level`** (`tuple[str, str] | None`, default: `None` ) – logging level.
- **`log_cli_format`** (`str | None`, default: `None` ) – Log format used by the logging module.
- **`log_cli_date_format`** (`str | None`, default: `None` ) – Log date format used by the logging module.
- **`log_file`** (`str | None`, default: `None` ) – Path to a file when logging will be written to.
- **`log_file_level`** (`str | None`, default: `None` ) – Log file logging level.
- **`log_file_format`** (`str | None`, default: `None` ) – Log format used by the logging module.
- **`log_file_date_format`** (`str | None`, default: `None` ) – Log date format used by the logging module.
- **`log_auto_indent`** (`str | None`, default: `None` ) – Auto-indent multiline messages passed to the logging module. Accepts true|on, false|off or an integer.

Methods:

- **`__call__`** – Run the command.
- **`add_args`** – Append CLI arguments.

Attributes:

- **`cli_args`** (`list[str]`) – Registered command-line arguments.
- **`cli_command`** (`str`) – The equivalent CLI command.
- **`cli_name`** – The name of the executable on PATH.
- **`py_args`** (`dict[str, Any]`) – Registered Python arguments.

Source code in `src/duty/_internal/tools/_pytest.py`

```
def __init__(
    self,
    *paths: str,
    config_file: str | None = None,
    select: str | None = None,
    select_markers: str | None = None,
    markers: bool | None = None,
    exitfirst: bool | None = None,
    fixtures: bool | None = None,
    fixtures_per_test: bool | None = None,
    pdb: bool | None = None,
    pdbcls: str | None = None,
    trace: bool | None = None,
    capture: str | None = None,
    runxfail: bool | None = None,
    last_failed: bool | None = None,
    failed_first: bool | None = None,
    new_first: bool | None = None,
    cache_show: str | None = None,
    cache_clear: bool | None = None,
    last_failed_no_failures: Literal["all", "none"] | None = None,
    stepwise: bool | None = None,
    stepwise_skip: bool | None = None,
    durations: int | None = None,
    durations_min: int | None = None,
    verbose: bool | None = None,
    no_header: bool | None = None,
    no_summary: bool | None = None,
    quiet: bool | None = None,
    verbosity: int | None = None,
    show_extra_summary: str | None = None,
    disable_pytest_warnings: bool | None = None,
    showlocals: bool | None = None,
    no_showlocals: bool | None = None,
    traceback: Literal["auto", "long", "short", "line", "native", "no"] | None = None,
    show_capture: Literal["no", "stdout", "stderr", "log", "all"] | None = None,
    full_trace: bool | None = None,
    color: str | None = None,
    code_highlight: bool | None = None,
    pastebin: str | None = None,
    junit_xml: str | None = None,
    junit_prefix: str | None = None,
    pythonwarnings: str | None = None,
    maxfail: int | None = None,
    strict_config: bool | None = None,
    strict_markers: bool | None = None,
    continue_on_collection_errors: bool | None = None,
    rootdir: str | None = None,
    collect_only: bool | None = None,
    pyargs: bool | None = None,
    ignore: list[str] | None = None,
    ignore_glob: list[str] | None = None,
    deselect: str | None = None,
    confcutdir: str | None = None,
    noconftest: bool | None = None,
    keep_duplicates: bool | None = None,
    collect_in_virtualenv: bool | None = None,
    import_mode: Literal["prepend", "append", "importlib"] | None = None,
    doctest_modules: bool | None = None,
    doctest_report: Literal["none", "cdiff", "ndiff", "udiff", "only_first_failure"] | None = None,
    doctest_glob: str | None = None,
    doctest_ignore_import_errors: bool | None = None,
    doctest_continue_on_failure: bool | None = None,
    basetemp: str | None = None,
    plugins: list[str] | None = None,
    no_plugins: list[str] | None = None,
    trace_config: bool | None = None,
    debug: str | None = None,
    override_ini: str | None = None,
    assert_mode: str | None = None,
    setup_only: bool | None = None,
    setup_show: bool | None = None,
    setup_plan: bool | None = None,
    log_level: str | None = None,
    log_format: str | None = None,
    log_date_format: str | None = None,
    log_cli_level: tuple[str, str] | None = None,
    log_cli_format: str | None = None,
    log_cli_date_format: str | None = None,
    log_file: str | None = None,
    log_file_level: str | None = None,
    log_file_format: str | None = None,
    log_file_date_format: str | None = None,
    log_auto_indent: str | None = None,
) -> None:
    """Run `pytest`.

    Parameters:
        *paths: Files or directories to select tests from.
        select: Only run tests which match the given substring expression. An expression is a Python evaluatable expression where all names are substring-matched against test names and their parent classes. Example: -k 'test_method or test_other' matches all test functions and classes whose name contains 'test_method' or 'test_other', while -k 'not test_method' matches those that don't contain 'test_method' in their names. -k 'not test_method and not test_other' will eliminate the matches. Additionally keywords are matched to classes and functions containing extra names in their 'extra_keyword_matches' set, as well as functions which have names assigned directly to them. The matching is case-insensitive.
        select_markers: Only run tests matching given mark expression. For example: -m 'mark1 and not mark2'.
        markers: show markers (builtin, plugin and per-project ones).
        exitfirst: Exit instantly on first error or failed test
        fixtures: Show available fixtures, sorted by plugin appearance (fixtures with leading '_' are only shown with '-v')
        fixtures_per_test: Show fixtures per test
        pdb: Start the interactive Python debugger on errors or KeyboardInterrupt
        pdbcls: Specify a custom interactive Python debugger for use with --pdb.For example: --pdbcls IPython.terminal.debugger:TerminalPdb
        trace: Immediately break when running each test
        capture: Per-test capturing method: one of fd|sys|no|tee-sys
        runxfail: Report the results of xfail tests as if they were not marked
        last_failed: Rerun only the tests that failed at the last run (or all if none failed)
        failed_first: Run all tests, but run the last failures first. This may re-order tests and thus lead to repeated fixture setup/teardown.
        new_first: Run tests from new files first, then the rest of the tests sorted by file mtime
        cache_show: Show cache contents, don't perform collection or tests. Optional argument: glob (default: '*').
        cache_clear: Remove all cache contents at start of test run
        last_failed_no_failures: Which tests to run with no previously (known) failures
        stepwise: Exit on test failure and continue from last failing test next time
        stepwise_skip: Ignore the first failing test but stop on the next failing test. Implicitly enables --stepwise.
        durations: Show N slowest setup/test durations (N 0 for all)
        durations_min: Minimal duration in seconds for inclusion in slowest list. Default: 0.005.
        verbose: Increase verbosity
        no_header: Disable header
        no_summary: Disable summary
        quiet: Decrease verbosity
        verbosity: Set verbosity. Default: 0.
        show_extra_summary: Show extra test summary info as specified by chars: (f)ailed, (E)rror, (s)kipped, (x)failed, (X)passed, (p)assed, (P)assed with output, (a)ll except passed (p/P), or (A)ll. (w)arnings are enabled by default (see --disable-warnings), 'N' can be used to reset the list. (default: 'fE').
        disable_pytest_warnings: Disable warnings summary
        showlocals: Show locals in tracebacks (disabled by default)
        no_showlocals: Hide locals in tracebacks (negate --showlocals passed through addopts)
        traceback: Traceback print mode (auto/long/short/line/native/no)
        show_capture: Controls how captured stdout/stderr/log is shown on failed tests. Default: all.
        full_trace: Don't cut any tracebacks (default is to cut)
        color: Color terminal output (yes/no/auto)
        code_highlight: {yes,no} Whether code should be highlighted (only if --color is also enabled). Default: yes.
        pastebin: Send failed|all info to bpaste.net pastebin service
        junit_xml: Create junit-xml style report file at given path
        junit_prefix: Prepend prefix to classnames in junit-xml output
        pythonwarnings: Set which warnings to report, see -W option of Python itself
        maxfail: Exit after first num failures or errors
        strict_config: Any warnings encountered while parsing the `pytest` section of the configuration file raise errors
        strict_markers: Markers not registered in the `markers` section of the configuration file raise errors
        config_file: Load configuration from `file` instead of trying to locate one of the implicit configuration files
        continue_on_collection_errors: Force test execution even if collection errors occur
        rootdir: Define root directory for tests. Can be relative path: 'root_dir', './root_dir', 'root_dir/another_dir/'; absolute path: '/home/user/root_dir'; path with variables: '$HOME/root_dir'.
        collect_only: Only collect tests, don't execute them
        pyargs: Try to interpret all arguments as Python packages
        ignore: Ignore path during collection (multi-allowed)
        ignore_glob: Ignore path pattern during collection (multi-allowed)
        deselect: Deselect item (via node id prefix) during collection (multi-allowed)
        confcutdir: Only load conftest.py's relative to specified dir
        noconftest: Don't load any conftest.py files
        keep_duplicates: Keep duplicate tests
        collect_in_virtualenv: Don't ignore tests in a local virtualenv directory
        import_mode: Prepend/append to sys.path when importing test modules and conftest files. Default: prepend.
        doctest_modules: Run doctests in all .py modules
        doctest_report: Choose another output format for diffs on doctest failure
        doctest_glob: Doctests file matching pattern, default: test*.txt
        doctest_ignore_import_errors: Ignore doctest ImportErrors
        doctest_continue_on_failure: For a given doctest, continue to run after the first failure
        basetemp: Base temporary directory for this test run. (Warning: this directory is removed if it exists.)
        plugins: Early-load given plugin module name or entry point (multi-allowed). To avoid loading of plugins, use the `no:` prefix, e.g. `no:doctest`.
        no_plugins: Early-load given plugin module name or entry point (multi-allowed). To avoid loading of plugins, use the `no:` prefix, e.g. `no:doctest`.
        trace_config: Trace considerations of conftest.py files
        debug: Store internal tracing debug information in this log file. This file is opened with 'w' and truncated as a result, care advised. Default: pytestdebug.log.
        override_ini: Override ini option with "option value" style, e.g. `-o xfail_strict True -o cache_dir cache`.
        assert_mode: Control assertion debugging tools. 'plain' performs no assertion debugging. 'rewrite' (the default) rewrites assert statements in test modules on import to provide assert expression information.
        setup_only: Only setup fixtures, do not execute tests
        setup_show: Show setup of fixtures while executing tests
        setup_plan: Show what fixtures and tests would be executed but don't execute anything
        log_level: Level of messages to catch/display. Not set by default, so it depends on the root/parent log handler's effective level, where it is "WARNING" by default.
        log_format: Log format used by the logging module.
        log_date_format: Log date format used by the logging module.
        log_cli_level: logging level.
        log_cli_format: Log format used by the logging module.
        log_cli_date_format: Log date format used by the logging module.
        log_file: Path to a file when logging will be written to.
        log_file_level: Log file logging level.
        log_file_format: Log format used by the logging module.
        log_file_date_format: Log date format used by the logging module.
        log_auto_indent: Auto-indent multiline messages passed to the logging module. Accepts true|on, false|off or an integer.
    """
    cli_args = list(paths)

    if select:
        cli_args.append("-k")
        cli_args.append(select)

    if select_markers:
        cli_args.append("-m")
        cli_args.append(select_markers)

    if markers:
        cli_args.append("--markers")

    if exitfirst:
        cli_args.append("--exitfirst")

    if fixtures:
        cli_args.append("--fixtures")

    if fixtures_per_test:
        cli_args.append("--fixtures-per-test")

    if pdb:
        cli_args.append("--pdb")

    if pdbcls:
        cli_args.append("--pdbcls")
        cli_args.append(pdbcls)

    if trace:
        cli_args.append("--trace")

    if capture:
        cli_args.append("--capture")

    if runxfail:
        cli_args.append("--runxfail")

    if last_failed:
        cli_args.append("--last-failed")

    if failed_first:
        cli_args.append("--failed-first")

    if new_first:
        cli_args.append("--new-first")

    if cache_show:
        cli_args.append("--cache-show")
        cli_args.append(cache_show)

    if cache_clear:
        cli_args.append("--cache-clear")

    if last_failed_no_failures:
        cli_args.append("--last-failed-no-failures")
        cli_args.append(last_failed_no_failures)

    if stepwise:
        cli_args.append("--stepwise")

    if stepwise_skip:
        cli_args.append("--stepwise-skip")

    if durations:
        cli_args.append("--durations")
        cli_args.append(str(durations))

    if durations_min:
        cli_args.append("--durations-min")
        cli_args.append(str(durations_min))

    if verbose:
        cli_args.append("--verbose")

    if no_header:
        cli_args.append("--no-header")

    if no_summary:
        cli_args.append("--no-summary")

    if quiet:
        cli_args.append("--quiet")

    if verbosity:
        cli_args.append("--verbosity")
        cli_args.append(str(verbosity))

    if show_extra_summary:
        cli_args.append("-r")
        cli_args.append(show_extra_summary)

    if disable_pytest_warnings:
        cli_args.append("--disable-pytest-warnings")

    if showlocals:
        cli_args.append("--showlocals")

    if no_showlocals:
        cli_args.append("--no-showlocals")

    if traceback:
        cli_args.append("--tb")
        cli_args.append(traceback)

    if show_capture:
        cli_args.append("--show-capture")
        cli_args.append(show_capture)

    if full_trace:
        cli_args.append("--full-trace")

    if color:
        cli_args.append("--color")
        cli_args.append(color)

    if code_highlight:
        cli_args.append("--code-highlight")

    if pastebin:
        cli_args.append("--pastebin")
        cli_args.append(pastebin)

    if junit_xml:
        cli_args.append("--junit-xml")
        cli_args.append(junit_xml)

    if junit_prefix:
        cli_args.append("--junit-prefix")
        cli_args.append(junit_prefix)

    if pythonwarnings:
        cli_args.append("--pythonwarnings")
        cli_args.append(pythonwarnings)

    if maxfail:
        cli_args.append("--maxfail")
        cli_args.append(str(maxfail))

    if strict_config:
        cli_args.append("--strict-config")

    if strict_markers:
        cli_args.append("--strict-markers")

    if config_file:
        cli_args.append("-c")
        cli_args.append(config_file)

    if continue_on_collection_errors:
        cli_args.append("--continue-on-collection-errors")

    if rootdir:
        cli_args.append("--rootdir")
        cli_args.append(rootdir)

    if collect_only:
        cli_args.append("--collect-only")

    if pyargs:
        cli_args.append("--pyargs")

    if ignore:
        for ign in ignore:
            cli_args.append("--ignore")
            cli_args.append(ign)

    if ignore_glob:
        for ign_glob in ignore_glob:
            cli_args.append("--ignore-glob")
            cli_args.append(ign_glob)

    if deselect:
        cli_args.append("--deselect")
        cli_args.append(deselect)

    if confcutdir:
        cli_args.append("--confcutdir")
        cli_args.append(confcutdir)

    if noconftest:
        cli_args.append("--noconftest")

    if keep_duplicates:
        cli_args.append("--keep-duplicates")

    if collect_in_virtualenv:
        cli_args.append("--collect-in-virtualenv")

    if import_mode:
        cli_args.append("--import-mode")
        cli_args.append(import_mode)

    if doctest_modules:
        cli_args.append("--doctest-modules")

    if doctest_report:
        cli_args.append("--doctest-report")
        cli_args.append(doctest_report)

    if doctest_glob:
        cli_args.append("--doctest-glob")
        cli_args.append(doctest_glob)

    if doctest_ignore_import_errors:
        cli_args.append("--doctest-ignore-import-errors")

    if doctest_continue_on_failure:
        cli_args.append("--doctest-continue-on-failure")

    if basetemp:
        cli_args.append("--basetemp")
        cli_args.append(basetemp)

    if plugins:
        for plugin in plugins:
            cli_args.append("-p")
            cli_args.append(plugin)

    if no_plugins:
        for no_plugin in no_plugins:
            cli_args.append("-p")
            cli_args.append(f"no:{no_plugin}")

    if trace_config:
        cli_args.append("--trace-config")

    if debug:
        cli_args.append("--debug")
        cli_args.append(debug)

    if override_ini:
        cli_args.append("--override-ini")
        cli_args.append(override_ini)

    if assert_mode:
        cli_args.append("--assert")
        cli_args.append(assert_mode)

    if setup_only:
        cli_args.append("--setup-only")

    if setup_show:
        cli_args.append("--setup-show")

    if setup_plan:
        cli_args.append("--setup-plan")

    if log_level:
        cli_args.append("--log-level")
        cli_args.append(log_level)

    if log_format:
        cli_args.append("--log-format")
        cli_args.append(log_format)

    if log_date_format:
        cli_args.append("--log-date-format")
        cli_args.append(log_date_format)

    if log_cli_level:
        cli_args.append("--log-cli-level")
        cli_args.extend(log_cli_level)

    if log_cli_format:
        cli_args.append("--log-cli-format")
        cli_args.append(log_cli_format)

    if log_cli_date_format:
        cli_args.append("--log-cli-date-format")
        cli_args.append(log_cli_date_format)

    if log_file:
        cli_args.append("--log-file")
        cli_args.append(log_file)

    if log_file_level:
        cli_args.append("--log-file-level")
        cli_args.append(log_file_level)

    if log_file_format:
        cli_args.append("--log-file-format")
        cli_args.append(log_file_format)

    if log_file_date_format:
        cli_args.append("--log-file-date-format")
        cli_args.append(log_file_date_format)

    if log_auto_indent:
        cli_args.append("--log-auto-indent")
        cli_args.append(log_auto_indent)

    super().__init__(cli_args)

```

#### cli_args

```
cli_args: list[str] = cli_args or []

```

Registered command-line arguments.

#### cli_command

```
cli_command: str

```

The equivalent CLI command.

#### cli_name

```
cli_name = 'pytest'

```

The name of the executable on PATH.

#### py_args

```
py_args: dict[str, Any] = py_args or {}

```

Registered Python arguments.

#### __call__

```
__call__() -> int

```

Run the command.

Returns:

- `int` – The exit code of the command.

Source code in `src/duty/_internal/tools/_pytest.py`

```
def __call__(self) -> int:
    """Run the command.

    Returns:
        The exit code of the command.
    """
    from pytest import main as run_pytest  # noqa: PT013,PLC0415

    return run_pytest(self.cli_args)

```

#### add_args

```
add_args(*args: str) -> Self

```

Append CLI arguments.

Source code in `src/duty/_internal/tools/_base.py`

```
def add_args(self, *args: str) -> Self:
    """Append CLI arguments."""
    self.cli_args.extend(args)
    return self

```

### ruff

```
ruff(
    cli_args: list[str] | None = None,
    py_args: dict[str, Any] | None = None,
)

```

Bases: `Tool`

Call [Ruff](https://github.com/astral-sh/ruff).

Parameters:

- **`cli_args`** (`list[str] | None`, default: `None` ) – Initial command-line arguments. Use add_args() to add more.
- **`py_args`** (`dict[str, Any] | None`, default: `None` ) – Python arguments. Your __call__ method will be able to access these arguments as self.py_args.

Methods:

- **`__call__`** – Run the command.
- **`add_args`** – Append CLI arguments.
- **`check`** – Run Ruff on the given files or directories.
- **`clean`** – Clear any caches in the current directory and any subdirectories.
- **`config`** – List or describe the available configuration options.
- **`format`** – Run Ruff formatter on the given files or directories.
- **`linter`** – List all supported upstream linters.
- **`rule`** – Explain a rule.

Attributes:

- **`cli_args`** (`list[str]`) – Registered command-line arguments.
- **`cli_command`** (`str`) – The equivalent CLI command.
- **`cli_name`** – The name of the executable on PATH.
- **`py_args`** (`dict[str, Any]`) – Registered Python arguments.

Source code in `src/duty/_internal/tools/_base.py`

```
def __init__(
    self,
    cli_args: list[str] | None = None,
    py_args: dict[str, Any] | None = None,
) -> None:
    """Initialize the tool.

    Parameters:
        cli_args: Initial command-line arguments. Use `add_args()` to add more.
        py_args: Python arguments. Your `__call__` method will be able to access
            these arguments as `self.py_args`.
    """
    self.cli_args: list[str] = cli_args or []
    """Registered command-line arguments."""
    self.py_args: dict[str, Any] = py_args or {}
    """Registered Python arguments."""

```

#### cli_args

```
cli_args: list[str] = cli_args or []

```

Registered command-line arguments.

#### cli_command

```
cli_command: str

```

The equivalent CLI command.

#### cli_name

```
cli_name = 'ruff'

```

The name of the executable on PATH.

#### py_args

```
py_args: dict[str, Any] = py_args or {}

```

Registered Python arguments.

#### __call__

```
__call__() -> int

```

Run the command.

Returns:

- `int` – The exit code of the command.

Source code in `src/duty/_internal/tools/_ruff.py`

```
def __call__(self) -> int:
    """Run the command.

    Returns:
        The exit code of the command.
    """
    process = subprocess.run(  # noqa: S603
        [_find_ruff(), *self.cli_args],
        capture_output=True,
        text=True,
        check=False,
    )
    print(process.stdout)  # noqa: T201
    return process.returncode

```

#### add_args

```
add_args(*args: str) -> Self

```

Append CLI arguments.

Source code in `src/duty/_internal/tools/_base.py`

```
def add_args(self, *args: str) -> Self:
    """Append CLI arguments."""
    self.cli_args.extend(args)
    return self

```

#### check

```
check(
    *files: str,
    config: str | None = None,
    fix: bool | None = None,
    show_source: bool | None = None,
    show_fixes: bool | None = None,
    diff: bool | None = None,
    watch: bool | None = None,
    fix_only: bool | None = None,
    output_format: str | None = None,
    statistics: bool | None = None,
    add_noqa: bool | None = None,
    show_files: bool | None = None,
    show_settings: bool | None = None,
    select: list[str] | None = None,
    ignore: list[str] | None = None,
    extend_select: list[str] | None = None,
    per_file_ignores: dict[str, list[str]] | None = None,
    fixable: list[str] | None = None,
    unfixable: list[str] | None = None,
    exclude: list[str] | None = None,
    extend_exclude: list[str] | None = None,
    respect_gitignore: bool | None = None,
    force_exclude: bool | None = None,
    no_cache: bool | None = None,
    isolated: bool | None = None,
    cache_dir: str | None = None,
    stdin_filename: str | None = None,
    exit_zero: bool | None = None,
    exit_non_zero_on_fix: bool | None = None,
    verbose: bool = False,
    quiet: bool = False,
    silent: bool = False,
) -> ruff

```

Run Ruff on the given files or directories.

Parameters:

- **`fix`** (`bool | None`, default: `None` ) – Attempt to automatically fix lint violations.
- **`config`** (`str | None`, default: `None` ) – Path to the pyproject.toml or ruff.toml file to use for configuration.
- **`show_source`** (`bool | None`, default: `None` ) – Show violations with source code.
- **`show_fixes`** (`bool | None`, default: `None` ) – Show an enumeration of all autofixed lint violations.
- **`diff`** (`bool | None`, default: `None` ) – Avoid writing any fixed files back; instead, output a diff for each changed file to stdout.
- **`watch`** (`bool | None`, default: `None` ) – Run in watch mode by re-running whenever files change.
- **`fix_only`** (`bool | None`, default: `None` ) – Fix any fixable lint violations, but don't report on leftover violations. Implies --fix.
- **`output_format`** (`str | None`, default: `None` ) – Output serialization format for violations (env: RUFF_FORMAT=) (possible values: text, json, junit, grouped, github, gitlab, pylint).
- **`statistics`** (`bool | None`, default: `None` ) – Show counts for every rule with at least one violation.
- **`add_noqa`** (`bool | None`, default: `None` ) – Enable automatic additions of noqa directives to failing lines.
- **`show_files`** (`bool | None`, default: `None` ) – See the files Ruff will be run against with the current settings.
- **`show_settings`** (`bool | None`, default: `None` ) – See the settings Ruff will use to lint a given Python file.
- **`select`** (`list[str] | None`, default: `None` ) – Comma-separated list of rule codes to enable (or ALL, to enable all rules).
- **`ignore`** (`list[str] | None`, default: `None` ) – Comma-separated list of rule codes to disable.
- **`extend_select`** (`list[str] | None`, default: `None` ) – Like --select, but adds additional rule codes on top of the selected ones.
- **`per_file_ignores`** (`dict[str, list[str]] | None`, default: `None` ) – List of mappings from file pattern to code to exclude.
- **`fixable`** (`list[str] | None`, default: `None` ) – List of rule codes to treat as eligible for autofix. Only applicable when autofix itself is enabled (e.g., via --fix).
- **`unfixable`** (`list[str] | None`, default: `None` ) – List of rule codes to treat as ineligible for autofix. Only applicable when autofix itself is enabled (e.g., via --fix).
- **`exclude`** (`list[str] | None`, default: `None` ) – List of paths, used to omit files and/or directories from analysis.
- **`extend_exclude`** (`list[str] | None`, default: `None` ) – Like --exclude, but adds additional files and directories on top of those already excluded.
- **`respect_gitignore`** (`bool | None`, default: `None` ) – Respect file exclusions via .gitignore and other standard ignore files.
- **`force_exclude`** (`bool | None`, default: `None` ) – Enforce exclusions, even for paths passed to Ruff directly on the command-line.
- **`no_cache`** (`bool | None`, default: `None` ) – Disable cache reads.
- **`isolated`** (`bool | None`, default: `None` ) – Ignore all configuration files.
- **`cache_dir`** (`str | None`, default: `None` ) – Path to the cache directory (env: RUFF_CACHE_DIR=).
- **`stdin_filename`** (`str | None`, default: `None` ) – The name of the file when passing it through stdin.
- **`exit_zero`** (`bool | None`, default: `None` ) – Exit with status code "0", even upon detecting lint violations.
- **`exit_non_zero_on_fix`** (`bool | None`, default: `None` ) – Exit with a non-zero status code if any files were modified via autofix, even if no lint violations remain.
- **`verbose`** (`bool`, default: `False` ) – Enable verbose logging.
- **`quiet`** (`bool`, default: `False` ) – Print lint violations, but nothing else.
- **`silent`** (`bool`, default: `False` ) – Disable all logging (but still exit with status code "1" upon detecting lint violations).

Source code in `src/duty/_internal/tools/_ruff.py`

```
@classmethod
def check(
    cls,
    *files: str,
    config: str | None = None,
    fix: bool | None = None,
    show_source: bool | None = None,
    show_fixes: bool | None = None,
    diff: bool | None = None,
    watch: bool | None = None,
    fix_only: bool | None = None,
    output_format: str | None = None,
    statistics: bool | None = None,
    add_noqa: bool | None = None,
    show_files: bool | None = None,
    show_settings: bool | None = None,
    select: list[str] | None = None,
    ignore: list[str] | None = None,
    extend_select: list[str] | None = None,
    per_file_ignores: dict[str, list[str]] | None = None,
    fixable: list[str] | None = None,
    unfixable: list[str] | None = None,
    exclude: list[str] | None = None,
    extend_exclude: list[str] | None = None,
    respect_gitignore: bool | None = None,
    force_exclude: bool | None = None,
    no_cache: bool | None = None,
    isolated: bool | None = None,
    cache_dir: str | None = None,
    stdin_filename: str | None = None,
    exit_zero: bool | None = None,
    exit_non_zero_on_fix: bool | None = None,
    verbose: bool = False,
    quiet: bool = False,
    silent: bool = False,
) -> ruff:
    """Run Ruff on the given files or directories.

    Parameters:
        fix: Attempt to automatically fix lint violations.
        config: Path to the `pyproject.toml` or `ruff.toml` file to use for configuration.
        show_source: Show violations with source code.
        show_fixes: Show an enumeration of all autofixed lint violations.
        diff: Avoid writing any fixed files back; instead, output a diff for each changed file to stdout.
        watch: Run in watch mode by re-running whenever files change.
        fix_only: Fix any fixable lint violations, but don't report on leftover violations. Implies `--fix`.
        output_format: Output serialization format for violations (env: RUFF_FORMAT=) (possible values: text, json, junit, grouped, github, gitlab, pylint).
        statistics: Show counts for every rule with at least one violation.
        add_noqa: Enable automatic additions of `noqa` directives to failing lines.
        show_files: See the files Ruff will be run against with the current settings.
        show_settings: See the settings Ruff will use to lint a given Python file.
        select: Comma-separated list of rule codes to enable (or ALL, to enable all rules).
        ignore: Comma-separated list of rule codes to disable.
        extend_select: Like --select, but adds additional rule codes on top of the selected ones.
        per_file_ignores: List of mappings from file pattern to code to exclude.
        fixable: List of rule codes to treat as eligible for autofix. Only applicable when autofix itself is enabled (e.g., via `--fix`).
        unfixable: List of rule codes to treat as ineligible for autofix. Only applicable when autofix itself is enabled (e.g., via `--fix`).
        exclude: List of paths, used to omit files and/or directories from analysis.
        extend_exclude: Like --exclude, but adds additional files and directories on top of those already excluded.
        respect_gitignore: Respect file exclusions via `.gitignore` and other standard ignore files.
        force_exclude: Enforce exclusions, even for paths passed to Ruff directly on the command-line.
        no_cache: Disable cache reads.
        isolated: Ignore all configuration files.
        cache_dir: Path to the cache directory (env: RUFF_CACHE_DIR=).
        stdin_filename: The name of the file when passing it through stdin.
        exit_zero: Exit with status code "0", even upon detecting lint violations.
        exit_non_zero_on_fix: Exit with a non-zero status code if any files were modified via autofix, even if no lint violations remain.
        verbose: Enable verbose logging.
        quiet: Print lint violations, but nothing else.
        silent: Disable all logging (but still exit with status code "1" upon detecting lint violations).
    """
    cli_args = ["check", *files]

    if fix:
        cli_args.append("--fix")

    if show_source:
        cli_args.append("--show-source")

    if show_fixes:
        cli_args.append("--show-fixes")

    if diff:
        cli_args.append("--diff")

    if watch:
        cli_args.append("--watch")

    if fix_only:
        cli_args.append("--fix-only")

    if output_format:
        cli_args.append("--format")
        cli_args.append(output_format)

    if config:
        cli_args.append("--config")
        cli_args.append(config)

    if statistics:
        cli_args.append("--statistics")

    if add_noqa:
        cli_args.append("--add-noqa")

    if show_files:
        cli_args.append("--show-files")

    if show_settings:
        cli_args.append("--show-settings")

    if select:
        cli_args.append("--select")
        cli_args.append(",".join(select))

    if ignore:
        cli_args.append("--ignore")
        cli_args.append(",".join(ignore))

    if extend_select:
        cli_args.append("--extend-select")
        cli_args.append(",".join(extend_select))

    if per_file_ignores:
        cli_args.append("--per-file-ignores")
        cli_args.append(
            " ".join(f"{path}:{','.join(codes)}" for path, codes in per_file_ignores.items()),
        )

    if fixable:
        cli_args.append("--fixable")
        cli_args.append(",".join(fixable))

    if unfixable:
        cli_args.append("--unfixable")
        cli_args.append(",".join(unfixable))

    if exclude:
        cli_args.append("--exclude")
        cli_args.append(",".join(exclude))

    if extend_exclude:
        cli_args.append("--extend-exclude")
        cli_args.append(",".join(extend_exclude))

    if respect_gitignore:
        cli_args.append("--respect-gitignore")

    if force_exclude:
        cli_args.append("--force-exclude")

    if no_cache:
        cli_args.append("--no-cache")

    if isolated:
        cli_args.append("--isolated")

    if cache_dir:
        cli_args.append("--cache-dir")
        cli_args.append(cache_dir)

    if stdin_filename:
        cli_args.append("--stdin-filename")
        cli_args.append(stdin_filename)

    if exit_zero:
        cli_args.append("--exit-zero")

    if exit_non_zero_on_fix:
        cli_args.append("--exit-non-zero-on-fix")

    if verbose:
        cli_args.append("--verbose")

    if quiet:
        cli_args.append("--quiet")

    if silent:
        cli_args.append("--silent")

    return cls(cli_args)

```

#### clean

```
clean(
    *,
    verbose: bool = False,
    quiet: bool = False,
    silent: bool = False,
) -> ruff

```

Clear any caches in the current directory and any subdirectories.

Parameters:

- **`verbose`** (`bool`, default: `False` ) – Enable verbose logging.
- **`quiet`** (`bool`, default: `False` ) – Print lint violations, but nothing else.
- **`silent`** (`bool`, default: `False` ) – Disable all logging (but still exit with status code "1" upon detecting lint violations).

Source code in `src/duty/_internal/tools/_ruff.py`

```
@classmethod
def clean(
    cls,
    *,
    verbose: bool = False,
    quiet: bool = False,
    silent: bool = False,
) -> ruff:
    """Clear any caches in the current directory and any subdirectories.

    Parameters:
        verbose: Enable verbose logging.
        quiet: Print lint violations, but nothing else.
        silent: Disable all logging (but still exit with status code "1" upon detecting lint violations).
    """
    cli_args = ["clean"]

    if verbose:
        cli_args.append("--verbose")

    if quiet:
        cli_args.append("--quiet")

    if silent:
        cli_args.append("--silent")

    return cls(cli_args)

```

#### config

```
config(
    *,
    verbose: bool = False,
    quiet: bool = False,
    silent: bool = False,
) -> ruff

```

List or describe the available configuration options.

Parameters:

- **`verbose`** (`bool`, default: `False` ) – Enable verbose logging.
- **`quiet`** (`bool`, default: `False` ) – Print lint violations, but nothing else.
- **`silent`** (`bool`, default: `False` ) – Disable all logging (but still exit with status code "1" upon detecting lint violations).

Source code in `src/duty/_internal/tools/_ruff.py`

```
@classmethod
def config(
    cls,
    *,
    verbose: bool = False,
    quiet: bool = False,
    silent: bool = False,
) -> ruff:
    """List or describe the available configuration options.

    Parameters:
        verbose: Enable verbose logging.
        quiet: Print lint violations, but nothing else.
        silent: Disable all logging (but still exit with status code "1" upon detecting lint violations).
    """
    cli_args = ["config"]

    if verbose:
        cli_args.append("--verbose")

    if quiet:
        cli_args.append("--quiet")

    if silent:
        cli_args.append("--silent")

    return cls(cli_args)

```

#### format

```
format(
    *files: str,
    config: str | None = None,
    check: bool | None = None,
    diff: bool | None = None,
    target_version: str | None = None,
    preview: bool | None = None,
    exclude: list[str] | None = None,
    extend_exclude: list[str] | None = None,
    respect_gitignore: bool | None = None,
    force_exclude: bool | None = None,
    no_cache: bool | None = None,
    isolated: bool | None = None,
    cache_dir: str | None = None,
    stdin_filename: str | None = None,
    verbose: bool = False,
    quiet: bool = False,
    silent: bool = False,
) -> ruff

```

Run Ruff formatter on the given files or directories.

Parameters:

- **`check`** (`bool | None`, default: `None` ) – Avoid writing any formatted files back; instead, exit with a non-zero status code if any files would have been modified, and zero otherwise
- **`config`** (`str | None`, default: `None` ) – Path to the pyproject.toml or ruff.toml file to use for configuration
- **`diff`** (`bool | None`, default: `None` ) – Avoid writing any fixed files back; instead, output a diff for each changed file to stdout
- **`target_version`** (`str | None`, default: `None` ) – The minimum Python version that should be supported [possible values: py37, py38, py39, py310, py311, py312]
- **`preview`** (`bool | None`, default: `None` ) – Enable preview mode; enables unstable formatting
- **`exclude`** (`list[str] | None`, default: `None` ) – List of paths, used to omit files and/or directories from analysis
- **`extend_exclude`** (`list[str] | None`, default: `None` ) – Like --exclude, but adds additional files and directories on top of those already excluded
- **`respect_gitignore`** (`bool | None`, default: `None` ) – Respect file exclusions via .gitignore and other standard ignore files
- **`force_exclude`** (`bool | None`, default: `None` ) – Enforce exclusions, even for paths passed to Ruff directly on the command-line
- **`no_cache`** (`bool | None`, default: `None` ) – Disable cache reads
- **`isolated`** (`bool | None`, default: `None` ) – Ignore all configuration files
- **`cache_dir`** (`str | None`, default: `None` ) – Path to the cache directory [env: RUFF_CACHE_DIR=]
- **`stdin_filename`** (`str | None`, default: `None` ) – The name of the file when passing it through stdin
- **`verbose`** (`bool`, default: `False` ) – Enable verbose logging.
- **`quiet`** (`bool`, default: `False` ) – Print lint violations, but nothing else.
- **`silent`** (`bool`, default: `False` ) – Disable all logging (but still exit with status code "1" upon detecting lint violations).

Source code in `src/duty/_internal/tools/_ruff.py`

```
@classmethod
def format(
    cls,
    *files: str,
    config: str | None = None,
    check: bool | None = None,
    diff: bool | None = None,
    target_version: str | None = None,
    preview: bool | None = None,
    exclude: list[str] | None = None,
    extend_exclude: list[str] | None = None,
    respect_gitignore: bool | None = None,
    force_exclude: bool | None = None,
    no_cache: bool | None = None,
    isolated: bool | None = None,
    cache_dir: str | None = None,
    stdin_filename: str | None = None,
    verbose: bool = False,
    quiet: bool = False,
    silent: bool = False,
) -> ruff:
    """Run Ruff formatter on the given files or directories.

    Parameters:
        check: Avoid writing any formatted files back; instead, exit with a non-zero status code if any files would have been modified, and zero otherwise
        config: Path to the `pyproject.toml` or `ruff.toml` file to use for configuration
        diff: Avoid writing any fixed files back; instead, output a diff for each changed file to stdout
        target_version: The minimum Python version that should be supported [possible values: py37, py38, py39, py310, py311, py312]
        preview: Enable preview mode; enables unstable formatting
        exclude: List of paths, used to omit files and/or directories from analysis
        extend_exclude: Like --exclude, but adds additional files and directories on top of those already excluded
        respect_gitignore: Respect file exclusions via `.gitignore` and other standard ignore files
        force_exclude: Enforce exclusions, even for paths passed to Ruff directly on the command-line
        no_cache: Disable cache reads
        isolated: Ignore all configuration files
        cache_dir: Path to the cache directory [env: RUFF_CACHE_DIR=]
        stdin_filename: The name of the file when passing it through stdin
        verbose: Enable verbose logging.
        quiet: Print lint violations, but nothing else.
        silent: Disable all logging (but still exit with status code "1" upon detecting lint violations).
    """
    cli_args = ["format", *files]

    if check:
        cli_args.append("--check")

    if diff:
        cli_args.append("--diff")

    if config:
        cli_args.append("--config")
        cli_args.append(config)

    if target_version:
        cli_args.append("--target-version")
        cli_args.append(target_version)

    if preview:
        cli_args.append("--preview")

    if exclude:
        cli_args.append("--exclude")
        cli_args.append(",".join(exclude))

    if extend_exclude:
        cli_args.append("--extend-exclude")
        cli_args.append(",".join(extend_exclude))

    if respect_gitignore:
        cli_args.append("--respect-gitignore")

    if force_exclude:
        cli_args.append("--force-exclude")

    if no_cache:
        cli_args.append("--no-cache")

    if isolated:
        cli_args.append("--isolated")

    if cache_dir:
        cli_args.append("--cache-dir")
        cli_args.append(cache_dir)

    if stdin_filename:
        cli_args.append("--stdin-filename")
        cli_args.append(stdin_filename)

    if verbose:
        cli_args.append("--verbose")

    if quiet:
        cli_args.append("--quiet")

    if silent:
        cli_args.append("--silent")

    return cls(cli_args)

```

#### linter

```
linter(
    *,
    output_format: str | None = None,
    verbose: bool = False,
    quiet: bool = False,
    silent: bool = False,
) -> ruff

```

List all supported upstream linters.

Parameters:

- **`output_format`** (`str | None`, default: `None` ) – Output format (default: pretty) (possible values: text, json, pretty).
- **`verbose`** (`bool`, default: `False` ) – Enable verbose logging.
- **`quiet`** (`bool`, default: `False` ) – Print lint violations, but nothing else.
- **`silent`** (`bool`, default: `False` ) – Disable all logging (but still exit with status code "1" upon detecting lint violations).

Source code in `src/duty/_internal/tools/_ruff.py`

```
@classmethod
def linter(
    cls,
    *,
    output_format: str | None = None,
    verbose: bool = False,
    quiet: bool = False,
    silent: bool = False,
) -> ruff:
    """List all supported upstream linters.

    Parameters:
        output_format: Output format (default: pretty) (possible values: text, json, pretty).
        verbose: Enable verbose logging.
        quiet: Print lint violations, but nothing else.
        silent: Disable all logging (but still exit with status code "1" upon detecting lint violations).
    """
    cli_args = ["linter"]

    if output_format:
        cli_args.append("--format")
        cli_args.append(output_format)

    if verbose:
        cli_args.append("--verbose")

    if quiet:
        cli_args.append("--quiet")

    if silent:
        cli_args.append("--silent")

    return cls(cli_args)

```

#### rule

```
rule(
    rule: str,
    *,
    output_format: str | None = None,
    verbose: bool = False,
    quiet: bool = False,
    silent: bool = False,
) -> ruff

```

Explain a rule.

Parameters:

- **`rule`** (`str`) – A rule code, or --all.
- **`output_format`** (`str | None`, default: `None` ) – Output format (default: pretty, possible values: text, json, pretty).
- **`verbose`** (`bool`, default: `False` ) – Enable verbose logging.
- **`quiet`** (`bool`, default: `False` ) – Print lint violations, but nothing else.
- **`silent`** (`bool`, default: `False` ) – Disable all logging (but still exit with status code "1" upon detecting lint violations).

Source code in `src/duty/_internal/tools/_ruff.py`

```
@classmethod
def rule(
    cls,
    rule: str,
    *,
    output_format: str | None = None,
    verbose: bool = False,
    quiet: bool = False,
    silent: bool = False,
) -> ruff:
    """Explain a rule.

    Parameters:
        rule: A rule code, or `--all`.
        output_format: Output format (default: pretty, possible values: text, json, pretty).
        verbose: Enable verbose logging.
        quiet: Print lint violations, but nothing else.
        silent: Disable all logging (but still exit with status code "1" upon detecting lint violations).
    """
    cli_args = ["rule", rule]

    if output_format:
        cli_args.append("--format")
        cli_args.append(output_format)

    if verbose:
        cli_args.append("--verbose")

    if quiet:
        cli_args.append("--quiet")

    if silent:
        cli_args.append("--silent")

    return cls(cli_args)

```

### safety

```
safety(
    cli_args: list[str] | None = None,
    py_args: dict[str, Any] | None = None,
)

```

Bases: `Tool`

Call [Safety](https://github.com/pyupio/safety).

Parameters:

- **`cli_args`** (`list[str] | None`, default: `None` ) – Initial command-line arguments. Use add_args() to add more.
- **`py_args`** (`dict[str, Any] | None`, default: `None` ) – Python arguments. Your __call__ method will be able to access these arguments as self.py_args.

Methods:

- **`__call__`** – Run the command.
- **`add_args`** – Append CLI arguments.
- **`check`** – Run the safety check command.

Attributes:

- **`cli_args`** (`list[str]`) – Registered command-line arguments.
- **`cli_command`** (`str`) – The equivalent CLI command.
- **`cli_name`** – The name of the executable on PATH.
- **`py_args`** (`dict[str, Any]`) – Registered Python arguments.

Source code in `src/duty/_internal/tools/_base.py`

```
def __init__(
    self,
    cli_args: list[str] | None = None,
    py_args: dict[str, Any] | None = None,
) -> None:
    """Initialize the tool.

    Parameters:
        cli_args: Initial command-line arguments. Use `add_args()` to add more.
        py_args: Python arguments. Your `__call__` method will be able to access
            these arguments as `self.py_args`.
    """
    self.cli_args: list[str] = cli_args or []
    """Registered command-line arguments."""
    self.py_args: dict[str, Any] = py_args or {}
    """Registered Python arguments."""

```

#### cli_args

```
cli_args: list[str] = cli_args or []

```

Registered command-line arguments.

#### cli_command

```
cli_command: str

```

The equivalent CLI command.

#### cli_name

```
cli_name = 'safety'

```

The name of the executable on PATH.

#### py_args

```
py_args: dict[str, Any] = py_args or {}

```

Registered Python arguments.

#### __call__

```
__call__() -> bool

```

Run the command.

Returns:

- `bool` – False when vulnerabilities are found.

Source code in `src/duty/_internal/tools/_safety.py`

```
def __call__(self) -> bool:
    """Run the command.

    Returns:
        False when vulnerabilities are found.
    """
    requirements = self.py_args["requirements"]
    ignore_vulns = self.py_args["ignore_vulns"]
    formatter = self.py_args["formatter"]
    full_report = self.py_args["full_report"]

    # set default parameter values
    ignore_vulns = ignore_vulns or {}

    # undo possible patching
    # see https://github.com/pyupio/safety/issues/348
    for module in sys.modules:
        if module.startswith("safety.") or module == "safety":
            del sys.modules[module]

    importlib.invalidate_caches()

    # reload original, unpatched safety
    from safety.formatter import SafetyFormatter  # noqa: PLC0415
    from safety.safety import calculate_remediations, check  # noqa: PLC0415
    from safety.util import read_requirements  # noqa: PLC0415

    # check using safety as a library
    if isinstance(requirements, (list, tuple, set)):
        requirements = "\n".join(requirements)
    packages = list(read_requirements(StringIO(cast("str", requirements))))

    # TODO: Safety 3 support, merge once support for v2 is dropped.
    check_kwargs = {"packages": packages, "ignore_vulns": ignore_vulns}
    try:
        from safety.auth.cli_utils import build_client_session  # noqa: PLC0415

        client_session, _ = build_client_session()
        check_kwargs["session"] = client_session
    except ImportError:
        pass

    vulns, db_full = check(**check_kwargs)
    remediations = calculate_remediations(vulns, db_full)
    output_report = SafetyFormatter(formatter).render_vulnerabilities(
        announcements=[],
        vulnerabilities=vulns,
        remediations=remediations,
        full=full_report,
        packages=packages,
    )

    # print report, return status
    if vulns:
        print(output_report)  # noqa: T201
        return False
    return True

```

#### add_args

```
add_args(*args: str) -> Self

```

Append CLI arguments.

Source code in `src/duty/_internal/tools/_base.py`

```
def add_args(self, *args: str) -> Self:
    """Append CLI arguments."""
    self.cli_args.extend(args)
    return self

```

#### check

```
check(
    requirements: str | Sequence[str],
    *,
    ignore_vulns: dict[str, str] | None = None,
    formatter: Literal["json", "bare", "text"] = "text",
    full_report: bool = True,
) -> safety

```

Run the safety check command.

This function makes sure we load the original, unpatched version of safety.

Parameters:

- **`requirements`** (`str | Sequence[str]`) – Python "requirements" (list of pinned dependencies).
- **`ignore_vulns`** (`dict[str, str] | None`, default: `None` ) – Vulnerabilities to ignore.
- **`formatter`** (`Literal['json', 'bare', 'text']`, default: `'text'` ) – Report format.
- **`full_report`** (`bool`, default: `True` ) – Whether to output a full report.

Returns:

- `safety` – Success/failure.

Source code in `src/duty/_internal/tools/_safety.py`

```
@classmethod
def check(
    cls,
    requirements: str | Sequence[str],
    *,
    ignore_vulns: dict[str, str] | None = None,
    formatter: Literal["json", "bare", "text"] = "text",
    full_report: bool = True,
) -> safety:
    """Run the safety check command.

    This function makes sure we load the original, unpatched version of safety.

    Parameters:
        requirements: Python "requirements" (list of pinned dependencies).
        ignore_vulns: Vulnerabilities to ignore.
        formatter: Report format.
        full_report: Whether to output a full report.

    Returns:
        Success/failure.
    """
    return cls(py_args=dict(locals()))

```

### ssort

```
ssort(
    *files: str,
    diff: bool | None = None,
    check: bool | None = None,
)

```

Bases: `Tool`

Call [ssort](https://github.com/bwhmather/ssort).

Parameters:

- **`*files`** (`str`, default: `()` ) – Files to format.
- **`diff`** (`bool | None`, default: `None` ) – Prints a diff of all changes ssort would make to a file.
- **`check`** (`bool | None`, default: `None` ) – Check the file for unsorted statements. Returns 0 if nothing needs to be changed. Otherwise returns 1.

Methods:

- **`__call__`** – Run the command.
- **`add_args`** – Append CLI arguments.

Attributes:

- **`cli_args`** (`list[str]`) – Registered command-line arguments.
- **`cli_command`** (`str`) – The equivalent CLI command.
- **`cli_name`** – The name of the executable on PATH.
- **`py_args`** (`dict[str, Any]`) – Registered Python arguments.

Source code in `src/duty/_internal/tools/_ssort.py`

```
def __init__(
    self,
    *files: str,
    diff: bool | None = None,
    check: bool | None = None,
) -> None:
    """Run `ssort`.

    Parameters:
        *files: Files to format.
        diff: Prints a diff of all changes ssort would make to a file.
        check: Check the file for unsorted statements. Returns 0 if nothing needs to be changed. Otherwise returns 1.
    """
    cli_args = list(files)

    if diff:
        cli_args.append("--diff")

    if check:
        cli_args.append("--check")

```

#### cli_args

```
cli_args: list[str] = cli_args or []

```

Registered command-line arguments.

#### cli_command

```
cli_command: str

```

The equivalent CLI command.

#### cli_name

```
cli_name = 'ssort'

```

The name of the executable on PATH.

#### py_args

```
py_args: dict[str, Any] = py_args or {}

```

Registered Python arguments.

#### __call__

```
__call__() -> None

```

Run the command.

Returns:

- `None` – The exit code of the command.

Source code in `src/duty/_internal/tools/_ssort.py`

```
def __call__(self) -> None:
    """Run the command.

    Returns:
        The exit code of the command.
    """
    from ssort._main import main as run_ssort  # noqa: PLC0415

    old_sys_argv = sys.argv
    sys.argv = ["ssort", *self.cli_args]
    try:
        run_ssort()
    finally:
        sys.argv = old_sys_argv

```

#### add_args

```
add_args(*args: str) -> Self

```

Append CLI arguments.

Source code in `src/duty/_internal/tools/_base.py`

```
def add_args(self, *args: str) -> Self:
    """Append CLI arguments."""
    self.cli_args.extend(args)
    return self

```

### twine

```
twine(
    cli_args: list[str] | None = None,
    py_args: dict[str, Any] | None = None,
)

```

Bases: `Tool`

Call [Twine](https://github.com/pypa/twine).

Parameters:

- **`cli_args`** (`list[str] | None`, default: `None` ) – Initial command-line arguments. Use add_args() to add more.
- **`py_args`** (`dict[str, Any] | None`, default: `None` ) – Python arguments. Your __call__ method will be able to access these arguments as self.py_args.

Methods:

- **`__call__`** – Run the command.
- **`add_args`** – Append CLI arguments.
- **`check`** – Checks whether your distribution's long description will render correctly on PyPI.
- **`register`** – Pre-register a name with a repository before uploading a distribution.
- **`upload`** – Uploads one or more distributions to a repository.

Attributes:

- **`cli_args`** (`list[str]`) – Registered command-line arguments.
- **`cli_command`** (`str`) – The equivalent CLI command.
- **`cli_name`** – The name of the executable on PATH.
- **`py_args`** (`dict[str, Any]`) – Registered Python arguments.

Source code in `src/duty/_internal/tools/_base.py`

```
def __init__(
    self,
    cli_args: list[str] | None = None,
    py_args: dict[str, Any] | None = None,
) -> None:
    """Initialize the tool.

    Parameters:
        cli_args: Initial command-line arguments. Use `add_args()` to add more.
        py_args: Python arguments. Your `__call__` method will be able to access
            these arguments as `self.py_args`.
    """
    self.cli_args: list[str] = cli_args or []
    """Registered command-line arguments."""
    self.py_args: dict[str, Any] = py_args or {}
    """Registered Python arguments."""

```

#### cli_args

```
cli_args: list[str] = cli_args or []

```

Registered command-line arguments.

#### cli_command

```
cli_command: str

```

The equivalent CLI command.

#### cli_name

```
cli_name = 'twine'

```

The name of the executable on PATH.

#### py_args

```
py_args: dict[str, Any] = py_args or {}

```

Registered Python arguments.

#### __call__

```
__call__() -> Any

```

Run the command.

Returns:

- `Any` – The return value of the corresponding Twine command / entrypoint.

Source code in `src/duty/_internal/tools/_twine.py`

```
def __call__(self) -> Any:
    """Run the command.

    Returns:
        The return value of the corresponding Twine command / entrypoint.
    """
    from twine.cli import dispatch as run_twine  # noqa: PLC0415

    return run_twine(self.cli_args)

```

#### add_args

```
add_args(*args: str) -> Self

```

Append CLI arguments.

Source code in `src/duty/_internal/tools/_base.py`

```
def add_args(self, *args: str) -> Self:
    """Append CLI arguments."""
    self.cli_args.extend(args)
    return self

```

#### check

```
check(
    *dists: str,
    strict: bool = False,
    version: bool = False,
    no_color: bool = False,
) -> twine

```

Checks whether your distribution's long description will render correctly on PyPI.

Parameters:

- **`dists`** (`str`, default: `()` ) – The distribution files to check, usually dist/\*.
- **`strict`** (`bool`, default: `False` ) – Fail on warnings.
- **`version`** (`bool`, default: `False` ) – Show program's version number and exit.
- **`no_color`** (`bool`, default: `False` ) – Disable colored output.

Source code in `src/duty/_internal/tools/_twine.py`

```
@classmethod
def check(
    cls,
    *dists: str,
    strict: bool = False,
    version: bool = False,
    no_color: bool = False,
) -> twine:
    """Checks whether your distribution's long description will render correctly on PyPI.

    Parameters:
        dists: The distribution files to check, usually `dist/*`.
        strict: Fail on warnings.
        version: Show program's version number and exit.
        no_color: Disable colored output.
    """
    cli_args = ["check", *dists]

    if version:
        cli_args.append("--version")

    if no_color:
        cli_args.append("--no-color")

    if strict is True:
        cli_args.append("--strict")

    return cls(cli_args)

```

#### register

```
register(
    package: str,
    *,
    repository: str = "pypi",
    repository_url: str | None = None,
    attestations: bool = False,
    sign: bool = False,
    sign_with: str | None = None,
    identity: str | None = None,
    username: str | None = None,
    password: str | None = None,
    non_interactive: bool = False,
    comment: str | None = None,
    config_file: str | None = None,
    skip_existing: bool = False,
    cert: str | None = None,
    client_cert: str | None = None,
    verbose: bool = False,
    disable_progress_bar: bool = False,
    version: bool = False,
    no_color: bool = False,
) -> twine

```

Pre-register a name with a repository before uploading a distribution.

Pre-registration is not supported on PyPI, so the register command is only necessary if you are using a different repository that requires it.

Parameters:

- **`package`** (`str`) – File from which we read the package metadata.
- **`repository`** (`str`, default: `'pypi'` ) – The repository (package index) to upload the package to. Should be a section in the config file (default: pypi). Can also be set via TWINE_REPOSITORY environment variable.
- **`repository_url`** (`str | None`, default: `None` ) – The repository (package index) URL to upload the package to. This overrides --repository. Can also be set via TWINE_REPOSITORY_URL environment variable.
- **`attestations`** (`bool`, default: `False` ) – Upload each file's associated attestations.
- **`sign`** (`bool`, default: `False` ) – Sign files to upload using GPG.
- **`sign_with`** (`str | None`, default: `None` ) – GPG program used to sign uploads (default: gpg).
- **`identity`** (`str | None`, default: `None` ) – GPG identity used to sign files.
- **`username`** (`str | None`, default: `None` ) – The username to authenticate to the repository (package index) as. Can also be set via TWINE_USERNAME environment variable.
- **`password`** (`str | None`, default: `None` ) – The password to authenticate to the repository (package index) with. Can also be set via TWINE_PASSWORD environment variable.
- **`non_interactive`** (`bool`, default: `False` ) – Do not interactively prompt for username/password if the required credentials are missing. Can also be set via TWINE_NON_INTERACTIVE environment variable.
- **`comment`** (`str | None`, default: `None` ) – The comment to include with the distribution file.
- **`config_file`** (`str | None`, default: `None` ) – The .pypirc config file to use.
- **`skip_existing`** (`bool`, default: `False` ) – Continue uploading files if one already exists. Only valid when uploading to PyPI. Other implementations may not support this.
- **`cert`** (`str | None`, default: `None` ) – Path to alternate CA bundle (can also be set via TWINE_CERT environment variable).
- **`client_cert`** (`str | None`, default: `None` ) – Path to SSL client certificate, a single file containing the private key and the certificate in PEM format.
- **`verbose`** (`bool`, default: `False` ) – Show verbose output.
- **`disable_progress_bar`** (`bool`, default: `False` ) – Disable the progress bar.
- **`version`** (`bool`, default: `False` ) – Show program's version number and exit.
- **`no_color`** (`bool`, default: `False` ) – Disable colored output.

Source code in `src/duty/_internal/tools/_twine.py`

```
@classmethod
def register(
    cls,
    package: str,
    *,
    repository: str = "pypi",
    repository_url: str | None = None,
    attestations: bool = False,
    sign: bool = False,
    sign_with: str | None = None,
    identity: str | None = None,
    username: str | None = None,
    password: str | None = None,
    non_interactive: bool = False,
    comment: str | None = None,
    config_file: str | None = None,
    skip_existing: bool = False,
    cert: str | None = None,
    client_cert: str | None = None,
    verbose: bool = False,
    disable_progress_bar: bool = False,
    version: bool = False,
    no_color: bool = False,
) -> twine:
    """Pre-register a name with a repository before uploading a distribution.

    Pre-registration is not supported on PyPI, so the register command
    is only necessary if you are using a different repository that requires it.

    Parameters:
        package: File from which we read the package metadata.
        repository: The repository (package index) to upload the package to.
            Should be a section in the config file (default: `pypi`).
            Can also be set via `TWINE_REPOSITORY` environment variable.
        repository_url: The repository (package index) URL to upload the package to. This overrides `--repository`.
            Can also be set via `TWINE_REPOSITORY_URL` environment variable.
        attestations: Upload each file's associated attestations.
        sign: Sign files to upload using GPG.
        sign_with: GPG program used to sign uploads (default: `gpg`).
        identity: GPG identity used to sign files.
        username: The username to authenticate to the repository (package index) as.
            Can also be set via `TWINE_USERNAME` environment variable.
        password: The password to authenticate to the repository (package index) with.
            Can also be set via `TWINE_PASSWORD` environment variable.
        non_interactive: Do not interactively prompt for username/password if the required credentials are missing.
            Can also be set via `TWINE_NON_INTERACTIVE` environment variable.
        comment: The comment to include with the distribution file.
        config_file: The `.pypirc` config file to use.
        skip_existing: Continue uploading files if one already exists.
            Only valid when uploading to PyPI. Other implementations may not support this.
        cert: Path to alternate CA bundle (can also be set via `TWINE_CERT` environment variable).
        client_cert: Path to SSL client certificate, a single file containing the private key and the certificate in PEM format.
        verbose: Show verbose output.
        disable_progress_bar: Disable the progress bar.
        version: Show program's version number and exit.
        no_color: Disable colored output.
    """
    cli_args = ["register", package]

    if version:
        cli_args.append("--version")

    if no_color:
        cli_args.append("--no-color")

    if repository:
        cli_args.append("--repository")
        cli_args.append(repository)

    if repository_url:
        cli_args.append("--repository-url")
        cli_args.append(repository_url)

    if attestations:
        cli_args.append("--attestations")

    if sign:
        cli_args.append("--sign")

    if sign_with:
        cli_args.append("--sign-with")
        cli_args.append(sign_with)

    if identity:
        cli_args.append("--identity")
        cli_args.append(identity)

    if username:
        cli_args.append("--username")
        cli_args.append(username)

    if password:
        cli_args.append("--password")
        cli_args.append(password)

    if non_interactive:
        cli_args.append("--non-interactive")

    if comment:
        cli_args.append("--repository")

    if config_file:
        cli_args.append("--config-file")
        cli_args.append(config_file)

    if skip_existing:
        cli_args.append("--skip-existing")

    if cert:
        cli_args.append("--cert")
        cli_args.append(cert)

    if client_cert:
        cli_args.append("--client-cert")
        cli_args.append(client_cert)

    if verbose:
        cli_args.append("--verbose")

    if disable_progress_bar:
        cli_args.append("--disable-progress-bar")

    return cls(cli_args)

```

#### upload

```
upload(
    *dists: str,
    repository: str = "pypi",
    repository_url: str | None = None,
    attestations: bool = False,
    sign: bool = False,
    sign_with: str | None = None,
    identity: str | None = None,
    username: str | None = None,
    password: str | None = None,
    non_interactive: bool = False,
    comment: str | None = None,
    config_file: str | None = None,
    skip_existing: bool = False,
    cert: str | None = None,
    client_cert: str | None = None,
    verbose: bool = False,
    disable_progress_bar: bool = False,
    version: bool = False,
    no_color: bool = False,
) -> twine

```

Uploads one or more distributions to a repository.

Parameters:

- **`dists`** (`str`, default: `()` ) – The distribution files to check, usually dist/\*.
- **`repository`** (`str`, default: `'pypi'` ) – The repository (package index) to upload the package to. Should be a section in the config file (default: pypi). Can also be set via TWINE_REPOSITORY environment variable.
- **`repository_url`** (`str | None`, default: `None` ) – The repository (package index) URL to upload the package to. This overrides --repository. Can also be set via TWINE_REPOSITORY_URL environment variable.
- **`attestations`** (`bool`, default: `False` ) – Upload each file's associated attestations.
- **`sign`** (`bool`, default: `False` ) – Sign files to upload using GPG.
- **`sign_with`** (`str | None`, default: `None` ) – GPG program used to sign uploads (default: gpg).
- **`identity`** (`str | None`, default: `None` ) – GPG identity used to sign files.
- **`username`** (`str | None`, default: `None` ) – The username to authenticate to the repository (package index) as. Can also be set via TWINE_USERNAME environment variable.
- **`password`** (`str | None`, default: `None` ) – The password to authenticate to the repository (package index) with. Can also be set via TWINE_PASSWORD environment variable.
- **`non_interactive`** (`bool`, default: `False` ) – Do not interactively prompt for username/password if the required credentials are missing. Can also be set via TWINE_NON_INTERACTIVE environment variable.
- **`comment`** (`str | None`, default: `None` ) – The comment to include with the distribution file.
- **`config_file`** (`str | None`, default: `None` ) – The .pypirc config file to use.
- **`skip_existing`** (`bool`, default: `False` ) – Continue uploading files if one already exists. Only valid when uploading to PyPI. Other implementations may not support this.
- **`cert`** (`str | None`, default: `None` ) – Path to alternate CA bundle (can also be set via TWINE_CERT environment variable).
- **`client_cert`** (`str | None`, default: `None` ) – Path to SSL client certificate, a single file containing the private key and the certificate in PEM format.
- **`verbose`** (`bool`, default: `False` ) – Show verbose output.
- **`disable_progress_bar`** (`bool`, default: `False` ) – Disable the progress bar.
- **`version`** (`bool`, default: `False` ) – Show program's version number and exit.
- **`no_color`** (`bool`, default: `False` ) – Disable colored output.

Source code in `src/duty/_internal/tools/_twine.py`

```
@classmethod
def upload(
    cls,
    *dists: str,
    repository: str = "pypi",
    repository_url: str | None = None,
    attestations: bool = False,
    sign: bool = False,
    sign_with: str | None = None,
    identity: str | None = None,
    username: str | None = None,
    password: str | None = None,
    non_interactive: bool = False,
    comment: str | None = None,
    config_file: str | None = None,
    skip_existing: bool = False,
    cert: str | None = None,
    client_cert: str | None = None,
    verbose: bool = False,
    disable_progress_bar: bool = False,
    version: bool = False,
    no_color: bool = False,
) -> twine:
    """Uploads one or more distributions to a repository.

    Parameters:
        dists: The distribution files to check, usually `dist/*`.
        repository: The repository (package index) to upload the package to.
            Should be a section in the config file (default: `pypi`).
            Can also be set via `TWINE_REPOSITORY` environment variable.
        repository_url: The repository (package index) URL to upload the package to. This overrides `--repository`.
            Can also be set via `TWINE_REPOSITORY_URL` environment variable.
        attestations: Upload each file's associated attestations.
        sign: Sign files to upload using GPG.
        sign_with: GPG program used to sign uploads (default: `gpg`).
        identity: GPG identity used to sign files.
        username: The username to authenticate to the repository (package index) as.
            Can also be set via `TWINE_USERNAME` environment variable.
        password: The password to authenticate to the repository (package index) with.
            Can also be set via `TWINE_PASSWORD` environment variable.
        non_interactive: Do not interactively prompt for username/password if the required credentials are missing.
            Can also be set via `TWINE_NON_INTERACTIVE` environment variable.
        comment: The comment to include with the distribution file.
        config_file: The `.pypirc` config file to use.
        skip_existing: Continue uploading files if one already exists.
            Only valid when uploading to PyPI. Other implementations may not support this.
        cert: Path to alternate CA bundle (can also be set via `TWINE_CERT` environment variable).
        client_cert: Path to SSL client certificate, a single file containing the private key and the certificate in PEM format.
        verbose: Show verbose output.
        disable_progress_bar: Disable the progress bar.
        version: Show program's version number and exit.
        no_color: Disable colored output.
    """
    cli_args = ["upload", *dists]

    if version:
        cli_args.append("--version")

    if no_color:
        cli_args.append("--no-color")

    if repository:
        cli_args.append("--repository")
        cli_args.append(repository)

    if repository_url:
        cli_args.append("--repository-url")
        cli_args.append(repository_url)

    if attestations:
        cli_args.append("--attestations")

    if sign:
        cli_args.append("--sign")

    if sign_with:
        cli_args.append("--sign-with")
        cli_args.append(sign_with)

    if identity:
        cli_args.append("--identity")
        cli_args.append(identity)

    if username:
        cli_args.append("--username")
        cli_args.append(username)

    if password:
        cli_args.append("--password")
        cli_args.append(password)

    if non_interactive:
        cli_args.append("--non-interactive")

    if comment:
        cli_args.append("--repository")

    if config_file:
        cli_args.append("--config-file")
        cli_args.append(config_file)

    if skip_existing:
        cli_args.append("--skip-existing")

    if cert:
        cli_args.append("--cert")
        cli_args.append(cert)

    if client_cert:
        cli_args.append("--client-cert")
        cli_args.append(client_cert)

    if verbose:
        cli_args.append("--verbose")

    if disable_progress_bar:
        cli_args.append("--disable-progress-bar")

    return cls(cli_args)

```

### yore

```
yore(
    cli_args: list[str] | None = None,
    py_args: dict[str, Any] | None = None,
)

```

Bases: `Tool`

Call [Yore](https://github.com/pawamoy/yore).

Parameters:

- **`cli_args`** (`list[str] | None`, default: `None` ) – Initial command-line arguments. Use add_args() to add more.
- **`py_args`** (`dict[str, Any] | None`, default: `None` ) – Python arguments. Your __call__ method will be able to access these arguments as self.py_args.

Methods:

- **`__call__`** – Run the command.
- **`add_args`** – Append CLI arguments.
- **`check`** – Check Yore comments against Python EOL dates or the provided next version of your project.
- **`fix`** – Fix your code by transforming it according to the Yore comments.

Attributes:

- **`cli_args`** (`list[str]`) – Registered command-line arguments.
- **`cli_command`** (`str`) – The equivalent CLI command.
- **`cli_name`** – The name of the executable on PATH.
- **`py_args`** (`dict[str, Any]`) – Registered Python arguments.

Source code in `src/duty/_internal/tools/_base.py`

```
def __init__(
    self,
    cli_args: list[str] | None = None,
    py_args: dict[str, Any] | None = None,
) -> None:
    """Initialize the tool.

    Parameters:
        cli_args: Initial command-line arguments. Use `add_args()` to add more.
        py_args: Python arguments. Your `__call__` method will be able to access
            these arguments as `self.py_args`.
    """
    self.cli_args: list[str] = cli_args or []
    """Registered command-line arguments."""
    self.py_args: dict[str, Any] = py_args or {}
    """Registered Python arguments."""

```

#### cli_args

```
cli_args: list[str] = cli_args or []

```

Registered command-line arguments.

#### cli_command

```
cli_command: str

```

The equivalent CLI command.

#### cli_name

```
cli_name = 'yore'

```

The name of the executable on PATH.

#### py_args

```
py_args: dict[str, Any] = py_args or {}

```

Registered Python arguments.

#### __call__

```
__call__() -> int

```

Run the command.

Returns:

- `int` – The exit code of the command.

Source code in `src/duty/_internal/tools/_yore.py`

```
def __call__(self) -> int:
    """Run the command.

    Returns:
        The exit code of the command.
    """
    from yore import main as run_yore  # noqa: PLC0415

    return run_yore(self.cli_args)

```

#### add_args

```
add_args(*args: str) -> Self

```

Append CLI arguments.

Source code in `src/duty/_internal/tools/_base.py`

```
def add_args(self, *args: str) -> Self:
    """Append CLI arguments."""
    self.cli_args.extend(args)
    return self

```

#### check

```
check(
    *paths: str,
    bump: str | None = None,
    eol_within: str | None = None,
    bol_within: str | None = None,
) -> yore

```

Check Yore comments against Python EOL dates or the provided next version of your project.

Parameters:

- **`paths`** (`str`, default: `()` ) – Path to files or directories to check.
- **`bump`** (`str | None`, default: `None` ) – The next version of your project.
- **`eol_within`** (`str | None`, default: `None` ) – The time delta to start checking before the End of Life of a Python version. It is provided in a human-readable format, like 2 weeks or 1 month. Spaces are optional, and the unit can be shortened to a single letter: d for days, w for weeks, m for months, and y for years.
- **`bol_within`** (`str | None`, default: `None` ) – The time delta to start checking before the Beginning of Life of a Python version. It is provided in a human-readable format, like 2 weeks or 1 month. Spaces are optional, and the unit can be shortened to a single letter: d for days, w for weeks, m for months, and y for years.

Source code in `src/duty/_internal/tools/_yore.py`

```
@classmethod
def check(
    cls,
    *paths: str,
    bump: str | None = None,
    eol_within: str | None = None,
    bol_within: str | None = None,
) -> yore:
    """Check Yore comments against Python EOL dates or the provided next version of your project.

    Parameters:
        paths: Path to files or directories to check.
        bump: The next version of your project.
        eol_within: The time delta to start checking before the End of Life of a Python version.
            It is provided in a human-readable format, like `2 weeks` or `1 month`.
            Spaces are optional, and the unit can be shortened to a single letter:
            `d` for days, `w` for weeks, `m` for months, and `y` for years.
        bol_within: The time delta to start checking before the Beginning of Life of a Python version.
            It is provided in a human-readable format, like `2 weeks` or `1 month`.
            Spaces are optional, and the unit can be shortened to a single letter:
            `d` for days, `w` for weeks, `m` for months, and `y` for years.
    """
    cli_args = ["check", *paths]

    if bump:
        cli_args.append("--bump")
        cli_args.append(bump)

    if eol_within:
        cli_args.append("--eol-within")
        cli_args.append(eol_within)

    if bol_within:
        cli_args.append("--bol-within")
        cli_args.append(bol_within)

    return cls(cli_args)

```

#### fix

```
fix(
    *paths: str,
    bump: str | None = None,
    eol_within: str | None = None,
    bol_within: str | None = None,
) -> yore

```

Fix your code by transforming it according to the Yore comments.

Parameters:

- **`paths`** (`str`, default: `()` ) – Path to files or directories to fix.
- **`bump`** (`str | None`, default: `None` ) – The next version of your project.
- **`eol_within`** (`str | None`, default: `None` ) – The time delta to start fixing before the End of Life of a Python version. It is provided in a human-readable format, like 2 weeks or 1 month. Spaces are optional, and the unit can be shortened to a single letter: d for days, w for weeks, m for months, and y for years.
- **`bol_within`** (`str | None`, default: `None` ) – The time delta to start fixing before the Beginning of Life of a Python version. It is provided in a human-readable format, like 2 weeks or 1 month. Spaces are optional, and the unit can be shortened to a single letter: d for days, w for weeks, m for months, and y for years.

Source code in `src/duty/_internal/tools/_yore.py`

```
@classmethod
def fix(
    cls,
    *paths: str,
    bump: str | None = None,
    eol_within: str | None = None,
    bol_within: str | None = None,
) -> yore:
    """Fix your code by transforming it according to the Yore comments.

    Parameters:
        paths: Path to files or directories to fix.
        bump: The next version of your project.
        eol_within: The time delta to start fixing before the End of Life of a Python version.
            It is provided in a human-readable format, like `2 weeks` or `1 month`.
            Spaces are optional, and the unit can be shortened to a single letter:
            `d` for days, `w` for weeks, `m` for months, and `y` for years.
        bol_within: The time delta to start fixing before the Beginning of Life of a Python version.
            It is provided in a human-readable format, like `2 weeks` or `1 month`.
            Spaces are optional, and the unit can be shortened to a single letter:
            `d` for days, `w` for weeks, `m` for months, and `y` for years.
    """
    cli_args = ["fix", *paths]

    if bump:
        cli_args.append("--bump")
        cli_args.append(bump)

    if eol_within:
        cli_args.append("--eol-within")
        cli_args.append(eol_within)

    if bol_within:
        cli_args.append("--bol-within")
        cli_args.append(bol_within)

    return cls(cli_args)

```

## validation

Deprecated. Import from `duty` directly.
