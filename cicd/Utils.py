#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re
from typing import Any, List, TypeVar, Type, cast, Callable
from types import (
    BuiltinFunctionType,
    BuiltinMethodType,
    FunctionType,
    MethodType,
    LambdaType,
    ModuleType,
    TracebackType,
)
from functools import partial
from toolz import curry
import inspect

T = TypeVar("T")


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def parse_dict_to_obj(parse_map: dict, obj: Any):
    if not isinstance(obj, dict):
        raise TypeError(f"Expected dictionary but got {type(obj).__name__}")
    result = {key: parse_func(obj.get(key)) for key, parse_func in parse_map.items()}
    return result


def format_value(value: any, separators=(',', ':'), sort_keys=True):
    """
    Formats a given value into a specific string representation based on its type.

    :param value: The value to be formatted.
    :param separators: Optional. The separators are to be used when formatting dictionaries or lists. Default is a comma (',') for keys and colons (':') for values.
    :param sort_keys: Optional. Specifies whether to sort the keys of dictionaries before formatting. Default is True.
    :return: The formatted value as a string.

    """
    if isinstance(value, bool):
        return str(value).lower()
    elif isinstance(value, int):
        return int(value)
    elif is_float(value):
        return float(value)
    elif isinstance(value, (dict, list)):
        return json.dumps(value, separators=separators, sort_keys=sort_keys)
    else:
        return f'"{value}"' if value else '""'


def is_float(value: any) -> bool:
    """
    :param value: The value to be checked if it is a float.
    :return: True if the value is a float, False otherwise.

    """
    try:
        if re.match(r'^\d+\.\d+$', value):
            result = float(value)
            return isinstance(result, float)
        return False
    except Exception as ex:
        print(ex)
        return False


def is_json_object(value: any) -> bool:
    """
    Check if the given value is a JSON object.

    :param value: The value to be checked.
    :return: True if the value is a JSON object, False otherwise.

    """
    try:
        if value:
            result = json.loads(value)
            return isinstance(result, dict)
        return False
    except Exception:
        return False


def isfunction(variable: any) -> bool:
    return isinstance(
        variable,
        (
            BuiltinFunctionType,
            BuiltinMethodType,
            FunctionType,
            MethodType,
            LambdaType,
            partial,
            curry
        ),
    )


isclass = inspect.isclass


def ismodule(variable: any) -> bool:
    return isinstance(variable, ModuleType)


def isexception(variable: any) -> bool:
    return isinstance(variable, Exception)


def istraceback(variable: any) -> bool:
    return isinstance(variable, TracebackType)


def isclassinstance(x: any) -> bool:
    if isfunction(x) or isclass(x) or ismodule(x) or istraceback(x) or isexception(x):
        return False
    return True
