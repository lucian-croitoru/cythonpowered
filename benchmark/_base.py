from typing import Optional, List
from time import time

from cythonpowered import MODULES


LINE_LENGTH = 80
THICK_LINE = "#" * LINE_LENGTH
MEDIUM_LINE = "=" * LINE_LENGTH
THIN_LINE = "-" * LINE_LENGTH
DEFAULT_RUNS = [100000, 1000000, 10000000]


class BaseFunctionDefinition:
    function: callable
    function_reference: str


class BaseBenchmarkDefinition:
    python_candidate: BaseFunctionDefinition
    cython_candidate: BaseFunctionDefinition
    cython_n_candidate: Optional[BaseFunctionDefinition] = None
    args: list = []
    kwargs: dict = {}
    runs: Optional[List[int]] = DEFAULT_RUNS


class BaseBenchmark:

    CYTHONPOWERED_MODULE: Optional[str] = None
    BENCHMARK_DEFINITIONS: List[BaseBenchmarkDefinition] = []
    LOG = []

    def __init__(self, iterations: int = 1000) -> None:
        if self.CYTHONPOWERED_MODULE not in MODULES:
            raise NotImplementedError
        self.iterations = iterations
        self._benchmark_intro()
        for benchmark_def in self.BENCHMARK_DEFINITIONS:
            self.run_benchmark(benchmark_def)

    def _log(self, msg, end: Optional[str] = None) -> None:
        self.LOG.append(msg)
        print(msg, end=end, flush=True)

    def _benchmark_intro(self):
        module = self.CYTHONPOWERED_MODULE
        defs = len(self.BENCHMARK_DEFINITIONS)
        self._log(THICK_LINE)
        self._log(
            f"Running benchmark for the cythonpowered [{module}] module ({defs} benchmarks)..."
        )
        self._log(THICK_LINE)

    def run_benchmark(self, benchmark_definition: BaseBenchmarkDefinition):
        python_func_ref = benchmark_definition.python_candidate.function_reference
        cython_func_ref = benchmark_definition.cython_candidate.function_reference
        self._log(MEDIUM_LINE)
        self._log(f"Comparing [{python_func_ref}] with [{cython_func_ref}]...")
        self._log(MEDIUM_LINE)

        python_func = benchmark_definition.python_candidate.function
        cython_func = benchmark_definition.cython_candidate.function
        args = benchmark_definition.args
        kwargs = benchmark_definition.kwargs
        runs = benchmark_definition.runs

        for run in runs:
            self._log(f"Generating {run} results...", end=" ")

            st = time()
            py_results = [python_func(*args, **kwargs) for i in range(run)]
            et = time()
            python_time = et - st

            st = time()
            cy_results = [cython_func(*args, **kwargs) for i in range(run)]
            et = time()
            cython_time = et - st

            comparison = "slower" if cython_time > python_time else "faster"

            self._log(f"{python_time:.6f}s vs. {cython_time:.6f}s")
            self._log(
                f"[{cython_func_ref}] is {(python_time / cython_time):.3f} times {comparison} than [{python_func_ref}] or has a time factor of {(cython_time / python_time):.3f}"
            )

            if benchmark_definition.cython_n_candidate is not None:
                cython_n_func_ref = (
                    benchmark_definition.cython_n_candidate.function_reference
                )
                cython_n_func = benchmark_definition.cython_n_candidate.function

                self._log(f"Generating results with [{cython_n_func_ref}]...", end=" ")
                st = time()
                n_results = cython_n_func(*args, run, **kwargs)
                et = time()
                cython_n_time = et - st
                self._log(f"{cython_n_time:.6f}s")

                py_comparison = "slower" if cython_n_time > python_time else "faster"
                cy_comparison = "slower" if cython_n_time > cython_time else "faster"

                self._log(
                    f"[{cython_n_func_ref}] is {(python_time / cython_n_time):.3f} times {py_comparison} than [{python_func_ref}] or has a time factor of {(cython_n_time / python_time):.3f}"
                )
                self._log(
                    f"[{cython_n_func_ref}] is {(cython_time / cython_n_time):.3f} times {cy_comparison} than [{cython_func_ref}] or has a time factor of {(cython_n_time / cython_time):.3f}"
                )

            self._log(THIN_LINE)
