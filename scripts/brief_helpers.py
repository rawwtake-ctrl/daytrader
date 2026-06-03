"""Deterministic helpers for the Pre-Open Briefing Pipeline.

These functions exist so the morning agent never has to *invent* a number or
a calendar fact. Prices come from the poller feed; the trading-day decision
comes from a hard-coded holiday set. Stdlib only.
"""
from __future__ import annotations

import json
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

NY = ZoneInfo("America/New_York")

# US equity full-closure holidays 2026 (NYSE/Nasdaq). Early-close days excluded.
US_MARKET_HOLIDAYS_2026 = {
    date(2026, 1, 1),    # New Year's Day
    date(2026, 1, 19),   # MLK Jr. Day
    date(2026, 2, 16),   # Presidents' Day
    date(2026, 4, 3),    # Good Friday
    date(2026, 5, 25),   # Memorial Day
    date(2026, 6, 19),   # Juneteenth
    date(2026, 7, 3),    # Independence Day (observed; Jul 4 is Sat)
    date(2026, 9, 7),    # Labor Day
    date(2026, 11, 26),  # Thanksgiving
    date(2026, 12, 25),  # Christmas
}


def is_trading_day(d: date) -> bool:
    """True if d is a weekday and not a US market holiday."""
    if d.weekday() >= 5:  # Sat=5, Sun=6
        return False
    return d not in US_MARKET_HOLIDAYS_2026


def ny_today() -> date:
    """Current date in America/New_York."""
    return datetime.now(NY).date()


def latest_poll(jsonl_path) -> dict:
    """Return the last non-blank JSONL record from the poller feed."""
    p = Path(jsonl_path)
    if not p.exists():
        raise FileNotFoundError(f"No poll feed at {p}")
    last = None
    with p.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                last = line
    if last is None:
        raise ValueError(f"Poll feed empty: {p}")
    return json.loads(last)
