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


SERIES_STEMS = [
    "Round", "Step", "Day", "Month", "Week", "Year", "Turn", "Level", "Customer", "Generation",
    "tick", "Floor", "Player", "Order", "Batch", "Phase", "Lap", "Test", "Case", "Item", "Box",
    "Room", "Stage", "Wave", "Hour", "Game", "Pass", "Trial", "Shelf", "Gate",
]

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


# what rules, bars and ASCII art are drawn with
RUN_FILLS = ["-", "=", "*", "~", "#", ".", " ", "_", "+", "|", "o", "<>", "-=", "ab", "[]", "xo", ". ", "/\\", "()"]
UNITS = ["s", "m", "km", "kg", "pts", "days", "weeks", "min", "C", "F", "cm", "h"]


def run_text(rng):
    """Text made of runs of one character, as written-out rules, bars and
    calendar rows are ('----------', '|=======-', ' ..... ', '  M  T  W')."""
    parts = []
    for _ in range(rng.randint(1, 4)):
        if rng.random() < 0.6:
            parts.append(rng.choice(RUN_FILLS[:11]) * rng.randint(2, 24))
        else:
            parts.append(rng.choice(WORDS + list("MTWFS|+:")))
    return "".join(parts)[:48]


def long_text(rng):
    """25-48 characters to copy and index: digit runs, patterns or words."""
    n = rng.randint(25, 48)
    r = rng.random()
    if r < 0.3:
        start = rng.randint(0, 9)
        return "".join(str((start + i) % 10) for i in range(n))
    if r < 0.6:
        alphabet = rng.choice(PATTERN_ALPHABETS)
        return "".join(rng.choice(alphabet) for _ in range(n))
    return " ".join(rng.choice(WORDS) for _ in range(12))[:n]


def label_text(rng):
    """A label of the kind long hand-written scripts print many near-identical
    copies of ('Hour 1: stove lit', 'Car at 538 s', '10 km at 5:20')."""
    stem = rng.choice(SERIES_STEMS)
    n = rng.randint(1, 12) if rng.random() < 0.7 else rng.randint(13, 999)
    word = rng.choice(WORDS).capitalize()
    r = rng.random()
    if r < 0.3:
        return f"{stem} {n}: " + " ".join(rng.choice(WORDS) for _ in range(rng.randint(1, 3)))
    if r < 0.5:
        return f"{word} at {n} {rng.choice(UNITS)}"
    if r < 0.65:
        return f"{n} {rng.choice(UNITS)} at {rng.randint(0, 23)}:{rng.randint(0, 59):02d}"
    if r < 0.8:
        return f"{word} {n} {rng.choice(UNITS)} {rng.randint(1, 9)} {rng.choice(UNITS)} {rng.choice(WORDS)}"
    return f"{word} from {stem.lower()} {n}"


def near_variant(rng, s, shuffle=True):
    """s changed a little, as near-identical strings differ: one character
    replaced or two swapped, a late word or number changed, cut short or
    extended; with shuffle, also reversed or rotated. May equal s."""
    if not s:
        return rng.choice(["a", " ", "x"])
    words = s.split(" ")
    r = rng.random() * (1.0 if shuffle else 0.77)
    if r < 0.2:
        i = rng.randrange(len(s))
        others = [c for c in sorted(set(s)) if c != s[i]] or ["."]
        out = s[:i] + rng.choice(others) + s[i + 1:]
    elif r < 0.32 and len(s) > 1:
        i = rng.randrange(len(s) - 1)
        out = s[:i] + s[i + 1] + s[i] + s[i + 2:]
    elif r < 0.5 and len(words) > 1:
        j = rng.randrange(len(words) // 2, len(words))
        if words[j].isdigit():
            n = int(words[j])
            words[j] = str(rng.randint(0, 999) if rng.random() < 0.5 else max(0, n + rng.choice([-2, -1, 1, 2, 10])))
        else:
            words[j] = rng.choice(WORDS)
        out = " ".join(words)
    elif r < 0.62:
        out = " ".join(words[:-1]) if len(words) > 1 and rng.random() < 0.6 else s[: rng.randint(0, len(s) - 1)]
    elif r < 0.77:
        out = s + (rng.choice(s) if rng.random() < 0.5 else " " + rng.choice(WORDS))
    elif r < 0.88:
        out = s[::-1]
    else:
        k = rng.randint(1, max(1, len(s) - 1))
        out = s[k:] + s[:k]
    return out[:48]


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
