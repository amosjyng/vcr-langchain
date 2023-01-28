from typing import Callable, Protocol


class Cassette(Protocol):
    _save: Callable
    append: Callable
    lookup: Callable
    write_protected: bool
