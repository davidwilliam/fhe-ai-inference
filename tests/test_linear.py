import numpy as np
import pytest

from fhe_ai_inference.fheai import FHEAI
from fhe_ai_inference.layers.linear import FHELinear


@pytest.fixture
def fhe():
    return FHEAI(mult_depth=4, scale_mod_size=50)


def test_fhe_linear_forward(fhe):
    input_vector = [1.0, 2.0, 3.0]
    weights = np.array([[0.5, 1.0, -1.0]])  # shape: (1, 3)
    bias = np.array([0.25])
    linear = FHELinear(weights, bias)  # transpose_weights=True by default

    enc_input = [fhe.encrypt(x) for x in input_vector]
    enc_output = linear(enc_input, fhe.crypto_context, fhe.key_pair.publicKey)
    output = fhe.decrypt(enc_output[0], length=1)[0]

    expected = np.dot(weights, input_vector)[0] + bias[0]
    assert abs(output - expected) < 1e-2, f"Expected {expected}, got {output}"
