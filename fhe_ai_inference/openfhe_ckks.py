from decimal import Decimal, ROUND_HALF_UP


class CKKSOperations:
    def __init__(
        self, poly_modulus_degree=16384, scaling_modulus_size=50, depth=3, slots=3
    ):
        """
        CKKSOperations provides a simplified interface to OpenFHE's CKKS scheme.

        Args:
            poly_modulus_degree (int): Ring dimension (e.g. 16384).
            scaling_modulus_size (int): Scaling modulus bit size (e.g. 45–60).
            depth (int): Multiplicative depth.
            slots (int): Number of active input slots (e.g. length of input vectors).
        """
        from openfhe import (
            CCParamsCKKSRNS,
            SecurityLevel,
            PKESchemeFeature,
            GenCryptoContext,
        )

        self.active_slots = slots  # ✅ Track number of real input slots

        params = CCParamsCKKSRNS()
        params.SetMultiplicativeDepth(depth)
        params.SetScalingModSize(scaling_modulus_size)
        params.SetRingDim(poly_modulus_degree)
        params.SetSecurityLevel(SecurityLevel.HEStd_128_classic)

        self.context = GenCryptoContext(params)
        self.context.Enable(PKESchemeFeature.PKE)
        self.context.Enable(PKESchemeFeature.LEVELEDSHE)
        self.context.Enable(PKESchemeFeature.ADVANCEDSHE)

        self.keypair = self.context.KeyGen()
        self.context.EvalMultKeyGen(self.keypair.secretKey)
        self.context.EvalSumKeyGen(self.keypair.secretKey)
        self._generate_rotation_keys(slots)

    def _generate_rotation_keys(self, slots):
        indexes = [0] + list(range(1, slots)) + list(range(-1, -slots, -1))
        self.context.EvalAtIndexKeyGen(self.keypair.secretKey, indexes)

    def encode(self, values):
        return self.context.MakeCKKSPackedPlaintext(values)

    def encrypt(self, values):
        pt = self.encode(values)
        return self.context.Encrypt(self.keypair.publicKey, pt)

    def decrypt(self, ciphertext, decimals=2, trim=True):
        """
        Decrypts and returns the list of values (optionally trimmed and rounded).

        Args:
            ciphertext: Ciphertext to decrypt.
            decimals (int): Decimal precision to round to.
            trim (bool): If True, only return active input slots.
        """
        pt = self.context.Decrypt(self.keypair.secretKey, ciphertext)
        values = pt.GetCKKSPackedValue()

        if trim:
            values = values[: self.active_slots]

        return [
            float(
                Decimal(c.real).quantize(
                    Decimal(f"1.{'0'*decimals}"), rounding=ROUND_HALF_UP
                )
            )
            for c in values
        ]

    def eval_add(self, ctxt_or_plain, pt_or_ctxt):
        if isinstance(pt_or_ctxt, list):
            pt = self.encode(pt_or_ctxt)
            return self.context.EvalAdd(ctxt_or_plain, pt)
        return self.context.EvalAdd(ctxt_or_plain, pt_or_ctxt)

    def eval_mult(self, ctxt_or_plain, pt_or_ctxt):
        if isinstance(pt_or_ctxt, list):
            pt = self.encode(pt_or_ctxt)
            return self.context.EvalMult(ctxt_or_plain, pt)
        return self.context.EvalMult(ctxt_or_plain, pt_or_ctxt)

    def eval_rotate(self, ciphertext, steps):
        return self.context.EvalRotate(ciphertext, steps)

    def eval_sum(self, ciphertext):
        """
        Manually sums only the active slots by controlled rotations.
        Prevents overflow into unused parts of the ciphertext.
        """
        acc = ciphertext
        for i in range(1, self.active_slots):
            rotated = self.eval_rotate(ciphertext, i)
            acc = self.context.EvalAdd(acc, rotated)
        return acc
