# TradingView — Platform Deep Dive & Signal Source Audit

**Project:** DayTrader bot research
**Author:** research/11
**Date compiled:** 2026-05-14
**Scope:** Is TradingView the right charting/signal layer for a day-trader bot? Which tier? Whose ideas/scripts matter? What's hype vs. edge?

**TL;DR for the boss:**
- Pay for **Premium ($59.95/mo)** — the alert ceiling (400/400) and 8 charts-per-tab are the only tiers that survive contact with a real day-trading workflow. Plus is a trap; Essential is a toy.
- Add **CME real-time data ($7/mo)** if any futures are in scope. Non-negotiable.
- **Use TradingView for charts, alerts, and Pine Script research — not for execution.** Route alerts via webhook to the bot; place orders through a broker API (IBKR, Tradovate, Tradier, Alpaca) or, for futures, a dedicated futures platform.
- **Stop following "ideas."** Follow a tight short list of practitioners with documented track records: Adam Mancini (ES levels), Brian Shannon (Anchored VWAP), Stockbee (momentum bursts), Tom Hougaard (psychology, not signals), Cem Karsan (vol regime, not chart calls). Almost everyone else on the platform is noise.
- The **only indicators with real edge in studies** are Anchored VWAP, Volume Profile (VPVR + Session), CVD, RVOL, and ATR for risk sizing. Everything else is decoration.
- **LuxAlgo/ChartPrime are not edge** — they're well-coded UX wrappers around standard signals. Backtest claims of 70% win rate are cherry-picked.

---

## Section A: TradingView Platform — What to Pay For

### Plan structure (as of 2026)

| Plan | Price/mo | Charts/tab | Indicators/chart | Price alerts | Server-side | Alert expiry |
|---|---|---|---|---|---|---|
| Free / Basic | $0 | 1 | 2 | 1 | Yes (limited) | 2 months |
| Essential | $14.95 | 2 | 5 | 20 | Yes | 2 months |
| Plus | $29.95 | 4 | 10 | 100 | Yes | 2 months |
| **Premium** | **$59.95** | **8** | **25** | **400** | **Yes** | **Never expires** |
| Ultimate | $199.95 | 16 | 50 | 1,000 | Yes | Never |

Notes:
- All paid plans run alerts server-side — the laptop can be closed.
- "No-expiry alerts" lives only on Premium/Ultimate. For a bot, you want a level set on SPX 5,600 to fire 7 months later without manual refresh. That alone justifies Premium.
- The "Pro/Pro+" labels referenced in older docs were renamed to Essential/Plus/Premium in the 2024 rebrand.

### Free tier — useful for what, useless for what

Useful: discovery, watching one chart, manually scrolling Pine scripts.
Useless: any serious workflow. 1 indicator per chart kills any multi-confirmation setup. 1 alert means you can watch SPY's VWAP or QQQ's VWAP — not both.

### Essential ($14.95) — the upsell trap

5 indicators per chart sounds fine until you stack VWAP + 20EMA + 50EMA + Bollinger + Volume Profile and you've already burned them all on a single timeframe. 20 alerts dies within a week if you're scanning a watchlist of 20 tickers. **Skip.**

### Plus ($29.95) — the middle child

100 alerts and 4 charts/tab is workable for a swing trader. For an active intraday bot scanning 30+ tickers across HTF/MTF/LTF panes, it hits the wall fast. Most professional reviewers ([newtrading.io](https://www.newtrading.io/tradingview-free-vs-paid/), [mindmathmoney.com](https://www.mindmathmoney.com/articles/tradingview-plans-compared-free-vs-essential-vs-plus-vs-premium-vs-ultimate-2025-guide)) recommend either Essential or Premium and skipping Plus.

### Premium ($59.95) — the actual answer for this project

What you actually unlock:
- **400 price alerts + 400 technical alerts** — enough for a 100-ticker watchlist with multi-level confluence (PDH/PDL, VWAP cross, ORB break)
- **8 charts per tab** — true HTF/MTF/LTF/execution grid plus three related symbols (e.g., ES/NQ/RTY/YM)
- **Alerts that never expire** — critical for swing levels, weekly opening range, monthly reference levels
- **Custom resolutions, second-based intervals** for high-frequency setups
- **Volume Footprint indicator** (added 2024) — a real footprint approximation, not just colored bars
- **20K bars of historical data** for backtesting Pine strategies further back

### Ultimate ($199.95) — overkill unless multi-account

Mostly relevant for prop firms or someone running 15+ scripts on a single chart. The boss does not need this.

### Real-time data add-ons

Charting plan ≠ data feed. Free CME data is **10-minute delayed**, which is useless for intraday futures. The $7/mo CME futures add-on (covers ES, NQ, RTY, CL, GC, ZB, ZN) is the cheapest serious-trader expense on the platform.
- Equities are real-time on US exchanges through most plans by default
- If a Tradovate, AMP, or IBKR account is linked, you may get the data free as a brokered customer ([TradingView data sources](https://www.tradingview.com/support/solutions/43000479666))

### Honest verdict for this project

**Premium ($59.95) + CME real-time ($7) = $66.95/mo.** Anything less is friction. Anything more is wasted budget.

---

## Section B: TradingView for Day Trading — Features That Move the Needle

### Multi-chart layout (HTF/MTF/LTF/execution)

The most underused power feature. A 4-pane layout, symbols synced:
- **Top-left (main / mobile fallback):** the execution chart (1m or 5m of the traded symbol)
- **Top-right:** MTF (15m or 1h) — the trend frame
- **Bottom-left:** HTF (daily) — for prior day H/L, VWAP, and trend context
- **Bottom-right:** related symbol or breadth (e.g., trade SPY here? Show ES, VIX, MOAT/IWM correlation)

Symbol sync, time sync, crosshair sync, and interval sync are independent toggles in the layout dropdown. Crosshair sync OFF + symbol sync OFF is the standard for the layout above. TradingView's [official guide](https://www.tradingview.com/support/solutions/43000629990-leveraging-multi-chart-layouts-in-your-analysis/) is the right reference.

**Critical:** the top-left chart is what the mobile app shows. Make it the execution chart, not the daily.

### Bar Replay — the single highest-ROI feature

Bar Replay lets you scroll back to any historical bar and step forward one bar at a time, with future data hidden. It is the closest thing to a flight simulator a discretionary trader has.

How to use it for the bot project:
1. Pick a setup the bot will trade (e.g., "ES breaks ORB high with RVOL > 1.5 on the breakout bar")
2. Replay 50–100 historical occurrences manually
3. Mark each entry, where stop got hit (or didn't), where target got hit (or didn't)
4. Build the rule set from observation, not theory

Limits: free plan only supports daily+ in replay. Essential gives 6 weeks of 1-minute replay history. Premium extends it. ([A1 Trading guide](https://www.a1trading.com/the-complete-guide-to-tradingview-bar-replay-for-backtesting/))

### Strategy Tester (Pine Script backtester)

The Pine Script Strategy Tester is fine for sanity-checking ideas — **not for production performance numbers**. Known issues:
- Repaints on `request.security()` calls if not careful
- Lookahead bias if `barstate.isconfirmed` not used
- Slippage and fill assumptions are optimistic
- Order types are simplified

**Verdict:** use Strategy Tester to get a rough shape of the equity curve, then validate manually with Bar Replay before trusting anything. Anyone showing you a 5-year backtest with no walk-forward and no slippage model is selling something.

### Drawing tools that matter

Pareto applies — 5 tools cover 90% of work:
1. **Anchored VWAP** (right-click → drawing toolbar). Anchor to: prior day high/low, earnings, IPO, swing high/low, news event.
2. **Long/Short Position** — visual R-multiple planner. Drag to set entry, stop, target; tells you R and dollar P&L. The fastest discipline tool on the platform.
3. **Fixed Range Volume Profile (FRVP)** — drag across any range, get the volume distribution. Better than the "Volume Profile Visible Range" indicator for ad-hoc analysis.
4. **Pitchfork (Andrews)** — only useful for medium-term trends; mostly skippable for day trading.
5. **Horizontal Ray** — for marking PDH, PDL, ON-high, ON-low, swing pivots. Don't use full horizontal lines (clutters off-screen).

### Pine Script for custom indicators / strategies

Pine v5/v6 is a domain-specific language, not a real programming language — but it's good enough for chart indicators and basic strategies. Key limits:
- Single-threaded per chart
- Can't make outbound HTTP requests (no external data joins)
- Limited array/matrix operations
- Repaints are easy to introduce, hard to debug

**For the bot:** use Pine to *visualize signals on chart*. Don't run the bot logic inside Pine. Compute signals in Python/Rust, send to TradingView only for visualization OR receive alerts via webhook → bot.

Webhook setup is well documented ([TradingView webhook docs](https://www.tradingview.com/support/solutions/43000529348-how-to-configure-webhook-alerts/)). The standard pattern: Pine indicator computes a signal, raises `alert()`, alert ships JSON payload to your bot's HTTPS endpoint, bot executes through broker.

---

## Section C: The 10 Indicators That Actually Have Edge

There are 100,000+ Pine scripts. Maybe 15 have edge. The rest are autocorrelated noise dressed up.

| # | Indicator | What it is | Where the edge actually comes from | Verdict |
|---|---|---|---|---|
| 1 | **Anchored VWAP** | Volume-weighted average price from a chosen anchor point | Institutional execution algos benchmark to VWAP — it becomes self-fulfilling support/resistance | **Tier 1 — essential** |
| 2 | **Session VWAP + bands** | Daily-reset VWAP with 1σ/2σ bands | Fade plays at 2σ work statistically in mean-reverting regimes | **Tier 1** |
| 3 | **Volume Profile Visible Range (VPVR)** | Horizontal volume histogram | Point of Control and HVN/LVN are real liquidity levels | **Tier 1** |
| 4 | **Cumulative Volume Delta (CVD)** | Net buy-minus-sell volume, accumulated | Divergence between price and CVD = absorption signal. *Note: TradingView CVD uses intrabar tick estimation, not true tape* | **Tier 1, with caveat** |
| 5 | **ATR (14)** | Average True Range | The ONLY honest way to size stops for the regime | **Tier 1 — for risk, not entry** |
| 6 | **RVOL (relative volume)** | Today's volume / average for this time-of-day | The single best filter for "is this real or is this nothing?" | **Tier 1** |
| 7 | **20/50/200 EMA** | Standard exponential MAs | Pure bias filter. Don't trade off crosses. Use as regime context. | **Tier 2 — bias only** |
| 8 | **Bollinger Bands (20, 2σ)** | Std-dev envelope around 20SMA | Context for vol expansion/contraction. The "squeeze" is a real setup. | **Tier 2** |
| 9 | **Footprint (Volume Candles, Premium)** | Bid/ask volume per price level inside each candle | Real order-flow proxy — but TradingView's version is approximate. For true footprint use Sierra/Bookmap. | **Tier 2 — useful if Premium** |
| 10 | **TPO / Market Profile** | Time-at-price distribution | Identifies value area, balance, breakouts from balance | **Tier 2 — requires study to use** |

### Indicators to actively avoid

- **RSI, Stochastic, MACD as buy/sell signals** — autocorrelated lagging junk in isolation
- **Ichimoku Cloud** — works occasionally but the 5-line clutter destroys clarity
- **Supertrend** — fits past data beautifully, whipsaws live
- **Any "AI-powered" buy/sell arrow indicator** — by construction, anything showing arrows is either repainting or curve-fit

### LuxAlgo / ChartPrime / Profitable Pip — honest review

**LuxAlgo** (~$50/mo) and **ChartPrime** (~$67/mo) are the two big paid indicator suites on TradingView. Both have legitimate code quality. Neither has independent edge.

What they actually are: well-packaged versions of standard concepts — supply/demand zones, order blocks, fair value gaps, market structure breaks. The "70% win rate" backtests circulating are:
- Cherry-picked timeframes and instruments
- Use look-ahead bias in some signal flavors
- Don't account for slippage, missed fills, or partial fills

**LuxAlgo's free library** ([200+ open-source indicators](https://www.tradingview.com/u/LuxAlgo/)) is genuinely useful and well-coded — that's the way to consume their work without paying. ChartPrime has fewer free offerings.

**Verdict:** if the boss wants pretty signal overlays for visualization, LuxAlgo Premium ($50) is fine. **Do NOT route the bot's decision-making through these.** The edge is in market structure understanding, not in the signal package.

---

## Section D: TradingView Community Accounts — Signal-to-Noise Ranking

**Caveat first:** TradingView removed its "accuracy rank" feature in 2022 because it was getting gamed. Almost all "top trader" rankings now are popularity, not performance. Treat anyone with a follower count and no PnL screenshots as marketing, not signal.

### Tier 1 — Follow (substantive content, transparent process)

**Adam Mancini (@AdamMancini4)** — ES intraday futures.
- Daily Substack newsletter with explicit support/resistance levels for ES
- Trades fully transparently — three setups (flag breakouts, fake breakdowns, trendline retests)
- Multiple community Pine indicators auto-plot his levels ([ZawTrader's "Adam Mancini ES Levels"](https://www.tradingview.com/script/nfHjTWnI-Adam-Mancini-ES-Levels/))
- For an ES/SPX bot, his levels are the cleanest input on the platform
- Subscription: ~$65/mo Substack. Worth it for ES traders.

**Brian Shannon (Alphatrends)** — Anchored VWAP authority.
- Wrote "Maximum Trading Gains With Anchored VWAP" (2022, CMT Association distributed)
- Methodology: anchor VWAPs to meaningful events (earnings, IPOs, news, swing pivots) — they become self-fulfilling S/R
- Multiple Pine community indicators in his name
- He doesn't post daily ideas on TradingView itself, but the methodology is everywhere on the platform

**Stockbee (Pradeep Bonde)** — Momentum bursts.
- Blog: stockbee.blogspot.com — 15+ years of momentum trading content
- Method: identify range expansion ON DAY 1 of a 3-5 day momentum burst, exit before exhaustion
- Cardinal rule: "Never buy after 3+ consecutive up days"
- Multiple Pine community indicators implementing his scans
- Signal is swing, not intraday — but the scan logic is reusable

### Tier 2 — Useful context (read, don't copy trades)

**Cem Karsan (@jam_croissant)** — Volatility regime, dealer positioning, 0DTE flows.
- Founder, Kai Volatility Advisors. 26 years vol/quant background.
- Doesn't post chart ideas — posts vol regime commentary
- Critical context for "is today a vol expansion or compression day"
- His "vanna/charm" flows analysis is the best public-facing dealer-flow explanation
- Twitter/X is the primary channel; TradingView is secondary

**Tom Hougaard (TraderTom)** — Psychology, not signals.
- Author "Best Loser Wins" (the single most useful trading psychology book of the last decade)
- Trades DAX live on YouTube; not a TradingView idea-poster
- Read him for the mental game, not for setups

**Linda Raschke** — Veteran swing/intraday trader. Multiple books ("Street Smarts"). Some setups (Holy Grail pullback, Turtle Soup reversal) are still cited. Not actively posting on TradingView.

### Tier 3 — Famous but mixed signal

Big-follower TradingView accounts like **AlanSantana** (140K+ followers, mostly crypto chart pattern calls) generate engagement, not edge. Read for entertainment, not execution.

### SKIP — popularity ≠ skill

- Anyone selling a "signals service" subscription via TradingView ideas
- Anyone with "guru," "master," "wizard" in handle
- Anyone showing only winning screenshots, no equity curve
- Anyone whose past calls aren't searchable in their feed (i.e. they delete losers)

### How to evaluate a TradingView idea-poster in 5 minutes

1. Click their profile → "Ideas" tab → sort by date ascending (oldest first)
2. Are old calls still there or have they been pruned?
3. Of the calls visible 1+ year ago, were the targets actually hit before stops?
4. Do they post during open hours with timestamps, or only post analysis after the move?
5. Do they show a verified broker statement anywhere on profile/website?

If 3 out of 5 fail → unfollow.

---

## Section E: TradingView Ideas Section — Friend or Trap?

### Editors' Picks

TradingView's [Editors' Picks](https://www.tradingview.com/ideas/editors-picks/) is curated by PineCoders staff. The selections favor educational quality over signal predictability — they're picked for novel chart annotation, clear methodology explanation, or interesting Pine code, not for "this trade will win."

**Useful for:** learning how experienced chart annotators think.
**Useless for:** "what should I trade tomorrow?"

### The structural problem with TradingView Ideas

Most idea posts are **published after the move started**. The platform has no enforced timestamp-before-entry mechanism. By the time an idea trends, the move it predicted is usually 30-60% complete or done. This is the "after-the-fact narrative" trap — chart looks obvious in hindsight, idea reads like genius.

**The 1-hour rule:** if a published idea is on a timeframe where the predicted move would already be in motion within an hour of the post, don't trade it. The author is documenting, not predicting.

### Pine Script community — the actual value

Where TradingView genuinely shines: the open-source Pine library. Worth knowing:

- **LuxAlgo's free library** — 200+ open-source indicators including market structure, liquidity, FVG. Best free toolkit on the platform.
- **PineCoders** — official PineCoders org publishes well-maintained reference scripts and libraries
- **ZenAndTheArtOfTrading** — high-quality educational scripts with clean code
- **TradingView's first-party scripts** — VWAP, Volume Profile, Bollinger, etc. — well-documented and reliable

### The over-stacking trap

Five clean indicators beats 15 messy ones. A common failure mode:
- Trader stacks VWAP + 20EMA + 50EMA + RSI + Stoch + MACD + Bollinger + Ichimoku + Supertrend + 3 LuxAlgo overlays
- Now every bar has a "signal" of some kind, every direction
- Trader cherry-picks confirmation post-hoc and calls it strategy
- Net result: random execution under the guise of "confluence"

**Rule for the bot:** ≤7 indicators per chart, each with a defined role (bias / level / trigger / risk / filter). If a new indicator doesn't displace an existing one, don't add it.

---

## Section F: TradingView vs. The Alternatives

| Feature | TradingView | ThinkOrSwim | Sierra Chart | NinjaTrader |
|---|---|---|---|---|
| **Charting quality** | Best-in-class, cloud, fast | Excellent, desktop-bound | Excellent, dense | Good, dated UI |
| **Order entry** | Via broker integrations only | Native (Schwab) | Native (multiple FCMs) | Native (NT Brokerage + others) |
| **Real footprint chart** | Approximate (Volume Candles) | Limited | **Yes, real** | **Yes, real** |
| **DOM ladder** | Basic | Yes | **Excellent** | **Excellent** |
| **Order flow tools** | CVD, basic | Limited | **Best-in-class** | Strong |
| **Scripting language** | Pine Script | ThinkScript | ACSIL (C++) | NinjaScript (C#) |
| **Broker integrations** | Many (~100) | Schwab only | Many FCMs | NT Brokerage + many |
| **Cost** | $0–$60/mo | Free w/ Schwab | $26–$160/mo | Free w/ NT broker, license otherwise |
| **Cloud / multi-device** | Yes | Limited | No (desktop only) | No (desktop only) |
| **Mobile** | Best mobile experience | Decent | Poor | Poor |
| **Best for** | Equities, crypto, swing, multi-device | Options, equities | **Futures scalping, order flow** | **Futures, automation, NT8 strategies** |

### When TradingView wins

- Equities and crypto charts
- Idea sharing, Pine Script research, community signals
- Anyone who wants charts on phone + tablet + multiple machines
- Anyone running a webhook-driven bot off chart-based signals
- Quick chart pattern visualization across many symbols

### When TradingView loses

- True footprint / orderflow scalping (use Sierra or Bookmap)
- Latency-sensitive futures execution (use Sierra/NinjaTrader/Rithmic)
- Heavy automated systematic strategies (use NinjaTrader, MultiCharts, or custom Python)
- Professional options chains and analytics (use ThinkOrSwim)

### Recommended stack for this project

- **Charting + alerts + Pine research:** TradingView Premium ($60) + CME data ($7)
- **Execution + true orderflow (if futures):** Sierra Chart ($36/mo Standard) OR NinjaTrader Free w/ NT Brokerage
- **Equities execution:** broker of choice via TradingView integration OR direct API (IBKR, Tradier, Alpaca)
- **Options analytics:** ThinkOrSwim free (no Schwab account required for paperMoney)

Total monthly: ~$70-100 depending on Sierra/NinjaTrader choice.

---

## Section G: The Recommended Workflow on TradingView

### 1. The single combined chart layout

Build it once, save it, never rebuild. The layout:

```
+--------------------+--------------------+
|  HTF: Daily        |  Symbol watchlist  |
|  Symbol            |  + correlation     |
|  20/50/200 EMA     |  (ES/NQ/RTY/VIX)   |
|  Anchored VWAPs    |                    |
|  PDH/PDL/PWH/PWL   |                    |
+--------------------+--------------------+
|  MTF: 15m          |  LTF: 1m/5m        |
|  Symbol            |  EXECUTION CHART   |
|  Session VWAP      |  Session VWAP      |
|  Volume Profile    |  VPVR              |
|  ATR (regime)      |  RVOL              |
+--------------------+--------------------+
```

Symbol sync ON, interval sync OFF, crosshair sync ON.

### 2. The minimal indicator stack (max 7 per chart)

For the **execution chart**:
1. Session VWAP + 1σ/2σ bands
2. Anchored VWAP from prior day high/low (2 anchors)
3. VPVR (visible range)
4. RVOL
5. 20 EMA
6. ATR (in a sub-pane)
7. CVD (in a sub-pane)

For the **HTF chart**:
1. 20/50/200 EMA
2. Anchored VWAP from year start, last earnings, last major swing
3. Horizontal rays at PDH/PDL/PWH/PWL/PMH/PML

### 3. Alert architecture (Premium tier)

Tier 1 alerts (always on, never expire):
- Price touches PDH / PDL on traded symbol
- Price crosses session VWAP (both directions)
- Price touches 200 EMA on daily
- RVOL > 1.5 on a 5m bar (per traded symbol)

Tier 2 alerts (set daily based on Mancini levels or own pre-market plan):
- Specific intraday support/resistance touches
- Opening Range Breakout (ORB) high/low cross

Tier 3 alerts (event-driven):
- Earnings dates (cross-reference earnings calendar)
- Economic calendar high-impact events ±15min windows

For the bot: route Tier 1 alerts to a webhook the bot consumes. Tier 2/3 can be human-confirmed.

### 4. Daily routine on TradingView

**Pre-market (1 hour before open):**
1. Open Bar Replay on yesterday's session, scroll to open, replay the first 2 hours
2. Mark today's PDH/PDL/POC on the chart
3. Pull Adam Mancini's levels from his Substack, plot as horizontal rays
4. Check the [TradingView economic calendar](https://www.tradingview.com/economic-calendar/) for the day's high-impact events (Fed speakers, CPI, NFP, PMI)
5. Check the [earnings calendar](https://www.tradingview.com/earnings-calendar/) for movers in the watchlist
6. Set 5-10 fresh price alerts based on the level confluence

**During session:**
- Don't add indicators. Don't draw new lines. Work the plan that was set.
- Only acknowledge alerts that have multi-factor confluence (e.g., PDH touch + RVOL > 1.5 + Session VWAP > 2σ below)

**Post-session:**
- Mark every trade taken on the chart, save snapshot
- Tag setup type, R-multiple result
- Weekly: review snapshots grouped by setup, prune the ones with negative expectancy

### 5. Economic + earnings calendar usage

TradingView's economic calendar covers 300,000+ indicators across 190 countries. The useful filters: country (US only for SPX/ES day-trader), importance (high only), time window (today + tomorrow). The earnings calendar is integrated into the chart — earnings markers appear directly on the daily chart of any equity.

Practical rule: **no new positions opened within ±15 minutes of a high-impact release** unless the strategy is explicitly news-driven.

---

## Final Verdict for the Bot Build

**Use TradingView for:**
- All chart analysis and visualization
- Alert generation → webhook → bot
- Pine Script signal prototyping
- Following a TIGHT short list of signal sources (Mancini for ES levels, Shannon for AVWAP methodology, Stockbee for momentum scans, Karsan for vol context)
- Economic + earnings calendar integration

**Do NOT use TradingView for:**
- Order execution (use broker API)
- True orderflow / footprint analysis (use Sierra/Bookmap if needed)
- Backtest validation in isolation (Pine Strategy Tester has known repaint/lookahead issues)
- Sourcing trade ideas from the public "Ideas" feed

**Spend:**
- TradingView Premium: $59.95/mo
- CME real-time data: $7/mo (if futures in scope)
- Optional: Adam Mancini Substack ($65/mo) if ES is a primary instrument
- Optional: LuxAlgo Premium ($50/mo) for visualization only — NOT for decisions
- Skip: Plus tier, Ultimate tier, ChartPrime, "signal services," any "AI buy/sell arrow" indicator

**The discipline that matters more than the platform:**
- 7 indicators max per chart
- Every indicator has a defined role
- Backtest via Bar Replay manually, not via Strategy Tester alone
- Alerts > screen-watching
- Process from idea posters: filter ruthlessly, distrust anyone selling subscriptions to signals

---

## Sources

**Pricing & plans**
- [TradingView Pricing](https://www.tradingview.com/pricing/)
- [TradingView Plans 2026 (Supa)](https://supa.is/article/tradingview-essential-vs-plus-vs-premium-which-plan-2026)
- [TradingView Plans Compared (Mind Math Money)](https://www.mindmathmoney.com/articles/tradingview-plans-compared-free-vs-essential-vs-plus-vs-premium-vs-ultimate-2025-guide)
- [Are TradingView Plans Worth It? (NewTrading)](https://www.newtrading.io/tradingview-free-vs-paid/)
- [Best TradingView Plan for Bots (Tickerly)](https://tickerly.net/best-tradingview-plan/)

**Real-time data**
- [TradingView Market Data Coverage](https://www.tradingview.com/data-coverage/)
- [How to purchase additional market data](https://www.tradingview.com/support/solutions/43000471705-how-to-purchase-additional-market-data/)
- [TradingView Real-Time Data Cost (FinancialTechWiz)](https://www.financialtechwiz.com/post/tradingview-real-time-data/)

**Platform features**
- [Multi-chart layouts](https://www.tradingview.com/support/solutions/43000629990-leveraging-multi-chart-layouts-in-your-analysis/)
- [Bar Replay how & why](https://www.tradingview.com/support/solutions/43000712747-bar-replay-how-and-why-to-test-a-strategy-in-the-past/)
- [Complete Guide to Bar Replay (A1 Trading)](https://www.a1trading.com/the-complete-guide-to-tradingview-bar-replay-for-backtesting/)
- [Webhook alerts configuration](https://www.tradingview.com/support/solutions/43000529348-how-to-configure-webhook-alerts/)
- [Webhooks for Alerts launch post](https://www.tradingview.com/blog/en/webhooks-for-alerts-now-available-14054/)

**Indicators**
- [Anchored VWAP drawing tool](https://www.tradingview.com/support/solutions/43000669764-anchored-vwap/)
- [VWAP scripts library](https://www.tradingview.com/scripts/vwap/)
- [Cumulative Volume Delta](https://www.tradingview.com/support/solutions/43000725058-cumulative-volume-delta/)
- [Volume Profile scripts](https://www.tradingview.com/scripts/volumeprofile/)
- [Brian Shannon — Maximum Trading Gains With Anchored VWAP (CMT)](https://cmtassociation.org/wp-content/uploads/2024/01/Shannon-Specific-Anchored-VWAP-Strategies-1.pdf)
- [Alphatrends — Master the Anchored VWAP Strategy](https://alphatrends.net/anchored-vwap/)

**Signal sources / accounts**
- [Adam Mancini Substack (Trade Companion)](https://tradecompanion.substack.com/)
- [Adam Mancini X profile](https://x.com/adammancini4)
- [Adam Mancini ES Levels indicator (TradingView)](https://www.tradingview.com/script/nfHjTWnI-Adam-Mancini-ES-Levels/)
- [Stockbee blog](https://stockbee.blogspot.com/)
- [Stockbee Momentum Pro (TradingView script)](https://in.tradingview.com/script/njlDpagc-Pradeep-Bonde-Stockbee-Momentum-Pro/)
- [Cem Karsan X profile](https://x.com/jam_croissant)
- [Tom Hougaard — Best Loser Wins](https://www.amazon.com/Best-Loser-Wins-Thinking-high-stake/dp/085719822X)
- [SMB Capital](https://smbcap.com/)

**Indicator suites**
- [LuxAlgo TradingView profile](https://www.tradingview.com/u/LuxAlgo/)
- [LuxAlgo Library](https://www.luxalgo.com/library/)
- [LuxAlgo Review (QuantVPS)](https://www.quantvps.com/blog/luxalgo-review)
- [ChartPrime](https://chartprime.com/)
- [ChartPrime Review (Lunefi)](https://lunefi.com/blog/chartprime-review-pros-cons-pricing-tradingview-comparison)
- [Free vs Paid TradingView Scripts](https://signals.coincodecap.com/free-vs-paid-tradingview-pine-scripts-vs-luxalgo-vs-indicator-vault)

**Calendars**
- [TradingView Economic Calendar](https://www.tradingview.com/economic-calendar/)
- [TradingView Earnings Calendar](https://www.tradingview.com/earnings-calendar/)
- [Economic Calendar guide](https://www.tradingview.com/support/solutions/43000759911-economic-calendar-track-all-major-market-events/)

**Platform comparisons**
- [Best Futures Trading Platforms (Phidias)](https://phidiaspropfirm.com/education/futures-trading-platforms)
- [Top 10 Futures Trading Platforms (QuantVPS)](https://www.quantvps.com/blog/futures-trading-platforms)
- [Best TradingView Alternatives (TrendSpider)](https://trendspider.com/learning-center/tradingview-alternative/)
- [TradingView vs NinjaTrader (XABCD)](https://www.xabcdtrading.com/blog/tradingview-vs-ninjatrader/)
- [NinjaTrader vs ThinkOrSwim](https://affordableindicators.com/articles/ninjatrader-vs-thinkorswim-which-platform-is-better-for-futures-traders/)
- [TradingView Review (StockBrokers)](https://www.stockbrokers.com/review/tools/tradingview)
