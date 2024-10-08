from typing import List, Optional, Type
from prettytable import PrettyTable

REPLACEMENT = "Drop-in replacement"


class BaseFunctionDefinition:
    function: callable
    reference: str
    usage: str = ""


class BaseFunctionDefinitionPrinter:

    FUNCTION_PAIRS: List[List[BaseFunctionDefinition]] = []

    def __init__(self) -> None:
        if len(self.FUNCTION_PAIRS) == 0:
            raise NotImplementedError("No pairs of function definitions provided")
        for pair in self.FUNCTION_PAIRS:
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
            "[cythonpowered] function",
            "Replaces [Python] function",
            "Usage / details",
        ]
        for f in table.field_names:
            table.align[f] = "r" if f == table.field_names[0] else "l"

        for i in range(len(self.FUNCTION_PAIRS)):
            table.add_row(
                [
                    i + 1,
                    self.FUNCTION_PAIRS[i][1].reference,
                    self.FUNCTION_PAIRS[i][0].reference,
                    self.FUNCTION_PAIRS[i][1].usage,
                ]
            )
        self.log(table)
