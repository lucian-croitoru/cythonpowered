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
|  cythonpowered.random.random()   | [10K, 100K, 1M] | [1.11, 1.11, 1.07] |     1.10     |
| cythonpowered.random.n_random()  | [10K, 100K, 1M] | [3.70, 4.01, 3.77] |     3.83     |
+----------------------------------+-----------------+--------------------+--------------+
|    [Python] random.randint()     | [10K, 100K, 1M] |        1.00        |     1.00     |
|  cythonpowered.random.randint()  | [10K, 100K, 1M] | [5.50, 4.64, 4.83] |     4.99     |
| cythonpowered.random.n_randint() | [10K, 100K, 1M] | [34.5, 18.7, 19.9] |     24.4     |
+----------------------------------+-----------------+--------------------+--------------+
|    [Python] random.uniform()     | [10K, 100K, 1M] |        1.00        |     1.00     |
|  cythonpowered.random.uniform()  | [10K, 100K, 1M] | [2.34, 2.03, 2.04] |     2.13     |
| cythonpowered.random.n_uniform() | [10K, 100K, 1M] | [15.8, 9.59, 9.82] |     11.7     |
+----------------------------------+-----------------+--------------------+--------------+
|     [Python] random.choice()     | [10K, 100K, 1M] |        1.00        |     1.00     |
|  cythonpowered.random.choice()   | [10K, 100K, 1M] | [6.15, 4.84, 5.59] |     5.53     |
+----------------------------------+-----------------+--------------------+--------------+
|    [Python] random.choices()     | [1K, 10K, 100K] |        1.00        |     1.00     |
|  cythonpowered.random.choices()  | [1K, 10K, 100K] | [4.82, 3.66, 2.64] |     3.70     |
+----------------------------------+-----------------+--------------------+--------------+
```

### cythonpowered.dateutil

```
+-------------------------------------------------------+-----------------+--------------------+--------------+
|                     Function name                     |   No. of runs   |    Speed factor    | Avg. speedup |
+-------------------------------------------------------+-----------------+--------------------+--------------+
|             [Python] datetime.date.today()            | [10K, 100K, 1M] |        1.00        |     1.00     |
|          cythonpowered.dateutil.date.today()          | [10K, 100K, 1M] | [1.17, 1.16, 1.14] |     1.15     |
+-------------------------------------------------------+-----------------+--------------------+--------------+
|               [Python] calendar.isleap()              | [10K, 100K, 1M] |        1.00        |     1.00     |
|          cythonpowered.dateutil.date.isleap()         | [10K, 100K, 1M] | [1.85, 1.62, 1.62] |     1.70     |
+-------------------------------------------------------+-----------------+--------------------+--------------+
|             [Python] calendar.monthrange()            | [10K, 100K, 1M] |        1.00        |     1.00     |
|        cythonpowered.dateutil.date.monthrange()       | [10K, 100K, 1M] | [4.34, 2.21, 5.74] |     4.10     |
+-------------------------------------------------------+-----------------+--------------------+--------------+
|      [Python] datetime.datetime.strptime().date()     | [10K, 100K, 1M] |        1.00        |     1.00     |
|        cythonpowered.dateutil.date.fromstring()       | [10K, 100K, 1M] | [11.1, 11.0, 10.8] |     11.0     |
+-------------------------------------------------------+-----------------+--------------------+--------------+
|          [Python] datetime.date().strftime()          | [10K, 100K, 1M] |        1.00        |     1.00     |
|        cythonpowered.dateutil.date().tostring()       | [10K, 100K, 1M] | [19.1, 16.0, 15.1] |     16.7     |
+-------------------------------------------------------+-----------------+--------------------+--------------+
|           [Python] datetime.date().weekday()          | [10K, 100K, 1M] |        1.00        |     1.00     |
|        cythonpowered.dateutil.date().weekday()        | [10K, 100K, 1M] | [3.56, 0.68, 1.01] |     1.75     |
+-------------------------------------------------------+-----------------+--------------------+--------------+
|      [Python] datetime.date().timetuple().tm_yday     | [10K, 100K, 1M] |        1.00        |     1.00     |
|        cythonpowered.dateutil.date().yearday()        | [10K, 100K, 1M] | [12.2, 15.7, 20.3] |     16.1     |
+-------------------------------------------------------+-----------------+--------------------+--------------+
|          [Python] datetime.date.fromordinal()         | [10K, 100K, 1M] |        1.00        |     1.00     |
|       cythonpowered.dateutil.date.fromordinal()       | [10K, 100K, 1M] | [1.08, 0.81, 0.81] |     0.90     |
+-------------------------------------------------------+-----------------+--------------------+--------------+
|          [Python] datetime.date().toordinal()         | [10K, 100K, 1M] |        1.00        |     1.00     |
|        cythonpowered.dateutil.date.toordinal()        | [10K, 100K, 1M] | [1.06, 0.93, 0.99] |     0.99     |
+-------------------------------------------------------+-----------------+--------------------+--------------+
|   [Python] datetime.date() +/- datetime.timedelta()   | [10K, 100K, 1M] |        1.00        |     1.00     |
|         cythonpowered.dateutil.date().offset()        | [10K, 100K, 1M] | [3.57, 3.61, 3.58] |     3.58     |
+-------------------------------------------------------+-----------------+--------------------+--------------+
| [Python] datetime.date() + datetime.timedelta(days=1) | [10K, 100K, 1M] |        1.00        |     1.00     |
|       cythonpowered.dateutil.date().increment()       | [10K, 100K, 1M] | [6.79, 7.74, 7.21] |     7.25     |
+-------------------------------------------------------+-----------------+--------------------+--------------+
|              [Python] pandas.date_range()             |  [100, 1K, 10K] |        1.00        |     1.00     |
|          cythonpowered.dateutil.date_range()          |  [100, 1K, 10K] | [46.5, 42.5, 21.1] |     36.7     |
+-------------------------------------------------------+-----------------+--------------------+--------------+
```

### cythonpowered.textparse

```
+-------------------------------------------------------+----------------+-----------------------+--------------+
|                     Function name                     |  No. of runs   |      Speed factor     | Avg. speedup |
+-------------------------------------------------------+----------------+-----------------------+--------------+
|          [Python] BeautifulSoup().get_text()          | [100, 1K, 10K] |          1.00         |     1.00     |
|        cythonpowered.textparse.html.get_text()        | [100, 1K, 10K] | [147.0, 158.9, 160.0] |    155.3     |
+-------------------------------------------------------+----------------+-----------------------+--------------+
|     [Python] lxml.html.fromstring().text_content()    | [100, 1K, 10K] |          1.00         |     1.00     |
|        cythonpowered.textparse.html.get_text()        | [100, 1K, 10K] |   [11.8, 12.6, 12.5]  |     12.3     |
+-------------------------------------------------------+----------------+-----------------------+--------------+
|            [Python] BeautifulSoup().find()            | [100, 1K, 10K] |          1.00         |     1.00     |
|          cythonpowered.textparse.html.find()          | [100, 1K, 10K] | [457.2, 462.8, 411.7] |    443.9     |
+-------------------------------------------------------+----------------+-----------------------+--------------+
|         [Python] lxml.html.fromstring().find()        | [100, 1K, 10K] |          1.00         |     1.00     |
|          cythonpowered.textparse.html.find()          | [100, 1K, 10K] |   [34.2, 24.9, 32.7]  |     30.6     |
+-------------------------------------------------------+----------------+-----------------------+--------------+
|          [Python] BeautifulSoup().find_all()          | [100, 1K, 10K] |          1.00         |     1.00     |
|        cythonpowered.textparse.html.find_all()        | [100, 1K, 10K] | [263.9, 343.9, 110.6] |    239.5     |
+-------------------------------------------------------+----------------+-----------------------+--------------+
|       [Python] lxml.html.fromstring().findall()       | [100, 1K, 10K] |          1.00         |     1.00     |
|        cythonpowered.textparse.html.find_all()        | [100, 1K, 10K] |   [22.0, 25.9, 22.7]  |     23.5     |
+-------------------------------------------------------+----------------+-----------------------+--------------+
|            [Python] BeautifulSoup Tag.get()           | [100, 1K, 10K] |          1.00         |     1.00     |
|        cythonpowered.textparse.html.get_attr()        | [100, 1K, 10K] |   [2.35, 1.40, 1.35]  |     1.70     |
+-------------------------------------------------------+----------------+-----------------------+--------------+
|              [Python] lxml Element.get()              | [100, 1K, 10K] |          1.00         |     1.00     |
|        cythonpowered.textparse.html.get_attr()        | [100, 1K, 10K] |   [4.83, 2.10, 1.81]  |     2.92     |
+-------------------------------------------------------+----------------+-----------------------+--------------+
|   [Python] re.findall(...) implementation to get IPs  | [100, 1K, 10K] |          1.00         |     1.00     |
|           cythonpowered.textparse.get_ips()           | [100, 1K, 10K] |   [17.7, 16.0, 15.1]  |     16.3     |
+-------------------------------------------------------+----------------+-----------------------+--------------+
| [Python] re.findall(...) implementation to get emails | [100, 1K, 10K] |          1.00         |     1.00     |
|          cythonpowered.textparse.get_emails()         | [100, 1K, 10K] |   [10.8, 8.52, 7.91]  |     9.06     |
+-------------------------------------------------------+----------------+-----------------------+--------------+
|  [Python] re.findall(...) implementation to get MACs  | [100, 1K, 10K] |          1.00         |     1.00     |
|        cythonpowered.textparse.get_mac_addrs()        | [100, 1K, 10K] |   [5.66, 4.72, 4.52]  |     4.97     |
+-------------------------------------------------------+----------------+-----------------------+--------------+
```
