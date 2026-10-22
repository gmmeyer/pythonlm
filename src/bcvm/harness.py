"""The runner: compile, support check, then a validated step loop.

A *stepper* proposes candidate next steps as token sequences (the model on the
5090; `OracleStepper` here, which wraps the reference interpreter behind the
same token interface). Every candidate is parsed and validated before it may
change the state or reach stdout; if every candidate fails, the run stops with
an error instead of printing anything wrong.

The validator only checks structure that follows from the listing, never
values: the successor ip, the stack depth (our own effect table, because
`dis.stack_effect` doesn't model FOR_ITER skipping END_FOR), that the stack
below the instruction's operands and every name it doesn't store are copied
unchanged, and that only print() produces output.
"""
import sys
from dataclasses import dataclass, field

from . import config, refvm, support, tokens
from .program import Program
from .state import _same_seq, same_value
from .values import Builtin

_NO_EFFECT = {"RESUME", "NOP", "NOT_TAKEN", "EXTENDED_ARG", "JUMP_FORWARD", "JUMP_BACKWARD"}
_PUSH1 = {"LOAD_SMALL_INT", "LOAD_CONST", "LOAD_NAME", "PUSH_NULL", "COPY"}
_POP1 = {"STORE_NAME", "POP_TOP", "POP_JUMP_IF_FALSE", "POP_JUMP_IF_TRUE", "END_FOR", "POP_ITER"}
_UNARY = {"UNARY_NEGATIVE", "UNARY_NOT", "TO_BOOL", "FORMAT_SIMPLE", "GET_ITER"}
_BINARY = {"BINARY_OP", "COMPARE_OP"}


def operand_effect(ins, jumped):
    """(values consumed, values produced) at the top of the stack."""
    op = ins.opname
    if op in _NO_EFFECT:
        return 0, 0
    if op in _PUSH1:
        return 0, 1
    if op in _POP1:
        return 1, 0
    if op in _UNARY:
        return 1, 1
    if op in _BINARY:
        return 2, 1
    if op == "SWAP":
        return ins.arg, ins.arg
    if op == "FOR_ITER":
        return (0, 0) if jumped else (1, 2)
    if op == "CALL":
        return ins.arg + 2, 1
    if op == "CALL_KW":
        return ins.arg + 3, 1
    if op == "BUILD_STRING":
        return ins.arg, 1
    raise ValueError(f"no effect for {op}")


def successors(ins):
    op, i = ins.opname, ins.index
    if op in ("JUMP_FORWARD", "JUMP_BACKWARD"):
        return (ins.arg,)
    if op in ("POP_JUMP_IF_FALSE", "POP_JUMP_IF_TRUE", "FOR_ITER"):
        return (i + 1, ins.arg)
    return (i + 1,)


def validate(prog, st, nxt, out):
    """Return None if (nxt, out) is a structurally possible successor of st, else a reason."""
    ins = prog.instrs[st.ip]
    succ = successors(ins)
    if nxt.ip not in succ:
        return f"ip {nxt.ip} not a successor of {ins.opname} at {st.ip} {succ}"
    if not 0 <= nxt.ip < len(prog.instrs):
        return "ip out of range"
    pops, pushes = operand_effect(ins, jumped=nxt.ip != st.ip + 1)
    depth = len(st.stack)
    if pops > depth:
        return f"{ins.opname} needs {pops} operands, stack has {depth}"
    if len(nxt.stack) != depth - pops + pushes:
        return f"stack depth {len(nxt.stack)}, expected {depth - pops + pushes}"
    keep = depth - pops
    if not _same_seq(st.stack[:keep], nxt.stack[:keep]):
        return "stack below the operands changed"
    if ins.opname == "COPY" and not same_value(nxt.stack[-1], st.stack[-ins.arg]):
        return "COPY pushed a different value"
    if ins.opname == "SWAP" and ins.arg >= 2:
        n = ins.arg
        want = st.stack[:depth - n] + (st.stack[-1],) + st.stack[depth - n + 1:-1] + (st.stack[-n],)
        if not _same_seq(nxt.stack, want):
            return "SWAP is not a swap"
    stored = ins.arg[1] if ins.opname == "STORE_NAME" else None
    if ins.opname == "STORE_NAME":
        if not same_value(nxt.names.get(stored, _MISSING), st.stack[-1]):
            return "STORE_NAME stored a different value"
    for k in set(st.names) | set(nxt.names):
        if k == stored:
            continue
        if k not in st.names or k not in nxt.names or not same_value(st.names[k], nxt.names[k]):
            return f"name N{k} changed"
    if any(k >= len(prog.names) for k in nxt.names):
        return "unknown name index"
    if out:
        if ins.opname not in ("CALL", "CALL_KW"):
            return f"output from {ins.opname}"
        n = ins.arg + (1 if ins.opname == "CALL_KW" else 0)
        if st.stack[-n - 2] != Builtin("print"):
            return "output from a call that isn't print"
    if len(nxt.stack) > config.MAX_STACK:
        return "stack too deep"
    return None


_MISSING = object()


# ---------------------------------------------------------------- steppers

class OracleStepper:
    """The reference interpreter behind the model's token interface.

    Used to test the harness end to end (token round trips, validator,
    grammar) before a model exists; also a correctness ceiling for the runner."""

    def __init__(self, corrupt=None):
        self.corrupt = corrupt  # optional fn(tokens) -> tokens, to test the safeguards

    def propose(self, prog, listing_tokens, state_tokens, n):
        st, _ = tokens.parse_state(state_tokens)
        nxt, out = refvm.step(prog, st)
        toks = tokens.enc_state(nxt) + tokens.enc_out(out) + ["<eos>"]
        cands = [toks] * n
        if self.corrupt:
            cands = [self.corrupt(toks)] + cands[1:]
        return cands


@dataclass
class RunResult:
    stdout: str = ""
    steps: int = 0
    refused: str | None = None
    error: str | None = None
    rejected: int = 0           # candidates the validator rejected
    rescued: int = 0            # steps where a later candidate passed after a rejection
    rejections: list = field(default_factory=list)


def run(src, phase, stepper, max_steps=10_000, candidates=3, stream=None):
    res = RunResult()
    try:
        prog = Program(src)
        support.check(prog, phase)
    except (support.Refusal, support.CompileError) as e:
        res.refused = str(e)
        return res
    listing = ["<bos>"] + tokens.enc_listing(prog)
    st = refvm.State(0, (), {})
    while prog.instrs[st.ip].opname != "RETURN_VALUE":
        if res.steps >= max_steps:
            res.error = f"stopped after {max_steps} steps"
            return res
        state_toks = tokens.enc_state(st) + ["=>"]
        accepted = None
        for k, cand in enumerate(stepper.propose(prog, listing, state_toks, candidates)):
            try:
                nxt, out, end = tokens.parse_step_output(cand)
                if end != len(cand):
                    raise tokens.ParseError("tokens after <eos>")
                reason = validate(prog, st, nxt, out)
            except tokens.ParseError as e:
                reason = f"malformed: {e}"
            if reason is None:
                accepted = (nxt, out)
                if k:
                    res.rescued += 1
                break
            res.rejected += 1
            if len(res.rejections) < 20:
                res.rejections.append((res.steps, reason))
        if accepted is None:
            res.error = f"step {res.steps}: every candidate failed validation ({res.rejections[-1][1]})"
            return res
        st, out = accepted
        if out:
            res.stdout += out
            if stream is not None:
                stream.write(out)
                stream.flush()
        res.steps += 1
    return res


def main_run(path, phase, oracle=True):
    with open(path) as f:
        src = f.read()
    if not oracle:
        raise SystemExit("model stepper lives on the training machine (bcvm.model); use --oracle here")
    res = run(src, phase, OracleStepper(), stream=sys.stdout)
    if res.refused:
        print(f"refused: {res.refused}", file=sys.stderr)
        return 2
    if res.error:
        print(f"error: {res.error}", file=sys.stderr)
        return 1
    return 0
