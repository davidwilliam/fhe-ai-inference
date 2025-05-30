# FHE-AI-Inference

![Python Version](https://img.shields.io/badge/python-3.13-blue.svg) ![License](https://img.shields.io/github/license/davidwilliam/fhe-ai-inference) ![Code Style: Ruff](https://img.shields.io/badge/style-ruff-orange) ![FHE](https://img.shields.io/badge/FHE-OpenFHE-blueviolet) ![Hatch](https://img.shields.io/badge/built_with-hatch-ff69b4)

**FHE-AI-Inference** is a Python library enabling **secure neural network inference** with **Fully Homomorphic Encryption (FHE)** using the [OpenFHE](https://github.com/openfheorg/openfhe-python) CKKS scheme. It allows privacy-preserving AI applications for sensitive data scenarios, such as encrypted medical diagnostics (healthcare) and encrypted fraud detection (finance).

## Why FHE-AI-Inference?

- **Easy Setup:** Fully automated environment setup with a powerful Makefile.
- **Truly Pythonic API:** Clean, intuitive, and fully tested Python interfaces.
- **Comprehensive Docs & Tutorials:** Clear, practical documentation and tutorials.
- **Developer-Friendly:** Quickly integrate secure inference into your AI workflow.

## Key Features

- **Secure Inference:** Encrypt data and perform neural network inference securely.
- **Neural Network Optimized:** Ideal for shallow neural networks (2-5 layers).
- **Fully Tested:** 100% test coverage ensuring reliability and robustness.
- **Open-Source:** MIT-licensed and welcoming contributions.

## Current Status

- Pythonic and tested API ready.
- Automated setup environment using Makefile.
- Initial documentation and beginner-friendly tutorials available.
- Planning further integration with PyTorch, TensorFlow, and ONNX.

Check the [Roadmap](ROADMAP.md) for upcoming milestones.

## Quick Start

### Setup Your Environment

One command to install everything (macOS / Linux):

```bash
make install
```

After the installation runs, you should see:

```
✅ OpenFHE context successfully initialized with CKKS.
```

This process installs Homebrew dependencies, builds & installs the OpenFHE C++ core, installs the Python bindings from source, and appends the proper `DYLD_LIBRARY_PATH` export into your `~/.zshrc`.

**Reload your shell** so the new library path is picked up:

```bash
source ~/.zshrc
```

To rebuild from scratch:

```bash
make clean
make install
```

#### Verify your setup

**Quick smoke test:**

```bash
python scripts/test_openfhe_init.py
```

You should see:

```
✅ OpenFHE context successfully initialized with CKKS.
```

**Full test suite & coverage** (via Hatch):

```bash
make test
```

### Run Your First Example

After setup, run your first encrypted neural inference example:

```bash
python tutorials/getting_started_with_openfhe.py
```

You should see a successful encryption, decryption, and homomorphic operations demonstration.

### A Truly Pythonic API for FHE

Instead of binding developers to verbose C++ cryptographic idioms, this library offers a **natural, Pythonic interface** to FHE operations.

All homomorphic encryption, decryption, and evaluation logic is cleanly exposed:

```python
from fhe_ai_inference.fheai import FHEAI

# Step 1: Create a homomorphic context
fhe = FHEAI(mult_depth=3, scale_mod_size=50)

# Step 2: Encrypt data
enc_x = fhe.encrypt([1.0, 2.0, 3.0])
enc_y = fhe.encrypt([4.0, 5.0, 6.0])

# Step 3: Compute homomorphically
enc_sum = fhe.add(enc_x, enc_y)
enc_prod = fhe.multiply(enc_x, enc_y)

# Step 4: Decrypt result
print(fhe.decrypt(enc_sum))    # [5.0, 7.0, 9.0]
print(fhe.decrypt(enc_prod))   # [4.0, 10.0, 18.0]
```

#### Bootstrapping Support

Bootstrapping refreshes a ciphertext’s noise budget, enabling deeper encrypted computations.

With `fhe-ai-inference`, enabling bootstrapping is seamless:

```python
from fhe_ai_inference.fheai import FHEAI

# Initialize with bootstrapping support
fhe = FHEAI(bootstrappable=True)

# Encrypt data at a high level
enc = fhe.encrypt([3.14], level=10)

# Refresh the ciphertext
refreshed = fhe.bootstrap(enc)

# Decrypt and verify accuracy
print(fhe.decrypt(refreshed))  # [3.14...] — ciphertext refreshed
```

All features work out of the box via `make install`.

## Tutorials & Documentation

- [Tutorials Index](tutorials/index.md): Practical guides covering key aspects of OpenFHE usage.
- [Getting Started with OpenFHE (CKKS)](tutorials/getting_started_with_openfhe.md): Detailed introduction covering encryption, decryption, and homomorphic operations.

> **Adaptive Logic**: Bootstrapping is applied only when needed (i.e., if the ciphertext’s level exceeds the bootstrapping threshold). This ensures optimal performance during deep computations.

See [`scripts/bootstrap_demo.py`](scripts/bootstrap_demo.py) for a working example that computes `x^16` homomorphically.

### Generate and view documentation

```bash
python3 -m http.server --directory docs
```

Then open your browser to [http://localhost:8000](http://localhost:8000).

## Linting and Code Quality

The project uses [Ruff](https://docs.astral.sh/ruff/) for linting and ensuring clean code:

```bash
ruff check . --fix
```

You can also run

```bash
hatch run dev
```

which will check lint, run tests, and update documents.

## Pre-Commit Hooks

Automatically format and lint your commits with Black and Ruff:

```bash
pre-commit install
```

## Project Vision & Roadmap

FHE-AI-Inference is evolving rapidly:

- **Phase 1 (Complete):** Environment automation, initial Pythonic API, testing.
- **Phase 2:** Integration with popular ML frameworks (PyTorch).
- **Phase 3:** Advanced features such as bootstrapping and secure deep neural networks.

Contributions are warmly welcomed! Check out [CONTRIBUTING.md](CONTRIBUTING.md).

## Maintainer

[David William Silva](https://github.com/davidwilliam)
📧 [contact@davidwsilva.com](mailto:contact@davidwsilva.com)

Feel free to reach out with questions, ideas, or to collaborate!
