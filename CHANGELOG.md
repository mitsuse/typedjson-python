## Unreleased


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
