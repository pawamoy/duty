def posonly_marker(ctx, a: int, /, b: int):
    pass


def kwonly_marker(ctx, a: int, *, b: int):
    pass


def only_markers(ctx, a: int, /, b: int, *, c: int):
    pass


def full(ctx, a: int, /, b: int, *c: int, d: int, e: int = 0, **f: int):
    pass
