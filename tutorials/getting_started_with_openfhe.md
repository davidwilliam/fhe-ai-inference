# Getting Started with OpenFHE (CKKS)

In this tutorial, we'll use the `fhe-ai-inference` Python library to demonstrate the essentials of Fully Homomorphic Encryption (FHE) with the CKKS scheme from OpenFHE.

We'll cover:

- Initializing the FHE context
- Encrypting and decrypting data
- Performing basic homomorphic arithmetic (addition, multiplication)

## Prerequisites

Make sure you've installed the library:

```bash
pip install -e .
```

## 1. Initialize the FHE Context

Create a Python file named `fhe_basics.py`:

```python
from fhe_ai_inference.fheai import FHEAI
import numpy as np

# Initialize FHE context
fheai = FHEAI(mult_depth=2, scale_mod_size=50)
```

- `mult_depth`: Determines how many homomorphic multiplications you can do.
- `scale_mod_size`: Number of bits for scaling modulus, impacts precision.

## 2. Encrypt and Decrypt Data

Let's encrypt and decrypt a simple array:

```python
# Original data
data = np.array([1.5, 2.5, 3.5])

# Encrypt the data
encrypted_data = fheai.encrypt(data)

# Decrypt the data (specify length to match original data size)
decrypted_data = fheai.decrypt(encrypted_data, length=len(data))

print("Original:", data)
print("Decrypted:", decrypted_data)
```

Run it:

```bash
python fhe_basics.py
```

You’ll see output like this:

```text
Original: [1.5 2.5 3.5]
Decrypted: [1.5 2.5 3.5]
```

## 3. Homomorphic Addition

Homomorphic addition lets you add encrypted data without decrypting it:

```python
data1 = np.array([1, 2, 3])
data2 = np.array([4, 5, 6])

enc1 = fheai.encrypt(data1)
enc2 = fheai.encrypt(data2)

enc_sum = fheai.add(enc1, enc2)
dec_sum = fheai.decrypt(enc_sum, length=len(data1))

print("Sum:", dec_sum)
```

Output:

```
Sum: [5. 7. 9.]
```

## 4. Homomorphic Multiplication

Multiply encrypted data homomorphically:

```python
data1 = np.array([2, 3, 4])
data2 = np.array([5, 6, 7])

enc1 = fheai.encrypt(data1)
enc2 = fheai.encrypt(data2)

enc_product = fheai.multiply(enc1, enc2)
dec_product = fheai.decrypt(enc_product, length=len(data1))

print("Product:", dec_product)
```

Output (approximately):

```
Product: [10. 18. 28.]
```

**Note:** Multiplication introduces slight numeric errors, which are normal. Usually, results will be precise up to at least 3 decimal places.

---

## Next Steps

Congratulations, you’ve successfully performed basic encryption, decryption, and homomorphic arithmetic with OpenFHE and the `fhe-ai-inference` Python library.

Next, explore more advanced concepts:

- Implement secure linear models (coming soon)
- Explore real-world applications like privacy-preserving analytics
- Experiment with bootstrapping for deeper computations

Check regularly as we expand our tutorials.

[← Back to Tutorials Index](./index.md)
