from fhe_ai_inference.params import FHEContextBuilder


def test_default_params():
    context = FHEContextBuilder.build()
    assert context is not None


def test_custom_depth_scale():
    context = FHEContextBuilder.build(mult_depth=4, scale_mod_size=55)
    assert context is not None


def test_ring_dimension_override():
    ring_dim = 32768
    context = FHEContextBuilder.build(
        mult_depth=3, scale_mod_size=50, ring_dim=ring_dim
    )
    assert context.GetRingDimension() == ring_dim


def test_multiple_contexts_differ():
    ctx1 = FHEContextBuilder.build(mult_depth=2, scale_mod_size=50)
    ctx2 = FHEContextBuilder.build(mult_depth=4, scale_mod_size=55, ring_dim=32768)
    assert ctx1.GetRingDimension() != ctx2.GetRingDimension()
