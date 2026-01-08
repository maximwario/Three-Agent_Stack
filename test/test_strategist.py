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
import re
import json
import logging

# Mock dependencies
class MockConfig:
    def get(self, *args, **kwargs): return None

class MockBot:
    def __init__(self, *args): pass

class MockLogger:
    def log(self, msg, level="INFO"): print(f"[{level}] {msg}")

def safe_parse_json(json_str):
    try:
        return json.loads(json_str)
    except:
        return None

# Simplified StrategistAgent for testing
class StrategistAgent:
    def __init__(self):
        self.log = MockLogger()
        self.prompts_file = "dynamic_prompts.json"
        self.current_prompts = {}

    def save_prompts(self, new_prompts_dict):
        print("SAVING PROMPTS:", new_prompts_dict)
        self.current_prompts.update(new_prompts_dict)

    def process_response(self, raw_text):
        decisions = []
        if "[AGENT3_START]" in raw_text:
            try:
                blocks = re.findall(r'\[AGENT3_START\](.*?)\[AGENT3_END\]', raw_text, re.DOTALL)
                print(f"DEBUG: Found {len(blocks)} blocks")
                for json_str in blocks:
                    decision = safe_parse_json(json_str)
                    if decision:
                        act = decision.get('action', 'HODL').upper().replace(' ', '_')
                        decision['action'] = act
                        decisions.append(decision)
                        self.log.log(f"Zdekodowano rozkaz: {act}")
                    else:
                        self.log.log("Błąd dekodowania bloku JSON (None)", "WARN")
                
                if not decisions: self.log.log("Nie znaleziono poprawnych bloków w tagach START/END", "WARN")

            except Exception as e:
                self.log.log(f"Błąd parsowania sekcji decyzji: {e}", "WARN")

        if "[NEXT_CYCLE_STRATEGY]" in raw_text:
            try:
                part = raw_text.split("[NEXT_CYCLE_STRATEGY]")[1].split("[END_STRATEGY]")[0]
                print(f"DEBUG: Extracted strategy part: {part[:50]}...")
                strat = safe_parse_json(part)
                if strat: 
                    self.save_prompts(strat)
                else:
                    print("DEBUG: safe_parse_json returned None for strategy")
            except Exception as e: 
                print(f"DEBUG: Strategy parsing exception: {e}")
                pass

        if not decisions: return None
        return decisions

# TEST DATA
raw_text = """**/// SYSTEM STATUS: ONLINE**
**/// ID: AGENT 2 (STRATEGIST)**
**/// INPUT DATA: MULTI-AGENT REPORTS + HARD MARKET DATA**
**/// MODE: DEFENSIVE HOLD WITH BULLISH UNDERTONES**

---

### 1. SYNTEZA SYTUACYJNA (SITREP)

**Status Pozycji:**
* **Entry:** 89,053.90 | **Price:** 88,612.00 (Hard Data) | **PNL:** Ujemny (-0.47$), ale bez paniki.
* **Drawdown:** Nadal siedzimy pod wodą, testując wytrzymałość strefy 88,600 - 88,800.

**Analiza Strukturalna (The Hidden Buy):**
* **CVD Divergence (Alpha Alert):** Qwen wykrył **silną byczą dywergencję na CVD**. Cena spada, ale CVD rośnie (netto +32,500 BTC w delcie). To oznacza, że ktoś agresywnie kupuje (market buy orders), ale cena jest trzymana w ryzach przez pasywne zlecenia sprzedaży (Iceberg Orders). To klasyczna **ukryta akumulacja**.
* **Whale Wall Defense:** Copilot potwierdza, że na poziomie **88,800 USDT** widać "Passive Buying" – zlecenia limit, które nie znikają po uderzeniu. To jest nasza kotwica. Instytucje bronią tego poziomu.
* **Funding Rate Drop:** Funding spadł do **-0.0010%**. To pogłębia negatywny sentyment (shorty płacą longom), co w połączeniu z ukrytą akumulacją (CVD) tworzy idealne warunki pod **Squeeze**.
* **DeepSeek's Math:** Mimo że EV jest bliskie zera (-$50), DeepSeek przyznaje, że scenariusz odbicia do 89,800 ma 50% szans. Biorąc pod uwagę ukrytą akumulację (której on nie widział w swoim modelu), realne prawdopodobieństwo jest wyższe.

**Decyzja Strategiczna:**
Trzymamy. Mamy konfluencję trzech potężnych sygnałów byczych:
1.  **Ujemny Funding** (Shorty są po złej stronie).
2.  **Rosnące CVD przy spadku ceny** (Ukryty popyt).
3.  **Pasywna Obrona 88,800** (Instytucjonalna podłoga).

Wyrzucenie pozycji teraz byłoby zignorowaniem twardych danych o przepływie zleceń.

---

### 2. ROZKAZ DLA AGENTA 3 (EXECUTION)

Bez zmian. Cierpliwość to teraz nasza przewaga.

[AGENT3_START]
{
  "action": "HODL",
  "entry_price": 89053,
  "take_profit": 90100,
  "stop_loss": 88400,
  "quantity": "0.002"
}
[AGENT3_END]

*Uzasadnienie:*
* **HODL:** Nie ruszamy SL (88,400), bo jest poniżej strefy akumulacji 88,800. Nie ruszamy TP, bo squeeze może być gwałtowny.

---

### 3. STRATEGIA NA NASTĘPNY CYKL (NEXT_CYCLE_STRATEGY)

Musimy wiedzieć, kiedy ta "sprężyna" pęknie.

[NEXT_CYCLE_STRATEGY]
{
    "GROK": "Analizuj frazy 'Hidden Buying' i 'Divergence'. Czy analitycy on-chain na X zaczynają zauważać to, co my widzimy w CVD? Jeśli tak, tłum może zacząć front-runnować.",
    "COPILOT": "Skup się na poziomie 89,200. Czy widzisz tam ścianę sprzedaży (Ask Wall), która blokuje wyjście? Jeśli ta ściana zniknie (będzie zdjęta), to droga do 90k stanie otworem.",
    "DEEPSEEK": "Scenariusz 'V-Shape Recovery': Jeśli cena wróci powyżej 89,000 w ciągu 15 minut, jak zmienia się Twoje wyliczenie EV? Czy wtedy bias zmienia się na Bullish?",
    "QWEN": "Monitoruj 'Taker Buy Volume' w 1-minutowych oknach. Szukaj nagłego skoku (spike) powyżej 500 BTC. To będzie sygnał, że akumulacja przeszła w fazę egzekucji (Mark-up)."
}
[END_STRATEGY]"""

agent = StrategistAgent()
result = agent.process_response(raw_text)
print("FINAL RESULT DECISIONS:", result)
