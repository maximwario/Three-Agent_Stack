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
import sys, os, traceback
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
from pynput import keyboard
from utils.helpers import CalibrationWizard
from config_manager import ConfigManager
# ZMIANA 1: Nowy import orkiestratora stanów
from core.state_orchestrator import StateOrchestrator
from utils.logger import AgentLogger
# IMPORTUJEMY HUD
from hud import HeadsUpDisplay 

class MainGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Perceptron v0.9.2 (Black Box Edition)") # Zaktualizowana wersja
        self.root.geometry("800x700")
        self.root.configure(bg="#1e1e1e")
        
        # PROTOCOL HANDLER
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.cfg = ConfigManager()
        self.log = AgentLogger("SYSTEM")
        
        # MENU
        self.create_menu()
        
        # GLOBAL EXCEPTION
        sys.excepthook = self.handle_exception
        
        # --- ZMIANA 2: PODMIANA W KONSTRUKTORZE ---
        # Inicjalizujemy nową maszynę stanów
        self.orchestrator = StateOrchestrator(self.cfg)
        
        # HUD otrzymuje callback do zatrzymywania maszyny stanów
        self.hud = HeadsUpDisplay(self.root, config_manager=self.cfg, stop_callback=self.orchestrator.stop_loop)
        
        # Wstrzykujemy HUD do orkiestratora
        self.orchestrator.hud = self.hud
        # ------------------------------------------
        
        # Hotkeys
        self.listener = keyboard.GlobalHotKeys({'<f3>': self.emergency_stop})
        self.listener.start()
        
        self.create_widgets()
        self.update_log_loop()

    def handle_exception(self, exc_type, exc_value, exc_traceback):
        """Globalny handler błędów"""
        err_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        self.log.log(f"CRITICAL ERROR: {exc_value}", "CRASH")
        messagebox.showerror("Critical Error", f"Wystąpił nieoczekiwany błąd:\n{exc_value}\n\nSprawdź logi.")
        with open("crash_dump.txt", "w", encoding="utf-8") as f: f.write(err_msg)

    def create_menu(self):
        menubar = tk.Menu(self.root)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.on_close)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # SYSTEM SETTINGS MENU
        sys_menu = tk.Menu(menubar, tearoff=0)
        # AGENT 3 SWITCH
        self.a3_var = tk.BooleanVar(value=self.cfg.get('SYSTEM', 'agent_3_enabled', 'True') == 'True')
        def toggle_a3_menu():
             self.cfg.set_and_save('SYSTEM', 'agent_3_enabled', str(self.a3_var.get()))
             if hasattr(self, 'hud') and self.hud and self.hud.is_alive():
                 self.hud._refresh_a3_visuals()
                 
        sys_menu.add_checkbutton(label="ENABLE AGENT 3 (EXECUTION)", variable=self.a3_var, command=toggle_a3_menu)
        sys_menu.add_separator()
        
        # Signal - CLI
        tk.Label(self.root, text="--- CLI-SIGNAL ---", bg="#1e1e1e", fg="yellow").pack()
        tk.Button(self.root, text="Konfiguruj Signal", command=self.setup_signal_ui, bg="#333", fg="white").pack(fill='x', padx=50)

        # WEB SCRAPER OPTS
        self.web_txt_var = tk.BooleanVar(value=self.cfg.get('SYSTEM', 'web_scraping_txt', 'False') == 'True')
        self.web_ss_var = tk.BooleanVar(value=self.cfg.get('SYSTEM', 'web_scraping_ss', 'False') == 'True')
        
        def save_web_settings():
            self.cfg.set_and_save('SYSTEM', 'web_scraping_txt', str(self.web_txt_var.get()))
            self.cfg.set_and_save('SYSTEM', 'web_scraping_ss', str(self.web_ss_var.get()))
            self.log.log(f"Web Settings: TXT={self.web_txt_var.get()}, SS={self.web_ss_var.get()}", "CONFIG")

        sys_menu.add_checkbutton(label="Enable Text Scraping (JSON)", variable=self.web_txt_var, command=save_web_settings)
        sys_menu.add_checkbutton(label="Enable Screenshots", variable=self.web_ss_var, command=save_web_settings)
        sys_menu.add_separator()
        sys_menu.add_command(label="Run Web PoC (Test)", command=self.run_web_poc_trigger)
        
        menubar.add_cascade(label="Control & Logs", menu=sys_menu)
        self.root.config(menu=menubar)

    def setup_signal_ui(self):
        """Proste okno do wpisania numerów i wygenerowania QR."""
        win = tk.Toplevel(self.root)
        win.title("Kalibracja Signal")
        win.geometry("300x250")
        
        tk.Label(win, text="Twój Numer (+48...)").pack()
        ent_user = tk.Entry(win); ent_user.insert(0, self.cfg.get('SIGNAL', 'recipient_phone', '')); ent_user.pack()
        
        def save_and_qr():
            self.cfg.set('SIGNAL', 'recipient_phone', ent_user.get())
            self.cfg.save()
            # Tutaj wywołujemy Twoją funkcję z test_signal.py
            from setup_signal_qr import generate_local_signal_qr
            generate_local_signal_qr() 
            messagebox.showinfo("QR", "Zeskanuj wygenerowany kod QR w telefonie.")

        tk.Button(win, text="Zapisz i Generuj QR", command=save_and_qr).pack(pady=20)
    
    def on_close(self):
        if messagebox.askokcancel("Quit", "Czy na pewno chcesz zamknąć system?"):
            self.log.log("Zamykanie systemu...", "SYSTEM")
            if self.orchestrator:
                self.orchestrator.stop_loop()
            if self.listener:
                self.listener.stop()  # ← DODANE
            self.root.destroy()
            sys.exit(0)

    def emergency_stop(self):
        self.log.log("!!! KILL SWITCH (F3) !!!", "CRITICAL")
        if self.orchestrator:
            self.orchestrator.stop_loop()
        if self.hud and self.hud.is_alive():
            self.hud.update_mission("STOPPED", 0, "F3 KILL", "USER INTERRUPT")

    def create_widgets(self):
        top = tk.Frame(self.root, bg="#252526")
        top.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Button(top, text="▶ START", bg="#006400", fg="white", font=("Arial", 10, "bold"), command=self.orchestrator.start_loop).pack(side=tk.LEFT, padx=2)
        tk.Button(top, text="⏹ STOP", bg="#8B0000", fg="white", font=("Arial", 10, "bold"), command=self.orchestrator.stop_loop).pack(side=tk.LEFT, padx=2)
        tk.Button(top, text="⚡ RUN ONCE", bg="#444", fg="white", command=self.orchestrator.run_once).pack(side=tk.LEFT, padx=2)
        
        tk.Button(top, text="🛠 KALIBRACJA", bg="#222", fg="gray", command=self.open_cal).pack(side=tk.RIGHT, padx=5)
        tk.Button(top, text="⏱️ TIMING", bg="#004444", fg="cyan", font=("Arial", 9, "bold"), command=self.open_timing).pack(side=tk.RIGHT, padx=5)
        
        self.log_area = scrolledtext.ScrolledText(self.root, bg="#111", fg="#00ff00", font=("Consolas", 10))
        self.log_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def open_timing(self):
        """Okno dostrajania czasów - TWOJA PEŁNA KONFIGURACJA"""
        t = tk.Toplevel(self.root)
        t.title("Chronos Settings - Szczegółowa Konfiguracja")
        t.configure(bg="#222")
        t.geometry("1100x750")
        
        canvas = tk.Canvas(t, bg="#222", highlightthickness=0)
        scrollbar = ttk.Scrollbar(t, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#222")

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        params = [
            ("Loop Interval", "loop_interval_min", 1, 120, "SYSTEM", 1, "Co ile minut bot wykonuje pełny cykl analizy (Main Loop)."),
            ("Grok Wait", "grok_wait", 10, 300, "TIMING", 10, "Czas (s) oczekiwania na wygenerowanie odpowiedzi przez Groka."),
            ("Copilot Wait", "copilot_wait", 10, 300, "TIMING", 10, "Czas (s) na odpowiedź Copilota (Bing/GPT-4)."),
            ("DeepSeek Wait", "deepseek_wait", 10, 600, "TIMING", 10, "Czas (s) dla DeepSeek R1 (wymaga dłuższego myślenia)."),
            ("Qwen Wait", "qwen_wait", 10, 300, "TIMING", 10, "Czas (s) na odpowiedź modelu Qwen."),
            ("Gemini Think", "gemini_think", 30, 300, "TIMING", 5, "Czas (s) dla Gemini (Master) na syntezę danych i decyzję."),
            ("Global AI Wait", "ai_wait_seconds", 30, 600, "TIMING", 10, "Minimalny czas oczekiwania na AI (jeśli inne nie są aktywne)."),
            ("Vision Load", "vision_load", 0.5, 10.0, "TIMING", 0.1, "Czas (s) na załadowanie zrzutu ekranu lub strony (np. Heatmap)."),
            ("Page Load Wait", "page_load_wait", 0.5, 10.0, "TIMING", 0.1, "Oczekiwanie (s) po pełnym przeładowaniu strony w przeglądarce."),
            ("Tab Switch Wait", "tab_switch_wait", 0.1, 3.0, "TIMING", 0.1, "Oczekiwanie (s) po kliknięciu w kartę (na renderowanie GUI)."),
            ("API Request Wait", "api_request_interval", 0.1, 5.0, "TIMING", 0.1, "Minimalny odstęp (s) między zapytaniami do API Coinglass."),
            ("Clipboard Lag", "clipboard_lag", 0.1, 5.0, "TIMING", 0.1, "Opóźnienie systemowe PowerShell przy kopiowaniu obrazków."),
            ("Clip Copy Wait", "clipboard_copy_wait", 0.1, 3.0, "TIMING", 0.1, "Czas (s) po Ctrl+C (system musi zdążyć skopiować tekst)."),
            ("Clip Paste Wait", "clipboard_paste_wait", 0.1, 3.0, "TIMING", 0.1, "Czas (s) po Ctrl+V (aplikacja musi zdążyć przyjąć dane)."),
            ("Mouse Speed", "mouse_speed", 0.0, 2.0, "TIMING", 0.01, "Czas trwania ruchu kursora (0 = teleport, >0 = human-like)."),
            ("Click Post Wait", "click_post_wait", 0.0, 2.0, "TIMING", 0.05, "Pauza (s) po każdym kliknięciu myszą (dla stabilności)."),
            ("Scroll Speed", "scroll_speed", 0.0, 2.0, "TIMING", 0.05, "Ogólny mnożnik szybkości operacji przewijania."),
            ("Scroll Step Wait", "scroll_step_wait", 0.00, 0.5, "TIMING", 0.01, "Pauza (s) między pojedynczymi krokami scrolla (płynność)."),
            ("Hotkey Wait", "key_hotkey_wait", 0.0, 1.0, "TIMING", 0.01, "Pauza (s) między klawiszami w skrótach (np. Ctrl... A)."),
        ]
        
        vars_map = {}
        for label, key, min_v, max_v, section, res, desc in params:
            f = tk.Frame(scrollable_frame, bg="#222")
            f.pack(fill=tk.X, padx=10, pady=5)
            tk.Label(f, text=label, fg="cyan", bg="#222", width=20, anchor="w", font=("Arial", 9, "bold")).pack(side=tk.LEFT)
            try: val_float = self.cfg.get_float(section, key)
            except: val_float = min_v
            val = tk.DoubleVar(value=val_float)
            vars_map[(key, section)] = val
            tk.Scale(f, variable=val, from_=min_v, to=max_v, resolution=res, orient=tk.HORIZONTAL, 
                     bg="#333", fg="white", highlightthickness=0, length=200).pack(side=tk.LEFT, padx=10)
            tk.Label(f, text=desc, fg="gray", bg="#222", anchor="w", font=("Arial", 9)).pack(side=tk.LEFT, fill=tk.X, expand=True)

        def save():
            for (k, section), v in vars_map.items():
                val = v.get()
                s_val = str(int(val)) if val > 10 or k == "loop_interval_min" else str(round(val, 3))
                self.cfg.set_and_save(section, k, s_val)
            t.destroy()
            self.log.log("Zapisano precyzyjne ustawienia czasu.", "CONFIG")

        tk.Button(t, text="ZAPISZ WSZYSTKO", bg="#006400", fg="white", font=("Arial", 12, "bold"), command=save).pack(pady=10, side=tk.BOTTOM)
    
    def open_cal(self):
        """TWOJE PEŁNE OKNO KALIBRACJI"""
        w = tk.Toplevel(self.root); w.configure(bg="#222")
        def r(s): CalibrationWizard(self.root, s, self.cfg, lambda: print("OK"))
        tk.Label(w, text="PLATFORMY", bg="#222", fg="orange").pack()
        tk.Button(w, text="Gemini", command=lambda: r("GEMINI_CONTROLS")).pack()
        tk.Button(w, text="Binance (Browser Tab)", command=lambda: r("BINANCE_CONTROLS")).pack()
        tk.Button(w, text="Binance (Deep Dive)", command=lambda: r("BINANCE_INTERNAL"), bg="#440000", fg="white").pack()
        tk.Button(w, text="TradingView (Deep Dive)", command=lambda: r("TRADINGVIEW_INTERNAL"), bg="#000044", fg="white").pack()
        tk.Button(w, text="Coinglass", command=lambda: r("COINGLASS")).pack()
        tk.Button(w, text="Bitmex", command=lambda: r("BITMEX")).pack()
        tk.Button(w, text="TradingView (Tab)", command=lambda: r("TRADINGVIEW")).pack()
        tk.Label(w, text="AI", bg="#222", fg="cyan").pack()
        for ai in ["GROK", "COPILOT", "DEEPSEEK", "QWEN"]:
            tk.Button(w, text=ai, command=lambda x=ai: r(f"AI_{x}")).pack()
            
        tk.Label(w, text="WEB INDICATORS (v0.6.6)", bg="#222", fg="#ff00ff").pack()
        ind_map = {"A": "A. Open Interest", "B": "B. L/S Ratio", "C": "C. Liquidations", "D": "D. Heatmap", "E": "E. Orderbook Walls", "F": "F. Funding Rate"}
        for k, v in ind_map.items():
            tk.Button(w, text=v, command=lambda x=k: r(f"WEB_INDICATOR_{x}")).pack()
            
    def run_web_poc_trigger(self):
        if messagebox.askyesno("Web PoC", "Czy chcesz uruchomić test skrobania (run_web_poc.py)?"):
            try:
                import subprocess
                subprocess.Popen(["python", "run_web_poc.py"], cwd=os.getcwd())
            except Exception as e: messagebox.showerror("Error", f"Nie udało się uruchomić: {e}")
            
    def update_log_loop(self):
        try:
            with open("system_log.txt", "r", encoding="utf-8") as f:
                c = f.read()
                if len(c)>5000: c=c[-5000:]
                self.log_area.delete(1.0, tk.END); self.log_area.insert(tk.END, c); self.log_area.see(tk.END)
        except: pass
        self.root.after(1000, self.update_log_loop)

if __name__ == "__main__":
    root = tk.Tk(); app = MainGUI(root)
    root.mainloop()