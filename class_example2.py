#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""By xuzhigui"""


import math

class Structure1(object):
    _fields = []

    def __init__(self, *args):
        print args
        print self._fields
        if len(args) != len(self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))

        for name, value in zip(self._fields, args):
            setattr(self, name, value)

class Stock(Structure1):
    _fields = ['name', 'shares', 'price']

s = Stock('ACME', 50, 91.1)
print s.__dict__
