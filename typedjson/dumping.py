#!/usr/bin/env python3

from __future__ import annotations

from typing import Any
from typing import Dict
from typing import IO
from typing import TypeVar

Decoded = TypeVar('Decoded')


def _serialize(decoded: Decoded) -> Dict[str, Any]:
    dict_ = dict()
    for k, v in decoded.__dict__.items():
        if hasattr(v, '__dict__'):
            dict_[k] = _serialize(v)
        elif v is not None:
            dict_[k] = v
    return dict_


def dump(decoded: Decoded, file_: IO[str]) -> None:
    import json

    from typedjson import DecodingError

    if isinstance(decoded, DecodingError):
        raise decoded
    else:
        if hasattr(decoded, '__dict__'):
            serialized = _serialize(decoded)
            json.dump(serialized, file_, indent=4)
        else:
            json.dump(decoded, file_)


def dumps(decoded: Decoded) -> str:
    import json

    from typedjson import DecodingError

    if isinstance(decoded, DecodingError):
        raise decoded
    else:
        if hasattr(decoded, '__dict__'):
            serialized = _serialize(decoded)
            return str(serialized)
        else:
            return json.dumps(decoded)
