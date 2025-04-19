import torch


class FHELinear:
    def __init__(self, weight: torch.Tensor, bias: torch.Tensor, context):
        self.weight = [context.MakeCKKSPackedPlaintext(row.tolist()) for row in weight]
        self.bias = [
            context.MakeCKKSPackedPlaintext([b.item()] * weight.shape[1]) for b in bias
        ]
        self.context = context

    def __call__(self, ciphertext_input):
        outputs = []
        for w_ptxt, b_ptxt in zip(self.weight, self.bias):
            # Element-wise multiplication
            ctxt_prod = self.context.EvalMult(ciphertext_input, w_ptxt)

            # Sum all slots to simulate dot product
            ctxt_sum = self.context.EvalSum(ctxt_prod, len(w_ptxt.GetCKKSPackedValue()))

            # Add bias
            ctxt_out = self.context.EvalAdd(ctxt_sum, b_ptxt)

            outputs.append(ctxt_out)
        return outputs
