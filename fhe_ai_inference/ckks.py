from openfhe.openfhe import (
    GenCryptoContext,
    CCParamsCKKSRNS,
    SecurityLevel,
    PKESchemeFeature,
)


def setup_ckks_context(poly_modulus_degree=16384, scaling_modulus_size=45):
    params = CCParamsCKKSRNS()
    params.SetMultiplicativeDepth(3)
    params.SetSecurityLevel(SecurityLevel.HEStd_128_classic)
    params.SetScalingModSize(scaling_modulus_size)
    params.SetRingDim(poly_modulus_degree)

    context = GenCryptoContext(params)
    context.Enable(PKESchemeFeature.PKE)
    context.Enable(PKESchemeFeature.LEVELEDSHE)
    context.KeyGen()

    return context
