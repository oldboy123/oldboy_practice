#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""By xuzhigui"""


class TypedProperty(object):

    def __init__(self, name, type, default=None):
        self.name = "_" + name
        self.type = type
        self.default = default if default else type()

    def __get__(self, instance, cls):
        print("i am called")
        return getattr(instance, self.name, self.default)

    def __set__(self, instance, value):
        print("self is", self)
        print("instance is", instance)
        if not isinstance(value, self.type):
            raise TypeError("Must be a %s" % self.type)
        setattr(instance, self.name, value)

    def __delete__(self, instance):
        raise AttributeError("Can't delete attribute")


class Foo(object):
    name = TypedProperty("name", str)
    num = TypedProperty("num", int, 42)

acct = Foo()
# acct.name = "obi"
print(acct.name)
# print(type(acct).__dict__["name"].__get__(acct, type(acct)))
# print(acct.__dict__)
# print(acct.__class__.__dict__)
# acct.num = 1234
# print(acct.num)
