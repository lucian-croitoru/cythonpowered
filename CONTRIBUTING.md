# Contributing to Cythonpowered

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/lucian-croitoru/cythonpowered.git
   cd cythonpowered
   ```

2. Create and activate a virtual environment:
   ```bash
   source dev_venv.sh
   ```

3. (Re)build Cython extensions:
   ```bash
   python setup.py build_ext --inplace
   ```

4. Run tests:
   ```bash
   pytest
   ```

5. Run containerized tests (requires Docker):
   ```bash
   ./test-container.sh
   ```

## Adding New Functions

1. Add Cython code to `cythonpowered/<module>/<module>.pyx`
2. Export from `cythonpowered/<module>/__init__.py`
3. Add definitions in `utils/definitions/_<module>.py`
4. Add benchmark definitions in `utils/benchmark/_<module>.py`
5. Add tests in `tests/unit/test_<module>.py`
6. Update `pyproject.toml` and `setup.py` packages list (if new module)

## Testing

- Write unit tests for all new functions in `tests/unit/`
- Include cross-validation tests against stdlib / Python equivalents where applicable
- Ensure all existing tests pass before submitting changes

## Reporting Issues

- Use GitHub Issues for bug reports and feature requests
- Include system specs, Python version, and steps to reproduce
