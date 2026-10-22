"""Grammar-constrained decoding: which tokens may come next in a step's output.

`OutputGrammar(n_instrs, n_names)` tracks the output side of a step,

    <state> ip @d @d @d stack VALUE* names (N<k> VALUE)* </state> [<out> c:x+ </out>] <eos>

and `allowed()` returns the token ids the model may emit next, so every decoded
step parses. It also enforces canonical ints (no leading zeros, no -0), names
in increasing order, ip within the listing and bounded stack and string sizes.
"""
from . import config, tokens

T = tokens.TOKEN_ID
_DIGITS = tokens.DIGITS
_CHARS = [f"c:{c}" for c in tokens.CHARS]
_VALUE_START = (["i+", "i-", "True", "False", "None", "NULL", '"', "RANGE", "RANGE_IT", "("]
                + tokens.BUILTIN_NAMES)
MAX_INT_DIGITS = 7
MAX_OUT_CHARS = 512


class GrammarError(Exception):
    pass


class OutputGrammar:
    def __init__(self, n_instrs, n_names, max_stack=config.MAX_STACK):
        self.max_addr = n_instrs - 1
        self.n_names = n_names
        self.max_stack = max_stack
        self.frames = [["start"]]
        self.addr = 0
        self.addr_digits = 0
        self.depth = 0
        self.last_name = -1
        self.out_chars = 0

    # -------------------------------------------------- allowed sets
    def allowed(self):
        return {T[t] for t in self._allowed()}

    def _allowed(self):
        f = self.frames[-1]
        kind = f[0]
        if kind == "int":
            _, sign, digits = f
            if not digits:
                return list(_DIGITS)
            out = list(_DIGITS) if len(digits) < MAX_INT_DIGITS else []
            can_end = not (len(digits) > 1 and digits[-1] == "0") and not (sign == "i-" and digits == ["0"])
            if can_end:
                out += self._follow_after_value(len(self.frames) - 2)
            return out
        if kind == "str":
            return (_CHARS if f[1] < config.MAX_STR_LEN else []) + ['"']
        if kind == "triple":
            return ["i+", "i-"]
        if kind == "tuple":
            return _VALUE_START + [")"]
        return self._top_allowed(kind)

    def _top_allowed(self, kind):
        if kind == "start":
            return ["<state>"]
        if kind == "ip":
            return ["ip"]
        if kind == "addr":
            k = self.addr_digits
            scale = 10 ** (2 - k)
            return [f"@{d}" for d in range(10) if (self.addr * 10 + d) * scale <= self.max_addr]
        if kind == "stack_kw":
            return ["stack"]
        if kind == "stack":
            return (_VALUE_START if self.depth < self.max_stack else []) + ["names"]
        if kind == "names":
            return [f"N{k}" for k in range(self.last_name + 1, self.n_names)] + ["</state>"]
        if kind == "name_val":
            return list(_VALUE_START)
        if kind == "after_state":
            return ["<out>", "<eos>"]
        if kind == "out_first":
            return list(_CHARS)
        if kind == "out":
            return (_CHARS if self.out_chars < MAX_OUT_CHARS else []) + ["</out>"]
        if kind == "after_out":
            return ["<eos>"]
        if kind == "done":
            return []
        raise AssertionError(kind)

    def _follow_after_value(self, parent):
        """Tokens that may follow a completed value whose parent frame is frames[parent]."""
        f = self.frames[parent]
        kind = f[0]
        if kind == "triple":
            if f[1] > 1:
                return ["i+", "i-"]
            return self._follow_after_value(parent - 1)
        if kind == "tuple":
            return _VALUE_START + [")"]
        if kind == "stack":
            return (_VALUE_START if self.depth + 1 < self.max_stack else []) + ["names"]
        if kind == "name_val":
            return [f"N{k}" for k in range(self.last_name + 1, self.n_names)] + ["</state>"]
        raise AssertionError(kind)

    # -------------------------------------------------- transitions
    def feed(self, tok):
        if tok not in self._allowed():
            raise GrammarError(f"token {tok!r} not allowed here")
        self._feed(tok)

    def feed_id(self, tid):
        self.feed(tokens.VOCAB[tid])

    def _feed(self, tok):
        f = self.frames[-1]
        kind = f[0]
        if kind == "int":
            if tok in _DIGITS:
                f[2].append(tok)
                return
            self.frames.pop()
            self._value_done()
            self._feed(tok)
            return
        if kind == "str":
            if tok == '"':
                self.frames.pop()
                self._value_done()
            else:
                f[1] += 1
            return
        if kind in ("triple", "tuple", "stack", "name_val"):
            if kind == "tuple" and tok == ")":
                self.frames.pop()
                self._value_done()
                return
            if kind == "stack" and tok == "names":
                f[0] = "names"
                return
            self._start_value(tok)
            return
        if kind == "start":
            f[0] = "ip"
        elif kind == "ip":
            f[0] = "addr"
        elif kind == "addr":
            self.addr = self.addr * 10 + int(tok[1])
            self.addr_digits += 1
            if self.addr_digits == 3:
                f[0] = "stack_kw"
        elif kind == "stack_kw":
            f[0] = "stack"
        elif kind == "names":
            if tok == "</state>":
                f[0] = "after_state"
            else:
                self.last_name = int(tok[1:])
                f[0] = "name_val"
        elif kind == "after_state":
            f[0] = "out_first" if tok == "<out>" else "done"
        elif kind == "out_first":
            self.out_chars = 1
            f[0] = "out"
        elif kind == "out":
            if tok == "</out>":
                f[0] = "after_out"
            else:
                self.out_chars += 1
        elif kind == "after_out":
            f[0] = "done"
        else:
            raise GrammarError(f"unexpected {tok!r} in state {kind}")

    def _start_value(self, tok):
        if tok in ("i+", "i-"):
            self.frames.append(["int", tok, []])
        elif tok == '"':
            self.frames.append(["str", 0])
        elif tok in ("RANGE", "RANGE_IT"):
            self.frames.append(["triple", 3])
        elif tok == "(":
            self.frames.append(["tuple"])
        else:
            self._value_done()  # single-token value

    def _value_done(self):
        f = self.frames[-1]
        kind = f[0]
        if kind == "triple":
            f[1] -= 1
            if f[1] == 0:
                self.frames.pop()
                self._value_done()
        elif kind == "stack":
            self.depth += 1
        elif kind == "name_val":
            f[0] = "names"

    @property
    def done(self):
        return self.frames[-1][0] == "done"
