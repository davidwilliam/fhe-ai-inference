import torch
from fhe_ai_inference.core import FHEInference
from fhe_ai_inference.encoder import encrypt_tensor, decrypt_tensor
from fhe_ai_inference.layers import FHELinear


def test_fhe_linear_layer():
    # Initialize FHE context and keys
    fhe = FHEInference(model=None)
    context = fhe.context
    pk = fhe.public_key
    sk = fhe.secret_key

    # Define plaintext input and weights
    x = torch.tensor([1.0, 2.0])  # input vector
    w = torch.tensor([[0.5, 1.0], [-1.0, 0.0]])  # weight matrix (2×2)
    b = torch.tensor([0.0, 1.0])  # bias vector

    # Encrypt the input vector
    ctxt_x = encrypt_tensor(x, context, fhe.encrypt, pk)

    # Instantiate and apply the homomorphic linear layer
    fhe_linear = FHELinear(w, b, context)
    out_ciphertexts = fhe_linear(ctxt_x)

    # Decrypt each output ciphertext
    decrypted_outputs = [
        decrypt_tensor(c, context, fhe.decrypt, sk)[0].item() for c in out_ciphertexts
    ]

    # Compute expected plaintext result
    expected = (w @ x) + b

    # Assert homomorphic result is approximately equal
    for actual, expected_val in zip(decrypted_outputs, expected.tolist()):
        assert abs(actual - expected_val) < 1e-1
