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
import tkinter as tk
from tkinter import messagebox
import pyautogui
from pynput import keyboard
import os
import time

class CalibrationWizard:
    def __init__(self, root, section, config_manager, on_complete_callback):
        self.top = tk.Toplevel(root)
        self.top.title(f"Kalibracja: {section}")
        self.top.geometry("550x350")
        self.top.attributes('-topmost', True)
        self.top.configure(bg="#222")
        
        self.section = section
        self.cfg = config_manager
        self.cb = on_complete_callback
        
        # Folder assets - upewnij się, że istnieje
        self.assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets')
        if not os.path.exists(self.assets_dir):
            os.makedirs(self.assets_dir)

        # === DEFINICJE ELEMENTÓW DO KALIBRACJI ===
        self.elements = []
        
        # 1. GŁĘBOKIE ZANURZENIE BINANCE (Deep Dive)
        if section == "BINANCE_INTERNAL":
            self.elements = [
                ("bn_sub_positions", "Tab POZYCJE (Na dole ekranu Binance)"),
                ("bn_sub_orders", "Tab OTWARTE ZLECENIA (Obok pozycji)"),
                ("bn_pos_focus", "Puste tło tabeli (Miejscie kliknięcia przed Ctrl+A)")
            ]
            
        # 2. GŁĘBOKIE ZANURZENIE TRADINGVIEW (Deep Dive) - TEGO BRAKOWAŁO!
        elif section == "TRADINGVIEW_INTERNAL":
            self.elements = [
                ("tv_sub_positions", "Panel Tradingowy - Zakładka POZYCJE"),
                ("tv_sub_orders", "Panel Tradingowy - Zakładka ZLECENIA"),
                ("tv_pos_focus", "Puste tło panelu (Miejsce kliknięcia przed Ctrl+A)")
            ]

        # 3. STANDARDOWE PLATFORMY
        elif section == "COINGLASS":
            self.elements = [
                ("cg_tab_main", "ZAKŁADKA PRZEGLĄDARKI (Celuj w Logo!)"),
                ("cg_focus", "Reset (Puste tło strony)"), 
                ("cg_ss_1", "Heatmapa - Lewy Górny Róg"), 
                ("cg_ss_2", "Heatmapa - Prawy Dolny Róg")
            ]
        elif section == "BITMEX":
            self.elements = [
                ("bm_tab", "ZAKŁADKA PRZEGLĄDARKI (Celuj w Logo!)"), 
                ("bm_focus", "Reset"), 
                ("bm_ss_1", "Orderbook - Lewy Górny Róg"), 
                ("bm_ss_2", "Orderbook - Prawy Dolny Róg")
            ]
        elif section == "TRADINGVIEW":
            self.elements = [
                ("tv_tab", "ZAKŁADKA PRZEGLĄDARKI (Celuj w Logo!)"), 
                ("tv_focus", "Środek Wykresu (Focus)")
            ]
        elif section == "BINANCE_CONTROLS":
             self.elements = [
                 ("bin_tab", "1. LOGO Binance (Zakładka przeglądarki)"), 
                 ("bin_focus", "2. TŁO strony (Kliknij by odznaczyć pola)"),
                 ("bin_tpsl", "3. Ikona OŁÓWKA (TP/SL) przy aktywnej pozycji"),
                 ("bin_modal_tp", "4. Pole TAKE PROFIT (W okienku TP/SL)"),
                 ("bin_modal_sl", "5. Pole STOP LOSS (W okienku TP/SL)"),
                 ("bin_modal_confirm", "6. Przycisk POTWIERDŹ (W okienku TP/SL)"),
                 
                 ("bin_cancel_all", "7. Przycisk KOSZ/Anuluj Wszystko (Zakładka Otwarte Zlecenia)"),
                 ("bin_close_all", "8. Przycisk ZAMKNIJ WSZYSTKIE (Close All przy pozycjach)"),
                 ("bin_confirm", "9. Przycisk POTWIERDŹ (⚠️ Otwórz okienko Close All wcześniej!)"),
                 
                 ("bin_market", "10. Zakładka MARKET (W panelu składania zleceń)"),
                 ("bin_market_qty", "11. Pole ILOŚĆ (Size) w zakładce Market"),
                 ("bin_market_tp", "12. Pole TP (Opcjonalne, w zakładce Market)"),
                 ("bin_market_sl", "13. Pole SL (Opcjonalne, w zakładce Market)"),
                 ("bin_buy", "14. Przycisk KUP/LONG (MARKET)"),
                 ("bin_sell", "15. Przycisk SPRZEDAJ/SHORT (MARKET)"),

                 ("bin_limit", "16. Zakładka LIMIT (W panelu składania zleceń)"),
                 ("bin_limit_price", "17. Pole CENA (Price) w zakładce Limit"),
                 ("bin_limit_qty", "18. Pole ILOŚĆ (Size) w zakładce Limit"),
                 ("bin_limit_tp", "19. Pole TP (Opcjonalne, w zakładce Limit)"),
                 ("bin_limit_sl", "20. Pole SL (Opcjonalne, w zakładce Limit)"),
                 ("bin_buy_limit", "21. Przycisk KUP/LONG (LIMIT)"),
                 ("bin_sell_limit", "22. Przycisk SPRZEDAJ/SHORT (LIMIT)")
            ]

        # 4. KONTROLA GEMINI
        elif section == "GEMINI_CONTROLS":
            self.elements = [
                ("gem_tab", "ZAKŁADKA GEMINI (Logo!)"), 
                ("gem_input", "Pole wpisywania tekstu"), 
                ("gem_send", "Przycisk WYŚLIJ (F2 tworzy asset)"), 
                ("gem_scroll_point", "Środek ekranu (do scrollowania)"), 
                ("gem_copy", "Przycisk KOPIUJ pod odpowiedzią (F2 tworzy asset)")
            ]

        # 5. KONSULTANCI AI (Grok, Copilot...)
        elif section.startswith("AI_"):
            self.elements = [
                ("ai_tab", "ZAKŁADKA PRZEGLĄDARKI (Logo!)"), 
                ("ai_input", "Pole wpisywania tekstu"), 
                ("ai_send", "Przycisk WYŚLIJ (F2 tworzy asset)"), 
                ("ai_copy", "Przycisk KOPIUJ (F2 tworzy asset)"), 
                ("ai_scroll", "Pasek Scrolla lub Tło (Opcjonalne)")
            ]
            
        # 6. NOWE WSKAŹNIKI WWW (Roadmap v0.6.6)
        elif section.startswith("WEB_INDICATOR"):
            self.elements = [
                ("tab", "LOGOTYP KARTY (F2 - Tworzy Asset)"),
                ("focus_text", "ŚRODEK STRONY (Kliknij przed Ctrl+A)"),
                ("focus_scroll", "PUNKT DO SCROLLOWANIA (Pasek/Tło)"),
                ("ss_tl", "Screenshot: LEWY GÓRNY RÓG"),
                ("ss_br", "Screenshot: PRAWY DOLNY RÓG")
            ]

            
        self.step = 0
        
        # UI
        self.lbl = tk.Label(self.top, text="Start...", fg="white", bg="#222", font=("Arial", 12))
        self.lbl.pack(pady=20)
        
        self.lbl_hint = tk.Label(self.top, text="Najedź myszką i wciśnij klawisz [F2]", fg="#00ff00", bg="#222", font=("Consolas", 10, "bold"))
        self.lbl_hint.pack(pady=10)
        
        self.lbl_info = tk.Label(self.top, text="", fg="gray", bg="#222", wraplength=500)
        self.lbl_info.pack(pady=5)
        
        self.listener = keyboard.Listener(on_release=self.on_key)
        self.listener.start()
        self.update_ui()

    def update_ui(self):
        if self.step < len(self.elements):
            key = self.elements[self.step][0]
            name = self.elements[self.step][1]
            
            self.lbl.config(text=f"KROK {self.step+1}/{len(self.elements)}:\n{name}")
            
            # Podpowiedzi kontekstowe
            if "ZAKŁADKA" in name:
                self.lbl_info.config(text="System wytnie mały obrazek wokół kursora (LOGO), aby móc znaleźć tę kartę nawet jak się przesunie.", fg="orange")
            elif "BTN" in name or "copy" in key or "send" in key:
                self.lbl_info.config(text="System wytnie obrazek PRZYCISKU. Upewnij się, że kursor jest na środku ikony!", fg="cyan")
            else:
                self.lbl_info.config(text="Zapisywanie współrzędnych X, Y.", fg="gray")
        else:
            self.finish()

    def on_key(self, key):
        if key == keyboard.Key.f2:
            x, y = pyautogui.position()
            key_name = self.elements[self.step][0]
            
            # 1. Zapisz koordynaty w Configu
            self.cfg.set_and_save(self.section, f"{key_name}_x", x)
            self.cfg.set_and_save(self.section, f"{key_name}_y", y)
            print(f"[CAL] Saved {key_name}: {x},{y}")

            # 2. Tworzenie Assetów (Vision Search)
            if "_tab" in key_name or "copy" in key_name or "send" in key_name or key_name == "tab":
                try:
                    region = (x - 20, y - 20, 40, 40)
                    suffix = self.section.replace("AI_", "").replace("_CONTROLS", "").upper()
                    
                    if "_tab" in key_name or key_name == "tab":
                        filename = f"logo_{suffix}.png"
                    else:
                        action = key_name.split("_")[-1] # copy, send
                        filename = f"btn_{action}_{suffix}.png"
                    
                    save_path = os.path.join(self.assets_dir, filename)
                    pyautogui.screenshot(region=region).save(save_path)
                    print(f"[ASSET] Zapisano obrazek: {filename}")
                    print('\a') 
                except Exception as e:
                    print(f"[ASSET ERROR] {e}")

            self.step += 1
            self.top.after(0, self.update_ui)

    def finish(self):
        self.listener.stop()
        self.top.destroy()
        messagebox.showinfo("Sukces", f"Kalibracja sekcji {self.section} zakończona!")
        if self.cb: self.cb()

# --- FUNKCJE POMOCNICZE ---
def safe_click(config_manager, section, key):
    try:
        x = config_manager.get(section, f"{key}_x")
        y = config_manager.get(section, f"{key}_y")
        if x and y:
            pyautogui.click(int(x), int(y))
            time.sleep(0.3)
            return True
    except: pass
    return False
