from typing import List, Optional, Type
from prettytable import PrettyTable

REPLACEMENT = "Drop-in replacement"


class BaseFunctionDefinition:
    function: callable
    reference: str
    usage: str = ""


class BaseFunctionDefinitionPrinter:

    FUNCTION_PAIRS: List[List[List[BaseFunctionDefinition]]] = []

    def __init__(self) -> None:
        if len(self.FUNCTION_PAIRS) == 0:
            raise NotImplementedError("No pairs of function definitions provided")
        for module in self.FUNCTION_PAIRS:
            for pair in module:
                if type(pair) != list:
                    raise TypeError
                if len(pair) != 2:
                    raise ValueError
        self.print_function_definitions()

    def log(self, msg, end: Optional[str] = None) -> None:
        print(msg, end=end, flush=True)

    def print_function_definitions(self) -> None:
        table = PrettyTable()
        table.field_names = [
            "#",
            "cythonpowered function",
            "Replaces (Python)",
            "Usage / details",
        ]
        for f in table.field_names:
            table.align[f] = "r" if f == table.field_names[0] else "l"
        i = 0
        for module in self.FUNCTION_PAIRS:
            for pair in module:
                i += 1
                table.add_row(
                    [
                        i,
                        pair[1].reference,
                        pair[0].reference,
                        pair[1].usage,
                    ]
                )
            table.add_divider()
        self.log(table)
