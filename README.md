# Cython-powered replacements for popular Python functions. And more.

`cythonpowered` is a library containing **replacements** for various `Python` functions,
that are generated with `Cython` and **compiled at setup**, intended to provide **performance gains** for developers.

Some functions are **drop-in replacements**, others are provided to **enhance** certain usages of the respective functions, or have slightly different implementations.

## Installation
`pip install cythonpowered`

## Usage
Simply **import** the desired function and use it in your `Python` code.

Run `cythonpowered --list` to view all available functions and their `Python` conunterparts.
#### Currently available functions:
```
               _   _                                                      _ 
     ___ _   _| |_| |__   ___  _ __  _ __   _____      _____ _ __ ___  __| |
    / __| | | | __| '_ \ / _ \| '_ \| '_ \ / _ \ \ /\ / / _ \ '__/ _ \/ _` |
   | (__| |_| | |_| | | | (_) | | | | |_) | (_) \ V  V /  __/ | |  __/ (_| |
    \___|\__, |\__|_| |_|\___/|_| |_| .__/ \___/ \_/\_/ \___|_|  \___|\__,_|
         |___/                      |_|                                     
                                                                  ver. 0.2.3

+----+----------------------------------------------+-------------------------------------------+----------------------------------------------------------------------------+
|  # | Python function                              | Is replaced by                            | Usage / details                                                            |
+----+----------------------------------------------+-------------------------------------------+----------------------------------------------------------------------------+
|  1 | random.random()                              | cythonpowered.random.random()             | Drop-in replacement                                                        |
|  2 | random.random()                              | cythonpowered.random.n_random()           | n_random(k) replaces [random() for i in range(k)]                          |
|  3 | random.randint()                             | cythonpowered.random.randint()            | Drop-in replacement                                                        |
|  4 | random.randint()                             | cythonpowered.random.n_randint()          | n_randint(a, b, k) replaces [randint(a, b) for i in range(k)]              |
|  5 | random.uniform()                             | cythonpowered.random.uniform()            | Drop-in replacement                                                        |
|  6 | random.uniform()                             | cythonpowered.random.n_uniform()          | n_uniform(a, b, k) replaces [uniform(a, b) for i in range(k)]              |
|  7 | random.choice()                              | cythonpowered.random.choice()             | Drop-in replacement                                                        |
|  8 | random.choices()                             | cythonpowered.random.choices()            | Drop-in replacement, only supports the 'k' keyword argument                |
+----+----------------------------------------------+-------------------------------------------+----------------------------------------------------------------------------+
|  9 | datetime.date.today()                        | cythonpowered.dateutil.date.today()       | Drop-in replacement, returns cythonpowered date object                     |
| 10 | calendar.isleap()                            | cythonpowered.dateutil.date.isleap()      | Drop-in replacement                                                        |
| 11 | calendar.monthrange()                        | cythonpowered.dateutil.date.monthrange()  | Drop-in replacement                                                        |
| 12 | datetime.datetime.strptime().date()          | cythonpowered.dateutil.date.fromstring()  | Assumes '%Y-%m-%d' format, returns cythonpowered date object               |
| 13 | datetime.date().strftime()                   | cythonpowered.dateutil.date().tostring()  | Assumes '%Y-%m-%d' format, uses cythonpowered date object                  |
| 14 | datetime.date().weekday()                    | cythonpowered.dateutil.date().weekday()   | Drop-in replacement, uses cythonpowered date object                        |
| 15 | datetime.date().timetuple().tm_yday          | cythonpowered.dateutil.date().yearday()   | Drop-in replacement, uses cythonpowered date object                        |
| 16 | datetime.date.fromordinal()                  | cythonpowered.dateutil.date.fromordinal() | Drop-in replacement, returns cythonpowered date object                     |
| 17 | datetime.date().toordinal()                  | cythonpowered.dateutil.date().toordinal() | Drop-in replacement, uses cythonpowered date object                        |
| 18 | datetime.date() +/- datetime.timedelta()     | cythonpowered.dateutil.date().offset()    | Supports days/weeks/months/years offset, returns cythonpowered date object |
| 19 | datetime.date() + datetime.timedelta(days=1) | cythonpowered.dateutil.date().increment() | Increments cythonpowered date object by 1 day                              |
| 20 | pandas.date_range()                          | cythonpowered.dateutil.date_range()       | Uses cythonpowered date object, returns a list of date strings             |
+----+----------------------------------------------+-------------------------------------------+----------------------------------------------------------------------------+
```

## Benchmark
Run `cythonpowered --benchmark` o view the performance gains **on your system** for all `cythonpowered` functions, compared to their `Python` counterparts.
#### Example benchmark output:
```
               _   _                                                      _ 
     ___ _   _| |_| |__   ___  _ __  _ __   _____      _____ _ __ ___  __| |
    / __| | | | __| '_ \ / _ \| '_ \| '_ \ / _ \ \ /\ / / _ \ '__/ _ \/ _` |
   | (__| |_| | |_| | | | (_) | | | | |_) | (_) \ V  V /  __/ | |  __/ (_| |
    \___|\__, |\__|_| |_|\___/|_| |_| .__/ \___/ \_/\_/ \___|_|  \___|\__,_|
         |___/                      |_|                                     
                                                                  ver. 0.2.3

CPU model:             11th Gen Intel(R) Core(TM) i7-11370H @ 3.30GHz
CPU base frequency:    3.3000 GHz
CPU cores:             4
CPU threads:           4
Architecture:          x86_64
Memory (RAM):          15.31 GB
Operating System:      Linux 6.8.0-106-generic
Python version:        3.12.3
C compiler:            GCC 13.3.0

================================================================================
Running benchmark for the [cythonpowered.random] module (5 benchmarks)...
================================================================================
Comparing Python random.random() with cythonpowered alternative(s)... 100.00%
Comparing Python random.randint() with cythonpowered alternative(s)... 100.00%
Comparing Python random.uniform() with cythonpowered alternative(s)... 100.00%
Comparing Python random.choice() with cythonpowered alternative(s)... 100.00%
Comparing Python random.choices() with cythonpowered alternative(s)... 100.00%
+----------------------------------+-----------------+--------------------+--------------+
|          Function name           |   No. of runs   |    Speed factor    | Avg. speedup |
+----------------------------------+-----------------+--------------------+--------------+
|     [Python] random.random()     | [10K, 100K, 1M] |        1.00        |     1.00     |
|  cythonpowered.random.random()   | [10K, 100K, 1M] | [1.02, 0.99, 0.98] |     1.00     |
| cythonpowered.random.n_random()  | [10K, 100K, 1M] | [3.06, 2.73, 2.83] |     2.88     |
+----------------------------------+-----------------+--------------------+--------------+
|    [Python] random.randint()     | [10K, 100K, 1M] |        1.00        |     1.00     |
|  cythonpowered.random.randint()  | [10K, 100K, 1M] | [4.96, 4.40, 4.99] |     4.78     |
| cythonpowered.random.n_randint() | [10K, 100K, 1M] | [24.3, 15.9, 17.1] |     19.1     |
+----------------------------------+-----------------+--------------------+--------------+
|    [Python] random.uniform()     | [10K, 100K, 1M] |        1.00        |     1.00     |
|  cythonpowered.random.uniform()  | [10K, 100K, 1M] | [2.18, 2.04, 2.03] |     2.08     |
| cythonpowered.random.n_uniform() | [10K, 100K, 1M] | [11.6, 7.43, 6.90] |     8.65     |
+----------------------------------+-----------------+--------------------+--------------+
|     [Python] random.choice()     | [10K, 100K, 1M] |        1.00        |     1.00     |
|  cythonpowered.random.choice()   | [10K, 100K, 1M] | [4.89, 4.84, 4.81] |     4.85     |
+----------------------------------+-----------------+--------------------+--------------+
|    [Python] random.choices()     | [1K, 10K, 100K] |        1.00        |     1.00     |
|  cythonpowered.random.choices()  | [1K, 10K, 100K] | [2.75, 2.61, 2.19] |     2.52     |
+----------------------------------+-----------------+--------------------+--------------+

================================================================================
Running benchmark for the [cythonpowered.dateutil] module (12 benchmarks)...
================================================================================
Comparing Python datetime.date.today() with cythonpowered alternative(s)... 100.00%
Comparing Python calendar.isleap() with cythonpowered alternative(s)... 100.00%
Comparing Python calendar.monthrange() with cythonpowered alternative(s)... 100.00%
Comparing Python datetime.datetime.strptime().date() with cythonpowered alternative(s)... 100.00%
Comparing Python datetime.date().strftime() with cythonpowered alternative(s)... 100.00%
Comparing Python datetime.date().weekday() with cythonpowered alternative(s)... 100.00%
Comparing Python datetime.date().timetuple().tm_yday with cythonpowered alternative(s)... 100.00%
Comparing Python datetime.date.fromordinal() with cythonpowered alternative(s)... 100.00%
Comparing Python datetime.date().toordinal() with cythonpowered alternative(s)... 100.00%
Comparing Python datetime.date() +/- datetime.timedelta() with cythonpowered alternative(s)... 100.00%
Comparing Python datetime.date() + datetime.timedelta(days=1) with cythonpowered alternative(s)... 100.00%
Comparing Python pandas.date_range() with cythonpowered alternative(s)... 100.00%
+-------------------------------------------------------+-----------------+--------------------+--------------+
|                     Function name                     |   No. of runs   |    Speed factor    | Avg. speedup |
+-------------------------------------------------------+-----------------+--------------------+--------------+
|             [Python] datetime.date.today()            | [10K, 100K, 1M] |        1.00        |     1.00     |
|          cythonpowered.dateutil.date.today()          | [10K, 100K, 1M] | [1.92, 1.83, 2.02] |     1.92     |
+-------------------------------------------------------+-----------------+--------------------+--------------+
|               [Python] calendar.isleap()              | [10K, 100K, 1M] |        1.00        |     1.00     |
|          cythonpowered.dateutil.date.isleap()         | [10K, 100K, 1M] | [1.98, 1.70, 1.56] |     1.74     |
+-------------------------------------------------------+-----------------+--------------------+--------------+
|             [Python] calendar.monthrange()            | [10K, 100K, 1M] |        1.00        |     1.00     |
|        cythonpowered.dateutil.date.monthrange()       | [10K, 100K, 1M] | [3.23, 1.82, 4.53] |     3.19     |
+-------------------------------------------------------+-----------------+--------------------+--------------+
|      [Python] datetime.datetime.strptime().date()     | [10K, 100K, 1M] |        1.00        |     1.00     |
|        cythonpowered.dateutil.date.fromstring()       | [10K, 100K, 1M] | [10.8, 10.4, 10.2] |     10.5     |
+-------------------------------------------------------+-----------------+--------------------+--------------+
|          [Python] datetime.date().strftime()          | [10K, 100K, 1M] |        1.00        |     1.00     |
|        cythonpowered.dateutil.date().tostring()       | [10K, 100K, 1M] | [19.3, 16.6, 15.8] |     17.2     |
+-------------------------------------------------------+-----------------+--------------------+--------------+
|           [Python] datetime.date().weekday()          | [10K, 100K, 1M] |        1.00        |     1.00     |
|        cythonpowered.dateutil.date().weekday()        | [10K, 100K, 1M] | [1.08, 0.97, 0.97] |     1.01     |
+-------------------------------------------------------+-----------------+--------------------+--------------+
|      [Python] datetime.date().timetuple().tm_yday     | [10K, 100K, 1M] |        1.00        |     1.00     |
|        cythonpowered.dateutil.date().yearday()        | [10K, 100K, 1M] | [6.76, 8.47, 11.2] |     8.82     |
+-------------------------------------------------------+-----------------+--------------------+--------------+
|          [Python] datetime.date.fromordinal()         | [10K, 100K, 1M] |        1.00        |     1.00     |
|       cythonpowered.dateutil.date.fromordinal()       | [10K, 100K, 1M] | [0.69, 0.68, 0.69] |     0.69     |
+-------------------------------------------------------+-----------------+--------------------+--------------+
|          [Python] datetime.date().toordinal()         | [10K, 100K, 1M] |        1.00        |     1.00     |
|       cythonpowered.dateutil.date().toordinal()       | [10K, 100K, 1M] | [0.58, 0.57, 0.56] |     0.57     |
+-------------------------------------------------------+-----------------+--------------------+--------------+
|   [Python] datetime.date() +/- datetime.timedelta()   | [10K, 100K, 1M] |        1.00        |     1.00     |
|         cythonpowered.dateutil.date().offset()        | [10K, 100K, 1M] | [3.02, 2.70, 2.78] |     2.83     |
+-------------------------------------------------------+-----------------+--------------------+--------------+
| [Python] datetime.date() + datetime.timedelta(days=1) | [10K, 100K, 1M] |        1.00        |     1.00     |
|       cythonpowered.dateutil.date().increment()       | [10K, 100K, 1M] | [3.48, 3.24, 3.21] |     3.31     |
+-------------------------------------------------------+-----------------+--------------------+--------------+
|              [Python] pandas.date_range()             |  [100, 1K, 10K] |        1.00        |     1.00     |
|          cythonpowered.dateutil.date_range()          |  [100, 1K, 10K] | [16.5, 15.6, 14.5] |     15.5     |
+-------------------------------------------------------+-----------------+--------------------+--------------+
```
---
