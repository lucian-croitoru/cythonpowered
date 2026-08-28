# AGENTS.md — Guidelines for AI agents working on cythonpowered

Read this file before writing or modifying any `.pyx`, build, test, or benchmark code in this repository.

## 1. Project overview

`cythonpowered` is intended to be a library of **Cython-compiled replacements for popular Python functions**. Extensions are compiled at install time; the core package aims **zero runtime dependencies**. `language_level=3`.

The supported Python versions, the required Cython version, and the current module list are declared in `setup.py` / `pyproject.toml` — treat those files (and `README.md`) as the source of truth, not this document.

## 2. Project philosophy (read first)

This project targets a **maintainable, portable, stable performance alternative** to Python functions — **not** absolute maximum performance.

- Simple, readable C-level code that is measurably faster than the pure-Python original beats clever code that is 5% faster but fragile or hard to maintain.
- When in doubt between a clever fast version and a simple correct version, **pick the simple correct version and measure**. If it is fast enough (it usually is), keep it.
- Functions aim to mirror familiar Python APIs **as closely as practical**: same name and signature where possible, same return types, equivalent behavior. Exact 1:1 mirroring is not always possible — **"close enough" is acceptable** when the deviation is deliberate and documented (see §12).
- Correctness and edge-case behavior versus the Python original is a **first-class requirement**, not an afterthought. If all edge cases cannot be covered due to the "close enough" guideline above, the gap must be documented.
- The core package stays **zero-dependency**. Heavier tooling lives only in optional extras used for benchmarking, never in the core.

## 3. Repository layout (general pattern)

Each module follows the same pattern:

```
cythonpowered/<module>/<module>.pyx     # Cython source (one file per module)
cythonpowered/<module>/__init__.py      # re-exports the public API
tests/unit/test_<module>.py             # pytest unit tests for the module
```

Supporting tooling (CLI, function listing, benchmarking) lives outside the core package. The exact layout, module list, and tooling can evolve — do not hardcode assumptions about them; consult `CONTRIBUTING.md` and `DEVELOPMENT.md` for the current state.

## 4. Build & test workflow (mandatory)

1. Edit the `.pyx` file.
2. **Rebuild before testing**: `python setup.py build_ext --inplace`
   - The `.so` files are gitignored and can silently go stale. A passing test run against a stale `.so` proves nothing about your change. Always rebuild first.
3. Run the full suite: `pytest` — all tests must pass.
4. For changes that may behave differently across Python versions, run the containerized multi-version tests (see `DEVELOPMENT.md`).
5. If performance changed: run the project's benchmark CLI and update `BENCHMARKS.md` on release.

## 5. Cython coding conventions (match the existing style)

- **Public API functions**: `cpdef inline`, with a docstring stating what the function does and which Python function it replaces.
- **Internal C-speed helpers**: `cdef inline`.
- **Naming prefixes**:
  - `c_` — internal `cdef` implementation (the fast C-level body)
  - `cp_` — public `cpdef` wrapper delegating to the `c_` implementation
  - `_` — private helper
  - Simple functions may be a single `cpdef` with no `c_`/`cp_` split.
- **Type every local variable in hot code**: loop counters `cdef unsigned int i`, string-scan indices `cdef Py_ssize_t`, flags `cdef bint`, chars `cdef unsigned char ch`.
- Use `bint` for booleans, never `int`/`bool` flags.
- **Static lookup tables** are typed C arrays: `cdef unsigned char[12] table = [...]`.
- **Block separators**: the codebase groups logical functions under `# -----------`-like banner comments. Keep this structure when adding functions.
- **Docstrings**: one line of what it does + `Replacement for: <python function>`.
- **Comments**: explain *why* and non-obvious invariants (algorithm source, "this is the only allocation", word-boundary rationale). Do not narrate obvious code.
- **C library access**: declare via `cdef extern from "stdlib.h"` / `from libc.string cimport memcmp` / `from cpython.unicode cimport ...`. Prefer libc/ctype over re-implementing.
- Python files (tests, utils) are formatted with **black**; keep them black-compatible. There is no linter for `.pyx` — rely on Cython compiler warnings and review.

## 6. Cython safety rules (critical)

The project relies on these being followed manually — there is no tooling that enforces them.

1. **C array indexing is NEVER bounds-checked.** Cython's `boundscheck` directive does **not** apply to typed C arrays (`cdef T[N] arr; arr[i]`). Verified on Cython 3.3.0: an out-of-range read silently returns garbage with no exception. **Validate or clamp every index before indexing a C array**, especially when the index derives from user input or from arithmetic that can exceed the table size.
2. **Validate inputs at the public boundary** and raise the **same exception type as the Python original** whenever the original raises:
   - empty sequence → `IndexError`, not `ZeroDivisionError` from `% 0`
   - inverted or out-of-range arguments (e.g. `a > b`) → `ValueError`
   - invalid field values (e.g. impossible date components) → `ValueError`
   - Cython 3 converts C integer division/modulo by zero into `ZeroDivisionError` instead of crashing (good), but the *type* should still match the original.
3. **Watch unsigned arithmetic.** `unsigned int` / `unsigned char` wrap silently. Values that can exceed the range must not be stored in narrow unsigned types (e.g. a month stored in `unsigned char` must stay 1–12; an offset computation can push it past 12 — normalize with carry into the year). When mixing signed and unsigned in one expression, the signed operand is silently converted to unsigned.
4. **Never divide or modulo by a value that can be zero** without a prior check.
5. **PRNG discipline**: do **not** re-seed the generator per call — it destroys sequence state, and seeding from `clock()` uses CPU time, not wall time. Seed once at module init if at all. Document that `srand48`/`drand48`/`lrand48` are **not thread-safe**.
6. **No global mutable state** except documented module-level constant tables.
7. **CPython C API**: use only stable, documented APIs (`PyUnicode_KIND`/`PyUnicode_DATA`/`PyUnicode_READ`, `PyUnicode_AsUTF8AndSize`, libc, ctype.h). Never access CPython struct internals. When writing into a unicode buffer of a specific kind (e.g. the 1-byte kind), the ASCII assumption must be documented or validated — non-ASCII input must not be silently mis-handled.
8. **Overflow**: compute in a wider type when a narrow-type expression can overflow (e.g. a years×days multiplication for large years).
9. **No runtime dependencies in the core.**

## 7. Compiler directives & build flags

- `language_level=3` is set in the build config — keep it.
- The build config (`cythonize(...)`) must always keep the **safe Cython 3.x defaults**: `boundscheck=True`, `wraparound=True`, `cdivision=False`, `overflowcheck=False`. **Never set unsafe values at the compiler/build level** — that would silently apply to every module, including ones that have never been audited.
- **Opting out is per-module, not global.** A module may disable checks only via a module-level `# cython:` pragma at the top of its `.pyx` file (e.g. `# cython: boundscheck=False, wraparound=False, cdivision=True`), and only if it adds no risk to **any** function defined in that module. Before adding the pragma, audit every function in the module:
  1. every C array index is validated or clamped (`boundscheck` does not apply to typed C arrays, so validation is still required);
  2. no unsigned expression can wrap unexpectedly;
  3. no division or modulo by a value that can be zero;
  4. no code path relies on negative-index wraparound (if `wraparound=False`);
  5. integer division semantics still match the Python original where it matters (if `cdivision=True` — C truncates toward zero, Python floors).
- The pragma must carry a short comment stating what was audited and why it is safe, and the change gets a `CHANGELOG.md` entry. After enabling it, re-run the full test suite **and** the containerized multi-version tests.
- If a full-module audit is not justified, narrow the scope instead: `@cython.boundscheck(False)` on a single function, or a `with cython.boundscheck(False):` block around an audited hot path. The scope of disabled checks must never be wider than the audit. Every function-level or block-level override must carry a comment explaining why that specific directive is safe for that specific function — which indices/expressions were checked and why they cannot misbehave.
- **Treat new Cython or C compiler warnings as regressions** (implicit C declarations, signed/unsigned comparisons, unsafe casts, unused declarations).
- `-fopenmp` is intentionally disabled (portability, arm64 issues). Do not re-enable it until instructed.

## 8. Testing requirements

- Every new or changed function gets unit tests in the module's test file.
- **Cross-validation is the gold standard**: compare against the Python original (stdlib, or the third-party library the function replaces) across a *range* of inputs, not a single example. Follow the cross-validation patterns already present in the test suite.
- **Edge cases are mandatory**: empty inputs, boundary values, invalid inputs, and domain transitions (e.g. leap-year and century rules, month-end and year-end carry, off-by-one at range limits).
- If the Python original raises on an input, the Cython version must raise the **same exception type** — assert with `pytest.raises`.
- Random tests stay deterministic: assert distribution properties (range, subset, length, distinctness), never specific values.
- Tests run against the freshly rebuilt extension (see §4).

## 9. Performance guidelines

- **Measure before and after.** Use the existing benchmark framework; every new function gets a benchmark definition (see §10).
- Target: beat the pure-Python original by a meaningful margin (see `BENCHMARKS.md`). 1.05× on a simple function is acceptable; 2× - 5× on complex code is expected; >10× is not uncommon. Some functions may be slower with Cython, but they should not be eliminated if they contribute to module completeness or are used internally by other functions.
- Preferred optimization techniques, in order of preference:
  1. Typed local variables and `cpdef`/`cdef` signatures (eliminate Python dispatch overhead)
  2. Batched `n_*` variants that replace list comprehensions
  3. Single-pass C-level scanning — no regex, no backtracking, no repeated substring allocation
  4. Typed C-array lookup tables for small static data
  5. CPython C API (`PyUnicode_*`) to avoid per-character Python object creation in hot loops
- **Avoid**: premature micro-optimization, compiler flags that trade correctness for speed, platform-specific intrinsics, anything that breaks the supported Python/platform matrix.
- Update `BENCHMARKS.md` on release with the new data.

## 10. Adding a new function (checklist)

1. Implement in the module's `.pyx` following §5–§6.
2. Re-export from the module's `__init__.py`.
3. Add tests (cross-validation + edge cases, §8).
4. Add a row to the module table in `README.md`.
5. Register the function in the project's listing and benchmark tooling — consult `CONTRIBUTING.md` and existing per-module definition/benchmark files for the current pattern.
6. Rebuild (`python setup.py build_ext --inplace`) and run `pytest`.
7. Add a `CHANGELOG.md` entry.

## 11. Adding a new module

- Create `cythonpowered/<name>/<name>.pyx` + `__init__.py`.
- Register the module in the build config (`setup.py` / `pyproject.toml`), the top-level package metadata, and the listing/benchmark tooling — consult `CONTRIBUTING.md` for the current registration points.
- Create the module's test file and register it with the test runner.
- Update `README.md` and `CHANGELOG.md`.

## 12. API & interop contract

- Public functions return plain Python types (`str`, `int`, `list`, `tuple`) matching the original.
- **Mirroring is "as close as practical" (§2)**: where exact parity is impossible, the deviation must be deliberate, documented in the `README.md` table and the function docstring, and covered by a test.
- Extension types that mirror a stdlib type must interop with it: `__eq__` should compare correctly against **both** the Cython type and the stdlib type, and whenever `__eq__` crosses types, `__hash__` must match the stdlib hash (delegate to the stdlib hash if needed). `__repr__`/`__str__` should match stdlib formatting; if the original lacks `__repr__`/`__str__`, provide a reasonable default.
- Keyword argument names match the Python original where the original has kwargs.

## 13. Versioning & release

- The version is duplicated across the build config and the top-level package `__init__.py` — update **all copies** on release.
- Every release gets a `CHANGELOG.md` entry.
- Build/publish workflow: see `DEVELOPMENT.md`.
- DO NOT PERFORM ANY GIT COMMITS OR PUSHES. DO NOT PUBLISH TO PYPY.ORG YOURSELF.

## 14. Anti-patterns (do not do)

- Do not chase absolute maximum performance at the cost of clarity, portability, or correctness.
- Do not set `boundscheck=False`/`wraparound=False`/`cdivision=True` in the build config — only via an audited per-module (or narrower) pragma in the `.pyx` itself, per §7.
- Do not index C arrays without validating the index (boundscheck does not help you here).
- Do not re-seed the PRNG per call.
- Do not add runtime dependencies to the core package.
- Do not use CPython struct internals, platform-specific code, or compiler tricks that break the supported matrix.
- Do not rely on a passing test run without rebuilding after `.pyx` edits.
- Do not port regex-based Python implementations into Cython as-is — rewrite as single-pass scanning.
- Do not leave debug prints or dead code in the core modules.
