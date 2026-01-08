# Contributing to EPIC_AGENT_v0_9_2

Dzięki za zainteresowanie! Projekt to open-source bot tradingowy (Three-Agent Stack) – forkuj, testuj na demo, zgłaszaj issues. Focus: Stability, EV+ trading, AI integration. GPL-3.0 – modyfikacje muszą być otwarte.

## Jak Wnieść Wkład
1. **Fork & Clone**: `git clone https://github.com/YOUR_USERNAME/EPIC_AGENT_v0_9_2.git`.
2. **Branch**: `git checkout -b feature/new-api`.
3. **Zmiany**:
   - Kod: Pythonic, modularny. Dodaj testy (tests/).
   - Docs: Uaktualnij README/docs (np. audyty w docs/audits/).
   - AI: Nowe prompty w docs/prompts/, testuj self-learning.
   - Trading: EV+ focus, test na history.jsonl.
4. **Commit**: `git commit -m "Fix error recovery in FSM"`.
5. **Push & PR**: Opisz changes, tests, issue ref.

## Zasady
- **Stability First**: Nie łam FSM. Użyj try/except, loggery.
- **AI Prompts**: Testuj w INIT_*.md, update dynamic_prompts.json.
- **Trading Rules**: Max 50% wallet, liquidity grabs.
- **Issues**: Bugs z logami, features z [roadmap.md](docs/roadmap.md).
- **Community**: Wykop (#plaisant_stack) lub issues.

## Setup dla Contrib
- `pip install -r requirements.txt`.
- Kalibracja: main.py → Kalibracja.
- Testy: test_strategist.py, verify_parser.py.

Kontakt: @plaisant na Wykop. Budujmy AGI trading razem! 😎