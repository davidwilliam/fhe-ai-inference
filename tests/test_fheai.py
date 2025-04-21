# tests/test_fheai.py
import numpy as np
import pytest

from fhe_ai_inference.fheai import FHEAI


@pytest.fixture
def fheai():
    """Fixture to initialize FHEAI instance."""
    return FHEAI(mult_depth=2, scale_mod_size=50)


def test_encrypt_decrypt_scalar(fheai):
    original = 3.14
    ciphertext = fheai.encrypt(original)
    decrypted = fheai.decrypt(ciphertext, length=1)
    assert np.allclose(decrypted, [original], atol=1e-5), "Scalar decryption failed"


def test_encrypt_decrypt_list(fheai):
    original = [1.0, 2.0, 3.0]
    ciphertext = fheai.encrypt(original)
    decrypted = fheai.decrypt(ciphertext, length=len(original))
    assert np.allclose(decrypted, original, atol=1e-5), "List decryption failed"


def test_encrypt_decrypt_numpy_array(fheai):
    original = np.array([0.5, 1.5, 2.5])
    ciphertext = fheai.encrypt(original)
    decrypted = fheai.decrypt(ciphertext, length=original.size)
    assert np.allclose(decrypted, original, atol=1e-5), "Numpy array decryption failed"


def test_decrypt_precision(fheai):
    original = np.random.uniform(-10, 10, 10)
    ciphertext = fheai.encrypt(original)
    decrypted = fheai.decrypt(ciphertext, length=original.size)
    assert np.allclose(decrypted, original, atol=1e-5), "Precision test failed"
