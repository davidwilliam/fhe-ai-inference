# Precision and Noise Budget in CKKS

When using the CKKS scheme, all computations are approximate. That means **precision** becomes a key concern especially when chaining multiple operations together. This tutorial helps you understand how homomorphic operations introduce noise, and how that noise affects your final decrypted result.

## What You'll Learn

- How noise accumulates in CKKS over repeated operations
- How to measure error (drift) after each operation
- How parameter choices like multiplicative depth and scale affect precision

## Noise Accumulation via Multiplication

We'll start by repeatedly squaring a plaintext value (e.g. \( \pi \approx 3.14 \)) and observe the **error drift** over time.

### Run the Diagnostic

Run the script:

```bash
python scripts/precision_drift.py
```

Expected output:

```
Initial Value: 3.14159

Drift over repeated multiplications:
Step  | Decrypted Value      | Absolute Error
-------------------------------------------------------
1     | 9.8695877281         | 0.0000000000
2     | 31.0061981106        | 0.0000000002
3     | 97.4087619222        | 0.0000000005
4     | 306.0183923669       | 0.0000000017
5     | DECRYPTION FAILED    | ---

[Expected result]: ❌ Decryption failed at step 5: The decryption failed because the approximation error is too high.
```

### What Happened?

Each multiplication introduces **multiplicative noise**. Eventually, the noise overwhelms the signal, and decryption becomes unreliable, resulting in a runtime error. The script now **gracefully detects and reports** this.

## What Affects Precision?

- **Scaling Modulus**: Larger values retain more precision after each operation but increase noise too.
- **Multiplicative Depth**: Higher depth supports more operations but narrows safe parameter ranges.
- **Number of Chained Ops**: Each multiplication adds noise and degrades the signal.

## Best Practices

- Use the **minimum number of operations** needed for your computation.
- Test representative values and measure their drift before deploying real models.
- Consider bootstrapping (future tutorial) if you need deeper circuits without losing precision.
- Catch and report `Decrypt` errors when chaining many operations.

## Next

Now that you’ve explored noise and precision, you’re ready to:

- [Learn about Bootstrapping (coming soon)](./bootstrapping.md)
- [Design and test a secure linear model](./secure_linear_models.md)

Or go back to the [Tutorials Index](./index.md).
