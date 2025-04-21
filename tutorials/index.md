# Tutorials Index

Welcome to the FHE AI Inference tutorials. Here you will find practical, well-structured guides that walk you through every key aspect of working with fully homomorphic encryption (FHE) using OpenFHE and the `fhe-ai-inference` Python project.

## Available Tutorials

- [Getting Started with OpenFHE (CKKS)](./getting_started_with_openfhe.md)
  Learn how to set up OpenFHE, create encryption keys, encrypt/decrypt data, and apply basic homomorphic operations like addition and multiplication using the CKKS scheme.

- [Security and Parameter Selection in CKKS](./security_and_parameters.md)
  Understand the core parameters of CKKS (depth, scale, ring dimension), how they affect security, precision, and performance, and how to select the right configuration for your workload.

- [Precision and Noise Budget in CKKS](./precision_and_noise.md)
  Explore how noise accumulates during computation, how to measure drift, and how to balance precision and circuit depth when building encrypted workloads.

- [Bootstrapping in CKKS](./bootstrapping.md)
  Learn how to refresh noisy ciphertexts to extend computation lifetimes using a clean, Pythonic API built on OpenFHE.

## Coming Soon

- Secure Linear Models with FHE
- Bootstrapping in Practice
- Real-World Use Cases: Privacy-Preserving Analytics
- FHE-Powered Neural Network Layers
- Debugging and Benchmarking Homomorphic Workflows

Each tutorial focuses on a specific learning outcome and builds incrementally toward advanced use cases.

Start with the [Getting Started guide](./getting_started_with_openfhe.md) if you're new, or check back regularly as we expand the library.
