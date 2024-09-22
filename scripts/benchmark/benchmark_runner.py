from cpuinfo import get_cpu_info
import platform
import psutil

from scripts.benchmark._random import RandomBenchmark
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


class BenchmarkRunner:

    BENCHMARKS = [RandomBenchmark]
    LOG = []

    def __init__(self) -> None:
        sys_info = self._get_system_info()
        sys_info_pretty = self._prettify_dict(sys_info)
        self._log(TITLE)
        for line in sys_info_pretty:
            self._log(line)
        self.run_benchmarks()

    def _log(self, msg) -> None:
        self.LOG.append(msg)
        print(msg)

    def _get_system_info(self) -> dict:

        # OS info
        os_name = platform.system()
        os_release = platform.release()
        os = f"{os_name} {os_release}"

        # CPU info
        cpu = get_cpu_info()
        cpu_name = cpu["brand_raw"]
        cpu_freq = cpu["hz_advertised_friendly"]
        cpu_cores = psutil.cpu_count(logical=False)
        cpu_threads = psutil.cpu_count(logical=True)
        arch = platform.machine()

        # Memory info
        svmem = psutil.virtual_memory()
        ram_size_gb = svmem.total / (1024**3)
        ram = f"{ram_size_gb:.2f} GB"

        # Compiler info
        compiler = platform.python_compiler()

        sysinfo = {
            "Operating System": os,
            "CPU model": cpu_name,
            "CPU base frequency": cpu_freq,
            "CPU cores": cpu_cores,
            "CPU threads": cpu_threads,
            "Architecture": arch,
            "Memory (RAM)": ram,
            "C compiler": compiler,
        }

        return sysinfo

    def _prettify_dict(self, input_dict: dict) -> list:
        spaces = 4
        keys = [k for k in input_dict.keys()]
        max_len = max([len(k) for k in keys])
        prettified = [f"{k}:{' '*(max_len-len(k)+spaces)}{input_dict[k]}" for k in keys]
        return prettified

    def run_benchmarks(self):
        for benchmark in self.BENCHMARKS:
            self._log("")
            benchmark()
