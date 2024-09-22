from scripts.benchmark._base import (
    BaseFunctionDefinition,
    BaseBenchmarkDefinition,
    BaseBenchmark,
)

import random as py_random
import cythonpowered.random as cy_random


###############################################################################
class PythonRandomRandomDef(BaseFunctionDefinition):
    function = py_random.random
    function_reference = "random.random"


class CythonRandomRandomDef(BaseFunctionDefinition):
    function = cy_random.random
    function_reference = "cythonpowered.random.random"


class CythonRandomNRandomDef(BaseFunctionDefinition):
    function = cy_random.n_random
    function_reference = "cythonpowered.random.n_random"


class RandomBenchmarkDefinition(BaseBenchmarkDefinition):
    python_candidate = PythonRandomRandomDef
    cython_candidate = CythonRandomRandomDef
    cython_n_candidate = CythonRandomNRandomDef


###############################################################################
class PythonRandomRandintDef(BaseFunctionDefinition):
    function = py_random.randint
    function_reference = "random.randint"


class CythonRandomRandintDef(BaseFunctionDefinition):
    function = cy_random.randint
    function_reference = "cythonpowered.random.randint"


class CythonRandomNRandintDef(BaseFunctionDefinition):
    function = cy_random.n_randint
    function_reference = "cythonpowered.random.n_randint"


class RandintBenchmarkDefinition(BaseBenchmarkDefinition):
    python_candidate = PythonRandomRandintDef
    cython_candidate = CythonRandomRandintDef
    cython_n_candidate = CythonRandomNRandintDef
    args = [-1000000, 1000000]


###############################################################################
class PythonRandomUniformDef(BaseFunctionDefinition):
    function = py_random.uniform
    function_reference = "random.uniform"


class CythonRandomUniformDef(BaseFunctionDefinition):
    function = cy_random.uniform
    function_reference = "cythonpowered.random.uniform"


class CythonRandomNUniformDef(BaseFunctionDefinition):
    function = cy_random.n_uniform
    function_reference = "cythonpowered.random.n_uniform"


class UniformBenchmarkDefinition(BaseBenchmarkDefinition):
    python_candidate = PythonRandomUniformDef
    cython_candidate = CythonRandomUniformDef
    cython_n_candidate = CythonRandomNUniformDef
    args = [-123456.789, 123456.789]


###############################################################################
class PythonRandomChoiceDef(BaseFunctionDefinition):
    function = py_random.choice
    function_reference = "random.choice"


class CythonRandomChoiceDef(BaseFunctionDefinition):
    function = cy_random.choice
    function_reference = "cythonpowered.random.choice"


class ChoiceBenchmarkDefinition(BaseBenchmarkDefinition):
    python_candidate = PythonRandomChoiceDef
    cython_candidate = CythonRandomChoiceDef
    args = [cy_random.n_randint(-100000, 100000, 10000)]


###############################################################################
class PythonRandomChoicesDef(BaseFunctionDefinition):
    function = py_random.choices
    function_reference = "random.choices"


class CythonRandomChoicesDef(BaseFunctionDefinition):
    function = cy_random.choices
    function_reference = "cythonpowered.random.choices"


class ChoicesBenchmarkDefinition(BaseBenchmarkDefinition):
    python_candidate = PythonRandomChoicesDef
    cython_candidate = CythonRandomChoicesDef
    args = [cy_random.n_randint(-100000, 100000, 10000)]
    kwargs = {"k": 10000}
    runs = [100, 1000, 10000]


###############################################################################
class RandomBenchmark(BaseBenchmark):
    CYTHONPOWERED_MODULE = "random"
    BENCHMARK_DEFINITIONS = [
        RandomBenchmarkDefinition,
        RandintBenchmarkDefinition,
        UniformBenchmarkDefinition,
        ChoiceBenchmarkDefinition,
        ChoicesBenchmarkDefinition,
    ]
