"""
高阶函数必须具有以下特征：
    1.可以将函数作为参数
    2.可以将函数作为返回值

    特征2的典型应用：闭包，什么时候该使用闭包？当有见不得人的数据需要藏起来的时候，就需要使用闭包。
    综合了特征1，特征2的典型应用：装饰器

装饰器语法：
    @f1(arg)
    @f2
    def func():pass
    等价于
    def func():pass
    func = f1(arg)(f2(func))

"""

"""
示例01
"""
print("=" * 20, "step1:高阶函数使用示例", "=" * 20)

l = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


def fn(i):
    if i % 2 != 0:
        return True
    return False


"""将函数作为参数传递进函数"""
print(list(filter(fn, l)))

"""使用lambda定义匿名函数 fn"""
print(list(filter((lambda x: x % 2 != 0), l)))
print(list(map(lambda x: x * x, l)))

"""匿名函数也是复制给变量，但是一般不这么玩"""
f = lambda x: x % 2 != 0
m = lambda x: x * x
print(list(filter(f, l)))
print(list(map(m, l)))

"""
示例02
"""
print("=" * 20, "step2:闭包的讲解", "=" * 20)


def outer():
    oa = "outer parameter"

    def inner():
        print("inner body", oa)

    return inner


outer()()

"""
示例03
"""
print("=" * 20, "step2.1:使用闭包求均值，实现变量安全", "=" * 20)


def outavg():
    nums = []
    def avg(i):
        nums.append(i)
        return sum(nums) / len(nums)
    return avg


avg = outavg()
# 此时外部函数无法直接设置nums的值了，确保了nums的安全。
print(avg(6))
print(avg(7))

"""
示例04：装饰器的示例
"""
print("=" * 20, "step3:装饰器的使用", "=" * 20)


def f01(arg):
    def f2(func):
        def f3(*args, **kws):
            print(arg, "f1 start...")
            func(*args, **kws)
            print(arg, "f1 end...")
        return f3
    return f2


def f02(func):
    def f(*args, **kws):
        print("f2 start...")
        func(*args, **kws)
        print("f2 end...")
    return f


def f03(arg):
    def f2(func):
        def f3(*args, **kws):
            print(arg, "f3 start...")
            func(*args, **kws)
            print(arg, "f3 end...")
        return f3
    return f2


@f01("hello f1")
@f02
@f03("hell f3")
def decorated(a: int, b: int) -> None:
    print("docerated method, a+b =", (a + b))


def decorated2(a: int, b: int) -> None:
    print("docerated method, a+b =", (a + b))


decorated(1, 3)
print("\ndecorated2的等效写法")
f01("hello f1")(f02(f03("hello f3")(decorated2)))(1, 4)
