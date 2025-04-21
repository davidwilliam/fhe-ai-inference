# fhe_ai_inference/fheai.py
from typing import List, Union

import numpy as np
from openfhe import (
    CCParamsCKKSRNS,
    Ciphertext,
    CryptoContext,
    GenCryptoContext,
    KeyPair,
    PKESchemeFeature,
)

from fhe_ai_inference.fheai_bootstrap import BootstrapMixin


class FHEAI(BootstrapMixin):
    def __init__(
        self,
        mult_depth: int = 2,
        scale_mod_size: int = 50,
        crypto_context: CryptoContext = None,
    ):
        """
        Initialize FHEAI with CKKS scheme for homomorphic encryption.
        If a crypto_context is provided, it will override mult_depth and scale_mod_size.
        """
        if crypto_context is not None:
            self.crypto_context = crypto_context
        else:
            params = CCParamsCKKSRNS()
            params.SetMultiplicativeDepth(mult_depth)
            params.SetScalingModSize(scale_mod_size)
            self.crypto_context = GenCryptoContext(params)

            self.crypto_context.Enable(PKESchemeFeature.PKE)
            self.crypto_context.Enable(PKESchemeFeature.LEVELEDSHE)
            self.crypto_context.Enable(PKESchemeFeature.FHE)

        self.key_pair: KeyPair = self.crypto_context.KeyGen()
        self.crypto_context.EvalMultKeyGen(self.key_pair.secretKey)

    def encrypt(self, data: Union[float, List[float], np.ndarray]) -> Ciphertext:
        """
        Encrypt a scalar, list, or numpy array using CKKS.

        Args:
            data: Input data to encrypt (float, list of floats, or numpy array).

        Returns:
            Ciphertext: Encrypted data.
        """
        # Convert input to numpy array for consistency
        if isinstance(data, (float, int)):
            data = np.array([float(data)])
        elif isinstance(data, list):
            data = np.array(data, dtype=float)
        elif not isinstance(data, np.ndarray):
            raise ValueError("Input must be a float, list of floats, or numpy array")

        # Encode data as plaintext
        plaintext = self.crypto_context.MakeCKKSPackedPlaintext(data.tolist())

        # Encrypt
        return self.crypto_context.Encrypt(self.key_pair.publicKey, plaintext)

    def decrypt(self, ciphertext: Ciphertext, length: int = None) -> np.ndarray:
        """
        Decrypt a ciphertext to retrieve the original data.

        Args:
            ciphertext: Ciphertext to decrypt.
            length: Optional; length of original data.

        Returns:
            np.ndarray: Decrypted data as a numpy array.
        """
        plaintext = self.crypto_context.Decrypt(ciphertext, self.key_pair.secretKey)
        decrypted_data = plaintext.GetRealPackedValue()

        if length is not None:
            decrypted_data = decrypted_data[:length]

        return np.array(decrypted_data)

    def add(self, ciphertext1: Ciphertext, ciphertext2: Ciphertext) -> Ciphertext:
        """
        Homomorphically add two ciphertexts.
        """
        return self.crypto_context.EvalAdd(ciphertext1, ciphertext2)

    def multiply(self, ciphertext1: Ciphertext, ciphertext2: Ciphertext) -> Ciphertext:
        """
        Homomorphically multiply two ciphertexts.
        """
        return self.crypto_context.EvalMult(ciphertext1, ciphertext2)
