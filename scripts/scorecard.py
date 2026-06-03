"""Scorecard — turns your paper-trade log into a learning surface.

Reads paper-trading/trades.csv (one row per paper trade you took in your
Tradovate demo / journal) and prints running expectancy: win rate, average R,
and a per-setup breakdown. THIS is the learning loop — it tells you which setups
actually pay and which to stop taking. Review it weekly.

The whole game is sample size: a setup needs ~20+ trades before its numbers mean
anything. Until then, every line here says "too few to trust" — on purpose.

USAGE:
    python3 scripts/scorecard.py
"""
from __future__ import annotations

import csv
import sys
from collections import defaultdict
from pathlib import Path

TRADES = Path(__file__).resolve().parent.parent / "paper-trading" / "trades.csv"
MIN_SAMPLE = 20  # below this, a setup's stats are noise


def _f(row, key):
    try:
        return float(row[key])
    except (KeyError, ValueError, TypeError):
        return None


def load_trades(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as fh:
        return [r for r in csv.DictReader(fh) if r.get("date")]


def summarize(rows: list[dict]) -> str:
    if not rows:
        return "No trades logged yet. Add rows to paper-trading/trades.csv as you take them."

    out = ["# Paper-Trade Scorecard", ""]

    # Overall
    rs = [_f(r, "R") for r in rows if _f(r, "R") is not None]
    wins = sum(1 for r in rs if r > 0)
    losses = sum(1 for r in rs if r < 0)
    total_r = sum(rs)
    n = len(rs)
    wr = f"{wins / n * 100:.0f}%" if n else "n/a"
    exp = f"{total_r / n:+.2f}R" if n else "n/a"
    followed = sum(1 for r in rows if (r.get("followed_rules", "").lower() == "yes"))
    out += [
        f"**Trades:** {n}  ·  **Win rate:** {wr} ({wins}W / {losses}L)",
        f"**Total:** {total_r:+.1f}R  ·  **Expectancy:** {exp} per trade",
        f"**Rules followed:** {followed}/{len(rows)}",
        "",
        f"_Sample is {'ADEQUATE' if n >= MIN_SAMPLE else 'TOO SMALL'} "
        f"(need {MIN_SAMPLE}+ for the numbers to mean anything; have {n})._",
        "",
        "## By setup",
    ]

    # Per setup
    by = defaultdict(list)
    for r in rows:
        rv = _f(r, "R")
        if rv is not None:
            by[r.get("setup", "?")].append(rv)
    out.append("| Setup | n | W/L | Expectancy | Verdict |")
    out.append("|---|---|---|---|---|")
    for setup, vals in sorted(by.items(), key=lambda kv: -len(kv[1])):
        w = sum(1 for v in vals if v > 0)
        l = sum(1 for v in vals if v < 0)
        e = sum(vals) / len(vals)
        verdict = "too few to trust" if len(vals) < MIN_SAMPLE else (
            "keep" if e > 0 else "drop")
        out.append(f"| {setup} | {len(vals)} | {w}/{l} | {e:+.2f}R | {verdict} |")

    # Rules-followed cut (process > outcome)
    fr = [_f(r, "R") for r in rows if r.get("followed_rules", "").lower() == "yes" and _f(r, "R") is not None]
    nr = [_f(r, "R") for r in rows if r.get("followed_rules", "").lower() != "yes" and _f(r, "R") is not None]
    out += ["", "## Discipline check (process beats outcome)"]
    if fr:
        out.append(f"- Rules-followed trades: {len(fr)}, {sum(fr) / len(fr):+.2f}R avg")
    if nr:
        out.append(f"- Rules-BROKEN trades: {len(nr)}, {sum(nr) / len(nr):+.2f}R avg  ← these should hurt")
    return "\n".join(out)


def main() -> int:
    print(summarize(load_trades(TRADES)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
