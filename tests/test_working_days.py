from datetime import date

from repairs.hazard_report import add_working_days, is_working_day


def test_weekend_is_not_a_working_day():
    assert is_working_day(date(2026, 11, 7)) is False   # Saturday


def test_bank_holiday_is_not_a_working_day():
    assert is_working_day(date(2026, 12, 25)) is False  # Christmas Day


def test_normal_weekday_is_a_working_day():
    assert is_working_day(date(2026, 11, 4)) is True    # Wednesday


def test_counting_skips_the_weekend():
    # Friday + 1 working day = Monday
    assert add_working_days(date(2026, 11, 6), 1) == date(2026, 11, 9)


def test_ten_working_days_over_christmas():
    assert add_working_days(date(2026, 12, 18), 10) == date(2027, 1, 6)
