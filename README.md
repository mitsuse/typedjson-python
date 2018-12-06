# typedjson

[![License][license-badge]][license]
[![Pypi][pypi-badge]][pypi]

JSON decoding for Python with type hinting (PEP 484).


## Requirements

- Python >= 3.7
- Use `from __future__ import annotations` (See [PEP 563][pep-563]).
- Use non-generic `@dataclasses.dataclass` without modifying `__init__` to decode JSON as class.


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

print(typedjson.decode(CatJson, json))  # CatJson(id='test-cat', age=13, name=NameJson(first='Jiji', last=None))

print(typedjson.decode(CatJson, {}))  # Output: <DecodingError path=('id',)>
```

Please refer to [test codes](/tests/test_.py) for more detail.


## TODO

- Use `__init__.__annotation__` to decode JSON as arbitrary class.
- Support API like `json.load` and `json.loads`.


[license-badge]: https://img.shields.io/badge/license-MIT-yellowgreen.svg?style=flat-square
[license]: LICENSE
[pypi-badge]: https://img.shields.io/pypi/v/typedjson.svg
[pypi]: https://pypi.org/project/typedjson/
[pep-563]: https://www.python.org/dev/peps/pep-0563/
