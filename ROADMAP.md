# FHE-AI-Inference Roadmap

This roadmap outlines the milestones for building a clean, testable, Pythonic library for secure AI inference using **Fully Homomorphic Encryption (FHE)** via **OpenFHE's CKKS scheme**.

Our approach emphasizes **modularity**, **developer experience**, and **practical security**, aiming to bring homomorphic AI workflows into real-world use with clarity and simplicity.

## Phase 0: Core Setup & Refactor

> 🔍 Focus: Make it easy to install, use, test, and extend the library.

- [x] Makefile-based full setup (OpenFHE C++ core + Python bindings)
- [x] Create Pythonic `FHEAI` class with high-level methods
- [x] Modularize: split core API, params, bootstrapping, etc.
- [x] Implement homomorphic operations: `encrypt`, `decrypt`, `add`, `multiply`
- [x] Build reproducible test suite with 100% coverage
- [x] Enable auto-generated documentation with `pdoc`
- [x] Write tutorials for getting started, parameter tuning, and precision drift
- [x] Clean style with `ruff` + pre-commit hooks
- [x] Bootstrap setup script (runs with OpenFHE, includes keygen + eval)

## Phase 1: Encrypted Neural Ops (Linear Models)

> 🔍 Focus: Enable core encrypted model operations like linear layers and forward passes.

- [ ] Implement `FHELinear` module (analog to `torch.nn.Linear`)
- [ ] Support encrypted matrix-vector multiplication
- [ ] Encode and apply biases under encryption
- [ ] Create `FHEModelRunner` for running encrypted forward passes
- [ ] Provide an example: encrypted 2-layer network with toy weights

## Phase 2: Serialization & Secure Model Sharing

> 🔍 Focus: Allow encrypted weights and model configs to be saved and reused.

- [ ] Define serialization format for encrypted weights and model structure
- [ ] Support PyTorch-style conversion to CKKS plaintexts
- [ ] Enable saving/loading CKKS-encrypted model checkpoints (JSON or binary)
- [ ] CLI or API for loading and serving encrypted models

## Phase 3: Activation Approximation

> 🔍 Focus: Homomorphic support for non-linear layers using safe approximations.

- [ ] Implement polynomial approximations: `square`, `relu`, `gelu`
- [ ] Create `FHEActivation` module (drop-in for model graph)
- [ ] Benchmark approximation accuracy vs computational cost
- [ ] Plug into `FHEModelRunner` for encrypted inference

## Phase 4: Secure Inference on Real Data

> 🔍 Focus: Build end-to-end inference pipelines using encrypted inputs and models.

- [ ] Add support for batch inference (slot-packing)
- [ ] Implement encrypted inference over tabular datasets (e.g., fraud detection, health scoring)
- [ ] Write real-world examples and tutorials
- [ ] Add utilities for data preprocessing and encrypted input handling

## Phase 5: Bootstrapping & Runtime Improvements

> 🔍 Focus: Keep ciphertexts fresh and inference stable in deeper networks.

- [x] Expose `bootstrap()` and `setup_bootstrap()` in a clean API
- [x] Add `params_bootstrap.py` with a working config for OpenFHE
- [x] Provide working bootstrapping demo script
- [ ] Refactor `BootstrapMixin` to support iterative bootstrapping
- [ ] Enable automatic bootstrapping within long inference chains
- [ ] Profile and optimize depth, scale, and rotation cost

## Phase 6: Documentation, Tutorials & Distribution

> 🔍 Focus: Make it easy to learn, adopt, and extend the project.

- [x] Create tutorial index and foundational guides (`getting_started`, `precision_drift`, `parameter_selection`)
- [x] Add bootstrapping tutorial (in progress)
- [ ] Write guide: “How to Build an FHE Model”
- [ ] Publish interactive notebooks on Colab / Jupyter
- [ ] Push to PyPI for easier adoption and feedback
- [ ] Prepare launch with landing page and announcement blog

## Stretch Goals (Post-MVP)

- [ ] Support for batching with multiple encrypted vectors (slot management)
- [ ] Add minimal `onnx` converter to CKKS encodings
- [ ] Explore SIMD-style FHE optimizations
- [ ] Integration with `PySyft` or other secure computation libraries
- [ ] Web-based demo: upload encrypted input → run FHE inference → get secure output

## Maintained by

[David William Silva](https://github.com/davidwilliam)
Built as a contribution for the future of **privacy-preserving AI**.
