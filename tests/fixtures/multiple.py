from duty import duty


@duty
def first_duty(ctx):
    ctx.run(lambda: 0, fmt="tap", title="first")


@duty
def second_duty(ctx):
    ctx.run(lambda: 0, fmt="tap", title="second")
