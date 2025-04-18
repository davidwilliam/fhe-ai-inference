# fhe_ai_inference/fhe.py
from openfhe import GenCryptoContext

def setup_ckks_context(poly_modulus_degree: int = 8192, security_level: int = 128):
    """Set up a CKKS context for FHE.

    Args:
        poly_modulus_degree (int): Polynomial modulus degree (default: 8192).
        security_level (int): Security level in bits (default: 128).

    Returns:
        CryptoContext: CKKS context for homomorphic operations.
    """
    # Use the literal scheme name "CKKS"
    cc = GenCryptoContext(scheme="CKKS",
                          poly_modulus_degree=poly_modulus_degree,
                          security_level=security_level)
    cc.Enable("PKCS")
    return cc
