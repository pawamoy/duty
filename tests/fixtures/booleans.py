from duty import duty


@duty
def boolean(ctx, zero: bool = True):
    ctx.run(lambda: 0 if zero else 1)
