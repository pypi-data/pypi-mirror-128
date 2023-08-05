from typing import Any, Callable, Generic, Optional, Type, TypeVar, overload


T = TypeVar('T')


class cached_property(Generic[T]):  # noqa: N801
    def __init__(self, func: Callable[[Any], T]) -> None:
        self.func = func

    @overload
    def __get__(self, instance: None, owner: Optional[Type[Any]] = ...) -> 'cached_property[T]':
        pass

    @overload
    def __get__(self, instance, owner: Optional[Type[Any]] = ...) -> T:
        pass

    def __get__(self, obj, cls):
        value = self.func(obj)
        obj.__dict__[self.func.__name__] = value
        return value
