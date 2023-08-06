#! /usr/bin/env python
# -*- coding: utf-8 -*-
import functools
from typing import Callable, Any

# from typing_extensions import ParamSpec

# P = ParamSpec("P")

# def wrapper(saqc: "SaQC", func: Callable[P, int]) -> Callable[P, "SaQC"]:
#     def inner(*args: P.args, **kwargs: P.kwargs) -> "SaQC":
#         return saqc
#     return inner

# def func(x: int, y: int) -> int:
#     """NotMuch"""
#     return x + y

# FUNC_MAP = {"func": func}

# class FuncDescriptor:
#     def __init__(self, callable):
#         self.f = callable
#         self.annotation = Callable[[float, float], float]

#     def __get__(self, obj, type=None):
#         return self.f

#     # @property
#     # def __annotations__(self):
#     #     return {**self.f.__annotations__, "return": "SaQC"}

#     @property
#     def __func__(self):
#         return self.f


# class SaQC:
#     def __init__(self):
#         self._planned = []

#     # def _wrap(self, func_name):
#     #     def inner(*args, **kwargs):
#     #         self._planned.append((func_name, args, kwargs))
#     #         return self
#     #     return inner

#     def _wrap(self, func_name, kwargs):
#         self._planned.append((func_name, kwargs))
#         return self

#     # def __getattr__(self, key):
#     #     if key not in FUNC_MAP:
#     #         raise AttributeError(f"no such attribute: '{key}'")
#     #     return self._wrap(key)

#     # @functools.wraps(func)
#     def funcMethod(self, x: int, y: int) -> "SaQC":
#         self._wrap("func", locals())
#         return self

#     def wrapper(self, *args, **kwargs):
#         self.wrapper.__annotations__.update({**func.__annotations__, "return": "SaQC"})
#         self._planned.append((func, args, kwargs))
#         return self


#     # fff = property(fget=lambda *args, **kwargs: func(*args, **kwargs))
#     ggg  = FuncDescriptor(func)
#     gggg = func

if __name__ == "__main__":
    from saqc.funcs.breaks import flagMissing
    import pdb

    pdb.set_trace()
    # saqc = SaQC()
    # xx = saqc.funcMethod
    # saqc.ggg(1)
