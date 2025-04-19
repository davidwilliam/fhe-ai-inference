from fhe_ai_inference.core import FHEInference
from fhe_ai_inference.encoder import encrypt_tensor, decrypt_tensor
import torch


def test_encrypt_decrypt_tensor():
    fhe = FHEInference(model=None)
    input_tensor = torch.tensor([1.0, 2.0])

    encrypted = encrypt_tensor(input_tensor, fhe.context, fhe.encrypt, fhe.public_key)
    decrypted = decrypt_tensor(
        encrypted,
        fhe.context,
        fhe.decrypt,
        fhe.secret_key,
        original_len=len(input_tensor),
    )

    assert torch.allclose(decrypted, input_tensor, atol=1e-1)
