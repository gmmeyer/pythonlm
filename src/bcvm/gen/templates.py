"""Templated classics with randomized parameters, names and minor style choices.

Each template is `f(rng, nm) -> source`, where nm(role) returns a variable name
for a role ("n", "total", ...) drawn per script so names vary.
"""
from .common import VAR_NAMES


class _Names:
    def __init__(self, rng):
        self.rng = rng
        self.used = {}
        self.pool = list(VAR_NAMES)
        rng.shuffle(self.pool)

    def __call__(self, role):
        if role not in self.used:
            if self.rng.random() < 0.5 and role not in self.used.values() and role.isidentifier():
                self.used[role] = role
            else:
                self.used[role] = next(v for v in self.pool if v not in self.used.values())
        return self.used[role]


def _lines(*ls):
    return "\n".join(line for line in ls if line is not None) + "\n"


# ------------------------------------------------------------------ phase A

def a_change(r, nm):
    c, q, d, n, p = nm("cents"), nm("quarters"), nm("dimes"), nm("nickels"), nm("pennies")
    amt = r.randint(1, 999)
    return _lines(f"{c} = {amt}", f"{q} = {c} // 25", f"{c} = {c} % 25", f"{d} = {c} // 10",
                  f"{c} %= 10", f"{n} = {c} // 5", f"{p} = {c} % 5",
                  'print("quarters:")' if r.random() < 0.5 else None, f"print({q})",
                  f"print({d})", f"print({n})", f"print({p})")


def a_time(r, nm):
    t, h, m, s = nm("total"), nm("hours"), nm("mins"), nm("secs")
    v = r.randint(0, 999)
    return _lines(f"{t} = {v}", f"{h} = {t} // 60" if r.random() < 0.5 else f"{h} = {t} // 3600",
                  f"{m} = {t} % 60 // 1" if r.random() < 0.3 else f"{m} = ({t} // 60) % 60",
                  f"{s} = {t} % 60", f"print({h})", f"print({m})", f"print({s})")


def a_digits(r, nm):
    n, a, b, c = nm("n"), nm("hundreds"), nm("tens"), nm("ones")
    v = r.randint(100, 999) * r.choice([1, 1, 1, -1])
    out = [f"{n} = {v}", f"{a} = {n} // 100", f"{b} = {n} // 10 % 10", f"{c} = {n} % 10"]
    if r.random() < 0.5:
        out += [f"print({a} + {b} + {c})"]
    else:
        out += [f"print({a})", f"print({b})", f"print({c})", f"print({c} * 100 + {b} * 10 + {a})"]
    return _lines(*out)


def a_rect(r, nm):
    w, h, area, per = nm("width"), nm("height"), nm("area"), nm("perimeter")
    a, b = r.randint(1, 31), r.randint(1, 31)
    return _lines(f"{w} = {a}", f"{h} = {b}", f"{area} = {w} * {h}", f"{per} = 2 * ({w} + {h})",
                  'print("Area:")' if r.random() < 0.5 else None, f"print({area})",
                  'print("Perimeter:")' if r.random() < 0.5 else None, f"print({per})")


def a_fib_unrolled(r, nm):
    a, b = nm("a"), nm("b")
    x, y = r.randint(0, 5), r.randint(1, 5)
    k = r.randint(3, 9)
    body = [f"{a}, {b} = {x}, {y}"]
    for _ in range(k):
        body += [f"print({a})", f"{a}, {b} = {b}, {a} + {b}"]
    return _lines(*body)


def a_average(r, nm):
    xs = [nm(f"x{i}") for i in range(r.randint(2, 5))]
    s, avg = nm("total"), nm("avg")
    out = [f"{x} = {r.randint(-99, 199)}" for x in xs]
    out += [f"{s} = {' + '.join(xs)}", f"{avg} = {s} // {len(xs)}", f"print({s})", f"print({avg})",
            f"print({s} % {len(xs)})"]
    return _lines(*out)


def a_clock(r, nm):
    h, d = nm("hour"), nm("delta")
    return _lines(f"{h} = {r.randint(0, 23)}", f"{d} = {r.randint(-99, 200)}",
                  f"print(({h} + {d}) % 24)", f"print(({h} + {d}) % 12)", f"print(({h} - {d}) % 24)")


def a_swap_ops(r, nm):
    x, y = nm("x"), nm("y")
    a, b = r.randint(-50, 99), r.randint(-50, 99)
    return _lines(f"{x} = {a}", f"{y} = {b}", f"{x}, {y} = {y}, {x}", f"print({x})", f"print({y})",
                  f"{x} = {x} - {y}", f"print(-{x})", f"print({x} * 2 - {y})")


A = [a_change, a_time, a_digits, a_rect, a_fib_unrolled, a_average, a_clock, a_swap_ops]


# ------------------------------------------------------------------ phase B

def b_gcd(r, nm):
    a, b, t = nm("a"), nm("b"), nm("t")
    x, y = r.randint(1, 999), r.randint(1, 999)
    if r.random() < 0.5:
        return _lines(f"{a} = {x}", f"{b} = {y}", f"while {b} != 0:", f"    {a}, {b} = {b}, {a} % {b}", f"print({a})")
    return _lines(f"{a} = {x}", f"{b} = {y}", f"while {b}:", f"    {t} = {b}", f"    {b} = {a} % {b}",
                  f"    {a} = {t}", f"print({a})")


def b_fib(r, nm):
    a, b, i, n = nm("a"), nm("b"), nm("i"), nm("n")
    k = r.randint(1, 15)
    if r.random() < 0.5:
        return _lines(f"{a}, {b} = 0, 1", f"for {i} in range({k}):", f"    print({a})", f"    {a}, {b} = {b}, {a} + {b}")
    lim = r.randint(10, 999)
    return _lines(f"{a} = 0", f"{b} = 1", f"while {a} < {lim}:", f"    print({a})", f"    {n} = {a} + {b}",
                  f"    {a} = {b}", f"    {b} = {n}")


def b_fizzbuzz(r, nm):
    i = nm("i")
    lo, hi = r.randint(1, 10), r.randint(10, 30)
    a, b = r.choice([(3, 5), (3, 5), (2, 7), (4, 6)])
    if r.random() < 0.5:
        return _lines(f"for {i} in range({lo}, {hi}):", f"    if {i} % {a * b} == 0:", '        print("FizzBuzz")',
                      f"    elif {i} % {a} == 0:", '        print("Fizz")', f"    elif {i} % {b} == 0:",
                      '        print("Buzz")', "    else:", f"        print({i})")
    return _lines(f"{i} = {lo}", f"while {i} < {hi}:", f"    if {i} % {a} == 0 and {i} % {b} == 0:",
                  '        print("FizzBuzz")', f"    elif {i} % {a} == 0:", '        print("Fizz")',
                  f"    elif {i} % {b} == 0:", '        print("Buzz")', "    else:", f"        print({i})",
                  f"    {i} += 1")


def b_collatz(r, nm):
    n, s = nm("n"), nm("steps")
    v = r.choice([r.randint(1, 30), r.randint(1, 60)])
    pr = r.random() < 0.5
    return _lines(f"{n} = {v}", f"{s} = 0", f"while {n} != 1:", f"    print({n})" if pr else None,
                  f"    if {n} % 2 == 0:", f"        {n} = {n} // 2", "    else:", f"        {n} = 3 * {n} + 1",
                  f"    {s} += 1", f"print({s})")


def b_digit_sum(r, nm):
    n, s = nm("n"), nm("total")
    v = r.randint(0, 999)
    return _lines(f"{n} = {v}", f"{s} = 0", f"while {n} > 0:", f"    {s} += {n} % 10", f"    {n} //= 10", f"print({s})")


def b_primes(r, nm):
    n, d, ok = nm("n"), nm("d"), nm("is_prime")
    lo = r.randint(2, 60)
    hi = lo + r.randint(1, 25)
    if r.random() < 0.5:
        return _lines(f"for {n} in range({lo}, {hi}):", f"    {ok} = True", f"    {d} = 2",
                      f"    while {d} * {d} <= {n}:", f"        if {n} % {d} == 0:", f"            {ok} = False",
                      "            break", f"        {d} += 1", f"    if {ok}:", f"        print({n})")
    v = r.randint(2, 997)
    return _lines(f"{n} = {v}", f"{d} = 2", f"{ok} = {n} > 1", f"while {d} * {d} <= {n}:",
                  f"    if {n} % {d} == 0:", f"        {ok} = False", "        break", f"    {d} = {d} + 1",
                  f"print({ok})")


def b_divisors(r, nm):
    n, d, c = nm("n"), nm("d"), nm("count")
    v = r.randint(1, 120)
    return _lines(f"{n} = {v}", f"{c} = 0", f"for {d} in range(1, {n} + 1):", f"    if {n} % {d} == 0:",
                  f"        {c} += 1", f"        print({d})" if r.random() < 0.5 else None, f"print({c})")


def b_sum_range(r, nm):
    i, s = nm("i"), nm("total")
    a = r.randint(-20, 20)
    b = a + r.randint(0, 40)
    st = r.choice([1, 1, 2, 3])
    cond = r.choice([None, f"{i} % 2 == 0", f"{i} % 3 != 0", f"{i} > {a + 3}"])
    out = [f"{s} = 0", f"for {i} in range({a}, {b}{', ' + str(st) if st != 1 else ''}):"]
    if cond:
        out += [f"    if not ({cond}):" if r.random() < 0.3 else f"    if {cond}:", f"        {s} += {i}"]
    else:
        out += [f"    {s} += {i}"]
    out += [f"print({s})"]
    return _lines(*out)


def b_reverse_num(r, nm):
    n, rev = nm("n"), nm("rev")
    v = r.randint(1, 999)
    return _lines(f"{n} = {v}", f"{rev} = 0", f"while {n} > 0:", f"    {rev} = {rev} * 10 + {n} % 10",
                  f"    {n} = {n} // 10", f"print({rev})", f"print({rev} == {v})")


def b_factorial(r, nm):
    f, i = nm("fact"), nm("i")
    n = r.randint(0, 6)
    return _lines(f"{f} = 1", f"for {i} in range(2, {n + 1}):", f"    {f} *= {i}", f"print({f})")


def b_minmax(r, nm):
    x, lo, hi, i = nm("x"), nm("lo"), nm("hi"), nm("i")
    seed, m, a = r.randint(0, 100), r.choice([97, 101, 89, 53]), r.randint(2, 9)
    k = r.randint(2, 12)
    return _lines(f"{x} = {seed}", f"{lo} = {x}", f"{hi} = {x}", f"for {i} in range({k}):",
                  f"    {x} = ({x} * {a} + {r.randint(1, 30)}) % {m}", f"    if {x} < {lo}:", f"        {lo} = {x}",
                  f"    if {x} > {hi}:", f"        {hi} = {x}", f"print({lo})", f"print({hi})")


def b_countdown(r, nm):
    n = nm("n")
    v = r.randint(0, 15)
    st = r.choice([1, 1, 2, 3])
    if r.random() < 0.5:
        return _lines(f"for {n} in range({v}, -1, -{st}):", f"    print({n})", f'print({"Liftoff!"!r})')
    return _lines(f"{n} = {v}", f"while {n} > 0:", f"    print({n})", f"    {n} -= {st}", 'print("Go")')


def b_nested_table(r, nm):
    i, j = nm("i"), nm("j")
    a, b = r.randint(1, 6), r.randint(1, 6)
    return _lines(f"for {i} in range(1, {a + 1}):", f"    for {j} in range(1, {b + 1}):",
                  f"        print({i} * {j})", '    print("--")' if r.random() < 0.5 else None)


def b_search(r, nm):
    n = nm("n")
    k, m = r.randint(2, 13), r.randint(0, 12)
    start = r.randint(1, 200)
    return _lines(f"{n} = {start}", "while True:", f"    if {n} % {k} == {m % k}:", "        break",
                  f"    {n} += 1", f"print({n})")


def b_leap(r, nm):
    y = nm("year")
    v = r.choice([r.randint(100, 999), r.choice([100, 200, 400, 800, 900, 104, 996])])
    return _lines(f"{y} = {v}", f"if {y} % 400 == 0:", '    print("leap")', f"elif {y} % 100 == 0:",
                  '    print("common")', f"elif {y} % 4 == 0:", '    print("leap")', "else:", '    print("common")')


def b_grade(r, nm):
    s = nm("score")
    v = r.randint(0, 100)
    cuts = sorted(r.sample(range(40, 100), 3), reverse=True)
    return _lines(f"{s} = {v}", f"if {s} >= {cuts[0]}:", '    print("A")', f"elif {s} >= {cuts[1]}:",
                  '    print("B")', f"elif {s} >= {cuts[2]}:", '    print("C")', "else:", '    print("F")')


def b_power(r, nm):
    b, e, res = nm("base"), nm("exp"), nm("result")
    x, n = r.randint(-4, 9), r.randint(0, 5)
    m = r.choice([None, 7, 13, 97])
    upd = f"    {res} = {res} * {b} % {m}" if m else f"    {res} *= {b}"
    return _lines(f"{b} = {x}", f"{e} = {n}", f"{res} = 1", f"while {e} > 0:", upd, f"    {e} -= 1", f"print({res})")


def b_isqrt(r, nm):
    n, k = nm("n"), nm("k")
    v = r.randint(0, 999)
    return _lines(f"{n} = {v}", f"{k} = 0", f"while ({k} + 1) * ({k} + 1) <= {n}:", f"    {k} += 1", f"print({k})")


B = [b_gcd, b_fib, b_fizzbuzz, b_collatz, b_digit_sum, b_primes, b_divisors, b_sum_range, b_reverse_num,
     b_factorial, b_minmax, b_countdown, b_nested_table, b_search, b_leap, b_grade, b_power, b_isqrt]


# ------------------------------------------------------------------ phase C

def c_banner(r, nm):
    t, w = nm("title"), nm("width")
    word = r.choice(["Report", "Menu", "Scores", "Hello", "Summary", "Totals", "Inventory"])
    ch = r.choice(["=", "-", "*", "#", "~"])
    return _lines(f"{t} = {word!r}", f"{w} = len({t}) + {r.randint(0, 8)}", f"print({ch!r} * {w})",
                  f"print({t})", f"print({ch!r} * {w})")


def c_reverse(r, nm):
    s, out, i = nm("s"), nm("out"), nm("i")
    word = r.choice(["hello", "python", "stack", "racecar", "level", "abc", "banana", "noon", "rotor", "step"])
    if r.random() < 0.5:
        return _lines(f"{s} = {word!r}", f"{out} = ''", f"for {i} in range(len({s}) - 1, -1, -1):",
                      f"    {out} += {s}[{i}]", f"print({out})", f"print({out} == {s})")
    return _lines(f"{s} = {word!r}", f'{out} = ""', f"{i} = len({s})", f"while {i} > 0:", f"    {i} -= 1",
                  f"    {out} = {out} + {s}[{i}]", f"print({out})")


def c_count_char(r, nm):
    s, c, n, i = nm("text"), nm("ch"), nm("count"), nm("i")
    text = r.choice(["banana", "mississippi", "hello world", "a b c a b", "aaabbbccc", "lollipop", "tattoo"])
    ch = r.choice(sorted(set(text)))
    return _lines(f"{s} = {text!r}", f"{c} = {ch!r}", f"{n} = 0", f"for {i} in range(len({s})):",
                  f"    if {s}[{i}] == {c}:", f"        {n} += 1", f'print(f"{{{c}}} appears {{{n}}} times")')


def c_bar(r, nm):
    i, bar = nm("i"), nm("bar")
    k = r.randint(1, 8)
    ch = r.choice(["#", "*", "=", "|"])
    if r.random() < 0.5:
        return _lines(f"for {i} in range(1, {k + 1}):", f"    print({ch!r} * {i})")
    return _lines(f"{bar} = ''", f"for {i} in range({k}):", f"    {bar} += {ch!r}", f'    print(f"{{{i}}}: {{{bar}}}")')


def c_table(r, nm):
    i, j = nm("i"), nm("j")
    n, m = r.randint(1, 5), r.randint(1, 6)
    sep = r.choice([" ", "\t", " | ", ","])
    return _lines(f"for {i} in range(1, {n + 1}):", f"    for {j} in range(1, {m + 1}):",
                  f"        print({i} * {j}, end={sep!r})", "    print()")


def c_receipt(r, nm):
    items = r.sample(["apple", "bread", "milk", "eggs", "tea", "jam", "rice", "soap"], r.randint(2, 4))
    t = nm("total")
    out = [f"{t} = 0"]
    for it in items:
        p = r.randint(1, 99)
        out += [f"print({it!r}, {p}, sep={r.choice([': ', ' - ', ' '])!r})", f"{t} += {p}"]
    out += [f'print("total:", {t})' if r.random() < 0.5 else f'print(f"Total: {{{t}}}")']
    return _lines(*out)


def c_fizz_f(r, nm):
    i, s = nm("i"), nm("s")
    hi = r.randint(5, 20)
    return _lines(f"for {i} in range(1, {hi}):", f"    {s} = ''", f"    if {i} % 3 == 0:", f"        {s} += 'Fizz'",
                  f"    if {i} % 5 == 0:", f"        {s} += 'Buzz'", f"    if {s} == '':", f"        {s} = str({i})",
                  f"    print({s})")


def c_palindrome(r, nm):
    s, i, j, ok = nm("word"), nm("i"), nm("j"), nm("ok")
    w = r.choice(["level", "radar", "hello", "abba", "abca", "noon", "python", "civic", "refer", "kayak", "xyzzy"])
    return _lines(f"{s} = {w!r}", f"{i} = 0", f"{j} = len({s}) - 1", f"{ok} = True", f"while {i} < {j}:",
                  f"    if {s}[{i}] != {s}[{j}]:", f"        {ok} = False", "        break", f"    {i} += 1",
                  f"    {j} -= 1", f"print({s}, {ok})")


def c_digits_str(r, nm):
    n, s = nm("n"), nm("s")
    v = r.randint(-999, 999)
    return _lines(f"{n} = {v}", f"{s} = str({n})", f"print(len({s}))", f"print({s}[0], {s}[-1])",
                  f'print("digits: " + {s})')


def c_report(r, nm):
    name, pts, lvl = nm("name"), nm("points"), nm("level")
    who = r.choice(["Ada", "Bob", "Cy", "Dee", "Eve", "Finn", "Gus"])
    p = r.randint(0, 999)
    return _lines(f"{name} = {who!r}", f"{pts} = {p}", f"{lvl} = {pts} // 100 + 1",
                  f'print(f"{{{name}}} has {{{pts}}} points")', f'print("Level", {lvl}, sep=": ")',
                  f'print({name} + " is level " + str({lvl}))')


def c_box(r, nm):
    w, h, i = nm("w"), nm("h"), nm("i")
    a, b = r.randint(2, 12), r.randint(2, 6)
    return _lines(f"{w} = {a}", f"{h} = {b}", "print('+' + '-' * (" + w + " - 2) + '+')",
                  f"for {i} in range({h} - 2):", "    print('|' + ' ' * (" + w + " - 2) + '|')",
                  "print('+' + '-' * (" + w + " - 2) + '+')")


C = [c_banner, c_reverse, c_count_char, c_bar, c_table, c_receipt, c_fizz_f, c_palindrome, c_digits_str,
     c_report, c_box]

BY_PHASE = {"A": A, "B": A + B, "C": B + C}
WEIGHTS = {"A": [1] * len(A), "B": [0.3] * len(A) + [1] * len(B), "C": [0.3] * len(B) + [1] * len(C)}


def generate(rng, phase):
    fn = rng.choices(BY_PHASE[phase], WEIGHTS[phase])[0]
    return fn(rng, _Names(rng))
