from __future__ import annotations

import inspect
import sys
from copy import deepcopy
from importlib import util as importlib_util
from typing import Any, Callable, ClassVar, Union

from duty._internal.context import Context

DutyListType = list[Union[str, Callable, "Duty"]]
"""Type of a list of duties, which can be a list of strings, callables, or Duty instances."""
default_duties_file = "duties.py"
"""Default path to the duties file, relative to the current working directory."""


class Duty:
    """The main duty class."""

    default_options: ClassVar[dict[str, Any]] = {}
    """Default options used to create the context instance."""

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

    @property
    def context(self) -> Context:
        """Return a new context instance.

        Returns:
            A new context instance.
        """
        return Context(self.options, self.options_override)

    def run(self, *args: Any, **kwargs: Any) -> None:
        """Run the duty.

        This is just a shortcut for `duty(duty.context, *args, **kwargs)`.

        Parameters:
            args: Positional arguments passed to the function.
            kwargs: Keyword arguments passed to the function.
        """
        self(self.context, *args, **kwargs)

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


class Collection:
    """A collection of duties.

    Attributes:
        path: The path to the duties file.
        duties: The list of duties.
        aliases: A dictionary of aliases pointing to their respective duties.
    """

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

    def clear(self) -> None:
        """Clear the collection."""
        self.duties.clear()
        self.aliases.clear()

    def names(self) -> list[str]:
        """Return the list of duties names and aliases.

        Returns:
            The list of duties names and aliases.
        """
        return list(self.duties.keys()) + list(self.aliases.keys())

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
