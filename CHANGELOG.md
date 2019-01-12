## Unreleased

- Use `__init__.__annotation__` to decode JSON as arbitrary class.


## 0.6.0

- Support API like 'json.dump' and 'json.dumps' ([#1][issue-001] by [@rruc][user-rruc]).
- Fix #5: Raise `TypeMismatching` with priority over `UnsupportedDecoding`.


## 0.5.0

- Support Python 3.6.x for environments where Python 3.7 is unavailable.


## 0.4.0

- Support decoding `List`.


## 0.3.0

- Support decoding parameterized data class.
- Prohibit decoding generic and raw type


## 0.2.0

- Support API like `json.load` and `json.loads`.


## 0.1.0

- Support decoding types as below:
    - primitive types like `str`, `int`, `float`, `bool` and `None`.
    -`Union` and `Optional`.
    - homogeneous and heterogeneous `Tuple`
    - variable-length `Tuple`.
    - non-generic dataclasses.

[issue-001]: https://github.com/mitsuse/typedjson-python/pull/1
[user-rruc]: https://github.com/rruc
