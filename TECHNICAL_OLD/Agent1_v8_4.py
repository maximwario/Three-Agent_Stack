# -*- coding: utf-8 -*-
"""
PROJEKT: AGENT 1 - NEURAL COMMANDER (v8.4 - JSON HARDENED)
AUTOR: Agent 2 & Operator & Agent 3
DATA: 30.11.2025

ZMIANY v8.4:
- Dodano clean_json_payload: Odporność na formatowanie Markdown (```json) i przecinki.
- Zabezpieczenie pętli: Błąd parsowania strategii nie zatrzymuje bota (loguje błąd i używa starych pytań).
- Obsługa polskich znaków przy odczycie/zapisie JSON.
- Dodano prompt bo Gemini wstawiała [ ] w komendach do Agenta 3 i w nowych pytaniach do innych AI.
- Dodano prompt by wpisywała najpierw TP a potem SL

"""

import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
import pyautogui
import pyperclip
import time
import configparser
import os
import threading
import json
import re
from datetime import datetime, timedelta, timezone
from pynput import keyboard

# --- KONFIGURACJA ---
CONFIG_FILE = "intel_config_v8_4.ini"
PROMPTS_FILE = "dynamic_prompts.json"
pyautogui.FAILSAFE = False 
pyautogui.PAUSE = 0.5

# --- DOMYŚLNE PROMPTY ---
DEFAULT_PROMPTS = {
    "GROK": "Act as an Institutional Sentiment Algo. SCAN TARGET: X (Twitter). 1. RETAIL PULSE? 2. SMART MONEY FLOW? 3. VERDICT?",
    "COPILOT": "Act as Senior On-Chain Analyst. Analyze Coinglass/Binance data. 1. Liquidation Heatmap? 2. Open Interest? 3. Funding Rate? Provide levels.",
    "DEEPSEEK": "Role: HFT Risk Manager. Calculate EV for current price. Scenario A (Bull) vs Scenario B (Bear). Verdict: IS EV POSITIVE?",
    "QWEN": "Role: Market Structure Quant. Analyze last 4H candles. Structure? Trap Detection? Momentum? Decision: BREAKOUT or DEFENSIVE?"
}

# --- ULTIMATE PROMPT DLA GEMINI ---
FINAL_GEMINI_PROMPT = """Jesteś Agentem 2 (Strategiem). Przeanalizuj dostarczony RAPORT.
Masz pełną autonomię na koncie Binance Demo.

TWOJE ZADANIA (Używaj ściśle tych formatów tagów):

1. DECYZJA HANDLOWA (Dla Agenta 3):
Jeśli chcesz wykonać ruch, wypisz JSON w tagach:
[AGENT3_START]
{
  "action": "OPEN_LONG" lub "UPDATE_TPSL" lub "CLOSE_ALL",
  "entry_price": "MARKET" lub cena,
  "stop_loss": 0,
  "take_profit": 0
}
[AGENT3_END]
(Jeśli HOLD, nie wpisuj tego bloku).

2. ZARZĄDZANIE WYWIADEM (Dla Agenta 1):
Jeśli chcesz zmienić pytania do AI na następną turę, wypisz je w tagach:
[NEXT_CYCLE_STRATEGY]
{
  "GROK": "Nowe pytanie...",
  "COPILOT": "Nowe pytanie...",
  "DEEPSEEK": "Nowe pytanie...",
  "QWEN": "Nowe pytanie..."
}
[END_STRATEGY]
(Jeśli pytania są OK, pomiń ten blok).

Wygeneruj analizę i odpowiednie bloki. Nie używaj [tekst] w tych nawiasach z wyjątkiem 
[AGENT3_START] 
[AGENT3_END] 
[NEXT_CYCLE_STRATEGY] 
[END_STRATEGY]. To jest używane w twoich odpowiedziach do zadań dla Agenta 1 i pytania wyspecjalizowane do innych AI. 
Pamiętaj rówwnież o wpisywaniu najpierw TP a potem SL gdy piszesz komendy dla Agenta 3."""

# --- MAPA ELEMENTÓW ---
CALIBRATION_MAP = {
    "GEMINI_CONTROLS": [
        ("gem_tab", "1. Zakładka GEMINI"),
        ("gem_input", "2. Pole pisania"),
        ("gem_send", "3. Przycisk WYŚLIJ"),
        ("gem_scroll_point", "4. ŚRODEK EKRANU (Scroll)"),
        ("gem_copy", "5. Przycisk KOPIUJ")
    ],
    "BINANCE": [
        ("bin_tab", "1. Zakładka BINANCE"), ("bin_focus", "2. Pusty punkt"),
        ("bin_ord_tab", "4. Zakładka 'ZLECENIA'"), ("bin_pos_tab", "3. Zakładka 'POZYCJE'"),
        ("bin_ss_1", "5. SS Lewy-Góra"), ("bin_ss_2", "6. SS Prawy-Dół")
    ],
    "TRADINGVIEW": [
        ("tw_tab", "1. Zakładka TW"), ("tw_focus", "2. Środek"),
        ("tw_ss_1", "3. SS Lewy-Góra"), ("tw_ss_2", "4. SS Prawy-Dół")
    ],
    "BITMEX": [
        ("bm_tab", "1. Zakładka BITMEX"), ("bm_focus", "2. Środek"),
        ("bm_ss_1", "3. SS Lewy-Góra"), ("bm_ss_2", "4. SS Prawy-Dół")
    ],
    "COINGLASS": [
        ("cg_tab_main", "1. Zakładka CG MAIN"), ("cg_tab_fund", "2. Zakładka CG FUND"),
        ("cg_focus", "3. Środek")
    ],
    "AI_GROK": [("ai_tab", "Zakładka"), ("ai_input", "Pole"), ("ai_send", "Wyślij"), ("ai_scroll_point", "Środek"), ("ai_copy", "Kopiuj")],
    "AI_COPILOT": [("ai_tab", "Zakładka"), ("ai_input", "Pole"), ("ai_send", "Wyślij"), ("ai_scroll_point", "Środek"), ("ai_copy", "Kopiuj")],
    "AI_DEEPSEEK": [("ai_tab", "Zakładka"), ("ai_input", "Pole"), ("ai_send", "Wyślij"), ("ai_scroll_point", "Środek"), ("ai_copy", "Kopiuj")],
    "AI_QWEN": [("ai_tab", "Zakładka"), ("ai_input", "Pole"), ("ai_send", "Wyślij"), ("ai_scroll_point", "Środek"), ("ai_copy", "Kopiuj")]
}

def clean_json_payload(text):
    """Czyści tekst z Markdown i błędów JSON przed parsowaniem"""
    # Usuń znaczniki kodu Markdown ```json ... ```
    text = re.sub(r'```json', '', text, flags=re.IGNORECASE)
    text = re.sub(r'```', '', text)
    # Usuń przecinki przed zamknięciem nawiasu (trailing commas)
    text = re.sub(r',(\s*[\}\]])', r'\1', text)
    return text.strip()

class CalibrationWizard:
    def __init__(self, master, section, config, on_complete):
        self.top = tk.Toplevel(master)
        self.top.geometry("500x250")
        self.top.configure(bg="#222")
        self.section = section
        self.config = config
        self.on_complete = on_complete
        self.elements = CALIBRATION_MAP[section]
        self.step = 0
        self.lbl = tk.Label(self.top, text="START", fg="white", bg="#222", font=("Arial", 12))
        self.lbl.pack(pady=20)
        self.listener = keyboard.Listener(on_release=self.on_key)
        self.listener.start()
        self.update_ui()
    
    def update_ui(self):
        if self.step < len(self.elements):
            self.lbl.config(text=f"KROK {self.step+1}: {self.elements[self.step][1]}")
        else:
            self.finish()
            
    def on_key(self, key):
        if key == keyboard.Key.f2:
            x, y = pyautogui.position()
            k = self.elements[self.step][0]
            if self.section not in self.config: self.config[self.section] = {}
            self.config[self.section][f"{k}_x"] = str(x)
            self.config[self.section][f"{k}_y"] = str(y)
            print('\a')
            self.step += 1
            self.top.after(0, self.update_ui)
            
    def finish(self):
        self.listener.stop()
        self.on_complete()
        self.top.destroy()
        messagebox.showinfo("OK", "Zapisano!")

class IntelAgentHUB:
    def __init__(self, root):
        self.root = root
        self.root.title("Agent 1 - Neural Commander v8.4")
        self.root.geometry("700x1000")
        self.root.configure(bg="#1e1e1e")
        self.config = configparser.ConfigParser()
        self.load_config()
        self.loop_active = False
        self.on_top = tk.BooleanVar(value=False)
        self.next_run_time = None
        self.current_prompts = self.load_prompts()
        self._create_ui()
        self._update_clocks()

    def _create_ui(self):
        # ZEGAR
        cf = tk.Frame(self.root, bg="black")
        cf.pack(fill=tk.X, padx=5, pady=5)
        self.lbl_world = tk.Label(cf, text="...", font=("Consolas", 9), bg="black", fg="cyan")
        self.lbl_world.pack()
        self.lbl_timer = tk.Label(cf, text="IDLE", font=("Consolas", 20, "bold"), bg="black", fg="orange")
        self.lbl_timer.pack()

        # OPCJE
        opt = tk.Frame(self.root, bg="#1e1e1e")
        opt.pack(fill=tk.X, padx=10)
        tk.Checkbutton(opt, text="Zawsze na wierzchu", var=self.on_top, command=self.toggle_top, bg="#1e1e1e", fg="white", selectcolor="#333").pack(side=tk.RIGHT)

        # CZASY (SUWAKI)
        tf = tk.LabelFrame(self.root, text="CZASY", bg="#252526", fg="white")
        tf.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(tf, text="Pętla (min):", fg="white", bg="#252526").grid(row=0, column=0)
        self.interval_min = tk.IntVar(value=30)
        tk.Spinbox(tf, from_=1, to=240, textvariable=self.interval_min, width=5).grid(row=0, column=1)
        
        tk.Label(tf, text="AI Wait (s):", fg="white", bg="#252526").grid(row=0, column=2)
        self.wait_ai = tk.IntVar(value=10) 
        tk.Spinbox(tf, from_=1, to=300, textvariable=self.wait_ai, width=5).grid(row=0, column=3)
        
        tk.Label(tf, text="Gemini Wait (s):", fg="yellow", bg="#252526").grid(row=0, column=4)
        self.wait_gemini = tk.IntVar(value=180)
        tk.Spinbox(tf, from_=5, to=600, textvariable=self.wait_gemini, width=5).grid(row=0, column=5)

        # Kalibracja
        cf = tk.LabelFrame(self.root, text="1. KALIBRACJA", bg="#222", fg="gray")
        cf.pack(fill=tk.X, padx=10)
        tk.Button(cf, text="GEMINI", command=lambda: self.cal("GEMINI_CONTROLS")).pack(side=tk.LEFT, padx=2)
        tk.Button(cf, text="BINANCE", command=lambda: self.cal("BINANCE")).pack(side=tk.LEFT, padx=2)
        tk.Button(cf, text="COINGLASS", command=lambda: self.cal("COINGLASS")).pack(side=tk.LEFT, padx=2)
        cf2 = tk.Frame(self.root, bg="#1e1e1e")
        cf2.pack(fill=tk.X, padx=10, pady=2)
        tk.Button(cf2, text="TW", command=lambda: self.cal("TRADINGVIEW")).pack(side=tk.LEFT, padx=2)
        tk.Button(cf2, text="BITMEX", command=lambda: self.cal("BITMEX")).pack(side=tk.LEFT, padx=2)
        cf3 = tk.Frame(self.root, bg="#1e1e1e")
        cf3.pack(fill=tk.X, padx=10, pady=2)
        for ai in ["GROK", "COPILOT", "DEEPSEEK", "QWEN"]:
            tk.Button(cf3, text=ai, command=lambda a="AI_"+ai: self.cal(a)).pack(side=tk.LEFT, padx=2)

        # Zadania
        sf = tk.LabelFrame(self.root, text="2. ZADANIA", bg="#252526", fg="orange")
        sf.pack(fill=tk.X, padx=10, pady=5)
        self.do_binance_txt = tk.BooleanVar(value=True)
        self.do_binance_ss = tk.BooleanVar(value=True)
        self.do_tw_txt = tk.BooleanVar(value=True)
        self.do_tw_ss = tk.BooleanVar(value=True)
        self.do_bitmex_ss = tk.BooleanVar(value=True)
        self.do_coinglass_txt = tk.BooleanVar(value=True)
        self.do_grok = tk.BooleanVar(value=True)
        self.do_copilot = tk.BooleanVar(value=True)
        self.do_deepseek = tk.BooleanVar(value=True)
        self.do_qwen = tk.BooleanVar(value=True)

        c1 = tk.Frame(sf, bg="#252526")
        c1.pack(side=tk.LEFT, anchor="n", padx=5)
        tk.Checkbutton(c1, text="[TXT] BINANCE", var=self.do_binance_txt, bg="#252526", fg="white", selectcolor="#444").pack(anchor="w")
        tk.Checkbutton(c1, text="[SS] BINANCE", var=self.do_binance_ss, bg="#252526", fg="white", selectcolor="#444").pack(anchor="w")
        tk.Checkbutton(c1, text="[TXT] TW", var=self.do_tw_txt, bg="#252526", fg="white", selectcolor="#444").pack(anchor="w")
        tk.Checkbutton(c1, text="[SS] TW", var=self.do_tw_ss, bg="#252526", fg="white", selectcolor="#444").pack(anchor="w")

        c2 = tk.Frame(sf, bg="#252526")
        c2.pack(side=tk.LEFT, anchor="n", padx=20)
        tk.Checkbutton(c2, text="[SS] BITMEX", var=self.do_bitmex_ss, bg="#252526", fg="white", selectcolor="#444").pack(anchor="w")
        tk.Checkbutton(c2, text="[TXT] COINGLASS", var=self.do_coinglass_txt, bg="#252526", fg="white", selectcolor="#444").pack(anchor="w")
        tk.Checkbutton(c2, text="[AI] GROK", var=self.do_grok, bg="#252526", fg="cyan", selectcolor="#444").pack(anchor="w")
        tk.Checkbutton(c2, text="[AI] COPILOT", var=self.do_copilot, bg="#252526", fg="cyan", selectcolor="#444").pack(anchor="w")
        
        c3 = tk.Frame(sf, bg="#252526")
        c3.pack(side=tk.LEFT, anchor="n", padx=5)
        tk.Checkbutton(c3, text="[AI] DEEPSEEK", var=self.do_deepseek, bg="#252526", fg="cyan", selectcolor="#444").pack(anchor="w")
        tk.Checkbutton(c3, text="[AI] QWEN", var=self.do_qwen, bg="#252526", fg="cyan", selectcolor="#444").pack(anchor="w")
        
        tk.Button(sf, text="[AI] WSZYSTKIE", command=self.toggle_all_ai, bg="#333", fg="white", font=("Arial", 8)).pack(anchor="e")

        self.btn_loop = tk.Button(self.root, text="START PĘTLI", bg="#005500", fg="white", font=("Arial", 12, "bold"), command=self.toggle_loop)
        self.btn_loop.pack(fill=tk.X, padx=20, pady=10)
        tk.Button(self.root, text="⚡ URUCHOM RAZ", bg="#444", fg="white", command=lambda: threading.Thread(target=self.run_tasks, daemon=True).start()).pack(fill=tk.X, padx=20, pady=5)
        self.log_box = scrolledtext.ScrolledText(self.root, bg="#111", fg="lime", height=12)
        self.log_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    def toggle_all_ai(self):
        val = not self.do_grok.get()
        self.do_grok.set(val)
        self.do_copilot.set(val)
        self.do_deepseek.set(val)
        self.do_qwen.set(val)

    # --- CORE LOGIC ---
    def run_tasks(self, is_loop=False):
        self.log(f"=== START CYKLU (Pytania: {len(self.current_prompts)}) ===")
        try:
            gem = self.config['GEMINI_CONTROLS']
            
            # 1. ZASIANIE AI (Dynamiczne pytania)
            active_ais = []
            for ai in ["AI_GROK", "AI_COPILOT", "AI_DEEPSEEK", "AI_QWEN"]:
                short_name = ai.replace("AI_", "")
                ai_var = getattr(self, f"do_{short_name.lower()}", None)
                if ai_var and ai_var.get():
                    active_ais.append(ai)
                    self.log(f">>> ZADAJE: {short_name}...")
                    self._send_ai_prompt(ai, short_name)
            
            # 2. GIEŁDY
            if self.do_binance_txt.get():
                self.log(">>> BINANCE TXT...")
                c = self.config['BINANCE']
                self._click(c, 'bin_tab'); time.sleep(1); self._click(c, 'bin_pos_tab'); self._copy_txt(); self._paste(gem, "BINANCE POZ", pyperclip.paste())
                self._click(c, 'bin_tab'); self._click(c, 'bin_ord_tab'); self._copy_txt(); self._paste(gem, "BINANCE ZLEC", pyperclip.paste())
            
            if self.do_binance_ss.get():
                self.log(">>> BINANCE SS...")
                c = self.config['BINANCE']
                self._click(c, 'bin_tab'); self._click(c, 'bin_pos_tab'); self._ss(c, gem, 'bin_ss_1', 'bin_ss_2')
                self._click(c, 'bin_tab'); self._click(c, 'bin_ord_tab'); self._ss(c, gem, 'bin_ss_1', 'bin_ss_2')

            if self.do_bitmex_ss.get():
                self.log(">>> BITMEX...")
                c = self.config['BITMEX']
                self._click(c, 'bm_tab'); self._click(c, 'bm_focus'); self._ss(c, gem, 'bm_ss_1', 'bm_ss_2')

            if self.do_coinglass_txt.get():
                self.log(">>> COINGLASS...")
                c = self.config['COINGLASS']
                self._click(c, 'cg_tab_main'); pyautogui.hotkey('Fn', 'f5'); time.sleep(6); self._click(c, 'cg_focus')
                self._copy_txt(); self._paste(gem, "COINGLASS MAIN", pyperclip.paste())
                self._click(c, 'cg_tab_fund'); pyautogui.hotkey('Fn', 'f5'); time.sleep(6); self._click(c, 'cg_focus')
                self._copy_txt(); self._paste(gem, "COINGLASS FUNDING", pyperclip.paste())

            if self.do_tw_txt.get():
                self.log(">>> TW TXT...")
                c = self.config['TRADINGVIEW']
                self._click(c, 'tw_tab'); time.sleep(1); self._click(c, 'tw_focus'); self._copy_txt(); self._paste(gem, "TW DATA", pyperclip.paste())

            if self.do_tw_ss.get():
                self.log(">>> TW SS...")
                c = self.config['TRADINGVIEW']
                self._click(c, 'tw_tab'); time.sleep(1); self._click(c, 'tw_focus'); self._ss(c, gem, 'tw_ss_1', 'tw_ss_2')

            # 3. ODBIÓR AI
            if active_ais:
                self.log(f"⏳ Czekam na AI ({self.wait_ai.get()}s)...")
                time.sleep(self.wait_ai.get())
                for ai in active_ais:
                    self.log(f">>> ODBIERAM: {ai}...")
                    self._retrieve_ai_response(ai, gem)

            # 4. GEMINI & PARSING
            self.log(">>> GEMINI...")
            self._click(gem, 'gem_tab'); time.sleep(1); self._click(gem, 'gem_input')
            pyperclip.copy(FINAL_GEMINI_PROMPT); pyautogui.hotkey('ctrl', 'v'); time.sleep(0.5)
            self._click(gem, 'gem_send')
            
            wait_g = self.wait_gemini.get()
            self.log(f"⏳ Czekam {wait_g}s na analizę...")
            time.sleep(wait_g)
            
            self.log("📜 Scroll & Copy...")
            self._click(gem, 'gem_scroll_point')
            # AGRESYWNY SCROLL
            for _ in range(10): 
                pyautogui.scroll(-500)
                time.sleep(0.02)
            
            time.sleep(1); self._click(gem, 'gem_copy')
            
            # 5. AKTUALIZACJA PYTAŃ
            time.sleep(1) # Chwila na załadowanie schowka
            response_text = pyperclip.paste()
            self._parse_and_save_new_prompts(response_text)
            
            self.log("✅ CYKL ZAKOŃCZONY. Wynik w schowku dla Agenta 3.")
        except Exception as e: self.log(f"BŁĄD KRYTYCZNY: {e}")

    def _parse_and_save_new_prompts(self, text):
        """Szuka bloku [NEXT_CYCLE_STRATEGY] i bezpiecznie parsuje JSON"""
        try:
            match = re.search(r'\[NEXT_CYCLE_STRATEGY\](.*?)\[END_STRATEGY\]', text, re.DOTALL)
            if match:
                raw_json = match.group(1).strip()
                cleaned_json = clean_json_payload(raw_json)
                
                new_prompts = json.loads(cleaned_json)
                
                count = 0
                for k, v in new_prompts.items():
                    key_upper = k.upper()
                    if key_upper in ["GROK", "COPILOT", "DEEPSEEK", "QWEN"]:
                        self.current_prompts[key_upper] = v
                        count += 1
                
                self.save_prompts()
                self.log(f"🧠 ZAKTUALIZOWANO {count} PYTAŃ NA NOWY CYKL!")
            else:
                self.log("ℹ️ Brak nowych pytań w odpowiedzi. Używam starych.")
        except json.JSONDecodeError as je:
            self.log(f"⚠️ Błąd składni JSON w strategii: {je}")
            self.log("Zachowuję stare pytania.")
        except Exception as e: 
            self.log(f"⚠️ Błąd parsowania nowych pytań: {e}")

    def _send_ai_prompt(self, sec, short_name):
        c = self.config[sec]
        self._click(c, 'ai_tab'); self._click(c, 'ai_input')
        prompt = self.current_prompts.get(short_name, DEFAULT_PROMPTS.get(short_name, "Analizuj."))
        pyperclip.copy(prompt)
        pyautogui.hotkey('ctrl', 'v'); time.sleep(0.5)
        if 'ai_send_x' in c: self._click(c, 'ai_send')
        else: pyautogui.press('enter')

    def load_prompts(self):
        if os.path.exists(PROMPTS_FILE):
            try:
                with open(PROMPTS_FILE, 'r', encoding='utf-8') as f: return json.load(f)
            except: pass
        return DEFAULT_PROMPTS.copy()

    def save_prompts(self):
        with open(PROMPTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.current_prompts, f, indent=4, ensure_ascii=False)

    def _update_clocks(self):
        utc = datetime.now(timezone.utc)
        txt = f"NY:{(utc-timedelta(hours=5)).strftime('%H:%M')} | LON:{utc.strftime('%H:%M')} | PAR:{(utc+timedelta(hours=1)).strftime('%H:%M')}"
        self.lbl_world.config(text=txt)
        if self.loop_active and self.next_run_time:
            rem = self.next_run_time - time.time()
            if rem > 0: m, s = divmod(int(rem), 60); self.lbl_timer.config(text=f"NEXT: {m:02}:{s:02}", fg="orange")
            else: self.lbl_timer.config(text="RUN...", fg="red")
        else: self.lbl_timer.config(text="IDLE", fg="gray")
        self.root.after(1000, self._update_clocks)

    def log(self, msg): t = datetime.now().strftime("%H:%M:%S"); self.log_box.insert(tk.END, f"[{t}] {msg}\n"); self.log_box.see(tk.END)
    def save_config(self):
        with open(CONFIG_FILE, 'w') as f: self.config.write(f)
    def load_config(self): 
        if not os.path.exists(CONFIG_FILE): self.save_config()
        self.config.read(CONFIG_FILE)
    def toggle_top(self): self.root.attributes('-topmost', self.on_top.get())
    def cal(self, sec): CalibrationWizard(self.root, sec, self.config, self.save_config)
    def toggle_loop(self):
        if self.loop_active: self.loop_active = False; self.btn_loop.config(text="START PĘTLI", bg="#005500"); self.log("STOP.")
        else: self.loop_active = True; self.btn_loop.config(text="STOP", bg="#880000"); threading.Thread(target=self.loop_worker, daemon=True).start()
    def loop_worker(self):
        while self.loop_active:
            self.run_tasks(is_loop=True); mins = self.interval_min.get(); self.next_run_time = time.time() + (mins * 60)
            while time.time() < self.next_run_time:
                if not self.loop_active: return
                time.sleep(1)
    def _retrieve_ai_response(self, sec, gem):
        c = self.config[sec]; self._click(c, 'ai_tab'); time.sleep(0.5)
        if 'ai_scroll_point_x' in c:
            self._click(c, 'ai_scroll_point')
            for _ in range(10): pyautogui.scroll(-500); time.sleep(0.02)
        else: pyautogui.press('pagedown')
        time.sleep(1); self._click(c, 'ai_copy'); time.sleep(1); self._paste(gem, f"RAPORT {sec}", pyperclip.paste())
    def _copy_txt(self): pyautogui.hotkey('ctrl', 'a'); time.sleep(0.3); pyautogui.hotkey('ctrl', 'c'); time.sleep(0.5)
    def _paste(self, gem, h, t): self._click(gem, 'gem_tab'); self._click(gem, 'gem_input'); pyperclip.copy(f"\n==={h}===\n"); pyautogui.hotkey('ctrl', 'v'); time.sleep(0.2); pyperclip.copy(t); pyautogui.hotkey('ctrl', 'v'); time.sleep(1)
    def _ss(self, src, dest, k1, k2): pyautogui.press('printscreen'); time.sleep(2); x1=int(src[f'{k1}_x']); y1=int(src[f'{k1}_y']); x2=int(src[f'{k2}_x']); y2=int(src[f'{k2}_y']); pyautogui.moveTo(x1,y1); pyautogui.mouseDown(); pyautogui.moveTo(x2,y2,0.5); pyautogui.mouseUp(); time.sleep(1); self._paste_ss(dest)
    def _paste_ss(self, gem): self._click(gem, 'gem_tab'); self._click(gem, 'gem_input'); pyautogui.hotkey('ctrl', 'v'); time.sleep(1.5)
    def _click(self, c, k):
        if f"{k}_x" in c: pyautogui.click(int(c[f"{k}_x"]), int(c[f"{k}_y"])); time.sleep(0.3)
        else: self.log(f"Brak: {k}")

if __name__ == "__main__":
    root = tk.Tk()
    app = IntelAgentHUB(root)
    root.mainloop()