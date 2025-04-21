SHELL := /bin/sh

# Makefile for fhe-ai-inference: Automates OpenFHE and OpenFHE-Python setup
.PHONY: all install clean verify test

# Configuration
OPENFHE_VERSION       = v0.9.0
OPENFHE_PYTHON_COMMIT = 608717f
OPENFHE_DIR           = $(HOME)/workspace_cpp/openfhe-development
OPENFHE_PYTHON_DIR    = $(HOME)/workspace_cpp/openfhe-python
INSTALL_PREFIX        = /usr/local
HATCH_ENV             = fhe-ai-inference

CMAKE_FLAGS = \
  -DCMAKE_INSTALL_PREFIX=$(INSTALL_PREFIX) \
  -DBUILD_SHARED=ON \
  -DBUILD_STATIC=OFF \
  -DCMAKE_C_COMPILER=/usr/bin/clang \
  -DCMAKE_CXX_COMPILER=/usr/bin/clang++ \
  -DBUILD_BENCHMARKS=OFF \
  -DBUILD_UNITTESTS=OFF \
  -DBUILD_EXAMPLES=OFF \
  -DOpenMP_C_FLAGS="-Xpreprocessor -fopenmp -I/opt/homebrew/opt/libomp/include" \
  -DOpenMP_CXX_FLAGS="-Xpreprocessor -fopenmp -I/opt/homebrew/opt/libomp/include" \
  -DOpenMP_C_LIB_NAMES="libomp" \
  -DOpenMP_CXX_LIB_NAMES="libomp" \
  -DOpenMP_libomp_LIBRARY="/opt/homebrew/opt/libomp/lib/libomp.dylib" \
  -DCMAKE_CXX_FLAGS="-Wno-error=unused-but-set-variable -Wno-error=deprecated-declarations"

ZSHRC = $(HOME)/.zshrc

# Default target
all: install

# Composite install
install: install-dependencies clone-repos build-openfhe build-openfhe-python setup-env verify

# Install Homebrew dependencies
install-dependencies:
	@echo "Installing Homebrew dependencies..."
	@brew install libomp gmp mpfr cmake || true

# Clone or update repositories
clone-repos:
	@echo "Cloning OpenFHE $(OPENFHE_VERSION)..."
	@if [ ! -d "$(OPENFHE_DIR)" ]; then \
	  git clone https://github.com/openfheorg/openfhe-development.git $(OPENFHE_DIR); \
	  cd $(OPENFHE_DIR) && git checkout $(OPENFHE_VERSION); \
	else \
	  cd $(OPENFHE_DIR) && git fetch && git checkout $(OPENFHE_VERSION); \
	fi
	@echo "Cloning OpenFHE-Python $(OPENFHE_PYTHON_COMMIT)..."
	@if [ ! -d "$(OPENFHE_PYTHON_DIR)" ]; then \
	  git clone https://github.com/openfheorg/openfhe-python.git $(OPENFHE_PYTHON_DIR); \
	  cd $(OPENFHE_PYTHON_DIR) && git checkout $(OPENFHE_PYTHON_COMMIT); \
	else \
	  cd $(OPENFHE_PYTHON_DIR) && git fetch && git checkout $(OPENFHE_PYTHON_COMMIT); \
	fi

# Build and install OpenFHE C++ library
build-openfhe:
	@echo "Building OpenFHE..."
	@mkdir -p $(OPENFHE_DIR)/build
	@cd $(OPENFHE_DIR)/build && \
	  rm -rf * && \
	  cmake $(CMAKE_FLAGS) --log-level=DEBUG .. && \
	  make -j4 && \
	  sudo make install

# Build and install Python bindings
build-openfhe-python:
	@echo "Installing OpenFHE-Python..."
	@cd $(OPENFHE_PYTHON_DIR) && pip install .

# Set up environment variables (idempotent)
setup-env:
	@echo "Configuring $(ZSHRC) for fhe-ai-inference…"
	@grep -F "# >>> fhe-ai-inference configuration >>>" "$(ZSHRC)" >/dev/null 2>&1 || { \
	  echo "# >>> fhe-ai-inference configuration >>>" >> "$(ZSHRC)"; \
	  echo "export DYLD_LIBRARY_PATH=\"$(INSTALL_PREFIX)/lib:\$$DYLD_LIBRARY_PATH\"" >> "$(ZSHRC)"; \
	  echo "# <<< fhe-ai-inference configuration <<<" >> "$(ZSHRC)"; \
	  echo "✔ fhe-ai-inference block added to $(ZSHRC)" >&2; \
	}
	@echo
	@echo "→ To pick up these changes, run:"
	@echo "    source $(ZSHRC)   (or restart your terminal)"

# Verify installation
verify:
	@echo "Verifying OpenFHE libraries in $(INSTALL_PREFIX)/lib…"
	@ls $(INSTALL_PREFIX)/lib | grep -i openfhe >/dev/null || (echo "Error: OpenFHE libraries not found" && exit 1)
	@echo "Locating openfhe.so in hatch env…"
	@FILE=$$(find "$(HOME)/Library/Application Support/hatch/env/virtual/$(HATCH_ENV)" -type f -name openfhe.so | head -n 1); \
	[ -n "$$FILE" ] || (echo "Error: openfhe.so not found" && exit 1); \
	@echo "Found $$FILE"; \
	otool -L "$$FILE" | grep -E 'libOPENFHE|libomp' || (echo "Error: openfhe.so dependencies not resolved" && exit 1)
	@echo "Running minimal OpenFHE Python smoke test…"
	@python -c "from openfhe import CCParamsCKKSRNS, GenCryptoContext; params=CCParamsCKKSRNS(); params.SetMultiplicativeDepth(3); params.SetScalingModSize(50); params.SetRingDim(16384); GenCryptoContext(params); print('OK')"

# Run full test suite
test:
	@echo "Running fhe-ai-inference tests…"
	@cd $(HOME)/workspace_python/fhe-ai-inference && \
	  hatch run pytest tests/test_original_ckks.py -v --log-file=pytest.log && \
	  hatch run pytest tests/test_context.py::test_ckks_context_creation -v --log-file=pytest.log && \
	  hatch run pytest tests/test_context.py -v --log-file=pytest.log && \
	  hatch run pytest tests/test_activations.py -v --log-file=pytest.log && \
	  hatch run pytest tests/test_inference.py -v --log-file=pytest.log && \
	  hatch run test && \
	  hatch run dev

# Clean build artifacts
clean:
	@echo "Cleaning up…"
	@rm -rf $(OPENFHE_DIR)/build
	@rm -rf $(OPENFHE_PYTHON_DIR)/build
	@pip uninstall -y openfhe || true
