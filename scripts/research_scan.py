"""
DayTrader Research Scan — ScrapeGraphAI-powered.

Scans a curated list of trader/market sources and dumps a structured markdown
brief to C:\\Claude\\DayTrader\\research\\daily-scans\\YYYY-MM-DD.md.

USAGE:
    # Set your LLM key first (one of):
    #   $env:OPENAI_API_KEY = "sk-..."          # for openai/gpt-4o-mini (default)
    #   $env:ANTHROPIC_API_KEY = "sk-ant-..."   # for anthropic (requires extra install)
    # Or use ollama with a local model (free).

    & "C:\\Claude\\ScrapeGraph\\.venv\\Scripts\\python.exe" `
        "C:\\Claude\\DayTrader\\scripts\\research_scan.py"

    # Or override which sources to hit:
    & "...python.exe" research_scan.py --sources market,academy --provider openai

WHAT IT SCANS:
    market   - bloomberg.com/markets, cnbc.com, reuters.com, marketwatch.com
    academy  - investopedia.com (specific articles), babypips.com (graduation/risk)
    signals  - tradingview ideas, mancini-style daily levels via substack
    youtube  - top channels' "Latest" descriptions (lightweight — full vids need transcript fetch)
    insto    - morningstar.com (free moat reports)

Each source is scraped with a focused prompt; the results are concatenated
into one markdown file with timestamps and source attribution.

COSTS:
    openai/gpt-4o-mini ≈ $0.01-0.05 per source per run
    ollama (local llama 3) = $0
    Full scan (all sources): ~$0.05-0.30 with OpenAI, $0 with Ollama
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

try:
    from scrapegraphai.graphs import SmartScraperGraph
except ImportError:
    sys.stderr.write("ERROR: scrapegraphai not installed. Use the venv at C:\\Claude\\ScrapeGraph\\.venv\\\n")
    sys.exit(1)

OUTPUT_DIR = Path(r"/Users/hitanshsharma/Claude/DayTrader/research/daily-scans")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SOURCES = {
    "market": [
        {
            "url": "https://www.bloomberg.com/markets",
            "prompt": (
                "Extract: top 3 market headlines, S&P 500 / Nasdaq / Dow current levels "
                "and % moves if visible, 10-year Treasury yield, oil price. "
                "If paywalled, return 'PAYWALLED' as the value."
            ),
        },
        {
            "url": "https://www.cnbc.com/markets/",
            "prompt": (
                "Extract: top 5 market headlines with one-sentence summary each. "
                "Pre-market or after-hours mover stories. Any Fed-speaker schedule for today."
            ),
        },
        {
            "url": "https://www.marketwatch.com/markets",
            "prompt": (
                "Extract: futures levels (ES, NQ, YM, RTY) and pre-market percentage moves, "
                "top 5 economic calendar items for today, biggest pre-market stock movers up/down."
            ),
        },
    ],
    "academy": [
        {
            "url": "https://www.investopedia.com/articles/active-trading/093014/10-day-trading-tips-beginners.asp",
            "prompt": "Summarize: the 10 day-trading tips. List each in one line.",
        },
        {
            "url": "https://www.babypips.com/learn/forex/undergraduate-senior",
            "prompt": (
                "Summarize: the risk management curriculum from BabyPips Undergraduate Senior. "
                "Extract specific position-sizing rules, drawdown limits, and Kelly references."
            ),
        },
    ],
    "signals": [
        {
            "url": "https://www.tradingview.com/markets/futures/ideas/",
            "prompt": (
                "Extract: top 5 futures trade ideas currently featured. For each: ticker, "
                "long or short, time horizon, and the headline reasoning in one sentence."
            ),
        },
    ],
    "insto": [
        {
            "url": "https://www.morningstar.com/stocks",
            "prompt": (
                "Extract: any wide-moat stock highlights, current 5-star (undervalued) names, "
                "1-star (overvalued) names. If paywalled, return 'PAYWALLED'."
            ),
        },
    ],
    "youtube": [
        # Channel landing pages — descriptions of latest videos
        {
            "url": "https://www.youtube.com/@SMBCapital/videos",
            "prompt": (
                "Extract: the 5 most recent video titles, view counts, and a one-sentence "
                "summary of each based on title alone."
            ),
        },
        {
            "url": "https://www.youtube.com/@traderlion/videos",
            "prompt": "Extract: 5 most recent video titles and one-line summary each.",
        },
    ],
}


def build_config(provider: str) -> dict:
    """Build scrapegraphai config based on chosen LLM provider."""
    if provider == "openai":
        key = os.environ.get("OPENAI_API_KEY")
        if not key:
            raise SystemExit(
                "Set OPENAI_API_KEY env var, or pass --provider ollama for free local."
            )
        return {
            "llm": {
                "api_key": key,
                "model": "openai/gpt-4o-mini",
                "temperature": 0.0,
            },
            "verbose": False,
            "headless": True,
        }
    if provider == "ollama":
        return {
            "llm": {
                "model": "ollama/llama3.2",
                "model_tokens": 8192,
                "temperature": 0.0,
            },
            "verbose": False,
            "headless": True,
        }
    raise SystemExit(f"Unknown provider: {provider}")


def scan_source(item: dict, config: dict) -> dict:
    """Run one source. Return dict with url, ok, data/error."""
    try:
        scraper = SmartScraperGraph(
            prompt=item["prompt"],
            source=item["url"],
            config=config,
        )
        result = scraper.run()
        return {"url": item["url"], "ok": True, "data": result}
    except Exception as e:  # noqa: BLE001 — top-level resilience
        return {"url": item["url"], "ok": False, "error": str(e)[:500]}


def ny_now() -> datetime:
    return datetime.now(ZoneInfo("America/New_York"))


def render_markdown(results_by_category: dict, provider: str) -> str:
    ts_ny = ny_now()
    ts_utc = datetime.now(timezone.utc)
    lines = [
        f"# Daily Research Scan — {ts_ny.strftime('%Y-%m-%d %H:%M')} ET",
        "",
        f"_Run at {ts_utc.isoformat()} UTC. Provider: `{provider}`._",
        "",
        "---",
        "",
    ]
    for category, items in results_by_category.items():
        lines.append(f"## {category.upper()}")
        lines.append("")
        for item in items:
            lines.append(f"### {item['url']}")
            if item["ok"]:
                # Pretty-print the data
                data = item["data"]
                if isinstance(data, (dict, list)):
                    lines.append("```json")
                    lines.append(json.dumps(data, indent=2, default=str))
                    lines.append("```")
                else:
                    lines.append(str(data))
            else:
                lines.append(f"**FAILED:** `{item['error']}`")
            lines.append("")
        lines.append("---")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--sources",
        default="market,academy,signals,insto",
        help="Comma-separated source categories. Default omits youtube (heavy).",
    )
    p.add_argument(
        "--provider",
        default="openai",
        choices=("openai", "ollama"),
        help="LLM provider. openai = better quality; ollama = free local.",
    )
    p.add_argument(
        "--out",
        default=None,
        help="Output file (default: YYYY-MM-DD.md in daily-scans/).",
    )
    args = p.parse_args()

    requested = {s.strip() for s in args.sources.split(",") if s.strip()}
    unknown = requested - set(SOURCES.keys())
    if unknown:
        sys.stderr.write(f"Unknown source categories: {unknown}. Valid: {list(SOURCES)}\n")
        return 1

    config = build_config(args.provider)

    print(f"Scanning categories: {sorted(requested)} (provider={args.provider})")
    results_by_category: dict = {}
    for cat in sorted(requested):
        print(f"  [{cat}] running {len(SOURCES[cat])} source(s)...")
        results_by_category[cat] = [scan_source(item, config) for item in SOURCES[cat]]
        ok = sum(1 for r in results_by_category[cat] if r["ok"])
        print(f"  [{cat}] {ok}/{len(SOURCES[cat])} succeeded")

    markdown = render_markdown(results_by_category, args.provider)
    out_path = (
        Path(args.out) if args.out else OUTPUT_DIR / f"{ny_now().strftime('%Y-%m-%d_%H%M')}.md"
    )
    out_path.write_text(markdown, encoding="utf-8")
    print(f"\nWrote {out_path}")
    print(f"Open with: code '{out_path}'")
    return 0


if __name__ == "__main__":
    sys.exit(main())
