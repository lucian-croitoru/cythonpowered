# Cythonpowered Benchmarks

## System Specifications

- **CPU model**: 11th Gen Intel(R) Core(TM) i7-11370H @ 3.30GHz
- **CPU base frequency**: 3.3000 GHz
- **CPU cores**: 4
- **CPU threads**: 4
- **Architecture**: x86_64
- **Memory (RAM)**: 15.31 GB
- **Operating System**: Linux 6.8.0-138-generic
- **Python version**: 3.12.3
- **C compiler**: GCC 13.3.0

## Benchmark Results

### cythonpowered.random

| Function | Runs | Speed factor | Avg. speedup |
|---|---|---|---|
| `[Python] random.random()` | [10K, 100K, 1M] | 1.00 | 1.00 |
| `cythonpowered.random.random()` | [10K, 100K, 1M] | [1.04, 1.05, 0.97] | 1.02 |
| `cythonpowered.random.n_random()` | [10K, 100K, 1M] | [3.39, 2.35, 2.92] | 2.89 |
| `[Python] random.randint()` | [10K, 100K, 1M] | 1.00 | 1.00 |
| `cythonpowered.random.randint()` | [10K, 100K, 1M] | [6.45, 4.76, 4.48] | 5.23 |
| `cythonpowered.random.n_randint()` | [10K, 100K, 1M] | [30.6, 14.8, 15.2] | 20.2 |
| `[Python] random.uniform()` | [10K, 100K, 1M] | 1.00 | 1.00 |
| `cythonpowered.random.uniform()` | [10K, 100K, 1M] | [1.95, 1.89, 1.90] | 1.91 |
| `cythonpowered.random.n_uniform()` | [10K, 100K, 1M] | [10.9, 7.10, 7.35] | 8.45 |
| `[Python] random.choice()` | [10K, 100K, 1M] | 1.00 | 1.00 |
| `cythonpowered.random.choice()` | [10K, 100K, 1M] | [5.40, 4.68, 4.90] | 5.00 |
| `[Python] random.choices()` | [1K, 10K, 100K] | 1.00 | 1.00 |
| `cythonpowered.random.choices()` | [1K, 10K, 100K] | [1.76, 2.57, 2.00] | 2.11 |

### cythonpowered.dateutil

| Function | Runs | Speed factor | Avg. speedup |
|---|---|---|---|
| `[Python] datetime.date.today()` | [10K, 100K, 1M] | 1.00 | 1.00 |
| `cythonpowered.dateutil.date.today()` | [10K, 100K, 1M] | [1.13, 1.10, 1.08] | 1.11 |
| `[Python] calendar.isleap()` | [10K, 100K, 1M] | 1.00 | 1.00 |
| `cythonpowered.dateutil.date.isleap()` | [10K, 100K, 1M] | [1.70, 1.77, 1.72] | 1.73 |
| `[Python] calendar.monthrange()` | [10K, 100K, 1M] | 1.00 | 1.00 |
| `cythonpowered.dateutil.date.monthrange()` | [10K, 100K, 1M] | [3.51, 1.90, 5.69] | 3.70 |
| `[Python] datetime.datetime.strptime().date()` | [10K, 100K, 1M] | 1.00 | 1.00 |
| `cythonpowered.dateutil.date.fromstring()` | [10K, 100K, 1M] | [10.2, 10.4, 10.3] | 10.3 |
| `[Python] datetime.date().strftime()` | [10K, 100K, 1M] | 1.00 | 1.00 |
| `cythonpowered.dateutil.date().tostring()` | [10K, 100K, 1M] | [17.7, 16.9, 14.8] | 16.5 |
| `[Python] datetime.date().weekday()` | [10K, 100K, 1M] | 1.00 | 1.00 |
| `cythonpowered.dateutil.date().weekday()` | [10K, 100K, 1M] | [1.02, 0.96, 0.97] | 0.98 |
| `[Python] datetime.date().timetuple().tm_yday` | [10K, 100K, 1M] | 1.00 | 1.00 |
| `cythonpowered.dateutil.date().yearday()` | [10K, 100K, 1M] | [6.39, 10.0, 13.0] | 9.80 |
| `[Python] datetime.date.fromordinal()` | [10K, 100K, 1M] | 1.00 | 1.00 |
| `cythonpowered.dateutil.date.fromordinal()` | [10K, 100K, 1M] | [0.74, 0.69, 0.71] | 0.71 |
| `[Python] datetime.date().toordinal()` | [10K, 100K, 1M] | 1.00 | 1.00 |
| `cythonpowered.dateutil.date.toordinal()` | [10K, 100K, 1M] | [0.66, 0.57, 0.62] | 0.62 |
| `[Python] datetime.date() +/- datetime.timedelta()` | [10K, 100K, 1M] | 1.00 | 1.00 |
| `cythonpowered.dateutil.date().offset()` | [10K, 100K, 1M] | [2.86, 2.87, 2.94] | 2.89 |
| `[Python] datetime.date() + datetime.timedelta(days=1)` | [10K, 100K, 1M] | 1.00 | 1.00 |
| `cythonpowered.dateutil.date().increment()` | [10K, 100K, 1M] | [3.41, 3.53, 3.30] | 3.41 |
| `[Python] pandas.date_range()` | [100, 1K, 10K] | 1.00 | 1.00 |
| `cythonpowered.dateutil.date_range()` | [100, 1K, 10K] | [17.0, 14.9, 14.7] | 15.5 |

### cythonpowered.textparse

| Function | Runs | Speed factor | Avg. speedup |
|---|---|---|---|
| `[Python] BeautifulSoup().get_text()` | [100, 1K, 10K] | 1.00 | 1.00 |
| `cythonpowered.textparse.html.get_text()` | [100, 1K, 10K] | [37.9, 38.3, 38.6] | 38.2 |
| `[Python] lxml.html.fromstring().text_content()` | [100, 1K, 10K] | 1.00 | 1.00 |
| `cythonpowered.textparse.html.get_text()` | [100, 1K, 10K] | [3.23, 2.92, 2.86] | 3.01 |
| `[Python] BeautifulSoup().find()` | [100, 1K, 10K] | 1.00 | 1.00 |
| `cythonpowered.textparse.html.find()` | [100, 1K, 10K] | [484.0, 584.5, 590.0] | 552.8 |
| `[Python] lxml.html.fromstring().find()` | [100, 1K, 10K] | 1.00 | 1.00 |
| `cythonpowered.textparse.html.find()` | [100, 1K, 10K] | [42.1, 44.7, 45.1] | 44.0 |
| `[Python] BeautifulSoup().find_all()` | [100, 1K, 10K] | 1.00 | 1.00 |
| `cythonpowered.textparse.html.find_all()` | [100, 1K, 10K] | [358.4, 415.3, 452.7] | 408.8 |
| `[Python] lxml.html.fromstring().findall()` | [100, 1K, 10K] | 1.00 | 1.00 |
| `cythonpowered.textparse.html.find_all()` | [100, 1K, 10K] | [36.2, 30.9, 33.5] | 33.5 |
| `[Python] BeautifulSoup().find().get()` | [100, 1K, 10K] | 1.00 | 1.00 |
| `cythonpowered.textparse.get_attr()` | [100, 1K, 10K] | [521.3, 661.1, 733.7] | 638.7 |
| `[Python] lxml.html.fromstring().find().get()` | [100, 1K, 10K] | 1.00 | 1.00 |
| `cythonpowered.textparse.get_attr()` | [100, 1K, 10K] | [117.2, 97.3, 108.7] | 107.7 |
| `[Python] re.findall(...) implementation to get IPs` | [100, 1K, 10K] | 1.00 | 1.00 |
| `cythonpowered.textparse.get_ips()` | [100, 1K, 10K] | [3.55, 3.57, 3.13] | 3.42 |
| `[Python] re.findall(...) implementation to get emails` | [100, 1K, 10K] | 1.00 | 1.00 |
| `cythonpowered.textparse.get_emails()` | [100, 1K, 10K] | [3.30, 2.96, 2.99] | 3.08 |
| `[Python] re.findall(...) implementation to get MACs` | [100, 1K, 10K] | 1.00 | 1.00 |
| `cythonpowered.textparse.get_mac_addrs()` | [100, 1K, 10K] | [1.75, 1.59, 1.54] | 1.63 |

## Notes

- Benchmarks run on system specs listed above
- Each benchmark is measured at 3 sample sizes (see "Runs" column per table)
- Speed factor = Python time / Cython time (>1 means Cython is faster)
- `date.fromordinal` and `date.toordinal` are faster in Python for this workload
- `textparse` HTML benchmarks compare against both `BeautifulSoup` and `lxml`; the very high factors for `find`/`find_all`/`get_attr` vs. `BeautifulSoup` reflect that the Python reference re-parses the whole document on every call
