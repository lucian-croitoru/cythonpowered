from utils.definitions._base import BaseFunctionDefinition, REPLACEMENT
import datetime as py_datetime
import calendar as py_calendar
import cythonpowered.dateutil as cy_dateutil


class PythonTodayDef(BaseFunctionDefinition):
    function = py_datetime.date.today
    reference = "datetime.date.today"


class CythonTodayDef(BaseFunctionDefinition):
    function = cy_dateutil.date.today
    reference = "cythonpowered.dateutil.date.today"
    usage = REPLACEMENT


class PythonIsleapDef(BaseFunctionDefinition):
    function = py_calendar.isleap
    reference = "calendar.isleap"


class CythonIsleapDef(BaseFunctionDefinition):
    function = cy_dateutil.dateutil.date.isleap
    reference = "cythonpowered.dateutil.date.isleap"
    usage = REPLACEMENT


class PythonMonthrangeDef(BaseFunctionDefinition):
    function = py_calendar.monthrange
    reference = "calendar.monthrange"


class CythonMonthrangeDef(BaseFunctionDefinition):
    function = cy_dateutil.date.monthrange
    reference = "cythonpowered.dateutil.date.monthrange"
    usage = REPLACEMENT


class PythonFromstringDef(BaseFunctionDefinition):
    function = py_datetime.datetime.strptime
    reference = "datetime.datetime.strptime"


class CythonFromstringDef(BaseFunctionDefinition):
    function = cy_dateutil.date.fromstring
    reference = "cythonpowered.dateutil.date.fromstring"
    usage = REPLACEMENT


class PythonTostringDef(BaseFunctionDefinition):
    function = py_datetime.date.strftime
    reference = "datetime.date.strftime"


class CythonTostringDef(BaseFunctionDefinition):
    function = cy_dateutil.date.tostring
    reference = "cythonpowered.dateutil.date.tostring"
    usage = REPLACEMENT


class PythonWeekdayDef(BaseFunctionDefinition):
    function = py_datetime.date.weekday
    reference = "datetime.date.weekday"


class CythonWeekdayDef(BaseFunctionDefinition):
    function = cy_dateutil.date.weekday
    reference = "cythonpowered.dateutil.date.weekday"
    usage = REPLACEMENT


class PythonYeardayDef(BaseFunctionDefinition):
    function = py_datetime.date.timetuple
    reference = "datetime.date.timetuple.tm_yday"


class CythonYeardayDef(BaseFunctionDefinition):
    function = cy_dateutil.date.yearday
    reference = "cythonpowered.dateutil.date.yearday"
    usage = REPLACEMENT


DATEUTIL_DEFINITION_PAIRS = [
    [PythonTodayDef, CythonTodayDef],
    [PythonIsleapDef, CythonIsleapDef],
    [PythonMonthrangeDef, CythonMonthrangeDef],
    [PythonFromstringDef, CythonFromstringDef],
    [PythonTostringDef, CythonTostringDef],
    [PythonWeekdayDef, CythonWeekdayDef],
    [PythonYeardayDef, CythonYeardayDef],
]
