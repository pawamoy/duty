"""Module containing all the logic."""

import inspect
from copy import deepcopy
from importlib import util as importlib_util
from typing import Any, Callable, Dict, List, Optional, Union

from duty.context import Context

DutyListType = List[Union[str, Callable, "Duty"]]
default_duties_file = "duties.py"


class Collection:
    """
    A collection of duties.

    Attributes:
        path: The path to the duties file.
        duties: The list of duties.
        aliases: A dictionary of aliases pointing to their respective duties.
    """

    def __init__(self, path: str = default_duties_file):
        """
        Initialize the collection.

        Arguments:
            path: The path to the duties file.
        """
        self.path = path
        self.duties: Dict[str, Duty] = {}
        self.aliases: Dict[str, Duty] = {}

    def clear(self) -> None:
        """Clear the collection."""
        self.duties.clear()
        self.aliases.clear()

    def names(self) -> List[str]:
        """
        Return the list of duties names and aliases.

        Returns:
            The list of duties names and aliases.
        """
        return list(self.duties.keys()) + list(self.aliases.keys())

    def get(self, name_or_alias: str) -> "Duty":
        """
        Get a duty by its name or alias.

        Arguments:
            name_or_alias: The name or alias of the duty.

        Returns:
            A duty.
        """
        try:
            return self.duties[name_or_alias]
        except KeyError:
            return self.aliases[name_or_alias]

    def show(self) -> None:
        """Show duties."""
        for name, duty in self.duties.items():
            description = duty.description.split("\n")[0]
            print(f"{name:20} - {description}")  # noqa: WPS421 (print)

    def load(self, path: Optional[str] = None) -> None:
        """
        Load duties from a Python file.

        Arguments:
            path: The path to the Python file to load.
                Uses the collection's path by default.
        """
        path = path or self.path
        spec = importlib_util.spec_from_file_location("duty.duties", path)
        duties = importlib_util.module_from_spec(spec)
        spec.loader.exec_module(duties)  # type: ignore
        for _, duty in inspect.getmembers(duties, lambda member: isinstance(member, Duty)):
            self.add(duty)

    def add(self, duty: "Duty") -> None:
        """
        Add a duty to the collection.

        Arguments:
            duty: The duty to add.
        """
        if duty.collection is not None:
            duty = deepcopy(duty)
        duty.collection = self  # type: ignore
        self.duties[duty.name] = duty
        for alias in duty.aliases:
            self.aliases[alias] = duty


class Duty:
    """The main duty class."""

    default_options: Dict[str, Any] = {}

    def __init__(
        self,
        name: str,
        description: str,
        function: Callable,
        collection: Optional[Collection] = None,
        aliases: Optional[set] = None,
        pre: Optional[DutyListType] = None,
        post: Optional[DutyListType] = None,
        opts: Dict[str, Any] = None,
    ) -> None:
        """
        Initialize the duty.

        Arguments:
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

        self.collection = None
        if collection:
            collection.add(self)

    def __call__(self, *args, **kwargs) -> None:
        """
        Run the duty function.

        Arguments:
            args: Positional arguments passed to the function.
            kwargs: Keyword arguments passed to the function.
        """
        self.run(*args, **kwargs)

    def __repr__(self):
        return f"Duty(name={self.name!r}, options={self.options!r})"

    def __str__(self):
        return self.name

    @property
    def context(self) -> Context:
        """
        Return a new context instance.

        Returns:
            A new context instance.
        """
        return Context(**self.options)

    def run(self, *args, **kwargs) -> None:
        """
        Run the duty function.

        This function also runs pre- and post-duties.

        Arguments:
            args: Positional arguments passed to the function.
            kwargs: Keyword arguments passed to the function.
        """
        self.run_duties(self.pre)
        self.function(self.context, *args, **kwargs)
        self.run_duties(self.post)

    def run_duties(self, duties_list: DutyListType) -> None:  # noqa: WPS231 (not complex)
        """
        Run a list of duties.

        Arguments:
            duties_list: The list of duties to run.

        Raises:
            RuntimeError: When a duty name is given to pre or post duties.
                Indeed, without a parent collection, it is impossible
                to find another duty by its name.
        """
        for duty_item in duties_list:
            if isinstance(duty_item, Duty):
                # Item is a proper duty, run it.
                duty_item.run()
            elif isinstance(duty_item, str):
                # Item is a reference to a duty.
                if self.collection is None:
                    raise RuntimeError(
                        f"Can't find duty by name without a collection ({duty_item})",
                    )
                # Get the duty and run it.
                self.collection.get(duty_item).run()
            elif callable(duty_item):
                # Item is a callable, call it.
                duty_item(self.context)
