#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""By xuzhigui"""


class DataDescriptor(object):
    def __init__(self, init_value):
        self.value = init_value

    def __get__(self, instance, typ):
        return 'DataDescriptor __get__'

    def __set__(self, instance, value):
        print ('DataDescriptor __set__')
        self.value = value


class NonDataDescriptor(object):
    def __init__(self, init_value):
        self.value = init_value

    def __get__(self, instance, typ):
        return('NonDataDescriptor __get__')


class Base(object):
    dd_base = DataDescriptor(0)
    ndd_base = NonDataDescriptor(0)


class Derive(Base):
    dd_derive = DataDescriptor(0)
    ndd_derive = NonDataDescriptor(0)
    same_name_attr = 'attr in class'

    def __init__(self):
        self.not_des_attr = 'I am not descriptor attr'
        self.same_name_attr = 'attr in object'
        # self.dd_derive = "123445"   
        # self.ndd_derive = "thissss"  #加上这一行就覆盖了class中dd_derive的属性
        # print("in init ndd_derive is", self.ndd_derive)
        # print(vars(self))   # 查看到实例的变量。说明任何时候实例的变量是优先的
        # print(vars(type(self)))

    def __getattr__(self, key):
        return '__getattr__ with key %s' % key

    def change_attr(self):
        # self.__dict__['dd_derive'] = 'dd_base now in object dict '
        # self.dd_derive = "123445"   #不管我怎么写都是这样的,亦或者写在__init__中都这是DataDescriptor __get__
        self.__dict__['ndd_derive'] = 'ndd_derive now in object dict '


def main():
    b = Base()
    d = Derive()
    print(d.ndd_derive)
    print('Derive object dict', d.__dict__)
    # assert d.dd_base == "DataDescriptor __get__"
    # assert d.ndd_derive == 'NonDataDescriptor __get__'
    # assert d.not_des_attr == 'I am not descriptor attr'
    # assert d.no_exists_key == '__getattr__ with key no_exists_key'
    # assert d.same_name_attr == 'attr in object'
    d.change_attr()
    print("before")
    print(vars(d))
    print(vars(type(d)))
    print("after")
    print(d.ndd_derive)
    print(d.dd_derive)
    # print('Derive object dict', d.__dict__)
    # assert d.dd_base != 'dd_base now in object dict '
    # assert d.ndd_derive == 'ndd_derive now in object dict '
    # print('d.dd_derive is', d.dd_derive)
    # print('d.ndd_derive is', d.ndd_derive)

    try:
        b.no_exists_key
    except Exception as e:
        assert isinstance(e, AttributeError)

if __name__ == '__main__':
    main()


# data descri > instance variable > non-data descri > getattr()
