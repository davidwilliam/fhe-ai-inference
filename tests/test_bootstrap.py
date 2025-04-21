# tests/test_bootstrap.py

import pytest

from fhe_ai_inference.fheai import FHEAI
from fhe_ai_inference.fheai_bootstrap import BootstrapMixin
from fhe_ai_inference.params_bootstrap import build_bootstrappable_context


class BootstrappableFHE(FHEAI, BootstrapMixin):
    def __init__(self):
        super().__init__(crypto_context=build_bootstrappable_context())


@pytest.fixture
def bootstrappable_fhe():
    return BootstrappableFHE()


@pytest.mark.skip(
    reason="OpenFHE's Python bootstrap support segfaults under "
    "current bindings on macOS (CKKS EvalBootstrapSetup)."
)
def test_bootstrap_refreshes_ciphertext(bootstrappable_fhe):
    fhe = bootstrappable_fhe
    level_budget = [4, 4]
    num_slots = 8

    fhe.setup_bootstrap(level_budget, num_slots)

    x = [0.25, 0.5, 0.75, 1.0, 2.0, 3.0, 4.0, 5.0]
    encrypted = fhe.encrypt(x)
    # decrypted_before = fhe.decrypt(encrypted, length=len(x))

    refreshed = fhe.bootstrap(encrypted)
    decrypted_after = fhe.decrypt(refreshed, length=len(x))

    assert len(decrypted_after) == len(x)
    assert all(isinstance(val, float) for val in decrypted_after)
