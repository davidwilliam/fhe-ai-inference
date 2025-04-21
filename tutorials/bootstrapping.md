# Bootstrapping in CKKS

Bootstrapping is the process of refreshing a ciphertext in CKKS to reduce accumulated noise, effectively allowing further encrypted computations without sacrificing correctness.

This tutorial walks you through how bootstrapping works with the `fhe-ai-inference` library, built on top of OpenFHE, and how to use it in a Pythonic, elegant way.

## Why Bootstrapping Matters

CKKS supports approximate arithmetic over encrypted floating-point numbers. However, each operation increases the noise, and once the noise budget is exhausted, decryption fails.

**Bootstrapping resets the noise budget**, making it possible to:
- Run long computation chains
- Reuse encrypted data across modules
- Support iterative algorithms (e.g., encrypted training, control loops)

## Step-by-Step: How to Bootstrap with `fhe-ai-inference`

### 1. Build a Bootstrappable CryptoContext

Use `build_bootstrappable_context()` from `params_bootstrap`:

```python
from fhe_ai_inference.params_bootstrap import build_bootstrappable_context

context = build_bootstrappable_context()
```

This sets up a CKKS context with safe defaults:
- `RingDim = 4096`
- `MultiplicativeDepth = 18`
- `ScalingTechnique = FLEXIBLEAUTO`
- KeySwitching and AdvancedSHE enabled

### 2. Create a Class with Bootstrapping Support

We use a mixin to keep our API clean:

```python
from fhe_ai_inference.fheai import FHEAI
from fhe_ai_inference.fheai_bootstrap import BootstrapMixin

class BootstrappableFHE(FHEAI, BootstrapMixin):
    def __init__(self):
        super().__init__(crypto_context=build_bootstrappable_context())
```

### 3. Setup Bootstrapping

This initializes the necessary precomputations and bootstrapping keys:

```python
fhe = BootstrappableFHE()
fhe.setup_bootstrap(level_budget=[4, 4], num_slots=8)
```

### 4. Encrypt, Compute, and Bootstrap

```python
x = [0.25, 0.5, 0.75, 1.0, 2.0, 3.0, 4.0, 5.0]
ciphertext = fhe.encrypt(x)

# Do work that consumes noise...
for _ in range(4):
    ciphertext = fhe.multiply(ciphertext, ciphertext)

# Refresh the ciphertext
ciphertext = fhe.bootstrap(ciphertext)

# Decrypt
result = fhe.decrypt(ciphertext, length=len(x))
print(result)
```

## Notes on macOS / Compatibility

⚠️ Bootstrapping works reliably when run as a standalone script (e.g., `bootstrap_demo.py`) but currently **segfaults inside test runners** on some macOS setups.

- We provide a skipped test with a full explanation.
- This issue is upstream in OpenFHE’s Python bindings.

## Summary

✅ Bootstrapping is supported via a clean, mixin-based API.

✅ You can configure slots and level budgets.

✅ Practical demo in `scripts/bootstrap_demo.py`.

❌ Test is skipped by default due to binding instability (macOS-specific).

## What's Next?

- Use bootstrapping to build secure iterative workloads
- Control bootstrapping precision and chaining
- Profile noise and performance under realistic workloads

Or go back to the [Tutorials Index](./index.md) to explore more topics.
