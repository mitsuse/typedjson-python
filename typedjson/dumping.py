#!/usr/bin/env python3

from typing import Any
from typing import Dict
from typing import IO
from typing import Optional


def _serialize(decoded: Any) -> Any:
    if isinstance(decoded, tuple) or isinstance(decoded, list):
        return tuple(map(_serialize, decoded))

    dict_ = getattr(decoded, "__dict__", None)
    if dict_ is None:
        return decoded

    serialized: Dict[str, Any] = {}
    for k, v in dict_.items():
        serialized[k] = _serialize(v)

    return serialized


def dump(decoded: Any, file_: IO[str], indent: Optional[int] = None) -> None:
    import json

    from typedjson import DecodingError

    if isinstance(decoded, DecodingError):
        raise decoded
    else:
        if hasattr(decoded, "__dict__"):
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
        serialized = _serialize(decoded)
        return json.dumps(serialized, indent=indent)
