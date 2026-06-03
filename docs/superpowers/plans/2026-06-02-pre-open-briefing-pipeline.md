# Pre-Open Briefing Pipeline — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A remote scheduled agent that fires twice each trading morning (6:00 + 8:45 AM ET), assembles a verified, action-first pre-open briefing, and commits it to a private git repo.

**Architecture:** Deterministic logic (trading-day check, poll parsing, hard-number rendering, level computation) lives in a tested Python module so the LLM never invents those values. A routine prompt orchestrates: run the Yahoo poller for hard numbers, run the helper to emit deterministic sections, `WebSearch` for cited narrative, assemble, commit. Two `/schedule` cloud agents run it on a trading-day-only cadence.

**Tech Stack:** Python 3.11+ (stdlib only — `json`, `datetime`, `zoneinfo`, `pathlib`, `urllib`), pytest, git + GitHub (private), Claude `/schedule` remote agents, built-in `WebSearch`/`WebFetch`.

---

## File Structure

| File | Responsibility |
|---|---|
| `scripts/brief_helpers.py` | **Create.** Deterministic, testable logic: `is_trading_day`, `latest_poll`, `format_hard_numbers`, `tier1_from_poll`. Single source of truth for the 2026 holiday set. |
| `tests/test_brief_helpers.py` | **Create.** Pytest unit tests for every helper. |
| `scripts/MORNING_BRIEF_ROUTINE.md` | **Create.** The instruction set the remote agent executes each morning. |
| `paper-trading/briefings/_TEMPLATE.md` | **Create.** Canonical brief layout (action-first, layered). |
| `US_MARKET_HOLIDAYS_2026.md` | **Create.** Human-readable holiday doc (mirrors the Python constant). |
| `.gitignore` | **Create.** Ignore `.venv/`, `live-feed.jsonl`, `__pycache__/`. |
| `scripts/live_poller.py` | **Modify.** Fix stale `C:\Claude\...` docstring (cosmetic). |

---

## Task 1: Initialize repo

**Files:**
- Create: `~/Claude/DayTrader/.gitignore`

- [ ] **Step 1: Write `.gitignore`**

```
.venv/
__pycache__/
*.pyc
paper-trading/live-feed.jsonl
.DS_Store
```

- [ ] **Step 2: Init repo and make first commit**

```bash
cd ~/Claude/DayTrader
git init
git add .
git commit -m "chore: initialize DayTrader repo with existing research + scripts + PBP spec"
```

Expected: commit succeeds listing research/, scripts/, docs/, paper-trading/.

- [ ] **Step 3: Verify `live-feed.jsonl` is ignored**

Run: `cd ~/Claude/DayTrader && touch paper-trading/live-feed.jsonl && git status --short paper-trading/live-feed.jsonl`
Expected: NO output (file is ignored).

---

## Task 2: `is_trading_day` (TDD)

**Files:**
- Create: `scripts/brief_helpers.py`
- Test: `tests/test_brief_helpers.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_brief_helpers.py
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ~/Claude/DayTrader && python -m pytest tests/test_brief_helpers.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'brief_helpers'`.

- [ ] **Step 3: Write minimal implementation**

```python
# scripts/brief_helpers.py
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd ~/Claude/DayTrader && python -m pytest tests/test_brief_helpers.py -v`
Expected: 3 passed.

- [ ] **Step 5: Commit**

```bash
cd ~/Claude/DayTrader
git add scripts/brief_helpers.py tests/test_brief_helpers.py
git commit -m "feat: trading-day check with 2026 US market holiday set"
```

---

## Task 3: `latest_poll` (TDD)

**Files:**
- Modify: `scripts/brief_helpers.py`
- Test: `tests/test_brief_helpers.py`

- [ ] **Step 1: Write the failing test**

```python
# append to tests/test_brief_helpers.py
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ~/Claude/DayTrader && python -m pytest tests/test_brief_helpers.py -k latest_poll -v`
Expected: FAIL — `AttributeError: module 'brief_helpers' has no attribute 'latest_poll'`.

- [ ] **Step 3: Write minimal implementation**

```python
# append to scripts/brief_helpers.py
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd ~/Claude/DayTrader && python -m pytest tests/test_brief_helpers.py -k latest_poll -v`
Expected: 3 passed.

- [ ] **Step 5: Commit**

```bash
cd ~/Claude/DayTrader
git add scripts/brief_helpers.py tests/test_brief_helpers.py
git commit -m "feat: latest_poll parses last record from poller feed"
```

---

## Task 4: `format_hard_numbers` (TDD)

**Files:**
- Modify: `scripts/brief_helpers.py`
- Test: `tests/test_brief_helpers.py`

- [ ] **Step 1: Write the failing test**

```python
# append to tests/test_brief_helpers.py
def test_format_hard_numbers_renders_table():
    record = {
        "ts_ny": "2026-06-03 06:00:01",
        "quotes": {
            "ES=F": {"price": 7500.0, "chg_pct": 0.5, "prev_close": 7462.0, "market_state": "PRE"},
        },
    }
    out = bh.format_hard_numbers(record)
    assert "2026-06-03 06:00:01" in out
    assert "ES (S&P fut)" in out
    assert "7500.0" in out
    assert "+0.50%" in out
    assert "| 10Y yield | n/a |" in out  # missing symbol renders n/a, not a crash


def test_format_hard_numbers_handles_null_price():
    record = {"ts_ny": "t", "quotes": {"ES=F": {"price": None}}}
    out = bh.format_hard_numbers(record)
    assert "| ES (S&P fut) | n/a |" in out
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ~/Claude/DayTrader && python -m pytest tests/test_brief_helpers.py -k format_hard_numbers -v`
Expected: FAIL — `AttributeError: ... 'format_hard_numbers'`.

- [ ] **Step 3: Write minimal implementation**

```python
# append to scripts/brief_helpers.py
SYMBOL_LABELS = {
    "ES=F": "ES (S&P fut)", "NQ=F": "NQ (Nasdaq fut)", "YM=F": "YM (Dow fut)",
    "RTY=F": "RTY (Russell fut)", "^VIX": "VIX", "^TNX": "10Y yield",
    "CL=F": "WTI crude", "GC=F": "Gold", "DX-Y.NYB": "DXY",
    "MSFT": "MSFT", "NVDA": "NVDA", "AAPL": "AAPL", "GOOGL": "GOOGL", "META": "META",
}


def format_hard_numbers(record: dict) -> str:
    """Render the HARD NUMBERS markdown section deterministically (no LLM)."""
    ts = record.get("ts_ny", "unknown")
    quotes = record.get("quotes", {})
    lines = [
        f"_Poller snapshot: {ts} ET (Yahoo; futures ~15-20 min delayed)_",
        "",
        "| Symbol | Price | Chg% | Prev close | State |",
        "|---|---|---|---|---|",
    ]
    for sym, label in SYMBOL_LABELS.items():
        q = quotes.get(sym)
        if not q or q.get("price") is None:
            lines.append(f"| {label} | n/a | n/a | n/a | n/a |")
            continue
        chg = q.get("chg_pct")
        chg_s = f"{chg:+.2f}%" if isinstance(chg, (int, float)) else "n/a"
        prev = q.get("prev_close")
        prev_s = str(prev) if prev is not None else "n/a"
        state = q.get("market_state", "n/a")
        lines.append(f"| {label} | {q['price']} | {chg_s} | {prev_s} | {state} |")
    return "\n".join(lines)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd ~/Claude/DayTrader && python -m pytest tests/test_brief_helpers.py -k format_hard_numbers -v`
Expected: 2 passed.

- [ ] **Step 5: Commit**

```bash
cd ~/Claude/DayTrader
git add scripts/brief_helpers.py tests/test_brief_helpers.py
git commit -m "feat: deterministic HARD NUMBERS table renderer"
```

---

## Task 5: `tier1_from_poll` (TDD)

**Files:**
- Modify: `scripts/brief_helpers.py`
- Test: `tests/test_brief_helpers.py`

- [ ] **Step 1: Write the failing test**

```python
# append to tests/test_brief_helpers.py
def test_tier1_from_poll_extracts_levels():
    record = {"quotes": {"ES=F": {"prev_close": 7462.0, "high": 7510.0, "low": 7455.0}}}
    levels = bh.tier1_from_poll(record, "ES=F")
    assert levels["symbol"] == "ES=F"
    assert levels["pdc"] == 7462.0
    assert levels["day_high"] == 7510.0
    assert levels["day_low"] == 7455.0
    assert levels["overnight_high"] is None  # not available from one snapshot
    assert "manually" in levels["note"]


def test_tier1_from_poll_missing_symbol_returns_nones():
    levels = bh.tier1_from_poll({"quotes": {}}, "ES=F")
    assert levels["pdc"] is None
    assert levels["day_high"] is None
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ~/Claude/DayTrader && python -m pytest tests/test_brief_helpers.py -k tier1 -v`
Expected: FAIL — `AttributeError: ... 'tier1_from_poll'`.

- [ ] **Step 3: Write minimal implementation**

```python
# append to scripts/brief_helpers.py
def tier1_from_poll(record: dict, symbol: str = "ES=F") -> dict:
    """Reference levels for a symbol from one poll snapshot.

    A single Yahoo quote exposes previous close + day high/low only. PDC is
    exact; day H/L approximate the most recent session range. True overnight
    H/L needs a time series, so it is None here and the routine flags it for
    manual marking.
    """
    q = record.get("quotes", {}).get(symbol, {})
    return {
        "symbol": symbol,
        "pdc": q.get("prev_close"),
        "day_high": q.get("high"),
        "day_low": q.get("low"),
        "overnight_high": None,
        "overnight_low": None,
        "note": ("PDC exact; day H/L = latest session range; overnight H/L "
                 "unavailable from single snapshot — mark manually on terminal."),
    }
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd ~/Claude/DayTrader && python -m pytest tests/test_brief_helpers.py -k tier1 -v`
Expected: 2 passed.

- [ ] **Step 5: Run the FULL suite + commit**

Run: `cd ~/Claude/DayTrader && python -m pytest tests/test_brief_helpers.py -v`
Expected: all (12) passed.

```bash
cd ~/Claude/DayTrader
git add scripts/brief_helpers.py tests/test_brief_helpers.py
git commit -m "feat: tier1 level extraction from poll snapshot"
```

---

## Task 6: Holiday doc + brief template

**Files:**
- Create: `US_MARKET_HOLIDAYS_2026.md`
- Create: `paper-trading/briefings/_TEMPLATE.md`

- [ ] **Step 1: Write the holiday doc**

```markdown
# US Market Holidays 2026 (NYSE / Nasdaq full closures)

> Source of truth for the pipeline is `scripts/brief_helpers.py::US_MARKET_HOLIDAYS_2026`.
> This file is the human-readable mirror. If they ever disagree, the Python set wins.
> Early-close (1 PM ET) days are NOT listed — the market is open, so a brief still fires.

| Date | Holiday |
|---|---|
| 2026-01-01 (Thu) | New Year's Day |
| 2026-01-19 (Mon) | Martin Luther King Jr. Day |
| 2026-02-16 (Mon) | Presidents' Day |
| 2026-04-03 (Fri) | Good Friday |
| 2026-05-25 (Mon) | Memorial Day |
| 2026-06-19 (Fri) | Juneteenth |
| 2026-07-03 (Fri) | Independence Day (observed; Jul 4 is Sat) |
| 2026-09-07 (Mon) | Labor Day |
| 2026-11-26 (Thu) | Thanksgiving |
| 2026-12-25 (Fri) | Christmas |

**For 2027:** add a `US_MARKET_HOLIDAYS_2027` set to `brief_helpers.py` and extend
`is_trading_day` to union all known years, or the routine will brief on 2027 holidays.
```

- [ ] **Step 2: Write the brief template**

```markdown
# Pre-Open Brief — {DATE} {SLOT} ET

## ⚡ ACTION
- **Regime:** {trend / balance / chop}  ·  **Gamma:** {positive / negative}  ·  **Bias:** {...}
- **Setup candidates:**

| # | Setup | Trigger | Entry | Stop | T1 / T2 | Confluence /10 |
|---|---|---|---|---|---|---|
| 1 | {Failed breakout / VWAP rejection / ORB failure} | {...} | {...} | {...} | {...} | {n} |

- **Stand-aside triggers (all must be CLEAR):** WTI > $105 · 10Y > 4.55% · VIX gap > 21 · {today's event risks}

## 📅 TODAY'S CALENDAR
- {HH:MM ET} — {event} — {consensus/prior} — [source]({url})

## 🌍 OVERNIGHT
- Asia: {...} [source]({url})
- Europe: {...} [source]({url})
- Cross-asset / geopolitics: {...} [source]({url})

## 📊 HARD NUMBERS
{deterministic table from brief_helpers.format_hard_numbers — do not hand-edit}

## ⚠️ Verify before trading
Futures numbers are delayed; levels are approximate. Confirm PDH/PDL/overnight H/L
and live prices on your own terminal before any entry. This brief is preparation, not a signal.
```

- [ ] **Step 3: Commit**

```bash
cd ~/Claude/DayTrader
git add US_MARKET_HOLIDAYS_2026.md paper-trading/briefings/_TEMPLATE.md
git commit -m "docs: 2026 holiday mirror + brief template"
```

---

## Task 7: The routine prompt

**Files:**
- Create: `scripts/MORNING_BRIEF_ROUTINE.md`

- [ ] **Step 1: Write the routine**

```markdown
# Morning Brief Routine

You are the DayTrader pre-open briefing agent. Execute these steps exactly. Your
job is preparation, not prediction. NEVER invent a number. Every price comes from
the poller; every narrative claim carries a cited source URL.

## Inputs
- Repo root: the DayTrader repo you are running in.
- Slot: `0600` or `0845` (passed in the trigger; default `0600` if unstated).

## Steps

1. **Trading-day gate.** Run:
   `python -c "import sys; sys.path.insert(0,'scripts'); import brief_helpers as b; print(b.is_trading_day(b.ny_today()))"`
   If it prints `False`, STOP. Do not write a brief. Exit cleanly.

2. **Poll hard numbers.** Run: `python scripts/live_poller.py --once`
   Then load the snapshot:
   `python -c "import sys,json; sys.path.insert(0,'scripts'); import brief_helpers as b; r=b.latest_poll('paper-trading/live-feed.jsonl'); print(b.format_hard_numbers(r)); print('---LEVELS---'); print(b.tier1_from_poll(r,'ES=F'))"`
   Capture the HARD NUMBERS table and the ES levels. If the poller failed (no
   snapshot), write the brief with HARD NUMBERS = "unavailable — Yahoo fetch
   failed" and continue. Do NOT substitute remembered or searched prices.

3. **Research narrative (built-in WebSearch only — do NOT rely on firecrawl/MCP).**
   Search for, and cite a source URL for each:
   - Today's US economic calendar (data prints, times ET, consensus/prior).
   - Overnight Asia (Nikkei/HSI) and Europe (STOXX/DAX/FTSE) closes.
   - Major market-moving / geopolitical news since yesterday's US close.
   - 0DTE dealer-gamma regime read (SpotGamma / Menthor Q / Cem Karsan public posts) — positive or negative gamma.
   Anything you cannot cite: omit it or tag `[UNVERIFIED]`. Never present an
   uncited number as fact.

4. **Classify + select.** From the data: name the regime (trend/balance/chop) and
   gamma sign. Pick 3-4 setup candidates ONLY from the 3 MVP setups — failed
   breakout, VWAP rejection, ORB failure (index ES/NQ), plus optionally one
   MSFT/NVDA single-name play. For each: trigger, entry, stop, T1/T2, confluence
   score /10. If conditions are unclear, the correct answer is an explicit
   STAND-ASIDE with the reason — that is a valid, good brief.

5. **Assemble** using `paper-trading/briefings/_TEMPLATE.md`. ACTION section first.
   Paste the deterministic HARD NUMBERS table verbatim from step 2.

6. **Write + commit.** Save to `paper-trading/briefings/YYYY-MM-DD-{slot}.md` (NY
   date). Then:
   `git add paper-trading/briefings/ paper-trading/live-feed.jsonl 2>/dev/null; git commit -m "brief: YYYY-MM-DD {slot} ET"; git push`
   (live-feed.jsonl is gitignored — the `2>/dev/null` is harmless if nothing to add.)
   If `git push` fails, retry once; if it still fails, note the failure in your
   final output so the operator knows to pull manually.

## Hard rules
- No invented prices. Poller or nothing.
- No uncited narrative claims.
- Not a trading day → no brief.
- Stand-aside is a valid brief. Do not manufacture setups to fill the table.
```

- [ ] **Step 2: Verify the routine references only things that exist**

Run: `cd ~/Claude/DayTrader && grep -oE "brief_helpers\.[a-z_]+" scripts/MORNING_BRIEF_ROUTINE.md | sort -u`
Expected: `brief_helpers.format_hard_numbers`, `brief_helpers.is_trading_day`, `brief_helpers.latest_poll`, `brief_helpers.ny_today`, `brief_helpers.tier1_from_poll` — all defined in Tasks 2-5.

- [ ] **Step 3: Commit**

```bash
cd ~/Claude/DayTrader
git add scripts/MORNING_BRIEF_ROUTINE.md
git commit -m "feat: morning brief routine prompt"
```

---

## Task 8: Fix stale poller docstring

**Files:**
- Modify: `scripts/live_poller.py:18`

- [ ] **Step 1: Fix the docstring path**

Replace the line in the module docstring:
```
    JSONL appended to C:\\Claude\\DayTrader\\paper-trading\\live-feed.jsonl
```
with:
```
    JSONL appended to paper-trading/live-feed.jsonl (see OUT_PATH below)
```

- [ ] **Step 2: Verify poller still runs**

Run: `cd ~/Claude/DayTrader && python scripts/live_poller.py --once`
Expected: prints a timestamped quote block; appends one line to `paper-trading/live-feed.jsonl`. (If Yahoo rate-limits/fails, that's acceptable here — the helper handles it; just confirm no syntax error.)

- [ ] **Step 3: Commit**

```bash
cd ~/Claude/DayTrader
git add scripts/live_poller.py
git commit -m "chore: fix stale Windows path in poller docstring"
```

---

## Task 9: GitHub private remote

**Files:** none (infra)

- [ ] **Step 1: Ensure `gh` is installed and authed**

Run: `command -v gh && gh auth status`
If `gh` is MISSING: `brew install gh` then `gh auth login` (HTTPS, follow browser prompt).
**This step needs the operator** — `gh auth login` is interactive. Stop and ask if not authed.

- [ ] **Step 2: Create the private remote and push**

```bash
cd ~/Claude/DayTrader
gh repo create daytrader --private --source=. --remote=origin --push
```
Expected: repo created at `github.com/<user>/daytrader` (private); branch pushed.

- [ ] **Step 3: Verify**

Run: `cd ~/Claude/DayTrader && git remote -v && git ls-remote --heads origin`
Expected: `origin` points to the private GitHub repo; remote branch listed.

---

## Task 10: Dry-run end-to-end (verification gate)

**Files:** produces `paper-trading/briefings/YYYY-MM-DD-0600.md`

- [ ] **Step 1: Execute the routine manually, start to finish**

Follow `scripts/MORNING_BRIEF_ROUTINE.md` by hand in this session (slot `0600`).
Market is closed, so expect "stand-aside / closed" — that is correct. The point
is to prove the mechanics: trading-day gate → poller → deterministic sections →
WebSearch narrative → assembled file → commit → push.

- [ ] **Step 2: Verify the produced brief**

Run: `cd ~/Claude/DayTrader && ls -la paper-trading/briefings/ && head -40 paper-trading/briefings/*-0600.md`
Expected: a well-formed brief with all 5 sections; HARD NUMBERS table present
(or an explicit "unavailable" note); no uncited numbers; commit pushed to origin.

- [ ] **Step 3: Confirm it landed on the remote**

Run: `cd ~/Claude/DayTrader && git log origin/main --oneline -1`
Expected: the `brief:` commit is on the remote.

---

## Task 11: Register the scheduled agents

**Files:** none (uses `/schedule`)

- [ ] **Step 1: Register the 6:00 AM ET agent**

Invoke the `schedule` skill to create a remote routine:
- **Schedule:** every Mon-Fri at 06:00 America/New_York.
- **Prompt:** "Clone/pull the private `daytrader` repo and execute
  `scripts/MORNING_BRIEF_ROUTINE.md` with slot `0600`. Follow its hard rules
  exactly — no invented numbers, stand-aside is valid, skip if not a trading day."

- [ ] **Step 2: Register the 8:45 AM ET agent**

Same as Step 1 but **08:45 America/New_York** and slot `0845`.

- [ ] **Step 3: Verify both are registered**

Run the schedule skill's list/`CronList` and confirm two routines exist with the
correct times and timezone. (Trading-day skip is enforced inside the routine, so
the cron itself is Mon-Fri.)

- [ ] **Step 4: Final commit**

```bash
cd ~/Claude/DayTrader
git add -A
git commit -m "chore: PBP complete — helpers, routine, schedules registered" --allow-empty
git push
```

---

## Done criteria
- `python -m pytest tests/ -v` → all green.
- Dry-run brief committed to the private remote.
- Two Mon-Fri ET schedules registered.
- First live brief: next trading morning, 06:00 ET.

## Out of scope (do not build)
- Trade execution, backtesting, broker integration, the other 7 setups, Telegram delivery.
