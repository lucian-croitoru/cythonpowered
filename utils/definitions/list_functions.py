from utils.definitions._base import BaseFunctionDefinitionPrinter
from utils.definitions._random import RANDOM_DEFINITION_PAIRS


ALL_PAIRS = RANDOM_DEFINITION_PAIRS


class AllFunctionDefinitionPrinter(BaseFunctionDefinitionPrinter):
    FUNCTION_PAIRS = ALL_PAIRS
