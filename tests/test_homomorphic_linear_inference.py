import torch

from fhe_ai_inference.core import FHEInference
from fhe_ai_inference.encoder import decrypt_tensor, encrypt_tensor


def test_homomorphic_linear_inference():
    fhe = FHEInference(model=None)
    context = fhe.context
    pk = fhe.public_key
    sk = fhe.secret_key

    x = torch.tensor([1.0, 2.0, 3.0])
    w = torch.tensor([0.5, -1.0, 2.0])
    b = torch.tensor([1.0])

    ctxt_x = encrypt_tensor(x, context, fhe.encrypt, pk)

    pt_w = context.MakeCKKSPackedPlaintext(w.tolist())
    pt_b = context.MakeCKKSPackedPlaintext([b.item()] * len(x))

    ctxt_mul = context.EvalMult(ctxt_x, pt_w)
    ctxt_result = context.EvalAdd(ctxt_mul, pt_b)

    decrypted = decrypt_tensor(ctxt_result, context, fhe.decrypt, sk)
    expected = (x * w) + b

    assert torch.allclose(decrypted[: len(x)], expected, atol=1e-1)
