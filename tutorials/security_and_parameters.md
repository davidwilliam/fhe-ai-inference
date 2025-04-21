# Security and Parameter Selection in CKKS

Before building AI models on encrypted data, it's crucial to understand the trade-offs in Fully Homomorphic Encryption (FHE), especially when using the CKKS scheme. This tutorial walks you through the key parameters that affect security, performance, and precision in `fhe-ai-inference`.

## Why Parameters Matter

CKKS encryption allows approximate computation on encrypted floating-point vectors. However, its behavior is deeply affected by three core parameters:

- **Multiplicative Depth**: How many consecutive multiplications your circuit supports before noise overwhelms the result.
- **Scaling Modulus Size**: Controls how much precision is retained after each operation. Larger values give better precision but reduce depth.
- **Ring Dimension**: Affects security level and performance. Larger values improve security and noise tolerance but increase ciphertext size and computation time.

## Exploring Parameter Effects

Use the script [`scripts/inspect_context.py`](../scripts/inspect_context.py) to visualize how different parameters impact the crypto context:

### Example:

```bash
python scripts/inspect_context.py
```

### Output:

```
--- Context with Depth=2, ScaleMod=50, RingDim=default ---
Ring Dimension     : 16384
Scaling Modulus    : 50
Multiplicative Depth (configured): 2

--- Context with Depth=4, ScaleMod=55, RingDim=default ---
Ring Dimension     : 16384
Scaling Modulus    : 55
Multiplicative Depth (configured): 4

--- Context with Depth=4, ScaleMod=50, RingDim=32768 ---
Ring Dimension     : 32768
Scaling Modulus    : 50
Multiplicative Depth (configured): 4
```

## Interpreting the Results

- Increasing **depth** means you can support more complex computations (like deeper neural networks) but you'll need higher ring dimension or smaller scaling modulus to accommodate the noise growth.
- Increasing **scaling modulus size** improves precision, but increases noise per operation. Overly large values (>= 60) are rejected.
- Increasing **ring dimension** boosts noise tolerance and security (≥ 32768 is considered high security), but it also slows down encryption and increases ciphertext size.

## Choosing Secure Parameters

| Ring Dimension | Security Level (bits) | Use Case Example           |
|----------------|------------------------|-----------------------------|
| 16384          | ~128 bits              | General applications        |
| 32768          | ~192 bits              | High-security environments  |

**Note:** These mappings are approximate and based on standard LWE hardness assumptions.

## Best Practices

- Start small: use default parameters (`depth=2`, `scale=50`) to prototype.
- Gradually increase depth/ring size as your circuits become more complex.
- Test precision loss by encrypting, evaluating, and decrypting representative data.
- Avoid scaling modulus ≥ 60 (unsupported in OpenFHE).

## Next

Now that you understand security and parameter selection, you're ready to:

- [Explore Precision and Noise Budget](./precision_and_noise.md) *(coming soon)*
- [Build a Linear Model with Encrypted Data](./secure_linear_models.md) *(coming soon)*

Or go back to the [Tutorials Index](./index.md) to explore more topics.
