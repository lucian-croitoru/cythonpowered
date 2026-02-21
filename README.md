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
                                                                  ver. 0.2.0

+----+-------------------------------------+------------------------------------------+---------------------------------------------------------------+
|  # | Python function                     | Is replaced by                           | Usage / details                                               |
+----+-------------------------------------+------------------------------------------+---------------------------------------------------------------+
|  1 | random.random()                     | cythonpowered.random.random()            | Drop-in replacement                                           |
|  2 | random.random()                     | cythonpowered.random.n_random()          | n_random(k) replaces [random() for i in range(k)]             |
|  3 | random.randint()                    | cythonpowered.random.randint()           | Drop-in replacement                                           |
|  4 | random.randint()                    | cythonpowered.random.n_randint()         | n_randint(a, b, k) replaces [randint(a, b) for i in range(k)] |
|  5 | random.uniform()                    | cythonpowered.random.uniform()           | Drop-in replacement                                           |
|  6 | random.uniform()                    | cythonpowered.random.n_uniform()         | n_uniform(a, b, k) replaces [uniform(a, b) for i in range(k)] |
|  7 | random.choice()                     | cythonpowered.random.choice()            | Drop-in replacement                                           |
|  8 | random.choices()                    | cythonpowered.random.choices()           | Drop-in replacement, only supports the 'k' keyword argument   |
+----+-------------------------------------+------------------------------------------+---------------------------------------------------------------+
|  9 | datetime.date.today()               | cythonpowered.dateutil.date.today()      | Drop-in replacement                                           |
| 10 | calendar.isleap()                   | cythonpowered.dateutil.date.isleap()     | Drop-in replacement                                           |
| 11 | calendar.monthrange()               | cythonpowered.dateutil.date.monthrange() | Drop-in replacement                                           |
| 12 | datetime.datetime.strptime().date() | cythonpowered.dateutil.date.fromstring() | Assumes '%Y-%m-%d' format, returns cythonpowered date object  |
| 13 | datetime.date().strftime()          | cythonpowered.dateutil.date().tostring() | Assumes '%Y-%m-%d' format, uses cythonpowered date object     |
| 14 | datetime.date().weekday()           | cythonpowered.dateutil.date().weekday()  | Drop-in replacement, uses cythonpowered date object           |
| 15 | datetime.date().timetuple().tm_yday | cythonpowered.dateutil.date().yearday()  | Drop-in replacement, uses cythonpowered date object           |
+----+-------------------------------------+------------------------------------------+---------------------------------------------------------------+
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
                                                                  ver. 0.2.0

CPU model:             11th Gen Intel(R) Core(TM) i7-11370H @ 3.30GHz
CPU base frequency:    3.3000 GHz
CPU cores:             4
CPU threads:           4
Architecture:          x86_64
Memory (RAM):          15.31 GB
Operating System:      Linux 6.8.0-100-generic
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
|  cythonpowered.random.random()   | [10K, 100K, 1M] | [1.11, 0.90, 0.98] |     1.00     |
| cythonpowered.random.n_random()  | [10K, 100K, 1M] | [3.81, 3.75, 2.53] |     3.36     |
+----------------------------------+-----------------+--------------------+--------------+
|    [Python] random.randint()     | [10K, 100K, 1M] |        1.00        |     1.00     |
|  cythonpowered.random.randint()  | [10K, 100K, 1M] | [4.47, 4.81, 4.42] |     4.57     |
| cythonpowered.random.n_randint() | [10K, 100K, 1M] | [23.6, 16.4, 15.7] |     18.6     |
+----------------------------------+-----------------+--------------------+--------------+
|    [Python] random.uniform()     | [10K, 100K, 1M] |        1.00        |     1.00     |
|  cythonpowered.random.uniform()  | [10K, 100K, 1M] | [2.35, 2.23, 2.07] |     2.22     |
| cythonpowered.random.n_uniform() | [10K, 100K, 1M] | [13.7, 8.09, 8.28] |     10.0     |
+----------------------------------+-----------------+--------------------+--------------+
|     [Python] random.choice()     | [10K, 100K, 1M] |        1.00        |     1.00     |
|  cythonpowered.random.choice()   | [10K, 100K, 1M] | [5.11, 4.67, 4.61] |     4.80     |
+----------------------------------+-----------------+--------------------+--------------+
|    [Python] random.choices()     | [1K, 10K, 100K] |        1.00        |     1.00     |
|  cythonpowered.random.choices()  | [1K, 10K, 100K] | [3.58, 2.64, 2.23] |     2.82     |
+----------------------------------+-----------------+--------------------+--------------+

================================================================================
Running benchmark for the [cythonpowered.dateutil] module (7 benchmarks)...
================================================================================
Comparing Python datetime.date.today() with cythonpowered alternative(s)... 100.00%
Comparing Python calendar.isleap() with cythonpowered alternative(s)... 100.00%
Comparing Python calendar.monthrange() with cythonpowered alternative(s)... 100.00%
Comparing Python datetime.datetime.strptime().date() with cythonpowered alternative(s)... 100.00%
Comparing Python datetime.date().strftime() with cythonpowered alternative(s)... 100.00%
Comparing Python datetime.date().weekday() with cythonpowered alternative(s)... 100.00%
Comparing Python datetime.date().timetuple().tm_yday with cythonpowered alternative(s)... 100.00%
+----------------------------------------------+-----------------+--------------------+--------------+
|                Function name                 |   No. of runs   |    Speed factor    | Avg. speedup |
+----------------------------------------------+-----------------+--------------------+--------------+
|        [Python] datetime.date.today()        | [10K, 100K, 1M] |        1.00        |     1.00     |
|     cythonpowered.dateutil.date.today()      | [10K, 100K, 1M] | [1.58, 1.88, 1.84] |     1.77     |
+----------------------------------------------+-----------------+--------------------+--------------+
|          [Python] calendar.isleap()          | [10K, 100K, 1M] |        1.00        |     1.00     |
|     cythonpowered.dateutil.date.isleap()     | [10K, 100K, 1M] | [1.92, 1.81, 1.83] |     1.85     |
+----------------------------------------------+-----------------+--------------------+--------------+
|        [Python] calendar.monthrange()        | [10K, 100K, 1M] |        1.00        |     1.00     |
|   cythonpowered.dateutil.date.monthrange()   | [10K, 100K, 1M] | [8.11, 4.00, 4.64] |     5.59     |
+----------------------------------------------+-----------------+--------------------+--------------+
| [Python] datetime.datetime.strptime().date() | [10K, 100K, 1M] |        1.00        |     1.00     |
|   cythonpowered.dateutil.date.fromstring()   | [10K, 100K, 1M] | [10.2, 10.2, 9.65] |     10.0     |
+----------------------------------------------+-----------------+--------------------+--------------+
|     [Python] datetime.date().strftime()      | [10K, 100K, 1M] |        1.00        |     1.00     |
|   cythonpowered.dateutil.date().tostring()   | [10K, 100K, 1M] | [4.76, 4.46, 4.37] |     4.53     |
+----------------------------------------------+-----------------+--------------------+--------------+
|      [Python] datetime.date().weekday()      | [10K, 100K, 1M] |        1.00        |     1.00     |
|   cythonpowered.dateutil.date().weekday()    | [10K, 100K, 1M] | [1.00, 0.99, 0.98] |     0.99     |
+----------------------------------------------+-----------------+--------------------+--------------+
| [Python] datetime.date().timetuple().tm_yday | [10K, 100K, 1M] |        1.00        |     1.00     |
|   cythonpowered.dateutil.date().yearday()    | [10K, 100K, 1M] | [31.9, 7.20, 11.6] |     16.9     |
+----------------------------------------------+-----------------+--------------------+--------------+
```
---
