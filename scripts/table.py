"""Print the live market table — run this on YOUR machine when you sit down.

The scheduled cloud brief can't fetch live prices (datacenter IPs are blocked by
free feeds). Your own machine's residential IP is NOT blocked, so this gives the
REAL numbers — actual ES/NQ futures, VIX, 10Y, WTI, gold, DXY, mega-caps — in a
couple of seconds, via Stooq. Pair it with the morning brief in Google Drive.

USAGE:
    python3 scripts/table.py
"""
from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import brief_helpers as bh   # noqa: E402
import live_poller as lp     # noqa: E402


def main() -> int:
    symbols = [s.strip() for s in lp.DEFAULT_SYMBOLS.split(",") if s.strip()]
    try:
        quotes = lp.fetch_quotes(symbols)
    except Exception as e:  # noqa: BLE001
        print(f"fetch failed: {e}", file=sys.stderr)
        return 1
    if not quotes:
        print("No quotes returned (Stooq may be rate-limiting — retry in a moment).",
              file=sys.stderr)
        return 1

    record = {
        "ts_ny": datetime.now(bh.NY).strftime("%Y-%m-%d %H:%M:%S"),
        "quotes": {
            sym: {
                "price": q.get("regularMarketPrice"),
                "chg_pct": q.get("regularMarketChangePercent"),
                "high": q.get("regularMarketDayHigh"),
                "low": q.get("regularMarketDayLow"),
                "volume": q.get("regularMarketVolume"),
                "prev_close": q.get("regularMarketPreviousClose"),
                "market_state": q.get("marketState"),
            }
            for sym, q in quotes.items()
        },
    }
    print(bh.format_hard_numbers(record))
    for s in ("ES=F", "NQ=F"):
        lv = bh.tier1_from_poll(record, s)
        print(f"\n{bh.SYMBOL_LABELS.get(s, s)} — PDC {lv['pdc']} · "
              f"day H {lv['day_high']} · day L {lv['day_low']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
