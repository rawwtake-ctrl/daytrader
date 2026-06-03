"""
Live Market Poller — Yahoo Finance via public quote API.

Polls a basket of symbols every N seconds and appends a JSONL line per poll
to live_feed.jsonl. Also prints a tidy line to stdout per poll.

USAGE:
    # Run in background; Ctrl-C to stop
    python live_poller.py
    python live_poller.py --interval 30 --symbols "ES=F,NQ=F,MSFT,NVDA"
    python live_poller.py --once     # one-shot for cron / Claude polling

ACCURACY:
    Yahoo quotes are typically 15-20 min delayed for futures, real-time for
    most US equities (with caveats). Free, no API key.

OUTPUT:
    JSONL appended to C:\\Claude\\DayTrader\\paper-trading\\live-feed.jsonl
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo
from urllib.request import Request, urlopen
from urllib.error import URLError

DEFAULT_SYMBOLS = "ES=F,NQ=F,YM=F,RTY=F,MSFT,NVDA,AAPL,GOOGL,META,^VIX,^TNX,CL=F,GC=F,DX-Y.NYB"
OUT_PATH = Path(r"/Users/hitanshsharma/Claude/DayTrader/paper-trading/live-feed.jsonl")
OUT_PATH.parent.mkdir(parents=True, exist_ok=True)


def fetch_quotes(symbols: list[str]) -> dict:
    """Hit Yahoo public quote endpoint. Returns dict keyed by symbol."""
    qs = ",".join(symbols)
    url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={qs}"
    req = Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
    })
    with urlopen(req, timeout=10) as resp:
        data = json.load(resp)
    quotes = data.get("quoteResponse", {}).get("result", [])
    return {q["symbol"]: q for q in quotes}


def format_quote(q: dict) -> str:
    """Single-line summary for stdout."""
    sym = q.get("symbol", "?")
    price = q.get("regularMarketPrice")
    chg_pct = q.get("regularMarketChangePercent")
    high = q.get("regularMarketDayHigh")
    low = q.get("regularMarketDayLow")
    vol = q.get("regularMarketVolume")
    if price is None:
        return f"  {sym:8s} (no data)"
    pct = f"{chg_pct:+.2f}%" if chg_pct is not None else "?"
    hl = f"H {high} L {low}" if (high and low) else ""
    v = f"v{vol:,}" if vol else ""
    return f"  {sym:8s} {price:>10}  {pct:>7}  {hl}  {v}"


def ny_now_str() -> str:
    return datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d %H:%M:%S")


def poll_once(symbols: list[str]) -> dict | None:
    """One poll. Append JSONL line, print summary, return data."""
    try:
        quotes = fetch_quotes(symbols)
    except (URLError, TimeoutError) as e:
        print(f"[{ny_now_str()}] FETCH FAILED: {e}", file=sys.stderr)
        return None

    ts_utc = datetime.now(timezone.utc).isoformat()
    ts_ny = ny_now_str()
    record = {
        "ts_utc": ts_utc,
        "ts_ny": ts_ny,
        "quotes": {
            sym: {
                "price": q.get("regularMarketPrice"),
                "chg_pct": q.get("regularMarketChangePercent"),
                "high": q.get("regularMarketDayHigh"),
                "low": q.get("regularMarketDayLow"),
                "volume": q.get("regularMarketVolume"),
                "prev_close": q.get("regularMarketPreviousClose"),
                "market_state": q.get("marketState"),
            } for sym, q in quotes.items()
        },
    }

    with OUT_PATH.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record) + "\n")

    print(f"\n[{ts_ny} ET]")
    for sym in symbols:
        q = quotes.get(sym)
        if q:
            print(format_quote(q))
        else:
            print(f"  {sym:8s} (missing)")

    return record


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--symbols", default=DEFAULT_SYMBOLS,
                   help="Comma-separated Yahoo symbols")
    p.add_argument("--interval", type=int, default=60,
                   help="Seconds between polls (default 60)")
    p.add_argument("--once", action="store_true",
                   help="Single poll then exit (for cron/Claude)")
    args = p.parse_args()

    symbols = [s.strip() for s in args.symbols.split(",") if s.strip()]

    if args.once:
        result = poll_once(symbols)
        return 0 if result else 1

    print(f"Starting live poller — interval {args.interval}s")
    print(f"Symbols: {symbols}")
    print(f"Writing to: {OUT_PATH}")
    print("Ctrl-C to stop.\n")

    try:
        while True:
            poll_once(symbols)
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nStopped.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
