# scripts/bootstrap_demo.py

from openfhe import (
    FHECKKSRNS,
    CCParamsCKKSRNS,
    CryptoContext,
    GenCryptoContext,
    PKESchemeFeature,
    ScalingTechnique,
    SecretKeyDist,
    SecurityLevel,
)


def main():
    print("🔐 Building bootstrappable CKKS context...")
    params = CCParamsCKKSRNS()
    params.SetSecretKeyDist(SecretKeyDist.UNIFORM_TERNARY)
    params.SetSecurityLevel(SecurityLevel.HEStd_NotSet)
    params.SetRingDim(1 << 12)

    rescale_tech = ScalingTechnique.FLEXIBLEAUTO
    dcrt_bits = 59
    first_mod = 60

    params.SetScalingModSize(dcrt_bits)
    params.SetScalingTechnique(rescale_tech)
    params.SetFirstModSize(first_mod)

    level_budget = [4, 4]
    levels_after_bootstrap = 10
    depth = levels_after_bootstrap + FHECKKSRNS.GetBootstrapDepth(
        level_budget,
        SecretKeyDist.UNIFORM_TERNARY,
    )
    params.SetMultiplicativeDepth(depth)

    context: CryptoContext = GenCryptoContext(params)
    context.Enable(PKESchemeFeature.PKE)
    context.Enable(PKESchemeFeature.KEYSWITCH)
    context.Enable(PKESchemeFeature.LEVELEDSHE)
    context.Enable(PKESchemeFeature.ADVANCEDSHE)
    context.Enable(PKESchemeFeature.FHE)

    print("✅ Context created.")

    num_slots = 8
    print(f"📐 Bootstrapping with {num_slots} slots and level_budget {level_budget}...")
    context.EvalBootstrapSetup(level_budget, [0, 0], num_slots)

    print("🔑 Generating keys...")
    keypair = context.KeyGen()
    context.EvalMultKeyGen(keypair.secretKey)
    context.EvalBootstrapKeyGen(keypair.secretKey, num_slots)

    values = [0.25, 0.5, 0.75, 1.0, 2.0, 3.0, 4.0, 5.0]
    ptxt = context.MakeCKKSPackedPlaintext(values, 1, depth - 1, None, num_slots)
    ptxt.SetLength(len(values))

    print(f"🔒 Encrypting: {values}")
    ciph = context.Encrypt(keypair.publicKey, ptxt)

    print(f"➡️  Ciphertext level before bootstrap: {ciph.GetLevel()}")
    ciph_refreshed = context.EvalBootstrap(ciph)
    print(f"✅ Ciphertext level after bootstrap: {ciph_refreshed.GetLevel()}")

    result = context.Decrypt(ciph_refreshed, keypair.secretKey)
    result.SetLength(len(values))
    print(f"🔓 Decrypted result after bootstrap: {result.GetCKKSPackedValue()}")


if __name__ == "__main__":
    main()
