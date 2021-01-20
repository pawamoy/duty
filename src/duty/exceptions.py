"""Module containing the project's exceptions."""


class DutyFailure(Exception):
    """An exception raised when a duty fails."""

    def __init__(self, code):
        """
        Initialize the object.

        Arguments:
            code: The exit code of a command.
        """
        super().__init__(self)
        self.code = code
