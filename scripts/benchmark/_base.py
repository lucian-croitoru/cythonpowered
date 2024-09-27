from typing import Optional, List
from time import time
from prettytable import PrettyTable

from cythonpowered import MODULES


LINE_LENGTH = 80
SEPARATOR = "=" * LINE_LENGTH
DEFAULT_RUNS = [10000, 100000, 1000000]


class BaseFunctionDefinition:
    function: callable
    reference: str


class BaseFunctionBenchmark:
    python_function: BaseFunctionDefinition
    cython_function: BaseFunctionDefinition
    cython_n_function: Optional[BaseFunctionDefinition] = None
    args: list = []
    kwargs: dict = {}
    runs: Optional[List[int]] = DEFAULT_RUNS

    def __init__(self) -> None:
        self.benchmark_data = {}
        self.run()

    def log(self, msg, end: Optional[str] = None) -> None:
        print(msg, end=end, flush=True)

    def log_progress(self, progress: int, total: int):
        cython_n_func_ref = None
        if self.cython_n_function is not None:
            cython_n_func_ref = self.cython_n_function.reference

        if progress == 0:
            end = ""
        else:
            self.log("\r", end="")
            end = "\r"

        cython_n_func_msg = (
            " and [" + cython_n_func_ref + "]" if cython_n_func_ref is not None else ""
        )
        self.log(
            f"Comparing [{self.cython_function.reference}]{cython_n_func_msg} with [{self.python_function.reference}]... {(progress/total*100):.2f}%",
            end=end,
        )

    def run(self):
        python_func = self.python_function.function
        cython_func = self.cython_function.function
        cython_n_func = None

        if self.cython_n_function is not None:
            cython_n_func = self.cython_n_function.function

        args = self.args
        kwargs = self.kwargs
        runs = self.runs

        progress = 0
        total = 6 if cython_n_func is None else 9

        self.log_progress(progress, total)

        for run in runs:
            # Run Python function
            st = time()
            py_results = [python_func(*args, **kwargs) for i in range(run)]
            et = time()
            python_time = et - st

            progress += 1
            self.log_progress(progress, total)

            # Run cythonpowered function
            st = time()
            cy_results = [cython_func(*args, **kwargs) for i in range(run)]
            et = time()
            cython_time = et - st

            progress += 1
            self.log_progress(progress, total)

            # Run cythonpowered n_function
            cython_n_time = None
            if cython_n_func is not None:
                st = time()
                n_results = cython_n_func(*args, run, **kwargs)
                et = time()
                cython_n_time = et - st

                progress += 1
                self.log_progress(progress, total)

            self.benchmark_data[str(run)] = [python_time, cython_time, cython_n_time]

        self.log("")


class BaseModuleBenchmark:

    MODULE: Optional[str] = None
    BENCHMARKS: List[BaseFunctionBenchmark] = []

    def __init__(self) -> None:
        if self.MODULE not in MODULES:
            raise NotImplementedError
        self.intro()
        self.results = [b() for b in self.BENCHMARKS]
        self.print_results()

    def log(self, msg, end: Optional[str] = None) -> None:
        print(msg, end=end, flush=True)

    def intro(self) -> None:
        module = self.MODULE
        defs = len(self.BENCHMARKS)
        self.log(SEPARATOR)
        self.log(
            f"Running benchmark for the [cythonpowered.{module}] module ({defs} benchmarks)..."
        )
        self.log(SEPARATOR)

    def format_number_magnitude(self, number) -> str:
        magnitudes = ["", "K", "M", "B"]
        i = 0
        while number // (1000**i) >= 1000 and i <= len(magnitudes):
            i += 1
        formatted = f"{int(number / (1000 ** i))}{magnitudes[i]}"
        return formatted

    def format_execution_times(self, times: List[float]) -> str:
        formatted = str(
            [
                f"{('{0:.' + str(4 - i) + 'f}').format(times[i])}"
                for i in range(len(times))
            ]
        ).replace("'", "")
        return formatted

    def format_factor(self, factor) -> str:
        _format = "{0:." + ("2" if factor < 10 else "1") + "f}"
        return _format.format(factor)

    def format_factors(
        self,
        times_1: List[float],
        times_2: List[float],
        inverted: bool = False,
    ) -> str:

        if inverted:
            formatted = str(
                [
                    self.format_factor(times_2[i] / times_1[i])
                    for i in range(len(times_2))
                ]
            ).replace("'", "")
        else:
            formatted = str(
                [
                    self.format_factor(times_1[i] / times_2[i])
                    for i in range(len(times_2))
                ]
            ).replace("'", "")

        return formatted

    def calculate_avg_factor(
        self,
        times_1: List[float],
        times_2: List[float],
        inverted: bool = False,
    ) -> str:
        if inverted is True:
            return sum(([times_1[i] / times_2[i] for i in range(len(times_1))])) / len(
                times_1
            )
        else:
            return sum([times_2[i] / times_1[i] for i in range(len(times_1))]) / len(
                times_2
            )

    def print_results(self) -> None:
        table = PrettyTable()
        table.field_names = [
            "Function name",
            "No. of runs",
            "Execution time (s)",
            "Time factor",
            "Speed factor",
            "Avg. speed factor",
        ]

        for r in self.results:

            items = [i[1] for i in r.benchmark_data.items()]

            cython_n_function = r.cython_n_function
            python_times = [t[0] for t in items]
            cython_times = [t[1] for t in items]
            if cython_n_function is not None:
                cython_n_times = [t[2] for t in items]

            runs = str([self.format_number_magnitude(n) for n in r.runs]).replace(
                "'", ""
            )

            table.add_row(
                [
                    f"[Python] {r.python_function.reference}",
                    runs,
                    self.format_execution_times(python_times),
                    "1.00",
                    "1.00",
                    "1.00",
                ]
            )
            table.add_row(
                [
                    r.cython_function.reference,
                    runs,
                    self.format_execution_times(cython_times),
                    self.format_factors(cython_times, python_times),
                    self.format_factors(cython_times, python_times, inverted=True),
                    self.format_factor(
                        self.calculate_avg_factor(cython_times, python_times)
                    ),
                ],
                divider=(cython_n_function is None),
            )

            if cython_n_function is not None:
                table.add_row(
                    [
                        r.cython_n_function.reference,
                        runs,
                        self.format_execution_times(cython_n_times),
                        self.format_factors(cython_n_times, python_times),
                        self.format_factors(
                            cython_n_times, python_times, inverted=True
                        ),
                        self.format_factor(
                            self.calculate_avg_factor(
                                cython_n_times, python_times, r.runs
                            )
                        ),
                    ],
                    divider=True,
                )

        self.log(table)
