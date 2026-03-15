from utils.definitions._base import BaseFunctionDefinition, REPLACEMENT
import datetime as py_datetime
import calendar as py_calendar
import cythonpowered.dateutil as cy_dateutil
import pandas


def py_offset(date, days=0, weeks=0):
    return date + py_datetime.timedelta(days=days, weeks=weeks)


class PythonTodayDef(BaseFunctionDefinition):
    function = py_datetime.date.today
    reference = "datetime.date.today()"


class CythonTodayDef(BaseFunctionDefinition):
    function = cy_dateutil.date.today
    reference = "cythonpowered.dateutil.date.today()"
    usage = f"{REPLACEMENT}, returns cythonpowered date object"


class PythonIsleapDef(BaseFunctionDefinition):
    function = py_calendar.isleap
    reference = "calendar.isleap()"


class CythonIsleapDef(BaseFunctionDefinition):
    function = cy_dateutil.dateutil.date.isleap
    reference = "cythonpowered.dateutil.date.isleap()"
    usage = REPLACEMENT


class PythonMonthrangeDef(BaseFunctionDefinition):
    function = py_calendar.monthrange
    reference = "calendar.monthrange()"


class CythonMonthrangeDef(BaseFunctionDefinition):
    function = cy_dateutil.date.monthrange
    reference = "cythonpowered.dateutil.date.monthrange()"
    usage = REPLACEMENT


class PythonFromstringDef(BaseFunctionDefinition):
    function = py_datetime.datetime.strptime
    reference = "datetime.datetime.strptime().date()"


class CythonFromstringDef(BaseFunctionDefinition):
    function = cy_dateutil.date.fromstring
    reference = "cythonpowered.dateutil.date.fromstring()"
    usage = "Assumes '%Y-%m-%d' format, returns cythonpowered date object"


class PythonTostringDef(BaseFunctionDefinition):
    function = py_datetime.date.strftime
    reference = "datetime.date().strftime()"


class CythonTostringDef(BaseFunctionDefinition):
    function = cy_dateutil.date.tostring
    reference = "cythonpowered.dateutil.date().tostring()"
    usage = "Assumes '%Y-%m-%d' format, uses cythonpowered date object"


class PythonWeekdayDef(BaseFunctionDefinition):
    function = py_datetime.date.weekday
    reference = "datetime.date().weekday()"


class CythonWeekdayDef(BaseFunctionDefinition):
    function = cy_dateutil.date.weekday
    reference = "cythonpowered.dateutil.date().weekday()"
    usage = f"{REPLACEMENT}, uses cythonpowered date object"


class PythonYeardayDef(BaseFunctionDefinition):
    function = py_datetime.date.timetuple
    reference = "datetime.date().timetuple().tm_yday"


class CythonYeardayDef(BaseFunctionDefinition):
    function = cy_dateutil.date.yearday
    reference = "cythonpowered.dateutil.date().yearday()"
    usage = f"{REPLACEMENT}, uses cythonpowered date object"


class PythonFromordinalDef(BaseFunctionDefinition):
    function = py_datetime.date.fromordinal
    reference = "datetime.date.fromordinal()"


class CythonFromordinalDef(BaseFunctionDefinition):
    function = cy_dateutil.date.fromordinal
    reference = "cythonpowered.dateutil.date.fromordinal()"
    usage = f"{REPLACEMENT}, returns cythonpowered date object"


class PythonToordinalDef(BaseFunctionDefinition):
    function = py_datetime.date.toordinal
    reference = "datetime.date().toordinal()"


class CythonToordinalDef(BaseFunctionDefinition):
    function = cy_dateutil.date.toordinal
    reference = "cythonpowered.dateutil.date().toordinal()"
    usage = f"{REPLACEMENT}, uses cythonpowered date object"


class PythonOffsetDef(BaseFunctionDefinition):
    function = py_offset
    reference = "datetime.date() +/- datetime.timedelta()"


class CythonOffsetDef(BaseFunctionDefinition):
    function = cy_dateutil.date.offset
    reference = "cythonpowered.dateutil.date().offset()"
    usage = "Supports days/weeks/months/years offset, returns cythonpowered date object"


class PythonIncrementDef(BaseFunctionDefinition):
    function = py_offset
    reference = "datetime.date() + datetime.timedelta(days=1)"


class CythonIncrementDef(BaseFunctionDefinition):
    function = cy_dateutil.date.increment
    reference = "cythonpowered.dateutil.date().increment()"
    usage = "Increments cythonpowered date object by 1 day"


class PythonDaterangeDef(BaseFunctionDefinition):
    function = pandas.date_range
    reference = "pandas.date_range()"


class CythonDaterangeDef(BaseFunctionDefinition):
    function = cy_dateutil.date.date_range
    reference = "cythonpowered.dateutil.date_range()"
    usage = "Uses cythonpowered date object, returns a list of date strings"


DATEUTIL_DEFINITION_PAIRS = [
    [PythonTodayDef, CythonTodayDef],
    [PythonIsleapDef, CythonIsleapDef],
    [PythonMonthrangeDef, CythonMonthrangeDef],
    [PythonFromstringDef, CythonFromstringDef],
    [PythonTostringDef, CythonTostringDef],
    [PythonWeekdayDef, CythonWeekdayDef],
    [PythonYeardayDef, CythonYeardayDef],
    [PythonFromordinalDef, CythonFromordinalDef],
    [PythonToordinalDef, CythonToordinalDef],
    [PythonOffsetDef, CythonOffsetDef],
    [PythonIncrementDef, CythonIncrementDef],
    [PythonDaterangeDef, CythonDaterangeDef],
]
