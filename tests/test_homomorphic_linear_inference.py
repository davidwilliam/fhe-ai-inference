import torch
from fhe_ai_inference.core import FHEInference
from fhe_ai_inference.encoder import encrypt_tensor, decrypt_tensor


def test_homomorphic_linear_inference():
    # Initialize FHE setup
    fhe = FHEInference(model=None)
    context = fhe.context
    pk = fhe.public_key
    sk = fhe.secret_key

    # Plaintext input and model parameters
    x = torch.tensor([1.0, 2.0, 3.0])  # Input vector
    w = torch.tensor([0.5, -1.0, 2.0])  # Weights
    b = torch.tensor([1.0])  # Scalar bias

    # Encrypt the input vector
    ctxt_x = encrypt_tensor(x, context, fhe.encrypt, pk)

    # Encode weights and broadcast bias across all slots
    pt_w = context.MakeCKKSPackedPlaintext(w.tolist())
    pt_b = context.MakeCKKSPackedPlaintext([b.item()] * len(x))  # Broadcasted bias

    # Homomorphic computation: (x * w) + b
    ctxt_mul = context.EvalMult(ctxt_x, pt_w)
    ctxt_result = context.EvalAdd(ctxt_mul, pt_b)

    # Decrypt and compare
    decrypted = decrypt_tensor(ctxt_result, context, fhe.decrypt, sk)
    expected = (x * w) + b  # Element-wise multiply + scalar bias

    # Validate approximation with tolerance
    assert torch.allclose(decrypted[: len(x)], expected, atol=1e-1)
