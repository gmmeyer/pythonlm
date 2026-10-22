"""Runtime values in the reference interpreter's state.

Ints, bools, strs, None and tuples are plain Python objects, so arithmetic and
printing follow CPython exactly. Everything else is a small frozen dataclass.
"""
from dataclasses import dataclass


class _Null:
    __slots__ = ()

    def __repr__(self):
        return "NULL"


NULL = _Null()


@dataclass(frozen=True, slots=True)
class Builtin:
    name: str


@dataclass(frozen=True, slots=True)
class RangeObj:
    start: int
    stop: int
    step: int


@dataclass(frozen=True, slots=True)
class RangeIter:
    """CPython's range iterator, as (next value, stop, step)."""
    next: int
    stop: int
    step: int

    def has_next(self):
        return self.next < self.stop if self.step > 0 else self.next > self.stop


class PyError(Exception):
    """The script raises a Python exception (data generation discards these)."""

    def __init__(self, exc_type, msg=""):
        super().__init__(f"{exc_type}: {msg}")
        self.exc_type = exc_type


class Unsupported(Exception):
    """The script does something the interpreter deliberately doesn't model."""


class LimitExceeded(Exception):
    """Instruction budget, int bound, string length or stack depth exceeded."""


def py_str(v):
    """str(v) for printable values, matching CPython."""
    t = type(v)
    if t is int or t is bool or t is str or v is None:
        return str(v)
    raise Unsupported(f"str() of {t.__name__}")


def is_int(v):
    return type(v) is int or type(v) is bool
