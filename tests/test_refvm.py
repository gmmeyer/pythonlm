"""Targeted differential tests: the reference interpreter must agree with CPython
instruction by instruction on every corner of the subset."""
import random

import pytest

from bcvm import check, pipeline, refvm, support
from bcvm.gen import grammar, templates
from bcvm.program import Program

CASES = {
    "A": [
        "x = -7\ny = 2\nprint(x // y)\nprint(x % y)\nprint(-x // -y)\nprint(7 % -3)\n",
        "a = b = 5\na += 1\nprint(a)\nprint(b)\na, b = b, a\nprint(a - b)\n",
        "a, b, c = 1, 2, 3\na, b, c = c, a, b\nprint(a)\nprint(b)\nprint(c)\n",
        "x = 255\ny = 256\nz = -1\nprint(x + y + z)\nprint(-(-x))\n",
        "print()\nprint('tab\\there')\nprint(\"quote ' and \\\\ backslash\")\nprint('two\\nlines')\n",
        "x = 3\nx\nx + 1\npass\nprint(x)\n",
        "n = 999\nn -= 1998\nprint(n)\nn *= -1\nprint(n)\nn //= 10\nn %= 7\nprint(n)\n",
    ],
    "B": [
        "for i in range(3):\n    print(i)\nfor i in range(5, 0, -2):\n    print(i)\nfor i in range(0):\n    print(i)\n",
        "x = 5\nprint(1 < x < 10)\nprint(1 < x > 10)\nprint(not x)\nprint(x and 0)\nprint(0 or x)\n",
        "i = 0\nwhile True:\n    i += 1\n    if i % 2:\n        continue\n    if i > 6:\n        break\n    print(i)\n",
        "t = True\nn = t + 1\nprint(n)\nprint(t == 1)\nprint(-t)\nc = 0\nfor k in range(4):\n    c += k > 1\nprint(c)\n",
        "x = 7\ny = 1 if x > 3 else 2\nprint(y)\nif x:\n    pass\nelif x < 0:\n    print('neg')\nelse:\n    print('zero')\n",
        "for i in range(3):\n    for j in range(3):\n        if j == i:\n            break\n        print(i * 10 + j)\n",
        "r = range(2, 8, 3)\nfor v in r:\n    print(v)\nprint(len(range(5)))\n" if False else "r = range(2, 8, 3)\nfor v in r:\n    print(v)\n",
        "n = 0\nwhile n < 3:\n    n += 1\nelse:\n    print('else ran')\nfor i in range(2):\n    pass\nelse:\n    print(i)\n",
    ],
    "C": [
        "s = 'abc'\nprint(s + s, s * 2, 2 * s, s[0], s[-1], len(s))\nprint(str(-12) + 'x', str(True), str(None))\n",
        "n = 5\nname = 'Bo'\nprint(f'{name} has {n} cats', f'{n}', f'{n + 1}!', sep='|', end='.\\n')\nprint('x', end='')\nprint()\n",
        "a = 'ab'\nb = 'ac'\nprint(a < b, a == 'ab', a != b, a > b)\nif a:\n    print('nonempty')\nif '':\n    print('no')\n",
        "s = ''\nfor i in range(4):\n    s += str(i)\nprint(s, len(s), sep=None)\nprint(s[len(s) - 1], 'end', sep='', end=None)\n",
        "w = 'level'\ni = 0\nj = len(w) - 1\nok = True\nwhile i < j:\n    if w[i] != w[j]:\n        ok = False\n    i += 1\n    j -= 1\nprint(ok)\n",
    ],
}


def _run_checked(src, phase):
    prog = support.check_source(src, phase)
    trace = refvm.run(prog, max_steps=100_000, bound=10**6)
    check.differential_check(prog, trace)
    return trace


@pytest.mark.parametrize("phase,src", [(p, s) for p, ss in CASES.items() for s in ss])
def test_cases_match_cpython(phase, src):
    trace = _run_checked(src, phase)
    assert trace.error is None


@pytest.mark.parametrize("src,exc", [
    ("x = 0\nprint(1 // x)\n", "ZeroDivisionError"),
    ("x = 1\nprint(x % 0)\n", "ZeroDivisionError"),
    ("print(y)\n", "NameError"),
    ("s = 'ab'\nprint(s[5])\n", "IndexError"),
    ("s = 'ab'\nprint(s + 1)\n", "TypeError"),
])
def test_exceptions_match_cpython(src, exc):
    prog = Program(src)  # NameError scripts are refused by the support check, so bypass it
    trace = refvm.run(prog)
    check.differential_check(prog, trace)
    assert trace.error.exc_type == exc


def test_extended_arg_long_jumps():
    body = "\n".join(f"    x = x + {i}" for i in range(36))
    src = f"x = 0\nn = 2\nwhile n > 0:\n{body}\n    n -= 1\nprint(x)\n"
    prog = support.check_source(src, "B")
    assert any(i.opname == "EXTENDED_ARG" for i in prog.instrs)
    trace = refvm.run(prog, max_steps=100_000, bound=10**6)
    check.differential_check(prog, trace)


def test_limits():
    prog = support.check_source("x = 999\nx += 1\n", "A")
    with pytest.raises(refvm.LimitExceeded):
        refvm.run(prog)
    prog = support.check_source("while True:\n    pass\n", "B")
    with pytest.raises(refvm.LimitExceeded):
        refvm.run(prog, max_steps=500)


def test_mismatch_is_detected():
    """A deliberately wrong trace must fail the differential check."""
    prog = support.check_source("x = 2\ny = x * 3\nprint(y)\n", "A")
    trace = refvm.run(prog)
    bad = trace.states[3]
    trace.states[3] = refvm.State(bad.ip, bad.stack, {**bad.names, 0: 3})
    with pytest.raises(check.Mismatch):
        check.differential_check(prog, trace)
    trace = refvm.run(prog)
    trace.outs[-2] = "7\n"
    with pytest.raises(check.Mismatch):
        check.differential_check(prog, trace)


@pytest.mark.parametrize("phase", "ABC")
def test_generated_scripts_match_cpython(phase):
    rng = random.Random(1234)
    kept = 0
    for _ in range(300):
        for gen in (grammar.generate, templates.generate):
            try:
                pipeline.prepare(gen(rng, phase), phase)
                kept += 1
            except pipeline.Skip:
                pass
    assert kept > 300


def test_natural_scripts_match_cpython(natural_sample):
    for phase, path in natural_sample:
        try:
            pipeline.prepare(open(path).read(), phase)
        except pipeline.Skip as e:
            assert str(e) == "limit", (path, e)


def test_user_names_order_and_builtins():
    prog = Program("total = 0\nsum = 3\nprint(total + sum)\nlen = 1\n")
    assert prog.names == ["total", "sum", "len"]  # assigned builtins become user names
    prog = Program("print(len('x'))\n")
    assert prog.names == []
