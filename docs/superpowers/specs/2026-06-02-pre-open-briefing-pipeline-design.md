# Pre-Open Briefing Pipeline (PBP) — Design Spec

**Date:** 2026-06-02
**Author:** Operator + Claude (advisor mode)
**Status:** Approved design. Next step: implementation plan.
**Project:** `~/Claude/DayTrader/` (Bucket B — Day Trader)

---

## 1. Problem statement

The DayTrader project has 61K words of research and **zero trades, zero backtests, no broker, no working live data feed**. Last activity was 2026-05-15 (18 days before this spec). The deficit is execution, not research.

One genuinely-missing, genuinely-useful piece was identified in the master file (`UNIFIED_OPERATING_SYSTEM.md` #12, "cheapest information edge"): a fresh, decision-ready pre-open briefing waiting each morning. The operator keeps skipping pre-open prep; the May 14 journal documents the cost (drifted off-screen, missed the MSFT reversal, no plan = panic).

**PBP ships a briefing machine — not a trader.** It removes the "I didn't prep" excuse. It does not place trades, prove expectancy, or substitute for the Bar Replay reps still owed in the 90-day plan.

## 2. Goals / non-goals

### Goals
- A decision-ready briefing exists each trading morning, fresh at wake-time.
- Every hard number is verifiable (no hallucinated prices).
- Output is action-first: ends in 3-4 concrete setup candidates or an explicit stand-aside.
- Runs autonomously while the operator's laptop is asleep.
- Archived (searchable history) per Marci's "collect your own data" rule.

### Non-goals (YAGNI)
- No trade execution.
- No backtesting / expectancy proof.
- No broker integration.
- No full 10-setup playbook — 3 MVP setups only.
- No multi-asset sprawl — index futures + 2 single names.

## 3. Decisions locked (from brainstorming)

| Decision | Choice |
|---|---|
| Output | Both layered — **action at top, macro context below** |
| Fire times | **6:00 AM ET** (overnight) + **8:45 AM ET** (final pre-open) |
| Delivery | **File only**, committed to a private git repo |
| Cadence | **Trading days only** (weekend + US market holiday no-op) |
| Execution substrate | **Remote scheduled agent** (`/schedule`) → private GitHub repo |
| Data accuracy | Hard numbers from Yahoo quote API only; narrative from cited `WebSearch` |

## 4. Architecture

### 4.1 Data anchor — `scripts/live_poller.py` (exists)
Polls Yahoo public quote endpoint for: `ES=F, NQ=F, YM=F, RTY=F, MSFT, NVDA, AAPL, GOOGL, META, ^VIX, ^TNX, CL=F, GC=F, DX-Y.NYB`. Appends JSONL to `paper-trading/live-feed.jsonl`. Run with `--once` for the routine.

**Contract:** this is the ONLY source of price numbers in the brief. Each number is timestamped and tagged delayed/real-time. Futures are 15-20 min delayed; equities pre-market.

Cleanup needed: docstring still references `C:\Claude\...` (cosmetic; `OUT_PATH` is already Mac-correct).

### 4.2 Routine prompt — `scripts/MORNING_BRIEF_ROUTINE.md` (ship)
The exact instruction set the remote agent executes. Steps:
1. Get NY time via `ZoneInfo("America/New_York")`. Verify trading day against `US_MARKET_HOLIDAYS_2026.md` + weekend check. **No-op + exit if not a trading day.**
2. Run `python scripts/live_poller.py --once`; parse latest JSONL record for hard numbers.
3. `WebSearch` (built-in — NOT firecrawl, which is absent in headless cron): economic calendar today, overnight Asia/Europe closes, major market/geopolitical news, 0DTE gamma regime (SpotGamma / Menthor Q free reads).
4. Compute Tier 1 levels from poller: PDH/PDL/PDC (prior session high/low/close), overnight H/L.
5. Classify regime (trend/balance/chop) + gamma (pos/neg).
6. Select 3-4 setup candidates from the 3 MVP setups + single-name, each with trigger/entry/stop/T1-T2/confluence score.
7. Assemble brief in the format below.
8. Write to `paper-trading/briefings/YYYY-MM-DD-{0600|0845}.md`; `git add/commit/push`.

**Accuracy rules baked into the prompt:** every narrative claim carries a cited source URL; any number lacking a poller source or citation is dropped or flagged `[UNVERIFIED]`. Footer always says "verify on your own terminal before trading."

### 4.3 Brief format — action-first, layered
```
## ⚡ ACTION
  Regime: [trend/balance/chop] · Gamma: [pos/neg] · Bias: [...]
  Setup candidates (3-4): name | trigger | entry | stop | T1/T2 | confluence /10
  Stand-aside triggers: WTI>$105 · 10Y>4.55 · VIX gap>21 · [today's events]
## 📅 TODAY'S CALENDAR   (data prints / earnings / Fed speakers — times ET, cited)
## 🌍 OVERNIGHT          (Asia/Europe closes, cross-asset, geopolitics — cited)
## 📊 HARD NUMBERS       (poller snapshot, timestamped)
## ⚠️ Verify-before-trading footer
```

### 4.4 Scope discipline
- Primary: ES / NQ index futures.
- Secondary: MSFT / NVDA single-name.
- Setups: failed breakout / VWAP rejection / ORB failure (the 3 MVP). No others.

### 4.5 Schedule
Two remote agents via `/schedule`, trading days only:
- 6:00 AM ET → `YYYY-MM-DD-0600.md`
- 8:45 AM ET → `YYYY-MM-DD-0845.md` (tighter; reflects 8:30 data)

## 5. Repo / infra
- `git init` in `~/Claude/DayTrader/`; private GitHub remote via `gh`.
- `.gitignore`: `.venv/`, `paper-trading/live-feed.jsonl` (churns), `__pycache__/`.
- First commit: existing research + scripts + this spec.

## 6. Failure modes & handling
| Failure | Handling |
|---|---|
| Yahoo API down | Brief notes "hard numbers unavailable"; narrative still ships; no invented numbers. |
| `WebSearch` returns thin/blocked | Section marked "limited data"; never fabricate. |
| Not a trading day | Agent no-ops, exits clean, no commit. |
| Git push fails | Agent retries once; logs failure in commit message / output. |
| Holiday list stale (post-2026) | Routine flags "holiday list expired — verify manually." |

## 7. What ships tonight
1. `git init` + private GitHub remote + first push.
2. `scripts/MORNING_BRIEF_ROUTINE.md`.
3. `briefings/` + `_TEMPLATE.md` + `US_MARKET_HOLIDAYS_2026.md`.
4. Dry-run the routine once (market closed — proves mechanics: poller→search→file→commit).
5. Register the two `/schedule` agents.
6. First live brief: Wed 2026-06-03 06:00 AM ET.

## 8. Success criteria
- Tonight's dry-run produces a well-formed brief file and a successful commit/push.
- Tomorrow's 6 AM brief exists in the repo by wake-time with no invented numbers.
- Within 1 week: operator reads the brief AND sits the 9:45-11:30 window (the real test PBP cannot enforce).

## 9. Honest limits
- Briefing machine, not a trader. No expectancy claim.
- Yahoo data is delayed for futures; treat levels as approximate until confirmed on a real terminal.
- Remote agent web research inherits the field's hallucination risk; mitigated by the poller-anchor + citation rules, not eliminated.
- The pipeline's value is gated entirely on operator screen-discipline, which it cannot enforce.
