from typing import Any, Callable, Optional, Type, Union


class ClassPropertyDescriptor:
    def __init__(self, fget: Union[classmethod, staticmethod], fset: Optional[Union[classmethod, staticmethod]] = None):
        self.fget = fget
        self.fset = fset

    def __get__(self, obj: Any, cls: Type = None):
        if cls is None:
            cls = type(obj)
        return self.fget.__get__(obj, cls)()

    def __set__(self, obj: Any, value: Any):
        if not self.fset:
            raise AttributeError('can\'t set attribute')
        type_ = type(obj)
        return self.fset.__get__(obj, type_)(value)

    def setter(self, func: Union[classmethod, staticmethod, Callable]):
        if not isinstance(func, (classmethod, staticmethod)):
            func = classmethod(func)
        self.fset = func
        return self


def classproperty(func: Union[classmethod, staticmethod, Callable]):
    if not isinstance(func, (classmethod, staticmethod)):
        func = classmethod(func)
    return ClassPropertyDescriptor(func)
