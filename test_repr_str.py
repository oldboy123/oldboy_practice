#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""By xuzhigui"""


class Book(object):
    def __init__(self, author, title, price):
        self.author = author
        self.title = title
        self.price = price

    def __repr__(self):
        print("repr is called")
        return "{0} - {1}".format(self.author, self.title)

    def __str__(self):
        print("str is called")
        return "{0}....{1}".format(self.author, self.title)

    def __call__(self, *args, **kwargs):
        return repr(self)

book = Book('123', '23', '568')
# print(book())
print(book)
# repr(book())

getattr()
