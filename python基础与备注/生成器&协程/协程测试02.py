def run(coroutine):
    try:
        print(coroutine.send(None))
        print(coroutine.send(None))
        print(coroutine.send(None))
    except StopIteration as e:
        print(("e.value=", e.value))


import asyncio


@asyncio.coroutine
def async_function():
    yield 1
    yield 2
    return 5


@asyncio.coroutine
def await_coroutine():
    result = yield from async_function()
    print(("result=", result))
    return 3


run(await_coroutine())
