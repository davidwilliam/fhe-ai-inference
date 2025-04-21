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


def test_invalid_input(fheai):
    """Test that invalid input types raise an error."""
    with pytest.raises(
        ValueError, match="Input must be a float, list of floats, or numpy array"
    ):
        fheai.encrypt("invalid")


def test_homomorphic_addition(fheai):
    original1 = np.array([1.0, 2.0, 3.0])
    original2 = np.array([4.0, 5.0, 6.0])

    ciphertext1 = fheai.encrypt(original1)
    ciphertext2 = fheai.encrypt(original2)

    result_ciphertext = fheai.add(ciphertext1, ciphertext2)
    decrypted_result = fheai.decrypt(result_ciphertext, length=original1.size)

    assert np.allclose(
        decrypted_result, original1 + original2, atol=1e-5
    ), "Homomorphic addition failed"


def test_homomorphic_multiplication(fheai):
    original1 = np.array([2.0, 3.0, 4.0])
    original2 = np.array([5.0, 6.0, 7.0])

    ciphertext1 = fheai.encrypt(original1)
    ciphertext2 = fheai.encrypt(original2)

    result_ciphertext = fheai.multiply(ciphertext1, ciphertext2)
    decrypted_result = fheai.decrypt(result_ciphertext, length=original1.size)

    assert np.allclose(
        decrypted_result, original1 * original2, atol=1e-3
    ), "Homomorphic multiplication failed"
