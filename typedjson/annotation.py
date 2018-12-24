#!/usr/bin/env python3

from typing import Any
from typing import Optional
from typing import Type
from typing import Tuple


def args_of(type_: Type) -> Tuple[Type, ...]:
    return type_.__args__ if hasattr(type_, '__args__') else tuple()  # type: ignore


def hints_of(type_: Type) -> Optional[Any]:
    import typing
    return typing.get_type_hints(type_) if hasattr(type_, '__annotations__') else None


def origin_of(type_: Type) -> Optional[Type]:
    import typing
    return type_.__origin__ if hasattr(type_, '__origin__') else None
