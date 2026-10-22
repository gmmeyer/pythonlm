"""Grammar-based random scripts for phases A-C.

Scripts are built statement by statement. While execution is still straight
line (phase A, or the prefix of a phase B/C script before its first branch or
loop) every variable's value is known, so expressions are chosen to stay
within the int bound and avoid division by zero. Inside control flow values
are unknown; the generator keeps loops bounded by construction and leaves the
rest to the reference interpreter, which discards scripts that break a limit.
"""
from .. import config
from .common import SERIES_STEMS, VAR_NAMES, WORDS, pattern_text, random_text, small_int, string_literal

# print separators and endings people use, beyond the standard mix's few
SEPS = ["", " ", "  ", ", ", ",", "-", " - ", "|", " | ", ":", ": ", "\t", "\n", " -> ", " = ", ". ", "/",
        " / ", "; ", "*", "...", " + ", "_", "#", "\n\n"]

BOUND = config.INT_BOUND

# precedence levels for parenthesisation
ATOM, UNARY, MUL, ADD, CMP, NOT, AND, OR, IFEXP = 100, 90, 80, 70, 60, 50, 40, 30, 20


class Expr:
    __slots__ = ("src", "prec", "val", "kind")

    def __init__(self, src, prec, val, kind):
        self.src, self.prec, self.val, self.kind = src, prec, val, kind


def _wrap(e, prec, right=False):
    if e.prec < prec or (right and e.prec == prec):
        return f"({e.src})"
    return e.src


def _in_bound(v):
    return v is None or (type(v) is not int) or -BOUND <= v <= BOUND


class Gen:
    def __init__(self, rng, phase, arith=False, copy=False, edge=False):
        self.rng = rng
        self.phase = phase
        # arith: a drill for the hardest steps, with * // % dominant and
        # divisors spread over 1-99 rather than the usual 2, 5, 10, 60, 100
        self.arith = arith
        # copy: a drill where most string literals are repetitive patterns
        self.copy = copy
        # edge: a drill of patterns the standard mix rarely makes and people
        # write: and/or used for their int value, chained comparisons with any
        # operators, range steps up to 25, long scripts full of near-identical
        # labels ("Round 1", "Round 2", ...) that must be told apart when copied,
        # tuple assignment of two and three names (SWAP 2, SWAP 3), and scripts
        # with 11-28 names (other sources stay within N0-N9); from phase B,
        # bools used as numbers (`t == 1`, `(not a) + (not b)`, `n += i > 0`);
        # in phase C, loops over a string's positions (`s[i]`, `s[-1 - i]`,
        # counting and building strings) and longer f-strings and prints; empty
        # strings, any print sep/end, fixed-width padding, `a = b = c = "."`
        self.edge = edge
        self.series = [rng.choice(SERIES_STEMS), rng.randint(0, 3)]
        self.op_weights = [10, 8, 22, 30, 30] if arith else [30, 25, 18, 13, 14]
        self.B = phase >= "B"
        self.C = phase >= "C"
        self.lines = []
        self.vars = {}          # name -> 'int' | 'bool' | 'str'
        self.known = {}         # name -> exact value while execution is straight-line
        self.straight = True
        self.protected = set()  # loop counters the body must not assign
        self.loops = []         # stack of 'for' / 'while'
        self.iter_budget = 1    # product of enclosing loop trip counts
        pool = list(VAR_NAMES)
        rng.shuffle(pool)
        self.pool = pool[: rng.randint(3, 10)]
        self.reuse = 0.55       # chance of assigning an existing name rather than a new one
        if edge and rng.random() < 0.4:
            self.pool = pool[: rng.randint(11, 28)]
            self.reuse = 0.3

    # ------------------------------------------------------------ helpers
    def emit(self, depth, text):
        self.lines.append("    " * depth + text)

    def chance(self, p):
        return self.rng.random() < p

    def vars_of(self, kind, assignable=False):
        out = [v for v, k in self.vars.items() if k == kind]
        if assignable:
            out = [v for v in out if v not in self.protected]
        return out

    def fresh_or_existing(self, kind):
        existing = self.vars_of(kind, assignable=True)
        unused = [v for v in self.pool if v not in self.vars]
        if existing and (not unused or self.chance(self.reuse)):
            return self.rng.choice(existing)
        if unused:
            return unused[0]
        name = f"v{len(self.vars)}"
        self.pool.append(name)
        return name

    def set_var(self, name, kind, val):
        self.vars[name] = kind
        if self.straight and val is not None:
            self.known[name] = val
        else:
            self.known.pop(name, None)

    def enter_control_flow(self):
        self.straight = False
        self.known.clear()

    # ------------------------------------------------------------ int exprs
    def int_literal(self):
        v = small_int(self.rng)
        if self.chance(0.12):
            v = -v
            return Expr(str(v), UNARY, v, "int")
        return Expr(str(v), ATOM, v, "int")

    def int_leaf(self):
        ints = self.vars_of("int")
        if self.C and self.chance(0.12):
            e = self.str_to_int()
            if e is not None:
                return e
        if ints and self.chance(0.7):
            name = self.rng.choice(ints)
            return Expr(name, ATOM, self.known.get(name), "int")
        return self.int_literal()

    def str_to_int(self):
        strs = self.vars_of("str")
        if not strs:
            return None
        s = self.rng.choice(strs)
        known = self.known.get(s)
        return Expr(f"len({s})", ATOM, None if known is None else len(known), "int")

    def int_expr(self, depth=0, maxdepth=3):
        for _ in range(6):
            e = self._int_expr(depth, maxdepth)
            if _in_bound(e.val):
                return e
        return self.int_leaf()

    def _int_expr(self, depth, maxdepth):
        rng = self.rng
        if depth >= maxdepth or self.chance(0.35 + 0.2 * depth):
            return self.int_leaf()
        r = rng.random()
        if r < 0.08:
            inner = self.int_expr(depth + 1, maxdepth)
            if inner.val is not None and inner.src.lstrip("-").isdigit():
                inner = Expr(inner.src, ATOM, inner.val, "int")
            v = None if inner.val is None else -inner.val
            return Expr("-" + _wrap(inner, UNARY), UNARY, v, "int")
        op = rng.choices(["+", "-", "*", "//", "%"], self.op_weights)[0]
        a = self.int_expr(depth + 1, maxdepth)
        if op in ("//", "%"):
            b = self.divisor(depth, maxdepth)
        elif op == "*":
            b = self.int_expr(depth + 1, maxdepth) if self.chance(0.4) else self.small_operand()
        else:
            b = self.int_expr(depth + 1, maxdepth)
        prec = ADD if op in ("+", "-") else MUL
        val = None
        if a.val is not None and b.val is not None:
            if op in ("//", "%") and b.val == 0:
                return a
            val = {"+": a.val + b.val, "-": a.val - b.val, "*": a.val * b.val,
                   "//": a.val // b.val if b.val else 0, "%": a.val % b.val if b.val else 0}[op]
        src = f"{_wrap(a, prec)} {op} {_wrap(b, prec, right=True)}"
        if self.chance(0.05):
            src = f"({src})"
            prec = ATOM
        return Expr(src, prec, val, "int")

    def small_operand(self):
        if self.chance(0.6):
            v = self.rng.randint(2, 12)
            return Expr(str(v), ATOM, v, "int")
        return self.int_leaf()

    def divisor(self, depth, maxdepth):
        ints = [v for v in self.vars_of("int") if self.known.get(v) not in (None, 0)]
        if ints and self.chance(0.35):
            name = self.rng.choice(ints)
            return Expr(name, ATOM, self.known[name], "int")
        if self.arith and self.chance(0.7):
            v = self.rng.randint(2, 9) if self.chance(0.4) else self.rng.randint(10, 99)
        elif self.chance(0.7):
            v = self.rng.choice([2, 2, 3, 4, 5, 7, 10, 10, 12, 60, 100])
        else:
            v = self.rng.randint(1, 50)
        if self.chance(0.1):
            return Expr(f"-{v}", UNARY, -v, "int")
        return Expr(str(v), ATOM, v, "int")

    # ------------------------------------------------------------ bool exprs
    def comparison(self):
        rng = self.rng
        op = rng.choice(["<", "<=", "==", "!=", ">", ">="])
        if self.C and self.vars_of("str") and self.chance(0.2):
            s = rng.choice(self.vars_of("str"))
            other = self.str_expr(shallow=True)
            op = rng.choice(["==", "!=", "==", "<", ">"])
            return Expr(f"{s} {op} {_wrap(other, CMP + 1)}", CMP, None, "bool")
        if self.edge and self.chance(0.35):
            parts = [self.int_expr(1, 2) if self.chance(0.4) else self.int_leaf() for _ in range(rng.randint(3, 4))]
            src = _wrap(parts[0], CMP + 1) + "".join(
                f" {rng.choice(['<', '<=', '==', '!=', '>', '>='])} {_wrap(p, CMP + 1)}" for p in parts[1:])
            return Expr(src, CMP, None, "bool")
        a = self.int_expr(1, 2)
        if self.chance(0.12):
            lo = self.int_literal()
            hi = Expr(str(rng.randint(0, 30) + (lo.val or 0)), ATOM, None, "int")
            op2 = rng.choice(["<", "<="])
            return Expr(f"{_wrap(lo, CMP + 1)} {op2} {_wrap(a, CMP + 1)} {rng.choice(['<', '<='])} {hi.src}",
                        CMP, None, "bool")
        b = self.int_expr(1, 2) if self.chance(0.4) else self.int_literal()
        val = None
        if a.val is not None and b.val is not None:
            val = {"<": a.val < b.val, "<=": a.val <= b.val, "==": a.val == b.val,
                   "!=": a.val != b.val, ">": a.val > b.val, ">=": a.val >= b.val}[op]
        return Expr(f"{_wrap(a, CMP + 1)} {op} {_wrap(b, CMP + 1)}", CMP, val, "bool")

    def cond(self, depth=0):
        rng = self.rng
        r = rng.random()
        if depth < 2 and r < 0.12:
            c = self.cond(depth + 1)
            return Expr(f"not {_wrap(c, NOT)}", NOT, None if c.val is None else not c.val, "bool")
        if depth < 2 and r < 0.30:
            op = rng.choice(["and", "or"])
            a, b = self.cond(depth + 1), self.cond(depth + 1)
            prec = AND if op == "and" else OR
            return Expr(f"{_wrap(a, prec)} {op} {_wrap(b, prec, right=True)}", prec, None, "bool")
        if r < 0.40 and self.vars_of("bool"):
            name = rng.choice(self.vars_of("bool"))
            return Expr(name, ATOM, self.known.get(name), "bool")
        if r < 0.48:
            ints = self.vars_of("int")
            if ints:
                name = rng.choice(ints)
                if self.chance(0.5):
                    m = rng.choice([2, 3, 5])
                    return Expr(f"{name} % {m}", MUL, None, "int")
                return Expr(name, ATOM, None, "int")
        if r < 0.52 and self.C and self.vars_of("str"):
            return Expr(rng.choice(self.vars_of("str")), ATOM, None, "str")
        if r < 0.54:
            v = rng.choice(["True", "False"])
            return Expr(v, ATOM, v == "True", "bool")
        return self.comparison()

    # ------------------------------------------------------------ str exprs (phase C)
    def str_literal_expr(self):
        if self.edge and self.C and self.chance(0.06):
            return Expr("''", ATOM, "", "str")
        if self.edge and self.chance(0.55):
            self.series[1] += self.rng.choice([1, 1, 1, 2, 0])
            s = f"{self.series[0]} {self.series[1]}"
            if self.chance(0.3):
                s += self.rng.choice([": ", " - ", " "]) + self.rng.choice(WORDS)
            return Expr(repr(s), ATOM, s, "str")
        s = pattern_text(self.rng) if self.copy and self.chance(0.6) else string_literal(self.rng)
        return Expr(repr(s), ATOM, s, "str")

    def str_expr(self, shallow=False):
        rng = self.rng
        strs = self.vars_of("str")
        r = rng.random()
        if shallow or r < 0.25:
            if strs and self.chance(0.5):
                name = rng.choice(strs)
                return Expr(name, ATOM, self.known.get(name), "str")
            return self.str_literal_expr()
        if r < 0.45:
            a = self.str_expr(shallow=True)
            b = self.str_expr(shallow=True)
            val = a.val + b.val if a.val is not None and b.val is not None else None
            return Expr(f"{_wrap(a, ADD)} + {_wrap(b, ADD, True)}", ADD, val, "str")
        if r < 0.55:
            a = self.str_expr(shallow=True)
            n = rng.randint(0, 6)
            val = a.val * n if a.val is not None else None
            if self.chance(0.5):
                return Expr(f"{_wrap(a, MUL)} * {n}", MUL, val, "str")
            return Expr(f"{n} * {_wrap(a, MUL, True)}", MUL, val, "str")
        if r < 0.70:
            return self.fstring()
        if r < 0.82:
            e = self.int_expr(1, 2)
            val = None if e.val is None else str(e.val)
            return Expr(f"str({e.src})", ATOM, val, "str")
        if strs:
            name = rng.choice(strs)
            known = self.known.get(name)
            if known:
                i = rng.randrange(-len(known), len(known))
                return Expr(f"{name}[{i}]", ATOM, known[i], "str")
            if known is None:
                return Expr(f"{name}[0]", ATOM, None, "str")
        return self.str_literal_expr()

    def fstring(self):
        rng = self.rng
        parts, srcs, known = [], [], True
        for _ in range(rng.randint(1, 6) if self.edge else rng.randint(1, 3)):
            if self.chance(0.7):
                text = rng.choice(WORDS + ["=", ":", " is ", " -> ", ", ", " + ", "#"]) if self.chance(0.8) else random_text(rng, 1, 5)
                text = "".join(ch for ch in text if ch not in '{}"\\\n\t')
                parts.append(text)
                srcs.append(text)
            if self.chance(0.65) or not self.vars_of("str"):
                e = self.int_expr(1, 2)
            else:
                name = rng.choice(self.vars_of("str"))
                e = Expr(name, ATOM, self.known.get(name), "str")
            srcs.append("{" + e.src + "}")
            if e.val is None:
                known = False
            else:
                parts.append(str(e.val))
        if self.chance(0.4):
            tail = rng.choice(["!", ".", "", " done", "?"])
            parts.append(tail)
            srcs.append(tail)
        return Expr('f"' + "".join(srcs) + '"', ATOM, "".join(parts) if known else None, "str")

    def sep_text(self, end=False):
        """For the edge drill, a print sep or end from the wide set (it may be
        ''); None means the standard choice."""
        if not self.edge or not self.chance(0.7):
            return None
        rng = self.rng
        if self.chance(0.35):
            return random_text(rng, 1, 4)
        s = rng.choice(SEPS)
        return s + "\n" if end and self.chance(0.4) else s

    def _kw(self, chosen, standard):
        return self.rng.choice(standard) if chosen is None else chosen

    # ------------------------------------------------------------ statements
    def print_stmt(self, depth):
        rng = self.rng
        if self.C and self.chance(0.45):
            n = rng.randint(0, 10) if self.edge else rng.randint(2, 4)
            args = []
            for _ in range(n):
                k = rng.random()
                if k < 0.35:
                    args.append(self.str_literal_expr().src)
                elif k < 0.55 and self.vars_of("str"):
                    args.append(rng.choice(self.vars_of("str")))
                elif k < 0.65:
                    args.append(self.cond().src)
                else:
                    args.append(self.int_expr(1, 2).src)
            kw = []
            if self.chance(0.25):
                kw.append(f"sep={self._kw(self.sep_text(), ['', ', ', '-', ' | ', ':', chr(9)])!r}")
            if self.chance(0.3):
                kw.append(f"end={self._kw(self.sep_text(end=True), ['', ' ', ', ', '!' + chr(10), chr(10) + chr(10), ';'])!r}")
            self.emit(depth, f"print({', '.join(args + kw)})")
            return
        r = rng.random()
        if r < 0.04:
            self.emit(depth, "print()")
        elif r < (0.65 if self.copy else 0.35 if self.edge else 0.20):
            self.emit(depth, f"print({self.str_literal_expr().src})")
        elif self.B and r < 0.30:
            self.emit(depth, f"print({self.cond().src})")
        elif self.C and r < 0.50:
            e = self.str_expr()
            if self.chance(0.3):
                self.emit(depth, f"print({e.src}, end={rng.choice(['', ' ', ', '])!r})")
            else:
                self.emit(depth, f"print({e.src})")
        else:
            ints = self.vars_of("int")
            if ints and self.chance(0.5):
                self.emit(depth, f"print({rng.choice(ints)})")
            else:
                self.emit(depth, f"print({self.int_expr().src})")

    def assign_int(self, depth):
        rng = self.rng
        ints = self.vars_of("int", assignable=True)
        if ints and self.chance(0.3):
            name = rng.choice(ints)
            if self.arith:
                weights = [10, 8, 12, 35, 35]
            else:
                weights = [40, 25, 10, 12, 13] if self.straight else [40, 25, 4, 12, 19]
            op = rng.choices(["+", "-", "*", "//", "%"], weights)[0]
            rhs = self.divisor(1, 2) if op in ("//", "%") else (self.small_operand() if op == "*" else self.int_expr(1, 2))
            cur = self.known.get(name)
            val = None
            if cur is not None and rhs.val is not None:
                if op in ("//", "%") and rhs.val == 0:
                    return
                val = {"+": cur + rhs.val, "-": cur - rhs.val, "*": cur * rhs.val,
                       "//": cur // rhs.val if rhs.val else 0, "%": cur % rhs.val if rhs.val else 0}[op]
                if not _in_bound(val):
                    return
            self.emit(depth, f"{name} {op}= {rhs.src}")
            self.set_var(name, "int", val)
            return
        r = rng.random()
        if r < 0.06 and len(self.vars_of("int", True)) >= 2:
            a, b = rng.sample(self.vars_of("int", True), 2)
            self.emit(depth, f"{a}, {b} = {b}, {a}")
            ka, kb = self.known.get(a), self.known.get(b)
            self.set_var(a, "int", kb)
            self.set_var(b, "int", ka)
            return
        if r < 0.11:
            a = self.fresh_or_existing("int")
            b = self.fresh_or_existing("int")
            if a == b:
                b = next((v for v in self.pool if v not in self.vars and v != a), None)
                if b is None:
                    return
            e1, e2 = self.int_expr(1, 2), self.int_expr(1, 2)
            if self.chance(0.5):
                self.emit(depth, f"{a}, {b} = {e1.src}, {e2.src}")
                self.set_var(a, "int", e1.val)
                self.set_var(b, "int", e2.val)
            else:
                self.emit(depth, f"{a} = {b} = {e1.src}")
                self.set_var(a, "int", e1.val)
                self.set_var(b, "int", e1.val)
            return
        name = self.fresh_or_existing("int")
        e = self.int_expr() if self.straight else self.int_expr(1, 3)
        self.emit(depth, f"{name} = {e.src}")
        self.set_var(name, "int", e.val)

    def tuple_assign(self, depth):
        """Two or three names reassigned at once, as people shuffle values:
        `a, b, c = c, a, b` (SWAP 3), `x, y = y, x % y` (SWAP 2)."""
        rng = self.rng
        ints = self.vars_of("int", assignable=True)
        k = 3 if len(ints) >= 3 and self.chance(0.7) else 2
        if len(ints) < k:
            return self.assign_int(depth)
        targets = rng.sample(ints, k)
        order = targets[:]
        while order == targets:
            rng.shuffle(order)
        rhs = [Expr(v, ATOM, self.known.get(v), "int") for v in order]
        if self.chance(0.4):
            rhs[rng.randrange(k)] = self.int_expr(1, 2)
        self.emit(depth, f"{', '.join(targets)} = {', '.join(e.src for e in rhs)}")
        for name, e in zip(targets, rhs):
            self.set_var(name, "int", e.val)

    def chain_assign(self, depth):
        """One value bound to many names: `a = b = c = d = "."` (COPY 1 each)."""
        rng = self.rng
        kind = "str" if self.C and self.chance(0.5) else "int"
        names = []
        for _ in range(rng.randint(2, 9)):
            unused = [v for v in self.pool if v not in self.vars and v not in names]
            existing = [v for v in self.vars_of(kind, assignable=True) if v not in names]
            if unused and (not existing or self.chance(0.6)):
                names.append(unused[0])
            elif existing:
                names.append(rng.choice(existing))
        if len(names) < 2:
            return
        if kind == "str":
            e = self.str_literal_expr() if self.chance(0.7) else self.str_expr(shallow=True)
            if e.val is not None and len(e.val) > config.MAX_STR_LEN:
                return
        else:
            e = self.int_expr(1, 2)
        self.emit(depth, " = ".join(names) + f" = {e.src}")
        for v in names:
            self.set_var(v, kind, e.val)

    def pad_stmt(self, depth):
        """Fixed-width text, as tables and ASCII art are built:
        `" " * (w - len(s)) + s`, `s + "." * (12 - len(s)) + "|"`, `"-" * w`."""
        rng = self.rng
        strs = self.vars_of("str")
        if not strs or self.chance(0.3):
            s = self.fresh_or_existing("str")
            if s in self.protected:
                return
            e = self.str_literal_expr() if self.chance(0.6) else Expr(repr(rng.choice(WORDS)), ATOM, None, "str")
            self.emit(depth, f"{s} = {e.src}")
            self.set_var(s, "str", e.val)
        else:
            s = rng.choice(strs)
        fill = repr(rng.choice([" ", " ", " ", ".", "-", "*", "#", "=", "_", "0", "~"]))
        w = rng.randint(4, 24)
        pad = f"{fill} * ({w} - len({s}))"
        r = rng.random()
        if r < 0.3:
            e = f"{pad} + {s}"
        elif r < 0.6:
            e = f"{s} + {pad} + {rng.choice(['|', ':', ' |', ''])!r}"
        elif r < 0.75:
            e = f"{rng.choice(['|', '[', '', '# '])!r} + {pad} + {s}"
        elif r < 0.9:
            e = f"{fill} * {w}"
        else:
            e = f"{s} + {pad} + {rng.choice(['|', ''])!r} + {fill} * {rng.randint(0, 6)}"
        if self.chance(0.6):
            self.emit(depth, f"print({e})")
            return
        t = self.fresh_or_existing("str")
        if t in self.protected:
            return
        self.emit(depth, f"{t} = {e}")
        self.set_var(t, "str", None)
        self.emit(depth, f"print({t}, len({t}))" if self.chance(0.3) else f"print({t})")

    def assign_bool(self, depth):
        name = self.fresh_or_existing("bool")
        c = self.cond()
        self.emit(depth, f"{name} = {c.src}")
        self.set_var(name, "bool", c.val if c.kind == "bool" else None)

    def assign_str(self, depth):
        rng = self.rng
        strs = self.vars_of("str", assignable=True)
        if strs and self.chance(0.3):
            name = rng.choice(strs)
            if self.loops:
                s = rng.choice(["*", "-", "#", ".", "ab", " ", "x", "=", "o", "|"])
                rhs = Expr(repr(s), ATOM, s, "str") if self.chance(0.7) else Expr(f"str({rng.choice(self.vars_of('int') or ['0'])})", ATOM, None, "str")
            else:
                rhs = self.str_expr(shallow=True) if self.chance(0.5) else self.fstring()
            cur = self.known.get(name)
            val = cur + rhs.val if cur is not None and rhs.val is not None else None
            self.emit(depth, f"{name} += {rhs.src}")
            self.set_var(name, "str", val)
            return
        name = self.fresh_or_existing("str")
        e = self.str_expr()
        if e.val is not None and len(e.val) > config.MAX_STR_LEN:
            e = self.str_literal_expr()
        self.emit(depth, f"{name} = {e.src}")
        self.set_var(name, "str", e.val)

    def logic_value(self, depth=0):
        """and/or used for their value, with int operands: `a or 7`, `n and n - 1 or 9`."""
        if depth >= 2 or self.chance(0.35):
            return Expr("0", ATOM, 0, "int") if self.chance(0.25) else self.int_expr(1, 2)
        op = self.rng.choice(["and", "or"])
        a, b = self.logic_value(depth + 1), self.logic_value(depth + 1)
        prec = AND if op == "and" else OR
        return Expr(f"{_wrap(a, prec)} {op} {_wrap(b, prec, right=True)}", prec, None, "int")

    def logic_stmt(self, depth):
        r = self.rng.random()
        if r < 0.45:
            name = self.fresh_or_existing("int")
            e = self.logic_value()
            self.emit(depth, f"{name} = {e.src}")
            self.set_var(name, "int", None)
        elif r < 0.85:
            self.emit(depth, f"print({self.logic_value().src})")
        else:
            ints = self.vars_of("int")
            self.emit(depth, f"print(not {self.rng.choice(ints) if ints else self.int_literal().src})")

    def boolish(self):
        """A bool of the kind people go on to count or compare: a bool name,
        `not x`, or a comparison."""
        rng = self.rng
        bools = self.vars_of("bool")
        r = rng.random()
        if bools and r < 0.35:
            return Expr(rng.choice(bools), ATOM, None, "bool")
        if r < 0.6:
            return Expr(f"not {_wrap(self.int_leaf(), NOT)}", NOT, None, "bool")
        a, b = self.int_leaf(), self.int_leaf()
        return Expr(f"{a.src} {rng.choice(['<', '>', '==', '!=', '<=', '>='])} {b.src}", CMP, None, "bool")

    def bool_arith(self, depth):
        """Bools used as numbers: `print(t == 1)`, `print((not a) + (not b))`,
        `n += i > 0`, `f = g = a > b`."""
        rng = self.rng
        a = self.boolish()
        r = rng.random()
        if r < 0.35:
            b = self.boolish() if self.chance(0.5) else Expr(str(rng.choice([0, 1, 1, 2])), ATOM, None, "int")
            self.emit(depth, f"print({_wrap(a, CMP + 1)} {rng.choice(['==', '!=', '<', '>'])} {_wrap(b, CMP + 1)})")
        elif r < 0.65:
            b = self.boolish() if self.chance(0.6) else self.int_leaf()
            op = rng.choice(["+", "-", "*"])
            prec = MUL if op == "*" else ADD
            e = f"{_wrap(a, prec)} {op} {_wrap(b, prec, right=True)}"
            if self.chance(0.5):
                self.emit(depth, f"print({e})")
            else:
                name = self.fresh_or_existing("int")
                self.emit(depth, f"{name} = {e}")
                self.set_var(name, "int", None)
        elif r < 0.85 and self.vars_of("int", assignable=True):
            name = rng.choice(self.vars_of("int", assignable=True))
            self.emit(depth, f"{name} {rng.choice(['+=', '+=', '-='])} {a.src}")
            self.set_var(name, "int", None)
        else:
            f = self.fresh_or_existing("bool")
            g = next((v for v in self.pool if v not in self.vars and v != f), None)
            if g is None:
                return
            self.emit(depth, f"{f} = {g} = {a.src}")
            self.set_var(f, "bool", None)
            self.set_var(g, "bool", None)
            self.emit(depth, f"print({f} {rng.choice(['==', '+', '!='])} {g})")

    def ifexp_assign(self, depth):
        name = self.fresh_or_existing("int")
        c = self.cond()
        a, b = self.int_expr(1, 2), self.int_expr(1, 2)
        self.emit(depth, f"{name} = {_wrap(a, IFEXP + 1)} if {_wrap(c, IFEXP + 1)} else {_wrap(b, IFEXP)}")
        self.set_var(name, "int", None)

    def simple_stmt(self, depth):
        rng = self.rng
        weights = {"print": 30, "int": 45}
        if self.B:
            weights.update(bool=6, ifexp=3, passs=1)
        if self.C:
            weights.update(str=35, print=40)
        if self.edge:
            weights.update(tuple=8, chain=4)
        if self.edge and self.C:
            weights.update(pad=10)
        if self.edge and self.B:
            weights.update(logic=25, boolmix=12)
        if self.chance(0.02):
            e = self.int_expr(1, 2)
            self.emit(depth, e.src)  # expression statement, value discarded
            return
        kind = rng.choices(list(weights), list(weights.values()))[0]
        if kind == "print":
            self.print_stmt(depth)
        elif kind == "int":
            self.assign_int(depth)
        elif kind == "bool":
            self.assign_bool(depth)
        elif kind == "str":
            self.assign_str(depth)
        elif kind == "ifexp":
            self.ifexp_assign(depth)
        elif kind == "logic":
            self.logic_stmt(depth)
        elif kind == "tuple":
            self.tuple_assign(depth)
        elif kind == "boolmix":
            self.bool_arith(depth)
        elif kind == "chain":
            self.chain_assign(depth)
        elif kind == "pad":
            self.pad_stmt(depth)
        else:
            self.emit(depth, "pass")

    # ------------------------------------------------------------ control flow (phase B+)
    def block(self, depth, n):
        """Emit a non-empty block. Names first bound inside it may be unbound
        afterwards (a branch not taken, a loop that never ran), so they go out
        of scope for the generator when the block ends."""
        before = set(self.vars)
        start = len(self.lines)
        for _ in range(n):
            self.stmt(depth)
        if len(self.lines) == start:
            self.emit(depth, "pass")
        for name in set(self.vars) - before:
            if name not in self.protected:
                del self.vars[name]

    def stmt(self, depth):
        rng = self.rng
        if self.edge and self.C and self.iter_budget == 1 and self.chance(0.2):
            return self.str_walk(depth)
        if self.B and depth < 3:
            r = rng.random() * (1 + depth)
            in_loop = bool(self.loops)
            if r < 0.16:
                return self.if_stmt(depth)
            if r < 0.24 and self.iter_budget <= 12:
                return self.for_stmt(depth)
            if r < 0.28 and self.iter_budget <= 12:
                return self.while_stmt(depth)
            if in_loop and r < 0.33:
                return self.break_continue(depth)
        self.simple_stmt(depth)

    def if_stmt(self, depth):
        self.enter_control_flow()
        rng = self.rng
        self.emit(depth, f"if {self.cond().src}:")
        self.block(depth + 1, rng.randint(1, 2))
        for _ in range(rng.choices([0, 1, 2], [65, 28, 7])[0]):
            self.emit(depth, f"elif {self.cond().src}:")
            self.block(depth + 1, rng.randint(1, 2))
        if self.chance(0.45):
            self.emit(depth, "else:")
            self.block(depth + 1, rng.randint(1, 2))

    def break_continue(self, depth):
        kind = self.loops[-1]
        self.emit(depth, f"if {self.cond().src}:")
        if kind == "for" and self.chance(0.4):
            self.emit(depth + 1, "continue")
        else:
            self.emit(depth + 1, "break")

    def range_args(self):
        rng = self.rng
        r = rng.random()
        if self.edge and r < 0.5:
            step = rng.randint(1, 25) * rng.choice([1, 1, -1])
            n = rng.randint(0, 10)
            a = rng.randint(-100, 400)
            b = a + step * n + (rng.randint(0, abs(step) - 1) * (1 if step > 0 else -1))
            return f"{a}, {b}, {step}", n + 1
        if r < 0.4:
            n = rng.randint(0, 10)
            return f"{n}", n
        if r < 0.75:
            a = rng.randint(-5, 20) if self.chance(0.8) else rng.randint(-200, 900)
            n = rng.randint(0, 10)
            b = a + n if self.chance(0.92) else a - rng.randint(1, 3)
            return f"{a}, {b}", max(0, b - a)
        step = rng.choice([2, 3, 5, -1, -1, -2, -3, 10])
        n = rng.randint(0, 9)
        a = rng.randint(-10, 30) if self.chance(0.8) else rng.randint(-200, 900)
        b = a + step * n + (rng.randint(0, abs(step) - 1) * (1 if step > 0 else -1) if abs(step) > 1 else 0)
        return f"{a}, {b}, {step}", n

    def loop_var(self):
        unused = [v for v in self.pool if v not in self.vars]
        name = unused[0] if unused else self.rng.choice(["i", "j", "k", "n"])
        return name

    def for_stmt(self, depth):
        self.enter_control_flow()
        rng = self.rng
        args, trips = self.range_args()
        var = self.loop_var()
        if var in self.protected:
            return
        self.emit(depth, f"for {var} in range({args}):")
        self.vars[var] = "int"
        self.protected.add(var)
        self.loops.append("for")
        saved = self.iter_budget
        self.iter_budget *= max(1, trips)
        self.block(depth + 1, rng.randint(1, 3))
        self.iter_budget = saved
        self.loops.pop()
        self.protected.discard(var)
        if not trips:
            self.vars.pop(var, None)

    # string walks: (range arguments, index expressions safe for that range)
    WALKS = [
        ("len({s})", ["{i}", "{i}", "-1 - {i}", "len({s}) - 1 - {i}", "{i} - 1", "-({i} + 1)", "({i} + {k}) % len({s})"]),
        ("len({s}) - 1", ["{i}", "{i} + 1", "-1 - {i}", "{i} - 1"]),
        ("1, len({s})", ["{i}", "{i} - 1", "-{i}"]),
        ("len({s}) - 1, -1, -1", ["{i}", "-1 - {i}"]),
        ("0, len({s}), {k}", ["{i}", "-1 - {i}"]),
    ]

    def str_walk(self, depth):
        """A loop over a string's positions, the way people index strings
        (strings are not iterable yet): `for i in range(len(s)):` with s[i],
        s[-1 - i], s[len(s) - 1 - i], counting matches, building a string,
        checking a palindrome; or the same as a while loop."""
        rng = self.rng
        strs = self.vars_of("str")
        if not strs or self.chance(0.3):
            s = self.fresh_or_existing("str")
            e = self.str_literal_expr()
            self.emit(depth, f"{s} = {e.src}")
            self.set_var(s, "str", e.val)
        else:
            s = rng.choice(strs)
        known = self.known.get(s)
        i = self.loop_var()
        if i in self.protected or i == s:
            return
        self.vars[i] = "int"    # so the names chosen below differ from it
        self.protected.add(i)
        use_while = self.chance(0.2)
        rargs, idxs = self.WALKS[0] if use_while else rng.choice(self.WALKS)
        k = rng.randint(2, 3)

        def idx():
            return f"{s}[{rng.choice(idxs).format(s=s, i=i, k=rng.randint(1, 9))}]"

        def char():
            c = rng.choice(known) if known and self.chance(0.7) else rng.choice("aeiou st.,-")
            return repr(c)

        before, body, after = [], [], []
        for kind in rng.sample(["count", "build", "show", "pair", "palindrome"], rng.choice([1, 1, 2])):
            if kind == "count":
                c = self.fresh_or_existing("int")
                before.append(f"{c} = 0")
                body += [f"if {idx()} {rng.choice(['==', '==', '!='])} {char()}:", f"    {c} += 1"]
                after.append(f"print({c})")
                self.set_var(c, "int", None)
            elif kind == "build":
                t = self.fresh_or_existing("str")
                if t == s:
                    continue
                before.append(f"{t} = " + rng.choice(["''", "''", "'>'"]))
                body.append(rng.choice([f"{t} = {t} + {idx()}", f"{t} = {idx()} + {t}", f"{t} += {idx()}"]))
                after.append(f"print({t})")
                self.set_var(t, "str", None)
            elif kind == "show":
                body.append(rng.choice([f"print({i}, {idx()})", f"print({idx()}, end='')", f"print(f'{{{i}}}: {{{idx()}}}')",
                                        f"print({idx()}, {idx()}, sep='')"]))
                if "end=''" in body[-1]:
                    after.append("print()")
            elif kind == "pair":
                c = self.fresh_or_existing("int")
                before.append(f"{c} = 0")
                body += [f"if {idx()} == {idx()}:", f"    {c} += 1"]
                after.append(f"print({c})")
                self.set_var(c, "int", None)
            else:
                f = self.fresh_or_existing("bool")
                before.append(f"{f} = True")
                body += [f"if {s}[{i}] != {s}[-1 - {i}]:", f"    {f} = False"]
                after.append(f"print({f})")
                self.set_var(f, "bool", None)
        if not body:
            self.protected.discard(i)
            self.vars.pop(i, None)
            return
        self.enter_control_flow()
        for line in before:
            self.emit(depth, line)
        if use_while:
            self.emit(depth, f"{i} = 0")
            self.emit(depth, f"while {i} < len({s}):")
            body.append(f"{i} += {rng.choice([1, 1, 1, 2])}")
        else:
            self.emit(depth, f"for {i} in range({rargs.format(s=s, k=k)}):")
        for line in body:
            self.emit(depth + 1, line)
        for line in after:
            self.emit(depth, line)
        self.protected.discard(i)
        self.vars.pop(i, None)

    def while_stmt(self, depth):
        self.enter_control_flow()
        rng = self.rng
        var = self.loop_var()
        if var in self.protected:
            return
        shape = rng.random()
        saved = self.iter_budget
        self.loops.append("while")
        self.protected.add(var)
        if shape < 0.5:
            start = rng.randint(-5, 10)
            trips = rng.randint(0, 10)
            step = rng.choice([1, 1, 1, 2, 3])
            stop = start + trips * step
            op = rng.choice(["<", "<=", "!="]) if step == 1 else "<"
            if op == "<=":
                stop -= 1
            self.emit(depth, f"{var} = {start}")
            self.vars[var] = "int"
            self.emit(depth, f"while {var} {op} {stop}:")
            self.iter_budget *= max(1, trips)
            self.block(depth + 1, rng.randint(1, 3))
            self.emit(depth + 1, f"{var} += {step}")
        elif shape < 0.75:
            n = rng.randint(1, 999)
            base = rng.choice([10, 10, 2, 3, 8])
            self.emit(depth, f"{var} = {n}")
            self.vars[var] = "int"
            self.emit(depth, f"while {var} > 0:" if self.chance(0.7) else f"while {var}:")
            self.iter_budget *= 10
            self.block(depth + 1, rng.randint(1, 3))
            self.emit(depth + 1, f"{var} //= {base}")
        else:
            limit = rng.randint(1, 10)
            self.emit(depth, f"{var} = 0")
            self.vars[var] = "int"
            self.emit(depth, "while True:")
            self.iter_budget *= limit
            self.emit(depth + 1, f"{var} += 1")
            self.block(depth + 1, rng.randint(1, 3))
            self.emit(depth + 1, f"if {var} >= {limit}:")
            self.emit(depth + 2, "break")
        self.iter_budget = saved
        self.loops.pop()
        self.protected.discard(var)

    # ------------------------------------------------------------ top level
    def script(self):
        rng = self.rng
        if self.phase == "A":
            n = rng.randint(10, 45) if self.edge else rng.randint(2, 18)
        else:
            n = rng.randint(2, 8)
        # seed a few variables so expressions have something to refer to
        if len(self.pool) > 10:
            # many names: declare a run of them up front, as long hand-written scripts do
            for name in self.pool[: rng.randint(len(self.pool) // 2, len(self.pool))]:
                e = self.int_literal() if self.chance(0.6) else self.int_expr(1, 2)
                self.emit(0, f"{name} = {e.src}")
                self.set_var(name, "int", e.val)
        else:
            for _ in range(rng.randint(1, 3)):
                self.assign_int(0)
        if self.C:
            for _ in range(rng.randint(1, 2)):
                self.assign_str(0)
        for _ in range(n):
            self.stmt(0)
        if not any("print(" in line for line in self.lines):
            self.print_stmt(0)
        return "\n".join(self.lines) + "\n"


def generate(rng, phase, arith=False, copy=False, edge=False):
    return Gen(rng, phase, arith, copy, edge).script()
