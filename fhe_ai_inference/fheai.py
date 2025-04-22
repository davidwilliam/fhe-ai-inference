# fhe_ai_inference/fheai.py

from typing import List, Union

import numpy as np
from openfhe import (
    FHECKKSRNS,
    CCParamsCKKSRNS,
    Ciphertext,
    CryptoContext,
    GenCryptoContext,
    KeyPair,
    PKESchemeFeature,
    ScalingTechnique,
    SecretKeyDist,
    SecurityLevel,
)


class FHEAI:
    def __init__(
        self,
        mult_depth: int = 2,
        scale_mod_size: int = 50,
        crypto_context: CryptoContext = None,
        bootstrappable: bool = False,
        num_slots: int = 2048,
        level_budget: list[int] = None,
        ring_dim: int = 1 << 12,
    ):
        level_budget = level_budget or [3, 3]
        self._bootstrappable = bootstrappable
        self._num_slots = num_slots
        self.level_budget = level_budget

        if crypto_context is not None:
            self.crypto_context = crypto_context
        else:
            params = CCParamsCKKSRNS()

            if bootstrappable:
                params.SetSecretKeyDist(SecretKeyDist.UNIFORM_TERNARY)
                params.SetSecurityLevel(SecurityLevel.HEStd_NotSet)
                params.SetRingDim(ring_dim)
                params.SetScalingModSize(scale_mod_size)
                params.SetScalingTechnique(ScalingTechnique.FLEXIBLEAUTO)
                params.SetFirstModSize(60)

                depth = FHECKKSRNS.GetBootstrapDepth(
                    level_budget, SecretKeyDist.UNIFORM_TERNARY
                ) + sum(level_budget)
                params.SetMultiplicativeDepth(depth)
            else:
                params.SetMultiplicativeDepth(mult_depth)
                params.SetScalingModSize(scale_mod_size)

            self.crypto_context = GenCryptoContext(params)
            self.crypto_context.Enable(PKESchemeFeature.PKE)
            self.crypto_context.Enable(PKESchemeFeature.LEVELEDSHE)
            self.crypto_context.Enable(PKESchemeFeature.FHE)

        self.key_pair: KeyPair = self.crypto_context.KeyGen()
        self.crypto_context.EvalMultKeyGen(self.key_pair.secretKey)

        if bootstrappable:
            self.crypto_context.Enable(PKESchemeFeature.KEYSWITCH)
            self.crypto_context.Enable(PKESchemeFeature.ADVANCEDSHE)
            self.crypto_context.EvalBootstrapSetup(
                self.level_budget,
                [0, 0],
                self._num_slots,
            )
            self.crypto_context.EvalBootstrapKeyGen(
                self.key_pair.secretKey,
                self._num_slots,
            )

    def encrypt(
        self, data: Union[float, List[float], np.ndarray], level: int = None
    ) -> Ciphertext:
        if isinstance(data, (float, int)):
            data = np.array([float(data)])
        elif isinstance(data, list):
            data = np.array(data, dtype=float)
        elif not isinstance(data, np.ndarray):
            raise ValueError("Input must be a float, list of floats, or numpy array")

        slots = self._num_slots  # this ensures consistency with bootstrapping setup

        if level is None:
            plaintext = self.crypto_context.MakeCKKSPackedPlaintext(
                data.tolist(), 1, 0, None, slots
            )
        else:
            plaintext = self.crypto_context.MakeCKKSPackedPlaintext(
                data.tolist(), 1, level, None, slots
            )

        return self.crypto_context.Encrypt(self.key_pair.publicKey, plaintext)

    def decrypt(self, ciphertext: Ciphertext, length: int = None) -> np.ndarray:
        plaintext = self.crypto_context.Decrypt(ciphertext, self.key_pair.secretKey)
        result = plaintext.GetRealPackedValue()
        return np.array(result[:length] if length is not None else result)

    def add(self, ciphertext1: Ciphertext, ciphertext2: Ciphertext) -> Ciphertext:
        return self.crypto_context.EvalAdd(ciphertext1, ciphertext2)

    def multiply(self, ciphertext1: Ciphertext, ciphertext2: Ciphertext) -> Ciphertext:
        return self.crypto_context.EvalMult(ciphertext1, ciphertext2)

    def mod_reduce(self, ciphertext: Ciphertext) -> Ciphertext:
        return self.crypto_context.ModReduce(ciphertext)

    def multiply_and_rescale(self, c1: Ciphertext, c2: Ciphertext) -> Ciphertext:
        return self.mod_reduce(self.multiply(c1, c2))

    def bootstrap(self, ciphertext: Ciphertext) -> Ciphertext:
        if not self._bootstrappable:
            raise RuntimeError("Bootstrapping is not enabled for this instance.")
        return self.crypto_context.EvalBootstrap(ciphertext)
