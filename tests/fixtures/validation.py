def no_params(ctx):
    pass  # pragma: no cover


def pos_or_kw_param(ctx, a: int):
    pass  # pragma: no cover


def pos_or_kw_params(ctx, a: int, b: int):
    pass  # pragma: no cover


def varpos_param(ctx, *a: int):
    pass  # pragma: no cover


def pos_and_varpos_param(ctx, a: int, *b: int):
    pass  # pragma: no cover


def kwonly_param(ctx, *a: int, b: int):
    pass  # pragma: no cover


def varkw_param(ctx, a: int, **b: int):
    pass  # pragma: no cover


def varkw_no_annotation(ctx, **a):
    pass  # pragma: no cover


def posonly_marker(ctx, a: int, /, b: int):
    pass  # pragma: no cover


def kwonly_marker(ctx, a: int, *, b: int):
    pass  # pragma: no cover


def only_markers(ctx, a: int, /, b: int, *, c: int):
    pass  # pragma: no cover


def full(ctx, a: int, /, b: int, *c: int, d: int, e: int = 0, **f: int):
    pass  # pragma: no cover
