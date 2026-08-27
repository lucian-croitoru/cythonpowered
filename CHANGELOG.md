# CHANGELOG

### 0.3.0 - 2026-08-27
- Added the `textparse` module
- License changed from `GPL-3.0` to `MIT`
- Benchmark-only dependencies moved to optional `[benchmark]` extra
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
