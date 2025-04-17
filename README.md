# FHE-AI-Inference

**FHE-AI-Inference** is an upcoming open-source Python library for **secure neural network inference** using **Fully Homomorphic Encryption (FHE)** with [OpenFHE](https://github.com/openfheorg/openfhe-python)’s CKKS scheme. It aims to enable privacy-preserving AI for sensitive data in domains like healthcare (e.g., encrypted medical diagnostics) and finance (e.g., encrypted fraud detection) by encrypting both inputs and model weights. Designed for developers, it will offer a high-level API with seamless PyTorch integration, with plans for TensorFlow and ONNX support.

This project is in its **early planning phase**, and we’re excited to build a community around secure AI! Contributions are welcome to help shape its development.

## Project Vision

FHE-AI-Inference will allow developers to perform neural network inference on encrypted data without compromising privacy, leveraging OpenFHE’s advanced CKKS scheme for efficient, AI-friendly FHE. Key features planned include:
- **Secure Inference**: Encrypt inputs and model weights for end-to-end privacy.
- **Neural Network Focus**: Optimized for shallow neural networks (e.g 2–5 layers) with polynomial approximations for activations (e.g., ReLU).
- **Developer-Friendly**: High-level Python API to abstract FHE complexities.
- **Use Cases**: Privacy-preserving applications in healthcare, finance, and beyond.
- **Open-Source**: MIT-licensed, community-driven development.

## Current Status

The project is in the **initial setup phase**:
- Repository created with `.gitignore`.
- Planning the Python library structure and MVP (secure inference for a 2-layer PyTorch network).
- No code or releases yet—stay tuned for updates!

We’re actively working on the first milestone (see [Roadmap](#roadmap)) and welcome contributors to join us in building this exciting tool.

## Comparison with Other FHE Libraries

FHE-AI-Inference aims to fill a unique niche by combining OpenFHE’s CKKS scheme with a neural network-focused API. Here’s how it compares to existing FHE and privacy-preserving ML libraries:

| Library/Project | FHE Backend | AI Inference Support | Neural Network Focus | Python API Usability | AI Framework Integration | Uses OpenFHE | Primary Use Case | Community & Maturity |
|-----------------|-----------------|----------------------|----------------------|----------------------|--------------------------|-------------|------------------|----------------------|
| **FHE-AI-Inference** | OpenFHE (CKKS) | Planned | Strong (shallow neural networks) | High-level (planned) | PyTorch, TensorFlow/ONNX (planned) | Yes | Secure neural network inference | New; seeking contributors |
| [Concrete ML](https://github.com/zama-ai/concrete-ml) | Concrete (Zama) | Yes | Moderate (neural networks, other ML models) | High-level (scikit-learn-like) | PyTorch-inspired | No | Privacy-preserving ML | Mature, active, backed by Zama |
| [TenSEAL](https://github.com/OpenMined/TenSEAL) | Microsoft SEAL (CKKS, BFV) | Yes | Moderate (shallow neural networks) | Medium-level (tensor-based) | Partial (PyTorch/TensorFlow preprocessing) | No | Encrypted tensor operations | Active, good docs, some installation issues |
| [Pyfhel](https://github.com/ibarrond/Pyfhel) | SEAL, HElib, PALISADE | Limited | Weak (no neural network focus) | High-level | No | No | General-purpose FHE | Moderate, less AI-focused |
| [PySEAL](https://github.com/Lab41/pyseal) | Microsoft SEAL | Limited | Weak (no neural network focus) | Medium-level | No | No | General-purpose FHE | Small, limited docs |
| [OpenFHE Python Wrapper](https://github.com/openfheorg/openfhe-python) | OpenFHE (CKKS, BFV, BGV) | Limited (ML demos) | Weak (no neural network focus) | Medium-level | No | Yes | General-purpose FHE | Growing, DARPA-backed, early-stage Python wrapper |

**Why FHE-AI-Inference?**
- **OpenFHE-Powered**: Leverages OpenFHE’s advanced CKKS for AI-friendly FHE.
- **Neural Network Focus**: Tailored for secure inference with PyTorch integration.
- **Developer-Friendly**: Aims to simplify FHE with high-level APIs.
- **Unique Niche**: Complements broader tools like Concrete ML by focusing on OpenFHE and neural networks.

## Getting Started

The project is not yet installable as a package, but you can set up the development environment to contribute:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/<your-username>/fhe-ai-inference.git
   cd fhe-ai-inference