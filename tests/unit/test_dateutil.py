"""Unit tests for the cythonpowered.dateutil module.

Cross-validates the Cython `date` class against the Python originals
(datetime / calendar / pandas) across a range of inputs, and covers the
mandatory edge cases: boundary values (year 1 / 9999, ordinal 1 / 3652059,
leap years and century rules), invalid inputs (asserting the same
exception type as the Python original), and domain transitions
(month-end / year-end carry, week-end alignment).
"""

import calendar
import datetime
import random

import pandas
import pytest

from cythonpowered.dateutil import date

# Deterministic sample of ordinals spread across the full valid range
# (1..3652059), so the cross-validation sweeps stay reproducible.
SAMPLE_ORDINALS = random.Random(42).sample(range(1, 3652060), 5000)
# Boundary ordinals: first/last day, century and quadricentennial
# transitions, and the maximum ordinal (datetime.date.max.toordinal()).
BOUNDARY_ORDINALS = [1, 2, 365, 366, 1460, 1461, 36524, 36525, 146096, 146097, 146098, 3652058, 3652059]
# Years covering the leap-year domain transitions: century non-leaps,
# quadricentennial leaps, and the year-range boundaries.
TEST_YEARS = [1, 4, 99, 100, 400, 1900, 2000, 2024, 2025, 2026, 2100, 9998, 9999]


def test_interop():
    """The cython date must interoperate with datetime.date: equality in
    both directions, matching hashes (hash/equality contract), and matching
    str/repr (modulo the documented "datetime." prefix difference)."""
    # Stage 1: equal values compare equal both ways (cython vs stdlib).
    one = datetime.date(2026, 1, 1)
    two = date(2026, 1, 1)
    assert one == two
    assert two == one
    # Stage 2: unequal values compare unequal both ways.
    assert one != date(2026, 1, 2)
    assert date(2026, 1, 2) != one
    # Stage 3: hashes must match so the two types are interchangeable in
    # sets and dicts (required because __eq__ crosses types).
    assert hash(two) == hash(one)
    # Stage 4: str matches isoformat(); repr matches apart from the
    # "datetime." module prefix (documented deviation).
    assert str(two) == one.isoformat()
    assert repr(two) == f"date({one.year}, {one.month}, {one.day})"
    # Stage 5: comparison against unrelated types returns NotImplemented
    # (falls back to inequality, no exception).
    assert (two == 5) is False
    assert (two == "2026-01-01") is False


def test_init_valid_boundaries():
    """The constructor must accept every valid boundary date, matching
    datetime.date's accepted range (year 1..9999, valid month/day)."""
    # Stage 1: year-range boundaries.
    assert date(1, 1, 1) == datetime.date(1, 1, 1)
    assert date(9999, 12, 31) == datetime.date(9999, 12, 31)
    # Stage 2: month/day boundaries, including the leap-day case.
    for y, m, d in [(2024, 2, 29), (2026, 2, 28), (2026, 12, 31), (2000, 2, 29)]:
        assert date(y, m, d) == datetime.date(y, m, d)


def test_init_invalid():
    """The constructor must reject invalid components with ValueError, the
    same exception type as datetime.date (which the old code silently
    accepted, producing corrupt dates)."""
    # Stage 1: year out of range (datetime.MINYEAR is 1, MAXYEAR is 9999).
    with pytest.raises(ValueError):
        date(0, 1, 1)
    with pytest.raises(ValueError):
        date(10000, 1, 1)
    with pytest.raises(ValueError):
        date(-1, 1, 1)
    # Stage 2: month out of range.
    with pytest.raises(ValueError):
        date(2026, 0, 1)
    with pytest.raises(ValueError):
        date(2026, 13, 1)
    with pytest.raises(ValueError):
        date(2026, -1, 1)
    # Stage 3: day out of range, including the leap/non-leap February
    # transition (2024 is a leap year, 2026 is not).
    with pytest.raises(ValueError):
        date(2026, 1, 0)
    with pytest.raises(ValueError):
        date(2026, 1, 32)
    with pytest.raises(ValueError):
        date(2026, 2, 29)  # non-leap year
    with pytest.raises(ValueError):
        date(2026, 4, 31)  # 30-day month
    with pytest.raises(ValueError):
        date(2000, 2, 30)  # even the quadricentennial leap year has 29 days


def test_readonly_fields():
    """year/month/day must be read-only, like datetime.date's properties
    (the old code exposed them as mutable attributes, allowing corrupt
    dates to be created after construction)."""
    d = date(2026, 1, 1)
    # Stage 1: reading the fields returns the constructed values.
    assert (d.year, d.month, d.day) == (2026, 1, 1)
    # Stage 2: writing any field raises AttributeError.
    for field in ("year", "month", "day"):
        with pytest.raises(AttributeError):
            setattr(d, field, 13)


def test_today():
    """today() must return the current local date, matching
    datetime.date.today()."""
    # Stage 1: both implementations agree on year, month and day.
    one = datetime.date.today()
    two = date.today()
    assert one.year == two.year
    assert one.month == two.month
    assert one.day == two.day


def test_isleap():
    """isleap() must match calendar.isleap() across the full valid year
    range, including the century transitions (1900 no, 2000 yes, 2100 no)."""
    # Stage 1: every year in the supported range (1..9999).
    for y in range(1, 10000):
        assert calendar.isleap(y) == date.isleap(y)
    # Stage 2: negative years are accepted by calendar.isleap() and must
    # match there too (Python floor-modulo semantics).
    for y in range(-400, 400):
        assert calendar.isleap(y) == date.isleap(y)


def test_monthrange():
    """monthrange() must match calendar.monthrange() for every month of a
    range of years spanning the leap-year transitions."""
    # Stage 1: cross-validation over test years x all 12 months.
    for y in TEST_YEARS:
        for m in range(1, 13):
            assert calendar.monthrange(y, m) == date.monthrange(y, m)
    # Stage 2: invalid months raise ValueError, like calendar.monthrange
    # (which raises IllegalMonthError, a ValueError subclass).
    with pytest.raises(ValueError):
        date.monthrange(2026, 0)
    with pytest.raises(ValueError):
        date.monthrange(2026, 13)


def test_fromstring():
    """fromstring() must parse zero-padded 'YYYY-MM-DD' strings (any
    single-character separator), matching strptime, and reject malformed
    input with ValueError like strptime."""
    # Stage 1: valid strings with different separators, including the
    # year-range and leap-day boundaries.
    for s in ["0001-01-01", "2026-01-01", "9999-12-31", "2024/02/29", "2026.12.31", "0100-03-01"]:
        one = datetime.datetime.strptime(s.replace("/", "-").replace(".", "-"), "%Y-%m-%d").date()
        two = date.fromstring(s)
        assert (one.year, one.month, one.day) == (two.year, two.month, two.day)
    # Stage 2: malformed input raises ValueError (same type as strptime):
    # too short, non-numeric fields, and out-of-range fields.
    for s in ["2026-1-1", "20260101", "abcd-ef-gh", "2026-13-01", "2026-01-32", ""]:
        with pytest.raises(ValueError):
            date.fromstring(s)


def test_tostring():
    """tostring() must produce the 'YYYY-MM-DD' form (year always
    zero-padded to 4 digits, like isoformat()) for a range of dates."""
    # Stage 1: cross-validation against isoformat() at boundaries and a
    # deterministic sample of the full ordinal range.
    for i in BOUNDARY_ORDINALS + SAMPLE_ORDINALS:
        one = datetime.date.fromordinal(i)
        two = date(one.year, one.month, one.day)
        assert two.tostring() == one.isoformat()
        assert str(two) == one.isoformat()
    # Stage 2: for years >= 1000 the output also matches strftime exactly
    # (glibc's %Y skips zero-padding below year 1000, a documented
    # platform quirk we deliberately do not replicate).
    for i in [365205, 3650000, 3652059]:  # years 1000, 9994, 9999
        one = datetime.date.fromordinal(i)
        assert date(one.year, one.month, one.day).tostring() == one.strftime("%Y-%m-%d")


def test_tostring_separator():
    """tostring(separator=...) must accept any single Latin-1 character
    (1-byte unicode buffer) and reject everything else with ValueError."""
    # Stage 1: valid single-character separators, including a Latin-1
    # character above the ASCII range.
    assert date(2026, 1, 1).tostring(separator=".") == "2026.01.01"
    assert date(2026, 1, 1).tostring(separator="e") == "2026e01e01"
    # Stage 2: empty, multi-character, and non-Latin-1 separators would be
    # silently corrupted in the 1-byte buffer, so they must raise.
    for sep in ["", "++", "\u20ac"]:  # last is the euro sign (U+20AC)
        with pytest.raises(ValueError):
            date(2026, 1, 1).tostring(separator=sep)


def test_weekday():
    """weekday() must match datetime.date.weekday() (Monday = 0) for every
    day of a range of years, including the year-boundary months."""
    # Stage 1: sweep every day of each test year (leap and non-leap).
    for y in TEST_YEARS:
        ndays = 366 if calendar.isleap(y) else 365
        test_pydate = datetime.date(y, 1, 1)
        test_cydate = date(y, 1, 1)
        for n in range(ndays):
            assert test_pydate.weekday() == test_cydate.weekday()
            # Do not advance on the last day: 9999-12-31 + 1 day overflows
            # in both implementations.
            if n < ndays - 1:
                test_pydate += datetime.timedelta(days=1)
                test_cydate = test_cydate.increment()


def test_yearday():
    """yearday() must match datetime.date().timetuple().tm_yday for every
    day of a range of years, including leap years."""
    # Stage 1: sweep every day of each test year.
    for y in TEST_YEARS:
        ndays = 366 if calendar.isleap(y) else 365
        test_pydate = datetime.date(y, 1, 1)
        test_cydate = date(y, 1, 1)
        for n in range(ndays):
            assert test_pydate.timetuple().tm_yday == test_cydate.yearday()
            # Do not advance on the last day: 9999-12-31 + 1 day overflows
            # in both implementations.
            if n < ndays - 1:
                test_pydate += datetime.timedelta(days=1)
                test_cydate = test_cydate.increment()
    # Stage 2: the year-end boundary returns the full day count.
    assert date(2024, 12, 31).yearday() == 366  # leap year
    assert date(2026, 12, 31).yearday() == 365  # non-leap year


def test_fromordinal():
    """fromordinal() must match datetime.date.fromordinal() at every
    boundary (century/quadricentennial transitions, min/max ordinal) and
    across a dense plus sampled range of the full ordinal space."""
    # Stage 1: boundary ordinals, including the max (9999-12-31) which the
    # old code mangled through an unsigned-char overflow.
    for i in BOUNDARY_ORDINALS:
        test_pydate = datetime.date.fromordinal(i)
        test_cydate = date.fromordinal(i)
        assert (test_pydate.year, test_pydate.month, test_pydate.day) == (
            test_cydate.year, test_cydate.month, test_cydate.day
        )
    # Stage 2: dense sweep of the first 300000 ordinals (covers the first
    # century and quadricentennial transitions many times over).
    for i in range(1, 300001):
        test_pydate = datetime.date.fromordinal(i)
        test_cydate = date.fromordinal(i)
        assert (test_pydate.year, test_pydate.month, test_pydate.day) == (
            test_cydate.year, test_cydate.month, test_cydate.day
        )
    # Stage 3: deterministic sample spread across the entire range.
    for i in SAMPLE_ORDINALS:
        test_pydate = datetime.date.fromordinal(i)
        test_cydate = date.fromordinal(i)
        assert (test_pydate.year, test_pydate.month, test_pydate.day) == (
            test_cydate.year, test_cydate.month, test_cydate.day
        )
    # Stage 4: out-of-range ordinals raise ValueError, like the stdlib.
    with pytest.raises(ValueError):
        date.fromordinal(0)
    with pytest.raises(ValueError):
        date.fromordinal(-1)
    with pytest.raises(ValueError):
        date.fromordinal(3652060)


def test_toordinal():
    """toordinal() must return the exact stdlib ordinal for a range of
    dates, so fromordinal(toordinal(d)) == d for every valid date."""
    # Stage 1: boundaries and a deterministic sample of the full range.
    for i in BOUNDARY_ORDINALS + SAMPLE_ORDINALS:
        test_pydate = datetime.date.fromordinal(i)
        test_cydate = date(test_pydate.year, test_pydate.month, test_pydate.day)
        assert test_cydate.toordinal() == i
    # Stage 2: the min/max dates map to the min/max ordinals.
    assert date(1, 1, 1).toordinal() == 1
    assert date(9999, 12, 31).toordinal() == 3652059


def test_offset_days_weeks():
    """offset(days=..., weeks=...) must match datetime.date + timedelta
    across a wide range of positive and negative offsets from several
    base dates (including leap day and the year-end boundary)."""
    # Stage 1: cross-validation from base dates at interesting positions.
    # Offsets that leave the 1..9999 range must raise OverflowError on BOTH
    # sides (the stdlib raises for its own base dates near the range edges,
    # and the cython version must agree).
    for base in [(1, 1, 1), (2024, 2, 29), (2026, 1, 1), (9999, 12, 31)]:
        test_pydate = datetime.date(*base)
        test_cydate = date(*base)
        for i in range(-2000, 2000):
            try:
                offset_pydate = test_pydate + datetime.timedelta(days=i, weeks=i)
            except OverflowError:
                with pytest.raises(OverflowError):
                    test_cydate.offset(days=i, weeks=i)
                continue
            offset_cydate = test_cydate.offset(days=i, weeks=i)
            assert (offset_pydate.year, offset_pydate.month, offset_pydate.day) == (
                offset_cydate.year, offset_cydate.month, offset_cydate.day
            )
    # Stage 2: explicit overflow cases at both range edges (the old code
    # silently wrapped the unsigned year instead of raising).
    with pytest.raises(OverflowError):
        date(9999, 12, 31).offset(days=1)
    with pytest.raises(OverflowError):
        date(1, 1, 1).offset(days=-1)
    with pytest.raises(OverflowError):
        date(9999, 12, 25).offset(weeks=1)  # 9999-12-25 + 7d = 10000-01-01


def test_offset_years_months():
    """offset(years=..., months=...) must behave like relativedelta: add
    the months, carry into the year, and clamp the day to the last day of
    the target month. The input date must not be mutated."""
    # Stage 1: a range of (base, offset, expected) cases covering clamping
    # (Jan 31 -> Feb 28/29), negative offsets crossing the year boundary,
    # and large multi-year month offsets.
    cases = [
        ((2026, 1, 1), dict(years=1, months=14), (2028, 3, 1)),
        ((2026, 12, 31), dict(months=1), (2027, 1, 31)),
        ((2026, 1, 31), dict(months=1), (2026, 2, 28)),
        ((2024, 1, 31), dict(months=1), (2024, 2, 29)),
        ((2026, 3, 31), dict(months=-1), (2026, 2, 28)),
        ((2026, 1, 31), dict(months=-1), (2025, 12, 31)),
        ((2026, 1, 1), dict(years=-1), (2025, 1, 1)),
        ((2026, 2, 28), dict(years=1), (2027, 2, 28)),
        ((2024, 2, 29), dict(years=1), (2025, 2, 28)),
        ((2026, 6, 15), dict(months=18), (2027, 12, 15)),
        ((2026, 6, 15), dict(months=-18), (2024, 12, 15)),
    ]
    for base, kw, expected in cases:
        offset_cydate = date(*base).offset(**kw)
        assert (offset_cydate.year, offset_cydate.month, offset_cydate.day) == expected
    # Stage 2: the input date is immutable — offset() returns a new object
    # and leaves the original unchanged (the old code mutated it in place).
    test_cydate = date(2026, 1, 1)
    offset_cydate = test_cydate.offset(years=1, months=2)
    assert (test_cydate.year, test_cydate.month, test_cydate.day) == (2026, 1, 1)
    assert offset_cydate is not test_cydate
    assert (offset_cydate.year, offset_cydate.month, offset_cydate.day) == (2027, 3, 1)


def test_offset_all_params():
    """offset() must combine years, months, weeks and days in one call:
    months/years are applied first (with day clamping), then the day
    offset, matching sequential application of the parts."""
    # Stage 1: combined offset from 2026-01-01: +1y +14m -> 2028-03-01,
    # then +2w +8d = +22 days -> 2028-03-23.
    offset_cydate = date(2026, 1, 1).offset(years=1, months=14, weeks=2, days=8)
    assert (offset_cydate.year, offset_cydate.month, offset_cydate.day) == (2028, 3, 23)
    # Stage 2: zero offset returns an equal date and raises nothing.
    assert date(2026, 1, 1).offset() == date(2026, 1, 1)


def test_increment():
    """increment() must return the date plus one day, matching
    datetime.date + timedelta(days=1), including the month-end, leap-day
    and year-end transitions."""
    # Stage 1: sweep every day of a leap and a non-leap year.
    for y in [2024, 2026]:
        test_pydate = datetime.date(y, 1, 1)
        test_cydate = date(y, 1, 1)
        for _ in range(365):
            assert test_cydate.increment() == test_pydate + datetime.timedelta(days=1)
            test_pydate += datetime.timedelta(days=1)
            test_cydate = test_cydate.increment()
    # Stage 2: the year-end boundary wraps to January 1st of the next year.
    assert date(2026, 12, 31).increment() == date(2027, 1, 1)
    # Stage 3: incrementing the maximum date raises OverflowError, like
    # the stdlib (the old code silently produced year 10000).
    with pytest.raises(OverflowError):
        date(9999, 12, 31).increment()


def test_date_range_D_W():
    """date_range(freq='D'/'W') must match pandas.date_range: 'D' lists
    every day inclusive of both ends, 'W' lists week-ending-Sunday dates."""
    # Stage 1: fixed expected lists (regression anchors) plus the pandas
    # cross-check for freq="D".
    start_pydate = datetime.date(2026, 1, 1)
    end_pydate = datetime.date(2026, 1, 20)
    start_cydate = date(2026, 1, 1)
    end_cydate = date(2026, 1, 20)
    expected_D = [f"2026-01-{d:02d}" for d in range(1, 21)]
    expected_W = ["2026-01-04", "2026-01-11", "2026-01-18"]

    test_pyrange = pandas.date_range(start_pydate, end_pydate, freq="D")
    test_cyrange = date.date_range(start_cydate, end_cydate, freq="D")
    assert [str(d)[0:10] for d in test_pyrange] == expected_D
    assert test_cyrange == expected_D
    # Stage 2: same for freq="W" (pandas 'W' defaults to W-SUN).
    test_pyrange = pandas.date_range(start_pydate, end_pydate, freq="W")
    test_cyrange = date.date_range(start_cydate, end_cydate, freq="W")
    assert [str(d)[0:10] for d in test_pyrange] == expected_W
    assert test_cyrange == expected_W
    # Stage 3: cross-check over wider ranges, including the year boundary
    # and the year-9999 edge (week ends past 9999-12-31 must stop cleanly).
    for s, e in [
        ((2025, 12, 28), (2026, 1, 4)),
        ((2000, 1, 1), (2002, 6, 30)),
        ((9999, 12, 25), (9999, 12, 31)),
    ]:
        test_pyrange = pandas.date_range(datetime.date(*s), datetime.date(*e), freq="W")
        test_cyrange = date.date_range(date(*s), date(*e), freq="W")
        assert [str(d)[0:10] for d in test_pyrange] == test_cyrange


def test_date_range_ME_QE():
    """date_range(freq='ME'/'QE') must match pandas.date_range: 'ME' lists
    month-ends, 'QE' lists calendar quarter-ends (QE-DEC)."""
    # Stage 1: fixed expected lists (regression anchors) plus the pandas
    # cross-check for freq="ME".
    start_pydate = datetime.date(2026, 1, 1)
    end_pydate = datetime.date(2026, 11, 20)
    start_cydate = date(2026, 1, 1)
    end_cydate = date(2026, 11, 20)
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

    test_pyrange = pandas.date_range(start_pydate, end_pydate, freq="ME")
    test_cyrange = date.date_range(start_cydate, end_cydate, "ME")
    assert [str(d)[0:10] for d in test_pyrange] == expected_ME
    assert test_cyrange == expected_ME
    # Stage 2: same for freq="QE", including a range that spans the
    # December->January quarter transition.
    test_pyrange = pandas.date_range(start_pydate, end_pydate, freq="QE")
    test_cyrange = date.date_range(start_cydate, end_cydate, "QE")
    assert [str(d)[0:10] for d in test_pyrange] == expected_QE
    assert test_cyrange == expected_QE
    test_pyrange = pandas.date_range(
        datetime.date(2025, 11, 1), datetime.date(2026, 2, 15), freq="QE"
    )
    test_cyrange = date.date_range(date(2025, 11, 1), date(2026, 2, 15), "QE")
    assert [str(d)[0:10] for d in test_pyrange] == test_cyrange


def test_date_range_SE_YE():
    """date_range(freq='SE'/'YE') must list six-month period-ends and
    year-ends; 'YE' is cross-checked against pandas. 'SE' is cython-only:
    pandas' 'SE' alias means SemiMonthEnd (15th + month end), a different
    concept, so it cannot be cross-validated."""
    # Stage 1: fixed expected lists (regression anchors) for freq="SE".
    start_pydate = datetime.date(2026, 1, 1)
    end_pydate = datetime.date(2028, 11, 20)
    start_cydate = date(2026, 1, 1)
    end_cydate = date(2028, 11, 20)
    expected_SE = [
        "2026-06-30",
        "2026-12-31",
        "2027-06-30",
        "2027-12-31",
        "2028-06-30",
    ]
    expected_YE = ["2026-12-31", "2027-12-31"]

    test_cyrange = date.date_range(start_cydate, end_cydate, "SE")
    assert test_cyrange == expected_SE
    # Stage 2: freq="YE" cross-checked against pandas, including the
    # year-9999 boundary (period ends at 9999-12-31 must stop cleanly).
    test_pyrange = pandas.date_range(start_pydate, end_pydate, freq="YE")
    test_cyrange = date.date_range(start_cydate, end_cydate, "YE")
    assert [str(d)[0:10] for d in test_pyrange] == expected_YE
    assert test_cyrange == expected_YE
    test_cyrange = date.date_range(date(9998, 6, 1), date(9999, 12, 31), "YE")
    assert test_cyrange == ["9998-12-31", "9999-12-31"]


def test_date_range_end_before_start():
    """date_range() must return an empty list when start > end, like
    pandas.date_range (the old code returned [start] for freq='D')."""
    # Stage 1: every supported frequency returns an empty list.
    for freq in ["D", "W", "ME", "QE", "SE", "YE"]:
        assert date.date_range(date(2026, 1, 10), date(2026, 1, 1), freq=freq) == []
    # Stage 2: start == end returns exactly that single period end.
    assert date.date_range(date(2026, 1, 1), date(2026, 1, 1), freq="D") == [
        "2026-01-01"
    ]


def test_date_range_invalid_freq():
    """date_range() must raise ValueError for an unknown frequency, like
    pandas.date_range (the old code silently returned an empty list)."""
    # Stage 1: unknown frequencies are rejected (case-sensitive, like pandas).
    for freq in ["X", "d", "M", "Q", "Y", ""]:
        with pytest.raises(ValueError):
            date.date_range(date(2026, 1, 1), date(2026, 1, 20), freq=freq)
