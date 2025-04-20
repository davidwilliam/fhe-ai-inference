from fhe_ai_inference.ckks import setup_ckks_context
from fhe_ai_inference.activations import square_activation
from fhe_ai_inference.openfhe_ckks import CKKSOperations


def test_square_activation():
    # Setup CKKS context
    context, keypair = setup_ckks_context(
        poly_modulus_degree=16384, scaling_modulus_size=45, slots=2
    )
    assert context is not None
    assert keypair is not None

    # Use CKKSOperations for easier encryption/decryption
    ckks = CKKSOperations(poly_modulus_degree=16384, scaling_modulus_size=45, slots=2)

    # Create a sample input
    input_values = [2.0, 3.0]  # Expected squares: [4.0, 9.0]
    ciphertext = ckks.encrypt(input_values)

    # Apply square activation
    result = square_activation(ciphertext, ckks.context)

    # Decrypt and verify
    decrypted = ckks.decrypt(result)
    expected = [4.0, 9.0]  # Squared values
    for actual, exp in zip(decrypted, expected):
        assert abs(actual - exp) <= 0.1, f"Expected {exp}, got {actual}"
