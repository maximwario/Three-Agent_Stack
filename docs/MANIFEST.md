📜 MANIFEST PROJEKTU: PERCEPTRON (Three-Agent Stack)
CEL: Stworzenie autonomicznego systemu tradingowego (HFT/Mid-Freq) opartego na architekturze wieloagentowej, działającego na lokalnym sprzęcie (Desktop) z wykorzystaniem modeli LLM jako warstwy decyzyjnej.

ARCHITEKTURA (The Stack):

AGENT 1 (The Executor/Orchestrator): Warstwa Python. Zarządza cyklem życia, zbiera dane (API + Vision), obsługuje pętlę zdarzeń. Musi być pancerny (error handling z v8.4).

AGENT 2 (The Strategist): Warstwa LLM (Gemini 3/Grok). Analizuje niepełne informacje (screenshoty, sentyment). Generuje strategię (JSON) i samouczące się prompty (dynamic_prompts.json). Kieruje się "Doktryną Plaisanta" (EV over Emotion, Liquidity Engineering).

AGENT 3 (The Tactician): Warstwa Egzekucji. Hybryda API (ccxt) i GUI Automation (pyautogui). Wykonuje zlecenia (OPEN, CLOSE, UPDATE, CANCEL) w sposób ukryty lub bezpośredni.

ZASADY ROZWOJU (Development Rules):

Stabilność ponad Feature'y: Używamy mechanizmów try-except i json cleaning z wersji v8.4. Błąd JSONA nie może zatrzymać bota.

Modułowość: Kod jest podzielony na sensors, agents, core. Nie tworzymy monolitów.

Hybrid Data: Łączymy twarde dane (Binance API via ccxt) z miękkimi danymi wizualnymi (Screenshoty Heatmap/Orderbooków).

Bezpieczeństwo: FAILSAFE = True (z opcją pauzy), limity wielkości pozycji hardcoded w configu.

AKTUALNY STATUS: v0.2.7 (Gemini mówi żeby napisać tu v0.3.0, instrukcje dla Gemini 3 Low Antygravity były aż do v0.3.1)