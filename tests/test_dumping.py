#!/usr/bin/env python3

from typing import Optional

from dataclasses import dataclass
import typedjson


@dataclass(frozen=True)
class NameJson:
    first: str
    last: Optional[str]


@dataclass(frozen=True)
class CatJson:
    id: str
    age: int
    name: NameJson


data = CatJson(
    id="test-cat",
    age=13,
    name=NameJson(
        first='jiji',
        last=None,
    ),
)

expectation = '''{
  "id": "test-cat",
  "age": 13,
  "name": {
    "first": "jiji"
  }
}'''


def test_dump() -> None:
    import io
    output = io.StringIO('')
    typedjson.dump(data, output, indent=2)
    assert output.getvalue() == expectation


def test_dumps() -> None:
    assert typedjson.dumps(data, indent=2) == expectation
