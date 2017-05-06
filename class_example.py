#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""By xuzhigui"""


class Foo(object):
    def __new__(cls, *args, **kwargs):
        self = object.__new__(Stranger, *args, **kwargs)
        # self.__init__(self, *args, **kwargs) == self.__class__.__init__(self, *args, **kwargs)
        self.__class__.__init__(self, *args, **kwargs)
        print("Foo self is", self)
        cls.__init__(cls, *args, **kwargs)
        return self

    def __init__(self, *args, **kwargs):
        print("test")
        self.names = args
        self.kwargs = kwargs
        print("self.names is ", self.names)
        print("self is", self)


class Stranger(object):
    def __init__(self, *args, **kwargs):
        self.name = args
        self.kw = kwargs
        print("stranger is", self.name)
        print("stranger object is", self)
        return '35465'

    def display(self):
        print(self.name)

foo = Foo("ahda")
foo.display()

print(type(foo).__init__(foo))  # type(foo)得到的结果是<class '__main__.Stranger'> 所以调用的Stranger的__init__

