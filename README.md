# EPIC_AGENT_v0_9_2: Three-Agent Stack for BTC Trading

Automatyczny bot tradingowy dla Bitcoin na Binance, oparty na AI (Grok, Copilot, DeepSeek, Qwen, Gemini). Zbiera dane z API (Coinglass, Binance), web scraping (vision-based) i analizuje sentyment dla EV+ trade'ów (expected value positive). Focus: Liquidity grabs, retests, HODL z day tradingiem.

## Architektura
Modularny system w Pythonie:
- **Agents**: BrowserBot (automatyzacja), Agent3 (trade exec), Tactician (dispatcher), Strategist (decyzje AI), Consultants (multi-AI council).
- **Core**: StateOrchestrator (FSM cycle: boot → seed → harvest → synthesis → execution → cooldown).
- **Sensors**: APICollector (Coinglass/Binance), WebCollector (indicators A-F), VisionSensor (screenshots).
- **Utils**: ConfigManager, Logger, Parsers (regex), SignalMessenger (commands).
- **GUI**: Main.py z Tkinter, HUD (statusy/PnL), CalibrationWizard (coordy).

Szczegóły: [docs/architecture.md](docs/architecture.md) (Hamilton-inspired resilience).

## Inspiracje i Analizy
- Three-Agent Stack w HFT: [docs/hft_inspiration.md](docs/IDEA_PLAISANT_GEMINI.md).
- Analiza Groka: Zalążek AGI tradingu – [docs/project_analysis.md](docs/IDEA_PLAISANT_GROK.md).
- Prompty AI: [docs/prompts/](prompts) (INIT_* files).

## Instalacja
1. Python 3.10+.
2. `pip install -r requirements.txt`.
3. Signal-CLI: [setup.md](setup.md).
4. Klucze: intel_config_v33.ini ([docs/api_guide.md](docs/API_DOC_COINCLASS.md) dla Coinglass).
5. Kalibracja: python main.py → Menu → Kalibracja.

## Usage
Szczegóły: [docs/setup.md](docs/setup.md) (uruchomienie, troubleshooting).

## Tests
- python tests/test_strategist.py (AI parsing).
- verify_parser.py (regex orders).

## Audyty i Historia
* - [docs/audits/](Audyt_Grok_v0_9_2.md) (Grok/Gemini reviews, stability 8/10).
- Archive: Technical_Old/ (stare wersje, logi).

## Roadmap
- v0.9.2: API, State Machine
- Więcej: [docs/roadmap.md](docs/roadmap.md). [docs/INSTRUKCJA_OBSŁUGI.md](docs/INSTRUKCJA_OBSŁUGI.md).

Licensed under GPL-3.0 – see [LICENSE](LICENSE).

#bitcoin #Three-Agent-Stack-by-plaisant


