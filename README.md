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

The project is not yet installable as a package, but you can set up the development environment to contribute. 

**Clone the Repository**:
   ```bash
   git clone https://github.com/<your-username>/fhe-ai-inference.git
   cd fhe-ai-inference
   ```

## Installation & Configuration

*Tested on macOS (MacBook Pro M3); similar steps apply to most Linux/Unix systems.*

### 1. Prerequisites

- **Homebrew** (macOS):  
  ```bash
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  ```
- **Command‐line tools**:  
  ```bash
  brew install cmake libomp pybind11
  ```
- **Python 3.13+**  
- **Git**

### 2. Clone & Build the OpenFHE C++ Core

```bash
cd ~/workspace_cpp

# 2.1 Clone the OpenFHE repo
git clone https://github.com/openfheorg/openfhe-development.git openfhe
cd openfhe

# 2.2 Create build directory & configure
mkdir build && cd build
cmake .. \
  -DCMAKE_BUILD_TYPE=Release \
  -DBUILD_SHARED=ON \
  -DBUILD_UNITTESTS=OFF \
  -DBUILD_EXAMPLES=OFF \
  -DBUILD_BENCHMARKS=OFF \
  -DCMAKE_INSTALL_PREFIX=/usr/local

# 2.3 Compile & install
make -j$(sysctl -n hw.ncpu)
sudo make install
```

> **What this does:**  
> - Installs shared libs (e.g. `/usr/local/lib/libOPENFHEpke.1.dylib`)  
> - Skips unit tests, examples, and benchmarks to avoid C++ `<regex>` issues

### 3. Prepare Your FHE‑AI‑Inference Environment

```bash
cd /path/to/fhe-ai-inference

# 3.1 Create & activate a Python venv
python3 -m venv venv
source venv/bin/activate

# 3.2 Upgrade pip & install test tools
pip install --upgrade pip
pip install pytest
```

### 4. Install the Python Bindings

```bash
# 4.1 Install the OpenFHE‑Python wrapper in editable mode
pip install -e ~/workspace_cpp/openfhe-python
```

### 5. Verify Dynamic Linking

macOS’s dynamic loader must find the OpenFHE `.dylib` in `/usr/local/lib`. Either:

- **Temporary (shell) fix**  
  ```bash
  export DYLD_LIBRARY_PATH="/usr/local/lib:${DYLD_LIBRARY_PATH:-}"
  ```
- **Permanent (bake into the .so)**  
  ```bash
  SOFILE=$(python - <<EOF
  import openfhe, os
  print(os.path.join(os.path.dirname(openfhe.__file__), "openfhe.so"))
  EOF
  )
  install_name_tool -add_rpath /usr/local/lib "$SOFILE"
  ```

### 6. Run the Tests

```bash
cd /path/to/fhe-ai-inference
pytest tests/
```

You should see all tests passing. At this point, your environment is fully configured for development on macOS. For Linux/Unix, replace Homebrew installs with your distro’s package manager (e.g. `apt install cmake libomp-dev pybind11-dev`), and adjust `DYLD_LIBRARY_PATH` → `LD_LIBRARY_PATH` as needed.

### Persisting Your Shell Configuration

To ensure your venv auto‑activates and the OpenFHE libraries remain discoverable every time you open a terminal, append the following to your `~/.zshrc`:

```bash
# ──────────────────────────────────────────────────────────────────────────────
# FHE‑AI‑Inference: dynamic library path
export DYLD_LIBRARY_PATH="/usr/local/lib:${DYLD_LIBRARY_PATH:-}"

# Auto‑activate the Python venv when entering the project directory
autoload -U add-zsh-hook

function .fhe_venv_auto_activate() {
  if [[ -f "venv/bin/activate" && $(pwd) == *"/fhe-ai-inference"* ]]; then
    # only if not already active
    if [[ -z "$VIRTUAL_ENV" ]]; then
      source venv/bin/activate
    fi
  fi
}

add-zsh-hook chpwd .fhe_venv_auto_activate
# also run it on shell startup if you're already in the project
.fhe_venv_auto_activate
# ──────────────────────────────────────────────────────────────────────────────
```

- **`DYLD_LIBRARY_PATH`** ensures macOS will always find the OpenFHE `.dylib` files in `/usr/local/lib`.  
- The **`chpwd` hook** makes Zsh automatically `source venv/bin/activate` whenever you `cd` into your `fhe-ai-inference` directory.  

After saving, reload your shell:

```bash
source ~/.zshrc
```

# Maintainer

[David William Silva](https://github.com/davidwilliam)

If you have any questions or comments, feel free to reach out to me at contact@davidwsilva.com.