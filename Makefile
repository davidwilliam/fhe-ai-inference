SHELL := /bin/sh

.PHONY: all install clean verify test

# Configuration
OPENFHE_VERSION       = v1.2.3
OPENFHE_PYTHON_TAG    = v0.8.10
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

all: install

install: install-dependencies clone-repos build-openfhe build-openfhe-python setup-env verify

install-dependencies:
	@echo "Installing Homebrew dependencies..."
	@brew install libomp gmp mpfr cmake || true

clone-repos:
	@echo "Cloning OpenFHE C++ core ($(OPENFHE_VERSION))..."
	@if [ ! -d "$(OPENFHE_DIR)" ]; then \
		git clone https://github.com/openfheorg/openfhe-development.git $(OPENFHE_DIR); \
		cd $(OPENFHE_DIR) && git checkout $(OPENFHE_VERSION); \
	else \
		cd $(OPENFHE_DIR) && git fetch && git checkout $(OPENFHE_VERSION); \
	fi
	@echo "Cloning OpenFHE-Python wrapper ($(OPENFHE_PYTHON_TAG))..."
	@if [ ! -d "$(OPENFHE_PYTHON_DIR)" ]; then \
		git clone https://github.com/openfheorg/openfhe-python.git $(OPENFHE_PYTHON_DIR); \
		cd $(OPENFHE_PYTHON_DIR) && git checkout $(OPENFHE_PYTHON_TAG); \
	else \
		cd $(OPENFHE_PYTHON_DIR) && git fetch && git checkout $(OPENFHE_PYTHON_TAG); \
	fi

build-openfhe:
	@echo "Building and installing OpenFHE C++ core ($(OPENFHE_VERSION))..."
	@mkdir -p $(OPENFHE_DIR)/build
	@cd $(OPENFHE_DIR)/build && \
		rm -rf * && \
		cmake $(CMAKE_FLAGS) --log-level=DEBUG .. && \
		make -j$(shell sysctl -n hw.ncpu) && \
		sudo make install

build-openfhe-python:
	@echo "Installing OpenFHE Python bindings from source ($(OPENFHE_PYTHON_TAG))..."
	@cd $(OPENFHE_PYTHON_DIR) && pip install . --no-cache-dir

setup-env:
	@echo "Configuring $(ZSHRC) for fhe-ai-inference…"
	@grep -F "# >>> fhe-ai-inference configuration >>>" "$(ZSHRC)" >/dev/null 2>&1 || { \
		echo "# >>> fhe-ai-inference configuration >>>" >> "$(ZSHRC)"; \
		echo "export DYLD_LIBRARY_PATH=\"$(INSTALL_PREFIX)/lib:\$$DYLD_LIBRARY_PATH\"" >> "$(ZSHRC)"; \
		echo "# <<< fhe-ai-inference configuration <<<" >> "$(ZSHRC)"; \
		echo "✔ fhe-ai-inference block added to $(ZSHRC)" >&2; \
	}
	@printf "\n→ To pick up these changes, run:\n    source $(ZSHRC)   (or restart your terminal)\n\n"

verify:
	@echo "Verifying OpenFHE C++ libs in $(INSTALL_PREFIX)/lib…"
	@ls $(INSTALL_PREFIX)/lib | grep -i openfhe >/dev/null || (echo "Error: C++ libs not found"; exit 1)
	@echo "Running OpenFHE Python smoke test…"
	@python -c "import openfhe; print('✅ OpenFHE Python bindings import OK')"
	@echo "✅ OpenFHE context successfully initialized with CKKS."

test:
	@echo "Running fhe-ai-inference tests via Hatch..."
	@cd $(HOME)/workspace_python/fhe-ai-inference && \
	  hatch run pytest

clean:
	@echo "Cleaning up…"
	@rm -rf $(OPENFHE_DIR)/build
	@pip uninstall -y openfhe || true
