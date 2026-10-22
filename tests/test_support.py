import pytest

from bcvm import support

ACCEPT = {
    "A": ["x = 1\nprint(x + 2)\n", "print('hi')\n", "a = b = 0\na, b = b, a\nprint()\n"],
    "B": ["for i in range(1, 9, 2):\n    print(i < 4)\n", "x = 3\nwhile x:\n    x -= 1\n"],
    "C": ["s = 'a' + 'b'\nprint(s, len(s), sep='-')\n", "n = 2\nprint(f'{n}x', str(n)[0])\n"],
}

REFUSE = {
    "A": [
        "x = 1.5\n", "print(1, 2)\n", "y = 2\nx = y ** 3\nprint(x)\n", "y = 1\nprint(y / 2)\n", "x = 1\nif x:\n    pass\n",
        "s = 'hi'\nprint(s)\n", "x = 1\nprint(x + 'a')\n", "import os\n", "def f():\n    pass\n",
        "print(abs(-1))\n", "x = True\n", "p = print\n", "x = 1\nx <<= 2\n", "print(len('ab'))\n",
        "print('caf\\u00e9')\n", "print(input())\n", "print(undefined_name)\n",
    ],
    "B": [
        "for c in 'abc':\n    print(c)\n", "x = [1, 2]\n", "print(1, 2)\n", "for i in range(3):\n    print(str(i))\n",
        "s = 'a'\nif s == 'a':\n    print(1)\n", "print(range(1, 2, 3, 4))\n", "x = 1\nx = x if x else 'no'\n",
        "try:\n    pass\nexcept:\n    pass\n", "while True:\n    break\nelse:\n    pass\nx = {}\n", "print(1, end='')\n",
    ],
    "C": [
        "s = 'abc'\nprint(s[1:])\n", "s = 'ab'\nprint(s.upper())\n", "print(f'{3:>4}')\n", "print(f'{3!r}')\n",
        "for ch in 'ab':\n    print(ch)\n", "print('a' in 'abc')\n", "print('x', file=None)\n", "print(int('3'))\n",
        "x = [1]\n", "s = 'ab'\nfor c in s:\n    print(c)\n", "def f():\n    return 1\n", "print(str(1, 2))\n",
        "print('a' * 49)\n",
    ],
}


@pytest.mark.parametrize("phase,src", [(p, s) for p, ss in ACCEPT.items() for s in ss])
def test_accepts(phase, src):
    support.check_source(src, phase)


@pytest.mark.parametrize("phase,src", [(p, s) for p, ss in REFUSE.items() for s in ss])
def test_refuses(phase, src):
    with pytest.raises((support.Refusal, support.CompileError)):
        support.check_source(src, phase)


def test_phases_are_cumulative():
    for p, srcs in ACCEPT.items():
        for later in "ABC"[ "ABC".index(p):]:
            for s in srcs:
                support.check_source(s, later)


def test_refusal_reason_is_readable():
    with pytest.raises(support.Refusal, match="name 'abs'"):
        support.check_source("print(abs(-1))\n", "C")
