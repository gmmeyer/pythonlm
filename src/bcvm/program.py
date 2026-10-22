"""Compile a script and turn its code object into an instruction listing.

The listing is what the model sees: one entry per instruction, addressed by
instruction index (not byte offset), with user names replaced by N-indices.
EXTENDED_ARG prefixes are folded into the instruction they extend, like
inline cache entries: dis already merges their value into its argument, and
CPython's only use of them is to widen that argument.
"""
import dis
from dataclasses import dataclass

from .phases import ALL_BUILTINS

NAME_OPS = {"LOAD_NAME", "STORE_NAME", "DELETE_NAME", "LOAD_GLOBAL", "STORE_GLOBAL", "DELETE_GLOBAL"}
STORE_OPS = {"STORE_NAME", "DELETE_NAME", "STORE_GLOBAL", "DELETE_GLOBAL"}
JUMP_OPS = {
    "POP_JUMP_IF_FALSE", "POP_JUMP_IF_TRUE", "POP_JUMP_IF_NONE", "POP_JUMP_IF_NOT_NONE",
    "JUMP_FORWARD", "JUMP_BACKWARD", "JUMP_BACKWARD_NO_INTERRUPT", "FOR_ITER",
}
INT_ARG_OPS = {"CALL", "CALL_KW", "COPY", "SWAP", "BUILD_STRING"}


@dataclass(slots=True)
class Instr:
    index: int
    offset: int
    opname: str
    arg: object
    line: int | None


class CompileError(Exception):
    pass


def compile_script(src):
    try:
        return compile(src, "<script>", "exec", dont_inherit=True)
    except (SyntaxError, ValueError) as e:
        raise CompileError(f"{type(e).__name__}: {e}") from None


def scan_names(code):
    """(user names in order of first appearance, names that are ever assigned).
    A builtin name the script never assigns is not a user name."""
    seen, stored = [], set()
    for ins in dis.get_instructions(code):
        if ins.opname in NAME_OPS:
            if ins.argval not in seen:
                seen.append(ins.argval)
            if ins.opname in STORE_OPS:
                stored.add(ins.argval)
    return [n for n in seen if n in stored or n not in ALL_BUILTINS], stored


def user_names(code):
    return scan_names(code)[0]


def _compare_symbol(argrepr):
    return argrepr[5:-1] if argrepr.startswith("bool(") else argrepr


class Program:
    def __init__(self, src, code=None):
        self.src = src
        self.code = code if code is not None else compile_script(src)
        self.names, self.stored = scan_names(self.code)
        self.name_index = {n: i for i, n in enumerate(self.names)}
        raw = list(dis.get_instructions(self.code))
        real = [ins for ins in raw if ins.opname != "EXTENDED_ARG"]
        self.prefix_offsets = frozenset(ins.offset for ins in raw if ins.opname == "EXTENDED_ARG")
        self.offset_to_index = {}
        index = 0
        for ins in raw:
            # a prefix maps to the instruction it extends, so jumps to it land there
            self.offset_to_index[ins.offset] = index
            if ins.opname != "EXTENDED_ARG":
                index += 1
        self.instrs = [self._convert(i, ins, real) for i, ins in enumerate(real)]

    def name_ref(self, name):
        if name in self.name_index:
            return ("N", self.name_index[name])
        return ("B", name)

    def _convert(self, i, ins, real):
        op = ins.opname
        if op in NAME_OPS:
            arg = self.name_ref(ins.argval)
        elif op == "LOAD_SMALL_INT" or op == "LOAD_CONST":
            arg = ins.argval
        elif op == "BINARY_OP":
            arg = ins.argrepr
        elif op == "COMPARE_OP":
            arg = _compare_symbol(ins.argrepr)
        elif op in JUMP_OPS:
            arg = self.offset_to_index[ins.argval]
            if op == "FOR_ITER":
                # On exhaustion CPython skips the END_FOR at the target, so the
                # listing gives the index where execution actually lands.
                if real[arg].opname != "END_FOR":
                    raise CompileError(f"FOR_ITER target is {real[arg].opname}, expected END_FOR")
                arg += 1
        elif op in INT_ARG_OPS:
            arg = ins.arg
        else:
            arg = None
        return Instr(i, ins.offset, op, arg, ins.line_number)

    def __len__(self):
        return len(self.instrs)
