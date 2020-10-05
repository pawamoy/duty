from duty import duty


@duty
def say_hello(ctx, cat, dog="dog"):
    ctx.run(lambda: 0, title=f"Hello cat {cat} and dog {dog}!")
