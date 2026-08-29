# -----------------------------------------------------------------------------
# Fast replacements for date utilities from Python's `datetime` and
# `calendar` modules, plus a small subset of pandas.date_range.
#
# Invariant: every `date` instance holds a valid Gregorian date
# (1 <= year <= 9999, 1 <= month <= 12, 1 <= day <= days in month),
# enforced exactly once in `date.__init__`. The internal cdef helpers rely
# on this invariant and do not re-validate fields, which is what makes
# their lookups into the static C tables below safe without bounds checks
# (boundscheck does not apply to typed C arrays).
# -----------------------------------------------------------------------------
import time
import datetime

from cpython.unicode cimport (
    PyUnicode_New,
    PyUnicode_DATA,
    PyUnicode_WRITE,
    PyUnicode_1BYTE_KIND
)


# -----------------------------------------------------------------------------
# Days per month in a non-leap year (index 0 = January). February is
# corrected by c_days_in_month().
cdef unsigned char[12] c_month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

cdef inline bint c_isleap(unsigned short yr):
    # Gregorian leap-year rule: divisible by 4, except centuries that are
    # not divisible by 400.
    return yr % 400 == 0 or (yr % 100 != 0 and yr % 4 == 0)


cdef inline unsigned char c_days_in_month(unsigned short year, unsigned char month):
    # Number of days in the given month. month must be in 1..12 (validated
    # at the public boundary) because c_month_days is a C array whose
    # indexing is never bounds-checked.
    if month == 2:
        return 28 + c_isleap(year)
    return c_month_days[month - 1]
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# Sakamoto month offsets for the weekday algorithm.
cdef unsigned char[12] weekday_helper = [0, 3, 2, 5, 0, 3, 5, 1, 4, 6, 2, 4]

cdef inline unsigned char c_weekday(date d):
    # Returns the weekday (Monday = 0 ... Sunday = 6).
    # Replacement for: datetime.date.weekday()
    # Based on the Sakamoto algorithm:
    # https://en.wikipedia.org/wiki/Determination_of_the_day_of_the_week
    # d is a valid date (validated in date.__init__), so the table index
    # month - 1 is in 0..11 and the year decrement cannot underflow.
    cdef unsigned short y = d._year
    if d._month < 3:
        y -= 1
    cdef char wd = ((y + y // 4 - y // 100 + y // 400 + weekday_helper[d._month - 1] + d._day) % 7) - 1
    return 6 if wd < 0 else wd
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# Cumulative days before each month in a non-leap year (index 0 = January).
cdef unsigned short[12] yearday_helper = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]

cdef inline unsigned short c_yearday(date d):
    # Returns the day of the year (1..366).
    # Replacement for: datetime.date().timetuple().tm_yday
    # d is a valid date, so the table index month - 1 is in 0..11.
    cdef unsigned short elapsed = yearday_helper[d._month - 1] + d._day
    if d._month >= 3:
        elapsed += c_isleap(d._year)
    return elapsed
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
cdef class date:
    # Replacement for Python's datetime.date class, with reduced functionality.
    # Fields are validated in __init__ (same ValueError behavior as
    # datetime.date) and exposed as read-only properties, like datetime.date.
    cdef unsigned short _year
    cdef unsigned char _month
    cdef unsigned char _day

    def __init__(self, int year, int month, int day):
        # Same validation and exception type as datetime.date.
        if year < 1 or year > 9999:
            raise ValueError(f"year {year} is out of range")
        if month < 1 or month > 12:
            raise ValueError("month must be in 1..12")
        if day < 1 or day > c_days_in_month(<unsigned short>year, <unsigned char>month):
            raise ValueError("day is out of range for month")
        self._year = year
        self._month = month
        self._day = day

    @property
    def year(self):
        # The year (1..9999), read-only like datetime.date.year.
        return self._year

    @property
    def month(self):
        # The month (1..12), read-only like datetime.date.month.
        return self._month

    @property
    def day(self):
        # The day (1..31), read-only like datetime.date.day.
        return self._day

    def __repr__(self):
        # Returns date(year, month, day) format, like datetime.date's
        # repr but without the "datetime." module prefix (this class is
        # named `date`, so `date(...)` is the standard ClassName(args) form).
        return f"date({self._year}, {self._month}, {self._day})"

    def __str__(self):
        # Returns "YYYY-MM-DD" format, matching datetime.date.isoformat()
        return self.tostring()

    def __eq__(self, other):
        # Supports comparison with both cythonpowered date and datetime.date
        cdef date o
        if isinstance(other, date):
            o = other
            return (self._year == o._year and
                    self._month == o._month and
                    self._day == o._day)
        if isinstance(other, datetime.date):
            return (self._year == other.year and
                    self._month == other.month and
                    self._day == other.day)
        return NotImplemented

    def __hash__(self):
        # Must match datetime.date's hash to satisfy Python's hash/equality
        # contract, since __eq__ compares against datetime.date instances.
        # Delegates to the stdlib hash (safe: fields are validated in __init__).
        return hash(datetime.date(self._year, self._month, self._day))

    @staticmethod
    def today():
        # Returns today's local date.
        # Replacement for: datetime.date.today()
        return cp_today()

    @staticmethod
    def isleap(year):
        # Checks if a given year is a leap year.
        # Replacement for: calendar.isleap()
        return cp_isleap(year)

    @staticmethod
    def monthrange(year, month):
        # Returns (first weekday, days in month) for a year/month.
        # Replacement for: calendar.monthrange()
        return cp_monthrange(year, month)

    @staticmethod
    def fromstring(yyyy_mm_dd):
        # Parses a zero-padded "YYYY-MM-DD" string into a date.
        # Replacement for: datetime.datetime.strptime(st, "%Y-%m-%d").date()
        return cp_fromstring(yyyy_mm_dd)

    @staticmethod
    def fromordinal(ordinal):
        # Returns the date for a proleptic Gregorian ordinal (>= 1).
        # Replacement for: datetime.date.fromordinal()
        return cp_fromordinal(ordinal)

    @staticmethod
    def date_range(date start, date end, str freq="D"):
        # Returns period-end dates between start and end (inclusive).
        # Replacement for: pandas.date_range()
        return cp_date_range(start=start, end=end, freq=freq)

    cpdef tostring(self, str separator="-"):
        # Returns a "YYYY-MM-DD" style string with the given separator.
        # Replacement for: datetime.date().strftime("%Y-%m-%d")
        return c_tostring(self, separator)

    cpdef int weekday(self):
        # Returns the weekday as an integer (Monday = 0 ... Sunday = 6).
        # Replacement for: datetime.date().weekday()
        return c_weekday(self)

    cpdef int yearday(self):
        # Returns the day of the year (1..366).
        # Replacement for: datetime.date().timetuple().tm_yday
        return c_yearday(self)

    cpdef int toordinal(self):
        # Returns the proleptic Gregorian ordinal (>= 1).
        # Replacement for: datetime.date().toordinal()
        return c_toordinal(self)

    cpdef date offset(self, int years=0, int months=0, int weeks=0, int days=0):
        # Returns a new date offset by years/months/weeks/days (input is not
        # mutated). years/months behave like relativedelta: the day is
        # clamped to the last day of the target month.
        # Replacement for: datetime.date() +/- datetime.timedelta()
        return c_offset(self, years=years, months=months, weeks=weeks, days=days)

    cpdef date increment(self):
        # Returns the date plus one day.
        # Replacement for: datetime.date() + datetime.timedelta(days=1)
        return c_increment(self)
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
cpdef inline date cp_today():
    # Returns today's local date.
    # Replacement for: datetime.date.today()
    # Uses time.localtime() which always returns the current local time.
    # No cached offset — correct even if the timezone changes after import.
    cdef object st = time.localtime()
    return date(st.tm_year, st.tm_mon, st.tm_mday)
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
cpdef inline int cp_isleap(int year):
    # Checks if a given year is a leap year.
    # Replacement for: calendar.isleap()
    # Computed with Python (floor) division semantics, matching
    # calendar.isleap() for all 32-bit years (including negative ones).
    return year % 400 == 0 or (year % 100 != 0 and year % 4 == 0)
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
cdef inline tuple c_monthrange(unsigned short year, unsigned char month):
    # month is in 1..12 (validated by cp_monthrange), so the date
    # constructor and the c_weekday table lookup are safe.
    cdef unsigned char first_weekday = c_weekday(date(year, month, 1))
    return first_weekday, c_days_in_month(year, month)


cpdef inline tuple cp_monthrange(int year, int month):
    # Returns a tuple containing the first weekday and the number of days
    # in the month.
    # Replacement for: calendar.monthrange()
    # Raises ValueError for an invalid month, like calendar.monthrange
    # (which raises IllegalMonthError, a ValueError subclass). The year is
    # restricted to 1..9999 (like datetime.date), unlike calendar, which
    # accepts any year.
    if month < 1 or month > 12:
        raise ValueError("month must be in 1..12")
    if year < 1 or year > 9999:
        raise ValueError(f"year {year} is out of range")
    return c_monthrange(<unsigned short>year, <unsigned char>month)
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
cdef inline date c_fromstring(str yyyy_mm_dd):
    # Parses a zero-padded "YYYY-MM-DD" string. The fields are read from
    # fixed positions, so any single-character separator works. Malformed
    # input raises ValueError, like strptime: the shape is checked
    # explicitly (exactly 10 characters, non-digit separators at positions
    # 4 and 7 — a digit there would be ambiguous with a missing
    # separator), then int() rejects non-numeric fields and the date
    # constructor rejects out-of-range fields.
    if len(yyyy_mm_dd) != 10 or yyyy_mm_dd[4].isdigit() or yyyy_mm_dd[7].isdigit():
        raise ValueError(f"expected a zero-padded 'YYYY-MM-DD' string, got {yyyy_mm_dd!r}")
    cdef int year = int(yyyy_mm_dd[0:4])
    cdef int month = int(yyyy_mm_dd[5:7])
    cdef int day = int(yyyy_mm_dd[8:10])
    return date(year, month, day)


cpdef inline date cp_fromstring(str yyyy_mm_dd):
    # Given a zero-padded string like "yyyy-mm-dd" (any single non-digit
    # separator character), returns a date.
    # Replacement for: datetime.datetime.strptime(st, "%Y-%m-%d").date()
    # Deviation: unlike strptime, the fields must be zero-padded.
    return c_fromstring(yyyy_mm_dd)
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
cdef inline str c_tostring(date d, str separator="-"):
    # Returns a "YYYY-MM-DD" style string (4-digit year, 2-digit month and
    # day), built directly in a C unicode buffer to avoid Python string
    # conversions.
    # Replacement for: datetime.date().strftime("%Y-%m-%d")
    # Deviation: the year is always zero-padded to 4 digits (like
    # isoformat()), while strftime("%Y") skips padding for years < 1000 on
    # some platforms (e.g. glibc).
    # The separator must be a single character with code point < 256: the
    # result buffer is created with the 1-byte (Latin-1) unicode kind, so
    # anything wider would be silently truncated.
    cdef Py_ssize_t sep_len = len(separator)
    if sep_len != 1:
        raise ValueError(f"separator must be a single character, got {separator!r}")
    cdef unsigned int sep = ord(separator[0])
    if sep > 255:
        raise ValueError(
            f"separator must have code point < 256 (1-byte unicode buffer), got {separator!r}"
        )

    cdef unsigned short y = d._year
    cdef unsigned char m = d._month
    cdef unsigned char day = d._day

    cdef object s = PyUnicode_New(10, 127)
    cdef void* data = PyUnicode_DATA(s)

    PyUnicode_WRITE(PyUnicode_1BYTE_KIND, data, 0, 48 + y // 1000)
    PyUnicode_WRITE(PyUnicode_1BYTE_KIND, data, 1, 48 + (y // 100) % 10)
    PyUnicode_WRITE(PyUnicode_1BYTE_KIND, data, 2, 48 + (y // 10) % 10)
    PyUnicode_WRITE(PyUnicode_1BYTE_KIND, data, 3, 48 + y % 10)
    PyUnicode_WRITE(PyUnicode_1BYTE_KIND, data, 4, sep)
    PyUnicode_WRITE(PyUnicode_1BYTE_KIND, data, 5, 48 + m // 10)
    PyUnicode_WRITE(PyUnicode_1BYTE_KIND, data, 6, 48 + m % 10)
    PyUnicode_WRITE(PyUnicode_1BYTE_KIND, data, 7, sep)
    PyUnicode_WRITE(PyUnicode_1BYTE_KIND, data, 8, 48 + day // 10)
    PyUnicode_WRITE(PyUnicode_1BYTE_KIND, data, 9, 48 + day % 10)

    return <str>s
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
cdef inline unsigned int c_toordinal(date d):
    # Returns the proleptic Gregorian ordinal (1..3652059).
    # Replacement for: datetime.date().toordinal()
    # d._year is in 1..9999 (validated in date.__init__), so year - 1
    # cannot underflow and the result fits in unsigned int.
    cdef unsigned short y = d._year - 1
    cdef unsigned int ordinal = 365 * y + y // 4 - y // 100 + y // 400 + c_yearday(d)
    return ordinal
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
cdef inline date c_fromordinal(unsigned int ordinal):
    # Inverse of c_toordinal (classic quadricentennial decomposition).
    # ordinal is in 1..3652059 (validated by cp_fromordinal), so every
    # intermediate value fits its declared C type and the month walk below
    # cannot run past December.
    cdef int day = ordinal - 1

    cdef unsigned char quadricentennial = day // 146097
    day -= quadricentennial * 146097

    cdef unsigned char centennial = day // 36524
    if centennial > 3:
        centennial = 3
    day -= centennial * 36524

    cdef unsigned short quadrennial = day // 1461
    day -= quadrennial * 1461

    cdef unsigned char annual = day // 365
    if annual > 3:
        annual = 3
    day -= annual * 365

    cdef unsigned short year = (
        quadricentennial * 400 +
        centennial * 100 +
        quadrennial * 4 +
        annual + 1
    )

    day += 1

    cdef unsigned char month = 1
    while day > c_days_in_month(year, month):
        day -= c_days_in_month(year, month)
        month += 1

    return date(year, month, day)


cpdef inline date cp_fromordinal(int ordinal):
    # Returns the date for a proleptic Gregorian ordinal.
    # Replacement for: datetime.date.fromordinal()
    # Raises ValueError outside 1..3652059, like datetime.date.fromordinal.
    # (3652059 is datetime.date.max.toordinal().)
    if ordinal < 1:
        raise ValueError("ordinal must be >= 1")
    if ordinal > 3652059:
        raise ValueError("ordinal must be <= 3652059")
    return c_fromordinal(<unsigned int>ordinal)
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
cdef inline date c_offset(date d, int years=0, int months=0, int weeks=0, int days=0):
    # Returns a new date offset by the given amounts; the input is not
    # mutated (datetime.date is immutable). years/months behave like
    # dateutil's relativedelta: the day is clamped to the last day of the
    # target month. Raises OverflowError when the result falls outside
    # 1..9999, like datetime.date() +/- datetime.timedelta().
    # Replacement for: datetime.date() +/- datetime.timedelta()
    cdef int total_months = years * 12 + months
    cdef int days_offset = weeks * 7 + days
    cdef int year = d._year
    cdef int month = d._month
    cdef int day = d._day
    cdef int month_end

    if total_months == 0 and days_offset == 0:
        return d

    if total_months != 0:
        month += total_months
        # Normalize month to 1..12, carrying the remainder into the year.
        # Floor division/modulo (cdivision=False) keeps negative offsets in
        # the correct year (e.g. January minus one month -> previous December).
        year += (month - 1) // 12
        month = (month - 1) % 12 + 1
        if year < 1 or year > 9999:
            raise OverflowError("date value out of range")
        month_end = c_days_in_month(<unsigned short>year, <unsigned char>month)
        if day > month_end:
            day = month_end

    cdef int ordinal = c_toordinal(date(year, month, day)) + days_offset
    if ordinal < 1 or ordinal > 3652059:
        raise OverflowError("date value out of range")
    return c_fromordinal(<unsigned int>ordinal)
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
cdef inline date c_increment(date d):
    # Returns the date plus one day, without a toordinal/fromordinal
    # round-trip. Intended as a fast alternative to c_offset for this
    # special use case (also used internally by c_date_range).
    # Replacement for: datetime.date() + datetime.timedelta(days=1)
    cdef unsigned char month_end = c_days_in_month(d._year, d._month)
    if d._day < month_end:
        return date(d._year, d._month, d._day + 1)
    if d._month < 12:
        return date(d._year, d._month + 1, 1)
    if d._year < 9999:
        return date(d._year + 1, 1, 1)
    raise OverflowError("date value out of range")
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
cdef inline list c_date_range(date start, date end, str freq):
    # Builds the list of period-end dates between start and end (inclusive),
    # like pandas.date_range. Returns an empty list when start > end, like
    # pandas.date_range. The supported frequencies mirror pandas:
    #   D  = daily, W = week-ending-Sunday, ME = month-end,
    #   QE = calendar quarter-end (QE-DEC), YE = year-end,
    #   SE = six-month period-end. Note: pandas also has an "SE" alias,
    #       but it means SemiMonthEnd (15th + month end), a different
    #       concept, so SE here is not cross-validated against pandas.
    cdef list period_ends = []
    cdef date period_start = date(start._year, start._month, start._day)
    cdef date period_end
    cdef date cursor
    cdef int i
    cdef int days_to_sunday
    cdef unsigned int startnum = c_toordinal(start)
    cdef unsigned int endnum = c_toordinal(end)
    cdef unsigned int pendnum

    if freq not in ("D", "W", "ME", "QE", "SE", "YE"):
        raise ValueError(f"Invalid frequency: {freq}")

    if startnum > endnum:
        return period_ends

    ### freq means days
    if freq == "D":
        period_ends.append(start)
        cursor = start
        for i in range(1, endnum - startnum + 1):
            cursor = c_increment(cursor)
            period_ends.append(cursor)
        return [dt.tostring() for dt in period_ends]

    ### freq means weeks (pandas freq="W" is week-ending-Sunday)
    if freq == "W":
        while True:
            days_to_sunday = 6 - c_weekday(period_start)
            # If the week end would go past 9999-12-31 it is necessarily
            # past `end` as well, so stop instead of overflowing.
            if c_toordinal(period_start) + days_to_sunday > 3652059:
                break
            period_end = c_offset(period_start, 0, 0, 0, days_to_sunday)
            pendnum = c_toordinal(period_end)
            if pendnum <= endnum:
                period_ends.append(period_end)
                # Period ends are strictly increasing, so once one equals
                # `end` all later ones are past it. Stopping here also avoids
                # incrementing 9999-12-31, which would overflow.
                if pendnum == endnum:
                    break
                period_start = c_increment(period_end)
            else:
                break

    ### freq means months
    if freq == "ME":
        while True:
            period_end = date(
                period_start._year,
                period_start._month,
                c_days_in_month(period_start._year, period_start._month),
            )
            pendnum = c_toordinal(period_end)
            if pendnum <= endnum:
                period_ends.append(period_end)
                # Period ends are strictly increasing, so once one equals
                # `end` all later ones are past it. Stopping here also avoids
                # incrementing 9999-12-31, which would overflow.
                if pendnum == endnum:
                    break
                period_start = c_increment(period_end)
            else:
                break

    ### freq means quarters (calendar quarters, like pandas QE-DEC)
    if freq == "QE":
        while True:
            if period_start._month >= 10:
                period_end = date(period_start._year, 12, 31)
            elif period_start._month >= 7:
                period_end = date(period_start._year, 9, 30)
            elif period_start._month >= 4:
                period_end = date(period_start._year, 6, 30)
            else:
                period_end = date(period_start._year, 3, 31)
            pendnum = c_toordinal(period_end)
            if pendnum <= endnum:
                period_ends.append(period_end)
                # Period ends are strictly increasing, so once one equals
                # `end` all later ones are past it. Stopping here also avoids
                # incrementing 9999-12-31, which would overflow.
                if pendnum == endnum:
                    break
                period_start = c_increment(period_end)
            else:
                break

    ### freq means six-month periods (pandas' "SE" means SemiMonthEnd, not this)
    if freq == "SE":
        while True:
            if period_start._month >= 7:
                period_end = date(period_start._year, 12, 31)
            else:
                period_end = date(period_start._year, 6, 30)
            pendnum = c_toordinal(period_end)
            if pendnum <= endnum:
                period_ends.append(period_end)
                # Period ends are strictly increasing, so once one equals
                # `end` all later ones are past it. Stopping here also avoids
                # incrementing 9999-12-31, which would overflow.
                if pendnum == endnum:
                    break
                period_start = c_increment(period_end)
            else:
                break

    ### freq means years
    if freq == "YE":
        while True:
            period_end = date(period_start._year, 12, 31)
            pendnum = c_toordinal(period_end)
            if pendnum <= endnum:
                period_ends.append(period_end)
                # Period ends are strictly increasing, so once one equals
                # `end` all later ones are past it. Stopping here also avoids
                # incrementing 9999-12-31, which would overflow.
                if pendnum == endnum:
                    break
                period_start = c_increment(period_end)
            else:
                break

    return [dt.tostring() for dt in period_ends]


cpdef inline list cp_date_range(date start, date end, str freq="D"):
    # Returns period-end dates between start and end (inclusive), as a list
    # of "YYYY-MM-DD" strings.
    # Replacement for: pandas.date_range()
    # Supports days, weeks, months, quarters, semesters, years
    # (freq in [D, W, ME, QE, SE, YE]). Raises ValueError for an unknown
    # frequency, like pandas.date_range.
    return c_date_range(start=start, end=end, freq=freq)
# -----------------------------------------------------------------------------
