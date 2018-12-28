class Person(object):
    def __init__(self, name, age):
        self._name = name
        self._age = age

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, age):
        self._age = age

    def __str__(self):
        return "name:%s, age=%d\n" % (self._name, self._age)


importeeVariable = 100


def sayHello(obj):
    print("%s say hello." % obj.name)
