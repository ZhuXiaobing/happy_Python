"""
Python中只有两种作用域：
    1.全局作用域
    2.函数作用域
    函数内部默认变量都是局部变量，如果要引入全局变量，必须用 global 关键字申明。

命名空间就是存储变量的空间，同理，函数只有两种命名空间
    1.全局命名空间
    2.局部命名空间

    命名空间是一个字典。
    函数内部通过调用locals()函数可以获取当前局部命名空间，
    全局作用域调用locals()获取的是全局命名空间。
    任意地方通过调用globals()函数可以获取全局命名空间。
"""

print("=" * 20, "Step1: 函数作用域测试", "=" * 20)

a = 1


def f1():
    a = 2
    print("f1=", a)

    def f2():
        """引用最外层全局作用域的 a 变量"""
        global a
        a = 3
        print("f2=", a)

    def f3():
        """引用最近的外层函数作用域的 a 变量"""
        print("f3=", a)

    f2()
    f3()


print("f=", a)
f1()

print("=" * 20, "Step2: 命名空间测试", "=" * 20)


def f():
    localscope = locals()
    globalscope = globals()

    localscope['b'] = 3
    print("localscope type=", type(localscope))
    print(localscope)

    # 命令行如下语句可行，能打印出b的值。在IDEA中会报错的。
    # print("b=",b)

    globalscope['c'] = 50  # 此处设置在全局作用于放入一个变量。


f()
# c虽然没有定义，但调用f()时，放入了一个局部变量到全局字典中了。
print("c=", c)
