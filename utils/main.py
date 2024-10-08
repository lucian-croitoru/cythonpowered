import argparse
import sys

from utils.benchmark.benchmark_runner import BenchmarkRunner
from utils.definitions.list_functions import AllFunctionDefinitionPrinter
from cythonpowered import VERSION


TITLE = f"""
               _   _                                                      _ 
     ___ _   _| |_| |__   ___  _ __  _ __   _____      _____ _ __ ___  __| |
    / __| | | | __| '_ \ / _ \| '_ \| '_ \ / _ \ \ /\ / / _ \ '__/ _ \/ _` |
   | (__| |_| | |_| | | | (_) | | | | |_) | (_) \ V  V /  __/ | |  __/ (_| |
    \___|\__, |\__|_| |_|\___/|_| |_| .__/ \___/ \_/\_/ \___|_|  \___|\__,_|
         |___/                      |_|                                     
                                                                  ver. {VERSION}
"""


def run_benchmark():
    print(TITLE, flush=True)
    BenchmarkRunner()


def list_functions():
    print(TITLE, flush=True)
    AllFunctionDefinitionPrinter()


def print_version():
    print(VERSION)


def main():
    parser = argparse.ArgumentParser(
        prog="cythonpowered",
        description="Utilities for the cythonpowered Python library",
    )

    parser.add_argument("-b", "--benchmark", help="run benchmark", action="store_true")
    parser.add_argument("-l", "--list", help="list functions", action="store_true")
    parser.add_argument("-v", "--version", help="print version", action="store_true")
    args = parser.parse_args()

    passed_args = [
        arg for arg in args.__dict__ if args.__dict__[arg] not in [False, None]
    ]
    if len(passed_args) == 0:
        parser.print_help()

    if args.benchmark is True:
        run_benchmark()
        sys.exit(0)

    if args.list is True:
        list_functions()
        sys.exit(0)

    if args.version is True:
        print_version()
        sys.exit(0)


if __name__ == "__main__":
    main()
