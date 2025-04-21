# fhe_ai_inference/params.py

from openfhe import CCParamsCKKSRNS, CryptoContext, GenCryptoContext, PKESchemeFeature


class FHEContextBuilder:
    @staticmethod
    def build(
        mult_depth: int = 2, scale_mod_size: int = 50, ring_dim: int = None
    ) -> CryptoContext:
        """
        Build a CryptoContext for CKKS with custom parameters.

        Args:
            mult_depth (int): Multiplicative depth.
            scale_mod_size (int): Scaling modulus size in bits.
            ring_dim (int, optional): Optional ring dimension override.

        Returns:
            CryptoContext: Configured crypto context.
        """
        params = CCParamsCKKSRNS()
        params.SetMultiplicativeDepth(mult_depth)
        params.SetScalingModSize(scale_mod_size)
        if ring_dim is not None:
            params.SetRingDim(ring_dim)

        context = GenCryptoContext(params)
        context.Enable(PKESchemeFeature.PKE)
        context.Enable(PKESchemeFeature.LEVELEDSHE)

        return context
