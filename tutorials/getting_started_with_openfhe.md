# Getting Started with OpenFHE: A Complete Tutorial

This tutorial provides a comprehensive introduction to fully homomorphic encryption (FHE) using the CKKS scheme with OpenFHE’s Python bindings. It is designed to help new users understand the core building blocks of FHE and get hands-on experience with encryption, computation, and decryption on encrypted data.

This tutorial uses the `fhe-ai-inference` library, which wraps and simplifies key OpenFHE features for practical use.

## Prerequisites

Before you begin, ensure that the following requirements are met:

- Python 3.10 or higher
- This repository is cloned and dependencies are installed

Installation steps:

```bash
git clone https://github.com/your-repo/fhe-ai-inference.git
cd fhe-ai-inference
hatch shell  # or `pip install -e .`
```

## Introduction to the CKKS Scheme

CKKS is an approximate homomorphic encryption scheme. It allows arithmetic operations on encrypted real-valued vectors, with small precision loss that is tolerable in most analytics and machine learning tasks. CKKS encodes data in a complex domain and supports operations like addition, multiplication, and rotation.

## Step 1: Setup CKKS Context and Key Generation

```python
from fhe_ai_inference.openfhe_ckks import CKKSOperations

original = [1.0, 2.0, 3.0]
ckks = CKKSOperations(
    poly_modulus_degree=16384,
    scaling_modulus_size=50,
    slots=len(original)
)
```

This sets up the encryption parameters and generates the necessary public/secret keys along with rotation keys for vector operations.

## Step 2: Encrypting a Vector

```python
ctxt = ckks.encrypt(original)
```

This converts the input vector to a plaintext object and encrypts it using the public key. The encrypted ciphertext can now be safely used in untrusted environments.

## Step 3: Homomorphic Addition

```python
add_values = [10.0] * len(original)
ctxt_add = ckks.eval_add(ctxt, add_values)
decrypted_add = ckks.decrypt(ctxt_add)
```

The `eval_add` function adds a plaintext vector to the ciphertext in encrypted space. Decryption yields values close to the expected result.

## Step 4: Homomorphic Multiplication

```python
mult_values = [2.0, 3.0, 4.0]
ctxt_mult = ckks.eval_mult(ctxt, mult_values)
decrypted_mult = ckks.decrypt(ctxt_mult)
```

This multiplies the ciphertext vector element-wise with a plaintext vector and returns an encrypted result.

## Step 5: Slot Rotations

```python
ctxt_rot_left = ckks.eval_rotate(ctxt, 1)
ctxt_rot_right = ckks.eval_rotate(ctxt, -1)

decrypted_rot_left = ckks.decrypt(ctxt_rot_left)
decrypted_rot_right = ckks.decrypt(ctxt_rot_right)
```

CKKS supports rotating vector elements left or right using `EvalRotate`. This is often used in summation and matrix-style operations.

## Step 6: Encrypted Slot Summation

```python
ctxt_sum = ckks.eval_sum(ctxt)
decrypted_sum = ckks.decrypt(ctxt_sum)
```

Instead of summing the entire ciphertext space (which may include many padded zeros), we manually sum only the active slots using controlled rotations and additions. This produces accurate results for smaller input vectors.

## Step 7: Interpreting the Results

Decryption in CKKS returns complex numbers, even if real values were originally encrypted. We extract and round the real part to a target number of decimal places (default is 2). 

You may observe slight differences due to the approximate nature of CKKS. These are expected and generally acceptable for applications in data science, analytics, and inference.

Example output:

```
Original:                [1.0, 2.0, 3.0]
Expected (add):          [11.0, 12.0, 13.0]
Decrypted (add):         [11.0, 12.0, 13.0]
Expected (mult):         [2.0, 6.0, 12.0]
Decrypted (mult):        [2.0, 6.0, 12.0]
Decrypted (rotate +1):   [2.0, 3.0, 0.0]
Decrypted (rotate -1):   [0.0, 1.0, 2.0]
Expected (sum):          [6.0, 6.0, 6.0]
Decrypted (sum):         [6.0, 6.0, 6.0]
```

## Summary

This tutorial covered:

- Creating a CKKS encryption context using OpenFHE
- Encrypting and decrypting vectors
- Performing homomorphic addition and multiplication
- Rotating encrypted vectors
- Implementing encrypted summation using manual EvalRotate and EvalAdd

The full working example can be found in [`getting_started_with_openfhe.py`](./getting_started_with_openfhe.py).

For any further questions, consult the official [OpenFHE documentation](https://openfhe-development.readthedocs.io/en/latest/) or continue exploring this repository.