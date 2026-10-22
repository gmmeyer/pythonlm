"""Shared vocabulary for generators: variable names, words, literals."""
import string

VAR_NAMES = (
    "a b c d e f g h k m n p q r s t u v w x y z i j "
    "total count result value num acc step left right low high base price qty cost "
    "rate score level temp diff prod rem carry limit size width height area delta "
    "offset idx pos speed dist hours mins secs days coins cents balance target guess "
    "best worst first second third old new prev cur nxt start stop end mid tmp "
    "num1 num2 x1 x2 y1 y2 a0 b0 n2 k2 big small lo hi sum_ cnt flag ok done found "
    "steps tries budget fee tax tip bonus points lives health damage gold age year month"
).split()

WORDS = (
    "total result done start end yes no ok error value sum count answer even odd "
    "big small hello world fizz buzz Fizz Buzz FizzBuzz prime composite found missing "
    "win lose draw hot cold warm high low left right up down stop go red green blue "
    "alpha beta gamma delta step loop item row col grid line box apple pear plum "
    "cat dog fox owl bee ant cow pig hen elk"
).split()

LABELS = [
    "Total:", "Result:", "Answer:", "x =", "y =", "count =", "sum:", "---", "===", "***",
    "Done", "done.", "Start", "End", "Hello, world!", "ok", "Average:", "Remainder:",
    "Change:", "Hours:", "Minutes:", "Seconds:", "Area:", "Perimeter:", "Score:", "Level up!",
    "Game over", "Balance:", "Warning: low", "Step", "Final:", "->", "#", "", " ",
    "Values:", "max:", "min:", "Even", "Odd", "Positive", "Negative", "Zero", "Prime",
    "Not prime", "Too big", "Too small", "Correct!", "Fizz", "Buzz", "FizzBuzz",
]

PRINTABLE = string.ascii_letters + string.digits + string.punctuation + " "


def random_text(rng, lo=1, hi=12):
    """A short string covering the full character vocabulary, including escapes."""
    n = rng.randint(lo, hi)
    pool = PRINTABLE if rng.random() < 0.9 else PRINTABLE + "\n\t"
    return "".join(rng.choice(pool) for _ in range(n))


def string_literal(rng, kind=None):
    r = rng.random() if kind is None else kind
    if r < 0.45:
        s = rng.choice(LABELS)
    elif r < 0.75:
        s = rng.choice(WORDS)
    elif r < 0.85:
        s = " ".join(rng.choice(WORDS) for _ in range(rng.randint(2, 4)))
    else:
        s = random_text(rng)
    return s


PATTERN_ALPHABETS = ["01", "01", "012", "10", "ab", "abc", "xy", "xo", "-=", "*.", "ACGT", string.digits]


def pattern_text(rng):
    """A repetitive string, hard to copy exactly: few distinct characters, so the
    same pairs recur with different continuations ('100101', 'abaab'), often
    after a label ('read bottom to top: 100101')."""
    alphabet = rng.choice(PATTERN_ALPHABETS)
    s = "".join(rng.choice(alphabet) for _ in range(rng.randint(3, 24)))
    if rng.random() < 0.4:
        s = rng.choice([w for w in LABELS if w.strip()] + WORDS) + " " + s
    return s


LITERAL_MAX = 999  # raised for the widened-number eval set


def small_int(rng):
    """Literal magnitudes skewed small, with real coverage of 3-digit values."""
    r = rng.random()
    if r < 0.45:
        return rng.randint(0, 10)
    if r < 0.75:
        return rng.randint(11, 99)
    if LITERAL_MAX > 999 and r < 0.9:
        return rng.randint(1000, LITERAL_MAX)
    return rng.randint(100, 999)
