import time
import datetime

from cpython.unicode cimport (
    PyUnicode_New,
    PyUnicode_DATA,
    PyUnicode_WRITE,
    PyUnicode_1BYTE_KIND
)

# -----------------------------------------------------------------------------
cdef class date:
    # Replacement for Python's datetime.date class, with reduced functionality
    cdef public unsigned short year
    cdef public unsigned char month
    cdef public unsigned char day

    def __init__(self, unsigned short year, unsigned char month, unsigned char day):
        self.year = year
        self.month = month
        self.day = day

    def __repr__(self):
        # Returns date(year, month, day) format, matching datetime.date
        return f"date({self.year}, {self.month}, {self.day})"

    def __str__(self):
        # Returns "YYYY-MM-DD" format, matching date.tostring()
        return self.tostring()

    def __eq__(self, other):
        # Supports comparison with both cythonpowered date and datetime.date
        if isinstance(other, date):
            return (self.year == other.year and
                    self.month == other.month and
                    self.day == other.day)
        if isinstance(other, datetime.date):
            return (self.year == other.year and
                    self.month == other.month and
                    self.day == other.day)
        return NotImplemented

    def __hash__(self):
        # Must match datetime.date hash to satisfy Python's hash/equality contract
        # since __eq__ compares with datetime.date instances
        return hash(datetime.date(self.year, self.month, self.day))
    
    @staticmethod
    def today():
        return cp_today()
    
    @staticmethod
    def isleap(year):
        return cp_isleap(year)
    
    @staticmethod
    def monthrange(year, month):
        return cp_monthrange(year, month)
    
    @staticmethod
    def fromstring(yyyy_mm_dd):
        return cp_fromstring(yyyy_mm_dd)
    
    cpdef tostring(self, separator = "-"):
        return c_tostring(self, separator)

    cpdef weekday(self):
        return c_weekday(self)
    
    cpdef yearday(self):
        return c_yearday(self)
    
    @staticmethod
    def fromordinal(ordinal):
        return cp_fromordinal(ordinal)
    
    cpdef toordinal(self):
        return c_toordinal(self)
    
    cpdef offset(self, short years=0, short months=0, short weeks=0, short days=0):
        return c_offset(self, years=years, months=months, weeks=weeks, days=days)
    
    cpdef increment(self):
        return c_increment(self)
    
    @staticmethod
    def date_range(date start, date end, str freq="D"):
        return cp_date_range(start=start, end=end, freq=freq)

# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
cpdef inline date cp_today():
    # Replacement for datetime.date.today()
    # Uses time.localtime() which always returns current local time
    # No cached offset — correct even if timezone changes after import
    cdef object st = time.localtime()
    return date(st.tm_year, st.tm_mon, st.tm_mday)
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
cdef inline unsigned char c_isleap(unsigned short yr):
    return yr % 400 == 0 or (yr % 100 != 0 and yr % 4 == 0)

cpdef inline unsigned char cp_isleap(unsigned short yr):
    # Checks if a given year is a leap year
    # Replacement for calendar.isleap()
    return c_isleap(yr)
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
cdef inline tuple c_monthrange(unsigned short year, unsigned char month):
    cdef first_weekeday = date(year, month, 1).weekday()
    if month in {1, 3, 5, 7, 8, 10, 12}:
        return first_weekeday, 31
    if month in {4, 6, 9, 11}:
        return first_weekeday, 30
    return first_weekeday, 28 + c_isleap(year)

cpdef inline tuple cp_monthrange(unsigned short year, unsigned char month):
    # Returns a tuple containing the first weekday and the number of days in the month
    # Replacement for calendar.monthrange()
    return c_monthrange(year, month)
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
cdef inline date c_fromstring(str yyyy_mm_dd):
    cdef unsigned short year = int(yyyy_mm_dd[0:4])
    cdef unsigned char month = int(yyyy_mm_dd[5:7])
    cdef unsigned char day = int(yyyy_mm_dd[8:10])
    return date(year, month, day)

cpdef inline date cp_fromstring(str yyyy_mm_dd):
    # Given a string like yyyy-mm-dd (or with any separator), returns a date
    # Replacement for datetime.datetime.strptime(st,'%Y-%m-%d').date()
    return c_fromstring(yyyy_mm_dd)
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
cdef inline str c_tostring(date d, str separator="-"):
    # Returns a date string similar to datetime.date().strftime('%Y-%m-%d')
    # Builds the string directly in C, avoids Python string conversions
    cdef unsigned short y = d.year
    cdef unsigned char m = d.month
    cdef unsigned char day = d.day

    cdef object s = PyUnicode_New(10, 127)
    cdef void* data = PyUnicode_DATA(s)

    PyUnicode_WRITE(PyUnicode_1BYTE_KIND, data, 0, 48 + y // 1000)
    PyUnicode_WRITE(PyUnicode_1BYTE_KIND, data, 1, 48 + (y // 100) % 10)
    PyUnicode_WRITE(PyUnicode_1BYTE_KIND, data, 2, 48 + (y // 10) % 10)
    PyUnicode_WRITE(PyUnicode_1BYTE_KIND, data, 3, 48 + y % 10)
    PyUnicode_WRITE(PyUnicode_1BYTE_KIND, data, 4, separator)
    PyUnicode_WRITE(PyUnicode_1BYTE_KIND, data, 5, 48 + m // 10)
    PyUnicode_WRITE(PyUnicode_1BYTE_KIND, data, 6, 48 + m % 10)
    PyUnicode_WRITE(PyUnicode_1BYTE_KIND, data, 7, separator)
    PyUnicode_WRITE(PyUnicode_1BYTE_KIND, data, 8, 48 + day // 10)
    PyUnicode_WRITE(PyUnicode_1BYTE_KIND, data, 9, 48 + day % 10)

    return <str>s
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
cdef inline unsigned char[12] weekday_helper = [0, 3, 2, 5, 0, 3, 5, 1, 4, 6, 2, 4]

cdef inline unsigned char c_weekday(date date):
    # Replacement for Python's datetime.date.weekday()
    # based on the Sakamoto algorithm:
    # https://en.wikipedia.org/wiki/Determination_of_the_day_of_the_week
    # returns Monday = 0, Tuesday = 1... Sunday = 6
    cdef unsigned short y = date.year
    if date.month < 3:
        y -= 1
    cdef char wd = ((y + y//4 - y//100 + y//400 + weekday_helper[date.month - 1] + date.day) % 7) - 1
    return 6 if wd < 0 else wd
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
cdef inline unsigned short[12] yearday_helper = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]

cdef inline unsigned short c_yearday(date date):
    # Returns the day of the year from a given date
    # Replaces datetime.date().timetuple().tm_yday
    cdef unsigned short elapsed = yearday_helper[date.month - 1] + date.day
    if date.month >= 3:
        elapsed += date.isleap(date.year)
    return elapsed
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
cdef inline date c_fromordinal(unsigned int ordinal):
    cdef int day = ordinal - 1

    cdef unsigned char quadricentennial = day // 146097
    day -= quadricentennial * 146097

    cdef unsigned char centennial = day // 36524
    if centennial > 3:
        centennial = 3
    day -= centennial * 36524

    cdef unsigned short quadrennial = day // 1461
    day -= quadrennial * 1461

    cdef unsigned short annual = day // 365
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
    cdef unsigned char[12] month_lengths = [31,28,31,30,31,30,31,31,30,31,30,31]

    if c_isleap(year):
        month_lengths[1] = 29

    while day > month_lengths[month - 1]:
        day -= month_lengths[month - 1]
        month += 1

    return date(year, month, day)


cpdef inline date cp_fromordinal(unsigned int ordinal):
    # Replacement for datetime.date.fromordinal()
    # May actually be slower, but it is required internally to speedup other functions
    return c_fromordinal(ordinal)
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
cdef inline unsigned int c_toordinal(date date):
    # Replacement for datetime.date().toordinal()
    # May actually be slower, but it is required internally to speedup other functions
    cdef unsigned short y = date.year - 1
    cdef unsigned int ordinal = 365 * y + y // 4 - y // 100 + y // 400 + c_yearday(date)
    return ordinal
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
cdef inline date c_offset(date date, short years=0, short months=0, short weeks=0, short days=0):
    # Replacement for datetime.date() +/- datetime.timedelta()
    # Supports extra arguments: `years` and `months`
    cdef unsigned char[12] month_lengths = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    cdef unsigned int ordinal
    cdef int days_offset = weeks * 7 + days

    if years != 0 or months != 0:
        date.year = date.year + years + months // 12
        date.month = date.month + months % 12
        if c_isleap(date.year):
            month_lengths[1] = 29
        if date.day > month_lengths[date.month-1]:
            date.day = month_lengths[date.month-1]
    
    if days_offset != 0:
        ordinal = c_toordinal(date) + days_offset
        return c_fromordinal(ordinal)
    
    return date
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
cdef inline date c_increment(date input_date):
    # Adds one day to a given date, without using fromordinal() or toordinal()
    # Intended as a fast alternative to date.offset() for this special use case
    cdef date newdate = date(input_date.year, input_date.month, input_date.day)
    cdef unsigned char mr = c_monthrange(newdate.year, newdate.month)[1]
    
    newdate.day += 1
    if newdate.day <= mr:
        return newdate
    else:
        newdate.day = 1
        newdate.month += 1
        if newdate.month > 12:
            newdate.year += 1
            newdate.month = 1
        return newdate
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
cdef inline list c_date_range(date start, date end, str freq="D"):
    cdef list period_ends = []
    cdef unsigned int i
    cdef str d
    cdef date dt
    cdef int startnum, endnum
    cdef date period_end = date(start.year, start.month, start.day)
    cdef date period_start = date(start.year, start.month, start.day)

    ### freq means days
    if freq == "D":
        startnum = start.toordinal()
        endnum = end.toordinal()
        period_ends = [start]

        for i in range(1, endnum - startnum + 1):
            period_end = c_increment(period_end)
            period_ends.append(period_end)
        period_ends = [dt.tostring() for dt in period_ends]
        return period_ends


    cdef unsigned int edatenum = end.toordinal()
    cdef unsigned int pendnum
    cdef unsigned int length


    ### freq means weeks
    if freq == "W":    
        while True:
            period_end = period_start.offset(days = 6 - period_start.weekday())
            
            pendnum = period_end.toordinal()
            
            if pendnum <= edatenum:
                period_ends.append(period_end)
                period_start = c_increment(period_end)
            else:
                break


    ### freq means months
    if freq == "ME":
        while True:
            period_end = date(period_start.year, period_start.month, c_monthrange(period_start.year, period_start.month)[1])
            
            pendnum = period_end.toordinal()
            
            if pendnum <= edatenum:
                period_ends.append(period_end)
                period_start = c_increment(period_end)
            else:
                break


    ### freq means quarters
    if freq == "QE":     
        while True:
            if period_start.month >= 10:
                period_end = date(period_start.year, 12, 31)
            if period_start.month >= 7 and period_start.month <= 9:
                period_end = date(period_start.year, 9, 30)
            if period_start.month >= 4 and period_start.month <= 6:
                period_end = date(period_start.year, 6, 30)
            if period_start.month <= 3:
                period_end = date(period_start.year, 3, 31)

            pendnum = period_end.toordinal()
            
            if pendnum <= edatenum:
                period_ends.append(period_end)
                period_start = c_increment(period_end)
            else:
                break


    ### freq means semesters
    if freq == "SE": 
        while True:
            if period_start.month >= 7:
                period_end = date(period_start.year, 12, 31)
            else:
                period_end = date(period_start.year, 6, 30)
            
            pendnum = period_end.toordinal()
            
            if pendnum <= edatenum:
                period_ends.append(period_end)
                period_start = c_increment(period_end)
            else:
                break


    ### freq means years
    if freq == "YE":
        while True:
            period_end = date(period_start.year, 12, 31)

            pendnum = period_end.toordinal()
            
            if pendnum <= edatenum:
                period_ends.append(period_end)
                period_start = c_increment(period_end)
            else:
                break

    length = len(period_ends)
    return [period_ends[i].tostring() for i in range(0, length)]


cpdef inline list cp_date_range(date start, date end, str freq="D"):
    # Replacement for pandas.date_range()
    # Supports days, weeks, months, quarters, semesters, years (freq in [D, W, ME, QE, SE, YE])
    return c_date_range(start=start, end=end, freq=freq)
# -----------------------------------------------------------------------------
