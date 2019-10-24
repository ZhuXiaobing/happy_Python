"""
3.4.1 Awaitable对象
    通常，
    实现了__await()__方法的对象是Awaitable对象，从"async def func():"定义的函数中返回的 Coroutine对象也是Awaitable对象。
    但是,
    被"types.coroutine()和asyncio.coroutine()"修饰的生成器的迭代器对象也是Awaitable对象，但是他们没有实现__await__()方法。

3.4.2 协程对象

    关键点：
        1：协程是awaitable对象
        2：通过await调用，并在调用结果上迭代 来控制协程的执行。
            不可以直接await调用两次协程对象，否则抛出RuntimeError
        3：协程执行完毕返回时，迭代器触发StopIteration（协程不可以直接抛出这个异常）。如果执行过程中，协程抛出异常，有迭代器传递出来。

    协程具有如下三个非常类似生成器的方法，但是与生成器不同，协程"不直接支持迭代操作"。
        1：coroutine.send(value):开始或恢复协程的执行
            value==None: 推进协程的执行
            value!=None: 方法调用委派给引起协程挂起的迭代器的send方法。
        2：coroutine.throw:
            在协程中触发指定的异常，如果引起协程挂起的迭代器有throw方法，则委派给迭代器，否则，这个异常会在挂起点抛出。
            如果异常没有在协程中处理，将传播给调用者。
        3：coroutine.close():
            Causes the coroutine to clean itself up and exit.
            If the coroutine is suspended, this method first delegates to the close() method of the iterator that caused the coroutine to suspend, if it has such a method.
            Then it raises GeneratorExit at the suspension point, causing the coroutine to immediately clean itself up.
            Finally, the coroutine is marked as having finished executing, even if it was never started.

3.4.3 异步迭代器对象


"""
