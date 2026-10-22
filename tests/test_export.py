"""ONNX export (web demo): the graph matches StepModel through the split cache."""
import asyncio

import numpy as np
import pytest

torch = pytest.importorskip("torch")
pytest.importorskip("onnxruntime")
pytest.importorskip("onnxscript")

from bcvm.train.export import CachedStep, OrtModel, empty_cache, export, ort_forward, ort_session  # noqa: E402
from bcvm.train.model import ModelConfig, StepModel  # noqa: E402


def test_export_matches_torch_through_the_cache(tmp_path):
    torch.manual_seed(0)
    cfg = ModelConfig(d_model=64, n_layers=2, n_heads=4, d_ff=128)
    model = StepModel(cfg).eval()
    path = str(tmp_path / "m.onnx")
    export(model, path)
    sess, step = ort_session(path), CachedStep(model)
    e = empty_cache(cfg)
    en = [x.numpy() for x in e]
    rng = np.random.default_rng(0)
    listing, a, b = (rng.integers(0, cfg.vocab_size, n).tolist() for n in (40, 9, 5))
    with torch.no_grad():
        _, pk, pv = step(torch.tensor([listing]), torch.arange(40)[None], *e, *e)
        la, sk, sv = step(torch.tensor([a]), torch.arange(40, 49)[None], pk, pv, *e)
        lb, _, _ = step(torch.tensor([b]), torch.arange(49, 54)[None], pk, pv, sk, sv)
    _, opk, opv = ort_forward(sess, [listing], np.arange(40)[None], *en, *en)
    oa, osk, osv = ort_forward(sess, [a], np.arange(40, 49)[None], opk, opv, *en)
    ob, _, _ = ort_forward(sess, [b], np.arange(49, 54)[None], opk, opv, osk, osv)
    assert np.abs(oa - la.numpy()).max() < 1e-4 and np.abs(ob - lb.numpy()).max() < 1e-4
    # the same through OrtModel, web.run's interface: prefill, forward, truncate
    m = OrtModel(path)
    V = cfg.vocab_size
    allow_all = bytes([1]) * (V * 9)

    async def run():
        await m.prefill(listing)
        first = await m.forward(a, allow_all)
        m.truncate(4)                                  # drop the last 5 of the 9 step tokens
        again = await m.forward(a[4:], allow_all[: V * 5])
        return first, again
    first, again = asyncio.run(run())
    assert first == la[0].argmax(-1).tolist() and again == first[4:]
