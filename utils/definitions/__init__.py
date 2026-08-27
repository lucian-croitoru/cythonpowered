"""Function definition utilities for cythonpowered."""

from utils.deps import require

LIST_DEPS = [
    {"pip_name": "prettytable", "module_name": "prettytable"},
    {"pip_name": "beautifulsoup4", "module_name": "bs4"},
    {"pip_name": "lxml", "module_name": "lxml"},
]


def run_list():
    """Print a table of all provided functions.

    The definition modules are imported only after the optional dependency
    check passes, so importing this package does not require
    cythonpowered[utils].
    """
    require("Listing functions", LIST_DEPS)
    from utils.definitions.list_functions import AllFunctionDefinitionPrinter

    AllFunctionDefinitionPrinter()
