from src.qpvdi.injector import component


class TypeB:
    def __init__(self):
        pass

    def __str__(self):
        return "This is type B"


@component(singleton=True, alias_for=TypeB)
class TypeB1(TypeB):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "This is type B1"
