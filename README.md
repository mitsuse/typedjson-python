# typedjson

[![License][license-badge]][license]
[![Pypi][pypi-badge]][pypi]
[![CI][ci-badge]][ci]

JSON decoding for Python with type hinting (PEP 484).


## Requirements and Restrictions

- Python >= 3.6
- Use non-generic or parameterized class to decode JSON.
- Use type hints without forward references.


## Features

- Support decoding types as below:
    - primitive types like `str`, `int`, `float`, `bool` and `None`.
    - `Union` and `Optional`.
    - homogeneous and heterogeneous `Tuple` and `List`.
    - variable-length `Tuple`.
    - non-generic and parameterized dataclasses.
- Support API like `json.load` and `json.loads`.


## Example


```python
from __future__ import annotations
from typing import Optional

import typedjson
from dataclasses import dataclass


@dataclass(frozen=True)
class NameJson:
    first: str
    last: Optional[str]


@dataclass(frozen=True)
class CatJson:
    id: str
    age: int
    name: Optional[NameJson]


json = {
    'id': 'test-cat',
    'age': 13,
    'name': {
        'first': 'Jiji',
    },
}

print(typedjson.decode(CatJson, json))  # Output: CatJson(id='test-cat', age=13, name=NameJson(first='Jiji', last=None))

print(typedjson.decode(CatJson, {}))  # Output: <DecodingError(TypeMismatch(('id',)))>
```

Please refer to [test codes](/tests/) for more detail.


## Contributions

Please read [CONTRIBUTING.md](/CONTRIBUTING.md).


## TODO

- Prohibit decoding `Set` and `Dict` explicitly.
- Provide the API document.
- Explain why typedjson uses undocumented APIs.
- Explain what typedjson resolves.
- Improve API to dump like `json.dump` and `json.dumps`.
    - Provide mypy plugin to check whether the class is encodable as JSON or not with `@typedjson.encodable` decorator.


[license-badge]: https://img.shields.io/badge/license-MIT-yellowgreen.svg?style=flat-square
[license]: LICENSE
[pypi-badge]: https://img.shields.io/pypi/v/typedjson.svg?style=flat-square
[pypi]: https://pypi.org/project/typedjson/
[ci-badge]: https://img.shields.io/travis/mitsuse/typedjson-python/master.svg?style=flat-square
[ci]: https://travis-ci.org/mitsuse/typedjson-python
[pep-563]: https://www.python.org/dev/peps/pep-0563/
