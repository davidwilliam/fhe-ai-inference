# FHE-AI-Inference Roadmap

This document outlines the key development milestones for building a fully homomorphic encryption (FHE)-powered neural network inference library using OpenFHE and CKKS.

## Phase 0: Foundation
- [x] Build & install OpenFHE C++ core
- [x] Set up local OpenFHE Python bindings
- [x] Configure dynamic linking (macOS and Unix)
- [x] Create CKKS operations class (add, multiply, rotate, eval_sum)
- [x] Write and pass end-to-end tests for encrypted vector ops
- [x] Set up CI-style `hatch run dev` command
- [x] Generate auto-docs using `pdoc`
- [x] Finalize developer setup instructions in README

## Phase 1: AI Core Infrastructure

> Focus: Enable basic homomorphic linear inference using encrypted inputs and model weights.

- [ ] Design a `FHELinear` module (like PyTorch `nn.Linear`, but encrypted)
- [ ] Support encrypted matrix-vector multiplication using CKKS
- [ ] Approximate bias addition under encryption
- [ ] Build helper class `FHEInference` to manage encrypted forward passes
- [ ] Write example: Encrypted inference for a 2-layer network with toy weights

## 🔜 Phase 2: Secure Model Tools & Format

> Focus: Allow encrypted model weights to be saved, loaded, and reused.

- [ ] Define encrypted model serialization format
- [ ] Add support for PyTorch `state_dict`–to–CKKS encoder
- [ ] Add JSON or binary checkpointing for encrypted layers

## Phase 3: Activation Approximation

> Focus: Enable non-linear activations using polynomial approximations.

- [ ] Implement square and ReLU approximation (e.g., degree-2, degree-4)
- [ ] Allow `FHEActivation` modules to be inserted in inference pipeline
- [ ] Benchmark polynomial accuracy vs standard ReLU
---

## Phase 4: Secure Inference Workflow

> Focus: Run encrypted inference on real datasets (MNIST, tabular, etc.)

- [ ] Build `FHEModelRunner` with preprocessing, encryption, inference, decryption
- [ ] Implement secure evaluation on encrypted input batches
- [ ] Create examples: fraud detection, health scoring, etc.

## Phase 5: Optimizations & Bootstrapping

> Focus: Improve scalability, accuracy, and ciphertext freshness.

- [ ] Add support for bootstrapping (if exposed in Python bindings)
- [ ] Profile and reduce multiplicative depth for common networks
- [ ] Add automatic slot packing/replication strategies

## Phase 6: Docs, Demos, and Pip Package

- [ ] Full documentation for all modules
- [ ] Interactive notebook demos
- [ ] Publish to PyPI for broader adoption