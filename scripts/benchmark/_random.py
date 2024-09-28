from scripts.benchmark._base import (
    BaseFunctionDefinition,
    BaseFunctionBenchmark,
    BaseModuleBenchmark,
)

import random as py_random
import cythonpowered.random as cy_random


# =============================================================================
class PythonRandomRandomDef(BaseFunctionDefinition):
    function = py_random.random
    reference = "random.random"


class CythonRandomRandomDef(BaseFunctionDefinition):
    function = cy_random.random
    reference = "cythonpowered.random.random"


class CythonRandomNRandomDef(BaseFunctionDefinition):
    function = cy_random.n_random
    reference = "cythonpowered.random.n_random"


class RandomBenchmarkDefinition(BaseFunctionBenchmark):
    python_function = PythonRandomRandomDef
    cython_function = CythonRandomRandomDef
    cython_n_function = CythonRandomNRandomDef


# =============================================================================
class PythonRandomRandintDef(BaseFunctionDefinition):
    function = py_random.randint
    reference = "random.randint"


class CythonRandomRandintDef(BaseFunctionDefinition):
    function = cy_random.randint
    reference = "cythonpowered.random.randint"


class CythonRandomNRandintDef(BaseFunctionDefinition):
    function = cy_random.n_randint
    reference = "cythonpowered.random.n_randint"


class RandintBenchmarkDefinition(BaseFunctionBenchmark):
    python_function = PythonRandomRandintDef
    cython_function = CythonRandomRandintDef
    cython_n_function = CythonRandomNRandintDef
    args = [-1000000, 1000000]


# =============================================================================
class PythonRandomUniformDef(BaseFunctionDefinition):
    function = py_random.uniform
    reference = "random.uniform"


class CythonRandomUniformDef(BaseFunctionDefinition):
    function = cy_random.uniform
    reference = "cythonpowered.random.uniform"


class CythonRandomNUniformDef(BaseFunctionDefinition):
    function = cy_random.n_uniform
    reference = "cythonpowered.random.n_uniform"


class UniformBenchmarkDefinition(BaseFunctionBenchmark):
    python_function = PythonRandomUniformDef
    cython_function = CythonRandomUniformDef
    cython_n_function = CythonRandomNUniformDef
    args = [-123456.789, 123456.789]


# =============================================================================
class PythonRandomChoiceDef(BaseFunctionDefinition):
    function = py_random.choice
    reference = "random.choice"


class CythonRandomChoiceDef(BaseFunctionDefinition):
    function = cy_random.choice
    reference = "cythonpowered.random.choice"


class ChoiceBenchmarkDefinition(BaseFunctionBenchmark):
    python_function = PythonRandomChoiceDef
    cython_function = CythonRandomChoiceDef
    args = [cy_random.n_randint(-100000, 100000, 10000)]


# =============================================================================
class PythonRandomChoicesDef(BaseFunctionDefinition):
    function = py_random.choices
    reference = "random.choices"


class CythonRandomChoicesDef(BaseFunctionDefinition):
    function = cy_random.choices
    reference = "cythonpowered.random.choices"


class ChoicesBenchmarkDefinition(BaseFunctionBenchmark):
    python_function = PythonRandomChoicesDef
    cython_function = CythonRandomChoicesDef
    args = [cy_random.n_randint(-100000, 100000, 10000)]
    kwargs = {"k": 100}
    runs = [1000, 10000, 100000]


# =============================================================================
class RandomBenchmark(BaseModuleBenchmark):
    MODULE = "random"
    BENCHMARKS = [
        RandomBenchmarkDefinition,
        RandintBenchmarkDefinition,
        UniformBenchmarkDefinition,
        ChoiceBenchmarkDefinition,
        ChoicesBenchmarkDefinition,
    ]
