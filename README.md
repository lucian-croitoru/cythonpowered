# Cythonpowered

Cython-powered replacements for popular Python functions — compiled for performance.

[![PyPI version](https://img.shields.io/pypi/v/cythonpowered.svg)](https://pypi.org/project/cythonpowered/)
[![Python versions](https://img.shields.io/pypi/pyversions/cythonpowered.svg)](https://pypi.org/project/cythonpowered/)
[![License](https://img.shields.io/pypi/l/cythonpowered.svg)](LICENSE)

## What cythonpowered IS

- A library of **Cython-compiled** function replacements designed for **performance**. Each function is written in Cython and compiled to native code, providing measurable speedups over the pure-Python equivalents it replaces.
- A set of **native extensions compiled at install time**. `pip install` builds the C extensions for your platform, so there is no runtime compilation, no build step, and no extra tooling required from end users.
- A collection of functions that **mirror familiar APIs** from the standard library and popular third-party packages. Many are drop-in replacements you can swap in with minimal code changes, while others extend functionality beyond what the originals offer.

## What cythonpowered is NOT

- A wrapper or fork of an existing Python library. Every function is implemented from scratch in Cython — cythonpowered does not re-export, subclass, or bind to CPython internals or third-party packages; it stands on its own.
- A 100% drop-in replacement for the libraries it draws inspiration from. Functions target the most common use cases and mirror familiar interfaces, but edge-case behavior or supported options may differ from the originals.
- A guarantee of speedups on every system. Measured speedups depend on hardware, data shapes, and usage patterns, and some operations may be slower than their pure-Python counterparts. Always benchmark for your specific use case before relying on the numbers.

## Quick Start

```bash
pip install cythonpowered
```

## Modules

### `cythonpowered.random` — Random number generation

| Function | Replaces | Speedup |
|---|---|---|
| `random()` | `random.random()` | ~1.0x |
| `n_random(k)` | `[random() for _ in range(k)]` | ~2.9x |
| `randint(a, b)` | `random.randint(a, b)` | ~5.2x |
| `n_randint(a, b, k)` | `[randint(a, b) for _ in range(k)]` | ~20.2x |
| `uniform(a, b)` | `random.uniform(a, b)` | ~1.9x |
| `n_uniform(a, b, k)` | `[uniform(a, b) for _ in range(k)]` | ~8.5x |
| `choice(pop)` | `random.choice(pop)` | ~5.0x |
| `choices(pop, k)` | `random.choices(pop, k=k)` | ~2.1x |

### `cythonpowered.dateutil` — Date utilities

| Function | Replaces | Speedup |
|---|---|---|
| `date.today()` | `datetime.date.today()` | ~1.1x |
| `date.isleap(y)` | `calendar.isleap(y)` | ~1.7x |
| `date.monthrange(y, m)` | `calendar.monthrange(y, m)` | ~3.7x |
| `date.fromstring(s)` | `strptime().date()` | ~10.3x |
| `date().tostring()` | `strftime('%Y-%m-%d')` | ~16.5x |
| `date().weekday()` | `datetime.date().weekday()` | ~1.0x |
| `date().yearday()` | `timetuple().tm_yday` | ~9.8x |
| `date.fromordinal(n)` | `datetime.date.fromordinal()` | ~0.7x |
| `date().toordinal()` | `datetime.date().toordinal()` | ~0.6x |
| `date().offset(...)` | `date + timedelta` | ~2.9x |
| `date().increment()` | `date + timedelta(days=1)` | ~3.4x |
| `date.date_range(...)` | `pandas.date_range()` | ~15.5x |

### `cythonpowered.textparse` — Text extraction

| Function | Replaces | Speedup |
|---|---|---|
| `html.get_text(html, strip=False)` | `BeautifulSoup().get_text()` | ~38.2x |
| `html.find(html, tag, recursive=True)` | `BeautifulSoup().find()` | ~552.8x |
| `html.find_all(html, tag, recursive=True)` | `BeautifulSoup().find_all()` | ~408.8x |
| `get_attr(tag, attr)` | `BeautifulSoup().find().get()` | ~638.7x |
| `get_ips(text)` | `re.findall(...)` | ~3.4x |
| `get_emails(text)` | `re.findall(...)` | ~3.1x |
| `get_mac_addrs(text)` | `re.findall(...)` | ~1.6x |

Note: `get_attr()` operates on a single tag string (e.g. the result of `html.find()`), not on a full HTML document. Speedups are vs. BeautifulSoup; comparisons vs. `lxml` are in [BENCHMARKS.md](BENCHMARKS.md).

See [BENCHMARKS.md](BENCHMARKS.md) for full benchmark data.

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

- [Changelog](CHANGELOG.md)
- [Benchmarks](BENCHMARKS.md)
- [Contributing](CONTRIBUTING.md)
- [Development](DEVELOPMENT.md)
- [GitHub](https://github.com/lucian-croitoru/cythonpowered)
