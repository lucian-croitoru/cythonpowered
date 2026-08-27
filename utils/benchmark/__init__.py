"""Benchmarking utilities for cythonpowered."""

from utils.deps import require

BENCHMARK_DEPS = [
    {"pip_name": "pandas", "module_name": "pandas"},
    {"pip_name": "psutil", "module_name": "psutil"},
    {"pip_name": "py-cpuinfo", "module_name": "cpuinfo"},
    {"pip_name": "prettytable", "module_name": "prettytable"},
    {"pip_name": "beautifulsoup4", "module_name": "bs4"},
    {"pip_name": "lxml", "module_name": "lxml"},
]


def run_benchmark():
    """Run the benchmark suite.

    The benchmark modules are imported only after the optional dependency
    check passes, so importing this package does not require
    cythonpowered[utils].
    """
    require("Benchmarking", BENCHMARK_DEPS)
    from utils.benchmark.benchmark_runner import BenchmarkRunner

    BenchmarkRunner()
