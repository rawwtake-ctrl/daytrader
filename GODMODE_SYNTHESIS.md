# GODMODE Day Trader — Synthesis

**For:** building a "lock in profits and exit cleanly" intraday bot, with the discretionary skill to operate it.
**Date:** 2026-05-13
**Built from:** 4 parallel research streams (Marci Silfrain dossier; candlesticks/price action; S/R/volume/order flow; exit strategies). See `research/01-04` files for full source citations.

---

## 0. The Honest Frame Before Anything Else

You asked me to learn day trading at world-class level using Marci Silfrain as the anchor. After deep research, here is the most important sentence in this entire document:

> **The 320% Marci put up in the Robbins World Cup was leveraged contest behavior. She herself calls that leverage "irresponsible" and "would never use it with private capital." Copying her contest sizing is the fastest way to blow up.**

What you CAN copy is her **method, philosophy, and discipline.** That's where the GODMODE actually lives. Section 1 below is the cleanest extraction of those keepers.

The second honest sentence:

> **The single highest-leverage idea in this entire research package is not a setup. It is Van Tharp's decomposition — position sizing ≈ 60% of equity-curve variance, exits ≈ 30%, entries ≈ 10%. Andrea Unger (4x World Cup champion, ACTUAL champion, not runner-up) says explicitly: "Entries are noise. The exit is the strategy."**

That means your bot's design budget should be **70%+ on exits and sizing, ≤ 20% on entries.** The "lock in profits and exit" premise you started with is structurally correct. The four research docs converge on the same conclusion from independent angles.

---

## 1. Marci Silfrain — Real-Money Method (NOT Contest)

### 1.1 The Operating System (one page)

| Element | Rule |
|---|---|
| **Markets** | ES + NQ futures only. Nothing else. She has explicit edge here and zero edge elsewhere — she avoids gold/stocks/crypto for live trading. |
| **Bias engine** | Top-down: Monthly → Weekly → Daily for trend + key levels. Execute intraday on lower TF (specific TF not public). |
| **Setup** | "Little RZY" Measured Move Trend-Continuation (see 1.2). |
| **Stops** | **Hard, static, no trailing.** Either target hits or stop hits. Her data shows trailing hurts her edge. |
| **Targets** | Measured-move projection (see 1.2). Partials allowed; let the move complete. |
| **Sizing** | Dynamic — adds to **confirmed winners**. Conservative base size in real money. |
| **Leverage** | Conservative. Ego + leverage = "the two enemies." |
| **Daily kill switch** | Behavioral, not numeric. Notice tilt → walk away for days or weeks. |
| **Routine** | 6 days/week. More hours in sim/backtest than live trading. Manual data collection. Trains across regimes (1929, 2000, 2008). |
| **Mental rule** | Pre-commit to 20 losses in a row. If that breaks you, you're over-sized. |
| **Win rate** | Below 50%, profitable via R-multiple expectancy + scaling into winners. |

### 1.2 The Little RZY Setup

Her published, named setup on Chart Fanatics. Step by step:

1. **Identify the trend on higher timeframes.** Down = LH/LL. Up = HH/HL.
2. **Wait for the impulse move AND THEN a pullback.** Never enter during the impulse. "The setup forms after the bounce, not during the impulse."
3. **Draw a trendline across the pullback.** Across pullback highs in a downtrend, pullback lows in an uptrend. Each Little RZY gets its **own** trendline — not one continuous line across the whole trend.
4. **Measure the move.** Vertical distance from swing extreme to trendline.
5. **Project that distance** in the trend direction → that's your target.
6. **Entry:** Wait for the pullback to form and BEGIN rejecting the trendline. Enter on the reversal off the trendline back in the direction of the larger trend.

**Reliability rule:** First and second RZY structures in a trend = strong continuation. Fourth/fifth structures = exhaustion warning.

**Bollinger Bands** used as context, not signal: best longs in uptrend = early RZY structures near LOWER band (room to run). Best shorts in downtrend = early structures near UPPER band. Reverse situation = exhaustion alert.

**Invalidation:** Close beyond trendline / irregular structure / collapse without pullback.

### 1.3 Quotes That Should Live Above Your Desk

1. *"The two biggest enemies of a trader are ego and leverage."*
2. *"Plan to lose the next twenty trades in a row. If that thought destroys you, you are over-leveraged."*
3. *"I am 100% model driven... I often am forced to trade against my own [intuition]."*
4. *"Without manually collecting your own data, you are flying blind."*
5. *"No trading system works in all market conditions."*
6. *"I spend more time looking at charts pretending to trade than I actually do trading."*
7. *"Trading without emotions is a lie. The skill is noticing and stopping — sometimes for days, sometimes for weeks."*

### 1.4 What She Did WRONG Early (the $250K loss period)

- Looking for shortcuts / paid courses
- Over-leverage + ego
- Trading other people's setups instead of running her own backtests
- Trading without practicing first
- Trading through emotional dysregulation

The pattern: she did not collect her own data, did not respect leverage, and did not have a tilt-stop. All three are non-negotiable now.

---

## 2. The Unified Mental Model — How a Pro Reads a Chart

This is the synthesis of curriculum docs 02 and 03. It is the lens through which Marci's setup (or any setup) actually works.

### 2.1 The HTF → MTF → LTF Cascade

> **HTF picks the bias. MTF picks the level. LTF picks the entry.**

| Role | TF (futures) | Question it answers |
|---|---|---|
| Macro bias | Daily/Weekly | Long bias / short bias / chop? Above or below prior week VAH/VAL? |
| Swing context | 60m or 4h | Where's the current intraday auction range? |
| Intraday bias | 15m | Trend direction this session? |
| Entry trigger | 5m | Specific setup forming? |
| Execution timing | 1m | Optimal entry tick within the 5m setup |

**Marci's framework maps directly:** Monthly/Weekly/Daily = HTF bias. Lower TF (her "execution timeframe") = entry trigger.

### 2.2 What ACTUALLY Causes Support and Resistance

Retail teaches "places price reversed before." Wrong. The actual causes:

1. **Resting limit-order liquidity** (real bids/offers parked) — the only literal definition
2. **Inventory/positioning levels** institutions must hedge against (VWAP, settlement, OPEX strikes, dealer gamma)
3. **Behavioral anchors with mass participation** (round numbers, ATHs, prior-year settlement)
4. **Reference prints anchoring P&L** (RTH open, prior session H/L/C, IB, London close, MOC)

**Signal-density hierarchy:**

| Tier | Sources | Trade these |
|---|---|---|
| **1** | Prior day H/L/C/POC, prior week H/L, ON H/L, VAH/VAL, VWAP+bands | ALWAYS mark, primary trade locations |
| **2** | Globex H/L, IB H/L, opening range, round numbers (50pt NQ, 5pt ES) | Confirmation only |
| **3** | HTF swing highs/lows on daily/weekly | Slow but durable context |
| **4** | Fibs, trendlines drawn from charts alone, supply/demand boxes | Confluence only — never standalone |

If a level isn't Tier 1 or 2, don't let it veto a trade.

### 2.3 Volume — Done Correctly

**RVOL is the only honest framing.** Absolute volume tells you nothing because of the intraday U-shape (open ~30%, close ~25%, lunch lowest).

Compare each bar to its **same time-of-day rolling average over last 20 days.** TradingView and most platforms have this as "RVOL" or "Relative Volume."

**VWAP =** the execution benchmark institutions are graded against. Algorithms target it. Use:
- Above session VWAP = long bias. Below = short. Crossed twice in 30 min = chop, stand aside.
- In trend day: VWAP rejection from the trend side is high-EV (see Setup #3 below).
- In balance day: VWAP is a magnet for mean reversion.

**Anchored VWAP** (Brian Shannon) — VWAP from a specific event (prior day high, news release, IPO, earnings). The anchor matters more than the math. Most useful: AVWAP from a news event for the next 1-3 hours.

**Volume Profile** (Dalton, Steidlmayer):
- POC = highest-volume price = "fair value" anchor
- VAH/VAL = 70% volume range = where price accepted
- **HVN** = chop magnet (trade through, not into)
- **LVN** = thin zone (price moves fast through it; good stop-loss location)

**Cumulative Delta** (only meaningful on futures with single book — ES/NQ/CL clean, equities messy due to dark pools):
- Delta divergence at S/R = reversal signal
- Stuck delta (big positive, no price move) = absorption = reversal warning
- Delta flush + return to support = capitulation = high-EV long

### 2.4 Liquidity & Microstructure (the SMC mechanic, without the cult)

The honest version of "Smart Money Concepts":

- **Equal highs/lows = stop clusters.** Empirically true, observable on Bookmap. Not controversial.
- **Sweep / stop run** = price punches obvious level → triggers resting stops → either continues (breakout) or fails (reversal).
- **Displacement** = outsized bar through a level with participation = Brooks "strong trend bar" = marubozu. Same concept under three names.
- **Failed auction** (Dalton) = Wyckoff spring/upthrust = Grimes 2B = Sperandeo failure test = **the single highest-EV intraday setup.** All four names describe the same trade.

**Ignore as cult-speak:** "Kill zones," "judas swings," "power of three," "AMD," "silver bullet," FVG mysticism. The underlying ideas are real but the framing inflates the precision.

### 2.5 Setup Signature: What Distinguishes a Real Failed Breakout from Noise

The single most repeatable intraday setup. Anatomy:

1. Market drifts toward known Tier-1/2 level on tepid volume
2. Approach accelerates — small algos test the level
3. **Sweep**: a burst of aggressor volume through, eating resting stops
4. Branch:
   - **Continuation**: real breakout — buyers above stops > sellers waiting → holds → extends
   - **Reversal (failed)**: resting offers > stop-run + continuation buyers → price slams back through level → trapped breakout traders feed the move

**How to tell which branch in real time:**

| Signal | Continuation | Reversal |
|---|---|---|
| Delta after sweep | Stays positive | Flips negative in 1-2 min |
| Bookmap above level | Thin (vacuum) sustained | Wall reappears OR iceberg seller |
| Time spent above | Holds 10+ min | Pokes and reclaims fast |
| Volume after sweep | Sustained high RVOL | Drops off a cliff |

**Trade rule:** Wait for reclaim of level. Enter on close back inside. Stop just past the swept extreme + 2 ticks (ES) / 5-10 ticks (NQ). Target = prior structure / VWAP / opposite side of range.

### 2.6 Time of Day = Edge

US equity-index futures volume distribution (U-shape, academic consensus):
- **9:30-10:30 ET**: ~30% of daily volume. ORB setups live here.
- **10:30-11:30 ET**: Continuation or first reversal.
- **11:30-13:30 ET**: Lunch lull. Mean-reverting; small VWAP scalps OR stand aside.
- **13:30-15:00 ET**: Afternoon trend.
- **15:00-16:00 ET**: Power hour. ~25% of daily volume. MOC imbalances build.

**If you can only trade two windows:** NY open (9:30-11:00) and power hour (15:00-16:00). Together = 55-65% of daily volume and majority of day-trader profits.

---

## 3. The 10 Setups Worth Trading

From integration of docs 02 and 03. Each has clear entry/stop/target. **Memorize these. Everything else is noise.**

| # | Setup | Trigger | Stop | Target | R:R | Best regime |
|---|---|---|---|---|---|---|
| 1 | **Failed Breakout / Failure Test** (the gold standard) | Close back inside level after sweep | Past swept extreme +2T | VWAP / opposite range edge | 2-4:1 | All |
| 2 | **Marci's Little RZY** | Reject off pullback trendline in HTF trend | Past trendline / swing | Measured-move projection | 2-3:1 | Trending |
| 3 | **VWAP Rejection (trend day)** | Wick rejection at VWAP ±1σ | Beyond VWAP cluster | HOD/LOD | 2-5:1 | Trend day only |
| 4 | **Prior Day High/Low Test** | Failure test OR clean break+retest | Past level | Opposite side of prior range | 3:1 | All |
| 5 | **ORB Failure** | Reclaim of OR range after extension fail | Beyond extension high | OR opposite extreme | 2:1 | Balance day |
| 6 | **Open-Drive Continuation** | Pullback to opening print or VWAP | Beyond OR opposite extreme | Prior swing on daily or 2 ATR | 2-4:1 | Trend day |
| 7 | **Trend Pullback (Brooks high-1/low-2)** | Break of pullback bar high (uptrend) | Below pullback low | Prior swing / 1.5 ATR | 1.5-3:1 | Trending |
| 8 | **Reversal at HTF Level** | LTF break of structure after HTF level test | Beyond HTF level | 3-8R home run | 3-8:1 | All |
| 9 | **LVN Traversal** | Entry from HVN into LVN with momentum | Back inside originating HVN | Opposite HVN | 2-3:1 | Profile-aware |
| 10 | **AVWAP-from-event Rejection** | Footprint imbalance + rejection at AVWAP | ATR-based above AVWAP | Prior swing / daily VWAP | 2-4:1 | Equities; gap/news days |

### Setups to NOT Trade (retail filler that doesn't backtest)

- Three white soldiers / three black crows as standalone entries (move is exhausted by bar 3)
- Cup & handle on intraday 5m (pattern needs many bars to form)
- Head & shoulders intraday (rare clean symmetry)
- "Ascending triangle = 70% bullish" pattern claims (cherry-picked, no robust evidence)
- MA crossovers as triggers (lagging by definition)
- Harmonic patterns (Gartley, butterfly, bat — retrofitted geometry)
- Doji-in-isolation reversals
- Indicator divergence as primary entry (RSI/MACD/Stoch)

---

## 4. The Exit Stack — Where 70% of Your Bot's Design Goes

From doc 04. This is the structural answer to "lock in profits and exit."

### 4.1 The 5-Layer Stack (every layer runs every bar — first fire wins)

```
LAYER 1 — Catastrophe Stop (broker-side bracket)
LAYER 2 — Hard Initial Stop (strategy logic, = 1R)
LAYER 3 — Profit Target 1 (scale 50% at +1R, move L2 to BE)
LAYER 4 — Trail on Remainder (Chandelier ATR×2.5, floor at BE)
LAYER 5 — Time Stop (no-progress kill + EOD flat)
```

### 4.2 The Minimum-Viable Defaults (start here, walk-forward later)

| Parameter | Default | Source justification |
|---|---|---|
| Initial stop | 1R | Standard; defines R for everything else |
| Catastrophe stop | 3R, broker-side | Protection against your own bugs |
| Profit target 1 | +1R, exit **50%** | Raschke/Connors + Grimes consensus |
| BE rule | Move stop to entry on L3 fill | Makes trade structurally unable to lose |
| Trail method | Chandelier (ATR-based) | Highest single-method winner across regimes (Pardo walk-forward) |
| Trail ATR period | 14 on entry TF | LeBeau original, optimized |
| Trail k-multiplier | 2.5 | Walk-forward cluster (Pardo Ch. 11) |
| No-progress | Flat if PnL < +0.3R after 30 min | Reduces opportunity cost |
| EOD flat | 15:45 ET (stocks/ETFs), 16:00 (futures) | Day-trading bot premise |

### 4.3 Adapt by Strategy Archetype

| Archetype | Win-rate | Scale at +1R | Trail k |
|---|---|---|---|
| Scalp / mean-reversion | >60% | **75-100%** (whole position OK) | n/a or tight |
| Momentum / pullback (Marci-style) | 45-55% | **50%** | 2.5 |
| Breakout / trend | <45% | **25-33%** | 3.5 OR structure trail |

**For your "lock in profits" project specifically:** 50% at +1R, Chandelier k=2.5 on remainder, BE floor, EOD flat. This is the canonical setup. Robust, well-studied, tolerant of optimization error.

### 4.4 Time-of-Day Exit Overrides

| Window (ET) | Override |
|---|---|
| 09:30-10:00 | Widen trail to k=3.5 (open volatility expands ATR) |
| 10:00-11:30 | Default stack |
| 11:30-13:30 | **Lunch lull.** Tighten no-progress to 20 min; force flat by 12:00 on chop |
| 13:30-15:00 | Default stack |
| 15:00-15:45 | Power hour. Default but enforce hard EOD at 15:45 |
| 15:45-16:00 | No new positions; flatten existing |

### 4.5 Regime Overrides

- **Chop day**: by 11:30, if day's range < 0.5 × 20-day ADR → force flat. No edge from holding.
- **Trend day**: by 11:30, if range > 1.5 × ADR and direction clear (close near high/low) → widen trail to k=4.0, disable no-progress kill, ride to EOD.

### 4.6 Marci's Exit Compared

She uses **hard static stops, no trailing.** Her data shows trailing hurts HER edge on HER setup (measured-move continuation). This is consistent with: **on systems where the right tail is the edge (her measured-move target IS the right tail), trailing cuts the tail.** For systems where you DON'T know the target in advance (which is most strategies), trailing is the answer.

**Decision for your bot:** if your entry has a clean target (measured move, level test), use Marci's static-stop approach. If your entry has no clear target (momentum / breakout), use the Chandelier trail. **Probably you'll want both, gated by setup type.**

---

## 5. The Cognitive / Psychology Layer

From Steenbarger's work (referenced across all 4 docs) + Marci's quotes:

### 5.1 The Tilt Detector (Marci's actual circuit breaker)

She has **no fixed dollar daily-loss cap.** Her rule is behavioral:

- Notice emotional dysregulation → STOP TRADING IMMEDIATELY → walk away for days or weeks until clean again.

For a bot, this translates to a **kill switch with cool-off**:
- Drawdown trigger: -2R intraday → halt entries for the session
- Consecutive losses: 3 in a row → halt for 30 min minimum, manual restart required
- Time-out trigger: 5 trades in 60 min → halt (over-trading symptom)

### 5.2 The 7 Cognitive Failure Modes (memorize)

1. **Confirmation bias on candles** — you decided ES is going up; you see hammers everywhere
2. **Over-detection** — "I see a hammer at every wick" — once you learn a pattern you over-fire it
3. **Small-sample overfitting** — 3 wins in a row ≠ 75% strategy; n=200 minimum for honest hit-rate
4. **Regime blindness** — pattern works in one regime, fails in another (ORB worked 2010-15, marginal now)
5. **Narrative construction after loss** — one loss → "the setup doesn't work" → abandons real edge
6. **Pattern without context worship** — the candle is the trigger, context is the edge
7. **Latency self-delusion** — most retail traders are 50-200ms slower than algos; structural edges > reflex edges

### 5.3 The 10 Anti-Patterns (everything aligns and you still lose)

1. Trend day misclassified as balance (you faded VWAP on an Open-Drive)
2. Macro/news override (FOMC kills your stop regardless of structure)
3. Stale level (3-week-old swing has no resting liquidity)
4. Spoofed wall (book wall pulls before price arrives)
5. Correlated double-counting (S/R + Fib + trendline + MA all from same swing = 1 level wearing 4 hats)
6. Time-of-day mismatch (failed auction in lunch lull peters out)
7. Wrong-instrument confirmation (ES level gorgeous but NQ already broke — laggard catches up)
8. Volume climax that wasn't (wide-range bar mid-range ≠ exhaustion)
9. Liquidity trap near roll/expiry/holiday
10. Setup was 8/10 but your size was 10/10 — process discipline failure

---

## 6. The Confluence Scoring Rubric

From doc 03. Use to force discipline. Score every setup 0-10. **Take trades at 6+. Size up at 8+.**

| Component | 0 | 1 | 2 |
|---|---|---|---|
| HTF context | Trade against HTF | Neutral | With HTF |
| MTF level quality | Tier 4 alone | Tier 2-3 single source | Tier 1 or 2+ sources confluent |
| Volume at level | Rising RVOL on approach (continuation risk) | RVOL ≈ 1 | Falling RVOL or arrival climax |
| Order flow / delta | None or contrary | Neutral | Divergence or absorption visible |
| Time of day | Lunch or last 5 min | Mid-morning/afternoon chop | Open (9:30-10:30) or close (15:00-16:00) |

**Discretionary additions:**
- +1 if clean failed-auction print visible
- +1 if liquidity behind your stop is a wall (defended) not a vacuum
- -2 if trading INTO an HVN expecting a fast move
- -2 if RVOL < 0.8 on level test

---

## 7. The Build Plan for the Day Trader Bot

Drawing from all 4 docs to translate research into a concrete build.

### 7.1 Architecture Sketch

```
┌─────────────────────────────────────────────────────┐
│ DATA LAYER                                          │
│  - Real-time bar feed (1m/5m/15m/60m for ES, NQ)    │
│  - Volume Profile composite (rolling 5-day + session)│
│  - VWAP + ±1σ/±2σ bands (session + anchored)        │
│  - RVOL (vs 20-day same-minute baseline)            │
│  - Cumulative delta (if futures broker supports)    │
└─────────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│ BIAS LAYER (HTF)                                    │
│  - Daily trend (HH/HL or LH/LL on 60m)             │
│  - Prior day H/L/C/POC                             │
│  - Prior week H/L                                  │
│  - Above/below 20-day VWAP                         │
│  - Today's classification: trend / balance / chop  │
└─────────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│ SETUP LAYER (10 setups from section 3)              │
│  - Each setup = function returning Signal or None   │
│  - Setup confluence score (0-10) per rubric         │
│  - Time-of-day gate                                 │
│  - Regime gate (trend vs balance vs chop)           │
└─────────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│ EXECUTION LAYER                                     │
│  - Position sizing (1% of capital per R as default) │
│  - Entry order (limit at trigger or market on close)│
│  - Layer 1: Broker-side catastrophe bracket at 3R   │
│  - Layer 2: Local hard stop at 1R                   │
│  - Layer 3: Limit at +1R for 50% scale              │
│  - Layer 4: Chandelier trail (active post-L3)       │
│  - Layer 5: Time stop + EOD flat                    │
└─────────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│ TILT DETECTOR                                       │
│  - -2R intraday → halt session entries              │
│  - 3 losses in a row → 30min cool-off               │
│  - 5 trades in 60min → over-trading halt            │
│  - Manual restart required after halt               │
└─────────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│ JOURNAL + ANALYTICS                                 │
│  - Every trade: setup_id, score, R outcome, regime │
│  - Process score (rules followed Y/N)               │
│  - 30-trade rolling stats per setup                 │
│  - Per-setup expectancy + Sharpe                    │
└─────────────────────────────────────────────────────┘
```

### 7.2 The MVP Setup Roster (start with 3, not 10)

For the first version of the bot:

1. **Failed breakout at PDH/PDL** (the gold standard, highest EV, works in any regime)
2. **VWAP rejection on trend days** (the cleanest continuation setup)
3. **ORB failure** (specific to first 30 min, well-defined trigger)

Three setups × hard-coded exits = enough surface area to find positive expectancy. Add more once these 3 are demonstrably profitable on walk-forward.

### 7.3 Walk-Forward Plan

Per Pardo (2008):
- **In-sample**: 2024 Q1-Q3 (9 months)
- **Out-of-sample**: 2024 Q4 (3 months)
- **Re-optimize quarterly** rolling forward
- **Required**: positive net expectancy on out-of-sample AND $1 slippage test passed AND ≥ 100 trades per setup in out-of-sample window

### 7.4 The Slippage Reality Check

Per doc 04 (Aronson's "$1 test"):
- Model **2 ticks slip on stops, 1 tick on limits, full spread on market exits**
- Add **commission**: $0.65-$1.50 per ES contract round-trip
- **If your backtested edge collapses at $1 of round-trip cost, the edge is fake.** Throw it out.

---

## 8. The 90-Day Drill Plan (Convert Reading → Reflex)

Adapted from doc 02 + Marci's "more hours pretending than trading."

**Days 1-30: Annotate, don't trade.**
- Mark up 50 historical 5-min ES sessions by hand
- Annotate: market structure (HH/HL/LH/LL), PDH/PDL, ORH/ORL, VWAP, VAH/VAL
- Identify every failure test, ORB break/fail, VWAP rejection that occurred
- Tag each session as trend / balance / chop after the fact
- Zero live trades. The goal is calibrating the eye.

**Days 31-60: Sim only.**
- Sim trade ONE setup: failure test at PDH/PDL/ORH
- Minimum 100 trades
- Journal every trade: screenshot, context, regime, R outcome, process score (rules followed?)
- Target ≥1.5R average, ≥50% hit rate
- Run the exit stack on every trade exactly as designed

**Days 61-90: Add second setup + small live.**
- Add VWAP rejection on trend days
- Move to micro-contract live ONLY after sim shows 100 trades positive expectancy
- Smallest size that still incurs commission (so the slippage reality bites)
- Same exit stack, same journal

**Days 90+: Scale.**
- If 100 live trades show same expectancy as sim → scale up
- If live underperforms sim by >0.3R per trade → diagnose execution / slippage / behavioral leak, do NOT scale

---

## 9. What To Read (Priority Order)

Compiled from all 4 docs. Read in this order.

**First (foundations):**
1. Adam Grimes — *The Art and Science of Technical Analysis* (2012) — single best book for someone with quant background moving to discretionary
2. Al Brooks — *Reading Price Charts Bar by Bar* (2009) — dense, repetitive, indispensable for price action vocabulary
3. James Dalton — *Mind Over Markets* (1990/2013 revised) — auction theory bible

**Second (execution + exits):**
4. Robert Pardo — *Evaluation and Optimization of Trading Strategies* (2008) — walk-forward methodology
5. Van Tharp — *Trade Your Way to Financial Freedom* + *Definitive Guide to Position Sizing* — R-multiple framework
6. David Aronson — *Evidence-Based TA* (2006) — bootstrap testing, kills bad strategies

**Third (microstructure + tape):**
7. Larry Harris — *Trading and Exchanges: Market Microstructure for Practitioners* (2002)
8. Brian Shannon — *Maximum Trading Gains with Anchored VWAP* (2022)
9. Trader Dale — *Order Flow Trading for Fun and Profit* (2017)

**Psychology (read alongside everything else):**
10. Brett Steenbarger — *Psychology of Trading* + *Trading Psychology 2.0*

**Free online:**
- Adam Grimes blog (adamhgrimes.com), especially the Failure Test series
- FuturesTrader71 / Morad Askar — free YouTube, Convergent Trading
- Bulkowski's Pattern Site — use as a debunking reference, not strategy

**For Marci specifically:**
- The Words of Rizdom interview (YouTube Dt9vzMmf__o)
- Her X feed @MarciSilfrain
- Chart Fanatics "Measured Move Trend Strategy" playbook

---

## 10. The TL;DR You Should Print and Tape to the Monitor

### Marci's wisdom that beats everything else
> **"The two biggest enemies of a trader are ego and leverage. Plan to lose 20 trades in a row."**

### The structural truth
> **Position sizing ≈ 60% of variance. Exits ≈ 30%. Entries ≈ 10%. Spend 70%+ of your design budget on the exit stack.**

### The minimum-viable bot exit stack
```
INITIAL STOP:        entry - 1R (Layer 2)
CATASTROPHE STOP:    entry - 3R, broker-side (Layer 1)
PROFIT TARGET 1:     entry + 1R, exit 50%, move L2 to BE (Layer 3)
TRAIL ON REMAINDER:  Chandelier ATR(14), k=2.5, BE floor (Layer 4)
NO-PROGRESS KILL:    flat if PnL < +0.3R after 30 min (Layer 5a)
EOD FLAT:            market exit at 15:45 ET (Layer 5b)

CHOP-DAY OVERRIDE:   flat by 12:00 if range < 0.5x ADR
TREND-DAY OVERRIDE:  widen trail to k=4.0, disable no-progress,
                     ride to EOD if range > 1.5x ADR by 11:30
```

### The 3 setups to start with
1. **Failed breakout at PDH/PDL** (the highest-EV intraday setup; works any regime)
2. **VWAP rejection on trend days** (cleanest continuation)
3. **ORB failure** (well-defined trigger in first 30 min)

### The confluence score rule
- Take trade at 6+/10
- Size up only at 8+/10
- Below 6 is not your trade, no matter how good it "looks"

### The non-negotiables
- No trade without HTF bias alignment
- No trade without a Tier 1 or 2 level
- No trade in the 30 min before high-impact data (FOMC, CPI, NFP)
- No trade after -2R intraday (session halt)
- No trade after 3 consecutive losses (30-min cool-off)
- No position held past EOD (15:45 ET hard flat)

---

## Appendix — File Map

All research files in `C:\Claude\DayTrader\research\`:

- **01-marci-silfrain-deep-dive.md** — Full dossier on Marci's method, quotes, history, contest-vs-real
- **02-candlesticks-price-action.md** — Curriculum: 10 candle patterns + market structure + breakouts + SMC honesty + 10 pro setups + failure modes
- **03-support-resistance-volume.md** — Curriculum: S/R causes + Volume Profile + VWAP/AVWAP + cumulative delta + order flow + microstructure
- **04-exit-strategy-lock-profits.md** — Exit taxonomy + comparative reality + 5-layer exit stack + Python pseudocode + "lock in profits" direct answers

This synthesis at `C:\Claude\DayTrader\GODMODE_SYNTHESIS.md`.

---

*Last updated 2026-05-13. This is the master synthesis. When in doubt, return to Section 0 — the contest leverage was not the method.*
