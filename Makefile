# Makefile for building and installing markdown_normalization Python wheel

PACKAGE_NAME := rustid
PYTHON := $(shell which python)

.PHONY: all check-deps install-deps build install clean test

all: check-deps install-deps build test install clean

check-deps:
	@command -v rustc >/dev/null 2>&1 || { echo >&2 "❌ rustc not found. Please install Rust: https://rustup.rs"; exit 1; }
	@command -v cargo >/dev/null 2>&1 || { echo >&2 "❌ cargo not found. Please install Rust: https://rustup.rs"; exit 1; }
	@command -v $(PYTHON) >/dev/null 2>&1 || { echo >&2 "❌ $(PYTHON) not found."; exit 1; }

install-deps:
	@$(PYTHON) -m pip show maturin >/dev/null 2>&1 || { \
		echo "📦 Installing maturin..."; \
		python3 -m pip install --upgrade maturin; \
	}

build:
	@echo "🔨 Building wheel with maturin..."
	@maturin build --release --strip
	@rm -f target/wheels/*linux_x86_64.whl
	
test:
	@echo "🧪 Running tests..."
	@$(PYTHON) -m pip install pytest
	@$(PYTHON) -m pytest -v -s

install:
	@echo "📦 Installing wheel locally..."
	@pip install --force-reinstall --no-cache-dir $(shell ls target/wheels/$(PACKAGE_NAME)-*.whl | head -n1)

clean:
	@echo "🧹 Cleaning build artifacts..."
	@rm -rf build dist target *.egg-info
	@find . -type d -name '__pycache__' -exec rm -rf {} +