# Candlesticks and Price Action — Professional Intraday Curriculum

**Audience:** experienced trader, ~15yr base, prediction-market quant background. Assumes you know what OHLC, ATR, ADX, VWAP, order flow, and standard deviation mean. No retail filler. The goal is to put you at the level where you can read a 5-minute ES or NQ chart the way a desk trader at SMB or DRW reads it: as a sequence of auction prints, not as a "pattern gallery."

**Bottom-line thesis (Grimes / Brooks / Steenbarger consensus):** Candlestick patterns in isolation have **no robust statistical edge**. They are conditional information — useful only when paired with (a) market structure, (b) location (S/R, VWAP, prior day levels), (c) regime (trend vs balance), and (d) execution discipline. The single biggest mistake the retail world makes is trading the pattern; pros trade the **context**, and the candle is just the trigger.

> "If you test candlestick patterns in isolation, you'll find there's no statistical edge. The edge is conditional — and quantifying the context is non-negotiable." — paraphrasing Adam Grimes, *The Art and Science of Technical Analysis* (Wiley 2012).

---

## PART A — Candlestick Patterns That Actually Matter

For each pattern below I give: visual definition, where it works, where it fails (the trap mechanic), data where it exists, and the noise filter pros actually use.

### A.1 Pin Bar / Hammer / Shooting Star

**Visual.** Single bar; body ≤ 1/3 of the total range; long wick on one side (≥ 2× body); short or absent wick on the other. Hammer = long lower wick, close in upper third, at a swing low. Shooting star = mirror image at a swing high. Color of the body matters less than location of the close within the range.

**Where it works.**
- At a tested level (prior day high/low, overnight high/low, VWAP, key swing pivot, round number, opening range edge).
- After an extended move, not in the middle of balance. Brooks calls these "exhaustion bars"; they only mean something when there is something to exhaust.
- On higher-volume timeframes intraday (5m, 15m on ES/NQ). On the 1m the noise drowns the signal.
- When the bar's range is meaningfully above average (≥ 1.5× ATR(14) of that timeframe — Grimes' rough rule).

**Where it fails (trap mechanic).**
- Mid-range, no level: it's noise. You're pattern-matching on random walks.
- Inside a strong trend with parabolic acceleration: a hammer mid-flag is often a continuation pause, not a reversal. People short shooting stars in trend days and get run over.
- Tiny body / tiny range hammers in chop: the bar simply prints because volatility collapsed for two minutes.
- News bars: the wick is reflex liquidity, not exhaustion. Algos faded and refilled the same second.

**Data.** Bulkowski's *Encyclopedia of Candlestick Charts* puts the hammer at a 60% bullish-reversal rate (rank 26/103 for reversal) but only 65/103 on **overall performance** — meaning even when it reverses, follow-through is weak. White-bodied hammers and hammers within the lower third of the yearly range outperform. ([thepatternsite.com](https://thepatternsite.com/Hammer.html))

**Noise filter pros use.**
1. Must be **at a level** marked before the bar prints (prior-day H/L, overnight H/L, VWAP ±1σ, opening range edge, weekly pivot).
2. Bar range ≥ 1.5× ATR of that timeframe.
3. Close must be in the upper (lower) 25% of the bar's range, not just upper third.
4. **Failure of the next bar to break the wick** is the actual confirmation. Brooks teaches "second-entry" — the second attempt at reversal is statistically stronger than the first because it has more committed participants.

---

### A.2 Engulfing (Bullish / Bearish)

**Visual.** Two-bar pattern. Bar 2's body fully engulfs bar 1's body (wicks don't have to be engulfed in the strict Nison definition; pros usually require body-engulf only). Bullish: down bar followed by larger up bar closing above bar 1's open. Bearish: mirror.

**Where it works.**
- At extension into a level. A bearish engulfing at prior-day high after a multi-hour drive is a real signal.
- When bar 2 closes near its extreme (no upper wick on bullish engulf).
- When bar 2's range >> ATR (it's a displacement bar in SMC language).

**Where it fails.**
- Inside trading ranges: engulfing bars print constantly in balance and mean nothing. This is where retail bloggers' "70% win rate" claims fall apart.
- Low-volume engulfings (e.g., into lunch): no participation, no follow-through.
- Engulfing on the open of a fresh session when prior bar was a doji: you're just measuring overnight gap, not intent.

**Data.** Bulkowski: bullish engulfing reverses 63% (rank 22/103 reversal) but overall performance rank 84/103 — translation, the reversal happens but follow-through is poor. Bearish engulfing reverses 79% (rank 5/103) but ranks 91 on continuation — same story: the signal fires, the move is shallow. ([Bull Engulfing](https://thepatternsite.com/BullEngulfing.html), [Bear Engulfing](https://thepatternsite.com/BearEngulfing.html))

**Noise filter.**
- Require engulfing at a marked level + bar 2 range ≥ 1.5× ATR.
- Use as a **trigger after a failure test**, not as a standalone setup. The engulfing at the failed-breakout level is the textbook Brooks "second-attempt reversal."
- Combine with delta divergence on order-flow software (Bookmap, Sierra, ATAS) if available — engulfing with negative delta on a down bar at resistance is a much stronger short trigger.

---

### A.3 Inside Bar

**Visual.** Bar 2's high ≤ bar 1's high AND bar 2's low ≥ bar 1's low. Compression. Brooks: "An inside bar is a one-bar trading range."

**Where it works.**
- After a strong trend leg as a flag (continuation). Inside bar at a moving average or after a 1- to 3-bar pause = trade in the direction of trend on break of the inside bar's extreme.
- At a key level as compression before a decision. Multiple consecutive inside bars (ii, iii patterns) are pressure-cooker setups beloved by Brooks.
- On higher TF (60m, daily) inside bars carry more weight; they imply a meaningful auction pause.

**Where it fails.**
- In chop. An inside bar in a 6-bar range is just random.
- Inside bars after a climactic bar (huge ATR bar): the next move is often two-sided, not directional.
- Around economic releases: inside bar before NFP is just pre-print compression, not a signal.
- "Inside bar breakout" trades on the 1m without trend context are coin flips.

**Data.** No clean academic win rate (Bulkowski's encyclopedia treats this under "harami" and similar). What's reproducible: inside-bar breaks **in the direction of the higher-TF trend** at a marked level have positive expectancy in most futures studies; counter-trend inside-bar breaks do not.

**Noise filter.**
- Trade only with HTF trend.
- Filter by location (must be at flag, pullback, or level).
- Brooks rule: if the bar before the inside bar is a strong trend bar (close in the top/bottom 20% of its range, ≥ 1× ATR), the inside bar break in the same direction is high-probability.

---

### A.4 Outside Bar

**Visual.** Bar 2's high > bar 1's high AND bar 2's low < bar 1's low. Two-bar volatility expansion.

**Where it works.**
- At the end of a move (reversal outside bar) when bar 2 closes in the opposite direction with strong range. This is essentially a one-bar failure test.
- As a "BAB" (breakout-and-back) when it sweeps a level and closes back inside.

**Where it fails.**
- Middle of trend: an outside bar mid-trend usually means a stop-run that resumes the trend after one or two bars. Fading it counter-trend is a classic noob mistake.
- News bars: the outside bar around CPI/FOMC is reflex; the true direction shows up 10–20 minutes later.
- Outside bars where the close is mid-range: indecision, not a trade.

**Filter.** Close must be in the upper or lower 25% AND at a level AND ideally on volume expansion. Without those three, ignore it.

---

### A.5 Doji Types (Gravestone, Dragonfly, Long-Legged)

**Visual.** Open ≈ close. Gravestone = long upper wick (sellers absorbed buyers). Dragonfly = long lower wick (mirror). Long-legged = wicks on both sides, body in the middle (full indecision).

**Where it works.**
- At extension into a level: a gravestone doji at prior-day high after a 20-handle ES drive is a real exhaustion print.
- Dragonfly at VWAP support in an uptrend during pullback = institutional accumulation tell.
- After multiple trend bars in a row, a doji often marks the first sign of trend weakening.

**Where it fails.**
- Mid-range: doji print constantly in chop. Trading them is essentially trading the randomness of the timeframe.
- Lunch dojis (11:45 ET – 13:30 ET): low volume, low information.
- Crypto / 24h markets: dojis on the 5m print every hour. Use 15m+ for meaningful dojis in 24h products.

**Data.** Bulkowski: dojis as a class are mediocre. The **gravestone at a top** and **dragonfly at a bottom**, with location filter, are the only two doji setups worth trading at the intraday timeframe.

**Filter.** Range ≥ 1× ATR + at a level + next-bar confirmation (a close in the direction of the doji's wick = confirmation).

---

### A.6 Morning Star / Evening Star

**Visual.** Three bars. Morning star = down bar, small-body bar (often doji) with gap or near-gap, then strong up bar closing into the body of bar 1. Evening star = mirror.

**Where it works.**
- Daily and 60m timeframes, especially at multi-day swing lows/highs.
- After capitulation / climax bars when the small middle body indicates exhaustion.

**Where it fails.**
- Intraday 5m: rarely meaningful unless at a major level. The "gap" requirement is essentially absent in continuous futures.
- Without volume confirmation on bar 3.

**Data.** Bulkowski rates **evening star at rank 4/103** for reversal performance (72% reversal). Morning star is solid but lower-ranked. ([CandlePerformers](https://www.thepatternsite.com/CandlePerformers.html)) These rankings are based on daily charts; the intraday equivalent is weaker because gap definition breaks down.

---

### A.7 Marubozu

**Visual.** Body = essentially the whole range. No wicks (or tiny wicks). Pure one-sided auction.

**Where it works.**
- As a **trend bar** in Brooks' terminology — it's the cleanest expression of imbalance.
- A marubozu at a level break is the textbook displacement candle (SMC term: displacement; Brooks term: strong trend bar; institutional term: aggressive print).
- Best traded as a continuation signal on the pullback to its 50% level, NOT as an entry on its close (chasing).

**Where it fails.**
- Chasing it at the close: by then the move is largely complete on that timeframe. Wait for the retracement.
- Marubozu into a major level: the level is likely to hold, and the bar is exhausting into resistance.

**Filter.** Look at the **next 1–3 bars**. If they hold above the marubozu's 50% (or 75%), trend continues. If they immediately erase it, you have a failure test setup in the opposite direction.

---

### A.8 Harami (Bullish / Bearish)

**Visual.** Reverse of engulfing. Bar 1 is large; bar 2's body is contained inside bar 1's body. Volatility contraction after a trend bar.

**Where it works.**
- Similar to inside bar — flag pattern after a trend bar, continuation in trend direction on break.
- After a climax bar at a level: harami can mark trend exhaustion.

**Where it fails.**
- As a standalone reversal signal in isolation. Bulkowski's data shows haramis are weak reversal patterns overall.

**Filter.** Treat harami the same as inside bar — direction comes from the break, not the pattern itself.

---

### A.9 Tweezer Top / Tweezer Bottom

**Visual.** Two consecutive bars with matching highs (tweezer top) or matching lows (tweezer bottom). Often with opposite colors.

**Where it works.**
- At a key level when the tweezer reflects double-rejection. Equal highs/lows at resistance with rejection wicks = liquidity pool above + failure = real signal.
- Higher TF: daily tweezers at multi-week levels are meaningful.

**Where it fails.**
- Mid-range or on small bars: just noise.
- Without a level: tweezers form constantly in trading ranges and mean nothing.

**Connection.** This is the candlestick expression of "equal highs / equal lows" that SMC calls a liquidity pool. Don't trade the tweezer in isolation — trade the sweep through the equal level and the failure back inside (covered in B.5).

---

### A.10 Patterns to Skip (retail filler that doesn't backtest cleanly)

- **Three white soldiers / three black crows** as standalone signals: Bulkowski ranks three black crows well, but in practice the move is often complete by the time the third bar prints. You're entering at the worst price.
- **Hanging man** (same shape as hammer but at top): poor empirical performance, easily confused with normal pullback bars.
- **Three inside up/down, three outside up/down**: rare; their high "win rates" are sample-size artifacts.
- **Spinning top, "rickshaw man," dragonfly cross**, and the rest of the Steve Nison long tail: more lore than edge.
- **Abandoned baby** (true gap-isolated reversal candle): real on daily charts, doesn't exist intraday on futures since gaps don't.

---

## PART B — Price Action Principles

### B.1 Market Structure — HH/HL vs LH/LL

The cleanest, oldest, still-best framework. Dow Theory updated for intraday.

- **Uptrend:** sequence of higher highs (HH) and higher lows (HL).
- **Downtrend:** lower highs (LH) and lower lows (LL).
- **Regime change:** a higher-timeframe HL is broken (uptrend → at risk); a LH is broken (downtrend → at risk). Confirmation arrives when the next swing makes a LL (downtrend confirmed) or HH (uptrend confirmed).

**How pros use it:**
- Mark swing highs/lows on the 60m or 15m for intraday context (bias).
- Trade in the direction of the most recent HTF structure shift until it's invalidated.
- Brooks' refinement: trends rarely give clean HH/HL; expect "always-in long" or "always-in short" regimes — meaning a hypothetical observer asked right now would be long or short. The flip happens on a strong trend bar in the opposite direction that breaks recent structure (a Break of Structure, BoS, in SMC vocabulary).

### B.2 Swing Highs and Lows — How Pros Mark Them

Retail uses 3-bar fractal (Williams): high bar with two lower-high bars on each side. That's fine for noise, terrible for actionable levels.

**Pro method:**
- **N-bar fractal** with N adapted to timeframe. On 5m ES: 5–7 bar fractal. On 15m: 3–5. On 1m: 9–15 (filter the noise).
- **Swing weight:** mark only the swings that **caused** a meaningful move or break of prior structure. A 3-tick wiggle that meets the fractal definition is not a tradeable swing.
- **Confluence:** the swings that matter most are those that coincide with VWAP touches, prior session levels, or visible volume nodes (HVNs from Volume Profile / TPO).
- Steenbarger's point: pattern recognition improves with **deliberate annotation** — pros mark swings the same way every day on the same timeframes, building an internal database. Most retail traders mark inconsistently and never develop the eye.

### B.3 Trend Lines

**Retail draws them wrong because they:**
- Connect any two random points and call it a trend line.
- Fit lines after the fact ("look, it broke!" — yes, because you drew it after).
- Use closes when wicks matter, or vice versa, with no rule.

**Brooks-style pro rules:**
- A trend line requires **at least three touches** to be tradeable, and the **second and third touches** are the entries — the line is born only after the third touch confirms it.
- Use **bodies (closes)** for trend line breaks on equities/futures cash sessions; use **wicks** on 24h products (futures overnight, crypto, FX).
- A "micro trend line" (Brooks term) drawn across the highs of a short pullback in a downtrend, broken upward, is one of the best 1–2 R counter-trend scalps — but **only if the larger trend is intact**.
- Trend channel lines (parallel to the trend line on the other side) define overextension. Two closes outside the channel line = high-probability mean reversion to the median.

### B.4 Breakouts vs Fakeouts — the Retest Rule

The single most important intraday concept after market structure.

**What makes a breakout valid:**
1. **Volume expansion** on the breakout bar (≥ 1.5–2× recent average volume on that timeframe).
2. **Close beyond the level**, not just a wick. Wick-only breaks are sweeps, not breakouts (see B.5).
3. **Follow-through bar** in the same direction within 1–3 bars.
4. **Successful retest**: price pulls back to the broken level and **holds** (close above prior resistance / below prior support). Pros usually wait for this retest — they sacrifice some R for confirmation.

**The "failure test" (Grimes / Sperandeo "2B" / Wyckoff "spring" or "upthrust"):**
- Price trades **beyond** a level and **fails back through it on the same bar or within 1–2 bars**.
- The trade is short the failed-up breakout, long the failed-down breakout.
- Best signal: bar range ≥ 1.5× ATR, close back beyond the level on the same bar. Stop just past the failed extreme.
- This is the **single most repeatable intraday setup** across futures, equities, and FX. ([Adam Grimes — Failure Test](https://www.adamhgrimes.com/failure-test-2/))

**Why retail loses on breakouts:**
- They buy the first close above resistance with no volume confirmation.
- They don't wait for retest — every level worth breaking is worth retesting in the next 30–60 minutes.
- They don't know whether they're in a trend day (most breakouts hold) or a balance day (most breakouts fail). On balance days, expect ~70% of breakouts to fail; on trend days, expect ~70% to hold. The regime call is more valuable than the pattern.

### B.5 Liquidity Concepts (SMC-flavored, without the cult)

The honest version, stripped of ICT mysticism:

**Equal highs / equal lows = stop clusters.** Two or more visits to a price with rejection forms a known liquidity pool. Algorithmic and discretionary stops accumulate just beyond. This is empirically observable on order-flow tools (DOM, Bookmap) and is not a controversial claim — every desk trader understands it.

**Sweep / stop run / liquidity grab.** Price punches just beyond the equal level, triggers resting stops (which become market orders), and reverses. The mechanic is real and well-documented. It's how large participants source liquidity to fill size — you can't get filled on 500 ES contracts without somebody offering 500; the easiest way to manufacture offers is to push price into resting buy stops on shorts (or sell stops on longs) above/below an obvious level.

**Displacement.** A bar (or 2–3 bar sequence) of clearly outsized range, often through a level, with high participation. It's the "fingerprint" of aggressive directional positioning. Same as Brooks' "strong trend bar," same as a marubozu, same as a one-bar BoS.

**Fair Value Gap (FVG) / imbalance.** A three-bar sequence where bar 1's wick and bar 3's wick don't overlap, leaving a price range that wasn't traded efficiently. The thesis: price tends to revisit those zones to "rebalance." Honest assessment:
- The underlying mechanic (impulsive moves leave gaps that often partial-fill) is real.
- The ICT mysticism around FVGs ("the algorithm wants this gap filled") is unfalsifiable nonsense.
- Backtest data on FVG strategies in isolation is **weak**. Practitioner studies show that FVG-only entries net out near breakeven once you include slippage. FVGs **at confluence** (with HTF level + structure shift) perform better — but again, the edge is the context, not the gap.

**Sober rule:** treat FVG and order block as **landmarks** (where to expect reactions), not signals (when to enter). The signal is still a structural setup — failure test, BoS-and-retest, etc. — at that landmark.

**Cult-speak to ignore:** "kill zones," "judas swings," "power of three," "AMD," "silver bullet" — the discretionary signals dressed up in lore. Many of these encode real ideas (e.g., "kill zones" = high-volume windows = NY open) but the framing inflates the precision they actually have.

### B.6 Multi-Timeframe Alignment

The professional intraday framework:

| Role | TF (equities / futures) | TF (24h products) |
|---|---|---|
| Macro bias | Daily | Daily |
| Swing context | 60m or 4h | 4h |
| Intraday bias | 15m | 1h |
| Entry trigger | 5m | 15m or 5m |
| Execution / fine timing | 1m | 1m |

**Common pairings used by intraday futures traders:**
- **60m bias + 5m entry**: standard ES/NQ day-trader setup.
- **15m structure + 1m execution**: for scalpers and tape readers (SMB-style).
- **Daily levels + 15m bias + 1m trigger**: for swing-to-intraday hybrid traders.

**Rules:**
- Bias comes from higher TF. Never fight the higher-TF trend with a lower-TF reversal unless you're at an HTF level.
- Entries always on the lower TF — the HTF gives you the *thesis*, the LTF gives you the *trigger* with a tight stop.
- A common error: using the same TF for bias and entry. You end up with sloppy stops and chase fills.

### B.7 Time of Day Effects (Stat-Backed)

US equities / equity-index futures have a **U-shaped intraday volume profile** (well documented, e.g., Bagnall et al., Brogaard, others). The practical buckets:

- **9:30 – 10:30 ET (NY open hour):** highest volume, widest ranges, strongest directional moves. ~30% of daily volume occurs in this hour. Opening range setups live here.
- **10:30 – 11:30 ET:** continuation or first reversal. Often the day's trend confirms or fails here. ICT "kill zone" 10:00–11:30 is essentially this window.
- **11:30 – 13:30 ET (lunch):** lowest volume, choppy, mean-reverting. Studies show signal-to-noise collapses during lunch; pros either stand aside, scalp tight VWAP-revert trades, or use the time to journal and re-rack. The "lunch effect" — small but real edge for mean reversion strategies during this window — is documented (QuantPedia and others).
- **13:30 – 15:00 ET:** afternoon trend resumption or reversal; rates / bonds settlement at 15:00 ET can drive moves.
- **15:00 – 16:00 ET (power hour):** second-highest volume of the day. MOC imbalances build into the close; institutional rebalancing flows dominate. ~25% of daily volume.
- **First 90 min + last 60 min** together account for ~55–65% of daily volume and the majority of day-trader profits.

**Practical translation:** if you can only trade two windows, trade NY open (9:30–11:00) and power hour (15:00–16:00). Trading lunch needs a specific mean-reversion edge or you're paying the spread for nothing.

---

## PART C — The 5–10 Setups Pros Actually Trade

These are the setups that recur across SMB Capital playbooks, Brooks' price-action library, prop firm training, and futures-desk curricula. Each one has clear entry, stop, and target logic. Memorize these; everything else is noise.

### C.1 Opening Range Breakout (ORB) and ORB Failure

**Definition.** The first 5/15/30 minutes establish a range. Trade the break of that range with trend; or trade its failure if the break is rejected.

**Entry trigger.** Close (5m) outside the OR range with volume ≥ 1.5× recent average. Enter on close or on first 1m pullback.

**Invalidation.** Re-entry back inside the OR range (failure test fires).

**Target / R:R.** Typically 1× to 2× the OR range. Trail with structure (HH/HL or LH/LL on 5m).

**Honest data.** ORB-on-everything is **less of an edge today than in 2010**. Many studies show ORB performance has degraded as algos arbitraged the basic version. Specific variants (e.g., 5-min ORB on stocks in play with relative volume > 2× ADV, news catalyst) still net positive. Naive 5-min ORB on index futures is roughly breakeven after costs. ORB **failure** (fade the failed break back into the range) often outperforms ORB **breakout** on balance days. ([Quantified Strategies — ORB backtest](https://www.quantifiedstrategies.com/opening-range-breakout-strategy/))

### C.2 Failed Breakout / Failure Test (Grimes 2B / Wyckoff Spring)

**Definition.** Price pokes beyond a marked level (prior day high/low, swing pivot, ORB edge) and immediately fails back through within 1–2 bars.

**Entry trigger.** Close back inside the level on the failure bar.

**Invalidation.** New high (for short) or new low (for long) beyond the failure bar's extreme.

**R:R.** Typically 2:1 to 4:1 — among the best R:R setups in price action, because the stop is tight (just beyond the swept extreme) and the move can run to the opposite side of the prior range.

**Why it works.** It's the same setup whether you call it 2B, spring, upthrust, liquidity grab + reversal, or failure test. Stop liquidity above the level fuels the move down (and vice versa). Empirically the most repeatable price-action setup in equities and futures.

### C.3 VWAP Rejection (in Trend)

**Definition.** In a trend day, price pulls back to session VWAP (or VWAP ± 1σ band) and rejects.

**Entry trigger.** Wick rejection at VWAP on 1m or 5m, often with a hammer/pin or engulfing candle.

**Invalidation.** Close beyond VWAP (and especially beyond VWAP ± 1σ).

**R:R.** 2:1 typical; can extend to 3–5:1 in strong trend days targeting new HOD/LOD.

**Where it fails.** In balance days, VWAP is a magnet, not a barrier — price oscillates around it. Apply only on days with clear directional bias (gap-and-go, news-driven, breakaway from prior range).

### C.4 Prior Day High / Low Test

**Definition.** Price tests yesterday's high or low (PDH/PDL); reaction or failure trades fire there. These are major resting-liquidity levels.

**Entry trigger.** Either (a) failure test at PDH/PDL (fade), or (b) clean break with retest (continuation). Setup depends on regime.

**Invalidation.** For failure-test fade: new high/low beyond level. For continuation: re-entry back inside prior day range.

**R:R.** Excellent — typically 3:1 because levels attract liquidity and stops sit just beyond.

**Why it works.** PDH/PDL are the most-watched intraday levels by every algo and discretionary trader. The order flow is concentrated there by definition.

### C.5 Range Break and Retest

**Definition.** Intraday consolidation forms; price breaks out; pulls back to broken edge; holds; resumes.

**Entry trigger.** The retest bar — ideally a small-range bar (inside bar or hammer) holding the broken level.

**Invalidation.** Close back inside the range.

**R:R.** 2:1 to 3:1.

**Refinement.** The "second push" off the retest is statistically higher-probability than the first impulse off the break (Brooks teaches this as "second entry").

### C.6 Trend Pullback Continuation (Brooks "high-1 / low-2")

**Definition.** In a clean trend, price pulls back to a moving average (often 20-EMA on 5m) or to a prior breakout level; one or two-bar pullback completes; trend resumes.

**Entry trigger.** Break of the high of the pullback bar (in uptrend); inverse for downtrend.

**Invalidation.** Pullback breaks structure (new LL in uptrend).

**R:R.** 1.5:1 to 3:1. Higher hit rate than R-magnitude trades; closer to a "base rate" income setup than a home run.

### C.7 Reversal at HTF Level

**Definition.** Price extends into a higher-timeframe level (daily S/R, weekly pivot, monthly VWAP, anchored VWAP from a major event); structure shifts on lower TF; counter-trend trade.

**Entry trigger.** Lower-TF break of structure (LH after a series of HH) following an HTF level test.

**Invalidation.** New high/low beyond the HTF level.

**R:R.** 3:1 to 8:1 — these are the "home run" trades. Lower hit rate but big magnitude.

### C.8 Opening Drive Continuation

**Definition.** Strong directional open (gap or first 1–2 bar drive of ≥ 1× ATR). Pullback to opening price or VWAP. Continuation in original direction.

**Entry trigger.** Failure of pullback to make new counter-trend extreme; break of pullback structure.

**Invalidation.** Full retracement through opening drive.

**R:R.** 2:1 to 4:1 on trend days.

### C.9 Late-Day Reversion / Power Hour Move

**Definition.** Late afternoon (15:00–15:45 ET), strong directional flow into MOC. Either continuation in trend direction or reversal of midday chop.

**Entry trigger.** Break of late-day consolidation OR failure test at HOD/LOD made earlier in the session.

**Invalidation.** Reversion to midday balance area.

**R:R.** 2:1 typical. These are short-duration trades but high participation.

### C.10 Setups That Don't Edge in Real Markets (call out)

- **"Ascending triangle = 70% bullish"** style chart-pattern claims: cherry-picked samples, no robust intraday futures evidence.
- **Cup & handle on intraday 5m:** the pattern needs many bars to form; by the time you see it on 5m it's already done.
- **Head & shoulders intraday:** real on daily, weak intraday because the symmetry rarely forms cleanly.
- **Three white soldiers / three black crows** as live entries: by bar 3 the move is exhausted; better as a context cue ("trend is intact") than as a trigger.
- **"Bullish marubozu = automatic buy"**: you're chasing.
- **MA crossovers** as standalone signals: lagging by definition; useful only as bias context, never as triggers.
- **"Doji = reversal"** without location: false. A doji in the middle of nothing is nothing.
- Most **harmonic patterns** (Gartley, butterfly, bat): retrofitted geometry, weak forward performance.

---

## PART D — Failure Modes and Cognitive Pitfalls

Steenbarger's research is the canonical reference here (*Psychology of Trading*; *Trading Psychology 2.0*; *Enhancing Trader Performance*). The categories below are the empirically common failure modes, mapped to the candlestick/price-action domain.

### D.1 Confirmation Bias on Candle Patterns

You decide ES is going up; you start seeing hammers everywhere. You don't see shooting stars. You discount evidence that contradicts your bias and weight evidence that confirms it.

**Mitigation:**
- Define the setup **before** the session in a written plan: "Today I trade failure tests at PDH and PDL." If a hammer prints mid-range, it's not your trade.
- Annotate trades both taken and **not taken**; review the no-trades for whether you missed valid signals or correctly filtered noise. This rebalances perception.

### D.2 "I See a Hammer at Every Wick"

Once you learn a pattern, you over-detect it. Every long lower wick looks like a hammer; every two-bar pullback looks like an engulfing setup.

**Mitigation:**
- Define the pattern in measurable terms: body ≤ 1/3 of range, wick ≥ 2× body, bar range ≥ 1.5× ATR, at a marked level. If the bar doesn't meet all four, it's not the pattern, regardless of what your eye says.
- Use the chart programmatically when possible — TradingView Pine, ThinkScript, NinjaTrader code — to label only bars that mathematically meet the definition. The visual surprise of "wait, that wasn't actually a hammer" is the most underrated learning tool.

### D.3 Overfitting on Small Samples

You see hammer-at-VWAP work three times in a week. You decide it's a 75% strategy. It was actually three random draws from a 55% setup that requires 200+ trades to estimate confidence intervals.

**Mitigation:**
- Treat any setup with < 50 instances as anecdotal.
- For an honest hit-rate estimate, you need ~100–200 trades. Even at 200, the 95% CI on a 60% win rate is roughly ±7 percentage points (53–67%).
- Always quote expectancy (avg win × win rate − avg loss × loss rate − costs) alongside hit rate. A 70% win rate on 1:1 R is great; a 70% win rate on 0.4:1 R after slippage is a losing strategy.
- Backtest, then **forward-test** in sim or small size, then scale. The forward-test reveals execution costs and behavioral leaks the backtest missed.

### D.4 Pattern Works in One Regime, Fails in Another

The biggest practical killer. ORB worked in 2010–2015 trending equities; it's marginal in 2020s low-vol regimes. VWAP mean reversion works in balance; it gets you killed on trend days. Failure tests work at marked levels; they're random noise mid-range.

**Mitigation:**
- Always classify the day **before** entry: trend day (open near low, close near high; ADR expanding) vs balance day (range-bound, mean-reverting) vs failed-trend / two-way day. Different setups for each.
- Use simple regime filters: VIX level, ATR vs 20-day average, open-vs-previous-close gap size, overnight ES range vs 5-day average.
- Brooks' shorthand: "always-in long" or "always-in short" or "two-way trading." Identify which one is in force every 30 minutes.

### D.5 Narrative Construction After Losses

You take a failure-test short, it stops you, you decide failure tests don't work. n = 1, sample = useless, but the loss is salient and you abandon a real edge.

**Mitigation (Steenbarger):**
- Journal in **process** terms ("Did I follow my rules?") not **outcome** terms ("Did I win?"). A losing trade that followed the rules is a good trade. A winning trade that violated the rules is a tax bill waiting.
- Track setups by 30-trade rolling windows. If a setup goes from 60% to 35% over 30 trades, that's signal — investigate regime change. If it goes 60% → 55% → 65% in three 30-trade windows, that's normal variance.

### D.6 Pattern Without Context Worship

The candle is the **trigger**. Context (location, regime, structure, time-of-day, participation) is the **edge**. Retail trades patterns; pros trade context with patterns as the trigger.

If you cannot articulate, in one sentence, why this specific bar at this specific level in this specific regime is a trade, you don't have a trade. You have a pattern recognition tic.

### D.7 Latency / Information Asymmetry Self-Delusion

Most retail traders are slower than the algos by 50–200ms even on retail-fast routes. If your "edge" depends on being first to react to a 5m close, you're competing against people who can see and act on the print before you. Build edges that don't decay in milliseconds — i.e., **structural** edges (regime + level + setup), not **reflex** edges.

---

## Sources and Further Reading

**Books (read these in this order if starting from a quant base):**
- Adam Grimes, *The Art and Science of Technical Analysis* (Wiley 2012). The single best book for a quant moving into discretionary technical analysis. ([Wiley/Amazon](https://www.amazon.com/Art-Science-Technical-Analysis-Strategies/dp/1118115120))
- Al Brooks, *Reading Price Charts Bar by Bar* (Wiley 2009) and the three-book *Trading Price Action* set: *Trends*, *Trading Ranges*, *Reversals* (Wiley 2011–2012). Dense, repetitive, indispensable. ([Reading Price Charts](https://www.amazon.com/Reading-Price-Charts-Bar-Technical/dp/0470443952))
- Mike Bellafiore, *One Good Trade* (Wiley 2010) and *The PlayBook* (Wiley 2013). The desk-trader playbook approach — codify your repeatable setups. ([One Good Trade](https://www.amazon.com/One-Good-Trade-Competitive-Proprietary/dp/0470529407))
- Brett Steenbarger, *The Psychology of Trading* (Wiley 2003), *Enhancing Trader Performance* (Wiley 2006), *Trading Psychology 2.0* (Wiley 2015). Pattern recognition, cognitive bias, deliberate practice. ([Psychology of Trading](https://www.amazon.com/Psychology-Trading-Techniques-Minding-Markets/dp/0471267619))
- Thomas Bulkowski, *Encyclopedia of Candlestick Charts* (Wiley 2008). Treat as a reference, not a strategy book. The win rates are point estimates; use them to disqualify the worst patterns, not to overfit the best.

**Blogs / online (free):**
- Adam Grimes — [adamhgrimes.com](https://www.adamhgrimes.com/) — especially the "[Failure Test](https://www.adamhgrimes.com/failure-test-2/)" series and "[First Principles of Technical Analysis](https://www.adamhgrimes.com/first-principles-of-technical-analysis-1/)."
- Brett Steenbarger — [TraderFeed](http://traderfeed.blogspot.com/).
- SMB Capital — [smbtraining.com/blog](https://www.smbtraining.com/blog/bellas-blog).
- Bulkowski's Pattern Site — [thepatternsite.com](https://www.thepatternsite.com/), specifically [Top 10 Candlestick Performers](https://www.thepatternsite.com/CandlePerformers.html) and the individual pattern pages.
- Stockbee (Pradeep Bonde) — episodic-pivot / momentum-burst playbook for stocks; less applicable to index futures but excellent for stocks-in-play.

**Data / studies referenced:**
- Bulkowski candlestick rankings: [Top 10 Performers](https://www.thepatternsite.com/CandlePerformers.html), [Hammer](https://thepatternsite.com/Hammer.html), [Bull Engulfing](https://thepatternsite.com/BullEngulfing.html), [Bear Engulfing](https://thepatternsite.com/BearEngulfing.html).
- ORB backtests / degradation: [Quantified Strategies — ORB](https://www.quantifiedstrategies.com/opening-range-breakout-strategy/); see also Concretum Group and Edgeful for stocks-in-play ORB nuance.
- Intraday volume / lunch effect: [QuantPedia — Lunch Effect](https://quantpedia.com/lunch-effect-in-the-u-s-stock-market-indices/); academic intraday volume studies (Bagnall, Brogaard) document the U-shape consistently.
- VWAP mean reversion: practitioner studies summarized at TradingView, edgeful, and SpotGamma; the directional edge sits in the 0.25–0.9 percentage-point range per signal, conditional on regime.
- FVG / SMC critique: GitHub [smart-money-concepts](https://github.com/joshyattridge/smart-money-concepts) Python package — useful for actually testing the claims rather than taking ICT lore at face value.

---

## Drill Plan (90 Days)

To convert this reading into reflex:

**Days 1–30:** Mark up 50 historical 5m ES sessions by hand. Annotate market structure (HH/HL/LH/LL), PDH/PDL, ORB, VWAP. Identify every failure test, every ORB break/fail, every VWAP rejection. No live trading.

**Days 31–60:** Sim trade only the failure test setup at PDH/PDL/ORB edges. 100 trades minimum. Journal every trade with screenshot, context, R outcome, regime tag. Target ≥ 1.5R average and ≥ 50% hit rate.

**Days 61–90:** Add VWAP rejection setup in trend days. Track regime classification accuracy daily. Move to small live size only after 100 sim trades with positive expectancy.

After 90 days you should be able to look at any 5m chart at any time and articulate in one sentence: (a) the regime, (b) the next two levels of interest, (c) the setup you would take and the one you would fade. That's the desk-trader bar.

---

*Last updated 2026-05-13. Curriculum file 02 of the DayTrader research series.*
