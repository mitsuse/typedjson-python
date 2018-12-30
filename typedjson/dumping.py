#!/usr/bin/env python3

from typing import Any
from typing import Dict
from typing import IO
from typing import Optional


def _serialize(decoded: Any) -> Dict[str, Any]:
    dict_ = dict()
    for k, v in decoded.__dict__.items():
        if hasattr(v, '__dict__'):
            dict_[k] = _serialize(v)
        elif v is not None:
            dict_[k] = v
    return dict_


def dump(decoded: Any, file_: IO[str], indent: Optional[int] = None) -> None:
    import json

    from typedjson import DecodingError

    if isinstance(decoded, DecodingError):
        raise decoded
    else:
        if hasattr(decoded, '__dict__'):
            serialized = _serialize(decoded)
            json.dump(serialized, file_, indent=indent)
        else:
            json.dump(decoded, file_, indent=indent)


def dumps(decoded: Any, indent: Optional[int] = None) -> str:
    import json

    from typedjson import DecodingError

    if isinstance(decoded, DecodingError):
        raise decoded
    else:
        if hasattr(decoded, '__dict__'):
            serialized = _serialize(decoded)
            return json.dumps(serialized, indent=indent)
        else:
            return json.dumps(decoded, indent=indent)
