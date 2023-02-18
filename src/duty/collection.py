"""Module containing all the logic."""
from __future__ import annotations

import inspect
from copy import deepcopy
from importlib import util as importlib_util
from typing import Any, Callable, List, Union

from duty.context import Context

DutyListType = List[Union[str, Callable, "Duty"]]
default_duties_file = "duties.py"


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
        self.duties: dict[str, Duty] = {}
        self.aliases: dict[str, Duty] = {}

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
        longest_name = max(max(len(name) for name in self.duties), 20)
        for name, duty in self.duties.items():
            description = duty.description.split("\n")[0]
            lines.append(f"{name:{longest_name}}  {description}")
        return "\n".join(lines)

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
            spec.loader.exec_module(duties)  # type: ignore[union-attr]
            declared_duties = inspect.getmembers(duties, lambda member: isinstance(member, Duty))
            for _, duty in declared_duties:
                self.add(duty)

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


class Duty:
    """The main duty class."""

    default_options: dict[str, Any] = {}

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
        self.description = description
        self.function = function
        self.aliases = aliases or set()
        self.pre = pre or []
        self.post = post or []
        self.options = opts or self.default_options
        self.options_override: dict = {}

        self.collection: Collection | None = None
        if collection:
            collection.add(self)

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
