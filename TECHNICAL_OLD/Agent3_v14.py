# -*- coding: utf-8 -*-
"""
PROJEKT: TRADING AGENT 3 (v14.0 - HYBRID EXECUTION)
AUTOR: Agent 2 & Operator
DATA: 29.11.2025

CECHY:
- PARSER: Reaguje tylko na [AGENT3_START] (z v12).
- LOGIKA: Pełna obsługa klikania (z v10.1).
- WIZJA: Obsługa 'icon_edit.png' dla UPDATE.
"""

import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
import pyautogui
import pyperclip
import json
import re
import threading
import configparser
import os
import time
from datetime import datetime

CONFIG_FILE = "trading_config_v10.ini"
HISTORY_FILE = "trading_history_v14.txt"
DEFAULT_QUANTITY = "0.002"

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.2

# MAPA ELEMENTÓW DO KALIBRACJI
PLATFORM_ELEMENTS = {
    "BINANCE_COMMON": [
        ("tab_browser", "1. Zakładka przeglądarki (Binance)"),
        ("anchor_point", "2. Pusty punkt na stronie (Reset)"),
        ("tab_positions", "3. Zakładka 'POZYCJE' (Na dole, żeby widzieć otwarte)"),
        ("btn_close_all", "4. Przycisk 'Zamknij Wszystkie / Flash Close'"),
        ("btn_confirm_yellow", "5. Przycisk 'POTWIERDŹ / OK' (Żółty w popupie)")
    ],
    "BINANCE_LIMIT": [
        ("btn_limit_mode", "1. Przycisk trybu 'LIMIT'"),
        ("input_price", "2. Pole CENY (Limit)"),
        ("input_qty", "3. Pole ILOŚCI (BTC)"),
        ("check_tpsl", "4. Checkbox TP/SL (Zaznacz go ręcznie przed kalibracją!)"),
        ("input_tp", "5. Pole TAKE PROFIT"),
        ("input_sl", "6. Pole STOP LOSS"),
        ("btn_long", "7. Przycisk KUP/LONG"),
        ("btn_short", "8. Przycisk SPRZEDAJ/SHORT")
    ],
    "BINANCE_MARKET": [
        ("btn_market_mode", "1. Przycisk trybu 'MARKET'"),
        ("input_qty", "2. Pole ILOŚCI (BTC)"),
        ("check_tpsl", "3. Checkbox TP/SL (Dla Market)"),
        ("input_tp", "4. Pole TAKE PROFIT"),
        ("input_sl", "5. Pole STOP LOSS"),
        ("btn_long", "6. Przycisk KUP/LONG"),
        ("btn_short", "7. Przycisk SPRZEDAJ/SHORT")
    ],
    "BINANCE_UPDATE": [
        ("btn_edit_pencil", "1. Ikonka 'Ołówek' (Edytuj TP/SL)"),
        ("popup_input_tp", "2. Pole TAKE PROFIT (W oknie)"),
        ("popup_input_sl", "3. Pole STOP LOSS (W oknie)"),
        ("popup_btn_confirm", "4. Przycisk 'ZATWIERDŹ'")
    ],
    "TRADINGVIEW": [
        ("tab_browser", "Zakładka przeglądarki (TradingView)"),
        ("anchor_point", "Środek wykresu"),
        ("btn_buy", "Przycisk BUY"),
        ("btn_sell", "Przycisk SELL"),
        ("btn_close", "X przy pozycji"),
        ("input_qty", "Pole Ilości (Units)"),
        ("input_price", "Pole Ceny (Limit)"),
        ("input_tp", "Pole Take Profit"),
        ("input_sl", "Pole Stop Loss"),
        ("tab_limit", "Zakładka Limit"),
        ("tab_market", "Zakładka Market")
    ]
}

def clean_json_string(text):
    text = re.sub(r',(\s*[\}\]])', r'\1', text)
    return text

class CalibrationWizard:
    def __init__(self, master, platform_group, config, on_complete):
        self.top = tk.Toplevel(master); self.top.geometry("600x250"); self.top.configure(bg="#222")
        self.platform_group = platform_group; self.config = config; self.on_complete = on_complete; self.elements = PLATFORM_ELEMENTS[platform_group]; self.current_step = 0
        self.lbl_step = tk.Label(self.top, text="START", font=("Arial", 10, "bold"), fg="orange", bg="#222"); self.lbl_step.pack(pady=5)
        self.lbl_instruction = tk.Label(self.top, text="", font=("Arial", 14, "bold"), fg="white", bg="#222", wraplength=580); self.lbl_instruction.pack(pady=10)
        self.lbl_hint = tk.Label(self.top, text="Najedź i naciśnij [F2]", font=("Arial", 12), fg="#00ff00", bg="#222"); self.lbl_hint.pack(side=tk.BOTTOM, pady=10)
        self.listener = keyboard.Listener(on_release=self.on_key_release); self.listener.start(); self.update_ui()
    def update_ui(self):
        if self.current_step < len(self.elements): 
            key, desc = self.elements[self.current_step]
            self.lbl_step.config(text=f"ELEMENT {self.current_step + 1}/{len(self.elements)}")
            self.lbl_instruction.config(text=desc)
        else: self.finish()
    def on_key_release(self, key):
        try:
            if key == keyboard.Key.f2:
                x, y = pyautogui.position(); self.save_current_step(x, y)
        except: pass
    def save_current_step(self, x, y):
        key, desc = self.elements[self.current_step]
        if self.platform_group not in self.config: self.config[self.platform_group] = {}
        self.config[self.platform_group][f"{key}_x"] = str(x)
        self.config[self.platform_group][f"{key}_y"] = str(y)
        print(f"Zapisano {self.platform_group}.{key}: {x}, {y}")
        print('\a'); self.current_step += 1; self.top.after(0, self.update_ui)
    def finish(self): self.listener.stop(); self.on_complete(); self.top.destroy(); messagebox.showinfo("Gotowe", "Kalibracja sekcji zakończona!")

class TradingAgentCommander:
    def __init__(self, root):
        self.root = root
        self.root.title("Agent 3 - Execution v14")
        self.root.geometry("1100x800")
        self.root.configure(bg="#1e1e1e")
        self.config = configparser.ConfigParser()
        self.is_monitoring = True
        self.last_clipboard_content = ""
        self.current_order_json = None
        self._create_ui()
        self.load_config()
        self.root.after(1000, self.monitor_clipboard_loop)

    def _create_ui(self):
        left_frame = tk.Frame(self.root, bg="#252526", width=350)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        tk.Label(left_frame, text="1. KALIBRACJA (F2)", bg="#252526", fg="white", font=("Arial", 12, "bold")).pack(pady=10)
        lb_bin = tk.LabelFrame(left_frame, text="Binance Modules", bg="#252526", fg="orange")
        lb_bin.pack(fill=tk.X, padx=5, pady=5)
        tk.Button(lb_bin, text="1. Wspólne", bg="#444", fg="white", command=lambda: self.start_calibration("BINANCE_COMMON")).pack(fill=tk.X, pady=2)
        tk.Button(lb_bin, text="2. Tryb LIMIT", bg="#444", fg="white", command=lambda: self.start_calibration("BINANCE_LIMIT")).pack(fill=tk.X, pady=2)
        tk.Button(lb_bin, text="3. Tryb MARKET", bg="#444", fg="white", command=lambda: self.start_calibration("BINANCE_MARKET")).pack(fill=tk.X, pady=2)
        tk.Button(lb_bin, text="4. Tryb UPDATE", bg="#444", fg="white", command=lambda: self.start_calibration("BINANCE_UPDATE")).pack(fill=tk.X, pady=2)
        lb_tw = tk.LabelFrame(left_frame, text="TradingView", bg="#252526", fg="#2962FF")
        lb_tw.pack(fill=tk.X, padx=5, pady=5)
        tk.Button(lb_tw, text="Kalibruj Panel TW", bg="#444", fg="white", command=lambda: self.start_calibration("TRADINGVIEW")).pack(fill=tk.X, pady=2)
        self.var_tpsl_open = tk.BooleanVar(value=True)
        tk.Checkbutton(left_frame, text="Binance TP/SL Otwarte", var=self.var_tpsl_open, bg="#252526", fg="white", selectcolor="#333").pack(pady=10)
        self.var_auto_start = tk.BooleanVar(value=True)
        tk.Checkbutton(left_frame, text="AUTO-START (Danger)", var=self.var_auto_start, bg="#252526", fg="red", selectcolor="#333").pack(pady=5)
        right_frame = tk.Frame(self.root, bg="#1e1e1e")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.lbl_status = tk.Label(right_frame, text="OCZEKIWANIE NA TAG [AGENT3_START]...", bg="#1e1e1e", fg="#00FF00", font=("Consolas", 14, "bold"))
        self.lbl_status.pack(pady=30)
        self.btn_execute = tk.Button(right_frame, text="WYKONAJ ROZKAZ", bg="#444444", fg="white", font=("Arial", 20, "bold"), state=tk.DISABLED, command=self.execute_order_sequence)
        self.btn_execute.pack(fill=tk.X, padx=50, pady=10, ipady=15)
        self.log_box = scrolledtext.ScrolledText(right_frame, bg="#111111", fg="#00FF00", font=("Consolas", 9))
        self.log_box.pack(fill=tk.BOTH, expand=True, pady=10)

    def log(self, msg):
        t = datetime.now().strftime("%H:%M:%S")
        self.log_box.insert(tk.END, f"[{t}] {msg}\n"); self.log_box.see(tk.END)
        with open(HISTORY_FILE, "a", encoding="utf-8") as f: f.write(f"[{t}] {msg}\n")

    def load_config(self): 
        if os.path.exists(CONFIG_FILE): self.config.read(CONFIG_FILE)
    def save_config(self): 
        with open(CONFIG_FILE, 'w') as f: self.config.write(f)
    def start_calibration(self, group): CalibrationWizard(self.root, group, self.config, self.save_config)

    def monitor_clipboard_loop(self):
        if self.is_monitoring:
            try:
                content = pyperclip.paste()
                if content != self.last_clipboard_content:
                    self.last_clipboard_content = content
                    if "[AGENT3_START]" in content:
                        self.parse_instruction(content)
            except: pass
        self.root.after(1000, self.monitor_clipboard_loop)

    def parse_instruction(self, text):
        try:
            match = re.search(r'\[AGENT3_START\](.*?)\[AGENT3_END\]', text, re.DOTALL)
            if match:
                json_str = match.group(1).strip()
                clean_json = clean_json_string(json_str)
                data = json.loads(clean_json)
                self.current_order_json = data
                
                action = data.get('action', 'UNKNOWN')
                price = data.get('entry_price', 'MKT')
                info = f"ROZKAZ: {action} @ {price}"
                self.lbl_status.config(text=info, fg="orange")
                self.log(f"📩 OTRZYMANO: {info}")
                
                if self.var_auto_start.get(): self.execute_order_sequence()
                else: self.btn_execute.config(state=tk.NORMAL, bg="#FF4500", text="WYKONAJ")
        except Exception as e: self.log(f"❌ BŁĄD JSON: {e}")

    def execute_order_sequence(self):
        if not self.current_order_json: return
        self.btn_execute.config(state=tk.DISABLED, bg="#444444", text="PRACUJĘ...")
        threading.Thread(target=self._execution_thread, daemon=True).start()

    def _execution_thread(self):
        order = self.current_order_json
        action = order['action'].upper()
        self.log(f"🚀 START: {action}")

        try:
            coords_common = self.config['BINANCE_COMMON']
            self.log("Binance: Aktywacja...")
            self._click(coords_common, 'tab_browser'); time.sleep(0.5)
            self._click(coords_common, 'anchor_point')

            if "CLOSE" in action:
                self._click(coords_common, 'btn_close_all'); time.sleep(0.5)
                self._click(coords_common, 'btn_confirm_yellow')
                self.log("Binance: Zamknięto pozycje.")

            elif "UPDATE" in action:
                self.log("Tryb UPDATE...")
                coords_upd = self.config['BINANCE_UPDATE']
                self._click(coords_common, 'tab_positions'); time.sleep(1.0)
                try:
                    icon_pos = pyautogui.locateCenterOnScreen('icon_edit.png', confidence=0.9)
                    if icon_pos: pyautogui.click(icon_pos)
                    else: self._click(coords_upd, 'btn_edit_pencil')
                except: self._click(coords_upd, 'btn_edit_pencil')
                time.sleep(1.5)
                if 'take_profit' in order: self._type(coords_upd, 'popup_input_tp', str(order['take_profit']))
                if 'stop_loss' in order: self._type(coords_upd, 'popup_input_sl', str(order['stop_loss']))
                self._click(coords_upd, 'popup_btn_confirm')
                self.log("Binance: Zaktualizowano TP/SL.")

            elif "OPEN" in action:
                order_type = order.get('order_type', 'MARKET').upper()
                if order_type == 'LIMIT':
                    coords = self.config['BINANCE_LIMIT']
                    self._click(coords, 'btn_limit_mode')
                    self._type(coords, 'input_price', str(order['entry_price']))
                    qty = str(order.get('quantity', DEFAULT_QUANTITY))
                    self._type(coords, 'input_qty', qty)
                    if not self.var_tpsl_open.get(): self._click(coords, 'check_tpsl')
                    if 'take_profit' in order: self._type(coords, 'input_tp', str(order['take_profit']))
                    if 'stop_loss' in order: self._type(coords, 'input_sl', str(order['stop_loss']))
                    btn = 'btn_long' if "LONG" in action else 'btn_short'
                    self._click(coords, btn)
                else:
                    coords = self.config['BINANCE_MARKET']
                    self._click(coords, 'btn_market_mode')
                    qty = str(order.get('quantity', DEFAULT_QUANTITY))
                    self._type(coords, 'input_qty', qty)
                    if not self.var_tpsl_open.get(): self._click(coords, 'check_tpsl')
                    if 'take_profit' in order: self._type(coords, 'input_tp', str(order['take_profit']))
                    if 'stop_loss' in order: self._type(coords, 'input_sl', str(order['stop_loss']))
                    btn = 'btn_long' if "LONG" in action else 'btn_short'
                    self._click(coords, btn)
                
                self.log(f"Binance: Zlecenie {action} wysłane.")

        except Exception as e: self.log(f"Błąd Binance: {e}")

        self.log("--- KONIEC ---")
        self.btn_execute.config(text="GOTOWY", bg="gray")
        self.current_order_json = None
        self.lbl_status.config(text="OCZEKIWANIE...", fg="#00FF00")

    def _click(self, coords, key):
        x, y = int(coords.get(f"{key}_x", 0)), int(coords.get(f"{key}_y", 0))
        if x > 0: pyautogui.click(x, y); time.sleep(0.3)

    def _type(self, coords, key, text):
        x, y = int(coords.get(f"{key}_x", 0)), int(coords.get(f"{key}_y", 0))
        if x > 0:
            pyautogui.click(x, y); time.sleep(0.1); pyautogui.click(x, y); time.sleep(0.1); pyautogui.click(x, y)
            pyautogui.press('backspace'); time.sleep(0.1)
            pyautogui.write(str(text)); time.sleep(0.2)

if __name__ == "__main__":
    root = tk.Tk()
    app = TradingAgentCommander(root)
    root.mainloop()