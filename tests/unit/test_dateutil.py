import cythonpowered.dateutil
import datetime
import calendar


def test_today():
    one = datetime.date.today()
    two = cythonpowered.dateutil.date.today()
    assert one.year == two.year
    assert one.month == two.month
    assert one.day == two.day


def test_isleap():
    for y in range(2000, 2010):
        assert calendar.isleap(y) == cythonpowered.dateutil.date.isleap(y)


def test_monthrange():
    for y in [2000, 2001]:
        for m in range(1, 13):
            one = calendar.monthrange(y, m)
            two = cythonpowered.dateutil.date.monthrange(y, m)
            assert one == two


def test_fromstring():
    datestring = "2022-02-02"
    one = datetime.datetime.strptime(datestring, "%Y-%m-%d").date()
    two = cythonpowered.dateutil.date.fromstring(datestring)
    assert one.year == two.year
    assert one.month == two.month
    assert one.day == two.day


def test_tostring():
    datestring = "2022-02-02"
    one = datetime.date(2022, 2, 2).strftime("%Y-%m-%d")
    two = cythonpowered.dateutil.date(2022, 2, 2).tostring()
    assert one == datestring
    assert two == datestring


def test_weekday():
    year = 2026
    month = 1
    for d in range(1, 32):  # a full month
        test_pydate = datetime.date(year, month, d)
        test_cydate = cythonpowered.dateutil.date(year, month, d)
        assert test_pydate.weekday() == test_cydate.weekday()


def test_yearday():
    for year in [2000, 2001]:
        for month in range(1, 13):
            rng = calendar.monthrange(year, month)[1] + 1
            for day in range(1, rng):
                test_pydate = datetime.date(year, month, day)
                test_cydate = cythonpowered.dateutil.date(year, month, day)
                assert test_pydate.timetuple().tm_yday == test_cydate.yearday()


def test_fromordinal():
    for i in range(1, 1000000):
        test_pydate = datetime.date.fromordinal(i)
        test_cydate = cythonpowered.dateutil.date.fromordinal(i)
        assert test_pydate.year == test_cydate.year
        assert test_pydate.month == test_cydate.month
        assert test_pydate.day == test_cydate.day


def test_toordinal():
    for i in range(1, 1000000):
        test_pydate = datetime.date.fromordinal(i)
        test_cydate = cythonpowered.dateutil.date(
            test_pydate.year, test_pydate.month, test_pydate.day
        )
        assert test_cydate.toordinal() == i


def test_offset():
    test_pydate = datetime.date(2026, 1, 1)
    test_cydate = cythonpowered.dateutil.date(2026, 1, 1)
    for i in range(-5000, 5000):
        offset_pydate = test_pydate + datetime.timedelta(days=i)
        offset_cydate = test_cydate.offset(i)
        assert offset_pydate.year == offset_cydate.year
        assert offset_pydate.month == offset_cydate.month
        assert offset_pydate.day == offset_cydate.day
