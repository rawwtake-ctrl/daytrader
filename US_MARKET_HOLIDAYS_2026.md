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
