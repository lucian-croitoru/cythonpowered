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
    PythonYeardayDef,
    CythonYeardayDef,
    PythonFromordinalDef,
    CythonFromordinalDef,
    PythonToordinalDef,
    CythonToordinalDef,
    PythonOffsetDef,
    CythonOffsetDef,
    PythonIncrementDef,
    CythonIncrementDef,
    PythonDaterangeDef,
    CythonDaterangeDef,
)


class TodayBenchmarkDefinition(BaseFunctionBenchmark):
    python_function = PythonTodayDef
    cython_function = CythonTodayDef


class IsleapBenchmarkDefinition(BaseFunctionBenchmark):
    python_function = PythonIsleapDef
    cython_function = CythonIsleapDef
    python_args = [2024]
    cython_args = python_args


class MonthrangeBenchmarkDefinition(BaseFunctionBenchmark):
    python_function = PythonMonthrangeDef
    cython_function = CythonMonthrangeDef
    python_args = [2017, 2]
    cython_args = python_args


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


class WeekdayBenchmarkDefinition(BaseFunctionBenchmark):
    python_function = PythonWeekdayDef
    cython_function = CythonWeekdayDef
    python_args = [datetime.date(2026, 1, 7)]
    cython_args = [date(2026, 1, 7)]


class YeardayBenchmarkDefinition(BaseFunctionBenchmark):
    python_function = PythonYeardayDef
    cython_function = CythonYeardayDef
    python_args = [datetime.date(2026, 4, 13)]
    cython_args = [date(2026, 4, 13)]


class FromordinalBenchmarkDefinition(BaseFunctionBenchmark):
    python_function = PythonFromordinalDef
    cython_function = CythonFromordinalDef
    python_args = [739669]
    cython_args = python_args


class ToordinalBenchmarkDefinition(BaseFunctionBenchmark):
    python_function = PythonToordinalDef
    cython_function = CythonToordinalDef
    python_args = [datetime.date(2026, 4, 13)]
    cython_args = [date(2026, 4, 13)]


class OffsetBenchmarkDefinition(BaseFunctionBenchmark):
    python_function = PythonOffsetDef
    cython_function = CythonOffsetDef
    python_args = [datetime.date(2026, 4, 13)]
    cython_args = [date(2026, 4, 13)]
    kwargs = {"days": 47, "weeks": -2}


class IncrementBenchmarkDefinition(BaseFunctionBenchmark):
    python_function = PythonIncrementDef
    cython_function = CythonIncrementDef
    python_args = [datetime.date(2026, 4, 13), 1]
    cython_args = [date(2026, 4, 13)]


class DaterangeBenchmarkDefinition(BaseFunctionBenchmark):
    python_function = PythonDaterangeDef
    cython_function = CythonDaterangeDef
    python_args = [datetime.date(2026, 4, 13), datetime.date(2027, 8, 28)]
    cython_args = [date(2026, 4, 13), date(2027, 8, 28)]
    kwargs = {"freq": "ME"}
    runs = [100, 1000, 10000]


class DateutilBenchmark(BaseModuleBenchmark):
    MODULE = "dateutil"
    BENCHMARKS = [
        TodayBenchmarkDefinition,
        IsleapBenchmarkDefinition,
        MonthrangeBenchmarkDefinition,
        FromstringBenchmarkDefinition,
        TostringBenchmarkDefinition,
        WeekdayBenchmarkDefinition,
        YeardayBenchmarkDefinition,
        FromordinalBenchmarkDefinition,
        ToordinalBenchmarkDefinition,
        OffsetBenchmarkDefinition,
        IncrementBenchmarkDefinition,
        DaterangeBenchmarkDefinition,
    ]
