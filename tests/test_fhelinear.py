import torch
from fhe_ai_inference.openfhe_ckks import CKKSOperations
from fhe_ai_inference.layers import FHELinear


def test_fhe_linear_layer_minimal():
    x = torch.tensor([1.0, 2.0])
    w = [[1.0, 0.0], [0.0, 1.0]]
    b = [0.0, 0.0]

    ckks = CKKSOperations(slots=2)
    ctxt_x = ckks.encrypt(x.tolist())

    layer = FHELinear(w, b, ckks)
    outputs = layer(ctxt_x)

    # outputs is already a list of decrypted value lists; take the first slot of each
    decrypted = [output[0] for output in outputs]

    # Validate results
    expected = (torch.tensor(w) @ x + torch.tensor(b)).tolist()
    for actual, expected_val in zip(decrypted, expected):
        assert abs(actual - expected_val) < 1e-1


def test_fhe_linear_no_ckks():
    w = [[1.0, 0.0], [0.0, 1.0]]
    b = [0.0, 0.0]

    # Initialize FHELinear without ckks to hit the else branch
    layer = FHELinear(w, b, ckks=None)
    assert layer.slot_len == 2  # Length of weight_matrix[0]
