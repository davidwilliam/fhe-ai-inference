# fhe_ai_inference/fheai_bootstrap.py

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from openfhe import Ciphertext

if TYPE_CHECKING:
    from fhe_ai_inference.fheai import FHEAI


class BootstrapMixin:
    def setup_bootstrap(
        self: FHEAI,
        level_budget: Optional[list[int]] = None,
        num_slots: int = 8,
    ) -> None:
        """
        Prepare the context for bootstrapping by performing setup and key generation.

        Args:
            level_budget (list[int]): Budget for encoding/decoding levels.
            Default is [4, 4].
            num_slots (int): Number of slots to use. Default is 8.
        """
        if level_budget is None:
            level_budget = [4, 4]

        self.crypto_context.EvalBootstrapSetup(level_budget)
        self.crypto_context.EvalBootstrapKeyGen(self.key_pair.secretKey, num_slots)

    def bootstrap(self: FHEAI, ciphertext: Ciphertext) -> Ciphertext:
        """
        Refresh a ciphertext to restore noise budget using CKKS bootstrapping.

        Args:
            ciphertext (Ciphertext): Encrypted input.

        Returns:
            Ciphertext: Refreshed ciphertext.
        """
        return self.crypto_context.EvalBootstrap(ciphertext)
