"""Vocabulary and the token encoding of listings, states and printed output.

Layout of one training step (see PLAN.md for the full grammar):

    <bos> <code> @0 @0 @0 RESUME @0 @0 @1 LOAD_SMALL_INT i+ 3 ... </code>
    <state> ip @0 @0 @7 stack print NULL i+ 4 names N0 i+ 3 </state>
    =>
    <state> ip @0 @0 @8 stack None names N0 i+ 3 </state> <out> c:4 c:\\n </out> <eos>

- Instruction indices are three address digits (@0-@9), most significant first.
  They are only ever copied, never computed.
- Ints are a sign token then decimal digits least significant first: 120 -> i+ 0 2 1.
- Strings are '"', one c:<char> token per character, '"'.
- The vocabulary already reserves tokens for phases D-F so it never changes.
"""
import hashlib

from . import config
from .values import NULL, Builtin, RangeIter, RangeObj

SPECIAL = ["<pad>", "<bos>", "<eos>", "<code>", "</code>", "<state>", "</state>",
           "<out>", "</out>", "=>"]
KEYWORDS = ["ip", "stack", "names", "heap", "frames", "locals"]
ADDR = [f"@{d}" for d in range(10)]
DIGITS = [str(d) for d in range(10)]
INT_SIGNS = ["i+", "i-"]
VALUE_WORDS = ["None", "True", "False", "NULL", '"', "(", ")", "[", "]",
               "RANGE", "RANGE_IT", "LIST", "LIST_IT", "STR_IT", "DICT", "DICT_IT", "FUNC"]
BUILTIN_NAMES = ["print", "range", "str", "len", "sum", "min", "max"]
METHOD_NAMES = ["append", "get", "items", "keys", "values"]
USER_NAMES = [f"N{i}" for i in range(config.MAX_GLOBALS)] + [f"L{i}" for i in range(config.MAX_LOCALS)]
REFS = [f"&{i}" for i in range(32)]
BINOPS = ["+", "-", "*", "//", "%", "+=", "-=", "*=", "//=", "%=", "[]"]
COMPARES = ["<", "<=", "==", "!=", ">", ">="]
OPCODES = sorted({
    # phases A-C
    "RESUME", "NOP", "LOAD_SMALL_INT", "LOAD_CONST", "LOAD_NAME", "STORE_NAME", "BINARY_OP",
    "UNARY_NEGATIVE", "PUSH_NULL", "CALL", "POP_TOP", "RETURN_VALUE", "COPY", "SWAP",
    "COMPARE_OP", "TO_BOOL", "UNARY_NOT", "POP_JUMP_IF_FALSE", "POP_JUMP_IF_TRUE",
    "JUMP_FORWARD", "JUMP_BACKWARD", "NOT_TAKEN", "GET_ITER", "FOR_ITER", "END_FOR",
    "POP_ITER", "FORMAT_SIMPLE", "BUILD_STRING", "CALL_KW",
    "EXTENDED_ARG",  # unused: prefixes are folded into the listing; kept so the vocab hash is stable
    # reserved for phases D-F
    "BUILD_LIST", "BUILD_TUPLE", "LIST_EXTEND", "LIST_APPEND", "LOAD_ATTR", "STORE_SUBSCR",
    "UNPACK_SEQUENCE", "CONTAINS_OP", "IS_OP", "BUILD_MAP", "MAP_ADD", "DICT_UPDATE",
    "MAKE_FUNCTION", "SET_FUNCTION_ATTRIBUTE", "LOAD_FAST", "LOAD_FAST_BORROW",
    "LOAD_FAST_LOAD_FAST", "LOAD_FAST_BORROW_LOAD_FAST_BORROW", "LOAD_FAST_CHECK",
    "LOAD_FAST_AND_CLEAR", "STORE_FAST", "STORE_FAST_LOAD_FAST", "STORE_FAST_STORE_FAST",
    "LOAD_GLOBAL", "STORE_GLOBAL", "POP_JUMP_IF_NONE", "POP_JUMP_IF_NOT_NONE",
    "JUMP_BACKWARD_NO_INTERRUPT", "BINARY_SLICE", "STORE_SLICE", "DELETE_SUBSCR",
    "CALL_INTRINSIC_1", "CONVERT_VALUE", "FORMAT_WITH_SPEC", "LIST_TO_TUPLE",
})
CHARS = [chr(c) for c in range(32, 127)] + ["\n", "\t"]
RESERVED = [f"<r{i}>" for i in range(24)]

VOCAB = (SPECIAL + KEYWORDS + ADDR + DIGITS + INT_SIGNS + VALUE_WORDS + BUILTIN_NAMES
         + METHOD_NAMES + USER_NAMES + REFS + [f"op:{o}" for o in BINOPS]
         + [f"cmp:{c}" for c in COMPARES] + ["in", "not in", "is", "is not"]
         + OPCODES + [f"c:{ch}" for ch in CHARS] + RESERVED)
assert len(VOCAB) == len(set(VOCAB))
TOKEN_ID = {t: i for i, t in enumerate(VOCAB)}
VOCAB_SIZE = len(VOCAB)
VOCAB_HASH = hashlib.sha256("\x00".join(VOCAB).encode()).hexdigest()[:16]
CHARSET = frozenset(CHARS)

_BUILTIN_SET = set(BUILTIN_NAMES)


class EncodeError(Exception):
    pass


class ParseError(Exception):
    pass


# ---------------------------------------------------------------- encoding

def addr(i):
    if not 0 <= i <= config.MAX_INSTRS:
        raise EncodeError(f"instruction index {i} out of range")
    return [f"@{i // 100}", f"@{i // 10 % 10}", f"@{i % 10}"]


def small_int(n):
    """Unsigned operand like CALL's argument count, least significant digit first."""
    return list(str(n)[::-1])


def enc_int(v):
    return ["i-" if v < 0 else "i+"] + list(str(abs(v))[::-1])


def enc_str(s):
    for ch in s:
        if ch not in CHARSET:
            raise EncodeError(f"character {ch!r} not in vocabulary")
    return ['"'] + [f"c:{ch}" for ch in s] + ['"']


def enc_value(v, out=None):
    out = [] if out is None else out
    t = type(v)
    if t is bool:
        out.append("True" if v else "False")
    elif t is int:
        out.extend(enc_int(v))
    elif t is str:
        out.extend(enc_str(v))
    elif v is None:
        out.append("None")
    elif v is NULL:
        out.append("NULL")
    elif t is Builtin:
        out.append(v.name)
    elif t is RangeObj:
        out.append("RANGE")
        for x in (v.start, v.stop, v.step):
            out.extend(enc_int(x))
    elif t is RangeIter:
        out.append("RANGE_IT")
        for x in (v.next, v.stop, v.step):
            out.extend(enc_int(x))
    elif t is tuple:
        out.append("(")
        for x in v:
            enc_value(x, out)
        out.append(")")
    else:
        raise EncodeError(f"cannot encode {t.__name__}")
    return out


def enc_name_ref(ref):
    kind, val = ref
    return f"N{val}" if kind == "N" else val


def enc_instr(ins):
    toks = addr(ins.index) + [ins.opname]
    op, arg = ins.opname, ins.arg
    if op in ("LOAD_SMALL_INT", "LOAD_CONST"):
        return enc_value(arg, toks)  # arg may be None, the constant
    if arg is None:
        return toks
    if op.endswith(("_NAME", "_GLOBAL")):
        toks.append(enc_name_ref(arg))
    elif op == "BINARY_OP":
        toks.append(f"op:{arg}")
    elif op == "COMPARE_OP":
        toks.append(f"cmp:{arg}")
    elif op.startswith(("JUMP", "POP_JUMP", "FOR_ITER")):
        toks.extend(addr(arg))
    else:
        toks.extend(small_int(arg))
    return toks


def enc_listing(program):
    toks = ["<code>"]
    for ins in program.instrs:
        toks.extend(enc_instr(ins))
    toks.append("</code>")
    return toks


def enc_state(st):
    toks = ["<state>", "ip"] + addr(st.ip) + ["stack"]
    for v in st.stack:
        enc_value(v, toks)
    toks.append("names")
    for k in sorted(st.names):
        toks.append(f"N{k}")
        enc_value(st.names[k], toks)
    toks.append("</state>")
    return toks


def enc_out(text):
    if not text:
        return []
    for ch in text:
        if ch not in CHARSET:
            raise EncodeError(f"character {ch!r} not in vocabulary")
    return ["<out>"] + [f"c:{ch}" for ch in text] + ["</out>"]


def enc_step(state_in, state_out, out_text):
    return enc_state(state_in) + ["=>"] + enc_state(state_out) + enc_out(out_text) + ["<eos>"]


def ids(tokens):
    try:
        return [TOKEN_ID[t] for t in tokens]
    except KeyError as e:
        raise EncodeError(f"unknown token {e.args[0]!r}") from None


def strs(token_ids):
    return [VOCAB[i] for i in token_ids]


# ---------------------------------------------------------------- decoding

class _Reader:
    __slots__ = ("toks", "pos")

    def __init__(self, toks, pos=0):
        self.toks = toks
        self.pos = pos

    def peek(self):
        if self.pos >= len(self.toks):
            raise ParseError("unexpected end of tokens")
        return self.toks[self.pos]

    def take(self, expect=None):
        t = self.peek()
        if expect is not None and t != expect:
            raise ParseError(f"expected {expect!r} at {self.pos}, got {t!r}")
        self.pos += 1
        return t


def _read_int(r):
    sign = r.take()
    if sign not in ("i+", "i-"):
        raise ParseError(f"expected int sign, got {sign!r}")
    digits = []
    while r.pos < len(r.toks) and r.toks[r.pos] in DIGITS:
        digits.append(r.take())
    if not digits:
        raise ParseError("int with no digits")
    if len(digits) > 1 and digits[-1] == "0":
        raise ParseError("non-canonical int (leading zero)")
    v = int("".join(reversed(digits)))
    if sign == "i-":
        if v == 0:
            raise ParseError("non-canonical int (-0)")
        v = -v
    return v


def _read_value(r):
    t = r.peek()
    if t in ("i+", "i-"):
        return _read_int(r)
    r.take()
    if t == "True":
        return True
    if t == "False":
        return False
    if t == "None":
        return None
    if t == "NULL":
        return NULL
    if t == '"':
        chars = []
        while r.peek() != '"':
            c = r.take()
            if not c.startswith("c:"):
                raise ParseError(f"bad string token {c!r}")
            chars.append(c[2:])
        r.take('"')
        return "".join(chars)
    if t in _BUILTIN_SET:
        return Builtin(t)
    if t == "RANGE":
        return RangeObj(_read_int(r), _read_int(r), _read_int(r))
    if t == "RANGE_IT":
        return RangeIter(_read_int(r), _read_int(r), _read_int(r))
    if t == "(":
        items = []
        while r.peek() != ")":
            items.append(_read_value(r))
        r.take(")")
        return tuple(items)
    raise ParseError(f"unexpected token {t!r} where a value was expected")


def _read_addr(r):
    n = 0
    for _ in range(3):
        t = r.take()
        if t not in ADDR:
            raise ParseError(f"expected address digit, got {t!r}")
        n = n * 10 + int(t[1])
    return n


def parse_state(toks, pos=0):
    """Parse '<state> ... </state>' starting at toks[pos]; returns (State, next pos)."""
    from .state import State

    r = _Reader(toks, pos)
    r.take("<state>")
    r.take("ip")
    ip = _read_addr(r)
    r.take("stack")
    stack = []
    while r.peek() != "names":
        stack.append(_read_value(r))
    r.take("names")
    names = {}
    last = -1
    while r.peek() != "</state>":
        t = r.take()
        if not (t.startswith("N") and t[1:].isdigit()):
            raise ParseError(f"expected name token, got {t!r}")
        k = int(t[1:])
        if k <= last:
            raise ParseError("names out of order")
        last = k
        names[k] = _read_value(r)
    r.take("</state>")
    return State(ip, tuple(stack), names), r.pos


def parse_step_output(toks, pos=0):
    """Parse a model's output side: '<state>...</state> [<out>...</out>] <eos>'."""
    st, pos = parse_state(toks, pos)
    r = _Reader(toks, pos)
    out = ""
    if r.peek() == "<out>":
        r.take()
        chars = []
        while r.peek() != "</out>":
            c = r.take()
            if not c.startswith("c:"):
                raise ParseError(f"bad output token {c!r}")
            chars.append(c[2:])
        r.take("</out>")
        if not chars:
            raise ParseError("empty <out> section")
        out = "".join(chars)
    r.take("<eos>")
    return st, out, r.pos
