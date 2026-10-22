"""The support check: refuse any script that steps outside a phase, before it runs.

Shared by data generation and the runner. Besides scanning opcodes, names and
constants, it runs a small abstract interpretation over the stack so it can
see which builtin each CALL invokes (and with how many arguments), and, before
phase C, that string literals only ever flow straight into print().
"""
from . import config, tokens
from .phases import Phase
from .program import CompileError, Program

_JUMPS_COND = {"POP_JUMP_IF_FALSE", "POP_JUMP_IF_TRUE"}
_JUMPS_ABS = {"JUMP_FORWARD", "JUMP_BACKWARD"}
_RESULT_KIND = {"print": "none", "range": "range", "len": "int", "str": "str"}


class Refusal(Exception):
    pass


def _const_kind(v):
    t = type(v)
    if t is bool:
        return "bool"
    if t is int:
        return "int"
    if t is str:
        return "str"
    if v is None:
        return "none"
    if t is tuple and v and all(type(x) is str for x in v):
        return "kw:" + ",".join(v)
    return "other:" + t.__name__


def _const_type_ok(kind, phase):
    if kind.startswith("kw:"):
        return "tuple" in phase.const_types
    return kind in phase.const_types


def check(prog, phase):
    """Raise Refusal if `prog` (a Program) uses anything outside `phase`."""
    if isinstance(phase, str):
        phase = Phase(phase)
    for c in prog.code.co_consts:
        if hasattr(c, "co_code"):
            raise Refusal("functions, classes and comprehensions are not supported yet")
    if len(prog.instrs) > config.MAX_INSTRS:
        raise Refusal(f"more than {config.MAX_INSTRS} instructions")
    if len(prog.names) > config.MAX_GLOBALS:
        raise Refusal(f"more than {config.MAX_GLOBALS} variable names")
    for name in prog.names:
        if name not in prog.stored:
            raise Refusal(f"name {name!r} is not supported in phase {phase.name}")
    for i, ins in enumerate(prog.instrs):
        op = ins.opname
        if op not in phase.opcodes:
            raise Refusal(f"{op} (line {ins.line}) is not supported in phase {phase.name}")
        if op == "BINARY_OP" and ins.arg not in phase.binops:
            raise Refusal(f"operator {ins.arg} (line {ins.line}) is not supported in phase {phase.name}")
        if op in ("LOAD_NAME", "STORE_NAME") and ins.arg[0] == "B" and ins.arg[1] not in phase.builtins:
            raise Refusal(f"name {ins.arg[1]!r} (line {ins.line}) is not supported in phase {phase.name}")
        if op == "LOAD_CONST":
            kind = _const_kind(ins.arg)
            if not _const_type_ok(kind, phase):
                raise Refusal(f"constant {ins.arg!r} (line {ins.line}) is not supported in phase {phase.name}")
            if kind.startswith("kw:") and prog.instrs[i + 1].opname != "CALL_KW":
                raise Refusal(f"tuple constant (line {ins.line}) is not supported in phase {phase.name}")
            if kind == "str":
                bad = [ch for ch in ins.arg if ch not in tokens.CHARSET]
                if bad:
                    raise Refusal(f"character {bad[0]!r} (line {ins.line}) is not supported")
                if len(ins.arg) > config.MAX_STR_LEN:
                    raise Refusal(f"string literal longer than {config.MAX_STR_LEN} characters (line {ins.line})")
    _abstract_check(prog, phase)
    n = len(tokens.enc_listing(prog))
    if n > config.MAX_LISTING_TOKENS:
        raise Refusal(f"listing is {n} tokens; the limit is {config.MAX_LISTING_TOKENS}")


def check_source(src, phase):
    """Compile and check. Returns the Program; raises Refusal (or CompileError)."""
    prog = Program(src)
    check(prog, phase)
    return prog


def _abstract_check(prog, phase):
    """Abstract interpretation over the CFG. Stack slots and names hold sets of
    kind tags; names are flow-insensitive (the union of everything ever stored
    to them), iterated to a fixpoint."""
    instrs = prog.instrs
    name_tags = {}
    while True:
        before = dict(name_tags)
        entry = {0: ()}
        work = [0]
        while work:
            i = work.pop()
            stack = list(entry[i])
            for j, st in _transfer(instrs[i], stack, phase, name_tags):
                st = tuple(st)
                old = entry.get(j)
                if old is None:
                    entry[j] = st
                    work.append(j)
                    continue
                if len(old) != len(st):
                    raise Refusal(f"inconsistent stack depth at instruction {j}")
                merged = tuple(a | b for a, b in zip(old, st))
                if merged != old:
                    entry[j] = merged
                    work.append(j)
        if name_tags == before:
            return


def _no_str(tags, what, ins, phase):
    if not phase.str_values and any("str" in t for t in tags):
        raise Refusal(f"{what} with strings (line {ins.line}) needs phase C")


def _transfer(ins, s, phase, name_tags):
    """Yield (successor index, stack) pairs; s is a list of frozenset tags."""
    op, i = ins.opname, ins.index
    nxt = i + 1
    one = frozenset
    if op in ("RESUME", "NOP", "NOT_TAKEN"):
        pass
    elif op == "LOAD_SMALL_INT":
        s.append(one({"int"}))
    elif op == "LOAD_CONST":
        s.append(one({_const_kind(ins.arg)}))
    elif op == "LOAD_NAME":
        kind, key = ins.arg
        s.append(name_tags.get(key, one({"unbound"})) if kind == "N" else one({"B:" + key}))
    elif op == "STORE_NAME":
        v = s.pop()
        if any(t.startswith("B:") for t in v):
            raise Refusal(f"builtins used as values (line {ins.line}) are not supported")
        _no_str([v], "variables", ins, phase)
        key = ins.arg[1]
        name_tags[key] = name_tags.get(key, frozenset()) | v
    elif op == "POP_TOP":
        s.pop()
    elif op == "PUSH_NULL":
        s.append(one({"null"}))
    elif op == "COPY":
        s.append(s[-ins.arg])
    elif op == "SWAP":
        s[-1], s[-ins.arg] = s[-ins.arg], s[-1]
    elif op == "BINARY_OP":
        b, a = s.pop(), s.pop()
        _no_str([a, b], "arithmetic", ins, phase)
        _no_builtin([a, b], ins)
        s.append(one({"str"}) if ("str" in a or "str" in b) else one({"int"}))
    elif op == "UNARY_NEGATIVE":
        v = s.pop()
        _no_str([v], "arithmetic", ins, phase)
        _no_builtin([v], ins)
        s.append(one({"int"}))
    elif op in ("UNARY_NOT", "TO_BOOL"):
        v = s.pop()
        _no_str([v], "truth tests", ins, phase)
        _no_builtin([v], ins)
        s.append(one({"bool"}))
    elif op == "COMPARE_OP":
        b, a = s.pop(), s.pop()
        _no_str([a, b], "comparisons", ins, phase)
        _no_builtin([a, b], ins)
        s.append(one({"bool"}))
    elif op in _JUMPS_COND:
        s.pop()
        yield ins.arg, list(s)
    elif op in _JUMPS_ABS:
        yield ins.arg, s
        return
    elif op == "GET_ITER":
        v = s.pop()
        bad = v - {"range", "iter", "unbound"}
        if bad:
            raise Refusal(f"iteration over anything but range() (line {ins.line}) is not supported in phase {phase.name}")
        s.append(one({"iter"}))
    elif op == "FOR_ITER":
        yield ins.arg, list(s)
        s.append(one({"int"}))
    elif op in ("END_FOR", "POP_ITER"):
        s.pop()
    elif op in ("CALL", "CALL_KW"):
        kw = ()
        if op == "CALL_KW":
            kwtag = s.pop()
            kinds = [t for t in kwtag if t.startswith("kw:")]
            if len(kinds) != 1 or len(kwtag) != 1:
                raise Refusal(f"keyword arguments (line {ins.line}) are not supported")
            kw = tuple(kinds[0][3:].split(","))
        n = ins.arg
        args = s[len(s) - n:]
        self_or_null = s[-n - 1]
        callee = s[-n - 2]
        del s[len(s) - n - 2:]
        if self_or_null != {"null"}:
            raise Refusal(f"method calls (line {ins.line}) are not supported in phase {phase.name}")
        names = [t[2:] for t in callee if t.startswith("B:")]
        if len(names) != 1 or len(callee) != 1:
            raise Refusal(f"calling a non-builtin (line {ins.line}) is not supported in phase {phase.name}")
        name = names[0]
        lo, hi = phase.builtins[name]
        npos = n - len(kw)
        if npos < lo or (hi is not None and npos > hi):
            raise Refusal(f"{name}() with {npos} arguments (line {ins.line}) is not supported in phase {phase.name}")
        if kw:
            if name != "print" or not set(kw) <= phase.print_kwargs or len(set(kw)) != len(kw):
                raise Refusal(f"keyword arguments to {name}() (line {ins.line}) are not supported")
        if name != "print":
            _no_str(args, f"{name}()", ins, phase)
        _no_builtin(args, ins)
        s.append(one({_RESULT_KIND[name]}))
    elif op == "FORMAT_SIMPLE":
        v = s.pop()
        _no_builtin([v], ins)
        s.append(one({"str"}))
    elif op == "BUILD_STRING":
        del s[len(s) - ins.arg:]
        s.append(one({"str"}))
    elif op == "RETURN_VALUE":
        return
    else:
        raise Refusal(f"{op} is not supported")
    yield nxt, s


def _no_builtin(tags, ins):
    if any(t.startswith("B:") for v in tags for t in v):
        raise Refusal(f"builtins used as values (line {ins.line}) are not supported")


__all__ = ["Refusal", "check", "check_source", "CompileError"]
