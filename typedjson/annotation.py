#!/usr/bin/env python3

from typing import Any
from typing import Dict
from typing import Optional
from typing import Type
from typing import Tuple


def args_of(type_: Type) -> Tuple[Type, ...]:
    return type_.__args__ if hasattr(type_, '__args__') else tuple()  # type: ignore


def hints_of(type_: Type) -> Optional[Dict[str, Type]]:
    from typing import get_type_hints
    from copy import copy

    origin = origin_of(type_)
    args = args_of(type_)
    type__ = type_ if origin is None else origin
    mapping = dict(zip(parameters_of(type_), args))

    if hasattr(type__, '__annotations__'):
        annotations = get_type_hints(type__)
        if len(mapping) > 0:
            annotations_: Dict[str, Type] = {}
            for n, t in annotations.items():
                t_ = mapping.get(t)
                if t_ is None:
                    return None
                else:
                    annotations_[n] = t_
            return annotations_
        else:
            return copy(annotations)
    else:
        return None


def origin_of(type_: Type) -> Optional[Type]:
    import typing
    return type_.__origin__ if hasattr(type_, '__origin__') else None


def parameters_of(type_: Type) -> Tuple[Type, ...]:
    origin = origin_of(type_)
    if origin is None:
        return tuple()
    else:
        return origin.__parameters__ if hasattr(origin, '__parameters__') else tuple()  # type: ignore
