#!/usr/bin/env python3

from typing import IO
from typing import Type
from typing import TypeVar

Decoded = TypeVar("Decoded")


def load(type_: Type[Decoded], file_: IO[str]) -> Decoded:
    import json

    from typedjson import decode
    from typedjson import DecodingError

    decoded = decode(type_, json.load(file_))
    if isinstance(decoded, DecodingError):
        raise decoded
    else:
        return decoded


def loads(type_: Type[Decoded], string: str) -> Decoded:
    import json

    from typedjson import decode
    from typedjson import DecodingError

    decoded = decode(type_, json.loads(string))
    if isinstance(decoded, DecodingError):
        raise decoded
    else:
        return decoded
