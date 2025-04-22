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


def test_encrypt_with_and_without_level(fheai):
    data = [1.0, 2.0]

    # Encrypt with default level (None)
    ct1 = fheai.encrypt(data)

    # Encrypt with explicit level
    ct2 = fheai.encrypt(data, level=0)

    # Should both decrypt to the same values
    decrypted1 = fheai.decrypt(ct1, length=len(data))
    decrypted2 = fheai.decrypt(ct2, length=len(data))

    assert np.allclose(
        decrypted1, decrypted2, atol=1e-5
    ), "Level-based encrypt mismatch"


def test_bootstrap_raises_when_disabled():
    fhe = FHEAI(bootstrappable=False)
    ct = fhe.encrypt(3.14)

    with pytest.raises(RuntimeError, match="Bootstrapping is not enabled"):
        fhe.bootstrap(ct)


def test_mod_reduce_runs(fheai):
    data = [1.23, 4.56]
    ct = fheai.encrypt(data)
    reduced = fheai.mod_reduce(ct)
    result = fheai.decrypt(reduced, length=len(data))
    assert isinstance(result, np.ndarray)


def test_fhe_context_enables_fhe():
    _ = FHEAI()
    # This test doesn't assert anything — it just ensures the constructor runs
    # and hits `.Enable(PKESchemeFeature.FHE)`


def test_fheai_default_enables_fhe():
    # Create with crypto_context=None and bootstrappable=False
    fhe = FHEAI(mult_depth=1, scale_mod_size=50, bootstrappable=False)
    # The line enabling FHE should now definitely be executed
    assert fhe.crypto_context is not None  # Sanity check
