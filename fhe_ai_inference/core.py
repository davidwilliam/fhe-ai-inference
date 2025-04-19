from fhe_ai_inference.ckks import setup_ckks_context


class FHEInference:
    def __init__(self, model, poly_modulus_degree=16384, scaling_modulus_size=45):
        self.backend = "openfhe"
        self.model = model
        self.context = setup_ckks_context(
            poly_modulus_degree=poly_modulus_degree,
            scaling_modulus_size=scaling_modulus_size,
        )

        self.encoder = self.context
        self.decoder = self.context
        self.keypair = self.context.KeyGen()
        self.public_key = self.keypair.publicKey
        self.secret_key = self.keypair.secretKey
        self.encrypt = self.context.Encrypt
        self.decrypt = self.context.Decrypt

    def predict(self, input_tensor):
        import torch

        with torch.no_grad():
            return self.model(input_tensor)
