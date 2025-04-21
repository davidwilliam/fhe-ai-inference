# fhe_ai_inference/layers/linear.py

from __future__ import annotations

from collections.abc import Sequence
from functools import reduce
from typing import Optional

import numpy as np
from openfhe import Ciphertext


class FHELinear:
    def __init__(
        self,
        weights: np.ndarray,
        bias: Optional[np.ndarray] = None,
        transpose_weights: bool = True,
    ):
        """
        Initialize an FHE-based linear layer.

        Args:
            weights (np.ndarray): Weight matrix of shape (out_features, in_features)
            bias (np.ndarray, optional): Bias vector of shape (out_features,)
            transpose_weights (bool): If True, transposes weights for dot product logic
        """
        if transpose_weights:
            weights = weights.T

        self.weights = weights.astype(np.float64)
        self.bias = bias.astype(np.float64) if bias is not None else None
        self.in_features, self.out_features = self.weights.shape

    def forward(
        self,
        inputs: list[Ciphertext] | list[list[Ciphertext]],
        crypto_context,
        public_key,
    ) -> list[Ciphertext] | list[list[Ciphertext]]:
        """
        If inputs is a single vector → compute W*x + b
        If inputs is a batch of vectors → apply W*x + b for each vector
        """
        is_batch = isinstance(inputs[0], Sequence) and not isinstance(
            inputs[0], Ciphertext
        )

        if is_batch:
            return [self.forward(vec, crypto_context, public_key) for vec in inputs]

        if len(inputs) != self.in_features:
            raise ValueError(f"Expected {self.in_features} inputs, got {len(inputs)}")

        outputs = []
        for i in range(self.out_features):
            weighted = [
                crypto_context.EvalMult(inputs[j], self.weights[j, i])
                for j in range(self.in_features)
            ]
            summed = reduce(lambda x, y: crypto_context.EvalAdd(x, y), weighted)

            if self.bias is not None:
                bias_plain = crypto_context.MakeCKKSPackedPlaintext([self.bias[i]])
                bias_enc = crypto_context.Encrypt(public_key, bias_plain)
                summed = crypto_context.EvalAdd(summed, bias_enc)

            outputs.append(summed)

        return outputs

    def __call__(
        self, inputs: list[Ciphertext], crypto_context, public_key
    ) -> list[Ciphertext]:
        return self.forward(inputs, crypto_context, public_key)
