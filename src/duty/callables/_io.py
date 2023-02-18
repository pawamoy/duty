import sys
from io import StringIO


class _LazyStdout(StringIO):
    def __repr__(self) -> str:
        return "stdout"

    def write(self, value: str) -> int:
        return sys.stdout.write(value)


class _LazyStderr(StringIO):
    def __repr__(self) -> str:
        return "stderr"

    def write(self, value: str) -> int:
        return sys.stderr.write(value)
