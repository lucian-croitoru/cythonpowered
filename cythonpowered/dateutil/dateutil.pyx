import time
from functools import lru_cache


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
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
cdef inline unsigned int c_today_seconds():
    cdef double t = time.time()
    return int(t // 86400 * 86400)

@lru_cache(maxsize=1)
def c_cached_today(unsigned int s):
    cdef d = time.localtime(s)
    return date(d.tm_year, d.tm_mon, d.tm_mday + 1)

cdef inline date c_today():
    cdef unsigned int s = c_today_seconds()
    return c_cached_today(s)

cpdef inline date cp_today():
    # Multi-function solution to get the current date
    # Replacement for datetime.date.today()
    return c_today()
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


# -----------------------------------------------------------------------
cdef date c_fromstring(str yyyy_mm_dd):
    cdef unsigned short year = int(yyyy_mm_dd[0:4])
    cdef unsigned char month = int(yyyy_mm_dd[5:7])
    cdef unsigned char day = int(yyyy_mm_dd[8:10])
    return date(year, month, day)

cpdef date cp_fromstring(str yyyy_mm_dd):
    # Given a string like yyyy-mm-dd (or with any separator), returns a date
    # Replacement for datetime.datetime.strptime(st,'%Y-%m-%d').date()
    return c_fromstring(yyyy_mm_dd)
# -----------------------------------------------------------------------


# -----------------------------------------------------------------------
cdef str c_tostring(date date, str separator = "-"):
# Returns a date string similar to datetime.date().strftime('%Y-%m-%d')
    cdef str datestr = str(date.year) + separator
    if date.month < 10:
        datestr += '0'
    datestr += str(date.month) + separator
    if date.day < 10:
        datestr += '0'
    datestr += str(date.day)
    return datestr
# -----------------------------------------------------------------------


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
