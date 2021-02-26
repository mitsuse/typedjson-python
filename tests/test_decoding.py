#!/usr/bin/env python3

from typing import Any
from typing import Dict
from typing import Generic
from typing import List
from typing import Optional
from typing import NewType
from typing import Tuple
from typing import TypeVar
from typing import Union

import typedjson
from typedjson import DecodingError
from typedjson import TypeMismatch
from typedjson import UnsupportedDecoding
from dataclasses import dataclass

A = NewType("A", str)


@dataclass(frozen=True)
class NameJson:
    first: str
    last: str


@dataclass(frozen=True)
class UserJson:
    id: str
    age: int
    name: NameJson


@dataclass(frozen=True)
class OwnerJson:
    id: str
    name: NameJson


@dataclass(frozen=True)
class DocumentJson:
    id: str
    content: str
    owner: Optional[OwnerJson]


T1 = TypeVar("T1")
T2 = TypeVar("T2")


@dataclass(frozen=True)
class GenericJson(Generic[T1, T2]):
    t1: T1
    t2: T2


def test_can_decode_str() -> None:
    json = "string"
    assert typedjson.decode(str, json) == json


def test_can_decode_int() -> None:
    json = 1234
    assert typedjson.decode(int, json) == json


def test_can_decode_int_as_float() -> None:
    json = 1234
    assert typedjson.decode(float, json) == json


def test_can_decode_float() -> None:
    json = 1.234
    assert typedjson.decode(float, json) == json


def test_can_decode_true() -> None:
    json = True
    assert typedjson.decode(bool, json) == json


def test_can_decode_false() -> None:
    json = False
    assert typedjson.decode(bool, json) == json


def test_can_decode_optional() -> None:
    json = None
    assert typedjson.decode(Optional[str], json) == json


def test_can_decode_homogeneous_fixed_tuple() -> None:
    json = (0, 1, 2, 3)
    assert typedjson.decode(Tuple[int, int, int, int], json) == json


def test_can_decode_homogeneous_variable_tuple() -> None:
    json_empty: Any = tuple()
    json_short = (0,)
    json_long = (0, 1, 2, 3)
    assert typedjson.decode(Tuple[int, ...], json_empty) == json_empty
    assert typedjson.decode(Tuple[int, ...], json_short) == json_short
    assert typedjson.decode(Tuple[int, ...], json_long) == json_long


def test_can_decode_heterogeneous_fixed_tuple() -> None:
    json = (0, 1.1, "hello", True)
    assert typedjson.decode(Tuple[int, float, str, bool], json) == json


def test_can_decode_homogeneous_list() -> None:
    json = list(range(10))
    assert typedjson.decode(List[int], json) == json


def test_can_decode_heterogeneous_list() -> None:
    json = [1, "foo"]
    assert typedjson.decode(List[Union[str, int]], json) == json


def test_can_decode_any_list() -> None:
    json = [1, "foo"]
    assert typedjson.decode(List[Any], json) == json


def test_can_decode_string_any_dict() -> None:
    json = {"foo": 1, "bar": "baz"}
    assert typedjson.decode(Dict[str, Any], json) == json


def test_cannot_decode_dict_with_bad_key() -> None:
    json = {"foo": 1, 5: "baz"}

    expectation = DecodingError(TypeMismatch(("5",)))
    assert typedjson.decode(Dict[str, Any], json) == expectation


def test_cannot_decode_dict_with_bad_value() -> None:
    json = {"foo": 1, "baz": "baz"}

    expectation = DecodingError(TypeMismatch(("foo",)))
    assert typedjson.decode(Dict[str, str], json) == expectation


def test_can_decode_dataclass() -> None:
    json = {"id": "test-user", "age": 28, "name": {"first": "Tomoya", "last": "Kose"}}

    expectation = UserJson(
        id="test-user", age=28, name=NameJson(first="Tomoya", last="Kose")
    )

    assert typedjson.decode(UserJson, json) == expectation


def test_can_decode_dataclass_with_redundancy() -> None:
    json = {
        "id": "test-user",
        "age": 28,
        "name": {"first": "Tomoya", "last": "Kose"},
        "role": "administrator",
    }

    expectation = UserJson(
        id="test-user", age=28, name=NameJson(first="Tomoya", last="Kose")
    )

    assert typedjson.decode(UserJson, json) == expectation


def test_can_decode_parameterized_dataclass() -> None:
    json = {"t1": 100, "t2": "hello"}
    expectation = GenericJson(t1=100, t2="hello")
    assert typedjson.decode(GenericJson[int, str], json) == expectation


def test_can_decode_dataclass_with_optional() -> None:
    json_lack = {"id": "test-document", "content": "Hello, world!"}

    json_none = {"id": "test-document", "content": "Hello, world!", "owner": None}

    json_filled = {
        "id": "test-document",
        "content": "Hello, world!",
        "owner": {"id": "test-owner", "name": {"first": "Tomoya", "last": "Kose"}},
    }

    expectation_none = DocumentJson(
        id="test-document", content="Hello, world!", owner=None
    )

    expectation_filled = DocumentJson(
        id="test-document",
        content="Hello, world!",
        owner=OwnerJson(id="test-owner", name=NameJson(first="Tomoya", last="Kose")),
    )

    assert typedjson.decode(DocumentJson, json_lack) == expectation_none
    assert typedjson.decode(DocumentJson, json_none) == expectation_none
    assert typedjson.decode(DocumentJson, json_filled) == expectation_filled


def test_can_decode_newtype() -> None:
    raw = "foo"
    expectation = A(raw)

    assert typedjson.decode(A, raw) == expectation


def test_can_decode_union() -> None:
    json_user = {
        "id": "test-user",
        "age": 28,
        "name": {"first": "Tomoya", "last": "Kose"},
    }

    json_document = {
        "id": "test-document",
        "content": "Hello, world!",
        "owner": {"id": "test-owner", "name": {"first": "Tomoya", "last": "Kose"}},
    }

    expectation_user = UserJson(
        id="test-user", age=28, name=NameJson(first="Tomoya", last="Kose")
    )

    expectation_document = DocumentJson(
        id="test-document",
        content="Hello, world!",
        owner=OwnerJson(id="test-owner", name=NameJson(first="Tomoya", last="Kose")),
    )

    assert (
        typedjson.decode(Union[UserJson, DocumentJson], json_user) == expectation_user
    )
    assert (
        typedjson.decode(Union[UserJson, DocumentJson], json_document)
        == expectation_document
    )


def test_cannot_decode_with_wrong_type() -> None:
    json = True
    assert typedjson.decode(str, json) == DecodingError(TypeMismatch(()))


def test_cannot_decode_float_as_int() -> None:
    json = 1.234
    assert typedjson.decode(int, json) == DecodingError(TypeMismatch(()))


def test_cannot_decode_none() -> None:
    json = None
    assert typedjson.decode(str, json) == DecodingError(TypeMismatch(()))


def test_cannote_decode_tuple_with_incompatible() -> None:
    json = (0, 1, 2, 3)
    expectation = DecodingError(TypeMismatch(("1",)))
    assert typedjson.decode(Tuple[int, str, int, int], json) == expectation


def test_cannot_decode_none_as_tuple() -> None:
    json = None
    assert typedjson.decode(Tuple[str, ...], json) == DecodingError(TypeMismatch(()))


def test_cannot_decode_fixed_tuple_with_short_sequence() -> None:
    json = (0, 1, 2)
    expectation = DecodingError(TypeMismatch(()))
    assert typedjson.decode(Tuple[int, int, int, int], json) == expectation


def test_cannot_decode_generic_tuple() -> None:
    U = TypeVar("U")
    json = (0, 1, 2)
    expectation = DecodingError(UnsupportedDecoding(()))
    assert typedjson.decode(Tuple[int, U, int], json) == expectation


def test_cannot_decode_generic_list() -> None:
    U = TypeVar("U")
    json = list(range(10))
    expectation = DecodingError(UnsupportedDecoding(()))
    assert typedjson.decode(List[U], json) == expectation


def test_cannot_decode_homogeneous_list_with_incompatible() -> None:
    json = [1, 2, 3]
    expectation = DecodingError(TypeMismatch(("0",)))
    assert typedjson.decode(List[str], json) == expectation


def test_cannot_decode_heterogeneous_list_with_incompatible() -> None:
    json = [1, "foo"]
    expectation = DecodingError(TypeMismatch(("0",)))
    assert typedjson.decode(List[Union[str, str]], json) == expectation


def test_cannot_decode_generic_union() -> None:
    U = TypeVar("U")
    json = 100
    expectation = DecodingError(UnsupportedDecoding(()))
    assert typedjson.decode(Union[int, U], json) == expectation


def test_cannot_decode_dataclass_with_lack_of_property() -> None:
    json = {"id": "test-user", "age": 28, "name": {"last": "Kose"}}

    expectation = DecodingError(TypeMismatch(("name", "first")))

    assert typedjson.decode(UserJson, json) == expectation


def test_cannot_decode_parameterized_dataclass_with_wrong_parameter() -> None:
    json = {"t1": 100, "t2": "hello"}
    expectation = DecodingError(TypeMismatch(("t2",)))
    assert typedjson.decode(GenericJson[int, int], json) == expectation


def test_cannot_decode_raw_dataclass() -> None:
    json = {"t1": 100, "t2": "hello"}
    expectation = DecodingError(UnsupportedDecoding(()))
    assert typedjson.decode(GenericJson, json) == expectation


def test_cannot_decode_generic_dataclass() -> None:
    U1 = TypeVar("U1")
    U2 = TypeVar("U2")
    json = {"t1": 100, "t2": "hello"}
    expectation = DecodingError(UnsupportedDecoding(()))
    assert typedjson.decode(GenericJson[U1, U2], json) == expectation
