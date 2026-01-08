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
import pyperclip
from utils.logger import AgentLogger
from agents.browser_bot import BrowserBot

# ... (importy bez zmian) ...

class IntelligenceCouncil:
    def __init__(self, config_manager, strategist_ref, hud_ref=None): # DODANO hud_ref
        self.cfg = config_manager
        self.log = AgentLogger("COUNCIL")
        self.bot = BrowserBot(config_manager)
        self.strategist = strategist_ref
        self.hud = hud_ref # Przechowujemy HUD
        self.consultants = ["GROK", "COPILOT", "DEEPSEEK", "QWEN"]

    def _update_hud(self, ai, status):
        """Helper do aktualizacji diod"""
        if self.hud and self.hud.is_alive():
            self.hud.set_ai_status(ai, status)

    def seed_questions(self):
        self.log.log(">>> FAZA 1: ZASIEW <<<")
        
        # Reset ikon na szaro
        for ai in self.consultants: self._update_hud(ai, "IDLE")

        for ai_name in self.consultants:
            section = f"AI_{ai_name}"
            if not self.cfg.get(section, "ai_tab_x"): continue

            self._update_hud(ai_name, "WORK") # Żółty
            try:
                # ... (logika klikania bez zmian) ...
                # Aktywacja, Input, Paste, Send
                if self.bot.click_element(section, "ai_tab"):
                    time.sleep(self.cfg.get_float('TIMING', 'tab_switch_wait', 0.5))
                    
                    if self.bot.click_element(section, "ai_input"):
                        self.bot.paste_text(self.strategist.current_prompts.get(ai_name, "Analyze."))
                        
                        if not self.bot.find_and_click_image(f"btn_send_{ai_name}.png"):
                            import pyautogui; pyautogui.press('enter')
                        
                        if self.hud: self.hud.log_action(f"{ai_name}: Question sent")
            except Exception as e:
                self.log.log(f"Seed Error {ai_name}: {e}", "WARN")
                self._update_hud(ai_name, "FAIL")

    def active_wait_cycle(self, duration_s):
        """Aktywne czekanie: skacze po zakładkach i scrolluje, by AI nie zasnęło."""
        self.log.log(f"--- ACTIVE KEEP-ALIVE ({int(duration_s)}s) ---")
        import random
        import pyautogui

        start = time.time()
        while (time.time() - start) < duration_s:
            rem = int(duration_s - (time.time() - start))
            if rem <= 0: break

            # Jeśli zostało mało czasu, po prostu śpij
            if rem < 5: 
                time.sleep(rem)
                break

            # Iteruj po AI
            for ai_name in self.consultants:
                # Sprawdź czy AI w ogóle aktywne w configu
                section = f"AI_{ai_name}"
                if not self.cfg.get(section, "ai_tab_x"): continue

                # Sprawdź czy mamy jeszcze czas (sprawdzamy wewnątrz pętli też)
                if (time.time() - start) >= duration_s: break

                try:
                    # Update HUD
                    if self.hud: self.hud.update_mission("KEEP-ALIVE", int(duration_s - (time.time() - start)), ai_name)

                    # Klik w zakładkę
                    self.bot.click_element(section, "ai_tab", verify=False)
                    time.sleep(self.cfg.get_float('TIMING', 'tab_switch_wait', 0.5))

                    # Scroll (Mouse Wheel)
                    # Najbezpieczniej najechać na środek ekranu
                    # Ale jeśli nie mamy koordynatów "safe_point", to po prostu scrollujemy tam gdzie mysz (zazwyczaj zakładka)
                    # Lepiej przesunąć mysz nieco w dół od zakładki
                    
                    # Pobierz koordynaty zakładki, żeby wiedzieć gdzie jesteśmy mniej więcej
                    # Ale bot.click_element już przeniósł mysz.
                    # Przesuńmy mysz w dół o 200px (na treść) i scroll
                    pyautogui.move(0, 200)
                    pyautogui.scroll(-300) # lekko w dół
                    time.sleep(self.cfg.get_float('TIMING', 'scroll_step_wait', 0.5))
                    pyautogui.scroll(100)  # lekko w górę (symulacja czytania)
                    
                    # Odczekaj chwilę na tej zakładce (np. 1/4 pozostałego czasu, ale max 10s)
                    wait_step = min(rem, 10.0) / len(self.consultants)
                    if wait_step < 2: wait_step = 2
                    time.sleep(wait_step)

                except Exception as e:
                    self.log.log(f"KeepAlive Error {ai_name}: {e}", "WARN")

    def harvest_responses(self):
        self.log.log(">>> FAZA 3: ŻNIWA <<<")
        full_report = ""
        
        for ai_name in self.consultants:
            section = f"AI_{ai_name}"
            if not self.cfg.get(section, "ai_tab_x"): continue
            
            self._update_hud(ai_name, "WORK") # Żółty
            try:
                # ... (logika powrotu, scrolla i copy bez zmian) ...
                if self.bot.click_element(section, "ai_tab"):
                    time.sleep(self.cfg.get_float('TIMING', 'tab_switch_wait', 0.5))
                    # Scroll logic...
                    if self.cfg.get(section, "ai_scroll_x"): self.bot.scroll_to_bottom(section, "ai_scroll")
                    else: 
                        import pyautogui
                        self.bot.click_element(section, "ai_input", verify=False)
                        step_wait = self.cfg.get_float('TIMING', 'scroll_step_wait', 0.05)
                        for _ in range(15): 
                            pyautogui.scroll(-800)
                            time.sleep(step_wait)
                    
                    time.sleep(self.cfg.get_float('TIMING', 'page_load_wait', 1.0))
                    import pyperclip; pyperclip.copy("")
                    
                    success = False
                    if self.bot.find_and_click_image(f"btn_copy_{ai_name}.png"): success = True
                    elif self.bot.click_element(section, "ai_copy", verify=False): success = True
                    
                    if success:
                        time.sleep(self.cfg.get_float('TIMING', 'clipboard_copy_wait', 0.5))
                        txt = pyperclip.paste()
                        if len(txt) > 10:
                            full_report += f"\n=== RAPORT {ai_name} ===\n{txt[:2500]}...\n"
                            self._update_hud(ai_name, "OK") # Zielony!
                            if self.hud: self.hud.log_action(f"{ai_name}: Data harvested")
                        else:
                            self._update_hud(ai_name, "FAIL")
                            if self.hud: self.hud.log_action(f"{ai_name}: Empty clipboard")
                    else:
                        self._update_hud(ai_name, "FAIL")
            except Exception as e:
                self.log.log(f"Harvest Error {ai_name}: {e}", "ERROR")
                self._update_hud(ai_name, "FAIL")

        return full_report