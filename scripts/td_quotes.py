"""Twelve Data quote fetcher — for the SCHEDULED CLOUD agent only.

Free no-key feeds (Stooq/Yahoo) block datacenter IPs, so the cloud agent can't
use live_poller.py. Twelve Data is a keyed API (authenticates by key, not IP),
so it works from the cloud. BUT its free tier only covers US equities, ETFs,
and gold — indices/VIX/DXY/WTI/treasuries are paywalled. So this fetches an
ETF-proxy basket (SPY≈S&P, QQQ≈Nasdaq, IWM≈Russell, DIA≈Dow) + gold + mega-caps.
Exact ES/NQ futures levels and VIX/10Y/WTI must come from web search in the brief.

Key comes from the TWELVEDATA_KEY env var (kept OUT of the public repo — the
cloud routine injects it). Free tier = 8 credits/min, so the basket is capped
at 8 symbols to fit a single batched /quote call.

USAGE:
    TWELVEDATA_KEY=xxxx python3 scripts/td_quotes.py        # prints markdown table
    python3 scripts/td_quotes.py --key xxxx
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo

NY = ZoneInfo("America/New_York")

# (Twelve Data symbol, display label). Capped at 8 to fit the free 8/min limit.
TD_BASKET = [
    ("SPY", "S&P 500 (SPY ETF)"),
    ("QQQ", "Nasdaq 100 (QQQ ETF)"),
    ("IWM", "Russell 2000 (IWM ETF)"),
    ("DIA", "Dow (DIA ETF)"),
    ("XAU/USD", "Gold"),
    ("MSFT", "MSFT"),
    ("NVDA", "NVDA"),
    ("AAPL", "AAPL"),
]


def fetch_td(symbols: list[str], key: str) -> dict:
    """Batched /quote for up to 8 symbols. Returns {symbol: quote_dict}."""
    joined = ",".join(symbols)
    url = (
        "https://api.twelvedata.com/quote?symbol="
        f"{urllib.parse.quote(joined)}&apikey={key}"
    )
    with urllib.request.urlopen(url, timeout=20) as resp:
        data = json.load(resp)
    # Single-symbol responses are a flat dict; multi-symbol are keyed by symbol.
    if isinstance(data, dict) and "symbol" in data and len(symbols) == 1:
        return {symbols[0]: data}
    return data if isinstance(data, dict) else {}


def render_table(quotes: dict) -> str:
    ts = datetime.now(NY).strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        f"_Twelve Data snapshot: {ts} ET (ETF proxies for index direction; "
        "real-time on free tier varies)_",
        "",
        "| Symbol | Price | Chg% | Prev close |",
        "|---|---|---|---|",
    ]
    for td_sym, label in TD_BASKET:
        q = quotes.get(td_sym)
        if not isinstance(q, dict) or q.get("status") == "error" or q.get("close") is None:
            lines.append(f"| {label} | n/a | n/a | n/a |")
            continue
        price = q.get("close")
        prev = q.get("previous_close")
        chg = q.get("percent_change")
        try:
            chg_s = f"{float(chg):+.2f}%"
        except (TypeError, ValueError):
            chg_s = "n/a"
        lines.append(f"| {label} | {price} | {chg_s} | {prev if prev is not None else 'n/a'} |")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--key", default=os.environ.get("TWELVEDATA_KEY", ""))
    args = ap.parse_args()
    if not args.key:
        print("ERROR: no API key (set TWELVEDATA_KEY env or pass --key)", file=sys.stderr)
        return 2
    try:
        quotes = fetch_td([s for s, _ in TD_BASKET], args.key)
    except Exception as e:  # noqa: BLE001 — surface any fetch failure to the caller
        print(f"ERROR: Twelve Data fetch failed: {e}", file=sys.stderr)
        return 1
    print(render_table(quotes))
    return 0


if __name__ == "__main__":
    sys.exit(main())
