"""Interpreter state for phases A-C: one module frame.

`names` maps N-index -> value and is treated as immutable: a step that stores
a name builds a new dict, so a trace can keep every state cheaply.
"""
from dataclasses import dataclass, field


@dataclass(slots=True)
class State:
    ip: int
    stack: tuple = ()
    names: dict = field(default_factory=dict)

    def same(self, other):
        """Exact equality, distinguishing True from 1 (Python's == does not)."""
        return (self.ip == other.ip and _same_seq(self.stack, other.stack)
                and self.names.keys() == other.names.keys()
                and all(same_value(v, other.names[k]) for k, v in self.names.items()))


def same_value(a, b):
    if type(a) is not type(b):
        return False
    if type(a) is tuple:
        return _same_seq(a, b)
    return a == b


def _same_seq(a, b):
    return len(a) == len(b) and all(same_value(x, y) for x, y in zip(a, b))
