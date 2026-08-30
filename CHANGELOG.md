# CHANGELOG


### 0.4.0 - 2026-08-31
**general**
 - Added `AGENTS.md` containing coding standards for accelerated agentic development
 - Aligned the entire library to the standards
 - Essential change summary below

**textparse**
- HTML fixes: non-ASCII text no longer corrupts results, bare `<` in text is handled, exact tag-name matching (`<scriptfoo>` ≠ `<script>`), case-insensitive tag/attribute names, `<wbr>` now a void element
- `get_emails()` / `get_mac_addrs()` now match the original regex exactly (no empty local part, mixed MAC separators allowed, no word boundaries)
- Various performance improvements

**random**
- Replaced the C library's 48-bit LCG with an inlined xorshift128 (period 2**128−1); state is now seeded exactly once at import
- `random()` now offers 32-bit precision (`stdlib`: 53 bits)
- `randint()` is now exactly uniform (rejection sampling) and raises `ValueError` when `a > b`
- `choice()`/`choices()` raise `IndexError` on empty populations — matching `stdlib`
- Various performance improvements


**dateutil**
- `date` validates fields in the constructor (`ValueError`, like `datetime.date`); `year`/`month`/`day` are now read-only
- `offset()` no longer mutates its input and raises `OverflowError` outside 1..9999
- `increment()` raises `OverflowError` at 9999-12-31
- `fromordinal()` no longer overflows on large ordinals
- `monthrange()` / `date_range()` / `tostring()` now raise on invalid input (matching `calendar`/ `pandas`)
- Various performance improvements

**setup.py**
- Dropped the NumPy-leftover `NPY_NO_DEPRECATED_API` macro
- Always build with `-O2`
- Made Cython 3.x safety flags explicit

### 0.3.2 - 2026-08-27
- Using absolute links in README

### 0.3.1 - 2026-08-27
- Minor tweaks to the CLI functionality

### 0.3.0 - 2026-08-27
- Added the `textparse` module
- License changed from `GPL-3.0` to `MIT`
- Benchmark-only dependencies moved to optional `[utils]` extra
- `date.today()` now correctly uses `time.localtime()` — timezone changes after import no longer affect results
- `date` class now has `__repr__`, `__str__`, `__eq__`, `__hash__` for better interoperability with `datetime.date`

### 0.2.3 - 2026-03-15
- Major performance improvement for `dateutil.date.tostring`
- `dateutil.date.offset` now supports days, weeks, months and years as parameters
- Added the `dateutil.date.increment` function (fast date incrementation by 1 day)
- Added the `deteutil.date.date_range` function, similar to `pandas.date_range`
- Dropped support for Python 3.8

### 0.2.2 - 2026-02-23
- Update project metadata

### 0.2.1 - 2026-02-23
- Extended the `dateutil` module with the `fromordinal`, `toordinal` and `offset` functions

### 0.2.0 - 2026-02-22
- Added the `dateutil` module
- Various internal tweaks

### 0.1.12 - 2026-02-13
- Bugfix in setup

### 0.1.11 - 2026-02-13
- Performance improvements for the `random` module
- Added containerized tests
- Supported Python versions are 3.8 - 3.14

### 0.1.10 - 2024-10-08
- Added the `cythonpowered --list` command
- Added initial documentation
- Various internal tweaks

### 0.1.9 - 2024-09-29
- Bugfix in retrieveing system information for benchmark

### 0.1.8 - 2024-09-29
- Bugfix in setup
- Temporarily disabled `-fopenmp` parameter until making more thorough troubleshooting for `arm46` arch

### 0.1.7 - 2024-09-28
- Pinned versions of `setuptools` and `wheel`

### 0.1.6 - 2024-09-28
- Used `prettytable` for benchmark output (`cythonpowered --benchmark`) 

### 0.1.5 - 2024-09-23
- Bugfix in setup

### 0.1.4 - 2024-09-23
- Added the `cythonpowered` CLI script as an entrypoint for all utils and scripts
- Deprecated the `cythonpowered-benchmark` script

### 0.1.3 - 2024-09-22
- Bugfix in Cython preinstallation

### 0.1.2 - 2024-09-22
- Added MANIFEST.in
- Ensured markdown project description

### 0.1.1 - 2024-09-22
- Bugfix in setup

### 0.1.0 - 2024-09-22
- Added the `cythonpowered-benchmark` script
- Development updates

### 0.0.3 - 2024-09-10
- Update requirements

### 0.0.2 - 2024-09-10
- Bugfix in setup

### 0.0.1 - 2024-09-10
- First release
- Includes the `cythonpowered.random` module
