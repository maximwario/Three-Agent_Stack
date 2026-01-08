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
# Wpisz TP i # Wpisz SL są zahardkodowane dwa TIMINGi tutaj do okna TP/SL binance
import time
import pyautogui
import pyperclip
from utils.logger import AgentLogger

class ExecutionAgent:
    def __init__(self, config_manager, browser_bot):
        self.cfg = config_manager
        self.log = AgentLogger("AGENT_3")
        self.bot = browser_bot
        
        # Konfiguracja timeingu
        self.type_interval = 0.15  # Wolne wpisywanie cyfr
        self.click_wait = 0.7      # Czekanie po kliknięciu
        
        # Nazwy obrazów (zakładamy, że są w assets)
        self.IMG_TPSL_BTN = "btn_tpsl.png"      # Ikona "ołówek" przy pozycji
        self.IMG_CLOSE_BTN = "btn_close_pos.png" # Ikona "X" lub "Close All"
        self.IMG_CANCEL_BTN = "btc_cancell_all.png" # Ikona "Kosz" lub "Cancel All"
        
    def execute_order(self, decision):
        """
        Główna metoda dispatchera.
        Przyjmuje słownik decision np.:
        {
          "action": "UPDATE_TP/SL",
          "entry_price": 90339,
          "take_profit": 92250,
          "stop_loss": 90450,
          "quantity": "0.025"
        }
        """
        action = decision.get("action", "").upper().replace(" ", "_")
        self.log.log(f"🚀 START: {action}")
        
        # --- AGENT 3 KILL SWITCH ---
        if self.cfg.get("SYSTEM", "agent_3_enabled", "True") != "True":
             self.log.log("⛔ AGENT 3 IS DISABLED (SAFETY SWITCH). SKIPPING EXECUTION.", "WARN")
             return
        
        # Logowanie że przeszliśmy check (dla pewności użytkownika)
        self.log.log("✅ SAFETY SWITCH: ON (Execution Allowed)", "DEBUG")
        # ---------------------------
        
        # Zawsze focus na Binance przed akcją
        if not self._focus_binance():
            self.log.log("❌ Nie udało się aktywować okna Binance!", "ERROR")
            return

        # Routing komendy
        try:
            if action in ["UPDATE_TP/SL", "UPDATE_TPSL"]:
                self._update_tp_sl(decision)
            
            elif action in ["OPEN_LONG_MARKET", "OPEN_LONG"]:
                self._open_position(decision, side="LONG", order_type="MARKET")
                
            elif action in ["OPEN_SHORT_MARKET", "OPEN_SHORT"]:
                self._open_position(decision, side="SHORT", order_type="MARKET")
                
            elif action == "OPEN_LONG_LIMIT":
                self._open_position(decision, side="LONG", order_type="LIMIT")
                
            elif action == "OPEN_SHORT_LIMIT":
                self._open_position(decision, side="SHORT", order_type="LIMIT")
                
            elif action in ["CLOSE_ALL_POSITIONS", "CLOSE_ALL"]:
                self._close_all_positions()
                
            elif action in ["CLOSE_ALL_ORDERS", "CANCEL_ALL"]:
                self._cancel_all_orders()
                
            elif action == "HODL":
                self.log.log("⏳ HODL - Czekam, nie robię nic.")
                
            else:
                self.log.log(f"❓ Nieznana komenda: {action}", "WARN")
                
        except Exception as e:
            self.log.log(f"🔥 BŁĄD WYKONANIA: {e}", "ERROR")

        self.log.log("--- KONIEC SEKWENCJI AGENT 3 ---")

    def _focus_binance(self):
        """Klika w zakładkę Binance aby upewnić się że mamy focus."""
        self.log.log("1. Focus Binance...")
        return self.bot.click_element("BINANCE_CONTROLS", "bin_tab")

    def _click_by_config(self, section, key_name):
        """
        Próbuje kliknąć w koordynaty z configu.
        Zwraca True jeśli koordynaty istniały i kliknięto.
        """
        x = self.cfg.get(section, f"{key_name}_x")
        y = self.cfg.get(section, f"{key_name}_y")
        
        if x and y:
            try:
                self.log.log(f"🎯 Klikam z Configu: {key_name} ({x},{y})")
                
                # Dynamic Timing
                mouse_spd = self.cfg.get_float("TIMING", "mouse_speed", 0.5)
                post_click = self.cfg.get_float("TIMING", "click_post_wait", 0.5)
                
                pyautogui.click(int(x), int(y), duration=mouse_spd) 
                time.sleep(post_click)
                return True
            except Exception as e:
                self.log.log(f"⚠️ Błąd klikania {key_name}: {e}", "WARN")
        return False

    def _switch_to_tab(self, tab_name):
        """Przełącza między zakładkami Pozycje a Zlecenia na dole ekranu."""
        # Pobieramy czas na przeładowanie/odświeżenie widoku (heavy UI change)
        wait_time = self.cfg.get_float("TIMING", "page_load_wait", 1.0)
        
        if tab_name == "POSITIONS":
            self.log.log("👉 Przełączam na zakładkę POZYCJE...")
            if not self._click_by_config("BINANCE_INTERNAL", "bn_sub_positions"):
                self.log.log("⚠️ Brak kalibracji [BINANCE_INTERNAL] bn_sub_positions!", "WARN")
        elif tab_name == "ORDERS":
            self.log.log("👉 Przełączam na zakładkę OTWARTE ZLECENIA...")
            if not self._click_by_config("BINANCE_INTERNAL", "bn_sub_orders"):
                self.log.log("⚠️ Brak kalibracji [BINANCE_INTERNAL] bn_sub_orders!", "WARN")
        
        time.sleep(wait_time)

    def _update_tp_sl(self, data):
        """
        Sekwencja:
        1. Idź do Open Orders
        2. Anuluj wszystko (Cancel All)
        3. Wróć do Positions
        4. Kliknij ołówek
        5. Wypełnij TP/SL
        """
        self.log.log(">>> UPDATE TP/SL (Complex Workflow) <<<")
        
        # KROK 1: Anuluj aktywne zlecenia
        self._switch_to_tab("ORDERS")
        self._cancel_all_orders_logic() # klika kosz
        
        # KROK 2: Wróć do pozycji i edytuj
        self._switch_to_tab("POSITIONS")
        
        tp = str(data.get("take_profit", ""))
        sl = str(data.get("stop_loss", ""))
        
        # Ołówek TP/SL
        if self.bot.find_and_click_image(self.IMG_TPSL_BTN):
             self.log.log("✅ Kliknięto TP/SL (Vision).")
        elif self._click_by_config("BINANCE_CONTROLS", "bin_tpsl"):
             self.log.log("✅ Kliknięto TP/SL (Config Fallback).")
        else:
             self.log.log("⚠️ Nie znaleziono przycisku TP/SL (Ani obraz, ani config)! Abort.", "ERROR")
             return
        
        # Czekamy na modal (to może chwilę potrwać) - tu jest dobrze
        modal_wait = self.cfg.get_float("TIMING", "page_load_wait", 1.0)
        time.sleep(modal_wait) 
        
        # Wpisz TP
        if tp and tp != "0":
            if self._click_by_config("BINANCE_CONTROLS", "bin_modal_tp"):
                # --- POPRAWKA: Czekamy na focus po kliknięciu ---
                time.sleep(0.8) 
                self.log.log(f"Wpisuję TP: {tp}")
                self._write_slowly(tp)
        
        # Wpisz SL
        if sl and sl != "0":
            if self._click_by_config("BINANCE_CONTROLS", "bin_modal_sl"):
                # --- POPRAWKA: Czekamy na focus po kliknięciu ---
                time.sleep(0.8)
                self.log.log(f"Wpisuję SL: {sl}")
                self._write_slowly(sl)
            
        # Zatwierdź
        if not self._click_by_config("BINANCE_CONTROLS", "bin_modal_confirm"):
             if not self._click_by_config("BINANCE_CONTROLS", "bin_confirm"):
                 pyautogui.press('enter')
            
        self.log.log("✅ TP/SL zaktualizowane.")

    def _open_position(self, data, side, order_type):
        """Otwiera pozycję Long/Short Market/Limit."""
        
        qty = str(data.get("quantity", "0.001"))
        entry = str(data.get("entry_price", ""))
        tp = str(data.get("take_profit", ""))
        sl = str(data.get("stop_loss", ""))
        
        self.log.log(f">>> OPEN {side} {order_type} | QTY: {qty} <<<")
        
        # Przerwa po zmianie zakładki/kliknięciu
        click_wait = self.cfg.get_float("TIMING", "click_post_wait", 0.5)

        # Wybierz Typ Zlecenia
        if order_type == "MARKET":
            self._click_by_config("BINANCE_CONTROLS", "bin_market")
            time.sleep(click_wait)
            if self._click_by_config("BINANCE_CONTROLS", "bin_market_qty"):
                self._write_slowly(qty)
            if tp and tp != "0" and self._click_by_config("BINANCE_CONTROLS", "bin_market_tp"):
                 self._write_slowly(tp)
            if sl and sl != "0" and self._click_by_config("BINANCE_CONTROLS", "bin_market_sl"):
                 self._write_slowly(sl)

        elif order_type == "LIMIT":
            self._click_by_config("BINANCE_CONTROLS", "bin_limit")
            time.sleep(click_wait)
            if entry and self._click_by_config("BINANCE_CONTROLS", "bin_limit_price"):
                self._write_slowly(entry)
            if self._click_by_config("BINANCE_CONTROLS", "bin_limit_qty"):
                self._write_slowly(qty)
            if tp and tp != "0" and self._click_by_config("BINANCE_CONTROLS", "bin_limit_tp"):
                 self._write_slowly(tp)
            if sl and sl != "0" and self._click_by_config("BINANCE_CONTROLS", "bin_limit_sl"):
                 self._write_slowly(sl)

        # Kliknij Buy lub Sell
        if side == "LONG":
            if order_type == "LIMIT":
                if not self._click_by_config("BINANCE_CONTROLS", "bin_buy_limit"):
                    self.log.log("❌ Brak koordynatów bin_buy_limit!", "ERROR")
            else:
                if not self._click_by_config("BINANCE_CONTROLS", "bin_buy"):
                    self.log.log("❌ Brak koordynatów bin_buy!", "ERROR")
                    
        elif side == "SHORT":
            if order_type == "LIMIT":
                if not self._click_by_config("BINANCE_CONTROLS", "bin_sell_limit"):
                    self.log.log("❌ Brak koordynatów bin_sell_limit!", "ERROR")
            else:
                if not self._click_by_config("BINANCE_CONTROLS", "bin_sell"):
                    self.log.log("❌ Brak koordynatów bin_sell!", "ERROR")

    def _close_all_positions(self):
        """Zamyka wszystkie pozycje."""
        self.log.log(">>> CLOSE ALL POSITIONS <<<")
        self._switch_to_tab("POSITIONS")
        
        modal_wait = self.cfg.get_float("TIMING", "page_load_wait", 1.0)
        
        if self.bot.find_and_click_image(self.IMG_CLOSE_BTN):
             time.sleep(modal_wait)
             pyautogui.press('enter')
             self.log.log("✅ Kliknięto Close All (Vision).")
        elif self._click_by_config("BINANCE_CONTROLS", "bin_close_all"):
            time.sleep(modal_wait) 
            if not self._click_by_config("BINANCE_CONTROLS", "bin_confirm"):
                pyautogui.press('enter')
            self.log.log("✅ Kliknięto Close All (Config).")
        else:
            self.log.log("❌ Nie znaleziono przycisku Close All.", "ERROR")

    def _cancel_all_orders(self):
        """Anuluje wszystkie zlecenia (przełącza na tab Orders)."""
        self.log.log(">>> CANCEL ALL ORDERS <<<")
        self._switch_to_tab("ORDERS")
        self._cancel_all_orders_logic()
        
    def _cancel_all_orders_logic(self):
        """Logika klikająca w kosz/cancel all będąc już w zakładce."""
        if self.bot.find_and_click_image(self.IMG_CANCEL_BTN):
             modal_wait = self.cfg.get_float("TIMING", "page_load_wait", 1.0)
             time.sleep(modal_wait)
             pyautogui.press('enter')
             self.log.log("✅ Cancel All clicked (Vision).")
        elif self._click_by_config("BINANCE_CONTROLS", "bin_cancel_all"):
             # Potwierdzenie? Zazwyczaj Cancel All ma potwierdzenie
             modal_wait = self.cfg.get_float("TIMING", "page_load_wait", 1.0)
             time.sleep(modal_wait)
             
             # Czasem wyskakuje modal 'Are you sure?'
             if not self._click_by_config("BINANCE_CONTROLS", "bin_confirm"):
                 pyautogui.press('enter')
             self.log.log("✅ Cancel All clicked (Config).")
        else:
            self.log.log("⚠️ Brak kalibracji bin_cancel_all i brak obrazu btc_cancell_all.", "WARN")
    
    def _write_slowly(self, text):
        """Czyści pole (Ctrl+A, Del) i wpisuje tekst powoli."""
        # Pobieramy timingi klaksonowe
        hk_wait = self.cfg.get_float("TIMING", "key_hotkey_wait", 0.3)
        
        # Dodatkowe upewnienie się, że pole jest aktywne przed Ctrl+A
        time.sleep(0.2)
        
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(hk_wait)
        pyautogui.press('backspace')
        time.sleep(hk_wait)
        
        # --- POPRAWKA: Używamy stałego, bezpiecznego interwału pisania (0.05s) ---
        # Zamiast hk_wait, który może być ustawiony na 0.3s (za wolno) lub zignorowany
        pyautogui.write(str(text), interval=0.05)
