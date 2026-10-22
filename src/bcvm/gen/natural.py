"""LLM-written natural scripts (natural/phase*/), plus variants with perturbed literals.

The originals keep the style of real code; perturbing int literals (and
occasionally string literals) multiplies them without changing their shape.
The model never sees source, so ast.unparse reformatting is harmless.
"""
import ast
import glob
import os

from .common import string_literal

ROOT = os.environ.get("BCVM_NATURAL") or os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "natural"))
_CACHE = {}


def load(phase, root=ROOT):
    """(phase, base_id, source) for every natural script usable in `phase`."""
    key = (phase, root)
    if key not in _CACHE:
        srcs = []
        for p in "ABCDEF"[: "ABCDEF".index(phase) + 1]:
            for path in sorted(glob.glob(os.path.join(root, f"phase{p}", "*.py"))):
                with open(path) as f:
                    srcs.append((p, os.path.basename(path)[:-3], f.read()))
        _CACHE[key] = srcs
    return _CACHE[key]


def _perturb_int(rng, v):
    if v in (0, 1) and rng.random() < 0.8:
        return v
    if v == 2 and rng.random() < 0.6:
        return v
    mag = abs(v)
    r = rng.random()
    if r < 0.5:
        new = mag + rng.randint(-max(2, mag // 3), max(2, mag // 3))
    elif r < 0.8:
        new = rng.randint(0, max(3, mag * 2))
    else:
        new = rng.randint(0, 999 if mag > 99 else 99 if mag > 9 else 12)
    new = max(0, new)
    return -new if v < 0 else new


class _Perturb(ast.NodeTransformer):
    def __init__(self, rng, p_int, p_str):
        self.rng, self.p_int, self.p_str = rng, p_int, p_str
        self.in_fstring = 0

    def visit_JoinedStr(self, node):
        self.in_fstring += 1
        self.generic_visit(node)
        self.in_fstring -= 1
        return node

    def visit_Constant(self, node):
        v = node.value
        if type(v) is int and self.rng.random() < self.p_int:
            return ast.copy_location(ast.Constant(_perturb_int(self.rng, v)), node)
        if type(v) is str and not self.in_fstring and self.rng.random() < self.p_str and len(v) > 1:
            return ast.copy_location(ast.Constant(string_literal(self.rng)), node)
        return node


def variant(rng, src, p_int=0.5, p_str=0.1):
    tree = ast.parse(src)
    tree = _Perturb(rng, p_int, p_str).visit(tree)
    return ast.unparse(tree) + "\n"


def generate(rng, phase, p_original=0.15):
    """Returns (source, base_id). Splits are assigned per base script, so every
    variant of a held-out natural script stays out of training."""
    srcs = load(phase)
    if not srcs:
        raise RuntimeError(f"no natural scripts for phase {phase} under {ROOT}")
    own = [s for s in srcs if s[0] == phase]
    pool = own if own and rng.random() < 0.75 else srcs
    _, base_id, src = rng.choice(pool)
    if rng.random() < p_original:
        return src, base_id
    return variant(rng, src), base_id
