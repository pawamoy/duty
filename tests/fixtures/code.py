from duty import duty


@duty
def exit_with(ctx, code):
    ctx.run(lambda: code)
