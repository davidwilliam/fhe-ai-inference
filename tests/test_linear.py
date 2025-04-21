import numpy as np
import pytest

from fhe_ai_inference.fheai import FHEAI
from fhe_ai_inference.layers.linear import FHELinear


@pytest.fixture
def fhe():
    return FHEAI(mult_depth=4, scale_mod_size=50)


def test_fhe_linear_forward(fhe):
    # Single input vector
    input_vector = [1.0, 2.0, 3.0]
    weights = np.array([[0.5, 1.0, -1.0]])  # shape: (1, 3)
    bias = np.array([0.25])
    linear = FHELinear(weights, bias)  # transpose=True → shape becomes (3, 1)

    enc_input = [fhe.encrypt(x) for x in input_vector]
    enc_output = linear(enc_input, fhe.crypto_context, fhe.key_pair.publicKey)
    output = fhe.decrypt(enc_output[0], length=1)[0]

    expected = np.dot(weights, input_vector)[0] + bias[0]
    assert abs(output - expected) < 1e-2, f"Expected {expected}, got {output}"


def test_fhe_linear_batch_forward(fhe):
    # Batch of two input vectors
    batch_input = [
        [1.0, 2.0, 3.0],
        [0.0, 1.0, 2.0],
    ]
    weights = np.array([[0.5, 1.0, -1.0]])  # shape: (1, 3)
    bias = np.array([0.25])
    linear = FHELinear(weights, bias)

    encrypted_batch = [[fhe.encrypt(x) for x in vec] for vec in batch_input]
    enc_outputs = linear(encrypted_batch, fhe.crypto_context, fhe.key_pair.publicKey)

    for i, (enc_out, plain_vec) in enumerate(zip(enc_outputs, batch_input)):
        decrypted = fhe.decrypt(enc_out[0], length=1)[0]
        expected = np.dot(weights, plain_vec)[0] + bias[0]
        assert (
            abs(decrypted - expected) < 1e-2
        ), f"Batch {i}: Expected {expected}, got {decrypted}"
