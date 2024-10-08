# Cython-powered replacements for popular Python functions. And more.

`cythonpowered` is a library containing **replacements** for various `Python` functions,
that are generated with `Cython` and **compiled at setup**, intended to provide **performance gains** for developers.

Some functions are **drop-in replacements**, others are provided to **enhance** certain usages of the respective functions.

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
                                                                  ver. 0.1.10

+---+--------------------------------+----------------------------+-----------------------------------------------------------------------+
| # | [cythonpowered] function       | Replaces [Python] function | Usage / details                                                       |
+---+--------------------------------+----------------------------+-----------------------------------------------------------------------+
| 1 | cythonpowered.random.random    | random.random              | Drop-in replacement                                                   |
| 2 | cythonpowered.random.n_random  | random.random              | n_random(k) is equivalent to [random() for i in range(k)]             |
| 3 | cythonpowered.random.randint   | random.randint             | Drop-in replacement                                                   |
| 4 | cythonpowered.random.n_randint | random.randint             | n_randint(a, b, k) is equivalent to [randint(a, b) for i in range(k)] |
| 5 | cythonpowered.random.uniform   | random.uniform             | Drop-in replacement                                                   |
| 6 | cythonpowered.random.n_uniform | random.uniform             | n_uniform(a, b, k) is equivalent to [uniform(a, b) for i in range(k)] |
| 7 | cythonpowered.random.choice    | random.choice              | Drop-in replacement                                                   |
| 8 | cythonpowered.random.choices   | random.choices             | Drop-in replacement, only supports the 'k' keyword argument           |
+---+--------------------------------+----------------------------+-----------------------------------------------------------------------+
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
                                                                  ver. 0.1.10

CPU model:             11th Gen Intel(R) Core(TM) i7-11370H @ 3.30GHz
CPU base frequency:    3.3000 GHz
CPU cores:             4
CPU threads:           4
Architecture:          x86_64
Memory (RAM):          15.31 GB
Operating System:      Linux 6.8.0-45-generic
Python version:        3.10.12
C compiler:            GCC 11.4.0

================================================================================
Running benchmark for the [cythonpowered.random] module (5 benchmarks)...
================================================================================
Comparing [random.random] with [cythonpowered.random.random] and [cythonpowered.random.n_random]... 100.00%
Comparing [random.randint] with [cythonpowered.random.randint] and [cythonpowered.random.n_randint]... 100.00%
Comparing [random.uniform] with [cythonpowered.random.uniform] and [cythonpowered.random.n_uniform]... 100.00%
Comparing [random.choice] with [cythonpowered.random.choice]... 100.00%
Comparing [random.choices] with [cythonpowered.random.choices]... 100.00%
+--------------------------------+-----------------+-----------------------+--------------------+--------------------+-------------------+
|         Function name          |   No. of runs   |   Execution time (s)  |    Time factor     |    Speed factor    | Avg. speed factor |
+--------------------------------+-----------------+-----------------------+--------------------+--------------------+-------------------+
|     [Python] random.random     | [10K, 100K, 1M] | [0.0007, 0.006, 0.06] |        1.00        |        1.00        |        1.00       |
|  cythonpowered.random.random   | [10K, 100K, 1M] | [0.0006, 0.006, 0.06] | [0.91, 0.95, 0.97] | [1.10, 1.05, 1.03] |        1.06       |
| cythonpowered.random.n_random  | [10K, 100K, 1M] | [0.0002, 0.002, 0.02] | [0.29, 0.32, 0.29] | [3.45, 3.16, 3.47] |        3.36       |
+--------------------------------+-----------------+-----------------------+--------------------+--------------------+-------------------+
|    [Python] random.randint     | [10K, 100K, 1M] | [0.0044, 0.043, 0.43] |        1.00        |        1.00        |        1.00       |
|  cythonpowered.random.randint  | [10K, 100K, 1M] | [0.0007, 0.008, 0.08] | [0.16, 0.18, 0.18] | [6.15, 5.65, 5.46] |        5.75       |
| cythonpowered.random.n_randint | [10K, 100K, 1M] | [0.0002, 0.003, 0.03] | [0.04, 0.07, 0.07] | [23.1, 14.7, 15.1] |        17.6       |
+--------------------------------+-----------------+-----------------------+--------------------+--------------------+-------------------+
|    [Python] random.uniform     | [10K, 100K, 1M] | [0.0015, 0.014, 0.15] |        1.00        |        1.00        |        1.00       |
|  cythonpowered.random.uniform  | [10K, 100K, 1M] | [0.0006, 0.007, 0.07] | [0.41, 0.46, 0.45] | [2.44, 2.19, 2.23] |        2.29       |
| cythonpowered.random.n_uniform | [10K, 100K, 1M] | [0.0001, 0.002, 0.02] | [0.07, 0.13, 0.11] | [14.2, 7.79, 8.74] |        10.3       |
+--------------------------------+-----------------+-----------------------+--------------------+--------------------+-------------------+
|     [Python] random.choice     | [10K, 100K, 1M] | [0.0033, 0.028, 0.28] |        1.00        |        1.00        |        1.00       |
|  cythonpowered.random.choice   | [10K, 100K, 1M] | [0.0006, 0.006, 0.06] | [0.18, 0.21, 0.21] | [5.51, 4.80, 4.71] |        5.01       |
+--------------------------------+-----------------+-----------------------+--------------------+--------------------+-------------------+
|    [Python] random.choices     | [1K, 10K, 100K] | [0.0080, 0.074, 0.75] |        1.00        |        1.00        |        1.00       |
|  cythonpowered.random.choices  | [1K, 10K, 100K] | [0.0032, 0.035, 0.39] | [0.40, 0.47, 0.52] | [2.48, 2.13, 1.94] |        2.18       |
+--------------------------------+-----------------+-----------------------+--------------------+--------------------+-------------------+
```
---
