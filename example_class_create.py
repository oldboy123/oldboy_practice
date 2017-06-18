class A(type):
    def __call__(self, *args, **kwargs):
        print("huaha")
        obj = super().__call__()
        return obj


class B(object, metaclass=A):
    def __init__(self):
        print("dhauda123444")


b = B()
