from openfhe.openfhe import (
    CCParamsCKKSRNS,
    GenCryptoContext,
    PKESchemeFeature,
    SecurityLevel,
)


def setup_ckks_context(poly_modulus_degree=16384, scaling_modulus_size=45, slots=3):
    params = CCParamsCKKSRNS()
    params.SetMultiplicativeDepth(3)
    params.SetSecurityLevel(SecurityLevel.HEStd_128_classic)
    params.SetScalingModSize(scaling_modulus_size)
    params.SetRingDim(poly_modulus_degree)

    context = GenCryptoContext(params)
    context.Enable(PKESchemeFeature.PKE)
    context.Enable(PKESchemeFeature.LEVELEDSHE)
    context.Enable(PKESchemeFeature.ADVANCEDSHE)

    keypair = context.KeyGen()
    context.EvalSumKeyGen(keypair.secretKey)
    context.EvalMultKeyGen(keypair.secretKey)

    powers = [2**i for i in range(slots.bit_length()) if 2**i < slots]
    indexes = powers + [-i for i in powers]
    context.EvalAtIndexKeyGen(keypair.secretKey, indexes)

    return context, keypair
