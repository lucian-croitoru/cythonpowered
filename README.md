# Cythonpowered

Cython-powered replacements for popular Python functions — compiled for performance.

[![PyPI version](https://img.shields.io/pypi/v/cythonpowered.svg)](https://pypi.org/project/cythonpowered/)
[![Python versions](https://img.shields.io/pypi/pyversions/cythonpowered.svg)](https://pypi.org/project/cythonpowered/)
[![License](https://img.shields.io/pypi/l/cythonpowered.svg)](https://github.com/lucian-croitoru/cythonpowered/blob/main/LICENSE)

## What cythonpowered IS

- A library of **Cython-compiled** function replacements designed for **performance**. Each function is written in Cython and compiled to native code, providing measurable speedups over the pure-Python equivalents it replaces.
- A set of **native extensions compiled at install time**. `pip install` builds the C extensions for your platform, so there is no runtime compilation, no build step, and no extra tooling required from end users.
- A collection of functions that **mirror familiar APIs** from the standard library and popular third-party packages. Many are drop-in replacements you can swap in with minimal code changes, while others extend functionality beyond what the originals offer.
- **Lightweight. Zero runtime dependencies**. A pure Cython core with no external packages means no dependency conflicts or transitive bloat, making it ideal for performance-critical or containerized deployments. Heavier tooling (e.g. `pandas`, `beautifulsoup4`) lives only in the optional `[utils]` extra for benchmarking, never in the core.

## What cythonpowered is NOT

- A wrapper or fork of an existing Python library. Every function is implemented from scratch in Cython — cythonpowered does not re-export, subclass, or bind to CPython internals or third-party packages; it stands on its own.
- A 100% drop-in replacement for the libraries it draws inspiration from. Functions target the most common use cases and mirror familiar interfaces, but edge-case behavior or supported options may differ from the originals.
- A universal speedup guarantee. Functions are designed to outperform the pure-Python equivalents they replace, and most deliver measurable gains — see [BENCHMARKS.md](https://github.com/lucian-croitoru/cythonpowered/blob/main/BENCHMARKS.md). Exact speedups vary with hardware, OS, Python version, C compiler, data and usage patterns, so benchmark on your own workload before relying on specific figures.

## Quick Start

```bash
pip install cythonpowered
```

## Modules

### `cythonpowered.random` — Random number generation

| # | Cythonpowered function | Replaces (Python function) | Usage / details |
|---|---|---|---|
|  1 | cythonpowered.random.random()             | random.random()                              | Drop-in replacement, 32-bit precision                                      |
|  2 | cythonpowered.random.n_random()           | random.random()                              | n_random(k) replaces [random() for i in range(k)]                          |
|  3 | cythonpowered.random.randint()            | random.randint()                             | Drop-in replacement                                                        |
|  4 | cythonpowered.random.n_randint()          | random.randint()                             | n_randint(a, b, k) replaces [randint(a, b) for i in range(k)]              |
|  5 | cythonpowered.random.uniform()            | random.uniform()                             | Drop-in replacement                                                        |
|  6 | cythonpowered.random.n_uniform()          | random.uniform()                             | n_uniform(a, b, k) replaces [uniform(a, b) for i in range(k)]              |
|  7 | cythonpowered.random.choice()             | random.choice()                              | Drop-in replacement                                                        |
|  8 | cythonpowered.random.choices()            | random.choices()                             | Drop-in replacement, only supports the 'k' keyword argument                |


### `cythonpowered.dateutil` — Date utilities

| # | Cythonpowered function | Replaces (Python function) | Usage / details |
|---|---|---|---|
|  9 | cythonpowered.dateutil.date.today()       | datetime.date.today()                        | Drop-in replacement, returns cythonpowered date object                     |
| 10 | cythonpowered.dateutil.date.isleap()      | calendar.isleap()                            | Drop-in replacement                                                        |
| 11 | cythonpowered.dateutil.date.monthrange()  | calendar.monthrange()                        | Drop-in replacement                                                        |
| 12 | cythonpowered.dateutil.date.fromstring()  | datetime.datetime.strptime().date()          | Assumes '%Y-%m-%d' format, returns cythonpowered date object               |
| 13 | cythonpowered.dateutil.date().tostring()  | datetime.date().strftime()                   | Assumes '%Y-%m-%d' format, uses cythonpowered date object                  |
| 14 | cythonpowered.dateutil.date().weekday()   | datetime.date().weekday()                    | Drop-in replacement, uses cythonpowered date object                        |
| 15 | cythonpowered.dateutil.date().yearday()   | datetime.date().timetuple().tm_yday          | Drop-in replacement, uses cythonpowered date object                        |
| 16 | cythonpowered.dateutil.date.fromordinal() | datetime.date.fromordinal()                  | Drop-in replacement, returns cythonpowered date object                     |
| 17 | cythonpowered.dateutil.date.toordinal()   | datetime.date().toordinal()                  | Drop-in replacement, uses cythonpowered date object                        |
| 18 | cythonpowered.dateutil.date().offset()    | datetime.date() +/- datetime.timedelta()     | Supports days/weeks/months/years offset, returns cythonpowered date object |
| 19 | cythonpowered.dateutil.date().increment() | datetime.date() + datetime.timedelta(days=1) | Increments cythonpowered date object by 1 day                              |
| 20 | cythonpowered.dateutil.date_range()       | pandas.date_range()                          | Uses cythonpowered date object, returns a list of date strings             |


### `cythonpowered.textparse` — Text extraction

| # | Cythonpowered function | Replaces (Python function) | Usage / details |
|---|---|---|---|
| 21 | cythonpowered.textparse.html.get_text()   | BeautifulSoup().get_text()                   | Drop-in replacement, no HTML entity decoding                               |
| 22 | cythonpowered.textparse.html.find()       | BeautifulSoup().find()                       | Drop-in replacement, raw substring                                         |
| 23 | cythonpowered.textparse.html.find_all()   | BeautifulSoup().find_all()                   | Drop-in replacement, raw substrings                                        |
| 24 | cythonpowered.textparse.html.get_attr()   | BeautifulSoup().find().get()                 | Takes single tag string as input, not a document                           |
| 25 | cythonpowered.textparse.get_ips()         | re.findall(...) implementation to get IPs    | Drop-in replacement, ASCII only                                            |
| 26 | cythonpowered.textparse.get_emails()      | re.findall(...) implementation to get emails | Drop-in replacement, ASCII only                                            |
| 27 | cythonpowered.textparse.get_mac_addrs()   | re.findall(...) implementation to get MACs   | Drop-in replacement                                                        |



Note: `get_attr()` operates on a single tag string (e.g. the result of `html.find()`), not on a full HTML document. `find()`/`find_all()` return raw substrings of the input (original tag-name case and attribute order are preserved; tag names are matched case-insensitively) and do not apply deep HTML error recovery (implicit end tags, foster parenting). See [BENCHMARKS.md](https://github.com/lucian-croitoru/cythonpowered/blob/main/BENCHMARKS.md) for full benchmark data (speedup comparison).

## Installation

```bash
# Core library (no runtime dependencies)
pip install cythonpowered

# Optional: benchmark tools and utils
pip install cythonpowered[utils]
```

## CLI

Installing the package provides the `cythonpowered` command:

```bash
cythonpowered --list       # list all functions and their Python counterparts
cythonpowered --benchmark  # run benchmarks on your system (requires the [utils] extra)
cythonpowered --version    # print the package version
```

## Links

- [Changelog](https://github.com/lucian-croitoru/cythonpowered/blob/main/CHANGELOG.md)
- [Benchmarks](https://github.com/lucian-croitoru/cythonpowered/blob/main/BENCHMARKS.md)
- [Contributing](https://github.com/lucian-croitoru/cythonpowered/blob/main/CONTRIBUTING.md)
- [Development](https://github.com/lucian-croitoru/cythonpowered/blob/main/DEVELOPMENT.md)
- [GitHub](https://github.com/lucian-croitoru/cythonpowered)
