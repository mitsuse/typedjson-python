#!/usr/bin/env python3

from typing import Generic
from typing import List
from typing import Tuple
from typing import Type
from typing import TypeVar

from typedjson.annotation import args_of
from typedjson.annotation import origin_of
from typedjson.annotation import parameters_of
from dataclasses import dataclass


@dataclass(frozen=True)
class NameJson:
    first: str
    last: str


T1 = TypeVar('T1')
T2 = TypeVar('T2')


@dataclass(frozen=True)
class GenericJson(Generic[T1, T2]):
    t1: T1
    t2: T2


def test_can_obtain_args_of_generics() -> None:
    expectation = (int, str)
    assert args_of(GenericJson[int, str]) == expectation


def test_can_obtain_parameters_of_generics() -> None:
    expectation = (T1, T2)
    assert parameters_of(GenericJson[int, str]) == expectation


def test_can_obtain_origin_of_generics() -> None:
    expectation = GenericJson
    assert origin_of(GenericJson[int, str]) == GenericJson


def test_can_obtain_origin_of_tuple() -> None:
    assert origin_of(Tuple[int, ...]) is tuple


def test_can_obtain_origin_of_list() -> None:
    assert origin_of(List[int]) is list


def test_cannot_obtain_args_of_raw_generics() -> None:
    expectation: Tuple[Type, ...] = tuple()
    assert args_of(GenericJson) == expectation


def test_cannot_obtain_parameters_of_raw_generics() -> None:
    expectation: Tuple[Type, ...] = tuple()
    assert parameters_of(GenericJson) == expectation


def test_cannot_obtain_origin_of_raw_generics() -> None:
    assert origin_of(GenericJson) is None


def test_cannot_obtain_args_of_non_generics() -> None:
    expectation: Tuple[Type, ...] = tuple()
    assert args_of(NameJson) == expectation


def test_cannot_obtain_parameters_of_non_generics() -> None:
    expectation: Tuple[Type, ...] = tuple()
    assert parameters_of(NameJson) == expectation


def test_cannot_obtain_origin_of_non_generics() -> None:
    assert origin_of(NameJson) is None
