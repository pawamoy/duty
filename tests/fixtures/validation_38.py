def posonly_marker(ctx, a: int, /, b: int):
    pass  # pragma: no cover


def kwonly_marker(ctx, a: int, *, b: int):
    pass  # pragma: no cover


def only_markers(ctx, a: int, /, b: int, *, c: int):
    pass  # pragma: no cover


def full(ctx, a: int, /, b: int, *c: int, d: int, e: int = 0, **f: int):
    pass  # pragma: no cover
