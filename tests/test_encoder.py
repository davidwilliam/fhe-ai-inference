import torch
from fhe_ai_inference.encoder import encrypt_tensor, decrypt_tensor


def test_encrypt_decrypt_tensor():
    input_tensor = torch.tensor([1.0, 2.0])
    encrypted = encrypt_tensor(input_tensor)
    decrypted = decrypt_tensor(encrypted)
    assert torch.allclose(decrypted, input_tensor)
