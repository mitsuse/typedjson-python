#!/usr/bin/env python3

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
    name: NameJson


data = CatJson(
    id="test-cat",
    age=13,
    name=NameJson(
        first='jiji',
        last=None,
    ),
)


expectation = {
    'id': 'test-cat',
    'age': 13,
    'name': {
        'first': 'jiji',
    },
}


def test_dump() -> None:
    import tempfile

    with tempfile.TemporaryFile('w+') as f:
        typedjson.dump(data, f)
        f.seek(0)
        json = f.read() # type: str

    import ast
    assert ast.literal_eval(json) == expectation


def test_dumps() -> None:
    assert typedjson.dumps(data) == str(expectation)

