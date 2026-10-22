"""Script sources. Each returns (source, base_id); base_id groups natural variants."""
from . import grammar, natural, templates

SOURCES = ("grammar", "template", "natural", "arith", "copy")


def make(rng, phase, source):
    if source == "grammar":
        return grammar.generate(rng, phase), None
    if source == "arith":
        return grammar.generate(rng, phase, arith=True), None
    if source == "copy":
        return grammar.generate(rng, phase, copy=True), None
    if source == "template":
        return templates.generate(rng, phase), None
    if source == "natural":
        return natural.generate(rng, phase)
    raise ValueError(f"unknown source {source!r}")
