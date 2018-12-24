#!/usr/bin/env python3

from __future__ import annotations

from typing import Generic
from typing import Optional
from typing import Tuple
from typing import TypeVar
from typing import Union

import typedjson
from dataclasses import dataclass


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


T1 = TypeVar('T1')
T2 = TypeVar('T2')


@dataclass(frozen=True)
class GenericJson(Generic[T1, T2]):
    t1: T1
    t2: T2


def test_can_decode_str() -> None:
    json = 'string'
    assert typedjson.decode(str, json) == json


def test_can_decode_nt() -> None:
    json = 1234
    assert typedjson.decode(int, json) == json


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
    json_short = (0, )
    json_long = (0, 1, 2, 3)
    assert typedjson.decode(Tuple[int, ...], json_short) == json_short
    assert typedjson.decode(Tuple[int, ...], json_long) == json_long


def test_can_decode_heterogeneous_fixed_tuple() -> None:
    json = (0, 1.1, 'hello', True)
    assert typedjson.decode(Tuple[int, float, str, bool], json) == json


def test_can_decode_dataclass() -> None:
    json = {
        'id': 'test-user',
        'age': 28,
        'name': {
            'first': 'Tomoya',
            'last': 'Kose',
        },
    }

    expectation = UserJson(
        id='test-user',
        age=28,
        name=NameJson(
            first='Tomoya',
            last='Kose',
        ),
    )

    assert typedjson.decode(UserJson, json) == expectation


def test_can_decode_dataclass_with_redundancy() -> None:
    json = {
        'id': 'test-user',
        'age': 28,
        'name': {
            'first': 'Tomoya',
            'last': 'Kose',
        },
        'role': 'administrator',
    }

    expectation = UserJson(
        id='test-user',
        age=28,
        name=NameJson(
            first='Tomoya',
            last='Kose',
        ),
    )

    assert typedjson.decode(UserJson, json) == expectation


def test_can_decode_parameterized_dataclass() -> None:
    json = {'t1': 100, 't2': 'hello'}
    expectation = GenericJson(t1=100, t2='hello')
    assert typedjson.decode(GenericJson[int, str], json) == expectation


def test_can_decode_dataclass_with_optional() -> None:
    json_lack = {'id': 'test-document', 'content': 'Hello, world!'}

    json_none = {'id': 'test-document', 'content': 'Hello, world!', 'owner': None}

    json_filled = {
        'id': 'test-document',
        'content': 'Hello, world!',
        'owner': {
            'id': 'test-owner',
            'name': {
                'first': 'Tomoya',
                'last': 'Kose',
            },
        },
    }

    expectation_none = DocumentJson(
        id='test-document',
        content='Hello, world!',
        owner=None,
    )

    expectation_filled = DocumentJson(
        id='test-document',
        content='Hello, world!',
        owner=OwnerJson(
            id='test-owner',
            name=NameJson(
                first='Tomoya',
                last='Kose',
            ),
        ),
    )

    assert typedjson.decode(DocumentJson, json_lack) == expectation_none
    assert typedjson.decode(DocumentJson, json_none) == expectation_none
    assert typedjson.decode(DocumentJson, json_filled) == expectation_filled


def test_can_decode_union() -> None:
    json_user = {
        'id': 'test-user',
        'age': 28,
        'name': {
            'first': 'Tomoya',
            'last': 'Kose',
        },
    }

    json_document = {
        'id': 'test-document',
        'content': 'Hello, world!',
        'owner': {
            'id': 'test-owner',
            'name': {
                'first': 'Tomoya',
                'last': 'Kose',
            },
        },
    }

    expectation_user = UserJson(
        id='test-user',
        age=28,
        name=NameJson(
            first='Tomoya',
            last='Kose',
        ),
    )

    expectation_document = DocumentJson(
        id='test-document',
        content='Hello, world!',
        owner=OwnerJson(
            id='test-owner',
            name=NameJson(
                first='Tomoya',
                last='Kose',
            ),
        ),
    )

    assert typedjson.decode(Union[UserJson, DocumentJson], json_user) == expectation_user
    assert typedjson.decode(Union[UserJson, DocumentJson], json_document) == expectation_document


def test_cannot_decode_with_wrong_type() -> None:
    json = True
    assert isinstance(typedjson.decode(str, json), typedjson.DecodingError)


def test_cannot_decode_none() -> None:
    json = None
    assert isinstance(typedjson.decode(str, json), typedjson.DecodingError)


def test_cannot_decode_object() -> None:
    json = object()
    assert isinstance(typedjson.decode(object, json), typedjson.DecodingError)


def test_cannote_decode_tuple_with_incompatible() -> None:
    json = (0, 1, 2, 3)
    assert isinstance(typedjson.decode(Tuple[int, str, int, int], json), typedjson.DecodingError)


def test_cannot_decode_fixed_tuple_with_short_sequence() -> None:
    json = (0, 1, 2)
    assert isinstance(typedjson.decode(Tuple[int, int, int, int], json), typedjson.DecodingError)


def test_cannot_decode_variable_tuple_with_short_sequence() -> None:
    json: Tuple = tuple()
    assert isinstance(typedjson.decode(Tuple[int, ...], json), typedjson.DecodingError)


def test_cannot_decode_generic_tuple() -> None:
    U = TypeVar('U')
    json = (0, 1, 2)
    assert isinstance(typedjson.decode(Tuple[int, U, int], json), typedjson.DecodingError)


def test_cannot_decode_generic_union() -> None:
    U = TypeVar('U')
    json = 100
    assert isinstance(typedjson.decode(Union[int, U], json), typedjson.DecodingError)


def test_cannot_decode_dataclass_with_lack_of_property() -> None:
    json = {
        'id': 'test-user',
        'age': 28,
        'name': {
            'last': 'Kose',
        },
    }

    expectation = typedjson.DecodingError(path=('name', 'first'))
    result = typedjson.decode(UserJson, json)

    assert isinstance(result, typedjson.DecodingError)
    assert result.path == expectation.path


def test_cannot_decode_parameterized_dataclass_with_wrong_parameter() -> None:
    json = {'t1': 100, 't2': 'hello'}
    assert isinstance(typedjson.decode(GenericJson[int, int], json), typedjson.DecodingError)


def test_cannot_decode_raw_dataclass() -> None:
    json = {'t1': 100, 't2': 'hello'}
    assert isinstance(typedjson.decode(GenericJson, json), typedjson.DecodingError)


def test_cannot_decode_generic_dataclass() -> None:
    U1 = TypeVar('U1')
    U2 = TypeVar('U2')
    json = {'t1': 100, 't2': 'hello'}
    assert isinstance(typedjson.decode(GenericJson[U1, U2], json), typedjson.DecodingError)
