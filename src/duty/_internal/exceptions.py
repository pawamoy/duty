class DutyFailure(Exception):  # noqa: N818
    """An exception raised when a duty fails."""

    def __init__(self, code: int) -> None:
        """Initialize the object.

        Parameters:
            code: The exit code of a command.
        """
        super().__init__(self)
        self.code = code
        """The exit code of the command that failed."""
