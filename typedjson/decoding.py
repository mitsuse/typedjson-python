#!/usr/bin/env python3

from typing import Any
from typing import Generic
from typing import Iterator
from typing import List
from typing import NamedTuple
from typing import Optional
from typing import Tuple
from typing import Type
from typing import TypeVar
from typing import Union

Decoded = TypeVar('Decoded')
Value = TypeVar('Value')

Path = Tuple[str, ...]


class DecodingError(Exception):
    def __init__(self, path: Path) -> None:
        self.__path = path

    def __str__(self) -> str:
        return f'<DecodingError path={self.path}>'

    @property
    def path(self) -> Path:
        return self.__path


def decode(type_: Type[Decoded], json: Any, path: Path = ()) -> Union[Decoded, DecodingError]:
    decoders = (
        decode_as_union,
        decode_as_tuple,
        decode_as_list,
        decode_as_primitive,
        decode_as_dataclass,
    )

    for d in decoders:
        result = d(type_, json, path)
        if not isinstance(result, DecodingError):
            break

    return result


def decode_as_primitive(type_: Type[Decoded], json: Any, path: Path) -> Union[Decoded, DecodingError]:
    if type_ in (str, float, int, bool, type(None)) and isinstance(json, type_):
        return json
    else:
        return DecodingError(path)


def decode_as_dataclass(type_: Type[Decoded], json: Any, path: Path) -> Union[Decoded, DecodingError]:
    from typedjson.annotation import hints_of

    def _decode(annotation: Tuple[str, Any]) -> Union[Decoded, DecodingError]:
        key, type_ = annotation
        value = json.get(key)
        return decode(type_, value, path + (key, ))

    annotations = hints_of(type_)
    if isinstance(json, dict) and annotations is not None:
        parameters = tuple(map(_decode, annotations.items()))

        for parameter in parameters:
            if isinstance(parameter, DecodingError):
                return parameter

        return type_(*parameters)  # type: ignore
    else:
        return DecodingError(path)


def decode_as_union(type_: Type[Decoded], json: Any, path: Path) -> Union[Decoded, DecodingError]:
    from typedjson.annotation import args_of
    from typedjson.annotation import origin_of

    if origin_of(type_) is Union:
        args = args_of(type_)
        for type_ in args:
            if type_.__class__ is TypeVar:
                return DecodingError(path)

        for type_ in args:
            decoded = decode(type_, json, path)
            if not isinstance(decoded, DecodingError):
                break

        return decoded
    else:
        return DecodingError(path)


def decode_as_tuple(type_: Type[Decoded], json: Any, path: Path) -> Union[Decoded, DecodingError]:
    from typedjson.annotation import args_of
    from typedjson.annotation import origin_of

    def _required_length(args: Tuple[Type, ...]) -> int:
        return len(args) - 1 if args[-1] is ... else len(args)

    def _iter_args(args: Tuple[Type, ...]) -> Iterator[Type]:
        last: Optional[Type] = None
        for type_ in args:
            if type_ is ...:
                if last is None:
                    raise
                else:
                    while True:
                        yield last
            else:
                yield type_
            last = type_

    if origin_of(type_) is tuple:
        list_decoded: List[Any] = []
        length = len(json)
        if _required_length(args_of(type_)) > length:
            return DecodingError(path)

        for (index, (type_, element)) in enumerate(zip(_iter_args(args_of(type_)), json)):
            decoded = decode(type_, element, path + (str(index), ))
            if isinstance(decoded, DecodingError):
                return decoded

            list_decoded.append(decoded)

        return tuple(list_decoded)  # type: ignore
    else:
        return DecodingError(path)


def decode_as_list(type_: Type[Decoded], json: Any, path: Path) -> Union[Decoded, DecodingError]:
    from typedjson.annotation import args_of
    from typedjson.annotation import origin_of

    if origin_of(type_) is list:
        Element = args_of(type_)[0]
        list_decoded: List[Any] = []

        for index, element in enumerate(json):
            decoded = decode(Element, element, path + (str(index), ))
            if isinstance(decoded, DecodingError):
                return decoded

            list_decoded.append(decoded)

        return list(list_decoded)  # type: ignore
    else:
        return DecodingError(path)
