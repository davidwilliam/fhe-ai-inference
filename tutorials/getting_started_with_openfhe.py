"""
Getting Started with OpenFHE (Python) — CKKS Tutorial

This tutorial walks through core operations using OpenFHE's CKKS scheme:
- Context and key generation
- Encryption and encoding
- Homomorphic addition and multiplication
- Rotations (left/right)
- Slot-wise summation (via EvalRotate + EvalAdd)
- Decryption and decoding

⚠️ Note:
CKKS is an *approximate* encryption scheme. Repeated operations (especially EvalSum
via rotations) can introduce minor inaccuracies in some slots.

To mitigate this, we decrypt the result and use the first slot — which is typically the
most accurate — to derive exact summaries like total sums.
"""

from fhe_ai_inference.openfhe_ckks import CKKSOperations

# Step 1: Setup CKKS context and keys
original = [1.0, 2.0, 3.0]
ckks = CKKSOperations(
    poly_modulus_degree=16384, scaling_modulus_size=50, slots=len(original)
)

# Encrypt input
ctxt = ckks.encrypt(original)

# Step 2: Homomorphic addition
add_values = [10.0] * len(original)
ctxt_add = ckks.eval_add(ctxt, add_values)

# Step 3: Homomorphic multiplication
mult_values = [2.0, 3.0, 4.0]
ctxt_mult = ckks.eval_mult(ctxt, mult_values)

# Step 4: Rotations
ctxt_rot_left = ckks.eval_rotate(ctxt, 1)
ctxt_rot_right = ckks.eval_rotate(ctxt, -1)

# Step 5: Slot-wise summation (manual via EvalRotate)
ctxt_sum = ckks.eval_sum(ctxt)

"""
Why are decrypted values returned as complex numbers?

CKKS uses approximate arithmetic over complex vectors.
Even if your inputs are real numbers,
the decrypted results will be complex —
often with a tiny imaginary component due to noise.

For example:
    (6.0 + 1.2e-15j)

In this tutorial, we discard the imaginary part and round the real part to two decimals:
    round(c.real, 2)

This behavior is handled automatically in `ckks.decrypt(...)`.
"""

# Step 6: Decryption
decrypted_original = ckks.decrypt(ctxt)
decrypted_add = ckks.decrypt(ctxt_add)
decrypted_mult = ckks.decrypt(ctxt_mult)
decrypted_rot_left = ckks.decrypt(ctxt_rot_left)
decrypted_rot_right = ckks.decrypt(ctxt_rot_right)
decrypted_sum = ckks.decrypt(ctxt_sum)

# Step 7: Compare results
print("Original:                ", original)

print("Expected (add):          ", [x + 10.0 for x in original])
print("Decrypted (add):         ", decrypted_add)

print("Expected (mult):         ", [x * y for x, y in zip(original, mult_values)])
print("Decrypted (mult):        ", decrypted_mult)

print("Decrypted (rotate +1):   ", decrypted_rot_left)
print("Decrypted (rotate -1):   ", decrypted_rot_right)

# EvalSum result: first slot is most accurate
first_slot_sum = decrypted_sum[0]
replicated_sum = [first_slot_sum] * len(original)

# Manual reference for validation
expected_sum = [sum(decrypted_original)] * len(original)

print("Expected (sum):          ", expected_sum)
print("Decrypted (sum):         ", replicated_sum)
