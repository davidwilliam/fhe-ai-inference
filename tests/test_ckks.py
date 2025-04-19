from fhe_ai_inference.ckks import setup_ckks_context


def test_ckks_context_creation():
    context = setup_ckks_context(poly_modulus_degree=16384, scaling_modulus_size=45)
    assert context is not None
    keypair = context.KeyGen()
    assert keypair is not None
