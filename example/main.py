from src.qpvdi.injector import get, auto_single
from typeb import TypeB
from typec import TypeC


class TypeA:
    def __init__(self, type_b: TypeB, type_c: TypeC):
        self.type_b = type_b
        self.type_c = type_c

    def __str__(self):
        return f'{self.type_b.__str__()} - {self.type_c.__str__()}'


# @component(alias_for=TypeA)
class TypeA1(TypeA):
    def __str__(self):
        return f'Custom {self.type_b.__str__()} - {self.type_c.__str__()}'


# single(TypeA, lambda f: TypeA1(f(TypeB), f(TypeC)))
# factory(TypeA, lambda f: TypeA1(f(TypeB), f(TypeC)))

auto_single(TypeA, TypeA1)

if __name__ == '__main__':
    type_a = get(TypeA)
    print(type_a.__str__())
    # print(TypeC().name())
