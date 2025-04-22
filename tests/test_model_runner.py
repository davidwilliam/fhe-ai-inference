# tests/test_model_runner.py

from unittest.mock import MagicMock

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


def test_model_runner_direct_run(fhe):
    weights = np.array([[1.0]])
    bias = np.array([0.0])
    linear = FHELinear(weights, bias)
    model = FHEModelRunner(fhe=fhe, layers=[linear])

    out = model.run([1.0])
    assert isinstance(out, list)


def test_model_runner_call_triggers_run(fhe):
    weights = np.array([[1.0]])
    bias = np.array([0.0])
    layer = FHELinear(weights, bias)
    model = FHEModelRunner(fhe=fhe, layers=[layer])
    out = model([1.0])
    assert isinstance(out, list)


def test_model_runner_docstring_exists():
    assert "Runs a sequence of FHE-compatible layers" in FHEModelRunner.__init__.__doc__


def test_model_runner_call_calls_run(fhe):
    weights = np.array([[2.0]])
    bias = np.array([0.0])
    layer = FHELinear(weights, bias)
    model = FHEModelRunner(fhe, layers=[layer])

    result = model([1.0])
    assert isinstance(result, list)
    assert np.allclose(result[0], 2.0, atol=1e-2)


def test_model_runner_call_uses_run():
    mock_runner = FHEModelRunner(fhe=MagicMock(), layers=[])
    mock_runner.run = MagicMock(return_value=[42.0])
    result = mock_runner([1.0])
    mock_runner.run.assert_called_once_with([1.0])
    assert result == [42.0]


def test_model_runner_call_directly_triggers_run():
    # Avoid mocking to keep coverage happy
    class DummyFHE:
        def encrypt(self, val, level=0):
            return val

        def decrypt(self, val, length=1):
            return [val]

        @property
        def crypto_context(self):
            return None

        @property
        def key_pair(self):
            class DummyKey:
                def __getattr__(self, name):
                    if name == "publicKey":
                        return None
                    raise AttributeError(f"{name} not found")

            return DummyKey()

        def bootstrap(self, ct):
            return ct

    class DummyLayer:
        def forward(self, inputs, *_args, **_kwargs):
            return inputs

    runner = FHEModelRunner(fhe=DummyFHE(), layers=[DummyLayer()])
    result = runner([42.0])
    assert result == [42.0]
