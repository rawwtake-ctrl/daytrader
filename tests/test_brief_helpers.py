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


def test_latest_poll_returns_last_record(tmp_path):
    feed = tmp_path / "live-feed.jsonl"
    feed.write_text(
        '{"ts_ny": "2026-06-03 06:00:01", "quotes": {"ES=F": {"price": 100}}}\n'
        '{"ts_ny": "2026-06-03 06:01:01", "quotes": {"ES=F": {"price": 200}}}\n',
        encoding="utf-8",
    )
    rec = bh.latest_poll(feed)
    assert rec["ts_ny"] == "2026-06-03 06:01:01"
    assert rec["quotes"]["ES=F"]["price"] == 200


def test_latest_poll_skips_blank_lines(tmp_path):
    feed = tmp_path / "live-feed.jsonl"
    feed.write_text(
        '{"ts_ny": "a", "quotes": {}}\n\n   \n',
        encoding="utf-8",
    )
    assert bh.latest_poll(feed)["ts_ny"] == "a"


def test_latest_poll_missing_file_raises(tmp_path):
    import pytest
    with pytest.raises(FileNotFoundError):
        bh.latest_poll(tmp_path / "nope.jsonl")
