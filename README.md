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
                                                                  ver. 0.1.11

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
                                                                  ver. 0.1.11

CPU model:             11th Gen Intel(R) Core(TM) i7-11370H @ 3.30GHz
CPU base frequency:    3.3000 GHz
CPU cores:             4
CPU threads:           4
Architecture:          x86_64
Memory (RAM):          15.31 GB
Operating System:      Linux 6.8.0-90-generic
Python version:        3.12.3
C compiler:            GCC 13.3.0

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
|  cythonpowered.random.random   | [10K, 100K, 1M] | [0.0007, 0.006, 0.06] | [0.94, 0.95, 0.97] | [1.07, 1.05, 1.03] |        1.05       |
| cythonpowered.random.n_random  | [10K, 100K, 1M] | [0.0002, 0.002, 0.02] | [0.30, 0.32, 0.33] | [3.33, 3.10, 3.07] |        3.17       |
+--------------------------------+-----------------+-----------------------+--------------------+--------------------+-------------------+
|    [Python] random.randint     | [10K, 100K, 1M] | [0.0041, 0.040, 0.39] |        1.00        |        1.00        |        1.00       |
|  cythonpowered.random.randint  | [10K, 100K, 1M] | [0.0008, 0.009, 0.08] | [0.18, 0.23, 0.21] | [5.48, 4.42, 4.69] |        4.86       |
| cythonpowered.random.n_randint | [10K, 100K, 1M] | [0.0002, 0.003, 0.03] | [0.04, 0.06, 0.06] | [25.0, 15.9, 15.6] |        18.8       |
+--------------------------------+-----------------+-----------------------+--------------------+--------------------+-------------------+
|    [Python] random.uniform     | [10K, 100K, 1M] | [0.0016, 0.025, 0.20] |        1.00        |        1.00        |        1.00       |
|  cythonpowered.random.uniform  | [10K, 100K, 1M] | [0.0007, 0.014, 0.08] | [0.44, 0.55, 0.40] | [2.27, 1.83, 2.49] |        2.20       |
| cythonpowered.random.n_uniform | [10K, 100K, 1M] | [0.0001, 0.005, 0.02] | [0.09, 0.20, 0.10] | [11.4, 4.98, 9.56] |        8.65       |
+--------------------------------+-----------------+-----------------------+--------------------+--------------------+-------------------+
|     [Python] random.choice     | [10K, 100K, 1M] | [0.0034, 0.032, 0.30] |        1.00        |        1.00        |        1.00       |
|  cythonpowered.random.choice   | [10K, 100K, 1M] | [0.0007, 0.007, 0.06] | [0.19, 0.21, 0.21] | [5.20, 4.74, 4.73] |        4.89       |
+--------------------------------+-----------------+-----------------------+--------------------+--------------------+-------------------+
|    [Python] random.choices     | [1K, 10K, 100K] | [0.0062, 0.062, 0.63] |        1.00        |        1.00        |        1.00       |
|  cythonpowered.random.choices  | [1K, 10K, 100K] | [0.0019, 0.025, 0.29] | [0.30, 0.39, 0.46] | [3.30, 2.53, 2.19] |        2.67       |
+--------------------------------+-----------------+-----------------------+--------------------+--------------------+-------------------+
```
---
