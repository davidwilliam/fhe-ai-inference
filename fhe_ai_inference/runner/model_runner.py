from __future__ import annotations

from typing import TYPE_CHECKING

from fhe_ai_inference.layers.linear import FHELinear

if TYPE_CHECKING:
    from fhe_ai_inference.fheai import FHEAI


class FHEModelRunner:
    def __init__(
        self, fhe: FHEAI, layers: list[FHELinear], bootstrap_threshold: int = 10
    ):
        """
        Runs a sequence of FHE-compatible layers over encrypted input.

        Args:
            layers (list): List of layers (e.g., FHELinear instances)
            fhe (FHEAI): FHE context and key manager
        """
        self.fhe = fhe
        self.layers = layers
        self.bootstrap_threshold = bootstrap_threshold

    def run(self, x: list[float]) -> list[float]:
        encrypted = [self.fhe.encrypt(val, level=0) for val in x]
        for layer in self.layers:
            encrypted = layer.forward(
                encrypted,
                self.fhe.crypto_context,
                self.fhe.key_pair.publicKey,
                bootstrap_fn=self.fhe.bootstrap,
                bootstrap_threshold=self.bootstrap_threshold,
            )
        return [self.fhe.decrypt(ciph, length=1)[0] for ciph in encrypted]

    def __call__(self, x: list[float]) -> list[float]:
        return self.run(x)
