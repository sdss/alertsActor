
import click

from functools import update_wrapper


def alerts_context(f):
    # Unpacks the context and send the actor and command.
    @click.pass_context
    def new_func(ctx, *args, **kwargs):
        return ctx.invoke(f, ctx.obj['actor'], ctx.obj['cmd'], ctx.obj['user'],
                          *args, **kwargs)
    return update_wrapper(new_func, f)
