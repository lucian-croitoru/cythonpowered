# Cythonpowered Benchmarks

## Notes

- The results below are an **example benchmark** — the output of `cythonpowered --benchmark`, available when installing the `[utils]` extra (`pip install cythonpowered[utils]`)
- Actual results may vary depending on OS, Python version, hardware configuration, or architecture
- Benchmarks run on the system specifications listed below
- Each benchmark is measured at 3 sample sizes (see "Runs" column per table)
- Speed factor (Avg. speedup) = Python time / Cython time (>1 means Cython is faster)
- `date.fromordinal` and `date.toordinal` are faster in Python for their specific workload, but their `cythonpowered.dateutil` counterparts speed up other `cythonpowered.dateutil` functions internally
- `textparse` HTML benchmarks compare against both `BeautifulSoup` and `lxml`; the very high factors for `find`/`find_all` vs. `BeautifulSoup` reflect that the Python reference re-parses the whole document on every call

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

```
+----------------------------------+-----------------+--------------------+--------------+
|          Function name           |   No. of runs   |    Speed factor    | Avg. speedup |
+----------------------------------+-----------------+--------------------+--------------+
|     [Python] random.random()     | [10K, 100K, 1M] |        1.00        |     1.00     |
|  cythonpowered.random.random()   | [10K, 100K, 1M] | [1.04, 1.07, 1.00] |     1.04     |
| cythonpowered.random.n_random()  | [10K, 100K, 1M] | [3.72, 3.00, 3.15] |     3.29     |
+----------------------------------+-----------------+--------------------+--------------+
|    [Python] random.randint()     | [10K, 100K, 1M] |        1.00        |     1.00     |
|  cythonpowered.random.randint()  | [10K, 100K, 1M] | [4.81, 4.98, 4.42] |     4.74     |
| cythonpowered.random.n_randint() | [10K, 100K, 1M] | [21.1, 17.1, 16.1] |     18.1     |
+----------------------------------+-----------------+--------------------+--------------+
|    [Python] random.uniform()     | [10K, 100K, 1M] |        1.00        |     1.00     |
|  cythonpowered.random.uniform()  | [10K, 100K, 1M] | [2.05, 1.87, 1.95] |     1.96     |
| cythonpowered.random.n_uniform() | [10K, 100K, 1M] | [12.1, 7.24, 8.00] |     9.13     |
+----------------------------------+-----------------+--------------------+--------------+
|     [Python] random.choice()     | [10K, 100K, 1M] |        1.00        |     1.00     |
|  cythonpowered.random.choice()   | [10K, 100K, 1M] | [4.91, 4.73, 4.61] |     4.75     |
+----------------------------------+-----------------+--------------------+--------------+
|    [Python] random.choices()     | [1K, 10K, 100K] |        1.00        |     1.00     |
|  cythonpowered.random.choices()  | [1K, 10K, 100K] | [4.46, 2.71, 2.25] |     3.14     |
+----------------------------------+-----------------+--------------------+--------------+
```

### cythonpowered.dateutil

```
+-------------------------------------------------------+-----------------+--------------------+--------------+
|                     Function name                     |   No. of runs   |    Speed factor    | Avg. speedup |
+-------------------------------------------------------+-----------------+--------------------+--------------+
|             [Python] datetime.date.today()            | [10K, 100K, 1M] |        1.00        |     1.00     |
|          cythonpowered.dateutil.date.today()          | [10K, 100K, 1M] | [1.03, 1.11, 1.08] |     1.07     |
+-------------------------------------------------------+-----------------+--------------------+--------------+
|               [Python] calendar.isleap()              | [10K, 100K, 1M] |        1.00        |     1.00     |
|          cythonpowered.dateutil.date.isleap()         | [10K, 100K, 1M] | [2.09, 1.59, 1.73] |     1.80     |
+-------------------------------------------------------+-----------------+--------------------+--------------+
|             [Python] calendar.monthrange()            | [10K, 100K, 1M] |        1.00        |     1.00     |
|        cythonpowered.dateutil.date.monthrange()       | [10K, 100K, 1M] | [3.48, 2.02, 4.84] |     3.45     |
+-------------------------------------------------------+-----------------+--------------------+--------------+
|      [Python] datetime.datetime.strptime().date()     | [10K, 100K, 1M] |        1.00        |     1.00     |
|        cythonpowered.dateutil.date.fromstring()       | [10K, 100K, 1M] | [10.3, 10.2, 10.3] |     10.3     |
+-------------------------------------------------------+-----------------+--------------------+--------------+
|          [Python] datetime.date().strftime()          | [10K, 100K, 1M] |        1.00        |     1.00     |
|        cythonpowered.dateutil.date().tostring()       | [10K, 100K, 1M] | [17.4, 16.2, 15.4] |     16.3     |
+-------------------------------------------------------+-----------------+--------------------+--------------+
|           [Python] datetime.date().weekday()          | [10K, 100K, 1M] |        1.00        |     1.00     |
|        cythonpowered.dateutil.date().weekday()        | [10K, 100K, 1M] | [1.17, 0.92, 0.98] |     1.02     |
+-------------------------------------------------------+-----------------+--------------------+--------------+
|      [Python] datetime.date().timetuple().tm_yday     | [10K, 100K, 1M] |        1.00        |     1.00     |
|        cythonpowered.dateutil.date().yearday()        | [10K, 100K, 1M] | [6.53, 9.23, 11.7] |     9.16     |
+-------------------------------------------------------+-----------------+--------------------+--------------+
|          [Python] datetime.date.fromordinal()         | [10K, 100K, 1M] |        1.00        |     1.00     |
|       cythonpowered.dateutil.date.fromordinal()       | [10K, 100K, 1M] | [0.78, 0.70, 0.72] |     0.73     |
+-------------------------------------------------------+-----------------+--------------------+--------------+
|          [Python] datetime.date().toordinal()         | [10K, 100K, 1M] |        1.00        |     1.00     |
|        cythonpowered.dateutil.date.toordinal()        | [10K, 100K, 1M] | [0.62, 0.56, 0.62] |     0.60     |
+-------------------------------------------------------+-----------------+--------------------+--------------+
|   [Python] datetime.date() +/- datetime.timedelta()   | [10K, 100K, 1M] |        1.00        |     1.00     |
|         cythonpowered.dateutil.date().offset()        | [10K, 100K, 1M] | [2.76, 3.08, 2.91] |     2.92     |
+-------------------------------------------------------+-----------------+--------------------+--------------+
| [Python] datetime.date() + datetime.timedelta(days=1) | [10K, 100K, 1M] |        1.00        |     1.00     |
|       cythonpowered.dateutil.date().increment()       | [10K, 100K, 1M] | [3.36, 3.24, 3.46] |     3.35     |
+-------------------------------------------------------+-----------------+--------------------+--------------+
|              [Python] pandas.date_range()             |  [100, 1K, 10K] |        1.00        |     1.00     |
|          cythonpowered.dateutil.date_range()          |  [100, 1K, 10K] | [16.0, 15.1, 14.7] |     15.2     |
+-------------------------------------------------------+-----------------+--------------------+--------------+
```

### cythonpowered.textparse

```
+-------------------------------------------------------+----------------+-----------------------+--------------+
|                     Function name                     |  No. of runs   |      Speed factor     | Avg. speedup |
+-------------------------------------------------------+----------------+-----------------------+--------------+
|          [Python] BeautifulSoup().get_text()          | [100, 1K, 10K] |          1.00         |     1.00     |
|        cythonpowered.textparse.html.get_text()        | [100, 1K, 10K] |   [30.6, 36.9, 36.2]  |     34.6     |
+-------------------------------------------------------+----------------+-----------------------+--------------+
|     [Python] lxml.html.fromstring().text_content()    | [100, 1K, 10K] |          1.00         |     1.00     |
|        cythonpowered.textparse.html.get_text()        | [100, 1K, 10K] |   [3.10, 2.89, 2.84]  |     2.95     |
+-------------------------------------------------------+----------------+-----------------------+--------------+
|            [Python] BeautifulSoup().find()            | [100, 1K, 10K] |          1.00         |     1.00     |
|          cythonpowered.textparse.html.find()          | [100, 1K, 10K] | [499.9, 578.1, 582.0] |    553.3     |
+-------------------------------------------------------+----------------+-----------------------+--------------+
|         [Python] lxml.html.fromstring().find()        | [100, 1K, 10K] |          1.00         |     1.00     |
|          cythonpowered.textparse.html.find()          | [100, 1K, 10K] |   [45.5, 42.6, 44.1]  |     44.1     |
+-------------------------------------------------------+----------------+-----------------------+--------------+
|          [Python] BeautifulSoup().find_all()          | [100, 1K, 10K] |          1.00         |     1.00     |
|        cythonpowered.textparse.html.find_all()        | [100, 1K, 10K] | [353.0, 434.5, 421.3] |    402.9     |
+-------------------------------------------------------+----------------+-----------------------+--------------+
|       [Python] lxml.html.fromstring().findall()       | [100, 1K, 10K] |          1.00         |     1.00     |
|        cythonpowered.textparse.html.find_all()        | [100, 1K, 10K] |   [37.9, 33.8, 36.3]  |     36.0     |
+-------------------------------------------------------+----------------+-----------------------+--------------+
|            [Python] BeautifulSoup Tag.get()           | [100, 1K, 10K] |          1.00         |     1.00     |
|           cythonpowered.textparse.get_attr()          | [100, 1K, 10K] |   [3.37, 1.15, 1.28]  |     1.93     |
+-------------------------------------------------------+----------------+-----------------------+--------------+
|              [Python] lxml Element.get()              | [100, 1K, 10K] |          1.00         |     1.00     |
|           cythonpowered.textparse.get_attr()          | [100, 1K, 10K] |   [2.71, 1.96, 1.93]  |     2.20     |
+-------------------------------------------------------+----------------+-----------------------+--------------+
|   [Python] re.findall(...) implementation to get IPs  | [100, 1K, 10K] |          1.00         |     1.00     |
|           cythonpowered.textparse.get_ips()           | [100, 1K, 10K] |   [3.54, 3.56, 3.46]  |     3.52     |
+-------------------------------------------------------+----------------+-----------------------+--------------+
| [Python] re.findall(...) implementation to get emails | [100, 1K, 10K] |          1.00         |     1.00     |
|          cythonpowered.textparse.get_emails()         | [100, 1K, 10K] |   [3.22, 3.21, 3.06]  |     3.16     |
+-------------------------------------------------------+----------------+-----------------------+--------------+
|  [Python] re.findall(...) implementation to get MACs  | [100, 1K, 10K] |          1.00         |     1.00     |
|        cythonpowered.textparse.get_mac_addrs()        | [100, 1K, 10K] |   [1.69, 1.64, 1.61]  |     1.65     |
+-------------------------------------------------------+----------------+-----------------------+--------------+
```
