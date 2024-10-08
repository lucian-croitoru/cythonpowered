from utils.benchmark._base import (
    BaseFunctionBenchmark,
    BaseModuleBenchmark,
)

from utils.definitions._random import (
    PythonRandomRandomDef,
    CythonRandomRandomDef,
    CythonRandomNRandomDef,
    PythonRandomRandintDef,
    CythonRandomRandintDef,
    CythonRandomNRandintDef,
    PythonRandomUniformDef,
    CythonRandomUniformDef,
    CythonRandomNUniformDef,
    PythonRandomChoiceDef,
    CythonRandomChoiceDef,
    PythonRandomChoicesDef,
    CythonRandomChoicesDef,
)

import cythonpowered.random as cy_random


class RandomBenchmarkDefinition(BaseFunctionBenchmark):
    python_function = PythonRandomRandomDef
    cython_function = CythonRandomRandomDef
    cython_n_function = CythonRandomNRandomDef


class RandintBenchmarkDefinition(BaseFunctionBenchmark):
    python_function = PythonRandomRandintDef
    cython_function = CythonRandomRandintDef
    cython_n_function = CythonRandomNRandintDef
    args = [-1000000, 1000000]


class UniformBenchmarkDefinition(BaseFunctionBenchmark):
    python_function = PythonRandomUniformDef
    cython_function = CythonRandomUniformDef
    cython_n_function = CythonRandomNUniformDef
    args = [-123456.789, 123456.789]


class ChoiceBenchmarkDefinition(BaseFunctionBenchmark):
    python_function = PythonRandomChoiceDef
    cython_function = CythonRandomChoiceDef
    args = [cy_random.n_randint(-100000, 100000, 10000)]


class ChoicesBenchmarkDefinition(BaseFunctionBenchmark):
    python_function = PythonRandomChoicesDef
    cython_function = CythonRandomChoicesDef
    args = [cy_random.n_randint(-100000, 100000, 10000)]
    kwargs = {"k": 100}
    runs = [1000, 10000, 100000]


class RandomBenchmark(BaseModuleBenchmark):
    MODULE = "random"
    BENCHMARKS = [
        RandomBenchmarkDefinition,
        RandintBenchmarkDefinition,
        UniformBenchmarkDefinition,
        ChoiceBenchmarkDefinition,
        ChoicesBenchmarkDefinition,
    ]
