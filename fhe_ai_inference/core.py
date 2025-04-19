# fhe_ai_inference/core.py
from fhe_ai_inference.ckks import setup_ckks_context

import torch


class FHEInference:
    def __init__(self, model, poly_modulus_degree=16384, scaling_modulus_size=45):
        self.backend = "openfhe"
        self.model = model
        self.context = setup_ckks_context(
            poly_modulus_degree=poly_modulus_degree,
            scaling_modulus_size=scaling_modulus_size,
        )

    def predict(self, input_tensor: torch.Tensor):
        with torch.no_grad():
            output = self.model(input_tensor)
            return output
