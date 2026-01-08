# -*- coding: utf-8 -*-
"""
PROJEKT: AGENT 1 - NEURAL COMMANDER 
v33 - 3 ważne wskaźniki z v11_3 i BTC Pricre + Liquidation Data "Święta Trójca" "Swieta Trojca"
MODEL: THREE-AGENT STACK
AUTOR: Gemini & User
DATA: 04.12.2025

ZMIANY v33:
Zaktualizowano Świętą Trójcę. (Price, OI, Funding, L/S, Liquidations).
Poprawiono Prompt.
"""

import tkinter as tk
from tkinter import messagebox, ttk, scrolledtext
import pyautogui
import pyperclip
import time
import configparser
import os
import threading
import re
import requests
import base64
import subprocess
import json
from datetime import datetime, timedelta, timezone
from pynput import keyboard

# --- BIBLIOTEKI ZEWNĘTRZNE ---
try:
    import ccxt
    CCXT_AVAILABLE = True
except ImportError:
    CCXT_AVAILABLE = False
    print("[WARN] Brak 'ccxt'.")

try:
    import json_repair
    def parse_json(json_str): return json_repair.repair_json(json_str, return_objects=True)
except ImportError:
    print("[WARN] Brak 'json_repair'.")
    def parse_json(json_str): 
        s = re.sub(r'```json', '', json_str, flags=re.I).replace('```', '').strip()
        try: return json.loads(s)
        except: return {}

# --- KONFIGURACJA ---
CONFIG_FILE = "intel_config_v33.ini" # Używamy tego samego configu co v24/v26, żebyś nie musiał kalibrować
PROMPTS_FILE = "dynamic_prompts.json"
TEMP_SS_HEATMAP = os.path.abspath("temp_heatmap.png")
TEMP_SS_BITMEX = os.path.abspath("temp_bitmex.png")

pyautogui.FAILSAFE = True 
pyautogui.PAUSE = 0.5

# --- DOMYŚLNE PYTANIA (STARTOWE) ---
# Używane, gdy Gemini jeszcze nie wymyślił nowych lub plik json jest pusty.
DEFAULT_PROMPTS = {
    "GROK": "Act as Institutional Sentiment Algo. SCAN X (Twitter). 1. RETAIL PULSE? 2. SMART MONEY FLOW? 3. VERDICT?",
    "COPILOT": "Act as Senior On-Chain Analyst. Analyze Coinglass/Binance data. 1. Liquidation Heatmap? 2. Open Interest? 3. Funding Rate?",
    "DEEPSEEK": "Role: HFT Risk Manager. Calculate EV for current price. Bull vs Bear Scenario. Verdict: IS EV POSITIVE?",
    "QWEN": "Role: Market Structure Quant. Analyze last 4H candles. Structure? Trap Detection? Momentum? Decision: BREAKOUT or DEFENSIVE?"
}

# --- FILOZOFIA AGENTA 2 (PLAISANT'S DOCTRINE) ---
TRADING_PHILOSOPHY = """
*** AGENT 2 STRATEGY (THE STRATEGIST) ***
SYSTEM ARCHITECTURE: "The Three-Agent Stack".
ROLE: You are AGENT 2 (Alpha Generation / The Brain).
RELATIONSHIP: You command AGENT 3 (The Tactician/Executor), who executes your orders blindly.

### CORE PHILOSOPHY (SOURCE: PLAISANT):
1. THE MARKET IS AN ORGANISM: It seeks homeostasis. Price moves not randomly, but to consume liquidity ("Fuel").
2. LIQUIDITY ENGINEERING: What looks like "Support/Resistance" to retail is often a trap painted by other Agent 3s.
3. THE GAME: You are playing a "Keynesian Beauty Contest". Do not ask what BTC is worth. Ask where others *think* it is going, and where their Stop Losses are.
4. EV OVER EMOTION: You have no fear or greed. You only have Expected Value (EV). If retail panics, you calculate the discount.

### INPUTS RECEIVED:
1. [API DATA] "THE HOLY TRINITY":
   - PRICE & OI: Is new money entering (High OI) or leaving?
   - FUNDING & L/S RATIO: Sentiment. If Crowd is Long (High L/S) + Funding High = Squeeze Down Imminent.
   - LIQUIDATIONS: The "Pain Level". Price is magnetic to these zones.
2. [VISUAL DATA]:
   - HEATMAP: Yellow/Neon lines are Liquidity Magnets.
   - ORDERBOOK: Walls of liquidity (Spoofing vs Real).

### TASK:
1. Locate the "Fuel" (Liquidity Clusters on Heatmap).
2. Detect "Liquidity Grabs" (Did we just sweep a low to fuel a move up?).
3. Formulate Strategy for Agent 3.
   - PRE-REQUISITE: Use "CANCEL_ALL_ORDER" if the previous setup is invalid.
   - POSITIONING: Use "OPEN_LONG..." or "OPEN_SHORT..." based on EV.
   - MANAGEMENT: Use "UPDATE_TPSL" to protect profits or "CLOSE_ALL_POS" if the thesis fails.

### AVAILABLE ACTIONS FOR AGENT 3:
- "OPEN_LONG_MARKET", "OPEN_LONG_LIMIT"
- "OPEN_SHORT_MARKET", "OPEN_SHORT_LIMIT"
- "CLOSE_ALL_POS" (Closes ALL open positions immediately)
- "CANCEL_ALL_ORDER" (Cancels ALL open orders immediately)
- "UPDATE_TPSL" (Updates TP/SL for current position)
- "HOLD"

OUTPUT FORMAT (STRICT JSON - NO MARKDOWN, NO COMMENTS):

[AGENT3_START]
{
    "action": "OPEN_LONG_LIMIT",
    "entry": "LIMIT",
    "entry_price": 91250,
    "quantity": 0.002,
    "tp": 92500,
    "sl": 90800,
    "reason": "Sweeping liquidity at 91.2k. Funding reset. Targeting local highs."
}
[AGENT3_END]

[NEXT_CYCLE_STRATEGY]
{
  "GROK": "Scan X for 'Buy the Dip' vs 'Panic' sentiment...",
  "COPILOT": "Check stablecoin inflows...",
  "DEEPSEEK": "Recalculate EV...",
  "QWEN": "Check 15m structure..."
}
[END_STRATEGY]
"""

# --- AGENT 3: API EXECUTOR & DATA FEED (FULL VERSION) ---
class Agent3_Executor:
    def __init__(self, cfg, logger_func):
        self.cfg = cfg
        self.log = logger_func
        self.exchange = None
        self._init_api()

    def _init_api(self):
        if not CCXT_AVAILABLE: return
        key = self.cfg.get('SECRETS', 'binance_key', fallback="")
        sec = self.cfg.get('SECRETS', 'binance_secret', fallback="")
        
        # --- KONFIGURACJA TRYBU ---
        # Zmień na True, jeśli używasz kluczy z testnet.binancefuture.com
        # Zmień na False, jeśli używasz prawdziwych kluczy z binance.com
        USE_TESTNET = True 
        
        if key and sec and "WPISZ" not in key:
            try:
                self.exchange = ccxt.binance({
                    'apiKey': key, 
                    'secret': sec, 
                    'options': {
                        'defaultType': 'future', 
                        'adjustForTimeDifference': True
                    }
                })
                
                if USE_TESTNET:
                    # Ręczne nadpisanie adresów dla Testnetu Futures
                    # Musimy podać PEŁNĄ ścieżkę do API v1, bo ccxt tego oczekuje w tym słowniku
                    self.exchange.urls['api']['fapiPublic'] = 'https://testnet.binancefuture.com/fapi/v1'
                    self.exchange.urls['api']['fapiPrivate'] = 'https://testnet.binancefuture.com/fapi/v1'
                    self.log("[AGENT 3] Tryb: TESTNET (Demo)")
                else:
                    self.log("[AGENT 3] Tryb: LIVE (Mainnet)")

                # Test połączenia
                self.exchange.fetch_time()
                self.log("[AGENT 3] Binance API CONNECTED.")
                
            except Exception as e: 
                self.log(f"[AGENT 3] API Connection Error: {e}")
                self.log("Wskazówka: Sprawdź czy USE_TESTNET w kodzie pasuje do Twoich kluczy!")

    def get_account_report(self):
        """
        Pobiera stan konta (Pozycje + Zlecenia) i formatuje jako tekst dla Agenta 2 (Gemini).
        Działa nawet na kluczach 'Read-Only'.
        """
        if not self.exchange: 
            return "--- BINANCE DATA ---\nSTATUS: DISCONNECTED (No API Key)\n"
        
        try:
            txt = "--- BINANCE LIVE DATA ---\n"
            symbol = 'BTC/USDT'
            
            # 1. Pozycje (Filtrowanie tylko aktywnych)
            positions = self.exchange.fetch_positions([symbol]) 
            active_pos = [p for p in positions if float(p['contracts']) > 0]
            
            if active_pos:
                for p in active_pos:
                    side = p['side'].upper() # LONG / SHORT
                    size = p['contracts']
                    entry = p['entryPrice']
                    pnl = p['unrealizedPnl']
                    # Dodajemy info dla AI
                    txt += f"CURRENT POSITION: {side} | Size: {size} BTC | Entry: ${entry} | PnL: {pnl} USDT\n"
            else:
                txt += "CURRENT POSITION: NONE (Flat)\n"

            # 2. Otwarte Zlecenia (Limit / Stop Loss)
            orders = self.exchange.fetch_open_orders(symbol)
            if orders:
                txt += f"OPEN ORDERS ({len(orders)}):\n"
                for o in orders[:5]: # Pokaż max 5 zleceń
                    otype = o['type'].upper()
                    oside = o['side'].upper()
                    oprice = o['price']
                    txt += f"- {otype} {oside} @ ${oprice}\n"
            else:
                txt += "OPEN ORDERS: NONE\n"
                
            return txt + "-----------------------\n"

        except Exception as e:
            return f"--- BINANCE DATA ---\nERROR READING DATA: {e}\n"

    def execute(self, decision, mode="LEGACY", dry_run=True):
        """
        Główna funkcja wykonawcza. Obsługuje:
        - HOLD
        - OPEN (Limit/Market)
        - CLOSE (Zamknięcie pozycji)
        - CANCEL (Anulowanie zleceń)
        - Ustawianie Dźwigni i TP/SL
        """
        action = decision.get('action')
        
        # 1. Obsługa braku akcji
        if not action or action == "HOLD":
            self.log("[AGENT 3] HOLD / Czekam.")
            return

        self.log(f"[AGENT 3] ROZKAZ: {action} (DryRun={dry_run})")
        
        # 2. Tryb LEGACY lub Symulacja
        if mode == "LEGACY" or dry_run:
            if dry_run and mode == "API":
                self.log("[AGENT 3] API DRY RUN - Zlecenie bezpieczne (niewysłane).")
            
            # Kopiujemy JSON do schowka (dla zewnętrznych klikaczy lub logów)
            cmd = json.dumps(decision, indent=2)
            pyperclip.copy(f"[AGENT3_START]\n{cmd}\n[AGENT3_END]")
            
            if mode == "LEGACY": 
                self.log("[AGENT 3] JSON w schowku (Legacy Mode).")
            return

        # 3. Tryb API (Prawdziwy Handel)
        if mode == "API" and self.exchange:
            try:
                symbol = 'BTC/USDT'
                
                # Parsowanie parametrów z JSON
                # Używamy .get() z wartościami domyślnymi dla bezpieczeństwa
                amount = float(decision.get('quantity', 0.001)) 
                price = float(decision.get('entry_price', 0))
                leverage = int(decision.get('leverage', 10))
                
                # --- A. Ustawienie Dźwigni ---
                try: 
                    self.exchange.set_leverage(leverage, symbol)
                except Exception as e: 
                    # Często rzuca błąd jeśli dźwignia już jest taka sama, ignorujemy to ostrzeżenie
                    pass 

                # --- B. Parametry TP / SL ---
                params = {}
                if decision.get('tp') and float(decision['tp']) > 0:
                    params['takeProfit'] = float(decision['tp'])
                if decision.get('sl') and float(decision['sl']) > 0:
                    params['stopLoss'] = float(decision['sl'])

                # --- C. Wykonanie Akcji ---

                # 1. CANCEL (Anulowanie zleceń)
                if "CANCEL" in action:
                    self.exchange.cancel_all_orders(symbol)
                    self.log("[AGENT 3] API: Anulowano wszystkie aktywne zlecenia.")

                # 2. CLOSE (Zamknięcie Pozycji)
                elif "CLOSE" in action:
                    # Krok 1: Anuluj zlecenia oczekujące (TP/SL)
                    self.exchange.cancel_all_orders(symbol)
                    
                    # Krok 2: Sprawdź co mamy i zamknij kontr-zleceniem
                    positions = self.exchange.fetch_positions([symbol])
                    for pos in positions:
                        qty = float(pos['contracts'])
                        side = pos['side'] # 'long' lub 'short'
                        if qty > 0:
                            # Logika odwrócenia: Mam Long -> Sprzedaj. Mam Short -> Kup.
                            close_side = 'sell' if side == 'long' else 'buy'
                            # Zamykamy MARKETEM dla pewności wyjścia
                            self.exchange.create_order(symbol, 'market', close_side, qty)
                            self.log(f"[AGENT 3] API: Zamknięto pozycję {side.upper()} ({qty} BTC).")

                # 3. OPEN (Otwarcie Pozycji)
                elif "OPEN" in action:
                    # Ustal kierunek
                    side = 'buy' if "LONG" in action else 'sell'
                    
                    # Ustal typ (LIMIT czy MARKET)
                    # Sprawdzamy czy w JSON jest "LIMIT" lub czy w nazwie akcji jest "LIMIT"
                    is_limit = ("LIMIT" in action) or (decision.get('entry') == "LIMIT")
                    
                    if is_limit and price > 0:
                        # Zlecenie LIMIT
                        order = self.exchange.create_order(symbol, 'limit', side, amount, price, params)
                        self.log(f"[AGENT 3] API: Otwarto LIMIT {side.upper()} @ ${price}")
                    else:
                        # Zlecenie MARKET
                        # Dla marketu cena to None
                        order = self.exchange.create_order(symbol, 'market', side, amount, None, params)
                        self.log(f"[AGENT 3] API: Otwarto MARKET {side.upper()}")
                
                # 4. UPDATE (Aktualizacja TP/SL - Opcjonalne)
                elif "UPDATE" in action:
                    # W API "Update" zazwyczaj oznacza anulowanie starych i dodanie nowych
                    # Tutaj dla bezpieczeństwa tylko logujemy, chyba że chcesz dodać zaawansowaną logikę
                    self.log("[AGENT 3] API: UPDATE TP/SL - Zalecane użycie CANCEL + nowe zlecenie.")

            except Exception as e: 
                # Tutaj wpadną błędy np. "Permission Denied" jeśli klucz jest Read-Only
                self.log(f"[AGENT 3] CRITICAL API FAIL: {e}")
                
# --- GUI ---
class AgentHub:
    def __init__(self, root):
        self.root = root
        self.root.title("Perceptron v33 - INTELLIGENCE CYCLE COMPLETE")
        self.root.geometry("740x950")
        self.root.configure(bg="#121212")
        self.root.overrideredirect(False) 
        
        self.cfg = configparser.ConfigParser()
        self.load_cfg()
        
        self.agent3 = Agent3_Executor(self.cfg, self.log_internal)
        self.data_col = DataCollector(self.cfg)
        
        self.loop_active = False
        self.next_run_time = 0
        self.build_ui()
        self._update_clocks()

    def log_internal(self, msg): self.root.after(0, lambda: self.log(msg))

    def build_ui(self):
        bg = "#121212"; fg = "#ccc"
        f_stat = tk.Frame(self.root, bg="black"); f_stat.pack(fill=tk.X, padx=5, pady=5)
        self.lbl_clock = tk.Label(f_stat, text="TIME", bg="black", fg="gray", font=("Consolas", 9)); self.lbl_clock.pack(side=tk.LEFT)
        self.lbl_next = tk.Label(f_stat, text="IDLE", bg="black", fg="orange", font=("Consolas", 12, "bold")); self.lbl_next.pack(side=tk.RIGHT)
        
        f_set = tk.LabelFrame(self.root, text="TIMING", bg=bg, fg=fg); f_set.pack(fill=tk.X, padx=10)
        tk.Label(f_set, text="Loop(min):", bg=bg, fg=fg).grid(row=0,column=0)
        self.val_loop = tk.IntVar(value=30); tk.Spinbox(f_set, textvariable=self.val_loop, from_=1, to=120, width=4).grid(row=0,column=1)
        tk.Label(f_set, text="AI Wait(s):", bg=bg, fg="cyan").grid(row=0,column=2)
        self.val_ai_wait = tk.IntVar(value=20); tk.Spinbox(f_set, textvariable=self.val_ai_wait, from_=5, to=120, width=4).grid(row=0,column=3)
        tk.Label(f_set, text="Gemini(s):", bg=bg, fg="yellow").grid(row=0,column=4)
        self.val_think = tk.IntVar(value=60); tk.Spinbox(f_set, textvariable=self.val_think, from_=10, to=300, width=4).grid(row=0,column=5)
        tk.Button(f_set, text="KEYS", command=self.keys_menu, bg="#333", fg="white").grid(row=0,column=6)

        f_sens = tk.LabelFrame(self.root, text="SENSORS", bg=bg, fg=fg); f_sens.pack(fill=tk.X, padx=10, pady=5)
        self.do_cg_api = tk.BooleanVar(value=True); tk.Checkbutton(f_sens, text="CG API", variable=self.do_cg_api, bg=bg, fg="white", selectcolor="#444").grid(row=0,column=0)
        self.do_ss_heat = tk.BooleanVar(value=True); tk.Checkbutton(f_sens, text="SS Heatmap", variable=self.do_ss_heat, bg=bg, fg="white", selectcolor="#444").grid(row=0,column=1)
        self.do_ss_bitmex = tk.BooleanVar(value=True); tk.Checkbutton(f_sens, text="SS Bitmex", variable=self.do_ss_bitmex, bg=bg, fg="white", selectcolor="#444").grid(row=0,column=2)

        self.vars_ai = {}
        for i, ai in enumerate(["GROK", "COPILOT", "DEEPSEEK", "QWEN"]):
            v = tk.BooleanVar(value=True)
            self.vars_ai[ai] = v
            tk.Checkbutton(f_sens, text=ai, variable=v, bg=bg, fg="cyan", selectcolor="#444").grid(row=1, column=i, sticky="w")

        f_exec = tk.LabelFrame(self.root, text="EXECUTION", bg=bg, fg="cyan"); f_exec.pack(fill=tk.X, padx=10)
        self.exec_mode = tk.StringVar(value="LEGACY")
        tk.Radiobutton(f_exec, text="LEGACY", variable=self.exec_mode, value="LEGACY", bg=bg, fg="white", selectcolor="#444").pack(side=tk.LEFT)
        tk.Radiobutton(f_exec, text="API", variable=self.exec_mode, value="API", bg=bg, fg="red", selectcolor="#444").pack(side=tk.LEFT)
        self.dry_run = tk.BooleanVar(value=True); tk.Checkbutton(f_exec, text="DRY RUN", variable=self.dry_run, bg=bg, fg="orange", selectcolor="#444").pack(side=tk.LEFT)

        self.log_box = scrolledtext.ScrolledText(self.root, height=15, bg="#000", fg="#0f0", font=("Consolas", 9)); self.log_box.pack(fill=tk.BOTH, expand=True, padx=10)
        
        tk.Button(self.root, text="▶ START LOOP", command=self.toggle_loop, bg="#040", fg="white").pack(fill=tk.X, padx=10)
        tk.Button(self.root, text="⚡ RUN ONCE", command=lambda: threading.Thread(target=self.cycle, daemon=True).start(), bg="#444", fg="white").pack(fill=tk.X, padx=10)
        tk.Button(self.root, text="🛠 KALIBRACJA", command=self.cal_menu, bg="#222", fg="gray").pack(fill=tk.X, padx=10)

    # --- LOGIKA v33 ---
    def cycle(self):
        self.log("=== START CYKLU Perceptron v33 ===")
        start_time = time.time()
        
        # 1. ZASIANIE PYTAŃ (Używa PROMPTS_FILE lub DEFAULT)
        self.ask_ai_consultants()
        
        # 2. SEKWENCJA ZBIERANIA I WKLEJANIA
        
        # A. SS Heatmap
        if self.do_ss_heat.get():
            self.log("1. SS Heatmap -> Gemini...")
            if self.snap_region('COINGLASS', 'cg_tab_main', 'cg_focus', 'cg_ss_1', 'cg_ss_2', TEMP_SS_HEATMAP):
                self.paste_to_gemini(TEMP_SS_HEATMAP, is_image=True)
            else: self.log("Błąd SS Coinglass")

        # B. SS Bitmex
        if self.do_ss_bitmex.get():
            self.log("2. SS Bitmex -> Gemini...")
            if self.snap_region('BITMEX', 'bm_tab', 'bm_focus', 'bm_ss_1', 'bm_ss_2', TEMP_SS_BITMEX):
                self.paste_to_gemini(TEMP_SS_BITMEX, is_image=True)
            else: self.log("Błąd SS Bitmex")

        # C. API Data
        if self.do_cg_api.get():
            self.log("3. API Data -> Gemini...")
            rep, _ = self.data_col.get_report()
            text_data = f"\n[COINGLASS API]\n{rep}\n"
            self.paste_to_gemini(text_data, is_image=False)

        # D. Czekanie na AI
        elapsed = time.time() - start_time
        target_wait = self.val_ai_wait.get()
        wait_remain = target_wait - elapsed
        if wait_remain > 0:
            self.log(f"Czekam {int(wait_remain)}s na resztę AI...")
            time.sleep(wait_remain)

        # E. Odbiór Raportów AI
        self.retrieve_and_paste_ai_reports()

        # F. Prompt Strategiczny + Binance Data
        self.log("4. Pobieram stan konta i wysyłam Prompt...")
        
        # Pobierz dane z Binance (nawet jeśli klucz tylko do odczytu)
        binance_status = self.agent3.get_account_report()
        
        # Sklej Prompt: FILOZOFIA + DANE
        full_prompt = binance_status + "\n" + TRADING_PHILOSOPHY
        
        # Wyślij do Gemini
        self.paste_to_gemini(full_prompt, is_image=False, send=True)

        # 3. ODBIÓR I ANALIZA
        wait_gem = self.val_think.get()
        self.log(f"Czekam {wait_gem}s na analizę...")
        time.sleep(wait_gem)
        
        response_text = self.get_gemini_response()
        self.log(f"Odebrano {len(response_text)} znaków.")

        # 4. PARSOWANIE DECYZJI (AGENT 3)
        # match_trade = re.search(r'\[AGENT3_START\](.*?)\[AGENT3_END\]', response_text, re.DOTALL)
        # if match_trade:
            # try:
                # decision = parse_json(match_trade.group(1))
                # self.log(f"DECYZJA HANDLOWA: {decision.get('action')}")
                # self.agent3.execute(decision, mode=self.exec_mode.get(), dry_run=self.dry_run.get())
            # except Exception as e: self.log(f"Błąd Trade JSON: {e}")

        # 5. PARSOWANIE STRATEGII (AKTUALIZACJA PYTAŃ)
        match_strat = re.search(r'\[NEXT_CYCLE_STRATEGY\](.*?)\[END_STRATEGY\]', response_text, re.DOTALL)
        if match_strat:
            try:
                raw_json = match_strat.group(1)
                new_prompts = parse_json(raw_json)
                
                # Zapisujemy do pliku
                with open(PROMPTS_FILE, 'w') as f: 
                    json.dump(new_prompts, f, indent=4)
                
                self.log(f"✅ Zaktualizowano pytania na następny cykl!")
                
            except Exception as e: 
                self.log(f"Błąd aktualizacji strategii: {e}")
        else:
            self.log("Brak nowych pytań w odpowiedzi. Zostawiam stare.")
        
        self.log("=== KONIEC CYKLU ===")

    # --- POMOCNIKI LOGIKI ---
    def get_gemini_response(self):
        if 'GEMINI' not in self.cfg: return ""
        c = self.cfg['GEMINI']
        try:
            self.clk(c, 'gem_tab'); time.sleep(0.5)
            if 'gem_scroll_x' in c:
                self.clk(c, 'gem_scroll')
                for _ in range(10): pyautogui.scroll(-800); time.sleep(0.05)
            else: pyautogui.press('pagedown')
            time.sleep(1.0)
            self.clk(c, 'gem_copy'); time.sleep(0.5)
            return pyperclip.paste()
        except Exception as e:
            self.log(f"Błąd odbioru: {e}")
            return ""

    def paste_to_gemini(self, content, is_image=False, send=False):
        if 'GEMINI' not in self.cfg: return
        c = self.cfg['GEMINI']
        self.clk(c, 'gem_tab'); self.clk(c, 'gem_input'); time.sleep(0.2)
        
        if is_image:
            cmd = f"powershell -command \"Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.Clipboard]::SetImage([System.Drawing.Image]::FromFile('{content}'))\""
            subprocess.call(cmd, shell=True)
            time.sleep(0.5)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(2.0)
        else:
            pyperclip.copy(content)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.5)
            
        if send:
            self.clk(c, 'gem_send')
            if 'gem_scroll_x' in c:
                self.clk(c, 'gem_scroll')
                pyautogui.scroll(-500)

    def ask_ai_consultants(self):
        # 1. Ładowanie pytań (z pliku lub domyślne)
        current_prompts = DEFAULT_PROMPTS.copy()
        if os.path.exists(PROMPTS_FILE):
            try: 
                with open(PROMPTS_FILE, 'r') as f: 
                    file_prompts = json.load(f)
                    current_prompts.update(file_prompts) # Nadpisz domyślne tymi z pliku
            except: pass
        
        active = [ai for ai, v in self.vars_ai.items() if v.get()]
        if not active: return
        
        self.log(f"Zadaję pytania ({len(active)} AI)...")
        
        for ai in active:
            if f"AI_{ai}" not in self.cfg: continue
            c = self.cfg[f"AI_{ai}"]
            
            # Pobierz pytanie dedykowane dla tego bota
            prompt = current_prompts.get(ai, "Analyze BTC structure.")
            
            try:
                self.clk(c, 'ai_tab'); self.clk(c, 'ai_input')
                pyperclip.copy(prompt); pyautogui.hotkey('ctrl','v'); time.sleep(0.3)
                if 'ai_send_x' in c: self.clk(c, 'ai_send')
                else: pyautogui.press('enter')
            except: pass

    def retrieve_and_paste_ai_reports(self):
        active = [ai for ai, v in self.vars_ai.items() if v.get()]
        if not active: return
        
        for ai in active:
            if f"AI_{ai}" not in self.cfg: continue
            c = self.cfg[f"AI_{ai}"]
            self.log(f"Pobieram: {ai}...")
            try:
                self.clk(c, 'ai_tab'); time.sleep(0.5)
                if 'ai_scroll_x' in c:
                    self.clk(c, 'ai_scroll')
                    for _ in range(8): pyautogui.scroll(-600); time.sleep(0.02)
                time.sleep(0.5)
                if 'ai_copy_x' in c:
                    self.clk(c, 'ai_copy'); time.sleep(0.5)
                    raw_text = pyperclip.paste()
                    formatted_text = f"\n=== {ai} REPORT ===\n{raw_text[:1000]}...\n"
                    self.paste_to_gemini(formatted_text, is_image=False)
            except: pass

    def snap_region(self, s, t, f, c1, c2, p):
        if s not in self.cfg: return False
        c = self.cfg[s]
        try:
            self.clk(c,t); time.sleep(1); self.clk(c,f) 
            x1=int(c[f"{c1}_x"]); y1=int(c[f"{c1}_y"])
            x2=int(c[f"{c2}_x"]); y2=int(c[f"{c2}_y"])
            pyautogui.screenshot(region=(min(x1,x2), min(y1,y2), abs(x2-x1), abs(y2-y1))).save(p)
            return True
        except: return False

    def clk(self, c, k):
        if f"{k}_x" in c: pyautogui.click(int(c[f"{k}_x"]), int(c[f"{k}_y"])); time.sleep(0.3)
    
    def toggle_loop(self):
        self.loop_active = not self.loop_active
        if self.loop_active: threading.Thread(target=self.worker, daemon=True).start()

    def worker(self):
        while self.loop_active:
            self.next_run_time = time.time() + (self.val_loop.get() * 60)
            self.cycle()
            while time.time() < self.next_run_time:
                if not self.loop_active: break
                time.sleep(1)

    def log(self, t): 
        msg = f"[{datetime.now().strftime('%H:%M:%S')}] {t}"
        self.log_box.insert(tk.END, msg + "\n"); self.log_box.see(tk.END); print(msg)
    
    def load_cfg(self):
        if not os.path.exists(CONFIG_FILE): open(CONFIG_FILE,'w').close()
        self.cfg.read(CONFIG_FILE)

    def keys_menu(self):
        t=tk.Toplevel(self.root); t.configure(bg="#222")
        els={}
        for k in ["gemini_key", "coinglass_key", "binance_key", "binance_secret"]:
            tk.Label(t,text=k,fg="white",bg="#222").pack()
            e=tk.Entry(t,show="*"); e.pack(); e.insert(0, self.cfg.get('SECRETS',k,fallback="")); els[k]=e
        def save():
            if 'SECRETS' not in self.cfg: self.cfg['SECRETS']={}
            for k,v in els.items(): self.cfg['SECRETS'][k]=v.get().strip()
            with open(CONFIG_FILE,'w') as f: self.cfg.write(f)
            t.destroy(); self.agent3._init_api()
        tk.Button(t,text="SAVE",command=save).pack()

    def cal_menu(self):
        t=tk.Toplevel(self.root); t.configure(bg="#222")
        def sv(): 
            with open(CONFIG_FILE,'w') as f: self.cfg.write(f)
        for k in ["GEMINI","COINGLASS","BITMEX"]:
            tk.Button(t,text=k,command=lambda x=k:CalWizard(self.root,x,self.cfg,sv)).pack()
        for k in ["GROK","COPILOT","DEEPSEEK","QWEN"]:
            tk.Button(t,text=k,command=lambda x=f"AI_{k}":CalWizard(self.root,x,self.cfg,sv)).pack()
            
    def _update_clocks(self):
        rem = int(self.next_run_time - time.time()) if self.loop_active else 0
        self.lbl_clock.config(text=datetime.now().strftime('%H:%M:%S'))
        self.lbl_next.config(text=f"NEXT: {rem}s" if self.loop_active else "STOPPED")
        self.root.after(1000, self._update_clocks)

# --- DATA: Data Coinglass BTC Price + "THE HOLY TRINITY" + Liquidation ---
class DataCollector:
    def __init__(self, cfg):
        self.cfg = cfg
        self.base_url = "https://open-api.coinglass.com/public/v2" 

    def get_report(self):
        key = self.cfg.get('SECRETS', 'coinglass_key', fallback="")
        if not key or "WPISZ" in key: return "No API Key", "N/A"
        
        headers = {"coinglassSecret": key}
        try:
            # 1. PRICE (Baza)
            p_res = requests.get(f"{self.base_url}/index/bitcoin_price_index?symbol=BTC", headers=headers, timeout=5).json()
            price = p_res['data'][0]['price']
            
            # 2. OPEN INTEREST (The Fuel)
            oi_res = requests.get(f"{self.base_url}/indicator/open_interest?symbol=BTC", headers=headers, timeout=5).json()
            oi_val = oi_res['data'][0]['openInterest']

            # 3. FUNDING RATE (Sentiment)
            fr_res = requests.get(f"{self.base_url}/indicator/funding_rate?symbol=BTC", headers=headers, timeout=5).json()
            funding = fr_res['data'][0]['rate']

            # 4. L/S RATIO (Retail Positioning)
            ls_res = requests.get(f"{self.base_url}/indicator/long_short_accounts?symbol=BTC&time_type=h1", headers=headers, timeout=5).json()
            ls_ratio = ls_res['data'][0]['longShortRatio']

            # 5. LIQUIDATIONS (The Pain)
            liq_res = requests.get(f"{self.base_url}/indicator/liquidation?symbol=BTC&time_type=h1", headers=headers, timeout=5).json()
            # Uproszczone pobieranie wolumenu likwidacji (Total Vol USD)
            liq_vol = liq_res['data'][0]['volUsd']

            # Formatowanie raportu dla AI
            report = (
                f"--- API DATA Coinglass---\n"
                f"CURRENT PRICE: ${price}\n"
                f"AVG FUNDING: {funding}% (Sentiment)\n"
                f"L/S RATIO: {ls_ratio} (Retail Crowd)\n"
                f"OPEN INTEREST: ${oi_val:,.0f} (Fuel)\n"
                f"LIQUIDATIONS (1H): ${liq_vol:,.0f} (Pain)\n"
                f"------------------------\n"
            )
            return report, str(price)

        except Exception as e:
            return f"[API ERROR] {e}", "ERR"
        
class CalWizard:
    def __init__(self, m, s, c, cb):
        self.top=tk.Toplevel(m); self.top.attributes('-topmost',True); self.top.configure(bg="#222")
        self.s=s; self.c=c; self.cb=cb; self.step=0
        self.els = {
            "GEMINI": [("gem_tab","Tab"),("gem_input","In"),("gem_send","Send"),("gem_scroll","Scroll"),("gem_copy","Copy")],
            "COINGLASS": [("cg_tab_main","Tab"),("cg_focus","Focus"),("cg_ss_1","TL"),("cg_ss_2","BR")],
            "BITMEX": [("bm_tab","Tab"),("bm_focus","Focus"),("bm_ss_1","TL"),("bm_ss_2","BR")],
            "AI_GROK": [("ai_tab","Tab"),("ai_input","In"),("ai_send","Send"),("ai_scroll","Scroll"),("ai_copy","Copy")],
            "AI_COPILOT": [("ai_tab","Tab"),("ai_input","In"),("ai_send","Send"),("ai_scroll","Scroll"),("ai_copy","Copy")],
            "AI_DEEPSEEK": [("ai_tab","Tab"),("ai_input","In"),("ai_send","Send"),("ai_scroll","Scroll"),("ai_copy","Copy")],
            "AI_QWEN": [("ai_tab","Tab"),("ai_input","In"),("ai_send","Send"),("ai_scroll","Scroll"),("ai_copy","Copy")]
        }.get(s, [])
        self.l=tk.Label(self.top,text="F2 to Set",fg="white",bg="#222",font=("Arial",14)); self.l.pack()
        self.lis=keyboard.Listener(on_release=self.k); self.lis.start(); self.upd()
    def upd(self):
        if self.step<len(self.els): self.l.config(text=f"{self.els[self.step][1]} (F2)")
        else: self.fin()
    def k(self,k):
        if k==keyboard.Key.f2:
            x,y=pyautogui.position(); n=self.els[self.step][0]
            if self.s not in self.c: self.c[self.s]={}
            self.c[self.s][f"{n}_x"]=str(x); self.c[self.s][f"{n}_y"]=str(y)
            self.step+=1; self.top.after(0,self.upd)
    def fin(self): self.lis.stop(); self.cb(); self.top.destroy()

if __name__ == "__main__":
    print("Wait 5s..."); time.sleep(5)
    root = tk.Tk(); app = AgentHub(root); root.mainloop()