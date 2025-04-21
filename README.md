# FHE-AI-Inference

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

Just one command sets up your entire environment (macOS/Linux):

```bash
make install
```

This command automatically installs all prerequisites, compiles OpenFHE, configures Python bindings, and sets up your Python virtual environment.

If for some reason you need to run the install command again, just do:

```bash
make clean
make install
```

After installing, to test everything is working as intended, run:

```
python scripts/test_openfhe_init.py
```

You should see the following result:

```
✅ OpenFHE context successfully initialized with CKKS.
```

### Run Your First Example

After setup, run your first encrypted neural inference example:

```bash
python tutorials/getting_started_with_openfhe.py
```

You should see a successful encryption, decryption, and homomorphic operations demonstration.

## Tutorials & Documentation

- [Tutorials Index](tutorials/index.md): Practical guides covering key aspects of OpenFHE usage.
- [Getting Started with OpenFHE (CKKS)](tutorials/getting_started_with_openfhe.md): Detailed introduction covering encryption, decryption, and homomorphic operations.

### Bootstrapping Support

Bootstrapping resets a ciphertext's noise budget, allowing deeper encrypted computations. With `fhe-ai-inference`, bootstrapping is supported through a clean `BootstrapMixin`:

```python
fhe = BootstrappableFHE()
fhe.setup_bootstrap(level_budget=[4, 4], num_slots=8)
cipher = fhe.encrypt([...])
cipher = fhe.bootstrap(cipher)
result = fhe.decrypt(cipher)
```

See [scripts/bootstrap_demo.py](scripts/bootstrap_demo.py)  for a working example.

> ⚠️ Known Issue: Bootstrapping segfaults under test runners on macOS due to OpenFHE Python bindings. Tests are skipped by default.

Generate and view documentation easily:

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

## Comparison with Other FHE Libraries

| Library | FHE Backend | AI Inference | Pythonic API | NN Focus | OpenFHE |
|---------|-------------|--------------|--------------|----------|---------|
| **FHE-AI-Inference** | OpenFHE (CKKS) | ✅ Planned | ✅ High | ✅ Strong | ✅ Yes |
| Concrete ML | Concrete (Zama) | ✅ Yes | ✅ High | ✅ Moderate | ❌ No |
| TenSEAL | SEAL | ✅ Yes | ✅ Medium | ✅ Moderate | ❌ No |
| Pyfhel | Multiple | ❌ Limited | ✅ High | ❌ Weak | ❌ No |

## Maintainer

[David William Silva](https://github.com/davidwilliam)
📧 [contact@davidwsilva.com](mailto:contact@davidwsilva.com)

Feel free to reach out with questions, ideas, or to collaborate!
