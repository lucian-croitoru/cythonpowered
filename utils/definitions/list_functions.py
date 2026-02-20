from itertools import chain
from utils.definitions._base import BaseFunctionDefinitionPrinter
from utils.definitions._random import RANDOM_DEFINITION_PAIRS
from utils.definitions._dateutil import DATEUTIL_DEFINITION_PAIRS


ALL_PAIRS = list(chain(RANDOM_DEFINITION_PAIRS, DATEUTIL_DEFINITION_PAIRS))


class AllFunctionDefinitionPrinter(BaseFunctionDefinitionPrinter):
    FUNCTION_PAIRS = ALL_PAIRS
