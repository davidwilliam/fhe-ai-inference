from openfhe import (
    CCParamsCKKSRNS,
    CryptoContext,
    GenCryptoContext,
    PKESchemeFeature,
    ScalingTechnique,
    SecretKeyDist,
    SecurityLevel,
)


def build_bootstrappable_context() -> CryptoContext:
    params = CCParamsCKKSRNS()

    params.SetSecretKeyDist(SecretKeyDist.UNIFORM_TERNARY)
    params.SetSecurityLevel(SecurityLevel.HEStd_NotSet)
    params.SetRingDim(1 << 12)

    params.SetScalingModSize(59)
    params.SetScalingTechnique(ScalingTechnique.FLEXIBLEAUTO)
    params.SetFirstModSize(60)

    # Estimate required multiplicative depth based on the example
    depth = 10 + 8  # conservative estimate

    params.SetMultiplicativeDepth(depth)

    context = GenCryptoContext(params)
    context.Enable(PKESchemeFeature.PKE)
    context.Enable(PKESchemeFeature.KEYSWITCH)
    context.Enable(PKESchemeFeature.LEVELEDSHE)
    context.Enable(PKESchemeFeature.ADVANCEDSHE)
    context.Enable(PKESchemeFeature.FHE)

    return context
