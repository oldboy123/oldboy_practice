#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""By xuzhigui"""


class MetaJoe(type):
    def __call__(cls, *args, **kwargs):
        print(super().mro())
        print('MetaJoe.__call__')
        # return super().__call__(*args, **kwargs)
        # return super(MetaJoe, cls).__call__(*args, **kwargs)
        return type.__call__(cls, *args, **kwargs)      #  上面三种写法完全一致

class Joe(metaclass=MetaJoe):

# class Joe():  # 和下面定义原类最终返回的类是一样的，但是上面的metaclass会调用 MetaJoe.__call__ 从而有一些输出，但是下面的这个就不会
#     __metaclass__ = "MetaJoe"
    def __new__(cls, *args, **kwargs):
        obj = super(Joe, cls).__new__(cls)
        print('__new__ called. got new obj id=0x%x' % id(obj))
        return obj

    def __init__(self, arg):
        print('__init__ called (self=0x%x) with arg=%s' % (id(self), arg))
        self.arg = arg

j = Joe(12)
print(type(j))
print(j.arg)
