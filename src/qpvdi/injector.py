import functools
import typing
from typing import Generic, TypeVar

T = TypeVar('T')
V = TypeVar('V')
InstanceProvider = typing.Callable[[V], V]
InstanceFactory = typing.Callable[[InstanceProvider], T]

COMPONENT = '__component__'


class Injector:

    def get(self, gen_type: T):
        pass


class Bean(Generic[T]):
    __value = None

    def __init__(self, creator: InstanceFactory, is_single: bool):
        self.__creator__ = creator
        self.__single__ = is_single

    def get_instance(self) -> T:
        if self.__single__:
            if self.__value is None:
                self.__value = self.__creator__(get)
            return self.__value
        return self.__creator__(get)


class DefinitionBean(Bean):
    def __init__(self, creator: InstanceFactory, is_single):
        super().__init__(creator, is_single)


class ComponentBean(Bean):
    def __init__(self, gen_type: Generic[T], param_types: [T], is_single):
        def create_instance(creator: InstanceProvider):
            if len(param_types) == 0:
                return gen_type()
            params = [creator(i) for i in param_types]
            return gen_type(*params)

        super().__init__(lambda creator: create_instance(creator), is_single)


class DIContext(Injector):
    def __init__(self):
        self.__cache = {}
        self.__implement_types__ = []

    def put(self, gen_type: Generic[T], bean: Bean):
        key = gen_type.__name__
        if self.__cache.__contains__(key):
            raise RuntimeError(f"{key} has been declared")
        self.__cache[gen_type.__name__] = bean

    def require(self, gen_type: Generic[T]) -> Bean:
        key = gen_type.__name__
        if not self.__cache.__contains__(key):
            raise RuntimeError(f"Not found declaration for type {key}")
        return self.__cache[key]

    def lookup(self, gen_type: Generic[T]) -> typing.Optional[Bean]:
        key = gen_type.__name__
        if not self.__cache.__contains__(key):
            return None
        return self.__cache[key]

    def get(self, gen_type: T):
        return self.require(gen_type).get_instance()

    def exists(self, implement_type):
        if self.__implement_types__.__contains__(implement_type.__name__):
            return True
        return False

    def put_component(self, alias_type, implement_type, component_bean):
        self.__implement_types__.append(implement_type.__name__)
        self.put(alias_type, component_bean)


di_context = DIContext()


def __create_component_bean__(di_type: Generic[T], singleton: bool) -> ComponentBean:
    constructor = di_type.__init__
    annotations = getattr(constructor, "__annotations__", None)
    code = getattr(constructor, "__code__", None)

    if code is not None and annotations is not None:
        if code.co_argcount - 1 != len(annotations):
            raise RuntimeError(f"You're missing hint type in class {di_type.__name__}")

    if annotations is None or len(annotations) == 0:
        return ComponentBean(di_type, [], singleton)
    param_types = [annotations[param_name] for param_name in annotations]
    return ComponentBean(di_type, param_types, singleton)


def component(f=None, alias_for: Generic[T] = None, singleton: bool = False):
    type_alias = alias_for
    if not f:
        if type_alias is not None:
            if di_context.exists(type_alias):
                raise RuntimeError(f"{type_alias.__name__} is base class, it can not be component")
        return functools.partial(component, alias_for=type_alias, singleton=singleton)

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)

    alias = type_alias

    if type_alias is None:
        alias = f

    di_context.put_component(alias, f, __create_component_bean__(f, singleton))

    return wrapper


def single(alias_type: Generic[T], creator: InstanceFactory):
    di_context.put(alias_type, DefinitionBean(creator, True))


def auto_single(alias_type: Generic[T], implement_type: Generic[T]):
    di_context.put_component(alias_type, implement_type, __create_component_bean__(implement_type, True))


def factory(alias_type: Generic[T], creator: InstanceFactory):
    di_context.put(alias_type, DefinitionBean(creator, False))


def auto_factory(alias_type: Generic[T], implement_type: Generic[T]):
    di_context.put_component(alias_type, implement_type, __create_component_bean__(implement_type, False))


def get(gen_type):
    return di_context.require(gen_type).get_instance()


def inject(f):
    @functools.wraps(f)
    def decorator(self, *args, **kwargs):
        key = f'{COMPONENT}{f.__name__}'
        result = getattr(self, key, None)
        if result is not None:
            return result
        type_hint = typing.get_type_hints(f)
        if not type_hint.__contains__('return'):
            raise RuntimeError("Inject field should have return type hint")
        return_type = type_hint['return']
        result = di_context.require(return_type).get_instance()
        setattr(self, key, result)
        return result

    return decorator
