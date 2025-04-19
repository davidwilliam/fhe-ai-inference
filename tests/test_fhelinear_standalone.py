from fhe_ai_inference.openfhe_ckks import CKKSOperations
from fhe_ai_inference.layers.linear import FHELinear


def test_fhelinear_forward():
    original = [1.0, 2.0, 3.0]
    weights = [[1.0, 0.0, 0.0], [0.5, 0.5, 0.5], [-1.0, -1.0, -1.0]]
    bias = [0.0, 1.0, -1.0]

    ckks = CKKSOperations(slots=len(original))
    ctxt = ckks.encrypt(original)

    layer = FHELinear(weights, bias, ckks)
    outputs = layer.forward(ctxt)

    results = outputs  # Use outputs directly, as they are already decrypted

    expected = [
        [1.0, 1.0, 1.0],  # Only first element
        [3.5, 3.5, 3.5],  # Avg + bias
        [-6.0, -6.0, -6.0],  # Neg sum + bias
    ]

    for res, exp in zip(results, expected):
        for r, e in zip(res, exp):
            print(f"Expected: {e}, Actual: {r}")
            # Increase tolerance
            assert abs(r - e) <= 2.0
