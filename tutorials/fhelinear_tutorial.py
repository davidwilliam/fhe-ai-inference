from fhe_ai_inference.openfhe_ckks import CKKSOperations
from fhe_ai_inference.layers import FHELinear
from decimal import Decimal, ROUND_HALF_UP


# Step 1: Setup CKKS context and keys
original = [1.0, 2.0]  # Example input vector
ckks = CKKSOperations(
    poly_modulus_degree=16384, scaling_modulus_size=50, slots=len(original)
)

# Encrypt the input data
ctxt_x = ckks.encrypt(original)

# Step 2: Define the FHELinear layer (weights and bias)
w = [[0.5, 1.0], [-1.0, 0.0]]  # Example 2x2 weight matrix
b = [0.0, 1.0]  # Example bias vector

# Initialize the FHELinear layer
fhe_linear = FHELinear(w, b, ckks)

# Step 3: Apply the FHELinear layer to the encrypted input
outputs = fhe_linear(ctxt_x)


# Step 4: Process the decrypted outputs (already decrypted by FHELinear)
# Take the first slot of each output and round to 2 decimal places
def round_value(value, decimals=2):
    """Rounds the decrypted value to a specific decimal place."""
    return float(
        Decimal(value).quantize(Decimal(f"1.{'0'*decimals}"), rounding=ROUND_HALF_UP)
    )


decrypted_outputs = [
    round_value(output[0]) for output in outputs
]  # Take first slot of each output
print("Decrypted outputs:", decrypted_outputs)

# Step 5: Compare with expected results
expected = [
    (sum([w[0][i] * original[i] for i in range(len(original))])) + b[0],
    (sum([w[1][i] * original[i] for i in range(len(original))])) + b[1],
]
print("Expected:", expected)
print("Decrypted:", decrypted_outputs)

# Step 6: Validation (Allowing for small tolerance due to encryption
# and homomorphic operations)
tolerance = 0.1  # Adjust tolerance as needed
for exp, dec in zip(expected, decrypted_outputs):
    assert abs(exp - dec) <= tolerance, f"Expected {exp}, but got {dec}."
