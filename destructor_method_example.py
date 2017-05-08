#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""By xuzhigui"""


from os.path import join

class FileObject(object):
    def __init__(self, filepath='~', filename='sample.txt'):
        self.file = open(join(filepath, filename), 'w')

    def __del__(self):
        print("close file", self.file)
        self.file.close()
        del self.file
        print("over close file")

a = FileObject(filepath="./")
a.file.write("abchda\n")
print(type(a.file))
print("program over")
print("program over")
print("program over")
print("program over")
print("program over")
print("program over")
print("program over")
