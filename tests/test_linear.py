import numpy as np
import pytest
from openfhe import Ciphertext

from fhe_ai_inference.fheai import FHEAI
from fhe_ai_inference.layers.linear import FHELinear


@pytest.fixture
def fhe():
    return FHEAI(mult_depth=2, scale_mod_size=59, bootstrappable=True)


def test_fhe_linear_forward(fhe):
    input_vector = [1.0, 2.0, 3.0]
    weights = np.array([[0.5, 1.0, -1.0]])  # shape: (1, 3)
    bias = np.array([0.25])
    linear = FHELinear(weights, bias)

    # Encrypted input at a high level
    enc_input = [fhe.encrypt(x, level=0) for x in input_vector]

    # Forward with adaptive bootstrapping
    enc_output = linear.forward(
        enc_input,
        fhe.crypto_context,
        fhe.key_pair.publicKey,
        bootstrap_fn=fhe.bootstrap,
        bootstrap_threshold=2,
    )
    output = fhe.decrypt(enc_output[0], length=1)[0]

    expected = np.dot(weights, input_vector)[0] + bias[0]
    assert abs(output - expected) < 1e-2, f"Expected {expected}, got {output}"


def test_fhe_linear_batch_forward(fhe):
    batch_input = [
        [1.0, 2.0, 3.0],
        [0.0, 1.0, 2.0],
    ]
    weights = np.array([[0.5, 1.0, -1.0]])  # shape: (1, 3)
    bias = np.array([0.25])
    linear = FHELinear(weights, bias)

    encrypted_batch = [[fhe.encrypt(x, level=0) for x in vec] for vec in batch_input]
    enc_outputs = linear.forward(
        encrypted_batch,
        fhe.crypto_context,
        fhe.key_pair.publicKey,
        bootstrap_fn=fhe.bootstrap,
        bootstrap_threshold=2,
    )

    for i, (enc_out, plain_vec) in enumerate(zip(enc_outputs, batch_input)):
        decrypted = fhe.decrypt(enc_out[0], length=1)[0]
        expected = np.dot(weights, plain_vec)[0] + bias[0]
        diff = abs(decrypted - expected)
        assert (
            diff < 1e-2
        ), f"Batch {i}: Expected {expected}, got {decrypted} (diff={diff})"


def test_forward_without_bootstrap(fhe):
    weights = np.array([[1.0]])
    linear = FHELinear(weights, bias=None)
    inp = [fhe.encrypt(2.0, level=0)]

    # Pass no bootstrap_fn
    out = linear.forward(inp, fhe.crypto_context, fhe.key_pair.publicKey)
    assert isinstance(out[0], Ciphertext)


def test_linear_transposes_weights():
    weights = np.array([[1.0, 2.0], [3.0, 4.0]])  # shape (2, 2)
    linear = FHELinear(weights, transpose_weights=True)
    assert linear.weights.shape == (2, 2)  # Post-transpose: shape (2, 2)


def test_linear_transpose_executes():
    weights = np.array([[1.0, 2.0, 3.0]])  # shape (1, 3)
    layer = FHELinear(weights, transpose_weights=True)
    assert layer.weights.shape == (3, 1)


def test_linear_input_length_mismatch(fhe):
    weights = np.array([[1.0, 2.0]])
    linear = FHELinear(weights)

    invalid_input = [fhe.encrypt(1.0, level=0)]  # only 1 element instead of 2

    with pytest.raises(ValueError, match="Expected 2 inputs, got 1"):
        linear.forward(invalid_input, fhe.crypto_context, fhe.key_pair.publicKey)
