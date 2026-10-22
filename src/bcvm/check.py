"""Differential check of a reference-interpreter trace against real CPython.

CPython is run with opcode-level tracing (`f_trace_opcodes`), which reports
every instruction executed. We require, for every script:

- the same sequence of executed instructions (byte offsets), step for step;
- the same user names and values before every instruction (stronger than the
  line-event check in the design doc);
- identical stdout, and the same exception type if the script raises.

The value stack is not visible from Python, but it determines every one of
those observations, so a stack bug shows up as a mismatch within a few steps.
A mismatch means the reference interpreter is wrong; callers must fail loudly.
"""
import builtins
import contextlib
import io
import sys
from dataclasses import dataclass

from .state import same_value
from .values import RangeObj


class Mismatch(Exception):
    pass


class _Budget(BaseException):
    pass


@dataclass(slots=True)
class CPyRun:
    stdout: str
    offsets: list
    names: list
    exc_type: str | None


def run_cpython(prog, max_events):
    code = prog.code
    user = frozenset(prog.names)
    g = {"__builtins__": builtins}
    offsets, snaps = [], []

    def tracer(frame, event, arg):
        if frame.f_code is not code:
            return None
        frame.f_trace_opcodes = True
        if event == "opcode":
            if len(offsets) > max_events:
                raise _Budget
            offsets.append(frame.f_lasti)
            snaps.append({k: v for k, v in g.items() if k in user})
        return tracer

    buf = io.StringIO()
    exc_type = None
    old = sys.gettrace()
    with contextlib.redirect_stdout(buf):
        sys.settrace(tracer)
        try:
            exec(code, g)
        except _Budget:
            raise Mismatch(f"CPython ran past {max_events} instructions") from None
        except Exception as e:  # noqa: BLE001 - the script's own exception
            exc_type = type(e).__name__
        finally:
            sys.settrace(old)
    # The RESUME at offset 0 runs before tracing switches to opcode events.
    if not offsets or offsets[0] != 0:
        offsets.insert(0, 0)
        snaps.insert(0, {})
    # EXTENDED_ARG prefixes are folded into the instruction they extend.
    keep = [i for i, off in enumerate(offsets) if off not in prog.prefix_offsets]
    return CPyRun(buf.getvalue(), [offsets[i] for i in keep], [snaps[i] for i in keep], exc_type)


def _matches(ref, py):
    if type(ref) is RangeObj:
        return type(py) is range and (py.start, py.stop, py.step) == (ref.start, ref.stop, ref.step)
    return same_value(ref, py)


def compare(prog, trace, cpy):
    """Raise Mismatch describing the first divergence, if any."""
    ref_offsets = [prog.instrs[s.ip].offset for s in trace.states]
    ref_exc = trace.error.exc_type if trace.error else None
    if ref_exc != cpy.exc_type:
        raise Mismatch(f"exception: ref {ref_exc}, CPython {cpy.exc_type}")
    if trace.stdout != cpy.stdout:
        raise Mismatch(f"stdout differs:\nref:  {trace.stdout!r}\ncpy:  {cpy.stdout!r}")
    n = min(len(ref_offsets), len(cpy.offsets))
    for i in range(n):
        if ref_offsets[i] != cpy.offsets[i]:
            raise Mismatch(f"step {i}: ref at offset {ref_offsets[i]} "
                           f"({prog.instrs[trace.states[i].ip].opname}), CPython at {cpy.offsets[i]}")
        ref_names = {prog.names[k]: v for k, v in trace.states[i].names.items()}
        py_names = cpy.names[i]
        if ref_names.keys() != py_names.keys() or not all(
                _matches(v, py_names[k]) for k, v in ref_names.items()):
            raise Mismatch(f"step {i} (offset {ref_offsets[i]}): names differ\n"
                           f"ref: {ref_names}\ncpy: {py_names}")
    if len(ref_offsets) != len(cpy.offsets):
        raise Mismatch(f"ref executed {len(ref_offsets)} instructions, CPython {len(cpy.offsets)}")


def differential_check(prog, trace):
    # runaway guard only; CPython also reports EXTENDED_ARG prefixes, up to 3 per instruction
    compare(prog, trace, run_cpython(prog, max_events=4 * len(trace.states) + 10))
