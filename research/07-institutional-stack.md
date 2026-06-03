# The Unified Institutional Analytical Stack

**Author:** Internal research note for solo-operator equity workflow
**Purpose:** Turn 8 "you are a senior X at firm Y" prompt templates into one coherent, honest, layered process.
**Verdict up front:** The 8 templates each mimic a real institutional role. They are useful as *checklists and structuring devices*. They are dangerous as *sources of specific numbers*. LLMs hallucinate financial data at rates of up to 41% on unconstrained finance queries (FINOS, Chainlink Blog research). Every number an LLM emits must be verified against a primary source before it touches a position size.

---

## Section A: The Real-World Analytical Hierarchy (Top-Down)

In real institutions, analysis is layered, not parallel. A portfolio manager at a multi-strategy fund doesn't run "DCF + screener + technicals + macro" in a blender. They flow from regime to entry, and each layer's output becomes the next layer's input. The CFA Institute's portfolio-management curriculum codifies this as the "planning -> execution -> feedback" loop, and the top-down vs. bottom-up distinction is one of the first things a Level I candidate is forced to internalize (CFA Institute, AnalystPrep).

Here is the realistic layering for the 8 templates:

### Layer 1 - Macro regime (the McKinsey lens)
**Question answered:** What economic environment are we in, and what does it favor?
**Inputs:** 10-yr yield, Fed funds path, inflation trajectory, dollar index, oil, employment, ISM.
**Output:** A regime label (early-cycle / mid / late / recession), a directional bias on duration, and a list of sectors that historically outperform in this regime.
**Source of truth:** Fidelity's "Business Cycle Approach to Equity Sector Investing" is the canonical retail-accessible version of what McKinsey GEI and Goldman's macro strategy team publish monthly (Fidelity).

### Layer 2 - Sector selection (the Bain industry lens)
**Question answered:** Within the favored regime, which industries have structural tailwinds *and* defensible competitive structure?
**Inputs:** Porter's Five Forces by industry, regulatory environment, secular demand drivers, capital cycle position.
**Output:** A short list of 3-5 sectors and 1-2 sub-industries to overweight.
**Source of truth:** Porter's HBR 1979 framework, plus Morgan Stanley's "Measuring the Moat" (Mauboussin/Counterpoint Global) which extends the moat concept with quantitative durability metrics.

### Layer 3 - Universe narrowing (the Goldman screener lens)
**Question answered:** Inside the favored sectors, which names pass quantitative filters?
**Inputs:** P/E vs. sector, revenue CAGR, ROIC, D/E, FCF yield, momentum, factor exposures.
**Output:** Working list of 10-30 tickers.
**Source of truth:** Goldman's actual published screening methodology uses four attributes - growth, returns, multiple, volatility - indexed and percentile-ranked within a regional coverage universe (Goldman Sachs Research). Retail equivalents: Finviz, Stock Rover, Koyfin, Yahoo screener.

### Layer 4 - Competitive deep-dive (the Bain single-name lens)
**Question answered:** Of the screener survivors, which have a *durable* edge versus the top 5-7 competitors?
**Inputs:** Market share trends, segment margins, R&D efficiency, switching costs, scale economics, management capital allocation track record.
**Output:** 2-5 finalists where moat is real, not narrative.
**Source of truth:** 10-Ks (segment data), industry trade press, Bain/McKinsey/BCG industry reports, Mauboussin's moat checklist.

### Layer 5 - Valuation (the Morgan Stanley DCF lens)
**Question answered:** At today's price, what are we paying for, and what has to be true for us to make money?
**Inputs:** 5-year revenue model, operating margin path, capex, working capital, WACC, terminal multiple or perpetuity growth.
**Output:** A fair-value range with sensitivity (not a point estimate), plus a list of "model-breakers" - the 2-3 assumptions that swing the answer.
**Source of truth:** Morgan Stanley's stated philosophy is that "everything is a DCF model" - even a P/E multiple is a compressed DCF (Morgan Stanley, Counterpoint Global). Their ModelWare framework explicitly links operating drivers to intrinsic value via a Profitability Tree.

### Layer 6 - Catalyst calendar (the JPMorgan earnings lens)
**Question answered:** What event windows over the next 1-4 quarters will re-rate the stock?
**Inputs:** Earnings dates, guidance cadence, conference appearances, product launches, regulatory decisions, options-implied move, historical post-earnings reaction.
**Output:** A timeline of "binary" events with expected magnitude and direction bias.
**Source of truth:** Consensus from Refinitiv/FactSet/Visible Alpha (institutional) or Zacks/Seeking Alpha/Yahoo (retail). Options-implied move from the at-the-money straddle nearest expiry post-earnings - a published, observable number, not an LLM estimate.

### Layer 7 - Entry timing (the Citadel technical lens)
**Question answered:** Given we want to own this, where do we actually buy, and where do we cut?
**Inputs:** D/W/M trend, S/R levels, 50/100/200 MAs, RSI/MACD, volume profile, options gamma levels.
**Output:** Entry zone, stop, first/second target, R:R ratio, position-sizing input (ATR-based).
**Source of truth:** Note - Citadel itself is *not* a technical-analysis shop. Citadel is quantitative: stat-arb, ML on order books, NLP on news (DayTrading.com, MIT News). The "Citadel technical analysis" template is a marketing fiction. The substance of technical analysis is real, but you should source the methodology from Edwards & Magee, John Murphy, or Brett Steenbarger - not from "what Citadel does."

### Layer 8 - Risk and sizing (the Bridgewater + BlackRock lens)
**Question answered:** Given the rest of the book, how much of this can we own without breaking the portfolio?
**Inputs:** Correlation to existing holdings, sector concentration, factor exposures, drawdown budget, liquidity, tail-risk scenarios.
**Output:** Position size in % NAV or risk units, hedge overlays if needed, rebalancing triggers.
**Source of truth:** Bridgewater's All-Weather / risk-parity methodology (Bridgewater, "The All Weather Story") balances *risk contribution* across asset classes, not dollars. BlackRock's strategic asset allocation framework (BlackRock SAA whitepaper, 2018) layers factor exposures across the core (cheap beta) and satellites (active/alpha).

This is the order. Skipping layers is the most common mistake. The second-most common mistake is running them in parallel and pretending the outputs are independent (they aren't - a screener result that ignores macro regime will hand you cyclicals at the top of the cycle).

---

## Section B: The Unified Workflow - 10-Step Institutional Analysis

For any single-name stock that lands on the watchlist, run these 10 steps in order. Each step has an explicit "data source" line because the LLM is the *structuring* engine, not the *data* engine.

**Step 1 - Regime check (5 minutes).** What is the 10-yr yield doing this week? Is the Fed cutting, holding, or hiking on the dot plot? Is the ISM above or below 50? Are credit spreads widening or tightening? Output: one sentence regime label.
*Data:* FRED, Fed dot plot, ISM monthly release.

**Step 2 - Sector fit (5 minutes).** Given the regime, is this name's sector a tailwind, a coin-flip, or a fight against gravity? Cyclicals into a slowdown is a fight. Defensives into early-cycle is a fight.
*Data:* Fidelity business-cycle sector charts; SSGA "How macroeconomic variables impact sector performance."

**Step 3 - Quality screen (10 minutes).** Pull the basic Goldman-style filters: revenue 5-yr CAGR, gross margin trend, ROIC vs. cost of capital, net debt / EBITDA, FCF conversion. If 3+ of these are red, stop. Do not proceed to DCF on a structurally weak business.
*Data:* Stock Analysis, Stratosphere, Koyfin, Stock Rover, or the 10-K directly. Never trust an LLM-stated ROIC.

**Step 4 - Competitive map (15 minutes).** Who are the top 5 competitors? What is each one's market share trend over 3 years? What is the moat - cost, scale, network, switching, IP, brand, regulatory? Is the moat widening or narrowing? Has management been a good or bad capital allocator (buybacks at lows or highs, M&A track record)?
*Data:* 10-K competition section, Mauboussin moat checklist, industry reports, IBISWorld where available.

**Step 5 - Valuation triangulation (20 minutes).** Build (or have the LLM build) a *skeleton* DCF: 5-yr revenue, operating margin path, capex, WACC, terminal. Then triangulate with EV/Sales, EV/EBITDA, P/FCF vs. 5-yr history and vs. peers. The DCF is not a price target - it is a discipline that surfaces *what has to be true* for the current price.
*Data:* Consensus from Zacks/Yahoo for inputs; verify against 10-Q segment data and management guidance. Never let the LLM invent margin or revenue numbers.

**Step 6 - Catalyst calendar (10 minutes).** Next earnings date. Consensus EPS and revenue. Last 4Q beat/miss pattern. Options-implied move (read off the straddle). Guidance cadence. Product / regulatory / macro events over the next 1-2 quarters.
*Data:* Earnings Whispers, Zacks, the broker's options chain. The implied move is observable - do not let the LLM estimate it.

**Step 7 - Technical setup (15 minutes).** Daily and weekly trend. Major S/R levels (look-and-eye, drawn from highs/lows and volume nodes). 50/100/200-day MAs. RSI and divergences. Volume confirmation on the recent move. Specific entry zone, hard stop, first target, second target. R:R must be at least 2:1 for the trade to even be considered.
*Data:* TradingView. The LLM can describe the rules but cannot read the chart - any price level it cites is fabricated unless you fed it the chart.

**Step 8 - Position sizing (10 minutes).** Given account size, what's the max dollar loss on this trade? Position size = max-loss-dollars / (entry - stop). Cross-check: position size as % of NAV, position size relative to other open positions in the same sector / factor, position size relative to ADV (don't take liquidity you can't exit).
*Data:* Your account, your spreadsheet. The LLM is irrelevant here.

**Step 9 - Portfolio-level risk overlay (10 minutes).** After this trade, what is the new sector concentration? Single-stock concentration? Beta-adjusted gross and net exposure? Correlation to existing top 3 holdings (use 90-day rolling)? Does this push the book outside any pre-committed limits?
*Data:* Portfolio Visualizer or your own correlation matrix; this is the Bridgewater step.

**Step 10 - Write the thesis on one page.** Entry, stop, targets, position size, *what would make me wrong* (3 specific falsifiable conditions), review date. If you can't fit it on one page, you don't understand the trade yet.
*Data:* You. The LLM can copy-edit; it cannot generate conviction.

Total time: roughly 105 minutes per name on initial deep dive. A daily watchlist scan should take 20-30 minutes by running Steps 1-2 once for the day, then Steps 6-7 for each name on the watchlist.

---

## Section C: Honest Grade of Each Prompt Template

For each of the 8 templates: what it actually does well, what it overpromises, and what you must verify externally.

### 1. Goldman Sachs Stock Screener
**Good at:** Forcing you to specify *criteria* explicitly (P/E vs. sector, growth threshold, debt cap). This is genuinely useful as a *scaffolding* prompt.
**Overpromises:** "Top 10 stocks matching my criteria" - the LLM does not have a real-time screener. It will return a plausible-sounding list pulled from training data months or years stale. Any specific P/E, dividend yield, or EPS growth number it cites is almost certainly wrong by the time you read it.
**Must verify externally:** Every single ticker, P/E, EPS-growth-5y, D/E, dividend yield, "moat strength" rating, and entry zone.
**Right data source:** Finviz Elite or Stock Rover for the screen itself, Yahoo Finance / Stock Analysis for ratios, the 10-K for debt.

**Grade: C+.** Useful as a *checklist generator*. Treat the actual ticker list as a starting brainstorm, never as a recommendation.

### 2. Morgan Stanley DCF Valuation
**Good at:** Structuring the DCF skeleton (revenue, margins, FCF, WACC, terminal, sensitivity). The model architecture it produces is genuine and matches a junior IB analyst's training.
**Overpromises:** The numbers inside the DCF. The LLM will happily project "12% revenue CAGR, 22% operating margin by Year 5" with the confidence of an MD. Those numbers are guesses dressed up as analysis.
**Must verify externally:** Base revenue, last-3-yr operating margin, capex %, working capital change, share count, current net debt, sector-appropriate WACC, peer exit multiples.
**Right data source:** 10-K and 10-Q for historicals, management guidance for forwards, Damodaran's data pages (NYU Stern) for WACC and industry multiples - this is the single best free source of valuation data on the internet.

**Grade: B-.** The DCF *form* is correct; the *content* must be your own. Treat the LLM output as a populated template you then overwrite cell by cell.

### 3. Bridgewater Risk Analysis
**Good at:** Surfacing portfolio-level questions a retail investor rarely asks - correlation between holdings, factor concentration, tail-risk scenarios, hedging options.
**Overpromises:** Specific correlation coefficients ("AAPL and MSFT correlation: 0.78") and stress-test outputs ("-32% in a 2008-style scenario"). These numbers are fabricated unless you feed in real historical data.
**Must verify externally:** Correlations, beta, drawdown stats, sector and factor exposures, liquidity ratings.
**Right data source:** Portfolio Visualizer (free), MSCI factor models if you have access, your broker's risk-analytics tab.

**Grade: B.** The *questions* it forces are excellent - those are the actual Bridgewater habits of mind. The *answers* must come from a real correlation engine.

### 4. JPMorgan Earnings Breakdown
**Good at:** Building the pre-earnings checklist - what to watch, which segments matter, what guidance commentary to listen for.
**Overpromises:** Consensus EPS, options-implied move, historical post-earnings reactions. All of these are real, public, observable numbers - and the LLM will hallucinate them with conviction.
**Must verify externally:** Consensus EPS and revenue, options-implied move (read the straddle), beat/miss history, prior 4Q stock reactions, segment growth rates.
**Right data source:** Earnings Whispers, Estimize, Zacks, Yahoo Finance, the broker's options chain. For the implied move: at-the-money call premium + at-the-money put premium of the nearest weekly post-earnings, divided by stock price.

**Grade: B-.** The structure is solid. The numbers must be pulled from public data the day of the prep, not from the LLM's training corpus.

### 5. BlackRock Portfolio Construction
**Good at:** Forcing a complete IPS (Investment Policy Statement) - the BlackRock-style template actually mirrors the CFA Level III portfolio-management module reasonably well.
**Overpromises:** Specific ETF tickers with "expected return 7-9%" - the expected-return numbers are wishful, and the tickers may have been merged, closed, or restructured since the training data.
**Must verify externally:** ETF tickers (still trade? expense ratio? AUM? tracking error?), historical max drawdown, current sector weights inside each ETF.
**Right data source:** ETF issuer fact sheets, etf.com, Morningstar, BlackRock's own iShares pages for iShares products. For long-run expected returns: BlackRock's published Capital Market Assumptions (updated quarterly) or Research Affiliates' "Asset Allocation Interactive."

**Grade: B+.** This is one of the better templates because portfolio construction is more about *process* than *prediction*. Just don't believe the return numbers.

### 6. Citadel Technical Analysis
**Good at:** Listing the standard TA checklist - trends, MAs, RSI, MACD, S/R, volume, pattern, Fib, R:R. This is essentially a junior chart-tech checklist.
**Overpromises:** Specific S/R prices, RSI readings, "the stock is in a falling wedge with bullish divergence" - the LLM cannot read a chart. Any specific price level or oscillator reading it produces is invented.
**Must verify externally:** Every single price level, MA value, RSI/MACD number, pattern claim, volume statistic.
**Right data source:** TradingView for charts; your own eyes for patterns. Note also the framing error: real Citadel is not a chart-reading firm - it is a quant / stat-arb / market-making firm. The template misrepresents the firm to dress up vanilla TA.

**Grade: D+.** Useful only as a checklist of *what to look at on the chart you opened separately*. Any specific number it emits is fiction.

### 7. Bain Competitive Advantage
**Good at:** Forcing the Porter-style competitive frame - top competitors, share trends, moat sources, threats, SWOT. This is genuine MBA-style strategy work and translates well into a prompt.
**Overpromises:** Specific market-share percentages, R&D spend numbers, "management capital allocation grade." These will be either stale or invented.
**Must verify externally:** Competitor list, market share % (with date and source), revenue and margin tables, R&D spend, capex history.
**Right data source:** 10-K competition section, IBISWorld, Statista (paywalled), trade-press estimates, Mauboussin's "Measuring the Moat" for moat taxonomy.

**Grade: B.** The *frame* is sound; the *data* must be sourced fresh. This is one of the strongest templates because moat analysis is more narrative than numerical.

### 8. McKinsey Macro Impact
**Good at:** Forcing the macro-to-sector linkage - which sectors win under which rate / inflation / growth regime, what sector rotation to expect.
**Overpromises:** Specific Fed-path forecasts, GDP-impact-on-earnings numbers, "USD will weaken 5% over 6 months." Macro forecasting is hard even for actual McKinsey GEI; an LLM cannot do it.
**Must verify externally:** Current 10-yr yield, current Fed funds rate, current ISM, current core CPI, the dot plot. All public, all current.
**Right data source:** FRED, Federal Reserve, BLS, ISM, Atlanta Fed GDPNow.

**Grade: B-.** Use it for *qualitative regime framing* (which sectors tend to lead which phase) and ignore the specific forecasts.

**Pattern across all 8 grades:** The templates are good at *structure*, mediocre to bad at *content*. Their highest-value use is as **checklists that force completeness**. Their lowest-value use is as **answer generators**. Mixing those two uses up is the single biggest reason retail investors get burned by LLM-driven analysis.

---

## Section D: The Combined Unified Analytical Stack Prompt

What follows is a single consolidated prompt that combines the best of all 8 templates. Paste this into Claude or GPT-5 along with **the actual data** (10-K excerpts, current price, current chart screenshot, recent consensus, current macro readings). Without the data, the output is creative writing.

```
You are a senior portfolio manager at a multi-strategy fund. I will give you a
single ticker plus the current data inputs. Produce a structured analysis in the
order below. For any number you do not have direct data for, write "REQUIRES
VERIFICATION" rather than inventing a number. Do not fabricate prices, ratios,
margins, market share, correlations, or implied moves. Mark every assumption.

INPUTS I AM PROVIDING (fill these before running the prompt):
- Ticker: ___
- Current price: ___
- Sector and sub-industry: ___
- Last 4 quarters revenue and EPS (actual and consensus): ___
- Most recent 10-K segment data: ___
- Current 10-yr yield, Fed funds, ISM, core CPI: ___
- Current options-implied move for next earnings (from straddle): ___
- Recent chart observations (trend, key S/R, MAs): ___
- Existing portfolio holdings and weights: ___

OUTPUT (in this order, do not skip sections):

PART 1 - MACRO REGIME (McKinsey lens)
- Regime label (early / mid / late / recession) given the data I provided.
- Three sectors that historically lead in this regime, three that lag. Cite the
  source convention (Fidelity business-cycle framework is fine).
- Does this ticker's sector lean tailwind, neutral, or headwind right now?

PART 2 - SECTOR AND COMPETITIVE LANDSCAPE (Bain lens)
- Top 5 competitors by name (mark REQUIRES VERIFICATION if uncertain).
- Where does this name sit in the Porter Five Forces map? Identify the single
  most relevant force (typically rivalry or threat of entry).
- Moat type: cost, scale, network, switching, IP, brand, regulatory, intangible.
- Is the moat widening, stable, or narrowing? What is the evidence?

PART 3 - QUALITY SCREEN (Goldman lens)
- From the data I provided, fill in: revenue 5-yr CAGR, gross margin trend,
  operating margin trend, FCF conversion, ROIC vs. WACC, net debt / EBITDA,
  share count change 3-yr. Use "REQUIRES VERIFICATION" wherever you don't have
  the data point.
- Pass / fail verdict on quality. Three reds = stop.

PART 4 - VALUATION (Morgan Stanley DCF lens)
- Skeleton DCF with my-provided revenue base. Project 5 years of revenue and
  operating margin with EXPLICIT assumptions labeled (e.g. "I'm assuming 8%
  revenue growth tapering to 4% by Year 5 - VERIFY against guidance").
- WACC range (provide the range and reasoning, not a point estimate).
- Terminal: exit-multiple and perpetuity-growth, both shown.
- Sensitivity table: WACC vs. terminal growth, 3x3 grid.
- The two or three "model-breakers" - the assumptions that swing the answer
  most.
- Triangulate against EV/Sales, EV/EBITDA, P/FCF vs. peers and vs. 5-yr history.
- Output: fair-value RANGE, not point.

PART 5 - CATALYST AND EARNINGS (JPMorgan lens)
- Next earnings date.
- What 3 metrics matter most for this name (segment revenue, take rate, gross
  margin, subscriber count - whatever is the key driver).
- Last 4Q beat/miss pattern from my-provided data.
- Options-implied move (from my-provided number).
- Three bull-case and three bear-case scenarios with explicit triggers.
- One-line play recommendation: own through, trim into, avoid.

PART 6 - TECHNICAL SETUP (chart-tech lens; note: real Citadel is quant not TA)
- Using only my-provided chart observations, summarize trend on D/W timeframes.
- Mark key S/R from what I provided.
- Suggest entry zone, hard stop, first target, second target.
- R:R ratio. If R:R < 2:1, recommend skip or wait.
- Confidence rating 1-10 with reasoning.

PART 7 - RISK OVERLAY (Bridgewater lens)
- Given my-provided portfolio, what does this position add in terms of:
  - Sector concentration change
  - Single-stock concentration
  - Correlation to top 3 existing holdings (mark REQUIRES VERIFICATION - you do
    not have rolling correlation data)
  - Factor exposure tilt (growth vs. value, large vs. small, US vs. ex-US)
- Tail-risk question: in a 20% market drawdown, what is the likely behavior?
- Hedge candidates (sector ETF short, put spread, pair with short of weakest
  peer).

PART 8 - POSITION SIZING (BlackRock lens)
- Given the entry, stop, and a max-loss-per-trade I will specify, compute
  position size in shares and dollars.
- Cross-check position size as % NAV.
- Cross-check vs. ADV (mark REQUIRES VERIFICATION).
- Rebalancing trigger: at what price / what time horizon do we reassess?

PART 9 - ONE-PAGE THESIS
- Three sentences: bull case, bear case, base case.
- Entry, stop, two targets, position size.
- Three falsifiable conditions that would make me wrong.
- Review date.

PART 10 - HONESTY LINE
- List every number in this analysis that you generated without my providing
  the underlying data. These are the cells the user must verify before acting.
```

The prompt above intentionally builds in a "REQUIRES VERIFICATION" output convention. This is the single most important guardrail against LLM hallucination in financial analysis - it makes the model's *uncertainty surface itself*, rather than hiding behind confident prose.

---

## Section E: Day-Trader vs. Long-Term Investor Split

The 8 templates were marketed as one stack. They are not. Roughly half of them only matter on day-trading timeframes; the other half only matter on multi-year investing timeframes. Mixing them is the most common retail mistake.

### Lenses that matter for DAY TRADING
- **Citadel-style technical analysis** (entry, stop, target, R:R). Most of the day's PnL is determined here.
- **JPMorgan earnings event template**, but only for the *event windows* - implied move, post-earnings drift, gamma squeeze setups. The fundamental commentary is irrelevant on a day-trade timeframe.
- **McKinsey macro impact**, but only in a "regime / risk-on vs. risk-off" form. Specifically: what is SPY / QQQ doing today, are credit spreads widening, is VIX above or below 18, is the 10-yr breaking a level. On the day, macro = the tape.
- **Bridgewater risk** in the form of *intra-day position correlation*: do not hold 4 long mega-cap tech names and call yourself diversified.

What does **not** matter for day trading: DCF, moat analysis, BlackRock IPS, 5-year revenue CAGR. None of these will move within your holding period. Spending an hour on a DCF for a name you plan to hold for 6 hours is not analysis - it is procrastination disguised as rigor.

### Lenses that matter for LONG-TERM INVESTING
- **Morgan Stanley DCF** as the central discipline.
- **Bain competitive moat analysis** - the single highest-correlation factor with multi-year returns once valuation is in a reasonable band.
- **BlackRock portfolio construction** - the architecture in which all single-name decisions live.
- **Bridgewater portfolio-level risk** - correlation, factor concentration, tail-risk overlays.

What does **not** matter for long-term investing: today's RSI, today's implied move, this week's macro headline. These are pure noise on a 3-5-year holding period.

### Why mixing is the most common retail mistake
Retail investors hear "do your homework" and conclude that more analysis is always better. They then run the long-term toolkit on a day-trade (taking a "high-conviction position" on a DCF in something they sell at 11:30am for a 1% loss) or they run the day-trade toolkit on a long-term position (selling a 10-year compounder because RSI hit 70).

The institutional answer is that these are *different jobs with different toolkits*. Goldman has separate equity research (long-term, fundamental) and trading desk (short-term, execution) groups for a reason. They do not run the same playbook. Solo operators who mix the playbooks tend to (a) sell winners early because the chart spooked them, (b) hold losers too long because "the DCF says it's cheap," and (c) blow up around earnings because they were trading a chart in a name they had a fundamental view on.

Decide first: am I in this trade for hours, or for years? Then pick the right four lenses and ignore the other four.

---

## Section F: How Real Institutions Actually Do It

The 8 prompt templates are not a single workflow. They are eight specialized roles compressed into eight prompts. In reality:

- **Equity research analyst** (sell-side or buy-side) covers a single sector deeply - typically 15-25 names. Does the DCF, the competitive analysis, the model maintenance, and writes the publishable note. This is the Morgan Stanley DCF + Bain competitive lens, run by one person on one sector. (Wall Street Prep; CFA Institute Research Challenge equity-report essentials guide.)
- **Strategist / macro strategist** does the top-down work. Publishes the regime view, asset-class outlook, sector rotation calls. This is the McKinsey macro lens. Goldman's chief equity strategist, Morgan Stanley's CIO, JPM's Marko Kolanovic / Dubravko Lakos-Bujas - these are the strategist seats. (Goldman Sachs Research methodology pages.)
- **Quantitative researcher** at a quant fund (Citadel, Two Sigma, AQR, Renaissance) builds the factor models, runs the screens, calibrates the signals. This is the Goldman screener lens, but on industrial-strength infrastructure with terabytes of clean data. They do not do DCFs. (Citadel Securities QR job description; Carnegie Mellon MSCF career paths.)
- **Trader (execution desk)** handles entries and exits within a mandate set by the PM. They care about slippage, market impact, liquidity, gamma, and the order book - not about whether the stock is fairly valued. This is the closest real analog to the Citadel-technical lens, except real desk traders use far more sophisticated tools than D/W trend and RSI. (Wall Street Prep "Roles in Sales and Trading.")
- **Portfolio manager / allocator** sizes the positions, sets the risk budget, decides what gets bought and how much. This is the Bridgewater + BlackRock lens. The PM does not build the DCF and does not pick the entry tick - they set the policy that constrains both. (CFA Institute portfolio management process: planning -> execution -> feedback.)

So the 8 prompts are essentially LARPing as five different specialists. That is fine - solo operators *do* have to wear all five hats - but it is important to understand that no single human at Goldman or Bridgewater is doing all 8 of these in one sitting. The compression happens at the PM seat, who *consumes* the outputs of the other four specialists and makes the allocation call.

The implication for the boss: when running the unified stack solo, you are the PM. You should *consume* the outputs of the LLM-as-specialist, not believe them uncritically.

---

## Section G: Recommended Workflow for a Solo Operator

A realistic cadence for one person running this stack with LLM tooling:

### Daily (30 minutes total)
- **Macro check (5 min):** Pull current 10-yr yield, VIX, dollar index, oil, S&P futures pre-market. Note any overnight macro data releases. One-sentence regime read.
- **Watchlist news (10 min):** Headlines on each ticker on the active watchlist. Anything unusual? Anything that changes the thesis?
- **Technical scan (15 min):** Daily charts on the watchlist. Mark anything at S/R, anything with a setup, anything that broke a level. Tag candidates for tomorrow.

### Weekly (2-4 hours)
- One or two deep dives on new names. Run Steps 1-10 from Section B for each.
- Update existing thesis pages on current holdings - any data this week that changes the case?
- Review weekly chart on every open position. Anything trending against the thesis?

### Quarterly (4-6 hours)
- Full portfolio review in the Bridgewater style. Correlation matrix on current holdings (Portfolio Visualizer). Sector concentration. Factor concentration (growth/value, large/small, US/ex-US). Drawdown stress test against the last three corrections.
- Re-confirm the IPS (BlackRock lens). Has the target allocation drifted more than 5% from the policy? Rebalance.

### Pre-earnings (1 hour per name)
- Run the JPM template with real data: consensus, implied move, last 4Q reactions, segment focus, options positioning.
- Decision: hold through, trim into, hedge, or close pre-print.

### New holding initiation (3-4 hours)
- Full 10-step workflow from Section B.
- Goldman-style screen for entry, MS-style DCF for fair value, Bain competitive frame for moat.
- Write the one-page thesis before the order is placed, not after.

### A note on tooling
Do not invest in an "AI stock picker" subscription. The leverage is not in better LLMs - it is in better *primary data* feeding the existing LLM. Spend money on (in priority order):
1. **A real screener** (Stock Rover, Koyfin, Finviz Elite) - $20-100/month.
2. **A real chart tool** (TradingView paid) - $20-60/month.
3. **A real fundamentals source** (Stratosphere, Stock Analysis, Tikr) - $20-50/month.
4. **A real news feed** (Benzinga, Seeking Alpha Premium) - $20-30/month.

The LLM is free or nearly so, and it is the *least* important component of the stack. The data is the bottleneck. The prompt templates promise a Goldman-grade analyst on tap; they deliver a structuring engine that needs an actual data pipe behind it.

---

## Closing honesty

LLMs are excellent at structure, scaffolding, and copy-editing. They are dangerous when used as a source of specific financial numbers. The 8 prompt templates are useful as checklists; treat them as such. Verify every number against a primary source before any position is sized. The cost of one fabricated input that survives into a trade is larger than the cost of all the verification work combined.

The 80/20 of this entire document: **layer the analysis top-down, verify every number, and never confuse "the LLM produced confident prose" with "the LLM produced correct data."**

---

## Sources

- Goldman Sachs Research methodology: https://www.goldmansachs.com/what-we-do/research and https://www.goldmansachs.com/insights/goldman-sachs-research
- Morgan Stanley "Everything Is a DCF Model" (Counterpoint Global / Mauboussin): https://www.morganstanley.com/im/en-us/financial-advisor/insights/consilient-observer/everything-is-a-dcf-model.html
- Morgan Stanley "Measuring the Moat" (Counterpoint Global): https://www.morganstanley.com/im/publication/insights/articles/article_measuringthemoat.pdf
- Bridgewater "The All Weather Story": https://www.bridgewater.com/research-and-insights/the-all-weather-story
- BlackRock "Building Resilience: A Framework for Strategic Asset Allocation" (2018): https://www.blackrock.com/corporate/literature/whitepaper/bii-portfolio-perspectives-december-2018.pdf
- BlackRock Strategic Asset Allocation framework: https://www.blackrock.com/uk/professionals/solutions/portfolio-design/a-modernised-toolkit-for-strategic-asset-allocation
- McKinsey Global Economics Intelligence: https://www.mckinsey.com/capabilities/strategy-and-corporate-finance/our-insights/mckinsey-global-economics-intelligence
- McKinsey "Banking on interest rates: A playbook for the new era of volatility": https://www.mckinsey.com/capabilities/risk-and-resilience/our-insights/banking-on-interest-rates-a-playbook-for-the-new-era-of-volatility
- Fidelity "The Business Cycle Approach to Equity Sector Investing": https://www.fidelity.com/bin-public/060_www_fidelity_com/documents/fixed-income/Business_Cycle_Sector_Approach.pdf
- Fidelity Sector Rotation Strategies: https://www.fidelity.com/learning-center/trading-investing/markets-sectors/intro-sector-rotation-strats
- SSGA "How macroeconomic variables impact sector performance": https://www.ssga.com/us/en/individual/insights/how-macroeconomic-variables-impact-sector-performance
- Citadel trading methodology overview: https://www.daytrading.com/citadel-ken-griffin-strategies
- Citadel Securities Quantitative Researcher role: https://www.citadelsecurities.com/careers/details/quantitative-researcher-quantitative-research-analyst/
- CFA Institute Portfolio Management Process: https://analystprep.com/cfa-level-1-exam/portfolio-management/portfolio-management-process/
- CFA Institute Analyst Skills: https://www.cfainstitute.org/programs/cfa-program/candidate-resources/practical-skills-modules/analyst-skills
- CFA Institute Equity Research Report Essentials: https://www.cfainstitute.org/sites/default/files/-/media/documents/support/research-challenge/challenge/rc-equity-research-report-essentials.pdf
- CFA Institute "Practical Guide for LLMs in the Financial Industry": https://rpc.cfainstitute.org/research/the-automation-ahead-content-series/practical-guide-for-llms-in-the-financial-industry
- Porter's Five Forces (Wall Street Prep): https://www.wallstreetprep.com/knowledge/porters-five-forces-model/
- Wall Street Prep "Roles in Sales and Trading": https://www.wallstreetprep.com/knowledge/sales-and-trading-roles-and-asset-classes/
- FINOS AI Governance Framework, Hallucination and Inaccurate Outputs: https://air-governance-framework.finos.org/risks/ri-4_hallucination-and-inaccurate-outputs.html
- Chainlink Blog "The Trust Dilemma: Overcoming LLM Hallucinations in Financial Services": https://blog.chain.link/the-trust-dilemma/
- BizTech Magazine "LLM Hallucinations: Implications for Financial Institutions": https://biztechmagazine.com/article/2025/08/llm-hallucinations-what-are-implications-financial-institutions
- Investor.gov "Thinking of Day Trading? Know the Risks.": https://www.investor.gov/additional-resources/spotlight/directors-take/thinking-day-trading-know-risks
- MIT News on Ken Griffin: https://news.mit.edu/2023/success-intersection-technology-and-finance-0510
