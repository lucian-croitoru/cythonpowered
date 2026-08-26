# Cythonpowered Benchmarks

## Notes

- The results below are an **example benchmark** — the output of `cythonpowered --benchmark`, available when installing the `[utils]` extra (`pip install cythonpowered[utils]`)
- Actual results may vary depending on OS, Python version, hardware configuration, or architecture
- Benchmarks run on the system specifications listed below
- Each benchmark is measured at 3 sample sizes (see "Runs" column per table)
- Speed factor (Avg. speedup) = Python time / Cython time (>1 means Cython is faster)
- `date.fromordinal` and `date.toordinal` are faster in Python for their specific workload, but their `cythonpowered.dateutil` counterparts speed up other `cythonpowered.dateutil` functions internally
- `textparse` HTML benchmarks compare against both `BeautifulSoup` and `lxml`; the very high factors for `find`/`find_all`/`get_attr` vs. `BeautifulSoup` reflect that the Python reference re-parses the whole document on every call

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
|  cythonpowered.random.random()   | [10K, 100K, 1M] | [1.04, 0.97, 0.98] |     1.00     |
| cythonpowered.random.n_random()  | [10K, 100K, 1M] | [2.96, 2.73, 2.71] |     2.80     |
+----------------------------------+-----------------+--------------------+--------------+
|    [Python] random.randint()     | [10K, 100K, 1M] |        1.00        |     1.00     |
|  cythonpowered.random.randint()  | [10K, 100K, 1M] | [4.82, 4.37, 4.47] |     4.55     |
| cythonpowered.random.n_randint() | [10K, 100K, 1M] | [19.0, 14.1, 16.0] |     16.4     |
+----------------------------------+-----------------+--------------------+--------------+
|    [Python] random.uniform()     | [10K, 100K, 1M] |        1.00        |     1.00     |
|  cythonpowered.random.uniform()  | [10K, 100K, 1M] | [2.11, 1.84, 1.96] |     1.97     |
| cythonpowered.random.n_uniform() | [10K, 100K, 1M] | [11.0, 5.65, 8.12] |     8.24     |
+----------------------------------+-----------------+--------------------+--------------+
|     [Python] random.choice()     | [10K, 100K, 1M] |        1.00        |     1.00     |
|  cythonpowered.random.choice()   | [10K, 100K, 1M] | [6.26, 4.57, 4.67] |     5.17     |
+----------------------------------+-----------------+--------------------+--------------+
|    [Python] random.choices()     | [1K, 10K, 100K] |        1.00        |     1.00     |
|  cythonpowered.random.choices()  | [1K, 10K, 100K] | [1.85, 2.72, 2.22] |     2.26     |
+----------------------------------+-----------------+--------------------+--------------+
```

### cythonpowered.dateutil

```
+-------------------------------------------------------+-----------------+--------------------+--------------+
|                     Function name                     |   No. of runs   |    Speed factor    | Avg. speedup |
+-------------------------------------------------------+-----------------+--------------------+--------------+
|             [Python] datetime.date.today()            | [10K, 100K, 1M] |        1.00        |     1.00     |
|          cythonpowered.dateutil.date.today()          | [10K, 100K, 1M] | [1.02, 1.09, 1.07] |     1.06     |
+-------------------------------------------------------+-----------------+--------------------+--------------+
|               [Python] calendar.isleap()              | [10K, 100K, 1M] |        1.00        |     1.00     |
|          cythonpowered.dateutil.date.isleap()         | [10K, 100K, 1M] | [1.90, 1.66, 1.75] |     1.77     |
+-------------------------------------------------------+-----------------+--------------------+--------------+
|             [Python] calendar.monthrange()            | [10K, 100K, 1M] |        1.00        |     1.00     |
|        cythonpowered.dateutil.date.monthrange()       | [10K, 100K, 1M] | [3.76, 2.10, 4.83] |     3.56     |
+-------------------------------------------------------+-----------------+--------------------+--------------+
|      [Python] datetime.datetime.strptime().date()     | [10K, 100K, 1M] |        1.00        |     1.00     |
|        cythonpowered.dateutil.date.fromstring()       | [10K, 100K, 1M] | [10.5, 10.3, 10.3] |     10.4     |
+-------------------------------------------------------+-----------------+--------------------+--------------+
|          [Python] datetime.date().strftime()          | [10K, 100K, 1M] |        1.00        |     1.00     |
|        cythonpowered.dateutil.date().tostring()       | [10K, 100K, 1M] | [17.2, 17.0, 15.3] |     16.5     |
+-------------------------------------------------------+-----------------+--------------------+--------------+
|           [Python] datetime.date().weekday()          | [10K, 100K, 1M] |        1.00        |     1.00     |
|        cythonpowered.dateutil.date().weekday()        | [10K, 100K, 1M] | [1.55, 0.92, 0.99] |     1.15     |
+-------------------------------------------------------+-----------------+--------------------+--------------+
|      [Python] datetime.date().timetuple().tm_yday     | [10K, 100K, 1M] |        1.00        |     1.00     |
|        cythonpowered.dateutil.date().yearday()        | [10K, 100K, 1M] | [6.51, 9.33, 12.0] |     9.27     |
+-------------------------------------------------------+-----------------+--------------------+--------------+
|          [Python] datetime.date.fromordinal()         | [10K, 100K, 1M] |        1.00        |     1.00     |
|       cythonpowered.dateutil.date.fromordinal()       | [10K, 100K, 1M] | [0.81, 0.70, 0.72] |     0.74     |
+-------------------------------------------------------+-----------------+--------------------+--------------+
|          [Python] datetime.date().toordinal()         | [10K, 100K, 1M] |        1.00        |     1.00     |
|        cythonpowered.dateutil.date.toordinal()        | [10K, 100K, 1M] | [0.58, 0.57, 0.62] |     0.59     |
+-------------------------------------------------------+-----------------+--------------------+--------------+
|   [Python] datetime.date() +/- datetime.timedelta()   | [10K, 100K, 1M] |        1.00        |     1.00     |
|         cythonpowered.dateutil.date().offset()        | [10K, 100K, 1M] | [2.78, 3.05, 2.99] |     2.94     |
+-------------------------------------------------------+-----------------+--------------------+--------------+
| [Python] datetime.date() + datetime.timedelta(days=1) | [10K, 100K, 1M] |        1.00        |     1.00     |
|       cythonpowered.dateutil.date().increment()       | [10K, 100K, 1M] | [3.67, 3.62, 3.42] |     3.57     |
+-------------------------------------------------------+-----------------+--------------------+--------------+
|              [Python] pandas.date_range()             |  [100, 1K, 10K] |        1.00        |     1.00     |
|          cythonpowered.dateutil.date_range()          |  [100, 1K, 10K] | [12.8, 15.1, 14.5] |     14.1     |
+-------------------------------------------------------+-----------------+--------------------+--------------+
```

### cythonpowered.textparse

```
+-------------------------------------------------------+----------------+-----------------------+--------------+
|                     Function name                     |  No. of runs   |      Speed factor     | Avg. speedup |
+-------------------------------------------------------+----------------+-----------------------+--------------+
|          [Python] BeautifulSoup().get_text()          | [100, 1K, 10K] |          1.00         |     1.00     |
|        cythonpowered.textparse.html.get_text()        | [100, 1K, 10K] |   [36.5, 37.7, 35.9]  |     36.7     |
+-------------------------------------------------------+----------------+-----------------------+--------------+
|     [Python] lxml.html.fromstring().text_content()    | [100, 1K, 10K] |          1.00         |     1.00     |
|        cythonpowered.textparse.html.get_text()        | [100, 1K, 10K] |   [2.89, 2.64, 2.70]  |     2.74     |
+-------------------------------------------------------+----------------+-----------------------+--------------+
|            [Python] BeautifulSoup().find()            | [100, 1K, 10K] |          1.00         |     1.00     |
|          cythonpowered.textparse.html.find()          | [100, 1K, 10K] | [405.5, 578.5, 576.6] |    520.2     |
+-------------------------------------------------------+----------------+-----------------------+--------------+
|         [Python] lxml.html.fromstring().find()        | [100, 1K, 10K] |          1.00         |     1.00     |
|          cythonpowered.textparse.html.find()          | [100, 1K, 10K] |   [35.5, 39.4, 42.5]  |     39.1     |
+-------------------------------------------------------+----------------+-----------------------+--------------+
|          [Python] BeautifulSoup().find_all()          | [100, 1K, 10K] |          1.00         |     1.00     |
|        cythonpowered.textparse.html.find_all()        | [100, 1K, 10K] | [318.8, 429.6, 421.4] |    389.9     |
+-------------------------------------------------------+----------------+-----------------------+--------------+
|       [Python] lxml.html.fromstring().findall()       | [100, 1K, 10K] |          1.00         |     1.00     |
|        cythonpowered.textparse.html.find_all()        | [100, 1K, 10K] |   [22.7, 20.9, 35.7]  |     26.4     |
+-------------------------------------------------------+----------------+-----------------------+--------------+
|         [Python] BeautifulSoup().find().get()         | [100, 1K, 10K] |          1.00         |     1.00     |
|           cythonpowered.textparse.get_attr()          | [100, 1K, 10K] | [533.5, 672.6, 749.9] |    652.0     |
+-------------------------------------------------------+----------------+-----------------------+--------------+
|      [Python] lxml.html.fromstring().find().get()     | [100, 1K, 10K] |          1.00         |     1.00     |
|           cythonpowered.textparse.get_attr()          | [100, 1K, 10K] |  [97.3, 83.5, 105.3]  |     95.3     |
+-------------------------------------------------------+----------------+-----------------------+--------------+
|   [Python] re.findall(...) implementation to get IPs  | [100, 1K, 10K] |          1.00         |     1.00     |
|           cythonpowered.textparse.get_ips()           | [100, 1K, 10K] |   [3.39, 3.61, 3.12]  |     3.37     |
+-------------------------------------------------------+----------------+-----------------------+--------------+
| [Python] re.findall(...) implementation to get emails | [100, 1K, 10K] |          1.00         |     1.00     |
|          cythonpowered.textparse.get_emails()         | [100, 1K, 10K] |   [3.16, 3.13, 3.13]  |     3.14     |
+-------------------------------------------------------+----------------+-----------------------+--------------+
|  [Python] re.findall(...) implementation to get MACs  | [100, 1K, 10K] |          1.00         |     1.00     |
|        cythonpowered.textparse.get_mac_addrs()        | [100, 1K, 10K] |   [1.75, 1.71, 1.64]  |     1.70     |
+-------------------------------------------------------+----------------+-----------------------+--------------+
```