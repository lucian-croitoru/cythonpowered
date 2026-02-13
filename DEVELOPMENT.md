# Development Workflow for cythonpowered

This document describes the commands needed to test, build, and publish the cythonpowered package after making updates to the Cython code.

## 1. Testing

### Local Testing (Development)

After updating Cython code, rebuild the extensions in-place:

```bash
# Rebuild Cython extensions in development mode
python setup.py build_ext --inplace
```

Then run the test suite:

```bash
# Run unit tests
pytest

# Or run the benchmark to verify Cython compilation
python -m utils.main -b
```

### Containerized Testing (All Python Versions)

Test across all supported Python versions (3.8-3.14) using Docker:

```bash
# Run containerized tests
./test-container.sh
```

This will:
- Build the package for each Python version
- Install it in a clean container
- Run benchmarks to verify Cython modules work
- Display results for all versions

## 2. Building the Package

### Clean Previous Builds

```bash
# Remove build artifacts
rm -rf build dist *.egg-info 
```

### Build Distribution Packages

```bash
# Build both source distribution (.tar.gz) and wheel (.whl)
python setup.py build
python setup.py sdist bdist_wheel
```

### Upload to PyPI

```bash
# Install twine (if not already installed)
pip install twine

# Upload to PyPI
twine upload --verbose dist/cythonpowered-*.tar.gz 
```

### Verify Upload

```bash
# Check PyPI package page
# https://pypi.org/project/cythonpowered/

# Or install from PyPI to verify
pip install --upgrade cythonpowered
python -c "import cythonpowered; print(cythonpowered.VERSION)"
```
