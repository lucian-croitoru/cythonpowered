from cpuinfo import get_cpu_info
import platform
import psutil
from typing import Optional

from utils.benchmark._random import RandomBenchmark


class BenchmarkRunner:

    MODULE_BENCHMARKS = [RandomBenchmark]

    def __init__(self) -> None:
        sys_info = self.get_system_info()
        sys_info_pretty = self.prettify_dict(sys_info)
        for line in sys_info_pretty:
            self.log(line)
        self.run_module_benchmarks()

    def log(self, msg, end: Optional[str] = None) -> None:
        print(msg, end=end, flush=True)

    def get_system_info(self) -> dict:

        # CPU info
        default_unsupported_param = "Unsupported parameter for this system"
        cpu = get_cpu_info()
        cpu_name = cpu.get("brand_raw", f"[{default_unsupported_param}]")
        cpu_freq = cpu.get("hz_advertised_friendly", f"[{default_unsupported_param}]")
        cpu_cores = psutil.cpu_count(logical=False)
        cpu_threads = psutil.cpu_count(logical=True)
        arch = platform.machine()

        # Memory info
        svmem = psutil.virtual_memory()
        ram_size_gb = svmem.total / (1024**3)
        ram = f"{ram_size_gb:.2f} GB"

        # OS info
        os_name = platform.system()
        os_release = platform.release()
        os = f"{os_name} {os_release}"

        # Python version
        py_version = platform.python_version()

        # Compiler info
        compiler = platform.python_compiler()

        sysinfo = {
            "CPU model": cpu_name,
            "CPU base frequency": cpu_freq,
            "CPU cores": cpu_cores,
            "CPU threads": cpu_threads,
            "Architecture": arch,
            "Memory (RAM)": ram,
            "Operating System": os,
            "Python version": py_version,
            "C compiler": compiler,
        }

        return sysinfo

    def prettify_dict(self, input_dict: dict) -> list:
        spaces = 4
        keys = [k for k in input_dict.keys()]
        max_len = max([len(k) for k in keys])
        prettified = [f"{k}:{' '*(max_len-len(k)+spaces)}{input_dict[k]}" for k in keys]
        return prettified

    def run_module_benchmarks(self):
        for module_benchmark in self.MODULE_BENCHMARKS:
            self.log("")
            module_benchmark()
