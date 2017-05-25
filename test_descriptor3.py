#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""By xuzhigui"""


class RevealAccess(object):
    """A data descriptor that sets and returns values
       normally and prints a message logging their access.
    """

    def __init__(self, initval=None, name='var'):
        self.val = initval
        self.name = name

    def __get__(self, obj, objtype):
        # print(obj)
        # print(objtype)
        # print(self)
        print('Retrieving', self.name)
        return self.val

    def __set__(self, obj, val):
        print('Updating' , self.name)
        self.val = val
    #     obj.var = val

class MyClass(object):

    x = RevealAccess(10, 'var "x"')
    y = 5
    def __init__(self):
        self.x = "3"

a = MyClass()
print(a.x)
# print(type(a).__dict__['x'].__get__(a, type(a)))
