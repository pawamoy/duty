from duty import duty


@duty
def documented(ctx, param="default"):
    """Run a documented duty.

    This second line must never appear in shell completions.

    Parameters:
        param: A parameter.
    """


@duty
def undocumented(ctx):
    pass
