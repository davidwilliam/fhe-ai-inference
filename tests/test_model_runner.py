# tests/test_model_runner.py

import numpy as np
import pytest

from fhe_ai_inference.fheai import FHEAI
from fhe_ai_inference.layers.linear import FHELinear
from fhe_ai_inference.runner.model_runner import FHEModelRunner


@pytest.fixture
def fhe():
    return FHEAI(mult_depth=6, scale_mod_size=59, bootstrappable=True)


def test_fhe_model_runner_forward(fhe):
    # Define input
    x = [1.0, 2.0]

    # Layer 1: 2 -> 2
    weights1 = np.array([[1.0, 0.0], [0.0, 1.0]])
    bias1 = np.array([0.0, 0.0])
    layer1 = FHELinear(weights1, bias1)

    # Layer 2: 2 -> 1
    weights2 = np.array([[0.5, -1.0]])
    bias2 = np.array([0.25])
    layer2 = FHELinear(weights2, bias2)

    model = FHEModelRunner(
        fhe=fhe,
        layers=[layer1, layer2],
        bootstrap_threshold=3,
    )

    # Run encrypted model
    outputs = model(x)
    output = outputs[0]  # Already decrypted

    # Compute expected result
    x_np = np.array(x)
    expected = np.dot(weights2, np.dot(weights1, x_np))[0] + bias2[0]

    # Assert correctness
    assert abs(output - expected) < 1e-2, f"Expected {expected}, got {output}"
