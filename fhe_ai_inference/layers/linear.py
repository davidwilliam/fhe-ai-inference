from fhe_ai_inference.openfhe_ckks import CKKSOperations
from decimal import Decimal, ROUND_HALF_UP


class FHELinear:
    def __init__(self, weight_matrix, bias_vector=None, ckks: CKKSOperations = None):
        self.weights = weight_matrix
        self.bias = bias_vector
        self.ckks = ckks

        if hasattr(ckks, "active_slots"):
            self.slot_len = ckks.active_slots
        else:
            # fallback: assume len of inputs (e.g., weights[0])
            self.slot_len = len(weight_matrix[0])

    def __call__(self, encrypted_input):
        return self.forward(encrypted_input)

    def round_value(self, value, decimals=2):
        """Rounds the decrypted value to a specific decimal place."""
        return float(
            Decimal(value).quantize(
                Decimal(f"1.{'0'*decimals}"), rounding=ROUND_HALF_UP
            )
        )

    def forward(self, encrypted_input):
        outputs = []
        num_out = len(self.weights)

        for i in range(num_out):
            row = self.weights[i]
            acc = None
            for shift, weight in enumerate(row):
                rotated = self.ckks.eval_rotate(encrypted_input, shift)
                scaled = self.ckks.eval_mult(rotated, [weight] * self.slot_len)
                acc = scaled if acc is None else self.ckks.eval_add(acc, scaled)

            if self.bias:
                acc = self.ckks.eval_add(acc, [self.bias[i]] * self.slot_len)

            # Round the result before returning
            outputs.append([self.round_value(val) for val in self.ckks.decrypt(acc)])

        return outputs
