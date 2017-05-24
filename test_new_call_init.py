#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""By xuzhigui"""


class A(object):
    def __call__(self, *args, **kwargs):
        print("args is", *args)
        print("i am called", self)

    def __new__(cls, *args, **kwargs):
        print("new exec")
        return super().__new__(cls)

    def __init__(self, *args, **kwargs):
        print("exec init")
        self.c = "123"

a = A("1", "2")

a("3", "4")

