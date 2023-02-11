import sys
from io import StringIO
from mypy.main import main as mypy


class _LazyStdout(StringIO):
    def __repr__(self) -> str:
        return "stdout"

    def write(self, value):
        return sys.stdout.write(value)


class _LazyStderr(StringIO):
    def __repr__(self) -> str:
        return "stderr"

    def write(self, value):
        return sys.stderr.write(value)


def run(*args):
    mypy(
        args=args,
        stdout=_LazyStdout(),
        stderr=_LazyStderr(),
        clean_exit=True,
    )
    return True
