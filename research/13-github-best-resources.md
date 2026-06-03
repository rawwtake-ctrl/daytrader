# GitHub Best Resources for Day Trading & Algorithmic Trading (Python)

**Compiled:** 2026-05-15
**Focus:** Free open-source tools for an ES/NQ futures + equities day-trading bot in Python. Zero budget. Stars verified via direct GitHub fetches and recent web sources. Star counts and release dates as of May 2026.

> NOTE: GitHub stars are a signal, not the truth. A 20k-star project written in 2017 that hasn't shipped a release in two years is a museum piece. I weighted star count × release recency × commit cadence × actual fit-for-purpose for futures intraday work. Several "famous" libraries are flagged honestly as DEAD or PAYWALLED-IN-DISGUISE.

---

## Category A — Backtest Frameworks

### A1. NautilusTrader — **TOP PICK FOR THIS PROJECT**

| Name | Stars | Last release | Maintenance | Use case for our bot | Top alternative |
|------|-------|--------------|-------------|----------------------|-----------------|
| NautilusTrader | 22.7k | v1.226 Beta (Apr 29, 2026) | Bi-weekly releases, very active | Unified backtest + paper + live for ES/NQ. Nanosecond-resolution event-driven engine. Same strategy code runs in sim and prod. | Lumibot (simpler), Lean (more mature) |

URL: https://github.com/nautechsystems/nautilus_trader

**Why this is #1 for your boss:** Rust core, Python control plane. Multi-venue, multi-asset, futures-native. Bi-weekly releases is institutional cadence for OSS. Time-in-force IOC/FOK/GTC/GTD/DAY/AT_THE_OPEN/AT_THE_CLOSE matters for intraday execution — most "toy" frameworks don't model these correctly. License: LGPL-3.0.

**Honest cons:** Steep learning curve. Documentation is dense. You will spend the first two weeks reading source. Backtest API is not pandas-friendly out of the box — Nautilus expects event streams, not vectors.

### A2. Lean (QuantConnect)

| Name | Stars | Last release | Maintenance | Use case | Top alternative |
|------|-------|--------------|-------------|----------|-----------------|
| QuantConnect/Lean | 19k | Active (240 open issues, 10 PRs) | Backed by QuantConnect Inc., very active | Polished platform, cloud + local backtest, Python wrapper exists | NautilusTrader |

URL: https://github.com/QuantConnect/Lean | CLI: https://github.com/QuantConnect/lean-cli

**Honest take:** Core is **94% C#**, only 5.7% Python. You're writing in a Python wrapper that calls C#. Free locally; QuantConnect's hosted version is paid. For a Python-first developer this is friction.

### A3. backtesting.py — **Best for Quick Prototyping**

| Name | Stars | Last release | Maintenance | Use case | Top alternative |
|------|-------|--------------|-------------|----------|-----------------|
| kernc/backtesting.py | 8.4k | Active, 58 open issues, 19 PRs | Active | Single-file ish, fast iteration for strategy ideas. Bokeh-based interactive output. | vectorbt for multi-asset |

URL: https://github.com/kernc/backtesting.py

**Use for:** Day-1 throwaway tests on a strategy idea. Not for production. No multi-asset, no real futures contract specs, no live trading.

### A4. vectorbt (community edition)

| Name | Stars | Last release | Maintenance | Use case | Top alternative |
|------|-------|--------------|-------------|----------|-----------------|
| polakowo/vectorbt | 7.5k | v1.0.0 (Apr 22, 2026) | Active but limited (free edition) | Vectorized speed for parameter sweeps across thousands of permutations | nautilus for prod |

URL: https://github.com/polakowo/vectorbt

**Honest take:** The free version is the **community edition**. License is "Apache 2.0 with Commons Clause" — meaning you cannot resell software using it. **vectorbt PRO is a paid product** (~$400/year subscription range historically). The free version is fine for personal use but is increasingly a marketing funnel for PRO. Vectorized = blazing fast for grid-search but harder to express event-driven logic (e.g., "if order filled, then place stop" — requires workarounds).

### A5. backtrader — **STUDY, DON'T BUILD ON**

| Name | Stars | Last release | Maintenance | Use case | Top alternative |
|------|-------|--------------|-------------|----------|-----------------|
| mementum/backtrader | 21.5k | Last meaningful update ~2018, sporadic PR merges 2026 | Effectively abandoned by original author | Reference code patterns only. Do not start new projects here. | NautilusTrader, Lumibot |

URL: https://github.com/mementum/backtrader

**Honest take:** This is the most over-recommended Python backtester on the internet. **Active development effectively stopped around 2018.** The 21.5k stars are legacy from when it was the only game in town. There are forks (smalinin/backtrader_next ships releases through 2026, cloudQuant/backtrader has performance forks) but the canonical repo is a museum.

**Verdict:** Star count is a trap. AVOID for greenfield builds. Read its source for elegant indicator/strategy abstractions; do not deploy in 2026.

### A6. Zipline — **DEAD-ish**

| Name | Stars | Last release | Maintenance | Use case | Top alternative |
|------|-------|--------------|-------------|----------|-----------------|
| quantopian/zipline | 19.8k | v1.4.1 (Oct 2020) | Quantopian shut down; minimal activity | Historic reference, US equities only, daily bars only | Anything in this list |

URL: https://github.com/quantopian/zipline

**Honest take:** Quantopian (the company) shut down in 2020. README explicitly says "we may not attend to your pull request, issue, or direct mention in months, or even years." Zipline was built for Quantopian's hosted environment; the open-source version is hard to set up cleanly with modern data sources. **Avoid for new projects.** A community fork called `zipline-reloaded` (stefan-jansen) is more usable, but for a futures bot it's still the wrong tool.

### A7. Lumibot — **STRONG #2 ALTERNATIVE FOR THIS PROJECT**

| Name | Stars | Last release | Maintenance | Use case | Top alternative |
|------|-------|--------------|-------------|----------|-----------------|
| Lumiwealth/lumibot | 1.5k | v4.5.22 (May 15, 2026) | Very active, daily commits | "Write once deploy anywhere" — backtest + paper + live across Alpaca, IBKR, Tradovate, TopstepX (ProjectX). Futures-native. | NautilusTrader |

URL: https://github.com/Lumiwealth/lumibot

**Why this matters for your project:** Lumibot has **official Tradovate and TopstepX integrations**. If your boss plans to trade prop firm funded accounts (Topstep) or directly with Tradovate brokerage, this is a massive head start. Far lower learning curve than Nautilus.

**Honest cons:** Only 1.5k stars (younger project), built by a real company (Lumiwealth) which sells trading courses — there's a soft commercial angle. Code quality is good but not as battle-tested as Nautilus.

### A8. freqtrade / jesse — **Reference only (crypto-only)**

| Name | Stars | Last release | Maintenance | Notes |
|------|-------|--------------|-------------|-------|
| freqtrade/freqtrade | 50.4k | 2026.4 (Apr 30, 2026) | Very active | Crypto only. Plugin architecture is elegant; study for code patterns. |
| jesse-ai/jesse | 7.9k | Active | Active | Crypto only. Similar — DEX support, multi-symbol. |

URLs: https://github.com/freqtrade/freqtrade | https://github.com/jesse-ai/jesse

These do not trade ES/NQ futures. Listed for completeness — their architectural patterns are excellent reference material for strategy + execution + risk module separation.

### Backtest Framework Ranking (honest)

| Rank | Framework | Speed | Learning curve | Futures | Slippage modeling | Custom data | Community |
|------|-----------|-------|----------------|---------|-------------------|-------------|-----------|
| 1 | NautilusTrader | Excellent | Steep | Native | Excellent | Excellent | Growing fast |
| 2 | Lumibot | Good | Easy | Native | Decent | Easy | Smaller |
| 3 | Lean | Very good | Moderate-Steep | Native | Excellent | Moderate | Large |
| 4 | vectorbt (free) | Excellent vectorized | Moderate | Workable | Decent | Easy | Forked into paid PRO |
| 5 | backtesting.py | Good | Very easy | Limited | Basic | Easy | Active |
| 6 | backtrader | Moderate | Easy | Workable but dated | Decent | Easy | Stagnant |
| 7 | zipline | Slow | Moderate | Poor | Decent | Painful | Dead |

---

## Category B — Data Sources / Free Python Clients

### B1. yfinance — **Use for free historical, NOT real-time**

| Name | Stars | Last release | Maintenance | Real-time? | Futures? |
|------|-------|--------------|-------------|------------|----------|
| ranaroussi/yfinance | 23.7k | v1.3.0 (Apr 2026) | Active, 109 releases | **15-min delayed** (Yahoo terms) | Yes (e.g. `ES=F`, `NQ=F`) but delayed |

URL: https://github.com/ranaroussi/yfinance

**Honest take:** Yahoo Finance's terms restrict commercial use. Free for personal research. Use for: historical bars, backtests, sanity checks. **Do NOT use for live execution signals.** v1.3.0 added a WebSocket client, but Yahoo's stream is best-effort, not exchange-grade.

### B2. alpaca-py — **Free real-time equities via paper account**

| Name | Stars | Last release | Maintenance | Real-time? | Futures? |
|------|-------|--------------|-------------|------------|----------|
| alpacahq/alpaca-py | 1.3k | v0.43.4 (Apr 29, 2026) | Active, 86 releases | **Yes, free, real-time stocks + crypto + options** | **No futures** |

URL: https://github.com/alpacahq/alpaca-py

**Why this is critical:** Free Alpaca paper account = real-time IEX equities data (Level 1) at no cost. For equity day-trading research and paper trading, this is the single best free data source on the planet. **Caveat: zero futures support** — Alpaca doesn't offer futures.

### B3. ib_async (formerly ib_insync) — **Best free futures access**

| Name | Stars | Last release | Maintenance | Real-time? | Futures? |
|------|-------|--------------|-------------|------------|----------|
| ib-api-reloaded/ib_async | 1.5k | v2.0.1 (Jun 2025), active 2026 | Active fork after original author's passing | Yes (with paid IBKR data subscriptions ~$1.50-15/month per exchange) | **Yes, full futures via CME, ICE, etc.** |
| erdewit/ib_insync | 3.3k | Archived Mar 2024 | DEAD (author passed away) | n/a | n/a |

URLs: https://github.com/ib-api-reloaded/ib_async | https://github.com/erdewit/ib_insync

**For your futures bot, this is the play:** IBKR account → cheap CME data subscription ($10-15/mo for CME real-time non-pro) → ib_async streams ticks. This is the realistic budget path to real-time ES/NQ futures data. Pro NAILED is "free if you can demonstrate non-pro tax status."

### B4. ccxt — **Crypto only, reference architecture**

| Name | Stars | Last release | Maintenance |
|------|-------|--------------|-------------|
| ccxt/ccxt | 42.5k | Active, 95k+ commits | Very active |

URL: https://github.com/ccxt/ccxt

100+ crypto exchanges, normalized API. Not relevant for ES/NQ but a textbook example of unified API design. Useful if the bot later expands to BTC futures.

### B5. python-binance

| Name | Stars | Last release | Maintenance |
|------|-------|--------------|-------------|
| sammchardy/python-binance | 7.2k | v1.0.36 (Mar 24, 2026) | Active |

URL: https://github.com/sammchardy/python-binance | Crypto only. Reference for WebSocket streaming patterns.

### B6. Polygon-io / Databento (paid — listed for completeness)

| Name | Stars | Last release | Maintenance | Cost |
|------|-------|--------------|-------------|------|
| polygon-io/client-python (now Massive) | 1.4k | v2.7.0 (May 4, 2026) | Active | $29-199/month for stocks. Polygon recently rebranded to Massive.com. |
| databento/databento-python | 270 | v0.78.0 (May 12, 2026) | Active | Pay-per-use. Best-in-class futures tick data. ES/NQ MBO is roughly $30-100/month at low usage. |

URLs: https://github.com/polygon-io/client-python | https://github.com/databento/databento-python

**Honest take:** When the boss's bot starts making money, Databento is the upgrade path for tick-level ES/NQ. Their MBO (market-by-order) data is institutional grade. Until then, stick with IBKR feed via ib_async.

### B7. OpenBB — **Unified data platform**

| Name | Stars | Last release | Maintenance |
|------|-------|--------------|-------------|
| OpenBB-finance/OpenBB | 67.6k | ODP Desktop (Apr 25, 2026) | Very active, AGPLv3 |

URL: https://github.com/OpenBB-finance/OpenBB

**Honest take:** OpenBB is a meta-aggregator — it plugs into Yahoo, Polygon, FMP, IEX Cloud, and 30+ others through one Python API. Free tier uses free underlying sources (Yahoo). It's the "OpenBB Terminal" reborn as a platform. Useful for: fundamentals, screening, macro. Less useful for: high-frequency intraday tick data.

---

## Category C — Technical Analysis Libraries

### C1. TA-Lib (Python wrapper) — **The standard**

| Name | Stars | Last release | Maintenance |
|------|-------|--------------|-------------|
| TA-Lib/ta-lib-python | 12k | v0.6.8 (Oct 20, 2025), active 2026 | Active |

URL: https://github.com/TA-Lib/ta-lib-python

**Use this.** C library underneath (fast), wrapper actively maintained, NumPy 2 compatibility shipped, supports Python 3.9-3.14. Install pain on Windows (need pre-built wheels from unofficial-windows-binaries or use `talib-binary` conda package), but once installed it's bulletproof.

### C2. pandas-ta — **DYING IN 2026, USE FORK**

| Name | Stars | Last release | Maintenance |
|------|-------|--------------|-------------|
| twopirllc/pandas-ta | ~9k previously | Repo went 404 on GitHub | **DELETED / moving to paid model** |
| xgboosted/pandas-ta-classic | 333 | v0.5.44 (Apr 30, 2026) | Active community fork |

URLs: original gone (404), https://github.com/xgboosted/pandas-ta-classic

**Critical situation 2026:** The original twopirllc/pandas-ta repo has been pulled. Author is moving to a paid model post-July 2025; threatens to archive by July 2026 if funding not raised. **Community has forked it as `pandas-ta-classic` (xgboosted)** — 200+ indicators, 62 candlestick patterns, actively maintained, free.

**Recommendation:** Skip pandas-ta entirely in 2026. Use TA-Lib (faster, more reliable C library) or pandas-ta-classic (pure pandas, easier install).

### C3. finta — **DEAD**

| Name | Stars | Last release | Maintenance |
|------|-------|--------------|-------------|
| peerchemist/finta | 2.3k | v1.3 (Apr 2021), archived Sep 2022 | DEAD |

URL: https://github.com/peerchemist/finta

Archived. Do not use.

### Modern TA standard

**Use TA-Lib for speed and reliability.** Use `pandas-ta-classic` if you need a pure-pandas fallback or want indicators TA-Lib doesn't have. vectorbt has built-in TA wrapping both. Avoid `finta` and original `pandas-ta`.

---

## Category D — Charting / Visualization

### D1. mplfinance — **Static finance charts**

| Name | Stars | Last release | Maintenance |
|------|-------|--------------|-------------|
| matplotlib/mplfinance | 4.4k | v0.12.10b0 (Aug 2023), 154 open issues | Slow but alive |

URL: https://github.com/matplotlib/mplfinance

Best for: static publication-quality candlestick charts. PNG output for daily reports.

### D2. Plotly — **Interactive winner**

Standard Python `plotly` library. Best for: interactive backtest output with hover details, buy/sell markers, multiple panels (price + volume + indicators). Integrates with `backtesting.py` natively (Bokeh) and `vectorbt` (Plotly).

### D3. Bokeh — **`backtesting.py`'s default**

Native to `backtesting.py`. Decent but candlesticks require workarounds.

### Best stack for backtest output

- **Quick interactive review:** Plotly with `plotly.graph_objects.Candlestick`
- **Daily PnL emails/reports:** mplfinance (PNG)
- **Hosted dashboards:** Plotly Dash or Streamlit (both free)

---

## Category E — Order Execution / Live Trading

| Library | Stars | Best for | URL |
|---------|-------|----------|-----|
| NautilusTrader | 22.7k | Multi-asset, multi-venue including IBKR, Binance, Bybit, Databento, more | https://github.com/nautechsystems/nautilus_trader |
| Lumibot | 1.5k | Alpaca, IBKR, **Tradovate, TopstepX (ProjectX)** for futures | https://github.com/Lumiwealth/lumibot |
| alpaca-py | 1.3k | Alpaca only — best for equity day-trading | https://github.com/alpacahq/alpaca-py |
| ib_async | 1.5k | IBKR only — best free futures execution path | https://github.com/ib-api-reloaded/ib_async |
| ccxt | 42.5k | 100+ crypto exchanges | https://github.com/ccxt/ccxt |

### Tradovate Python wrappers (futures prop firms)

Tradovate has **no official Python SDK**. Community wrappers exist but are low-star and incomplete:

- antonio-hickey/TradovatePy — async wrapper
- cullen-b/Tradovate-Python-Client — focused on trading
- MLAlgoTrader/tradovate-python-wrapper — modified Swagger client
- tradovate/example-api-trading-strategy — official examples (JS-leaning)

**Recommendation:** If trading Topstep funded accounts, use **Lumibot's TopstepX (ProjectX) integration** — it abstracts away the Tradovate quirks. If raw API control is needed, antonio-hickey/TradovatePy is the most actively maintained community wrapper, but expect to write your own resilience layer.

---

## Category F — Day-Trading Strategy Repos Worth Studying

**Honest framing:** 99% of "trading bot" repos on GitHub are toys, abandoned student projects, or pump-the-author's-newsletter funnels. The ones with provable substance:

### F1. je-suis-tm/quant-trading — **17 strategies, study not deploy**

| Stars | Last commit | Notes |
|-------|-------------|-------|
| 9.9k | Sporadic | Implements London Breakout, Pair Trading, MACD, RSI, Bollinger, Parabolic SAR, Heikin-Ashi, Dual Thrust, Awesome Oscillator, options straddle. **Author admits: backtests assume frictionless markets (no slippage, no fees).** |

URL: https://github.com/je-suis-tm/quant-trading

**Verdict:** Excellent reference code for strategy logic. Do not run as-is (frictionless backtests lie). Read it to understand patterns.

### F2. stefan-jansen/machine-learning-for-trading — **Companion code to a serious book**

| Stars | Last commit | Notes |
|-------|-------------|-------|
| 17.3k | 351 commits | 150+ Jupyter notebooks accompanying the textbook "Machine Learning for Algorithmic Trading, 2nd Ed." Covers data sourcing, linear models, deep learning, RL. |

URL: https://github.com/stefan-jansen/machine-learning-for-trading

**Verdict:** Best ML-for-trading reference on GitHub. Code is pedagogical, not production. Read for technique.

### F3. microsoft/qlib — **Industrial-strength but Asian-equity-biased**

| Stars | Last release | Notes |
|-------|--------------|-------|
| 43k | v0.9.7 (Aug 2025) | Microsoft Research's quant platform. Includes 20+ ML models, RL workflow, RD-Agent LLM-based factor mining. |

URL: https://github.com/microsoft/qlib

**Verdict:** Heavyweight platform. Mostly tuned for Chinese A-shares historically; US equity support is workable. **Overkill for a small day-trading bot** but worth studying if going down the ML factor route.

### F4. AI4Finance-Foundation/FinRL — **Deep reinforcement learning**

| Stars | Last release | Notes |
|-------|--------------|-------|
| 15.2k | v0.3.8 (Mar 20, 2026) | First open-source RL framework for finance. 5 DRL algos (A2C, DDPG, PPO, SAC, TD3). |

URL: https://github.com/AI4Finance-Foundation/FinRL

**Verdict:** Research-grade. The team's own note says original FinRL is now "education/benchmarking/research" — production users should look at FinRL-X. **Treat as a learning curriculum, not a production system.** RL in markets is famously hard to make robust.

---

## Category G — Curated Awesome Lists

### G1. wilsonfreitas/awesome-quant — **The canonical list**

| Stars | Notes |
|-------|-------|
| 26.2k | Comprehensive curated list of quant Python libraries. Updated regularly. |

URL: https://github.com/wilsonfreitas/awesome-quant

### G2. paperswithbacktest/awesome-systematic-trading

| Stars | Notes |
|-------|-------|
| 8.2k | 97 libraries, 40+ documented strategies (with academic citations), 55 books, 23 videos. Goes deeper than awesome-quant on strategies specifically. |

URL: https://github.com/paperswithbacktest/awesome-systematic-trading (also mirrored at edarchimbaud/awesome-systematic-trading)

### G3. Bookmark these too

- https://github.com/topics/algorithmic-trading?l=python&o=desc&s=stars — sorted by stars
- https://github.com/topics/quantitative-finance
- https://github.com/topics/backtesting

---

## Category H — Real-Time Data: Honest Free Options

**Reality check:** Truly free real-time **futures** data does not exist. Exchanges (CME, ICE) charge for the feed itself. Anyone offering it "free" is delayed, sampled, or violating ToS.

| Source | Cost | Real-time? | Futures? | Worth it? |
|--------|------|------------|----------|-----------|
| Alpaca paper account | Free | Yes (IEX equities) | No | YES for equity bot dev |
| IBKR paper account | Free | Yes WITH data subscription (~$10-15/mo) | Yes (CME, ICE add-ons) | YES — best path to real ES/NQ |
| Tradovate demo | Free | 10-min delayed unless funded | Yes | Only useful if planning to fund |
| yfinance | Free | 15-min delayed | Yes (`ES=F`, `NQ=F`) | Backtesting only |
| TradingView (tvDatafeed scraper) | Free | Yes but ToS-violating | Yes | Not for production |
| Databento | Pay-per-use | Yes, MBO-grade | Yes | When the bot is profitable |
| Polygon/Massive | $29-199/mo | Yes equities, futures coming | Limited futures | Equity bot upgrade path |

**Verdict:** Free real-time futures from a GitHub project = no. The realistic free-ish path is **IBKR account + $10-15/mo CME non-pro data + ib_async**.

---

## Category I — Machine Learning for Trading

### I1. mlfinlab (Hudson & Thames) — **PAYWALLED in disguise**

| Stars | Status |
|-------|--------|
| 4.7k | License: "all rights reserved" — **public GitHub for issue tracking only**. Library itself requires Business/Enterprise license purchase. |

URL: https://github.com/hudson-and-thames/mlfinlab

**Honest take:** This used to be open-source implementations of Lopez de Prado's *Advances in Financial Machine Learning*. Hudson & Thames pivoted to commercial in 2020-2021. The GitHub repo gives the false impression of being free. **It is not.** If you want the techniques, read Lopez de Prado's book and implement yourself, or use the AI4Finance Foundation projects.

### I2. stefan-jansen/machine-learning-for-trading (covered in F2)

Best free alternative to mlfinlab for ML-for-trading code.

### I3. microsoft/qlib (covered in F3)

Heaviest industrial-strength free ML quant platform.

### I4. AI4Finance-Foundation/FinRL (covered in F4)

RL specifically.

---

## Category J — Portfolio Analytics (bonus, worth knowing)

### J1. QuantStats

| Stars | Last release | Notes |
|-------|--------------|-------|
| 7.1k | v0.0.81 (Jan 13, 2026) | Tear sheets, Sharpe, drawdowns, Monte Carlo. From the same author as yfinance. |

URL: https://github.com/ranaroussi/quantstats

**Use it.** Drop your bot's daily PnL series in, get a publication-quality HTML report. Free, active, simple.

### J2. PyPortfolioOpt

| Stars | Notes |
|-------|-------|
| ~5k | Markowitz, Black-Litterman, HRP. For portfolio allocation, not day trading. |

URL: https://github.com/PyPortfolio/PyPortfolioOpt

### J3. Riskfolio-Lib

| Stars | Notes |
|-------|-------|
| 4.2k | More advanced than PyPortfolioOpt — 24 risk measures, Kelly Criterion optimization. Built on CVXPY. |

URL: https://github.com/dcajasn/Riskfolio-Lib

For day trading, these are out-of-scope, but if the bot later does multi-strategy allocation across signals they're the standard.

---

## ============================================================
## FINAL VERDICTS
## ============================================================

### TOP 5 MUST-USE FOR THE BOT (in priority order)

1. **NautilusTrader** — https://github.com/nautechsystems/nautilus_trader — Core execution + backtest engine. Unified sim/paper/live for ES/NQ. Will pay dividends as the bot grows. Steep curve but worth it.
2. **ib_async** — https://github.com/ib-api-reloaded/ib_async — Free-ish path to real-time CME ES/NQ data via an IBKR account. The realistic budget option for futures.
3. **TA-Lib (Python)** — https://github.com/TA-Lib/ta-lib-python — Fast, reliable indicators. C-backed. Standard since 1999, still actively maintained 2026. (Use `pandas-ta-classic` as fallback for indicators TA-Lib lacks.)
4. **alpaca-py** — https://github.com/alpacahq/alpaca-py — Free real-time equities for the equity side of the bot. Paper trading included.
5. **QuantStats** — https://github.com/ranaroussi/quantstats — Drop-in tear sheets for performance reporting. Skip building your own.

### TOP 3 NICE-TO-HAVE (FUTURE)

1. **Lumibot** — https://github.com/Lumiwealth/lumibot — If the boss ever wants to trade a Topstep funded account, Lumibot's TopstepX/Tradovate integration is the fastest path. Consider as a parallel framework or a Nautilus alternative if Nautilus learning curve becomes a blocker.
2. **Databento Python client** — https://github.com/databento/databento-python — Upgrade path for institutional-grade ES/NQ tick data when the bot is profitable and IBKR's feed quality becomes a ceiling.
3. **OpenBB** — https://github.com/OpenBB-finance/OpenBB — Fundamentals, macro, screening across many providers under one Python API. Useful for adding context (earnings dates, macro events) to the bot's decision-making.

### 3 REPOS TO STUDY FOR CODE PATTERNS (not necessarily deploy)

1. **freqtrade** — https://github.com/freqtrade/freqtrade — Crypto-only, but the cleanest example of strategy + risk + execution module separation in OSS trading bots. 50k stars, mature plugin system, backtest hyperopt patterns. Worth a weekend of reading.
2. **stefan-jansen/machine-learning-for-trading** — https://github.com/stefan-jansen/machine-learning-for-trading — 150+ notebooks covering everything from feature engineering to deep learning for markets. Study before applying ML to the bot.
3. **je-suis-tm/quant-trading** — https://github.com/je-suis-tm/quant-trading — 17 classical strategies implemented cleanly in Python. Read the London Breakout, Dual Thrust, and Pair Trading code — these patterns map to ES/NQ intraday well.

### 5 POPULAR BUT AVOID (overhyped, dead, broken, or paywalled-in-disguise)

1. **mementum/backtrader** (21.5k stars) — Effectively abandoned by author since ~2018. Stars are legacy. Use NautilusTrader, Lumibot, or backtesting.py instead. https://github.com/mementum/backtrader
2. **quantopian/zipline** (19.8k stars) — Quantopian shut down in 2020. Maintainers explicitly say PRs may sit "months or even years." Hard to set up cleanly. Use anything else. https://github.com/quantopian/zipline
3. **hudson-and-thames/mlfinlab** (4.7k stars) — Public GitHub repo gives false impression of being open-source. License is "all rights reserved." The actual library requires a paid Business/Enterprise license. Misleading. https://github.com/hudson-and-thames/mlfinlab
4. **peerchemist/finta** (2.3k stars) — Archived September 2022. Dead. Use TA-Lib or pandas-ta-classic. https://github.com/peerchemist/finta
5. **erdewit/ib_insync** (3.3k stars) — Original author passed away in 2024, repo archived March 2024. Use ib_async (the maintained fork). https://github.com/erdewit/ib_insync — and avoid **original twopirllc/pandas-ta**, which has been removed from GitHub and is moving to paid model (archive scheduled July 2026 if funding fails) — use **xgboosted/pandas-ta-classic** instead.

### Honorable mentions to bookmark but not install

- **microsoft/qlib** (43k stars) — Excellent ML quant platform but overkill for a single-developer day-trading bot. Star and revisit if scaling to multi-strategy multi-factor.
- **AI4Finance-Foundation/FinRL** (15.2k stars) — RL research framework. Their own team admits original FinRL is now "research/benchmarking" — production users go to FinRL-X. Star, don't build prod on top.
- **vectorbt PRO** (paid) — The community edition (7.5k stars) is fine for grid-search backtests. PRO subscription is worth it only if doing thousands of parameter sweeps daily.

---

## Concrete First-Week Setup for the Bot

If the boss were to start tomorrow, here's the stack to install:

```bash
# Core
pip install nautilus_trader
pip install ib_async
pip install alpaca-py
pip install quantstats
pip install yfinance      # historical backtest data
pip install pandas-ta-classic   # fallback indicators

# TA-Lib (Windows: download wheel from unofficial-windows-binaries or use conda)
conda install -c conda-forge ta-lib

# Visualization
pip install mplfinance plotly

# Optional: quick prototyping
pip install backtesting   # backtesting.py
```

Then:
1. Open IBKR paper account → subscribe to CME non-pro data ($10-15/mo) → connect via ib_async → confirm live ES/NQ ticks streaming.
2. Build a vanilla VWAP-deviation strategy in backtesting.py first (one weekend).
3. Port the working logic into NautilusTrader once the strategy is validated (one to two weeks).
4. Paper trade through IBKR paper for 30-60 days. Use QuantStats to track daily.
5. Only then consider real capital.

**Total infrastructure cost first 90 days:** ~$30-45 (IBKR CME data feed × 3 months) + $0 in software. Everything else is free open source.

---

## Cited URLs (master list)

**Backtest frameworks**
- https://github.com/nautechsystems/nautilus_trader
- https://github.com/QuantConnect/Lean
- https://github.com/QuantConnect/lean-cli
- https://github.com/kernc/backtesting.py
- https://github.com/polakowo/vectorbt
- https://github.com/mementum/backtrader
- https://github.com/smalinin/backtrader_next
- https://github.com/quantopian/zipline
- https://github.com/Lumiwealth/lumibot
- https://github.com/freqtrade/freqtrade
- https://github.com/jesse-ai/jesse

**Data sources**
- https://github.com/ranaroussi/yfinance
- https://github.com/alpacahq/alpaca-py
- https://github.com/ib-api-reloaded/ib_async
- https://github.com/erdewit/ib_insync (archived)
- https://github.com/ccxt/ccxt
- https://github.com/sammchardy/python-binance
- https://github.com/polygon-io/client-python
- https://github.com/databento/databento-python
- https://github.com/OpenBB-finance/OpenBB
- https://github.com/rongardF/tvdatafeed

**Technical analysis**
- https://github.com/TA-Lib/ta-lib-python
- https://github.com/xgboosted/pandas-ta-classic
- https://github.com/peerchemist/finta (archived)

**Visualization**
- https://github.com/matplotlib/mplfinance
- https://plotly.com/python/
- https://bokeh.org/

**Execution (Tradovate community wrappers)**
- https://github.com/antonio-hickey/TradovatePy
- https://github.com/cullen-b/Tradovate-Python-Client
- https://github.com/MLAlgoTrader/tradovate-python-wrapper

**Strategy study repos**
- https://github.com/je-suis-tm/quant-trading
- https://github.com/stefan-jansen/machine-learning-for-trading
- https://github.com/microsoft/qlib
- https://github.com/AI4Finance-Foundation/FinRL

**Awesome lists**
- https://github.com/wilsonfreitas/awesome-quant
- https://github.com/paperswithbacktest/awesome-systematic-trading

**Portfolio analytics**
- https://github.com/ranaroussi/quantstats
- https://github.com/PyPortfolio/PyPortfolioOpt
- https://github.com/dcajasn/Riskfolio-Lib

**ML for trading (paid-in-disguise)**
- https://github.com/hudson-and-thames/mlfinlab — AVOID, not free.

---

*End of report. Total word count: ~3,800.*
