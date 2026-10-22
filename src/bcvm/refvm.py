"""Reference interpreter for the supported subset of CPython 3.14 bytecode.

`step(program, state)` executes exactly one instruction and returns the next
state plus whatever that instruction printed. `run` drives it to completion
and keeps every state; that trace is the source of all training labels and is
checked against real CPython by `check.py`.

Arithmetic, comparison and str() are delegated to Python on plain values, so
they match CPython by construction; what this module has to get right is
stack discipline and control flow.
"""
from dataclasses import dataclass

from . import config
from .state import State
from .values import (NULL, Builtin, LimitExceeded, PyError, RangeIter, RangeObj,
                     Unsupported, is_int, py_str)

_SCALAR = (int, bool, str, type(None))


def _scalar(v):
    if type(v) not in _SCALAR:
        raise Unsupported(f"operand of type {type(v).__name__}")
    return v


def _binop(op, a, b):
    _scalar(a)
    _scalar(b)
    base = op[:-1] if op.endswith("=") and op not in ("==",) else op
    try:
        if base == "+":
            if type(a) is str or type(b) is str:
                if not (type(a) is str and type(b) is str):
                    raise PyError("TypeError", "can only concatenate str to str")
            return a + b
        if base == "-":
            if type(a) is str or type(b) is str:
                raise PyError("TypeError", "unsupported operand for -")
            return a - b
        if base == "*":
            if type(a) is str and type(b) is str:
                raise PyError("TypeError", "can't multiply sequence by str")
            if (a is None) or (b is None):
                raise PyError("TypeError", "unsupported operand for *")
            return a * b
        if base in ("//", "%"):
            if type(a) is str or type(b) is str:
                # str % x is printf-style formatting, which we don't model
                raise Unsupported(f"{base} with a str operand")
            return a // b if base == "//" else a % b
        if base == "[]":
            if type(a) is not str:
                raise Unsupported(f"subscript of {type(a).__name__}")
            if not is_int(b):
                raise PyError("TypeError", "string indices must be integers")
            return a[b]
    except ZeroDivisionError:
        raise PyError("ZeroDivisionError") from None
    except IndexError:
        raise PyError("IndexError") from None
    except TypeError as e:
        raise PyError("TypeError", str(e)) from None
    raise Unsupported(f"BINARY_OP {op}")


def _compare(op, a, b):
    _scalar(a)
    _scalar(b)
    try:
        if op == "<":
            return a < b
        if op == "<=":
            return a <= b
        if op == "==":
            return a == b
        if op == "!=":
            return a != b
        if op == ">":
            return a > b
        if op == ">=":
            return a >= b
    except TypeError as e:
        raise PyError("TypeError", str(e)) from None
    raise Unsupported(f"COMPARE_OP {op}")


def _truth(v):
    if type(v) in _SCALAR:
        return bool(v)
    raise Unsupported(f"truth value of {type(v).__name__}")


def _call_builtin(name, args, kwargs):
    """Returns (result, printed text)."""
    if name == "print":
        sep, end = " ", "\n"
        for k, v in kwargs.items():
            if k not in ("sep", "end"):
                raise Unsupported(f"print keyword {k}")
            if v is not None and type(v) is not str:
                raise PyError("TypeError", f"{k} must be None or a string")
            if v is not None:
                if k == "sep":
                    sep = v
                else:
                    end = v
        return None, sep.join(py_str(a) for a in args) + end
    if kwargs:
        raise Unsupported(f"keyword arguments to {name}")
    if name == "range":
        if not 1 <= len(args) <= 3:
            raise PyError("TypeError", "range expected 1 to 3 arguments")
        if not all(is_int(a) for a in args):
            raise PyError("TypeError", "range arguments must be ints")
        if len(args) == 3 and args[2] == 0:
            raise PyError("ValueError", "range() arg 3 must not be zero")
        r = range(*args)
        return RangeObj(r.start, r.stop, r.step), ""
    if name == "len":
        if len(args) != 1:
            raise PyError("TypeError", "len takes one argument")
        (a,) = args
        if type(a) is str:
            return len(a), ""
        if type(a) is RangeObj:
            return len(range(a.start, a.stop, a.step)), ""
        raise PyError("TypeError", "object has no len()")
    if name == "str":
        if len(args) > 1:
            raise Unsupported("str() with encoding arguments")
        return (py_str(args[0]) if args else ""), ""
    raise Unsupported(f"builtin {name}")


def _do_call(func, self_or_null, args, kwargs):
    if self_or_null is not NULL:
        raise Unsupported("method calls")
    if type(func) is not Builtin:
        raise PyError("TypeError", "object is not callable") if type(func) in _SCALAR else Unsupported("callable")
    return _call_builtin(func.name, args, kwargs)


def step(prog, st):
    """Execute the instruction at st.ip. Returns (next State, printed text)."""
    ins = prog.instrs[st.ip]
    op = ins.opname
    stack = list(st.stack)
    names = st.names
    ip = st.ip + 1
    out = ""

    if op in ("RESUME", "NOP", "NOT_TAKEN"):
        pass
    elif op == "LOAD_SMALL_INT" or op == "LOAD_CONST":
        stack.append(ins.arg)
    elif op == "LOAD_NAME":
        kind, key = ins.arg
        if kind == "N":
            if key not in names:
                raise PyError("NameError", prog.names[key])
            stack.append(names[key])
        else:
            stack.append(Builtin(key))
    elif op == "STORE_NAME":
        kind, key = ins.arg
        if kind != "N":
            raise Unsupported(f"assignment to builtin {key}")
        names = dict(names)
        names[key] = stack.pop()
    elif op == "POP_TOP":
        stack.pop()
    elif op == "PUSH_NULL":
        stack.append(NULL)
    elif op == "COPY":
        stack.append(stack[-ins.arg])
    elif op == "SWAP":
        n = ins.arg
        stack[-1], stack[-n] = stack[-n], stack[-1]
    elif op == "BINARY_OP":
        b = stack.pop()
        a = stack.pop()
        stack.append(_binop(ins.arg, a, b))
    elif op == "UNARY_NEGATIVE":
        v = stack.pop()
        if not is_int(v):
            raise PyError("TypeError", "bad operand type for unary -") if type(v) in _SCALAR else Unsupported("unary -")
        stack.append(-v)
    elif op == "UNARY_NOT":
        stack.append(not _truth(stack.pop()))
    elif op == "TO_BOOL":
        stack.append(_truth(stack.pop()))
    elif op == "COMPARE_OP":
        b = stack.pop()
        a = stack.pop()
        stack.append(_compare(ins.arg, a, b))
    elif op == "POP_JUMP_IF_FALSE":
        if not _truth(stack.pop()):
            ip = ins.arg
    elif op == "POP_JUMP_IF_TRUE":
        if _truth(stack.pop()):
            ip = ins.arg
    elif op in ("JUMP_FORWARD", "JUMP_BACKWARD"):
        ip = ins.arg
    elif op == "GET_ITER":
        v = stack.pop()
        if type(v) is RangeObj:
            stack.append(RangeIter(v.start, v.stop, v.step))
        elif type(v) is RangeIter:
            stack.append(v)
        elif type(v) in (int, bool, type(None)):
            raise PyError("TypeError", "object is not iterable")
        else:
            raise Unsupported(f"iteration over {type(v).__name__}")
    elif op == "FOR_ITER":
        it = stack[-1]
        if type(it) is not RangeIter:
            raise Unsupported(f"FOR_ITER over {type(it).__name__}")
        if it.has_next():
            stack[-1] = RangeIter(it.next + it.step, it.stop, it.step)
            stack.append(it.next)
        else:
            ip = ins.arg
    elif op in ("END_FOR", "POP_ITER"):
        stack.pop()
    elif op == "CALL":
        n = ins.arg
        args = stack[len(stack) - n:]
        self_or_null = stack[-n - 1]
        func = stack[-n - 2]
        del stack[len(stack) - n - 2:]
        result, out = _do_call(func, self_or_null, args, {})
        stack.append(result)
    elif op == "CALL_KW":
        n = ins.arg
        kwnames = stack.pop()
        args = stack[len(stack) - n:]
        self_or_null = stack[-n - 1]
        func = stack[-n - 2]
        del stack[len(stack) - n - 2:]
        npos = n - len(kwnames)
        result, out = _do_call(func, self_or_null, args[:npos], dict(zip(kwnames, args[npos:])))
        stack.append(result)
    elif op == "FORMAT_SIMPLE":
        stack.append(py_str(stack.pop()))
    elif op == "BUILD_STRING":
        n = ins.arg
        parts = stack[len(stack) - n:]
        del stack[len(stack) - n:]
        stack.append("".join(parts))
    else:
        raise Unsupported(f"opcode {op}")
    return State(ip, tuple(stack), names), out


def is_halt(prog, st):
    return prog.instrs[st.ip].opname == "RETURN_VALUE"


def _check_value(v, bound):
    t = type(v)
    if t is int:
        if not -bound <= v <= bound:
            raise LimitExceeded(f"int {v} beyond bound {bound}")
    elif t is str:
        if len(v) > config.MAX_STR_LEN:
            raise LimitExceeded(f"string of length {len(v)}")
    elif t is RangeObj:
        _check_value(v.start, bound)
        _check_value(v.stop, bound)
        _check_value(v.step, bound)
    elif t is RangeIter:
        _check_value(v.next, bound)
        _check_value(v.stop, bound)
        _check_value(v.step, bound)
    elif t is tuple:
        for x in v:
            _check_value(x, bound)


def check_limits(st, bound=config.INT_BOUND):
    """Values only enter the state by being pushed, so checking the stack suffices."""
    if len(st.stack) > config.MAX_STACK:
        raise LimitExceeded("stack too deep")
    for v in st.stack:
        _check_value(v, bound)


def check_constants(prog, bound=config.INT_BOUND):
    for ins in prog.instrs:
        if ins.opname in ("LOAD_CONST", "LOAD_SMALL_INT"):
            _check_value(ins.arg, bound)


@dataclass(slots=True)
class Trace:
    states: list       # states[i] is the state before step i; the last is at RETURN_VALUE
    outs: list         # outs[i] is the text printed by step i
    error: PyError | None = None

    @property
    def steps(self):
        return len(self.outs)

    @property
    def stdout(self):
        return "".join(self.outs)


def run(prog, max_steps=config.MAX_STEPS, bound=config.INT_BOUND):
    """Run to completion. Raises LimitExceeded or Unsupported; a Python-level
    exception in the script is returned as trace.error (with the states so far)."""
    st = State(0, (), {})
    states, outs = [st], []
    instrs = prog.instrs
    while instrs[st.ip].opname != "RETURN_VALUE":
        if len(outs) >= max_steps:
            raise LimitExceeded(f"more than {max_steps} steps")
        try:
            st, out = step(prog, st)
        except PyError as e:
            return Trace(states, outs, e)
        check_limits(st, bound)
        states.append(st)
        outs.append(out)
    return Trace(states, outs)
