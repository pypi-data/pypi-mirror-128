# Implementing this contract will catch any exception from any state


async def call(hub, ctx):
    try:
        ret = ctx.func(*ctx.args, **ctx.kwargs)
        return await hub.pop.loop.unwrap(ret)
    except Exception as e:
        return {
            "changes": {},
            "comment": f"{e.__class__.__name__}: {e}",
            "name": ctx.kwargs["name"],
            "result": False,
        }
