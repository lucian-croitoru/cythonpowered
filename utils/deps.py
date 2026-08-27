import importlib
import sys
from typing import Dict, List


def require(feature: str, deps: List[Dict[str, str]]) -> None:
    """Exit with a helpful message if any optional dependency is missing.

    ``deps`` is a sequence of dicts with:
      - ``pip_name``: the PyPI distribution name, used in the install hint
      - ``module_name``: the importable module name, used for the import check
    """
    missing = []
    for dep in deps:
        try:
            importlib.import_module(dep["module_name"])
        except ImportError:
            missing.append(dep["pip_name"])
    if missing:
        print(
            f"{feature} requires optional dependencies: {', '.join(missing)}. "
            f"Run 'pip install cythonpowered[utils]' to enable this functionality."
        )
        sys.exit(0)
