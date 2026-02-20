from utils.benchmark._base import (
    BaseFunctionBenchmark,
    BaseModuleBenchmark,
)
from cythonpowered.dateutil.dateutil import date
import datetime

from utils.definitions._dateutil import (
    PythonWeekdayDef,
    CythonWeekdayDef,
    PythonTodayDef,
    CythonTodayDef,
    PythonIsleapDef,
    CythonIsleapDef,
    PythonMonthrangeDef,
    CythonMonthrangeDef,
    PythonFromstringDef,
    CythonFromstringDef,
    PythonTostringDef,
    CythonTostringDef,
)


class TodayBenchmarkDefinition(BaseFunctionBenchmark):
    python_function = PythonTodayDef
    cython_function = CythonTodayDef


class WeekdayBenchmarkDefinition(BaseFunctionBenchmark):
    python_function = PythonWeekdayDef
    cython_function = CythonWeekdayDef
    python_args = [datetime.date(2026, 1, 7)]
    cython_args = [date(2026, 1, 7)]


class MonthrangeBenchmarkDefinition(BaseFunctionBenchmark):
    python_function = PythonMonthrangeDef
    cython_function = CythonMonthrangeDef
    args = [2017, 2]


class IsleapBenchmarkDefinition(BaseFunctionBenchmark):
    python_function = PythonIsleapDef
    cython_function = CythonIsleapDef
    args = [2024]


class FromstringBenchmarkDefinition(BaseFunctionBenchmark):
    python_function = PythonFromstringDef
    cython_function = CythonFromstringDef
    python_args = ["2026-01-07", "%Y-%m-%d"]
    cython_args = ["2026-01-07"]


class TostringBenchmarkDefinition(BaseFunctionBenchmark):
    python_function = PythonTostringDef
    cython_function = CythonTostringDef
    python_args = [datetime.date(2026, 1, 7), "%Y-%m-%d"]
    cython_args = [date(2026, 1, 7)]


class DateutilBenchmark(BaseModuleBenchmark):
    MODULE = "dateutil"
    BENCHMARKS = [
        TodayBenchmarkDefinition,
        IsleapBenchmarkDefinition,
        MonthrangeBenchmarkDefinition,
        FromstringBenchmarkDefinition,
        TostringBenchmarkDefinition,
        WeekdayBenchmarkDefinition,
    ]
