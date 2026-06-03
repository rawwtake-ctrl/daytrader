# BabyPips School of Pipsology, Curated for an Experienced Systems Trader

**Author:** Internal research note for solo-operator day-trader workflow
**Purpose:** Map the full BabyPips free curriculum, mark what an experienced bot operator actually needs to read, and call out the retail mythology that the school still teaches.
**Verdict up front:** BabyPips is the best free *vocabulary and mechanics* primer on the internet. Its risk-management and trading-plan curriculum is genuinely good. Its indicator-and-pattern curriculum is dated retail folklore that does not survive serious backtesting. The site is 80% generic to any leveraged instrument and 20% forex-specific; the forex-specific 20% (carry, sessions, COT, currency correlation) is the part most outside reading is weakest on. Total reading time for a structured systems trader filtering at "USEFUL or better" is roughly 6-8 hours.

---

## Section A: The School of Pipsology Curriculum Mapped

The school is structured as a school: 10 grade-bands, each with multiple lessons (300+ lessons total, ~40-60 hours for a thorough learner per BabyPips' own estimate). Below is every grade with the topics it covers and a verdict.

### Preschool — Forex 101
URL: `https://www.babypips.com/learn/forex/preschool`
Covers: What forex is, why people trade it, who trades it, the major/minor/exotic pair taxonomy, when markets are open, the four trading sessions (Sydney/Tokyo/London/New York), session overlaps.
**Verdict: SKIP for an experienced trader**, except the session-overlap page (`/learn/forex/session-overlaps`) which is the cleanest one-page summary of why FX liquidity isn't uniform across the 24-hour day. The 08:00-12:00 ET London/NY overlap carries roughly 70% of daily FX volume — a load-bearing fact for any bot that schedules execution.

### Kindergarten — Brokers, Charts, Three Types of Analysis
URL: `https://www.babypips.com/learn/forex/kindergarten`
Covers: Choosing a broker, regulation by jurisdiction, line/bar/candle chart types, and the "three legs of the stool" framing (technical, fundamental, sentiment).
**Verdict: SKIP**, with one exception — the three-legs framing is genuinely useful as a reminder that pure-technical bots leave money on the table when macro and positioning data are cheap to integrate. The broker-selection material is heavily slanted toward retail spot-FX brokers (MT4/MT5/cTrader) and is irrelevant if you trade futures, equities, or crypto.

### Elementary — Classical Technical Analysis
URL: `https://www.babypips.com/learn/forex/elementary`
Covers: Support and resistance, Japanese candlesticks (every named pattern), Fibonacci retracement/extension, moving averages (SMA, EMA, crossovers, dynamic S/R), the "common chart indicators" stack (Bollinger Bands, MACD, parabolic SAR, Stochastic, RSI, ADX, Ichimoku).
**Verdict: USEFUL for vocabulary, DANGEROUS if taken as edge.** Every term in this section appears in trading discourse, so reading it gives you the shared vocabulary. But virtually every claim in this grade — "a hammer at support is a buy signal," "RSI > 70 is overbought," "MACD crossover means trend change" — fails when backtested rigorously on out-of-sample data. The honest framing the site itself uses elsewhere (RSI is "for confirming not predicting," MACD lags by construction) is buried; the headline lessons present these as standalone signals.
**Read for:** terminology compatibility with other traders. **Don't:** wire any of these into a bot as a primary signal.

### Middle School — Indicator Stack and Pivots
URL: `https://www.babypips.com/learn/forex/middle-school`
Covers: Leading vs. lagging indicators, oscillators (Stochastic, RSI, Williams %R, Momentum), important chart patterns (double tops/bottoms, head-and-shoulders, wedges, rectangles, pennants, triangles), pivot points (standard, Camarilla, Woodie, Fibonacci) for range trading and breakouts.
**Verdict: SKIP indicator content, USEFUL for pivot-point math.** The leading-vs-lagging discussion is intellectually honest about the trade-off but stops short of the obvious conclusion: a lagging indicator that is also unreliable is just slow noise. The pivot-point lessons are the most useful in this grade — pivot levels are a real intraday reference grid that institutional FX desks actually watch, and the formulas are simple enough to wire into a bot in one afternoon.
**Read:** `/learn/forex/forex-pivot-points` and `/learn/forex/pivot-points-summary`. **Skip:** the rest.

### Summer School — Heikin Ashi, Elliott Wave, Harmonic Patterns
URL: `https://www.babypips.com/learn/forex/summer-school`
Covers: Heikin Ashi candles, the full Elliott Wave construct (impulses, corrections, fractal nesting), harmonic patterns (ABCD, Gartley, Butterfly, Bat, Crab, "animal" patterns generally).
**Verdict: DANGEROUS.** This is the curriculum's weakest grade. Elliott Wave is unfalsifiable in real time (every count works in hindsight, the "valid" count is the one that worked), and harmonic patterns are pareidolia codified into Fibonacci ratios. There are no published backtests with edge here that survive multiple-testing correction. Heikin Ashi is a useful *visualization* of trend persistence but should never be wired into an execution rule (it smooths price, so signals are confirmed after the move).
**Read:** the Heikin Ashi page only, and only for visualization vocabulary.

### High School — Breakouts, MTF, Trading Styles, News
URL: `https://www.babypips.com/learn/forex/high-school`
Covers: Trending vs. ranging environments, breakouts and fakeouts, divergence trading, market environment recognition, multiple-timeframe (MTF) analysis (the top-down 3-tier framework), trading styles (scalper/day/swing/position), news trading mechanics.
**Verdict: ESSENTIAL for the MTF and trending/ranging pages, USEFUL for news trading, SKIP divergence.** The top-down MTF framework (higher TF for bias, intermediate for setup, lower for entry) is a discipline every systems trader should encode explicitly rather than implicitly. The "know your market environment" page (`/learn/forex/trendspotting`) is the cleanest articulation of the single most important pre-trade question: *am I in a trend or a range?* Strategy selection collapses if you don't answer it first. News-trading material is solid on mechanics (volatility traps around scheduled releases) but light on actual edge.

### Undergraduate Freshman — Fundamental Analysis
URL: `https://www.babypips.com/learn/forex/undergraduate-freshman`
Covers: What moves a currency, central banks and policy rates, GDP/CPI/PCE/PPI/unemployment, leading vs. lagging economic indicators, top-down macro trade thesis construction, planning around scheduled releases. Includes the carry-trade introduction (`/learn/forex/what-is-carry-trade`, `/learn/forex/how_do_carry_trades_work_for_forex`).
**Verdict: ESSENTIAL.** This is the curriculum's strongest grade for a quantitatively-minded trader. The framing — "currencies are priced off interest-rate differentials and growth/inflation expectations, not chart patterns" — is correct and not optional. The carry-trade mechanics page explains rollover, swap, and overnight financing in concrete terms that map directly onto bot accounting (positions held past 17:00 ET get debited/credited the differential).

### Undergraduate Sophomore — Intermarket and Currency Crosses
URL: `https://www.babypips.com/learn/forex/undergraduate-sophomore`
Covers: Currency correlation, intermarket analysis (bonds-FX, equities-FX, commodities-FX, gold-silver, oil-CAD, AUD-iron-ore), currency crosses (non-USD pairs), commodity currencies, how to use crosses to triangulate the majors.
**Verdict: ESSENTIAL for correlation, USEFUL for the rest.** The currency-correlation lesson is the part of the BabyPips curriculum that most directly applies to portfolio-level risk management for a multi-instrument bot. If you have positions in EUR/USD, GBP/USD, and AUD/USD simultaneously, you do not have three independent dollar trades — you have one dollar trade with three legs and your "diversification" is roughly half of what your position-count suggests. The Currency Correlation Calculator (`/tools/currency-correlation`) makes this concrete.

### Undergraduate Junior — Sentiment, COT, Risk-On/Risk-Off
URL: `https://www.babypips.com/learn/forex/undergraduate-junior`
Covers: What market sentiment is and how to read it, the CFTC Commitment of Traders (COT) report (legacy and TFF, commercial vs. non-commercial vs. small spec, open interest), how to set up COT indicators on TradingView, risk-on/risk-off regime detection, the BabyPips Risk-On/Risk-Off Meter (`/tools/risk-on-risk-off-meter`).
**Verdict: ESSENTIAL.** The COT-report lessons are the highest-density edge material in the entire free curriculum. The standard contrarian read — when non-commercial (specs) are at multi-year extreme positioning, fade them — is a real published edge with academic backing. The school's framing of the three groups, the divergence between commercials and specs, and open-interest context as "the layer most traders miss" is correct and not commonly taught elsewhere for free. Read this grade in full.

### Undergraduate Senior — Risk and Position Sizing
URL: `https://www.babypips.com/learn/forex/undergraduate-senior`
Covers: Why most retail traders lose, drawdown math and the breakeven recovery formula, risk per trade (and why the 2% rule has been updated downward), the position-size calculation (account × risk% ÷ stop_distance_in_pips × pip_value), layered risk budgeting (per-trade / per-idea / per-day / weekly circuit breakers), portfolio heat, the stop-loss playbook, prop-firm-specific risk rules.
**Verdict: ESSENTIAL.** This is the most useful grade in the school for a working bot operator. The drawdown asymmetry (you need +25% to recover from -20%, +100% to recover from -50%) is the single most important number in retail trading and the school presents it cleanly. The layered risk-budget construct (per-trade is necessary but insufficient; daily and weekly circuit breakers are what actually save accounts) maps directly onto bot guardrails. Read in full; this is what justifies the entire curriculum.

### Graduation — Trading Plan, Psychology, Journal, Plus Prop Firms 101
URLs: `https://www.babypips.com/learn/forex/graduation`, `/learn/forex/what-is-a-trading-plan`, `/learn/forex/congratulations-you-made-it`
Covers: Trading-plan construction (personality, expectations, risk rules, system, journal, review), trading-style fit to lifestyle, psychology (fear, greed, the four stages of competence, common pitfalls), journal architecture (three-layer: pre-trade plan, in-trade observations, post-trade review), Prop Firms 101 (business model, common pitfalls, risk rules of funded-trader programs).
**Verdict: USEFUL.** See Section E below.

---

## Section B: The Genuinely Advanced Content Buried in BabyPips

Filtering out the indicator folklore, the school has substantive material in five areas worth pulling out.

### B1: Risk management (Senior year)

The school's risk curriculum has four ideas that are correctly stated and worth encoding:

1. **Drawdown is asymmetric.** Recovery percentage > drawdown percentage, always. The school states the breakeven formula plainly: recovery_needed = drawdown / (1 - drawdown). At -10% you need +11.1%, at -20% +25%, at -50% +100%, at -90% +900%. This kills the "I'll just trade my way back" instinct.
2. **2% per trade is now considered too high** for serious capital. The school updates the legacy Van Tharp / Alexander Elder "2% rule" to 0.5%-1% for traders running anything resembling Kelly-aware sizing.
3. **Layered risk budget**, not just per-trade. Per-trade limit + per-idea (correlated trades counted together) + per-day stop + per-week circuit breaker. The school's framing is: a per-trade cap alone gives you no protection against a clustering bad day. This is exactly how serious systematic shops structure live risk and is the right mental model for a bot's guardrails.
4. **Portfolio heat** = sum of open risk across positions, not just position-count or notional. `/learn/forex/portfolio-heat-managing-total-risk-exposure` is the cleanest free statement of this concept.

### B2: Position-sizing math

The core formula the school teaches:

```
Position Size = (Account Balance × Risk%) / (Stop Distance × Pip Value)
```

Example: $10,000 account, 1% risk, 50-pip stop, EUR/USD where pip value is $10 per standard lot → max risk $100 → 100 / (50 × 10) = 0.2 lots = 20,000 units (a "mini" position). This formula generalizes outside FX cleanly: replace pip-value-per-lot with point-value-per-contract or dollar-per-share. The honest answer the school gives — "your stop loss is just a number on a screen unless this calculation drives your size" — is the single most important transferable lesson from the entire curriculum.

The free `/tools/position-size-calculator` and `/tools/pip-value-calculator` will compute it for any account currency and instrument. Worth bookmarking even if you have your own bot-side sizer.

### B3: Market microstructure introduction

**Honest assessment:** there isn't much. BabyPips covers bid/ask/spread as terms, talks about brokers as market makers vs. ECN, and touches on slippage and rollover mechanics. There is no real treatment of order-book dynamics, queue priority, latency, hidden liquidity, or auction mechanics. This is a gap. For microstructure substance go elsewhere (Larry Harris *Trading and Exchanges*, Robert Kissell on transaction-cost analysis, or the actual venue specifications).

### B4: Psychology (compared to Steenbarger)

BabyPips' psychology section is competent, journalist-level coverage of common emotional pitfalls — fear, greed, revenge trading, overtrading, FOMO, the four stages of competence, the urge-to-get-rich frame. It is not in the same intellectual category as Brett Steenbarger's body of work (*The Psychology of Trading*, *The Daily Trading Coach*, *Trading Psychology 2.0*).

Where they differ:
- **BabyPips:** describes the pitfalls and says "have a plan, journal, be disciplined."
- **Steenbarger:** treats trading psychology as applied behavioral science, builds an explicit performance-coaching framework, and writes for traders who are already past the basics.

If a trader is going to read one psychology source, it should be Steenbarger. BabyPips' psychology pages are useful for vocabulary and as a checklist of failure modes, not as a coaching system. The school's strongest psychology contribution is the *journaling* prescription (three-layer: pre-trade plan, mid-trade observations, post-trade review) — see Section E.

### B5: Carry-trade mechanics

The school's carry-trade pages are the cleanest free explanation of forex's structural-yield trade. Three correctly-stated points:

1. **Carry is the interest-rate differential** between the two currencies of a pair. Holding long AUD/JPY when AUD policy rate is 4% and JPY policy rate is 0% earns ~4% annualized in swap, paid daily on the broker's tomorrow-next (T/N) cycle.
2. **The trade isn't free.** When risk appetite deteriorates, carry trades unwind violently — the 2008 and 2020 JPY-cross moves are the canonical examples. The school says this but doesn't fully connect it to position-sizing: carry-trade max drawdown clusters are 4-6x larger than the daily distribution suggests because returns are negatively skewed.
3. **The cleanest carry pairs are AUD/JPY, NZD/JPY, and crosses involving high-yield EM (TRY, ZAR, MXN, BRL)** — but those EM crosses have wide spreads and political-event tail risk that often eats the carry.

This is forex-specific edge that does not translate to futures or equities, and it is worth the time to internalize even if your bot doesn't trade FX directly, because the macro mental model (capital flows to yield until risk-off forces unwind) drives cross-asset behavior generally.

### B6: Forex-specific edges that don't apply to futures/equities

- **24-hour markets with session structure.** Liquidity is not uniform; the 08:00-12:00 ET London/NY overlap dominates. Equities (RTH) and futures (effectively 23x5) have different liquidity profiles.
- **Currency-pair correlation as the default state.** EUR/USD, GBP/USD, AUD/USD are not three trades; they are roughly one dollar trade. Cross-asset traders are used to thinking about correlation; FX traders cannot avoid it because the dollar is on one side of every major pair.
- **Carry as a structural return component.** Equities have dividends; futures have roll yield; FX has overnight swap. Each is a discrete cashflow component separate from price.
- **Central-bank policy as primary driver.** Currencies are priced off relative monetary policy and growth expectations more cleanly than equities, which have idiosyncratic earnings risk on top of macro.
- **No exchange-traded order book in retail spot FX.** Spot FX is OTC; "the order book" you see at a broker is that broker's book, not a centralized venue. This is invisible in BabyPips and is a real microstructure point: every retail FX trader trades against their broker's pricing, not a global venue.

---

## Section C: BabyPips Tools Worth Using

The site's tool suite is at `https://www.babypips.com/tools`.

### C1: Economic Calendar — `/economic-calendar`

**Honest comparison vs. ForexFactory:** BabyPips' calendar has better event descriptions and a cleaner UI; ForexFactory's calendar is faster, has a stricter impact-level legend, and is the de facto standard in retail-FX discourse. The two disagree on impact ratings for the same event with surprising frequency — events that ForexFactory marks high-impact sometimes show as medium or low on BabyPips. **Use ForexFactory as primary; cross-check on BabyPips for event description if the ForexFactory tooltip is too terse.** If you only want one source, pick ForexFactory.

### C2: MarketMilk — `https://marketmilk.babypips.com/`

A web-based visualization that shows currency strength, pair trend strength, overbought/oversold across timeframes, and volatility for the 8 major currencies and major crypto. Useful as a **pre-trade scan** — at a glance, which majors are strong, which are weak, which pairs are stretched. Not a signal source. Treat it as the FX equivalent of a heatmap and nothing more. Free, browser-based, no account required for the public view.

### C3: Trader Sentiment Data

This is the one most often misused. The retail-sentiment indicators that brokers publish (FXCM SSI, OANDA positioning, Myfxbook Community Outlook, IG client sentiment) are useful **only at extremes** and **only as a contrarian signal**. The school states this correctly: 70-80% of retail traders lose money, so when 80%+ of retail is positioned one way, fading them is statistically the right side. It does not say — and you should know — that at modest skew (60/40, 65/35) the signal is noise. The contrarian-at-extremes read needs roughly 75%+ one-sided positioning to clear the noise threshold.

The school links the FXCM SSI history; it does not host its own retail-positioning feed. For a bot, the data sources to wire in are: OANDA's positioning API (free with account), Myfxbook community feed, and the CFTC's weekly COT (the institutional version, free, more reliable than retail SSI for swing-timeframe decisions).

### C4: Position Size Calculator — `/tools/position-size-calculator`

Best-in-class for free FX position sizing across account currencies. Wire the same formula into your own bot, but the web tool is correct and worth keeping as a sanity-check calculator. Mirror on Google Play as the "Babypips Lot Size Calculator."

### C5: Pip Value Calculator — `/tools/pip-value-calculator`

Same use case. Useful for cross-checking pip-value math when an instrument's quote currency differs from your account currency (e.g., trading GBP/JPY with a USD account).

### C6: Currency Correlation Calculator — `/tools/currency-correlation`

The right answer to "am I really diversified across these 4 FX positions or am I just long-dollar four ways?" Updates with rolling correlation windows. Use before adding a fourth FX position to an existing FX book.

### C7: Pivot Point Calculator — `/tools/pivot-point-calculator`

Computes daily/weekly/monthly classical, Woodie, Camarilla, and Fibonacci pivot levels. Pivot levels are watched by enough professional FX desks that they self-fulfill at the daily and weekly cadence — particularly for the majors during the London/NY overlap.

### C8: Risk-On / Risk-Off Meter — `/tools/risk-on-risk-off-meter`

A composite that scores cross-asset risk appetite (equity indices, credit spreads, safe-haven flows, JPY/CHF strength, gold). Useful as a regime tag for a bot — risk-off regimes mean carry trades unwind, JPY strengthens, USD strengthens vs. EM, AUD/NZD weaken. Not actionable on its own but a good single-number context input.

---

## Section D: What BabyPips Gets Wrong

Calling out the retail mythology the school still teaches as fact, ranked by how much damage taking it seriously does.

### D1: Indicator-as-signal content (DANGEROUS)

The Elementary and Middle School lessons present RSI, MACD, Stochastic, parabolic SAR, and friends as actionable signals. Every published rigorous backtest of vanilla overbought/oversold thresholds on liquid instruments shows no edge after costs once you correct for multiple testing and survivorship bias. The school's own forum posts (and forum users) frequently say "RSI is for confirming, not predicting" — but the curriculum lessons do not lead with that caveat. A new trader who learns the Elementary curriculum and trades it loses money systematically; the lessons should be read as **vocabulary** and not as **method**.

### D2: Chart-pattern claims without statistics (USEFUL but skeptically)

Head-and-shoulders, double tops, pennants, flags, wedges, triangles — the school describes each pattern's textbook setup and target rule. Bulkowski's *Encyclopedia of Chart Patterns* is the canonical statistical reference for these patterns and shows that the headline reliability numbers in retail education ("head-and-shoulders is 81% reliable") collapse when you adjust for selection bias (patterns are easier to find in hindsight) and for the asymmetric definition of "success" (any move toward the target counts). The school doesn't cite the underlying statistics. Read the patterns as descriptive vocabulary for what other traders are watching, not as standalone edge.

### D3: Round-number percentages that don't survive Kelly (CORRECTABLE)

The "1-2% per trade" rule is a survival heuristic, not an optimum. Real Kelly fraction for a system depends on win rate, win/loss ratio, and the correlation structure of consecutive trades. For a typical retail discretionary system (50-55% win rate, 1.3 win/loss ratio), full Kelly is roughly 8-12% per trade, and conventional wisdom recommends quarter- to half-Kelly (so 2-6%) for path-dependence reasons. The 1% rule is conservative for that system; for a 35% win rate, 2.5R-average trend-following system, 1% might actually be too high. The school's risk content updates the legacy 2% downward to 0.5-1% but doesn't connect the number to system characteristics. **The right framing for a bot operator:** size by Kelly fraction off measured (not theoretical) system statistics, capped by max-drawdown tolerance and correlation-adjusted at the portfolio level.

### D4: Retail-mythology framings

A few specific claims to flag:

- **"The trend is your friend"** — true at low resolution, useless at execution scale. Trend definitions are timeframe-dependent and trend-following systems are notorious for whipsaws when implemented naively.
- **"Cut your losses, let your profits run"** — the school states it correctly but doesn't note that for systems with high win-rate and modest tails (mean-reversion, scalping), the opposite is structurally correct (take small profits frequently, accept that occasional larger losses are part of the distribution). The dictum is style-specific.
- **"Forex is a zero-sum game"** — repeated frequently. Not quite right: forex is **negative-sum after spread and rollover costs** to retail (broker takes the spread, sometimes the rollover differential at unfavorable rates). The implication — "for me to win, someone else has to lose" — is true only after you've already given the broker their cut.
- **Demo accounts as preparation.** The school recommends demo trading. It's directionally right for mechanics-familiarization but psychologically misleading: P&L stress with real money is qualitatively different and is the actual skill being tested. Demo is a syntax check, not a system test.

### D5: Where it conflates retail folklore with edge

- **"Round numbers (00, 50) act as support and resistance."** Sort of, sometimes, with lower reliability than the lessons imply. Real S/R clustering is at *prior pivot levels* and *prior session high/low* far more reliably than at round levels.
- **"Pin bars and engulfing candles at S/R are high-probability setups."** Single-candle patterns at S/R levels have small edge in liquid FX majors that's mostly consumed by spread. They're more useful as confirming evidence within a multi-factor setup than as standalone triggers.
- **"News trading is profitable if you can predict the data."** The school correctly notes that the headline number matters less than the surprise vs. consensus, but doesn't fully spell out that retail traders trying to trade news releases are racing institutional algorithmic flow that has co-located access and millisecond-class execution. **News trading at retail speeds is structurally disadvantaged.** Trade the consequences, not the print.

---

## Section E: The Graduation Exam — The Trading Plan Walkthrough

The school's final grade asks the student to assemble a complete trading plan. The structure they recommend (from `/learn/forex/what-is-a-trading-plan` and the Graduation lessons) has six components. Each maps onto a corresponding section of a systems-trader's bot specification.

### E1: Trader Personality / Style Fit (school) → Bot Style Charter (you)

The school's framing: who are you, what timeframe matches your temperament, what hours can you actually trade. **The bot-operator translation:** what style of edge is this bot designed to capture (mean-reversion, momentum, carry, event-driven, market-making), what holding-period distribution does it target, what's the latency tolerance, what hardware budget supports it. A bot is a style charter executed in code — write the charter first.

### E2: Risk Management Rules (school) → Risk Guardrails (you)

The school's six-item list: per-trade risk, max concurrent positions, daily loss limit, weekly loss limit, max drawdown shutdown level, correlation-adjusted position aggregation. **For a bot:** every one of these belongs as explicit, codified, hard-coded guardrails that the strategy logic cannot override. Per-trade is the easiest; daily and weekly circuit breakers are what actually save accounts in the failure modes that matter; max-drawdown auto-shutdown is the difference between a -20% bad week and account-blown. Reference the `MEMORY.md` rules already in this workspace — **"every dollar," "cancel before kill," "verify buy fill on chain"** — those are exactly the layered guardrails the school's Senior year curriculum describes, just specific to a different instrument.

### E3: The Trading System (school) → Strategy Spec (you)

The school's required content: entry rules, exit rules, position-size rule, asset selection, timeframe, market environment filter. **For a bot:** the strategy module's interface — `get_signal(bar) -> {direction, size, stop, target}`, `should_enter(market_state) -> bool`, `should_exit(position, market_state) -> bool`. The school's discipline of writing every rule down before risking capital maps directly onto having a versioned strategy spec checked into the repo before live deploy.

### E4: The Journal (school) → Trade Log + Postmortem (you)

The school recommends three journal layers:
1. **Pre-trade plan** — written before entry: the setup, the rationale, the invalidation level.
2. **In-trade observations** — what's happening that you didn't expect.
3. **Post-trade review** — what worked, what didn't, what you'd change.

**For a bot:** structured trade logs (entry rationale stamped at decision time, market context snapshot, all parameters), live event log (slippage vs. expected, partial fills, unexpected order rejects), and post-trade reconciliation (P&L vs. expected, chain/broker-verified fills, attribution: alpha vs. costs vs. slippage). This is the part of the curriculum that translates most directly. The existing bot work in this workspace (AlphaTrader, BTCBash) already implements layer 2 (event logs) and layer 3 (post-trade reconciliation, daily postmortems). The school's discipline of also writing layer 1 — the rationale, formalized, before the trade — is the part that's easy to skip and worth adding.

### E5: Review Cadence (school) → Daily / Weekly / Monthly Cycles (you)

The school recommends daily journal entry, weekly review of completed trades, and monthly performance analytics. **For a bot:** daily summary (P&L, fills, errors), weekly performance attribution (system performance vs. expected by regime), monthly walk-forward audit (does the recent live distribution match the backtest distribution, or has the edge decayed). The monthly audit is the one that catches dead strategies before they bleed serious capital.

### E6: Plan Update Protocol (school) → Versioned Strategy Changes (you)

The school says: don't change the plan mid-trade, but review and update on a fixed schedule. **For a bot:** strategy changes go through a code-review and forward-test gate before live; ad-hoc parameter tweaks while live are a known failure mode. This connects to the rule already in the workspace memory: "discuss before edit." The school's framing makes the same point for human traders.

---

## Section F: 1-Hour Speed-Run for an Experienced Trader

Reading order to extract the 80% of value in roughly one hour. URLs listed; all are free, no account required.

**Minute 0-10: Risk math (the most important 10 minutes)**
- `https://www.babypips.com/learn/forex/undergraduate-senior` — drawdown asymmetry, recovery math, layered risk budget, portfolio heat.
- `https://www.babypips.com/learn/forex/portfolio-heat-managing-total-risk-exposure` — total open risk concept.
- `https://www.babypips.com/learn/forex/stop-loss-playbook` — stop placement frameworks.

**Minute 10-20: Position sizing**
- `https://www.babypips.com/learn/forex/position-sizing` and `/calculating-your-position-sizes` and `/calculate-position-size-different-forex-pairs`.
- `https://www.babypips.com/tools/position-size-calculator` — bookmark.

**Minute 20-30: Sentiment and positioning (the edge-bearing grade)**
- `https://www.babypips.com/learn/forex/commitment-of-traders-report` — COT mechanics.
- `https://www.babypips.com/learn/forex/the-cot-trading-strategy` — the contrarian-at-extremes read.
- `https://www.babypips.com/learn/forex/understanding-cot-report` and `/getting-down-and-dirty-with-the-numbers`.
- `https://www.babypips.com/learn/forex/summary-of-market-sentiment`.

**Minute 30-40: Carry and intermarket**
- `https://www.babypips.com/learn/forex/what-is-carry-trade` and `/how_do_carry_trades_work_for_forex` and `/taking-advantage-of-interest-rate-differential`.
- `https://www.babypips.com/learn/forex/intermarket-analysis-cheat-sheet`.
- `https://www.babypips.com/learn/forex/what-is-currency-correlation`.

**Minute 40-50: Session structure and market environment**
- `https://www.babypips.com/learn/forex/session-overlaps`.
- `https://www.babypips.com/learn/forex/trendspotting` — trend vs. range, the single most important pre-trade question.
- `https://www.babypips.com/learn/forex/multiple-time-frame-analysis` and `/time-frame-combinations` — top-down MTF.

**Minute 50-60: Plan, journal, psychology**
- `https://www.babypips.com/learn/forex/what-is-a-trading-plan` and `/summary-developing-a-trading-plan`.
- `https://www.babypips.com/learn/forex/reviewing-your-trading-journal`.
- `https://www.babypips.com/learn/forex/why-traders-fail` — the "5 Deadly O's" framework as a failure-mode checklist.

What you intentionally skip: all of Preschool, Kindergarten, Elementary, Middle School (except pivots if needed), Summer School (entirely), and the indicator pages in High School. Roughly 70% of the school by lesson-count, 20% by edge-content.

---

## Section G: Where BabyPips Beats Investopedia

- **Practical and step-by-step.** Investopedia is written for SEO definition lookups; BabyPips is written for someone who is sequentially building a skill. The school's progression from mechanics → analysis types → risk → plan is pedagogically coherent.
- **Trader-written, not journalist-written.** The voice is conversational and the framings are recognizable to anyone who has actually traded. Investopedia's articles often read as competent reportage by writers who have not put on a trade.
- **Free tools are actually useful.** Position-size calculator, currency-correlation calculator, pip-value calculator, MarketMilk, risk-on/risk-off meter. Investopedia has a small set of calculators (mortgage, retirement) that are not trader-facing.
- **Forex-specific depth.** Carry trade, session structure, COT report use for FX, currency correlation, intermarket FX relationships — BabyPips goes deeper than Investopedia on every forex-native topic.
- **Quizzes and a curriculum spine.** Each lesson has a check-yourself quiz; the curriculum has a structure you can complete. Investopedia is a reference library, not a course.

---

## Section H: Where Investopedia Beats BabyPips

- **Definitions and reference lookup.** When you need "what is convexity," "what is gamma scalping," "what is a CDS index roll," Investopedia is the right destination — entries are tighter, scoped to the term, and aggressively SEO-optimized so they surface fastest.
- **Wider scope.** Equities, options, futures, fixed income, structured products, accounting, tax, real estate, crypto — Investopedia covers all of them. BabyPips is FX-first and FX-mostly.
- **SEO discoverability.** For any specific concept, the Investopedia page is almost always in Google's top 3 results. BabyPips ranks well for forex-specific terms but loses for cross-asset terms.
- **Academic / formal references.** Investopedia entries often cite source papers, regulations, or formal definitions. BabyPips is conversational and rarely cites primary sources.
- **Term-of-art breadth.** Greeks, term-structure, basis, contango, backwardation, repo, haircut, VIX-term-structure — Investopedia has standalone articles; BabyPips mostly doesn't.

**Practical rule:** use Investopedia when you have a specific term you need defined precisely; use BabyPips when you want a sequenced curriculum on a forex-relevant topic, or any of the free calculators.

---

## Closing assessment

The free BabyPips curriculum is significantly better than its reputation in serious trader circles, and significantly worse than its reputation in retail forums. The middle grades (Elementary through Summer School) are retail folklore and largely a waste of time for someone who already knows what an EMA is. The late undergraduate grades (Junior on COT and sentiment, Senior on risk and position sizing) are the highest-density free trading curriculum on the open web. The Graduation trading-plan structure maps directly onto how a systems trader should specify a bot.

The honest read for an experienced systems trader: skip ~70% of the lesson count, read ~30% in roughly 6-8 hours, lift the Senior-year risk framework and the Junior-year COT/sentiment material into your bot's specification and live guardrails, bookmark the position-size and currency-correlation calculators, and move on. The school is a launchpad, not a destination — its own Graduation Speech says exactly that.

---

## Sources

- [Learn Forex Trading at School of Pipsology](https://www.babypips.com/learn/forex)
- [Preschool](https://www.babypips.com/learn/forex/preschool)
- [Kindergarten](https://www.babypips.com/learn/forex/kindergarten)
- [Elementary](https://www.babypips.com/learn/forex/elementary)
- [Middle School](https://www.babypips.com/learn/forex/middle-school)
- [Summer School](https://www.babypips.com/learn/forex/summer-school)
- [High School](https://www.babypips.com/learn/forex/high-school)
- [Undergraduate Freshman](https://www.babypips.com/learn/forex/undergraduate-freshman)
- [Undergraduate Sophomore](https://www.babypips.com/learn/forex/undergraduate-sophomore)
- [Undergraduate Junior](https://www.babypips.com/learn/forex/undergraduate-junior)
- [Undergraduate Senior](https://www.babypips.com/learn/forex/undergraduate-senior)
- [Graduation](https://www.babypips.com/learn/forex/graduation)
- [Forex Trading Sessions](https://www.babypips.com/learn/forex/forex-trading-sessions)
- [Session Overlaps](https://www.babypips.com/learn/forex/session-overlaps)
- [Three Types of Analysis](https://www.babypips.com/learn/forex/the-big-three)
- [Multiple Time Frame Analysis](https://www.babypips.com/learn/forex/multiple-time-frame-analysis)
- [Time Frame Combinations](https://www.babypips.com/learn/forex/time-frame-combinations)
- [Know Your Market Environment](https://www.babypips.com/learn/forex/trendspotting)
- [Forex Pivot Points](https://www.babypips.com/learn/forex/forex-pivot-points)
- [Pivot Points Summary](https://www.babypips.com/learn/forex/pivot-points-summary)
- [What is a Currency Carry Trade?](https://www.babypips.com/learn/forex/how_do_carry_trades_work_for_forex)
- [What is the Carry Trade?](https://www.babypips.com/learn/forex/what-is-carry-trade)
- [Trade Interest Rate Differential](https://www.babypips.com/learn/forex/taking-advantage-of-interest-rate-differential)
- [Currency Correlation](https://www.babypips.com/learn/forex/what-is-currency-correlation)
- [Intermarket Analysis Cheat Sheet](https://www.babypips.com/learn/forex/intermarket-analysis-cheat-sheet)
- [What Are Currency Crosses?](https://www.babypips.com/learn/forex/what-is-a-currency-cross-pair)
- [Using Crosses to Trade Majors](https://www.babypips.com/learn/forex/how-to-use-crosses-to-trade-the-majors)
- [What Is Market Sentiment?](https://www.babypips.com/learn/forex/what-is-market-sentiment)
- [Sentiment Analysis](https://www.babypips.com/learn/forex/sentimental-analysis)
- [The COT Report](https://www.babypips.com/learn/forex/commitment-of-traders-report)
- [Understanding the COT Report](https://www.babypips.com/learn/forex/understanding-cot-report)
- [How to Interpret the COT Report](https://www.babypips.com/learn/forex/getting-down-and-dirty-with-the-numbers)
- [The COT Trading Strategy](https://www.babypips.com/learn/forex/the-cot-trading-strategy)
- [Summary of Market Sentiment](https://www.babypips.com/learn/forex/summary-of-market-sentiment)
- [What's Risk Control?](https://www.babypips.com/z/learn/forex/what-is-risk-management)
- [Summary Risk Management](https://www.babypips.com/learn/forex/summary-risk-management)
- [Risk Management Plan for Prop Traders](https://www.babypips.com/learn/forex/risk-management-plan-prop-traders)
- [Portfolio Heat](https://www.babypips.com/learn/forex/portfolio-heat-managing-total-risk-exposure)
- [Stop Loss Playbook](https://www.babypips.com/learn/forex/stop-loss-playbook)
- [Position Sizing](https://www.babypips.com/learn/forex/position-sizing)
- [Calculating Position Sizes](https://www.babypips.com/learn/forex/calculating-your-position-sizes)
- [Calculate Position Size Different Pairs](https://www.babypips.com/learn/forex/calculate-position-size-different-forex-pairs)
- [Summary Position Sizing](https://www.babypips.com/learn/forex/summary-position-sizing)
- [What is a Trading Plan?](https://www.babypips.com/learn/forex/what-is-a-trading-plan)
- [Summary Developing a Trading Plan](https://www.babypips.com/learn/forex/summary-developing-a-trading-plan)
- [Reviewing Your Trading Journal](https://www.babypips.com/learn/forex/reviewing-your-trading-journal)
- [Why Traders Fail (5 Deadly O's)](https://www.babypips.com/learn/forex/why-traders-fail)
- [Graduation Speech](https://www.babypips.com/learn/forex/congratulations-you-made-it)
- [Fundamental Analysis](https://www.babypips.com/learn/forex/fundamental-analysis)
- [Top-Down Macro Trade Thesis](https://www.babypips.com/learn/forex/building-a-top-down-fundamental-trade-thesis)
- [Types of Forex Orders](https://www.babypips.com/learn/forex/types-of-orders)
- [Order Types Cheat Sheet](https://www.babypips.com/learn/forex/order-types-cheat-sheet)
- [Leading vs Lagging Indicators](https://www.babypips.com/learn/forex/leading-vs-lagging-indicators)
- [Summary of Leading and Lagging](https://www.babypips.com/learn/forex/summary-leading-and-lagging-indicators)
- [Popular Chart Indicators Summary](https://www.babypips.com/learn/forex/summary-common-chart-indicators)
- [Forex Trading Tools](https://www.babypips.com/tools)
- [Position Size Calculator](https://www.babypips.com/tools/position-size-calculator)
- [Pip Value Calculator](https://www.babypips.com/tools/pip-value-calculator)
- [Currency Correlation Calculator](https://www.babypips.com/tools/currency-correlation)
- [Pivot Point Calculator](https://www.babypips.com/tools/pivot-point-calculator)
- [Forex Market Hours](https://www.babypips.com/tools/forex-market-hours)
- [Risk-On / Risk-Off Meter](https://www.babypips.com/tools/risk-on-risk-off-meter)
- [Forex Economic Calendar](https://www.babypips.com/economic-calendar)
- [MarketMilk](https://marketmilk.babypips.com/)
- [What is MarketMilk](https://support.babypips.com/hc/en-us/articles/26602828855060-What-is-MarketMilk)
- [BabyPips Trading Psychology Articles](https://www.babypips.com/trading/psychology)
- [Understanding Fear and Greed in Trading](https://www.babypips.com/trading/understanding-the-role-of-fear-and-greed-in-trading)
- [4 Stages of Forex Trading Competence](https://www.babypips.com/trading/psychology-4-stages-of-forex-competence-2025-07-09)
