.PHONY: help install dev lint format test test-cov build clean

# ──────────────────────────────────────────────
# Default target
# ──────────────────────────────────────────────
help:
	@echo ""
	@echo "ShortcutsPy — available commands:"
	@echo ""
	@echo "  make install     Install the package"
	@echo "  make dev         Install with dev dependencies"
	@echo "  make lint        Run Ruff linter"
	@echo "  make format      Run Ruff formatter"
	@echo "  make test        Run tests"
	@echo "  make test-cov    Run tests with coverage report"
	@echo "  make build       Build wheel and sdist"
	@echo "  make clean       Remove build artifacts"
	@echo ""

# ──────────────────────────────────────────────
# Installation
# ──────────────────────────────────────────────
install:
	pip install -e .

dev:
	pip install -e ".[dev]"
	pre-commit install

# ──────────────────────────────────────────────
# Code quality
# ──────────────────────────────────────────────
lint:
	ruff check shortcutspy/ tests/

format:
	ruff format shortcutspy/ tests/

# ──────────────────────────────────────────────
# Testing
# ──────────────────────────────────────────────
test:
	pytest

test-cov:
	pytest --cov=shortcutspy --cov-report=term-missing --cov-report=html

# ──────────────────────────────────────────────
# Build
# ──────────────────────────────────────────────
build:
	python -m build

# ──────────────────────────────────────────────
# Cleanup
# ──────────────────────────────────────────────
clean:
	rm -rf build/ dist/ *.egg-info/ .pytest_cache/ htmlcov/ .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -name "*.pyc" -delete
