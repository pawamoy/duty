def no_params(ctx):
    pass


def pos_or_kw_param(ctx, a: int):
    pass


def pos_or_kw_params(ctx, a: int, b: int):
    pass


def varpos_param(ctx, *a: int):
    pass


def pos_and_varpos_param(ctx, a: int, *b: int):
    pass


def kwonly_param(ctx, *a: int, b: int):
    pass


def varkw_param(ctx, a: int, **b: int):
    pass


def varkw_no_annotation(ctx, **a):
    pass
