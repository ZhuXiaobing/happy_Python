"""
生成器：
    iterable：代表了一个包含若干items的整体，这类整体是可以进行迭代(遍历)的；
    iterator：表达了一个拥有当前状态的iterable对象，这个iterator对象会经过next()对其自身的状态进行变更。
    比如，一个列表对象(iterable)是包含若干items的sequence，但是列表对象(iterable)并不应该标记当前状态是哪一个item——这个工作应该交给一个与iterable相关的迭代器对象（iterator）来处理（通过iter(iterable)得到）

    不要以为Python的序列类型（如list,tuple,str）是迭代器，实际上它们只是可迭代对象

    对于Python
    如果一个对象，拥有iter()方法（可以给定自己初始状态），则其为iterable。
    如果一个对象，拥有iter()和next()方法（可以给定自己的初始状态+可以从一个状态变化到另一个后续状态），则其为迭代器。


生成器：
    是迭代器的一个派生类。

    生成器的两种常用表现形式：
    1：函数内部使用yield来使函数对象表现出迭代器的性质
        e.g:
            for i in a_list:
                yield f(i)
    2：使用生成器表达式：生成器表达式的值是迭代器（iterator）！生成器表达式的值具有一次性使用的特点！
        e.g:
            (f(i) for in in a_list)
            区别于列表解析：[f(i) for i in a_list]
"""


# 定义一个迭代器类对象
class Fib:
    def __init__(self, max):
        self.__max = max

    # iter()方法放回迭代器对象本身
    def __iter__(self):
        self.__a = 0
        self.__b = 1
        return self

    def __next__(self):
        fib = self.__a
        if fib > self.__max:
            raise StopIteration
        self.__a, self.__b = self.__b, self.__a + self.__b
        return fib


for n in Fib(1000):
    print(n, )

# 生成器测试
a_dict = {"a": 1, "b": 2}
x_gen = ((a, b) for a, b in a_dict.items())
for item in x_gen:
    print(item)
