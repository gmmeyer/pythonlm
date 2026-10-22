"""Quick self-check for LLM-written natural scripts (run with python3.14).

Usage: python3.14 natural/check_natural.py natural/phaseB/b1_*.py

Checks each file runs without error, prints something, executes fewer than
1,500 instructions, and keeps every int bound to a name within -999..999.
The full support check and reference interpreter filter again later.
"""
import contextlib
import io
import sys


def check(path):
    src = open(path).read()
    code = compile(src, path, "exec")
    count = 0
    worst = 0

    def tracer(frame, event, arg):
        nonlocal count, worst
        if frame.f_code is not code:
            return None
        frame.f_trace_opcodes = True
        if event == "opcode":
            count += 1
            if count > 1500:
                raise RuntimeError("over 1500 instructions")
            for v in frame.f_locals.values():
                if type(v) is int:
                    worst = max(worst, abs(v))
        return tracer

    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        sys.settrace(tracer)
        try:
            exec(code, {"__builtins__": __builtins__})
        finally:
            sys.settrace(None)
    problems = []
    if not out.getvalue():
        problems.append("prints nothing")
    if worst > 999:
        problems.append(f"int {worst} out of bound")
    return count, problems


def main():
    bad = 0
    for path in sys.argv[1:]:
        try:
            count, problems = check(path)
        except Exception as e:  # noqa: BLE001
            count, problems = -1, [f"{type(e).__name__}: {e}"]
        if problems:
            bad += 1
            print(f"FAIL {path}: {'; '.join(problems)}")
    print(f"{len(sys.argv) - 1 - bad}/{len(sys.argv) - 1} ok")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
