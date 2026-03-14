import cythonpowered.dateutil
import datetime
import calendar
import pandas


def test_today():
    one = datetime.date.today()
    two = cythonpowered.dateutil.date.today()
    assert one.year == two.year
    assert one.month == two.month
    assert one.day == two.day


def test_isleap():
    for y in range(1900, 2100):
        assert calendar.isleap(y) == cythonpowered.dateutil.date.isleap(y)


def test_monthrange():
    for y in [2000, 2001]:
        for m in range(1, 13):
            one = calendar.monthrange(y, m)
            two = cythonpowered.dateutil.date.monthrange(y, m)
            assert one == two


def test_fromstring():
    datestring = "2026-01-01"
    one = datetime.datetime.strptime(datestring, "%Y-%m-%d").date()
    two = cythonpowered.dateutil.date.fromstring(datestring)
    assert one.year == two.year
    assert one.month == two.month
    assert one.day == two.day


def test_tostring():
    datestring = "2026-01-01"
    one = datetime.date(2026, 1, 1).strftime("%Y-%m-%d")
    two = cythonpowered.dateutil.date(2026, 1, 1).tostring()
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


def test_offset_days_weeks():
    test_pydate = datetime.date(2026, 1, 1)
    test_cydate = cythonpowered.dateutil.date(2026, 1, 1)
    for i in range(-5000, 5000):
        offset_pydate = test_pydate + datetime.timedelta(days=i, weeks=i)
        offset_cydate = test_cydate.offset(days=i, weeks=i)
        assert offset_pydate.year == offset_cydate.year
        assert offset_pydate.month == offset_cydate.month
        assert offset_pydate.day == offset_cydate.day


def test_offset_years_months():
    test_cydate = cythonpowered.dateutil.date(2026, 1, 1)
    offset_cydate = test_cydate.offset(years=1, months=14)
    assert offset_cydate.year == 2028
    assert offset_cydate.month == 3
    assert offset_cydate.day == 1


def test_offset_all_params():
    test_cydate = cythonpowered.dateutil.date(2026, 1, 1)
    offset_cydate = test_cydate.offset(years=1, months=14, weeks=2, days=8)
    assert offset_cydate.year == 2028
    assert offset_cydate.month == 3
    assert offset_cydate.day == 23


def test_date_range_D_W():
    start_pydate = datetime.date(2026, 1, 1)
    end_pydate = datetime.date(2026, 1, 20)
    start_cydate = cythonpowered.dateutil.date(2026, 1, 1)
    end_cydate = cythonpowered.dateutil.date(2026, 1, 20)
    expected_D = [
        "2026-01-01",
        "2026-01-02",
        "2026-01-03",
        "2026-01-04",
        "2026-01-05",
        "2026-01-06",
        "2026-01-07",
        "2026-01-08",
        "2026-01-09",
        "2026-01-10",
        "2026-01-11",
        "2026-01-12",
        "2026-01-13",
        "2026-01-14",
        "2026-01-15",
        "2026-01-16",
        "2026-01-17",
        "2026-01-18",
        "2026-01-19",
        "2026-01-20",
    ]
    expected_W = ["2026-01-04", "2026-01-11", "2026-01-18"]

    # Compare cythonpowered and pandas for freq="D"
    test_pyrange = pandas.date_range(start_pydate, end_pydate, freq="D")
    test_cyrange = cythonpowered.dateutil.date.date_range(
        start_cydate, end_cydate, freq="D"
    )
    assert [str(d)[0:10] for d in test_pyrange] == expected_D
    assert test_cyrange == expected_D

    # Compare cythonpowered and pandas for freq="W"
    test_pyrange = pandas.date_range(start_pydate, end_pydate, freq="W")
    test_cyrange = cythonpowered.dateutil.date.date_range(
        start_cydate, end_cydate, freq="W"
    )
    assert [str(d)[0:10] for d in test_pyrange] == expected_W
    assert test_cyrange == expected_W

    # Check for include_partial_ranges=True (freq=W only)
    test_cyrange = cythonpowered.dateutil.date.date_range(
        start_cydate, end_cydate, freq="W", include_partial_ranges=True
    )
    assert test_cyrange == expected_W + [end_cydate.tostring()]


def test_date_range_ME_QE():
    start_pydate = datetime.date(2026, 1, 1)
    end_pydate = datetime.date(2026, 11, 20)
    start_cydate = cythonpowered.dateutil.date(2026, 1, 1)
    end_cydate = cythonpowered.dateutil.date(2026, 11, 20)
    expected_ME = [
        "2026-01-31",
        "2026-02-28",
        "2026-03-31",
        "2026-04-30",
        "2026-05-31",
        "2026-06-30",
        "2026-07-31",
        "2026-08-31",
        "2026-09-30",
        "2026-10-31",
    ]
    expected_QE = ["2026-03-31", "2026-06-30", "2026-09-30"]

    # Compare cythonpowered and pandas for freq="ME"
    test_pyrange = pandas.date_range(start_pydate, end_pydate, freq="ME")
    test_cyrange = cythonpowered.dateutil.date.date_range(
        start_cydate, end_cydate, "ME"
    )
    assert [str(d)[0:10] for d in test_pyrange] == expected_ME
    assert test_cyrange == expected_ME

    # Compare cythonpowered and pandas for freq="QE"
    test_pyrange = pandas.date_range(start_pydate, end_pydate, freq="QE")
    test_cyrange = cythonpowered.dateutil.date.date_range(
        start_cydate, end_cydate, "QE"
    )
    assert [str(d)[0:10] for d in test_pyrange] == expected_QE
    assert test_cyrange == expected_QE

    # Check for include_partial_ranges=True
    test_cyrange = cythonpowered.dateutil.date.date_range(
        start_cydate, end_cydate, "ME", include_partial_ranges=True
    )
    assert test_cyrange == expected_ME + [end_cydate.tostring()]
    test_cyrange = cythonpowered.dateutil.date.date_range(
        start_cydate, end_cydate, "QE", include_partial_ranges=True
    )
    assert test_cyrange == expected_QE + [end_cydate.tostring()]


def test_date_range_SE_YE():
    start_pydate = datetime.date(2026, 1, 1)
    end_pydate = datetime.date(2028, 11, 20)
    start_cydate = cythonpowered.dateutil.date(2026, 1, 1)
    end_cydate = cythonpowered.dateutil.date(2028, 11, 20)
    expected_SE = [
        "2026-06-30",
        "2026-12-31",
        "2027-06-30",
        "2027-12-31",
        "2028-06-30",
    ]
    expected_YE = ["2026-12-31", "2027-12-31"]

    # Test cythonpowered (only) for freq="SE" (pandas does not support freq="SE")
    test_cyrange = cythonpowered.dateutil.date.date_range(
        start_cydate, end_cydate, "SE"
    )
    assert test_cyrange == expected_SE

    # Compare cythonpowered and pandas for freq="YE"
    test_pyrange = pandas.date_range(start_pydate, end_pydate, freq="YE")
    test_cyrange = cythonpowered.dateutil.date.date_range(
        start_cydate, end_cydate, "YE"
    )
    assert [str(d)[0:10] for d in test_pyrange] == expected_YE
    assert test_cyrange == expected_YE

    # Check for include_partial_ranges=True
    test_cyrange = cythonpowered.dateutil.date.date_range(
        start_cydate, end_cydate, "SE", include_partial_ranges=True
    )
    assert test_cyrange == expected_SE + [end_cydate.tostring()]
    test_cyrange = cythonpowered.dateutil.date.date_range(
        start_cydate, end_cydate, "YE", include_partial_ranges=True
    )
    assert test_cyrange == expected_YE + [end_cydate.tostring()]
