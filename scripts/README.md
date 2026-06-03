# DayTrader Scripts

## research_scan.py — ScrapeGraphAI-powered daily scan

Scrapes a curated set of market + academy + signals + institutional sources, asks an LLM to extract structured data from each, and writes a markdown brief.

### Setup (one-time)

You need an LLM API key. Cheapest path:

```powershell
# OpenAI (recommended — gpt-4o-mini is ~$0.15/1M tokens)
$env:OPENAI_API_KEY = "sk-..."

# OR fully free: install Ollama + llama3.2 locally
# https://ollama.com/download — then run: ollama pull llama3.2
```

### Usage

```powershell
# Default scan (market + academy + signals + insto, skipping heavy youtube)
& "C:\Claude\ScrapeGraph\.venv\Scripts\python.exe" "C:\Claude\DayTrader\scripts\research_scan.py"

# Just market data
& "...python.exe" research_scan.py --sources market

# Free local provider
& "...python.exe" research_scan.py --provider ollama

# Custom output path
& "...python.exe" research_scan.py --out C:\tmp\my-scan.md
```

### Output

Lands in `C:\Claude\DayTrader\research\daily-scans\YYYY-MM-DD_HHMM.md`.

### Cost per run

| Provider | All sources | Just market |
|---|---|---|
| openai/gpt-4o-mini | ~$0.05-0.30 | ~$0.02-0.10 |
| ollama (local) | $0 | $0 |

### Schedule it (Windows Task Scheduler)

```powershell
# Run weekday mornings at 07:00 ET
schtasks /create /tn "DayTrader Morning Scan" /tr `
    "'C:\Claude\ScrapeGraph\.venv\Scripts\python.exe' 'C:\Claude\DayTrader\scripts\research_scan.py'" `
    /sc weekly /d MON,TUE,WED,THU,FRI /st 07:00 /f
```

### Honest limits

- **Paywalled sites** (Bloomberg sometimes, Morningstar premium) will return "PAYWALLED" or empty data
- **JS-heavy sites** (TradingView ideas) work via Playwright but slow
- **YouTube** descriptions only — full video transcripts need a separate yt-dlp + Whisper pipeline (skip by default)
- **The LLM still hallucinates** specific numbers — verify any actionable data against a primary source
