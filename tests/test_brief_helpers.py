import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import brief_helpers as bh


def test_weekday_is_trading_day():
    assert bh.is_trading_day(date(2026, 6, 3)) is True   # Wednesday


def test_weekend_is_not_trading_day():
    assert bh.is_trading_day(date(2026, 6, 6)) is False  # Saturday
    assert bh.is_trading_day(date(2026, 6, 7)) is False  # Sunday


def test_holiday_is_not_trading_day():
    assert bh.is_trading_day(date(2026, 6, 19)) is False  # Juneteenth
    assert bh.is_trading_day(date(2026, 7, 3)) is False   # Independence Day (observed)
    assert bh.is_trading_day(date(2026, 12, 25)) is False  # Christmas
