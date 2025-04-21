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


class FHEAI:
    def __init__(self, mult_depth: int = 2, scale_mod_size: int = 50):
        """
        Initialize FHEAI with CKKS scheme for homomorphic encryption.

        Args:
            mult_depth (int): Multiplicative depth for the circuit. Default is 2.
            scale_mod_size (int): Number of bits for scaling modulus. Default is 50.
        """
        # Set up CKKS parameters
        parameters = CCParamsCKKSRNS()
        parameters.SetMultiplicativeDepth(mult_depth)
        parameters.SetScalingModSize(scale_mod_size)

        # Generate crypto context
        self.crypto_context: CryptoContext = GenCryptoContext(parameters)

        # Enable necessary features
        self.crypto_context.Enable(PKESchemeFeature.PKE)
        # Enable LEVELEDSHE for EvalMult operations
        self.crypto_context.Enable(PKESchemeFeature.LEVELEDSHE)

        # Generate key pair
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
