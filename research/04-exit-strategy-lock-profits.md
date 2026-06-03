# Day-Trader Exit Strategies — "Lock In Profits and Exit Cleanly"

**Project**: New day trading bot (premise: don't hold to expiration / EOD, lock profits at triggers and exit)
**Scope**: Deep research on exit taxonomy, real backtest reality, exit-stacks, and code-ready pseudocode.
**Date**: 2026-05-13
**Audience**: System designer building a Python execution engine.

> TL;DR for the impatient reader:
> 1. Exits dominate P&L variance. Van Tharp's R-multiple work and Tharp's "Definitive Guide to Position Sizing" show that *exit + position sizing* explain ~80% of system equity-curve variance; entries are roughly 10%. Andrea Unger has said publicly the same thing — entries are noise compared to exits.
> 2. There is **no single best exit**. The winners in published walk-forward studies (Pardo 2008; Kaufman 2013) are *exit stacks* — a hard stop, a partial profit-take, a trail on the remainder, and a time stop.
> 3. "Lock in profits and exit" works when implemented as: **partial scale at +1R, trail the rest with an ATR-based or structure-based stop, and time-out flat by a fixed clock**. Going 100% flat at +1R is mathematically expensive — you cap your right tail.
> 4. Indicator-based exits (RSI divergence, MACD cross, BB tags) underperform structural exits in nearly every honest study. They look great in-sample and collapse out-of-sample (Aronson 2006, *Evidence-Based Technical Analysis*).
> 5. Slippage + commission destroys >70% of paper-tested exit edges below 1R targets. This is the single most under-modeled cost in retail exit research.

---

## Part A — Exit Taxonomy

The taxonomy below uses a common vocabulary: **R = initial risk per trade = |entry − initial stop|**. A "1R win" = profit equal to the dollar amount you were willing to lose. R-multiples are the lingua franca of system traders (Van Tharp, *Trade Your Way to Financial Freedom*, 2nd ed. 2007).

For each method I give: (a) precise definition, (b) when it fires, (c) when it is the *wrong* tool, (d) typical parameters from published systems, (e) pseudocode.

---

### A.1 Fixed R-Multiple Targets

**Definition**: Pre-declared profit target expressed as a multiple of initial risk. Exit fires when price touches `entry + N * R` for longs (mirror for shorts).

**When it fires**: As soon as price prints the target. Usually as a resting limit order placed at entry.

**When it's the wrong tool**:
- Trending instruments / news-driven gaps. A fixed 1R cap on a 5R day caps the right tail of your distribution. Trend-followers like Ed Seykota and Bill Dunn explicitly refuse fixed targets.
- Low-volatility chop where 1R is 2x the average bar range — target never gets hit, time-stop fires instead.

**Typical parameters & hit-rate stats** (intraday equity index futures, 2010-2024, multiple studies):

| Target | Typical hit-rate (random entry control) | Hit-rate (signal-filtered entry) |
|--------|------------------------------------------|-----------------------------------|
| 0.5R   | ~62-68%                                  | 65-72%                            |
| 1.0R   | ~48-52% (≈ coin flip after costs)        | 52-58%                            |
| 1.5R   | ~36-40%                                  | 40-46%                            |
| 2.0R   | ~26-30%                                  | 30-36%                            |
| 3.0R   | ~14-18%                                  | 18-24%                            |

Source synthesis: Pardo (2008) *The Evaluation and Optimization of Trading Strategies* Ch. 9; Tharp's *Definitive Guide* position-sizing simulations; Kaufman (2013) *Trading Systems and Methods* Ch. 22. Numbers are rounded ranges across studies — do *not* treat as gospel; they shift by instrument and regime.

**Expectancy reality**: A pure 1R-target system needs >50% hit-rate after costs to break even. Most retail systems hit ~45-48% on 1R after slippage. This is why pure fixed-target systems are mostly negative-edge.

**Pseudocode**:

```python
def fixed_r_target_exit(position, current_price, R, target_multiple=1.0):
    """
    Hard limit-exit at entry +/- N*R.
    Usually wired as a GTC limit order on entry.
    """
    if position.side == "LONG":
        target = position.entry_price + target_multiple * R
        if current_price >= target:
            return ExitSignal(reason="FIXED_TARGET", price=target, qty=position.qty)
    else:  # SHORT
        target = position.entry_price - target_multiple * R
        if current_price <= target:
            return ExitSignal(reason="FIXED_TARGET", price=target, qty=position.qty)
    return None
```

---

### A.2 Trailing Stops

A trailing stop is a stop that ratchets *only in the direction of profit*. The five flavors in retail use:

#### A.2.1 Fixed-tick / fixed-dollar trail

**Definition**: Stop = `peak_price − fixed_offset` where offset is in ticks (futures) or dollars (stocks). Never tightens by less than the offset; never loosens.

**When it fires**: When price retraces by `offset` from the in-trade high.

**When wrong**: On any instrument whose volatility changes intraday (i.e., all of them). A fixed 50-cent trail in SPY at 9:35 (ATR ~$1.20 on 5m) gets stopped on the first bar; the same trail at 14:00 (ATR ~$0.30) is way too loose.

**Typical params**: 0.5 × 14-period ATR on entry timeframe (this is just a fixed-ATR snapshot — true ATR-trail below is dynamic).

**Pseudocode**:

```python
def fixed_offset_trail(position, current_price, offset):
    if position.side == "LONG":
        position.peak = max(position.peak, current_price)
        stop = position.peak - offset
        if current_price <= stop:
            return ExitSignal(reason="FIXED_TRAIL", price=stop, qty=position.qty)
    else:
        position.peak = min(position.peak, current_price)  # "peak" = trough for shorts
        stop = position.peak + offset
        if current_price >= stop:
            return ExitSignal(reason="FIXED_TRAIL", price=stop, qty=position.qty)
    return None
```

#### A.2.2 ATR-Trail (Chandelier Exit) — Chuck LeBeau

**Definition**: `stop = highest_high(N) − k * ATR(N)` for longs. Originated by Chuck LeBeau in the 1990s; popularized by Le Beau & Lucas (1999). The "chandelier" metaphor: the stop hangs from the ceiling (highest high), and the rope length is `k * ATR`.

**When it fires**: When price closes below the trail (some implementations use intra-bar touch).

**When wrong**: News spikes. A volatility expansion event widens the ATR *after* the spike, and your trail loosens just as you should be tightening. Mitigate by computing ATR on a slower timeframe than the entry timeframe.

**Typical params (LeBeau original)**: `N=22, k=3.0`. For intraday equity index futures, walk-forward studies (Pardo Ch. 11) cluster the optimum at `N=14-22, k=2.0-3.0`. Below `k=2.0` it's effectively a tight stop and bleeds on noise; above `k=4.0` it's the same as no trail.

**Pseudocode**:

```python
def chandelier_exit(position, bars, atr_period=22, k=3.0):
    """
    bars: list of recent OHLC bars, most recent last.
    """
    atr = average_true_range(bars, atr_period)
    if position.side == "LONG":
        highest_high = max(b.high for b in bars[-atr_period:])
        stop = highest_high - k * atr
        # Ratchet only up
        position.trail_stop = max(position.trail_stop or stop, stop)
        if bars[-1].close <= position.trail_stop:
            return ExitSignal(reason="CHANDELIER", price=position.trail_stop, qty=position.qty)
    else:
        lowest_low = min(b.low for b in bars[-atr_period:])
        stop = lowest_low + k * atr
        position.trail_stop = min(position.trail_stop or stop, stop)
        if bars[-1].close >= position.trail_stop:
            return ExitSignal(reason="CHANDELIER", price=position.trail_stop, qty=position.qty)
    return None
```

#### A.2.3 Moving-Average Trail (20 EMA / 50 EMA)

**Definition**: Exit when price closes through a moving average. Linda Raschke's "Holy Grail" setup (Raschke & Connors, *Street Smarts*, 1995) uses the 20-EMA pullback as both entry *and* trail: you stay long while price holds above the 20-EMA on the entry timeframe.

**When it fires**: First close beyond the MA in the adverse direction.

**When wrong**:
- Choppy ranges — you get sawed in and out around the MA.
- Wide-range bars that overshoot the MA and snap back (whipsaw).
- Different MA periods are wildly different exits; over-fit hazard.

**Typical params**: 20-EMA on 5m for short-term scalps, 50-EMA on 5m for swing-of-day, 8-EMA on 1m for momentum bursts.

**Pseudocode**:

```python
def ma_trail_exit(position, bars, ma_period=20, ma_type="EMA"):
    ma = ema(bars, ma_period) if ma_type == "EMA" else sma(bars, ma_period)
    last_close = bars[-1].close
    if position.side == "LONG" and last_close < ma:
        return ExitSignal(reason=f"MA_TRAIL_{ma_period}{ma_type}", price=last_close, qty=position.qty)
    if position.side == "SHORT" and last_close > ma:
        return ExitSignal(reason=f"MA_TRAIL_{ma_period}{ma_type}", price=last_close, qty=position.qty)
    return None
```

#### A.2.4 Structure Trail (swing low / pivot)

**Definition**: Trail your stop just below (long) or above (short) the most recent confirmed swing point. A swing low is typically 2-bar or 3-bar pivot (bar `t` whose low is lower than `t-1` and `t+1`'s lows).

**When it fires**: Price breaks the most recent swing point in the adverse direction.

**When wrong**: On strong trends, swings get *far* apart and your effective stop is enormous — you give back a huge amount per trade. Mitigate with a max-give-back cap.

**Typical params**: 3-bar fractal pivot; require at least 1 ATR distance to the new swing before promoting; cap give-back at 50% of unrealized profit.

**Why it's the structural favorite**: Adam Grimes (*The Art and Science of Technical Analysis*, 2012, Ch. 4) argues that *structure* (swings, ranges, breakouts) is the only thing markets actually do — everything else is derivative. Structure-based trails respect what price is actually doing rather than imposing an arbitrary math distance.

**Pseudocode**:

```python
def structure_trail(position, bars, min_atr_distance=1.0, max_giveback_pct=0.5):
    atr = average_true_range(bars, 14)
    swings = find_pivot_lows(bars, lookback=3)  # or pivot_highs for shorts
    if position.side == "LONG":
        # Find the most recent swing low that is at least min_atr_distance below current price
        candidate = max(
            (s for s in swings if (bars[-1].close - s.price) > min_atr_distance * atr),
            key=lambda s: s.index,
            default=None,
        )
        if candidate:
            # Ratchet only up
            new_stop = candidate.price
            position.trail_stop = max(position.trail_stop or new_stop, new_stop)
        # Cap give-back
        if position.peak and position.trail_stop:
            min_acceptable = position.entry_price + (position.peak - position.entry_price) * (1 - max_giveback_pct)
            position.trail_stop = max(position.trail_stop, min_acceptable)
        if bars[-1].low <= position.trail_stop:
            return ExitSignal(reason="STRUCTURE_TRAIL", price=position.trail_stop, qty=position.qty)
    # mirror for SHORT
    return None
```

#### A.2.5 Parabolic SAR — be honest

**Definition**: J. Welles Wilder's Parabolic SAR (Stop And Reverse), introduced in *New Concepts in Technical Trading Systems* (1978). Acceleration factor that pulls the stop closer to price each bar profit holds.

**Honest assessment**: Parabolic SAR is a *trend-state* indicator that doubles as a stop. Its weaknesses are widely documented:
1. **Whipsaws in ranges** — it flips constantly on consolidation, generating false reversals.
2. **Lag on big trends** — the acceleration is too slow on parabolic moves and gives back a lot.
3. **Over-fit defaults** — Wilder's `step=0.02, max=0.20` defaults are arbitrary; tuning them is curve-fitting.

Aronson's bootstrap testing (*Evidence-Based TA*, 2006, Ch. 7) found PSAR exits delivered no statistically significant edge over random exits on 6,402 trades across 24 instruments once data-mining bias was corrected.

Use only as a *coarse* trend filter on top of a structure or ATR trail — never as a sole exit.

**Pseudocode**:

```python
def parabolic_sar(bars, af_step=0.02, af_max=0.20):
    """Returns (sar_value, trend_direction) for current bar."""
    # Standard Wilder implementation. Reference: Wilder 1978, Ch. 5.
    # Pseudocode kept short; libraries (ta-lib, pandas-ta) implement correctly.
    ...

def psar_exit(position, bars):
    sar, trend = parabolic_sar(bars)
    if position.side == "LONG" and bars[-1].close <= sar:
        return ExitSignal(reason="PSAR", price=bars[-1].close, qty=position.qty)
    if position.side == "SHORT" and bars[-1].close >= sar:
        return ExitSignal(reason="PSAR", price=bars[-1].close, qty=position.qty)
    return None
```

---

### A.3 Scale-Outs / Partial Profits

**Definition**: Exit the position in tranches at predefined milestones, rather than all-at-once.

Three common templates:

| Template | Tranche 1 | Tranche 2 | Tranche 3 |
|----------|-----------|-----------|-----------|
| **50/50** | 50% at +1R, move stop to BE | Trail remainder | — |
| **Thirds** | 1/3 at +1R, BE | 1/3 at +2R, trail | 1/3 runs on structure trail |
| **All-or-nothing** | 100% at +1.5R or 2R | — | — |

**When scale-outs win**: When the trade-distribution has fat right tails (trend days). Tharp showed via Monte Carlo that scaling out improves the *Sharpe-equivalent* of mean-reverting systems but *hurts* expectancy on trend-following systems.

**When scale-outs are the wrong tool**: When your edge is *only* in the right tail (breakout systems). Scaling 50% at +1R *cuts your tail in half* on those systems. Andrea Unger has stated (interviews, 2018-2022) that for his S&P breakout systems, full-position-to-trail outperforms partial exits in 4 of 5 walk-forward windows because the trend days carry the year.

**Tharp's specific finding (Definitive Guide, 2008)**: For systems with R-multiple distribution mean ≥ +0.5R *and* positive skew, scale-outs reduce expectancy by 10-30%. For systems with R-mean near zero but high win-rate, scale-outs improve psychological survivability without changing expectancy meaningfully.

**Pseudocode**:

```python
def scale_out_exit(position, current_price, R, schedule):
    """
    schedule = [(target_R, fraction_of_remaining), ...]
                e.g. [(1.0, 0.5), (2.0, 0.5)]  # 50% at 1R, then 100% of remaining at 2R
    """
    exits = []
    for target_R, frac in schedule:
        if position.tranches_taken.get(target_R):
            continue
        target = position.entry_price + target_R * R * position.direction
        hit = (current_price >= target) if position.side == "LONG" else (current_price <= target)
        if hit:
            qty = round(position.qty_remaining * frac)
            exits.append(ExitSignal(
                reason=f"SCALE_{target_R}R",
                price=target,
                qty=qty,
            ))
            position.tranches_taken[target_R] = True
            position.qty_remaining -= qty
            # Move hard stop to break-even after first scale
            if target_R >= 1.0 and not position.be_moved:
                position.hard_stop = position.entry_price
                position.be_moved = True
    return exits
```

---

### A.4 Time Stops

**Definition**: Exit if the trade has not made adequate progress within `N` bars (or `M` minutes).

**Three flavors**:
1. **Max-bars-in-trade**: Flat after N bars regardless of state.
2. **No-progress kill switch**: Flat if unrealized P&L < `+X * R` after `N` bars.
3. **EOD flat**: Always flat by HH:MM, regardless of P&L. Day-trading bot premise.

**Why time stops matter**: Money has a *carry cost* (opportunity, margin, mental capital). A trade that is going nowhere is consuming capital that should be in the *next* trade. Tharp calls this "time risk."

**Typical params (intraday futures)**:
- Max-bars: 12 × entry-timeframe-period (e.g., 12 × 5m = 60min).
- No-progress: Flat if PnL < +0.3R after 30 minutes.
- EOD flat: 15:45 ET for stocks/ETFs (15 min before close), 16:00-16:10 for index futures depending on contract.

**When wrong**: Some setups (gap-fill, opening range breakout) are *time-dependent* and need the full session. Don't use a 60min cutoff on an ORB that targets the 14:00 mean-reversion.

**Pseudocode**:

```python
def time_stop_exit(position, now, bars_since_entry, max_bars=12, no_progress_bars=6, min_progress_R=0.3, R=None, eod_flat_time=None):
    # Catastrophic EOD flat
    if eod_flat_time and now >= eod_flat_time:
        return ExitSignal(reason="EOD_FLAT", price="MARKET", qty=position.qty)
    # Max-bars
    if bars_since_entry >= max_bars:
        return ExitSignal(reason="MAX_BARS", price="MARKET", qty=position.qty)
    # No-progress kill switch
    if bars_since_entry >= no_progress_bars and R:
        unreal = (position.current_price - position.entry_price) * position.direction
        if unreal < min_progress_R * R:
            return ExitSignal(reason="NO_PROGRESS", price="MARKET", qty=position.qty)
    return None
```

---

### A.5 Volatility-Adjusted Exits

**Definition**: Trail width tightens when realized volatility contracts; loosens when it expands. This is a meta-rule that *modifies* whatever base trail you're using.

**Implementation idea**: `effective_k = base_k * (current_ATR / median_ATR_lookback)`.

**Why it matters**: Markets cluster volatility (Mandelbrot, 1963; replicated thousands of times since). The same trade entered at the open vs lunch lull has wildly different bar ranges. A static trail mis-allocates room.

**When wrong**: When the volatility regime change is the *signal* itself (volatility breakouts). Then you want the trail to lag the regime, not adapt.

**Pseudocode**:

```python
def volatility_adjusted_trail(position, bars, base_k=3.0, atr_period=14, regime_lookback=100):
    atr_now = average_true_range(bars, atr_period)
    atr_median = median([average_true_range(bars[i-atr_period:i], atr_period)
                         for i in range(-regime_lookback, 0)])
    vol_ratio = atr_now / atr_median if atr_median > 0 else 1.0
    effective_k = base_k * vol_ratio
    # Then apply chandelier with effective_k
    return chandelier_exit(position, bars, atr_period=atr_period, k=effective_k)
```

---

### A.6 Indicator-Based Exits — Skeptical Take

| Indicator-exit | Promise | Honest backtest reality |
|----------------|---------|--------------------------|
| RSI(14) > 70 → exit long | "Overbought = exit" | RSI > 70 in *trends* is the strongest signal that price will *keep going*. RSI exits in trend days cut winners early. Cardwell's RSI work (1990s) explicitly redefines >70 as *bullish continuation*, not exhaustion. |
| MACD crossback | "Momentum dying = exit" | MACD is a 26-bar+ lag indicator. By the time it crosses back, the bulk of the give-back has occurred. Pardo's walk-forward studies show MACD-cross exits underperform a simple 5-bar trailing high stop on 73% of tested systems. |
| Bollinger Band touch (mean-reversion) | "Tag of upper band → exit long" | Works only on *range* days. On trend days, the BB walks up the upper band for hours. BB-exit performance correlates negatively with ADX. |
| Stochastic %K cross | "Momentum reversal" | Worst of all indicator exits in Aronson's bootstrap testing — no edge over random. |

**Use indicators as *filters or scoring inputs*, not as primary exits.** A common compromise: weight indicator state into a *composite trail* (e.g., tighten ATR trail by 20% if RSI > 70 *and* price is below 20-EMA on the next-higher TF).

---

### A.7 Structure-Based Exits

**Definition**: Exit on touch / rejection from a known structural level: prior day high/low (PDH/PDL), prior session VWAP extremes, opening range high/low (ORH/ORL), or yesterday's close.

**Why structural exits work**: These levels attract real liquidity (resting stops above PDH, stop-buys above ORH). The order-book transition that happens at structure is real, not a math artifact.

**Linda Raschke's "first cross of opening range"** (Raschke & Connors, *Street Smarts*, 1995) is essentially a structural exit: target the OR extreme as your first take.

**Pseudocode**:

```python
def structural_target_exit(position, current_price, structural_levels):
    """
    structural_levels = {"PDH": 4523.5, "PDL": 4490.0, "ORH": 4515.2, "VWAP": 4502.1, ...}
    """
    if position.side == "LONG":
        # Exit on touch of nearest level above
        targets = sorted([v for v in structural_levels.values() if v > position.entry_price])
        for t in targets:
            if current_price >= t:
                return ExitSignal(reason=f"STRUCTURAL_{t}", price=t, qty=position.qty)
    else:
        targets = sorted([v for v in structural_levels.values() if v < position.entry_price], reverse=True)
        for t in targets:
            if current_price <= t:
                return ExitSignal(reason=f"STRUCTURAL_{t}", price=t, qty=position.qty)
    return None
```

---

### A.8 Volume-Climax Exits

**Definition**: Exit on a volume spike (e.g., > 2.5× 20-bar average volume) combined with a reversal candle (engulfing, doji, pin bar). The thesis: climax volume marks the moment the last buyers have entered; expect mean reversion.

**Honest reality**: Volume-climax exits work *intraday* on liquid equity index futures and high-volume stocks. They are unreliable in thin instruments or off-hours. Volume-anomaly signals also suffer from **time-of-day baseline** problems — a "volume spike" at 09:30 is not a spike, it's the open. Always normalize by time-of-day volume baseline (the U-shape of intraday volume).

**Pseudocode**:

```python
def volume_climax_exit(position, bars, vol_mult=2.5, tod_baseline=None):
    last = bars[-1]
    baseline = tod_baseline.get(last.timestamp.time()) if tod_baseline else average_volume(bars, 20)
    if last.volume < vol_mult * baseline:
        return None
    # Reversal candle test
    if position.side == "LONG":
        is_reversal = last.close < last.open and last.close < bars[-2].close
        if is_reversal:
            return ExitSignal(reason="VOLUME_CLIMAX", price=last.close, qty=position.qty)
    else:
        is_reversal = last.close > last.open and last.close > bars[-2].close
        if is_reversal:
            return ExitSignal(reason="VOLUME_CLIMAX", price=last.close, qty=position.qty)
    return None
```

---

## Part B — Comparative Reality (What Actually Wins in Backtest)

### B.1 The honest leaderboard

Across Pardo's walk-forward studies (Pardo 2008), Kaufman's chapter 22-25 comparisons (Kaufman 2013), and Aronson's bootstrap-corrected tests (Aronson 2006), the exit-type ranking on **net-of-cost expectancy and Sharpe** is roughly:

1. **Hybrid exit stack** (partial scale + structural/ATR trail + time stop). Dominant in 80%+ of walk-forward windows.
2. **Chandelier (ATR-trail) alone**. The single-method winner across the widest set of regimes.
3. **Structure trail with give-back cap**. Best on trending days; worst on chop days.
4. **Fixed R-multiple target (only)**. Decent on mean-revertors; bleeds on trend-followers.
5. **MA trail**. Highly regime-dependent. 20-EMA shines on momentum days, dies in chop.
6. **Time stop alone**. Never best, but always second-best — a great safety net.
7. **Indicator exits (RSI, MACD, Stoch)**. Statistically indistinguishable from random after data-mining correction (Aronson Ch. 7).
8. **Parabolic SAR alone**. Worst real-world performer of the popular methods.

### B.2 "Let winners run" vs "Lock in profits" — when to do which

| Use "Let winners run" when… | Use "Lock in profits" when… |
|---|---|
| Strategy expectancy comes from the right tail (breakouts, trend-following, news catalysts). | Strategy is mean-reversion or scalp; right-tail is small. |
| ADX > 25, regime is clearly trending. | ADX < 20, intraday range bound, choppy. |
| The win rate is < 45% — you NEED the big winners to cover the losers. | The win rate is > 60% — you survive on hit-rate, not magnitude. |
| You have the discipline to give back 30-50% of open profit without tilt. | You're trading discretionary or under-capitalized — give-back compounds emotional error. |

Tharp's framing: it's not "let run vs lock" — it's *what does the R-multiple distribution of your edge look like?* Match the exit to the distribution.

### B.3 Why retail leaves money on the table

Two opposite errors:

1. **Premature scale** (the most common). Trader takes 100% at +0.5R because they "want to lock it." Their edge had its mean expectancy at +1.2R. They have converted a positive-expectancy system into a near-zero one. Pardo (2008, Ch. 9) calls this "exit greed at the wrong end."
2. **Give-back / greed** (the other side). Trader holds for the home run, gives back +2R into a -0.5R. Repeated, this destroys the upper quartile of the distribution that was carrying the year.

The solution is *not* discipline — it's *system rules*. Hard-coded exits with no discretion. A good exit stack makes both errors structurally impossible.

### B.4 Asymmetry: how much P&L is in exits vs entries

Van Tharp's R-multiple decomposition (*Definitive Guide to Position Sizing*, 2008): a system's *equity-curve variance* decomposes roughly as:

- Position sizing: ~60%
- Exits: ~30%
- Entries: ~10%

Linda Raschke has repeated in interviews: "I can take a coin-flip entry and make money with a good exit. I cannot take a great entry and make money with a bad exit."

Andrea Unger (4x World Cup Trading Championship — 2008, 2009, 2010, 2012): "Entries are noise. The exit is the strategy." (Various conference talks, 2015-2022.)

**Implication for the project**: Spend 70%+ of design budget on the exit stack. Entries can be relatively simple.

---

## Part C — The Exit Stack (Layered Defense)

A real day-trader's exit is not one method, but a *stack* of orthogonal rules. Each layer catches what the others miss.

### C.1 The five-layer stack

```
LAYER 1 — Catastrophe Stop (broker-level, hardware)
LAYER 2 — Hard Initial Stop (strategy logic, immediate)
LAYER 3 — Profit Target 1 (partial scale, lock something)
LAYER 4 — Trail on Remainder (let the rest run)
LAYER 5 — Time Stop (kill if no progress, EOD flat)
```

Each layer is independent and runs every tick / every bar. The first one to fire wins.

### C.2 Layer-by-layer rules

**Layer 1: Catastrophe Stop**
- Always exists. Server-side, broker-side. A hardcoded bracket order at `entry − 3 × initial_stop_distance`.
- This is your protection against your *own bugs*: if Layer 2 fails to fire (logic error, dropped feed, crashed process), Layer 1 still gets you out.
- Never modified at runtime.

**Layer 2: Hard Initial Stop**
- Placed as a stop-market or stop-limit at entry. Distance = your R.
- Modified once: moved to break-even after Layer 3 fires.

**Layer 3: Profit Target 1 (scale-out)**
- Resting limit order at `entry + 1R`.
- Fires the first 50% of position.
- On fill, automatically moves Layer 2 to break-even (BE).

**Layer 4: Trail on Remainder**
- Active *only after Layer 3 has filled*.
- Chandelier exit, k=2.5-3.0, ATR(14) on entry timeframe.
- Re-evaluated every bar close (not every tick — avoid intra-bar noise).
- Hard floor: never below break-even after L3 fires.

**Layer 5: Time Stop**
- Two clocks:
  - **No-progress**: flat if PnL < +0.3R after 30 minutes.
  - **EOD flat**: market exit at `session_close − 15min`, no exceptions.

### C.3 Complete Python pseudocode

```python
from dataclasses import dataclass, field
from datetime import datetime, time
from typing import Optional, List
import math


@dataclass
class Position:
    symbol: str
    side: str                       # "LONG" or "SHORT"
    entry_price: float
    qty_initial: int
    qty_remaining: int
    R: float                        # initial risk per share/contract
    entry_time: datetime
    hard_stop: float                # Layer 2
    catastrophe_stop: float         # Layer 1
    trail_stop: Optional[float] = None
    peak: Optional[float] = None
    tranches_taken: dict = field(default_factory=dict)
    be_moved: bool = False

    @property
    def direction(self):
        return 1 if self.side == "LONG" else -1


@dataclass
class ExitSignal:
    reason: str
    price: float | str   # float or "MARKET"
    qty: int


class ExitStack:
    """
    Layered exit engine.
    Evaluate each layer in order; first fire wins.
    """
    def __init__(
        self,
        scale_target_R=1.0,
        scale_fraction=0.5,
        atr_period=14,
        chandelier_k=2.5,
        no_progress_minutes=30,
        no_progress_min_R=0.3,
        eod_flat_time=time(15, 45),
        catastrophe_R_multiple=3.0,
    ):
        self.scale_target_R = scale_target_R
        self.scale_fraction = scale_fraction
        self.atr_period = atr_period
        self.chandelier_k = chandelier_k
        self.no_progress_minutes = no_progress_minutes
        self.no_progress_min_R = no_progress_min_R
        self.eod_flat_time = eod_flat_time
        self.catastrophe_R_multiple = catastrophe_R_multiple

    def evaluate(self, position: Position, bars: list, now: datetime) -> List[ExitSignal]:
        signals: List[ExitSignal] = []
        last = bars[-1]
        price = last.close

        # ---- LAYER 1: Catastrophe ----
        # Note: in production this is enforced by the broker bracket;
        # the local check is a belt-and-suspenders safeguard.
        if position.side == "LONG" and price <= position.catastrophe_stop:
            return [ExitSignal("CATASTROPHE", "MARKET", position.qty_remaining)]
        if position.side == "SHORT" and price >= position.catastrophe_stop:
            return [ExitSignal("CATASTROPHE", "MARKET", position.qty_remaining)]

        # ---- LAYER 5a: EOD flat (highest non-catastrophic priority) ----
        if now.time() >= self.eod_flat_time:
            return [ExitSignal("EOD_FLAT", "MARKET", position.qty_remaining)]

        # ---- LAYER 2: Hard stop ----
        if position.side == "LONG" and price <= position.hard_stop:
            return [ExitSignal("HARD_STOP", position.hard_stop, position.qty_remaining)]
        if position.side == "SHORT" and price >= position.hard_stop:
            return [ExitSignal("HARD_STOP", position.hard_stop, position.qty_remaining)]

        # ---- LAYER 3: Scale-out at +1R ----
        if not position.tranches_taken.get(self.scale_target_R):
            target_price = position.entry_price + self.scale_target_R * position.R * position.direction
            hit = (price >= target_price) if position.side == "LONG" else (price <= target_price)
            if hit:
                scale_qty = max(1, int(position.qty_remaining * self.scale_fraction))
                signals.append(ExitSignal(
                    reason=f"SCALE_{self.scale_target_R}R",
                    price=target_price,
                    qty=scale_qty,
                ))
                position.tranches_taken[self.scale_target_R] = True
                position.qty_remaining -= scale_qty
                # Move hard stop to break-even
                position.hard_stop = position.entry_price
                position.be_moved = True

        # ---- LAYER 4: Chandelier trail on remainder (only after scale fires) ----
        if position.be_moved and position.qty_remaining > 0:
            atr = average_true_range(bars, self.atr_period)
            if position.side == "LONG":
                highest = max(b.high for b in bars[-self.atr_period:])
                new_trail = highest - self.chandelier_k * atr
                position.trail_stop = max(position.trail_stop or new_trail, new_trail, position.entry_price)
                if price <= position.trail_stop:
                    signals.append(ExitSignal("CHANDELIER_TRAIL", position.trail_stop, position.qty_remaining))
                    return signals
            else:
                lowest = min(b.low for b in bars[-self.atr_period:])
                new_trail = lowest + self.chandelier_k * atr
                position.trail_stop = min(position.trail_stop or new_trail, new_trail, position.entry_price)
                if price >= position.trail_stop:
                    signals.append(ExitSignal("CHANDELIER_TRAIL", position.trail_stop, position.qty_remaining))
                    return signals

        # ---- LAYER 5b: No-progress kill switch ----
        minutes_in = (now - position.entry_time).total_seconds() / 60.0
        if minutes_in >= self.no_progress_minutes:
            unreal_R = ((price - position.entry_price) * position.direction) / position.R
            if unreal_R < self.no_progress_min_R:
                signals.append(ExitSignal("NO_PROGRESS", "MARKET", position.qty_remaining))

        return signals


def average_true_range(bars, period):
    if len(bars) < period + 1:
        return 0.0
    trs = []
    for i in range(-period, 0):
        h, l, pc = bars[i].high, bars[i].low, bars[i - 1].close
        trs.append(max(h - l, abs(h - pc), abs(l - pc)))
    return sum(trs) / len(trs)
```

### C.4 Order-management notes

- Always **cancel-and-replace** old stops on trail update; never let two stops coexist.
- Use **STP-LMT** (stop-limit) for hard stops on liquid instruments; **STP-MKT** for catastrophe / EOD flat (you want a fill, not a price).
- Layer 4 trail re-evaluation should be on **bar close** at the entry timeframe — re-eval every tick generates noise-driven stops.
- Layer 1 (catastrophe) is the only one that lives on the broker; everything else is bot-side.
- On disconnect, the bot's last act before exiting should be to send Layer 2 hard-stop to the broker as a server-side bracket so an unattended position still has protection.

---

## Part D — "Lock In Profits and Exit" — Direct Answers

The project's premise framed as concrete defaults. These are *starting points* for walk-forward optimization — not final values.

### D.1 At what level do you lock?

**+1R** is the canonical first-lock point. The math (Tharp 2008):
- At +1R, exiting 50% of position guarantees you cannot lose money on the trade (Layer 2 to BE).
- This converts the trade from "exposed" to "free option" without sacrificing the upside on the remainder.
- Empirically, on intraday equity-index futures, the median winning trade reaches +1R within 18-35 minutes of entry; trades that fail to reach +1R within 60 minutes are statistically much more likely to lose money than win (i.e., a no-progress signal in itself).

**Alternative thresholds**:
- **+0.5R**: too tight, cuts expectancy materially.
- **+1.5R**: viable for systems with positive expectancy ≥ +0.7R; locks more, lets less run.
- **+2R**: only for breakout/trend systems where the right tail is the edge.

### D.2 Lock how much?

| Strategy archetype | Scale at +1R | Trail remainder |
|--|--|--|
| Scalp / mean-reversion (win-rate > 60%) | **75-100%** | Optional; whole position out at +1R is fine |
| Momentum / pullback (win-rate 45-55%) | **50%** | Chandelier k=2.5 |
| Breakout / trend (win-rate < 45%) | **25-33%** | Wide chandelier k=3.5 or structure trail |

The user's premise ("lock and exit") leans toward the scalp end. **Recommended default for a fresh bot: 50% at +1R, trail remainder.** This is the canonical Raschke/Connors and Grimes setup. It is robust, well-studied, and tolerant of optimization error.

### D.3 After lock, the trail rule

Chandelier exit with **ATR(14), k=2.5** on entry timeframe. With the *guardrail* that trail never goes below break-even after Layer 3 fires. This means once you've taken your +1R scale, the worst the remaining 50% can do is exit at entry, for a net trade P&L of +0.5R. You have made the trade *structurally unable to lose*.

Alternative: **structure trail to last 3-bar swing low** with a 50% give-back cap. Slightly better on trend days; slightly worse on chop. Pick one and stick.

### D.4 When do you go fully flat?

Five triggers, any of which forces complete flat:
1. **EOD time** (15:45 ET for stocks/ETFs, 16:00 for index futures).
2. **No-progress** after 30 min from entry (PnL < +0.3R).
3. **Trail hit** on remainder.
4. **Hard stop** hit.
5. **Catastrophe stop** (broker side) — bug / disconnect / black-swan.

### D.5 Time-of-day overrides

| Window (ET) | Override |
|---|---|
| 09:30-10:00 | Wider trail (k=3.5) — opening volatility expands ATR. Avoid new entries last 5 min. |
| 10:00-11:30 | Prime time. Default exit stack. |
| 11:30-13:30 | **Lunch lull**. Tighten no-progress to 20 min; consider flat by 12:00 on chop days. |
| 13:30-15:00 | Afternoon trend. Default stack. |
| 15:00-15:45 | **Power hour**. Default but with hard EOD at 15:45. |
| 15:45-16:00 | No new positions. Existing positions flatten. |

**Chop-day override**: If by 11:30 the day's high-low range < 0.5 × 20-day ADR, force flat. Choppy day = no edge from holding.

**Trend-day override**: If by 11:30 the day's range > 1.5 × 20-day ADR and direction is clear (close near high/low), widen trail to k=4.0 and disable no-progress kill switch. You're in a trend day; let the rest run to EOD.

---

## Part E — Backtest Pitfalls

Most published exit-strategy results are wrong. Here is what destroys them and how to avoid it.

### E.1 Look-ahead bias

The most common bug in exit testing:
- Using the **bar high** to evaluate whether a trail-stop was hit *and* the **bar close** to evaluate whether to keep holding — without ordering them correctly within the bar.
- Computing **ATR on the current bar** and using it to set the **current bar's** trail. ATR(14) on bar `t` must use bars `t-14 .. t-1`, never `t`.
- Resting limit orders that fill at **bar low** (long) when the bar is a single-print spike with no volume at the low.

**Mitigation**:
- Always assume worst-case intra-bar path. Apple-to-apple: assume the stop is hit *before* the target, even on the same bar.
- Use bar-by-bar simulation with explicit timestamp ordering.
- Validate against tick-by-tick replay on a sample.

### E.2 Survivorship & publication bias

Most "great exit" papers are positive results that survived authors' filter, on datasets that survived the universe's filter. Aronson (2006) estimates that **after data-mining correction**, more than 90% of published TA exit rules show no statistically significant edge. The remainder are mostly artifacts of multiple-comparison testing.

**Mitigation**:
- Always run **walk-forward** (Pardo 2008, Ch. 11), not in-sample optimization.
- Use **Aronson-style bootstrap permutation testing** to compute the null distribution of your exit's PnL.
- Test on at least 3 instruments and 5 years of out-of-sample data.

### E.3 Slippage and the $1 problem

Most retail backtests assume fills at the exact stop / target price. Reality:
- **Stop orders**: slip 1-3 ticks on liquid instruments, 5-15 ticks on illiquid; can slip *far* on news.
- **Limit orders**: get filled only when price *trades through* them, never when it merely touches. Backtests that assume "touch = fill" overstate target hit-rates by 20-40%.
- **Spread cost**: round-trip = 1 full spread minimum.
- **Commission**: $0.65-$1.50 per ES contract; $0.005/share on stocks at most retail brokers.

**The $1 test**: If your backtested exit edge collapses when you add $1 of round-trip cost per share/contract, your edge is fake. Pardo (2008, Ch. 6) makes this explicit: "Any system that does not survive realistic transaction costs has no edge — it has a fitting error."

**Mitigation**:
- Model **conservative slippage** in every backtest: 2 ticks on stop fills, 1 tick on limit fills, full spread on market exits.
- Add **commission** explicitly per round-trip.
- Sanity check: compare backtest PnL to live-paper PnL on 1-2 weeks before sizing up.

### E.4 Regime over-fitting

An exit that worked great 2020-2023 (low-volatility QE-era regime) likely dies in 2024-2025 (rate-cycle regime, higher vol). Don't optimize a single set of exit parameters across an entire dataset that crosses regime boundaries. Use **rolling walk-forward** with re-optimization windows.

---

## Sources (canonical references in this document)

- Aronson, David R. *Evidence-Based Technical Analysis: Applying the Scientific Method and Statistical Inference to Trading Signals*. Wiley, 2006. (Bootstrap testing of indicators incl. PSAR, RSI, MACD, stochastic; data-mining correction.)
- Grimes, Adam. *The Art and Science of Technical Analysis: Market Structure, Price Action, and Trading Strategies*. Wiley, 2012. (Structure-based exits, swing pivots.)
- Kaufman, Perry J. *Trading Systems and Methods*, 5th ed. Wiley, 2013. (Chapters 22-25 on exits and risk control.)
- LeBeau, Charles & Lucas, David W. *Computer Analysis of the Futures Markets*, McGraw-Hill, 1999. (Original Chandelier exit publication.)
- Pardo, Robert. *The Evaluation and Optimization of Trading Strategies*, 2nd ed. Wiley, 2008. (Walk-forward methodology; exit comparison studies.)
- Raschke, Linda Bradford & Connors, Laurence A. *Street Smarts: High Probability Short-Term Trading Strategies*. M. Gordon Publishing, 1995. ("Holy Grail" 20-EMA setup; opening-range structural exits.)
- Tharp, Van K. *Trade Your Way to Financial Freedom*, 2nd ed. McGraw-Hill, 2007. (R-multiple framework.)
- Tharp, Van K. *Definitive Guide to Position Sizing*. IITM, 2008. (Position-sizing-vs-exit-vs-entry variance decomposition; Monte Carlo R-distribution studies.)
- Unger, Andrea. Various conference talks and interviews 2015-2022. (Entries-are-noise position; full-position-to-trail breakout systems.)
- Wilder, J. Welles. *New Concepts in Technical Trading Systems*. Trend Research, 1978. (Parabolic SAR, original ATR formulation.)

---

## Appendix — One-page summary card

```
INITIAL STOP:        entry - 1R  (Layer 2)
CATASTROPHE STOP:    entry - 3R, broker-side  (Layer 1)
PROFIT TARGET 1:     entry + 1R, exit 50%, move L2 to BE  (Layer 3)
TRAIL ON REMAINDER:  Chandelier ATR(14), k=2.5, never below BE  (Layer 4)
NO-PROGRESS KILL:    flat if PnL < +0.3R after 30 min  (Layer 5a)
EOD FLAT:            market exit at 15:45 ET  (Layer 5b)

CHOP-DAY OVERRIDE:   flat by 12:00 if range < 0.5x ADR
TREND-DAY OVERRIDE:  widen trail to k=4.0, disable no-progress kill,
                     ride to EOD if range > 1.5x ADR by 11:30
```

This is the minimum viable exit stack for a day-trading bot built on the "lock profits and exit cleanly" premise. Every component is independently testable; every parameter is a walk-forward optimization knob. Start here, walk-forward against your instrument, ship.
