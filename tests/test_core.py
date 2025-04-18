# tests/test_core.py
from fhe_ai_inference.core import FHEInference


def test_fhe_inference_init():
    """Test initialization of FHEInference class."""
    fhe_inf = FHEInference(model=None, backend="openfhe")
    assert isinstance(fhe_inf, FHEInference)
    assert fhe_inf.backend == "openfhe"
    assert fhe_inf.model is None
    assert fhe_inf.context is None
