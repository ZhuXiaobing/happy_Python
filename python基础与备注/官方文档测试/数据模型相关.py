"""
3.3.8：with语句 上下文管理器 测试
"""


class myWithObject(object):
    def __enter__(self):
        print("with 上下文进入了哈。")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("with 上下文退出了哈")

    def __getattribute__(self, item):
        print("通过__getattribute__访问属性了哈。")
        return object.__getattribute__(self, item)

    def __len__(self):
        return 10


print("\nwith 上下文测试" + "*" * 20)
with myWithObject() as mwo:
    # 特殊方法的隐式调用，参考官方文档3.3.9
    print(len(mwo))
    # 特殊方法的显示调用
    print(mwo.__len__())

"""
3.3.9: 特殊方法的查找
"""


class TestSpecialMethod(object):
    def __len__(self):
        print("特殊方法，会绕过__getattribute__方法调用")
        return 10

    def normalMethod(self):
        return "普通方法，会通过__getattribute__方法调用"

    def __getattribute__(self, item):
        print("WOW!! __getattribute__表调用了")
        return object.__getattribute__(self, item)


tsm = TestSpecialMethod()

print("\ntsm.name" + "*" * 20)
tsm.name = "zxb"
print(tsm.name)

print("\nlen(tsm)" + "*" * 20)
print(len(tsm))

print("\ntsm.__len__()" + "*" * 20)
print(tsm.__len__())

print("\ntsm.normalMethod()" + "*" * 20)
print(tsm.normalMethod())
