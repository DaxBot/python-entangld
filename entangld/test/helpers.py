import asyncio

def block_until(coroutine):
    async def _await():
        return await coroutine
    return asyncio.run(_await())
