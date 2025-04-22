import numpy as np
import pytest

from fhe_ai_inference.fheai import FHEAI
from fhe_ai_inference.layers.linear import FHELinear


@pytest.fixture
def fhe():
    return FHEAI(mult_depth=2, scale_mod_size=59)


def test_linear_no_bias_no_transpose(fhe):
    weights = np.array([[1.0, 2.0], [3.0, 4.0]])  # shape (2, 2), no transpose
    linear = FHELinear(weights, bias=None)

    input_vector = [1.0, 2.0]
    enc_input = [fhe.encrypt(x, level=0) for x in input_vector]
    outputs = linear(enc_input, fhe.crypto_context, fhe.key_pair.publicKey)

    decrypted = [fhe.decrypt(c, length=1)[0] for c in outputs]
    # Expected: dot(weights[i], input_vector)
    expected = [np.dot(weights[i], input_vector) for i in range(2)]
    assert np.allclose(
        decrypted, expected, rtol=1e-2
    ), f"Expected {expected}, got {decrypted}"


def test_linear_input_length_mismatch(fhe):
    weights = np.array([[1.0, 2.0]])  # expects 2 features
    linear = FHELinear(weights)

    wrong_input = [fhe.encrypt(1.0, level=0)]  # only 1 feature
    with pytest.raises(ValueError, match="Expected 2 inputs, got 1"):
        linear(wrong_input, fhe.crypto_context, fhe.key_pair.publicKey)


def test_linear_bootstrap_not_triggered(fhe):
    weights = np.array([[1.0, 2.0]])
    bias = np.array([0.0])
    linear = FHELinear(weights, bias)

    # Small input, low levels → no bootstrap
    input_vector = [1.0, 2.0]
    enc_input = [fhe.encrypt(x, level=0) for x in input_vector]

    outputs = linear.forward(
        enc_input,
        fhe.crypto_context,
        fhe.key_pair.publicKey,
        bootstrap_fn=fhe.bootstrap,  # will NOT be called
        bootstrap_threshold=999,  # unreachable threshold
    )

    decrypted = fhe.decrypt(outputs[0], length=1)[0]
    expected = np.dot(weights, input_vector)[0] + bias[0]
    assert abs(decrypted - expected) < 1e-2
