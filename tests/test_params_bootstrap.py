# tests/test_params_bootstrap.py

import numpy as np

from fhe_ai_inference.params_bootstrap import build_bootstrappable_context


def test_build_bootstrappable_context():
    ctx = build_bootstrappable_context()

    # Minimal smoke test: encrypt + decrypt
    key_pair = ctx.KeyGen()
    ctx.EvalMultKeyGen(key_pair.secretKey)

    values = [3.14]
    plaintext = ctx.MakeCKKSPackedPlaintext(values)
    ciphertext = ctx.Encrypt(key_pair.publicKey, plaintext)
    decrypted = ctx.Decrypt(ciphertext, key_pair.secretKey)
    result = decrypted.GetRealPackedValue()

    assert np.allclose(result[0], values[0], rtol=1e-2)
