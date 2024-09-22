import argparse
import sys

from scripts.benchmark.benchmark_runner import BenchmarkRunner
from cythonpowered import VERSION


def run_benchmark():
    BenchmarkRunner()
    sys.exit(0)


def print_version():
    print(VERSION)
    sys.exit(0)


def main():
    parser = argparse.ArgumentParser(
        prog="cythonpowered",
        description="Utilities for the cythonpowered Python library",
    )

    parser.add_argument("-b", "--benchmark", help="run benchmark", action="store_true")
    parser.add_argument("-v", "--version", help="print version", action="store_true")
    args = parser.parse_args()

    passed_args = [
        arg for arg in args.__dict__ if args.__dict__[arg] not in [False, None]
    ]
    if len(passed_args) == 0:
        parser.print_help()

    if args.benchmark is True:
        run_benchmark()

    if args.version is True:
        print_version()


if __name__ == "__main__":
    main()
