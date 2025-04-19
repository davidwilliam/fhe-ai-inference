import torch


def encrypt_tensor(tensor, context, encrypt_fn, public_key):
    values = tensor.numpy().tolist()
    plaintext = context.MakeCKKSPackedPlaintext(values)
    ciphertext = encrypt_fn(public_key, plaintext)
    return ciphertext


def decrypt_tensor(ciphertext, context, decrypt_fn, private_key, original_len=None):
    decrypted = decrypt_fn(private_key, ciphertext)
    decoded = decrypted.GetRealPackedValue()
    if original_len is not None:
        decoded = decoded[:original_len]
    return torch.tensor(decoded)
