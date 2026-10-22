"""What each phase accepts. Phases are cumulative: phase C accepts everything A and B do."""

PHASES = "ABC"  # implemented so far; D-F are designed in PLAN.md

_OPCODES = {
    "A": {
        "RESUME", "NOP", "LOAD_SMALL_INT", "LOAD_CONST", "LOAD_NAME", "STORE_NAME",
        "BINARY_OP", "UNARY_NEGATIVE", "PUSH_NULL", "CALL", "POP_TOP", "RETURN_VALUE",
        "COPY", "SWAP", "EXTENDED_ARG",
    },
    "B": {
        "COMPARE_OP", "TO_BOOL", "UNARY_NOT", "POP_JUMP_IF_FALSE", "POP_JUMP_IF_TRUE",
        "JUMP_FORWARD", "JUMP_BACKWARD", "NOT_TAKEN", "GET_ITER", "FOR_ITER",
        "END_FOR", "POP_ITER",
    },
    "C": {"FORMAT_SIMPLE", "BUILD_STRING", "CALL_KW"},
}

_BINOPS = {
    "A": {"+", "-", "*", "//", "%", "+=", "-=", "*=", "//=", "%="},
    "B": set(),
    "C": {"[]"},
}

# builtin -> (min args, max args); None means unbounded
_BUILTINS = {
    "A": {"print": (0, 1)},
    "B": {"range": (1, 3)},
    "C": {"print": (0, None), "str": (1, 1), "len": (1, 1)},
}

_CONST_TYPES = {
    "A": {"int", "str", "none"},
    "B": {"bool"},
    "C": {"tuple"},  # only as CALL_KW keyword-name tuples
}

_PRINT_KWARGS = {"A": set(), "B": set(), "C": {"sep", "end"}}

# Builtin names known to any phase. A name in this set that the script never
# assigns is a builtin; otherwise it is a user name.
ALL_BUILTINS = {"print", "range", "str", "len", "sum", "min", "max"}


def _upto(table, phase, merge):
    acc = None
    for p in PHASES[: PHASES.index(phase) + 1]:
        acc = merge(acc, table[p])
    return acc


def _union(a, b):
    return set(b) if a is None else a | b


def _dict_merge(a, b):
    out = dict(a or {})
    out.update(b)
    return out


class Phase:
    def __init__(self, name):
        if name not in PHASES:
            raise ValueError(f"unknown phase {name!r}; implemented: {PHASES}")
        self.name = name
        self.opcodes = _upto(_OPCODES, name, _union)
        self.binops = _upto(_BINOPS, name, _union)
        self.builtins = _upto(_BUILTINS, name, _dict_merge)
        self.const_types = _upto(_CONST_TYPES, name, _union)
        self.print_kwargs = _upto(_PRINT_KWARGS, name, _union)
        # Before phase C, string literals may only be passed straight to print().
        self.str_values = name >= "C"

    def __repr__(self):
        return f"Phase({self.name})"
