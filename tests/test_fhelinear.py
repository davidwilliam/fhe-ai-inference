import torch
from fhe_ai_inference.core import FHEInference
from fhe_ai_inference.encoder import encrypt_tensor, decrypt_tensor
from fhe_ai_inference.layers import FHELinear


def test_fhe_linear_layer():
    fhe = FHEInference(model=None)
    context = fhe.context
    pk = fhe.public_key
    sk = fhe.secret_key

    x = torch.tensor([1.0, 2.0])  # input vector
    w = torch.tensor([[0.5, 1.0], [-1.0, 0.0]])  # weight matrix (2×2)
    b = torch.tensor([0.0, 1.0])  # bias vector

    ctxt_x = encrypt_tensor(x, context, fhe.encrypt, pk)

    fhe_linear = FHELinear(w, b, context)
    out_ciphertexts = fhe_linear(ctxt_x)

    decrypted_outputs = [
        decrypt_tensor(c, context, fhe.decrypt, sk)[0].item() for c in out_ciphertexts
    ]

    expected = (w @ x) + b

    for actual, expected_val in zip(decrypted_outputs, expected.tolist()):
        assert abs(actual - expected_val) < 1e-1
