from utils.definitions._base import BaseFunctionDefinition, REPLACEMENT
import random as py_random
import cythonpowered.random as cy_random


# =============================================================================
class PythonRandomRandomDef(BaseFunctionDefinition):
    function = py_random.random
    reference = "random.random"


class CythonRandomRandomDef(BaseFunctionDefinition):
    function = cy_random.random
    reference = "cythonpowered.random.random"
    usage = REPLACEMENT


class CythonRandomNRandomDef(BaseFunctionDefinition):
    function = cy_random.n_random
    reference = "cythonpowered.random.n_random"
    usage = "n_random(k) is equivalent to [random() for i in range(k)]"


# =============================================================================
class PythonRandomRandintDef(BaseFunctionDefinition):
    function = py_random.randint
    reference = "random.randint"


class CythonRandomRandintDef(BaseFunctionDefinition):
    function = cy_random.randint
    reference = "cythonpowered.random.randint"
    usage = REPLACEMENT


class CythonRandomNRandintDef(BaseFunctionDefinition):
    function = cy_random.n_randint
    reference = "cythonpowered.random.n_randint"
    usage = "n_randint(a, b, k) is equivalent to [randint(a, b) for i in range(k)]"


# =============================================================================
class PythonRandomUniformDef(BaseFunctionDefinition):
    function = py_random.uniform
    reference = "random.uniform"


class CythonRandomUniformDef(BaseFunctionDefinition):
    function = cy_random.uniform
    reference = "cythonpowered.random.uniform"
    usage = REPLACEMENT


class CythonRandomNUniformDef(BaseFunctionDefinition):
    function = cy_random.n_uniform
    reference = "cythonpowered.random.n_uniform"
    usage = "n_uniform(a, b, k) is equivalent to [uniform(a, b) for i in range(k)]"


# =============================================================================
class PythonRandomChoiceDef(BaseFunctionDefinition):
    function = py_random.choice
    reference = "random.choice"


class CythonRandomChoiceDef(BaseFunctionDefinition):
    function = cy_random.choice
    reference = "cythonpowered.random.choice"
    usage = REPLACEMENT


# =============================================================================
class PythonRandomChoicesDef(BaseFunctionDefinition):
    function = py_random.choices
    reference = "random.choices"


class CythonRandomChoicesDef(BaseFunctionDefinition):
    function = cy_random.choices
    reference = "cythonpowered.random.choices"
    usage = "Drop-in replacement, only supports the 'k' keyword argument"


# =============================================================================


RANDOM_DEFINITION_PAIRS = [
    [PythonRandomRandomDef, CythonRandomRandomDef],
    [PythonRandomRandomDef, CythonRandomNRandomDef],
    [PythonRandomRandintDef, CythonRandomRandintDef],
    [PythonRandomRandintDef, CythonRandomNRandintDef],
    [PythonRandomUniformDef, CythonRandomUniformDef],
    [PythonRandomUniformDef, CythonRandomNUniformDef],
    [PythonRandomChoiceDef, CythonRandomChoiceDef],
    [PythonRandomChoicesDef, CythonRandomChoicesDef],
]
