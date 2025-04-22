# tests/test_bootstrap.py

import numpy as np
import pytest

from fhe_ai_inference.fheai import FHEAI


@pytest.fixture
def fhe():
    return FHEAI(
        bootstrappable=True,
        level_budget=[4, 4],
        num_slots=8,
        scale_mod_size=59,
        ring_dim=1 << 12,
    )


def test_bootstrap_recovers_accuracy(fhe):
    values = [1.0, 2.0]
    initial_level = 6

    # Encrypt values at high level
    enc = fhe.encrypt(values, level=initial_level)

    # Exhaust depth (x^4)
    for _ in range(2):
        enc = fhe.multiply_and_rescale(enc, enc)

    enc = fhe.bootstrap(enc)

    # Decrypt and compare
    decrypted = fhe.decrypt(enc, length=len(values))
    expected = np.power(values, 4)

    # Focus on numerical correctness, not internal level behavior
    assert np.allclose(
        decrypted, expected, rtol=1e-2
    ), f"Expected {expected}, got {decrypted}"
