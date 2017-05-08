def a(*args, **kwargs):
    print(args)
    print(type(args))

    print(kwargs)
    print(type(kwargs))

    #print(**kwargs)
    return [i*3 for i in [int(j)*4 for j in [*args]] if i>4]


abc = a("1", "2", "3", "4", name="dada", age="dahuia")
print(abc)


def b(*args):
    print(args)
    print(type(args))
    print([i for i,j in (args)])

b(("a", "b"))
