from fhe_ai_inference.fheai import FHEAI
from fhe_ai_inference.params import FHEContextBuilder


def test_fheai_accepts_explicit_crypto_context():
    ctx = FHEContextBuilder.build(mult_depth=2)
    fhe = FHEAI(crypto_context=ctx)
    assert fhe.crypto_context is ctx
