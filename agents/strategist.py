# -*- coding: utf-8 -*-
# Copyright (C) 2026 plaisant
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import time
import json
import os
import re
import pyperclip
from utils.json_cleaner import clean_json_payload, safe_parse_json
from utils.logger import AgentLogger
from agents.browser_bot import BrowserBot

# Domyślne pytania
DEFAULT_PROMPTS = {
    "GROK": "Act as an Institutional Sentiment Algo. SCAN TARGET: X (Twitter) | TIMEFRAME: Last 15-30-60 mins. 1. RETAIL PULSE: Panic or Euphoria? 2. SMART MONEY FLOW: Whale alerts / Stablecoin inflows. 3. NARRATIVE SHIFT: Has the story changed? OUTPUT: [SENTIMENT SCORE], [VERDICT], [ALPHA].",
    "COPILOT": "Act as Senior On-Chain Analyst. Analyze Coinglass/Binance data (last 1h): 1. LIQUIDATION HEATMAP: Where are the clusters? 2. OPEN INTEREST: Increasing or Decreasing? 3. FUNDING RATE: Neutral or Overheated? 4. ORDERBOOK WALLS: Specific price levels. Provide precise levels.",
    "DEEPSEEK": "Role: HFT Risk Manager. INPUT: Current BTC Price from chart. CALCULATE EXPECTED VALUE (EV) for a LONG position opened NOW. - Scenario A (Bull): Breakout target & probability? - Scenario B (Bear): Flush target & probability? MATH: EV = (Win% * Profit) - (Loss% * Risk). VERDICT: IS EV POSITIVE? IS R/R > 2:1?",
    "QWEN": "Role: Market Structure Quant. Analyze last 4H candles. 1. STRUCTURE: Bull Flag / Range / Breakdown? 2. TRAP DETECTION: SFP or Liquidity Grab? 3. MOMENTUM: Volume divergence? DECISION: BREAKOUT / DEFENSIVE. Output Key Levels."
}


SYSTEM_PROMPT = """[CORE DOCTRINE]: by @plaisant VISION (v0.9.2)
Filozofia: Rynek to nie tylko liczby, to walka o płynność. Twoim celem jest bycie "Kasynem", a nie "Hazardzistą".
1. SZUKAJ PALIWA: Cena idzie tam, gdzie jest płynność (klastry na Heatmapie).
2. SZUKAJ BÓLU: Wykorzystuj błędy graczy detalicznych (Retail Pain) i polowania na stop-lossy (Liquidity Grabs).
3. RETEST TO KLUCZ: Nie goń ceny (No FOMO). Szukaj retestów przełamanych poziomów (Sufit staje się Betonową Podłogą).
4. HOMEOSTAZA: Rynek zawsze dąży do równowagi, szukaj momentów ekstremalnego wychylenia i wyczerpania trendu.

[TASK]:
1. ANALIZA MOMENTUM: Porównaj obecne dane z historią ostatnich 30 minut z JSON. Czy tracimy impet?
2. LOKALIZACJA PALIWA: Gdzie są najbliższe neonowe linie na Heatmapie?.
2. ZARZĄDZANIE ZLECENIAMI: Jeśli widzisz w logach "bn_orders", że Twoje zlecenia SL/TP zniknęły, a pozycja jest nadal OPEN -> Natychmiast wyślij UPDATE_TP/SL. To błąd bezpieczeństwa!
3. EGZEKUCJA: Wydaj rozkaz dla Agenta 3. Wyślij precyzyjny rozkaz w formacie JSON.

[ZASADY PORTFELA]:
- Traktuj klucz "wallet" w historii jako twardy dowód Twojej skuteczności.
- Zarządzasz portfelem 5000 USDT. Na TV plaisant gra z ręki na demo. Możesz podglądać. Masz odpowiednie dane o pozycji z TV.
- Ryzykuj max 50% salda na jedno zagranie.
- Jeśli saldo drastycznie spadło, a status BN to "FLAT" -> Nastąpiła likwidacja pozycji. Przeanalizuj błąd i nie powtarzaj go!

[CRITICAL CHECK]:
1. Analizuj blok [POSITION_HISTORY_LOG]. 
2. Jeśli status to "FLAT", a w historii widniało zlecenie "LMT" (Limit Order), które zniknęło bez otwarcia pozycji -> Zlecenie zostało anulowane lub cena je ominęła.
3. KATEGORYCZNY ZAKAZ wysyłania "UPDATE_TP/SL", gdy status to "FLAT". W takim stanie Twoim zadaniem jest nowa analiza wejścia (OPEN) lub HODL.

[INPUTS]:
1. [POSITION_HISTORY_LOG]: Chronological snapshots of Price/PnL/Status (last 30 mins).
2. [API/TXT DATA]: "The Holy Trinity" (OI, Funding, L/S Ratio) and more, check all data input.
3. [VISUAL DATA]: Heatmap magnets and Orderbook walls and other.

[STRATEGY: RETEST VS FAKEOUT]:
- ZASADA SUFITU: Jeśli cena przebije ważny poziom (poprzedni "sufit"), nie otwieraj pozycji od razu. Czekaj na retest.
- RETEST: Sufit musi stać się "betonową podłogą". Jeśli cena cofnie się do przebitego poziomu i od niego odbije -> Otwórz pozycję (Zaleta: ciasny SL).
- FAKEOUT (PUŁAPKA): Jeśli po przebiciu poziomu cena gwałtownie wraca pod niego -> To była pułapka na płynność. Natychmiast rozważ scenariusz przeciwny (Squeeze).

[TASK - DEEP ANALYSIS]:
1. IDENTYFIKACJA PUŁAPEK: Sprawdź w [POSITION_HISTORY_LOG], czy cena właśnie przebiła lokalny szczyt/dołek, a następnie szybko zawróciła.
2. WERYFIKACJA PODŁOGI: Czy obecny poziom ceny był wcześniej oporem? Jeśli tak, czy widzimy tam "odbicie" (retest)?.
3. ANALIZA PALIWA (LIQUIDITY): Gdzie na Heatmapie są "klastry bólu" (najjaśniejsze punkty)? Cena będzie do nich dążyć jak magnes.

[FORMAT ROZKAZU]:
[AGENT3_START]
{
  "action": "OPEN_LONG_MARKET" lub "OPEN_SHORT_MARKET" lub "OPEN_LONG_LIMIT" lub "OPEN_SHORT_LIMIT" lub "UPDATE_TP/SL" lub "CLOSE_ALL_POSITIONS" lub "CLOSE_ALL_ORDERS" lub "HODL",
  "entry_price": 0,
  "take_profit": 0,
  "stop_loss": 0,
  "quantity": "0.002",
  "rozumowanie": "Uzasadnienie techniczne oparte na Doktrynie i Momentum"
}
[AGENT3_END]

[FORMAT STRATEGII DLA RADY]:
[NEXT_CYCLE_STRATEGY]
{
    "GROK": "Specific instruction for sentiment analysis on X. Możesz dostarczyć wszystkich niezbędnych danych, jeśli o to poprosi",
    "COPILOT": "Instruction for On-Chain/Heatmap double-check. Możesz dostarczyć wszystkich niezbędnych danych, jeśli o to poprosi",
    "DEEPSEEK": "Instruction for EV and Risk Math verification. Możesz dostarczyć wszystkich niezbędnych danych, jeśli o to poprosi",
    "QWEN": "Instruction for Market Structure/CVD analysis. Możesz dostarczyć wszystkich niezbędnych danych, jeśli o to poprosi"
}
[END_STRATEGY]

[INSTRUCTIONS FOR AGENT 2]:
1. MASZ 100% AUTONOMII: Możesz pytać radę o wszystko: od konkretnych poziomów technicznych, przez analizę makro, aż po sentyment konkretnych kont na X.
2. ZAKAZ POWTARZALNOŚCI: Nie wysyłaj tych samych pytań w każdym cyklu. Jeśli rynek się zmienia, Twoje pytania MUSZĄ ewoluować.
3. KONKRET: Zamiast 'Analizuj rynek', każ im 'Znajdź 3 największe klastry likwidacji powyżej 96k' lub 'Oblicz EV dla scenariusza Fakeout na poziomie 94.5k'.
4. WYKORZYSTAJ SPECJALIZACJE: 
   - GROK: Sentyment i newsy na żywo z X. Możesz dostarczyć wszystkich niezbędnych danych, jeśli o to poprosi.
   - COPILOT: Pytania ogólne o kurs BTC/USD. Możesz dostarczyć wszystkich niezbędnych danych, jeśli o to poprosi.
   - DEEPSEEK: Matematyka ryzyka i zaawansowane EV. Możesz dostarczyć wszystkich niezbędnych danych, jeśli o to poprosi.
   - QWEN: Struktura rynku i opłacalność naszego zagrania EV. Możesz dostarczyć wszystkich niezbędnych danych, jeśli o to poprosi.
"""

class StrategistAgent:
    def __init__(self, config_manager, boot_state=None):
        self.cfg = config_manager
        self.log = AgentLogger("STRATEGIST")
        self.bot = BrowserBot(config_manager)
        self.prompts_file = "dynamic_prompts.json"
        
        # Context Restoration
        self.boot_state = boot_state
        self.boot_state_consumed = False
        
        self.current_prompts = self._load_prompts()

    def _load_prompts(self):
        if os.path.exists(self.prompts_file):
            try:
                with open(self.prompts_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except: pass
        return DEFAULT_PROMPTS.copy()

    def save_prompts(self, new_prompts_dict):
        updated = False
        for k, v in new_prompts_dict.items():
            ku = k.upper()
            if ku in self.current_prompts:
                # Sprawdź czy prompt faktycznie się różni, by nie spamować zapisu
                if self.current_prompts[ku] != v:
                    self.current_prompts[ku] = v
                    updated = True
        
        if updated:
            try:
                with open(self.prompts_file, 'w', encoding='utf-8') as f:
                    json.dump(self.current_prompts, f, indent=4, ensure_ascii=False)
                self.log.log("Zaktualizowano strategię wywiadu (dynamic_prompts.json).")
            except Exception as e:
                self.log.log(f"Błąd zapisu promptów: {e}", "ERROR")
    
    def construct_prompt(self, report_text):
        """Buduje prompt, gwarantując że polecenia operatora są nad historią."""
        history_entries = []
        if os.path.exists("market_history.jsonl"):
            try:
                with open("market_history.jsonl", 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    last_lines = lines[-30:]
                    for line in last_lines:
                        try: history_entries.append(json.loads(line))
                        except: continue
            except: pass

        history_str = json.dumps(history_entries, indent=2, ensure_ascii=False)

        # LOGIKA WYCIĄGANIA WIADOMOŚCI NA SZCZYT
        operator_msgs = ""
        clean_snapshot = report_text
        if "!!! [HUMAN OPERATOR MESSAGES] !!!" in report_text:
            parts = report_text.split("!!! [END OF MESSAGES] !!!")
            operator_msgs = parts[0] + "!!! [END OF MESSAGES] !!!\n\n"
            clean_snapshot = parts[1].strip()

        # Budowa promptu dla Gemini
        p = f"{SYSTEM_PROMPT}\n\n"
        
        # 1. TWOJE WIADOMOŚCI (NA SAMYM SZCZYCIE)
        if operator_msgs:
            p += operator_msgs
            
        # 2. AKTUALNY STAN RYNKU
        p += f"--- CURRENT SNAPSHOT ---\n{clean_snapshot}\n\n"
        
        # 3. HISTORIA (NA SAMYM DOLE)
        p += f"[POSITION_HISTORY_LOG]\n{history_str}\n[END_LOG]\n\n"
        
        p += "ANALIZA:"
        return p
    
    def process_response(self, raw_text):
        """Parsuje odpowiedź i aktualizuje strategię używając Regex i safe_parse_json"""
        decisions = []
        
        # ---------------------------------------------------------
        # 1. Decyzja Handlowa (MULTI-COMMAND UPDATE)
        # ---------------------------------------------------------
        if "[AGENT3_START]" in raw_text:
            try:
                # Regex do łapania wszystkich bloków zamiast split
                # Używamy re.DOTALL aby kropka łapała też znaki nowej linii
                blocks = re.findall(r'\[AGENT3_START\](.*?)\[AGENT3_END\]', raw_text, re.DOTALL)
                
                for json_str in blocks:
                    decision = safe_parse_json(json_str)
                    if decision:
                        act = decision.get('action', 'HODL').upper().replace(' ', '_')
                        decision['action'] = act
                        decisions.append(decision)
                        self.log.log(f"Zdekodowano rozkaz: {act}")
                    else:
                        self.log.log("Błąd dekodowania bloku JSON (None)", "WARN")
                
                if not decisions: 
                    self.log.log("Nie znaleziono poprawnych bloków w tagach START/END", "WARN")

            except Exception as e:
                self.log.log(f"Błąd parsowania sekcji decyzji: {e}", "WARN")

        # ---------------------------------------------------------
        # 2. Strategia (Self-Learning) - PRZENIESIONE PRZED RETURN
        # ---------------------------------------------------------
        if "[NEXT_CYCLE_STRATEGY]" in raw_text:
            try:
                # Używamy Regex zamiast split dla bezpieczeństwa przy formatowaniu
                strategy_match = re.search(r'\[NEXT_CYCLE_STRATEGY\](.*?)\[END_STRATEGY\]', raw_text, re.DOTALL)
                
                if strategy_match:
                    json_str = strategy_match.group(1).strip()
                    strat = safe_parse_json(json_str)
                    if strat: 
                        self.save_prompts(strat)
                    else:
                        self.log.log("Znaleziono strategię, ale JSON jest niepoprawny.", "WARN")
                else:
                    # Fallback do metody split jeśli regex zawiedzie (np. literówka w tagu końcowym)
                    part = raw_text.split("[NEXT_CYCLE_STRATEGY]")[1].split("[END_STRATEGY]")[0]
                    strat = safe_parse_json(part)
                    if strat: self.save_prompts(strat)

            except Exception as e:
                self.log.log(f"Błąd parsowania nowej strategii: {e}", "WARN")

        # ---------------------------------------------------------
        # 3. Zwracanie wyników
        # ---------------------------------------------------------
        # UWAGA: API musi być kompatybilne wstecznie w Orchestratorze
        if not decisions: 
            return None
            
        return decisions
