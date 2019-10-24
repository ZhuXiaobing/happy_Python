import pprint

"""
int(),str(),bool()...这些都是类，以小写字母开头，是因为这些都python内置类。自定义等非内置类以大写字母+驼峰标识表示。
a = int(10) 等价于 a = 10

Python 类的设计思路：
    1：方法定义在类对象中
    2：属性定义在实例对象中
    3：通过类的“__init__”方法设置相关方法用到的必填属性。


Python 面向对象三要素讲解：

    1：封装（保证数据安全性）：隐藏对象中不希望被外部直接访问的属性或方法。（防小人，不防君子）

        1.1：如何隐藏对象属性
            使用双"__"开头的隐藏属性，内部会将“__Attribute”改名为“_ClassName__Attribute”，此类属性只能在类中访问,无法通过对象访问。不过此方式用的少。
            生产环境中，使用“_”开头的变量“标识隐藏属性”，但是这个属性是可以直接被访问的，用“_”开头仅仅是告诉用户这是一个不希望外部直接访问的属性。

        1.2：property装饰器（使用property装饰的方法，方法名[get/set]必须和属性名保持一致，get/set必须同时设置）
            作用：
                用@property装饰get方法，使得可以像调用属性一样使用get方法。
                用@属性名.setter修饰set方法
            示例：
                class Person(object):
                    def __init__(self, name):
                        self._name = name
                    @property
                    def name(self):
                        return self._name
                    @name.setter
                    def name(self, name):
                        self._name = name

    2：继承（保证程序可扩展性）（默认父类object）
        作用：使子类获取到父类所有的属性和方法，包括特殊方法（魔术方法）。

        方法重写：
            子类方法会覆盖父类同名方法，方法查找时一层层往上找。
            super()调用可以获取当前类的父类，且调用父类方法时不需要传递self参数。
        示例：
            class A():
                def __init__(self, name):
                    self._name = name
            class a(A):
                def __init__(self, name, age):
                    # 高耦合写法，不推荐使用
                    # A.__init__(self, name)
                    # 推荐写法
                    super.__init__(name)
                    self._age = age

        多重继承：
            多重继承会使得子类获取到所有父类中的所有方法。如果多个父类中有重名方法，则按照父类申明顺序，排在前面的父类，其方法优先调用。
            可以通过"类.__bases__"获取到类的所有父类元组集合。
            开发中，多重继承会复杂化代码，应当尽量避免使用多重继承。

    3：多态（保证程序灵活性）：一个类型具有多种形态。提高了面向对象编程的灵活性。
        经典概念：python中多态的鸭子理论：一个对象如果具有鸭子的特征，那么它就是鸭子。
        实例：如果一个类具有__len__方法，那个其对象都可以调用len方法求长度。


类的属性和方法小结
    1：直接在类中定义的属性是类属性，类属性可以通过类或者类实例访问到，但是"只能通过类对象去修改"。
    2：实例属性只能通过实例访问和修改，无法通过类对象访问和修改。

    实例方法：类中定义的，第一个参数是self的方法。
            实例方法可以通过实例去调用，此时self自动赋值
            实例方法也可以通过类对象去调用，此时self不会自动赋值。必须手动对self复制。

    类方法：在类中定义的，且用@classmethod装饰的方法是类方法。
            类方法的第一个参数是cls，也会被自动赋值，cls就是当前的类对象。
            类方法可以用类对象调用，也可以用实例对象调用，没有区别。

    静态方法：在类中用@staticmethod装饰的方法。
            静态方法没有任何默认参数（self,cls),可以通过类对象和实例对象去调用。
            静态方法基本上可以看作是一个与类没什么关系的普通方法，只是存放在类这个命名空间的函数而已。

Python中的垃圾回收：
    Python会自调回收"没有引用"的对象，而且回收之前，会调用对象的__del__这个特殊方法（魔术方法）。
    示例：
        class A():
            def __del__(self):
                print("A() is deleted.")
        a = A()
        del a # 通过del删除a这个引用，此时垃圾回收会触发之前新建的对象的del方法。



Python中的特殊方法（魔术方法）小结：
    特征：
    1：”__“开头和结尾
    2：无需手动调用，特殊情况自动调用。

    学习重点：
    1：特殊方法作用
    2：特殊方法调用时机

    常用的魔法函数：
    1:__str__():在尝试将对象转换为字符串时会调用，类似于”>>>print(a)”。object类的默认实现调用的是__repr__()
    2:__repr__():会在当前对象调用repr(obj)时调用此方法，指定对象在交互模式中直接输出的效果，类似于”>>>a“
    3:__eq__():
    4:__hash__():
        所有类默认具有__eq__与__hash__，所有类的实例在默认实现中都不相等。如果x==y,则"x is y"和"hash(x)==hasy(y)"都成立。
        如果一个类实现了__eq__(),则__hash__默认为None，其类的对象不支持hash相关操作，如果要继承父类__hash__()，必须显示指定：__hash__ = <ParentClass>.__hash__


类似于函数，python的类也可以被装饰。
    @f1(arg)
    @f2
    class Foo: pass
    等价于
    class Foo: pass
    Foo = f1(arg)(f2(Foo))


特殊说明：
    1：类的内部，实例使用字典来实现的，可以用示例对象的"__dict__"访问该字典，对对象属性的修改会反应到该字典中。
    2：python实例属性查找设计到两个魔术方法：
        2.1:__getattribute__():此方法具有绝对高优先级，
            此方法的查找顺序是：data descriptor --> 实例字典 --> non-data descriptor.
        2.2:__getattr__():只有在__getattribute__()找不到对应的属性时，才会调用此方法查找属性。这是一个兜底方法。
    3：del x 并不等同于x.__del__():
        del x 只会将x对应对象的引用减少1
        x.__del__()只在x对象的引用数为0时才会调用。
    4：尤其注意官方文档"3.3.9节：特殊方法的查找"。
        在通过对象隐式调用特殊方法的时候，是会绕过__getattribute__方法，即不去调用此方法。
"""

print("\n" + "*" * 20 + "以下测试说明属性访问优先级顺序是：data descriptor --> 实例字典 --> non-data descriptor" + "*" * 20)


# 数据描述符（定义了__set__ 和/或 __delete__）
class Name(object):
    def __get__(self, instance, owner):
        print("invoke Name get")
        return instance.abc

    def __set__(self, instance, value):
        print("invoke Name set")
        instance.abc = "数据描述符的固定值，实例无法改变"

    def __set_name__(self, owner, name):
        pass


# 非数据描述符
class Age(object):
    def __get__(self, instance, owner):
        print("invoke Name get")
        return "实例字典中的只可以覆盖该值"


# 测试类
class Test(object):
    name = Name()
    age = Age()


pprint.pprint(Test.__dict__)

t = Test()
t.name = "t1"
t.age = "t1's age"
pprint.pprint(t.__dict__)
# 访问的是数据描述符，实例不可定制。
print(t.name)
# 访问的是非数据描述符，实例可定制
print(t.age)

t2 = Test()
t2.name = "t2"
t2.age = "t2's age"
pprint.pprint(t2.__dict__)
# 访问的是数据描述符，实例不可定制。
print(t2.name)
# 访问的是非数据描述符，实例可定制
print(t2.age)
# 删除实例字典中的属性，将调用非数据描述符中的数据。
del t2.age
print(t2.age)

print("\n" + "*" * 20 + "以下测试__dict__和__slots__的关系" + "*" * 20)


class SlotsTest(object):
    # 若想SlotsTest的对象有__dict__属性，则必须把__dict__放入__slots__中。
    __slots__ = ["age", "name", "__dict__"]


s = SlotsTest()
s.age = 10
s.name = "hello"
print("发现：__slots__中已经列举的属性age,name，不会出现在__dict__中。")
print(s.__dict__)
s.pk = "pk"
print(s.__dict__)
