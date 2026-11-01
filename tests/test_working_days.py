from datetime import date
from repairs.hazard_report import add_workingdays, is_workingday


def test_weekend_not_workingday():
    assert is_workingday(date(2026, 11, 7)) is False 
    
def test_normal_weekday_workingday():
    assert is_workingday(date(2026, 11, 4)) is True 

def test_bankholiday_not_workingday():
    assert is_workingday(date(2026, 12, 25)) is False 

def test_ten_workingdays_christmas():
    assert add_workingdays(date(2026, 12, 18), 10) == date(2027, 1, 6)

def test_counting_skips_weekend():
    assert add_workingdays(date(2026, 11, 6), 1) == date(2026, 11, 9)