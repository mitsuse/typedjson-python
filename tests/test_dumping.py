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


data = CatJson(id="test-cat", age=13, name=NameJson(first="jiji", last=None))

expectation = """{
  "id": "test-cat",
  "age": 13,
  "name": {
    "first": "jiji",
    "last": null
  }
}"""


def test_dump() -> None:
    import io

    output = io.StringIO("")
    typedjson.dump(data, output, indent=2)
    assert output.getvalue() == expectation


def test_dumps() -> None:
    assert typedjson.dumps(data, indent=2) == expectation


def test_dumps_int() -> None:
    expectation = "100"
    assert typedjson.dumps(100, indent=2) == expectation


def test_dumps_float() -> None:
    expectation = "1.0"
    assert typedjson.dumps(1.0, indent=2) == expectation


def test_dumps_str() -> None:
    expectation = '"hello"'
    assert typedjson.dumps("hello", indent=2) == expectation


def test_dumps_bool() -> None:
    expectation = "true"
    assert typedjson.dumps(True, indent=2) == expectation


def test_dumps_none() -> None:
    expectation = "null"
    assert typedjson.dumps(None, indent=2) == expectation


def test_dumps_tuple_of_name() -> None:
    names = (
        NameJson(first="jiji", last=None),
        NameJson(first="gin", last="mitsuse"),
        NameJson(first="konoha", last="mitsuse"),
    )

    expectation = "\n".join(
        (
            "[",
            "  {",
            '    "first": "jiji",',
            '    "last": null',
            "  },",
            "  {",
            '    "first": "gin",',
            '    "last": "mitsuse"',
            "  },",
            "  {",
            '    "first": "konoha",',
            '    "last": "mitsuse"',
            "  }",
            "]",
        )
    )

    assert typedjson.dumps(names, indent=2) == expectation


def test_dumps_list_of_name() -> None:
    names = [
        NameJson(first="jiji", last=None),
        NameJson(first="gin", last="mitsuse"),
        NameJson(first="konoha", last="mitsuse"),
    ]

    expectation = "\n".join(
        (
            "[",
            "  {",
            '    "first": "jiji",',
            '    "last": null',
            "  },",
            "  {",
            '    "first": "gin",',
            '    "last": "mitsuse"',
            "  },",
            "  {",
            '    "first": "konoha",',
            '    "last": "mitsuse"',
            "  }",
            "]",
        )
    )

    assert typedjson.dumps(names, indent=2) == expectation
