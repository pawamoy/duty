import sys
from io import StringIO


class _LazyStdout(StringIO):
    def write(self, value: str) -> int:
        return sys.stdout.write(value)

    def __repr__(self) -> str:
        return "stdout"


class _LazyStderr(StringIO):
    def write(self, value: str) -> int:
        return sys.stderr.write(value)

    def __repr__(self) -> str:
        return "stderr"
