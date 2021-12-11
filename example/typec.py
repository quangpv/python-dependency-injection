from src.injector import component, inject
from typeb import TypeB


@component()
class TypeD:
    def __str__(self):
        return "Type D"


@component
class TypeC:
    def __init__(self, type_b: TypeB, type_d: TypeD):
        self.type_b = type_b
        self.type_d = type_d

    @inject
    def name(self) -> TypeB: pass

    def __str__(self):
        return f"This is type C {self.type_d} {self.name()}"
