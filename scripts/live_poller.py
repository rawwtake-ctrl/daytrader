"""
Live Market Poller — Stooq keyless light-quote API.

Polls a basket of symbols every N seconds and appends a JSONL line per poll
to live_feed.jsonl. Also prints a tidy line to stdout per poll.

USAGE:
    # Run in background; Ctrl-C to stop
    python live_poller.py
    python live_poller.py --interval 30 --symbols "ES=F,NQ=F,MSFT,NVDA"
    python live_poller.py --once     # one-shot for cron / Claude polling

ACCURACY:
    Stooq quotes are ~15 min delayed, free, no API key. Crucially, Stooq serves
    datacenter IPs — Yahoo's v7/v8 endpoints block them, so the scheduled cloud
    agent could never fetch from Yahoo. Symbol mapping lives in STOOQ_MAP below.

OUTPUT:
    JSONL appended to paper-trading/live-feed.jsonl (see OUT_PATH below)
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


# Map our canonical (Yahoo-style) symbols to Stooq tickers. Yahoo's v7/v8
# endpoints block datacenter IPs — the scheduled cloud agent runs from one, so
# every cloud poll came back empty. Stooq's light-quote endpoint is keyless and
# serves datacenter requests. RTY/Dow use ETF/index tickers where Stooq lacks a
# clean front-month future; all others are direct.
STOOQ_MAP = {
    "ES=F": "es.f", "NQ=F": "nq.f", "YM=F": "ym.f", "RTY=F": "iwm.us",
    "MSFT": "msft.us", "NVDA": "nvda.us", "AAPL": "aapl.us",
    "GOOGL": "googl.us", "META": "meta.us",
    "^VIX": "vi.f", "^TNX": "10yusy.b", "CL=F": "cl.f", "GC=F": "gc.f",
    "DX-Y.NYB": "dx.f",
}
_STOOQ_REV = {v.upper(): k for k, v in STOOQ_MAP.items()}


def _to_float(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


def fetch_quotes(symbols: list[str]) -> dict:
    """Fetch quotes from Stooq's keyless light-quote endpoint in one request.

    Field code `sd2t2ohlcvp` returns Symbol,Date,Time,Open,High,Low,Close,
    Volume,Prev. We map results back into v7-style field names keyed by our
    canonical symbols, so downstream code (poll_once, format_quote,
    brief_helpers) is unchanged. Symbols Stooq can't resolve (date == "N/D")
    are omitted and render n/a downstream.
    """
    tickers = [STOOQ_MAP[s] for s in symbols if s in STOOQ_MAP]
    if not tickers:
        return {}
    qs = "+".join(tickers)
    url = f"https://stooq.com/q/l/?s={qs}&f=sd2t2ohlcvp&h&e=csv"
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req, timeout=15) as resp:
        text = resp.read().decode("utf-8", "replace")

    out = {}
    for line in text.strip().splitlines()[1:]:  # skip header row
        parts = line.split(",")
        if len(parts) < 9:
            continue
        sym, date, _time, _open, high, low, close, vol, prev = parts[:9]
        canon = _STOOQ_REV.get(sym.upper())
        if not canon or date == "N/D":
            continue
        price = _to_float(close)
        prevc = _to_float(prev)
        chg = (price - prevc) / prevc * 100.0 if (price is not None and prevc) else None
        out[canon] = {
            "symbol": sym,
            "regularMarketPrice": price,
            "regularMarketChangePercent": chg,
            "regularMarketDayHigh": _to_float(high),
            "regularMarketDayLow": _to_float(low),
            "regularMarketVolume": _to_float(vol),
            "regularMarketPreviousClose": prevc,
            "marketState": None,
        }
    return out


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
