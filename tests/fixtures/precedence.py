from duty import duty


@duty(nofail=True)
def precedence(ctx):
    ctx.run(lambda: 1, title="Precedence", nofail=False)
