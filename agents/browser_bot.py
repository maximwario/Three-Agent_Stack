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
import pyautogui
import time
import pyperclip
import subprocess
import os
from utils.logger import AgentLogger

class BrowserBot:
    def __init__(self, config_manager):
        self.cfg = config_manager
        self.log = AgentLogger("BROWSER_BOT")
        self.pause = 0.5
        self.assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets')
        
    def _get_timing(self, key, default=0.5):
        return self.cfg.get_float('TIMING', key, fallback=default)

    def verify_page_active(self, section_name):
        if self.cfg.get('SYSTEM', 'verify_pages', fallback='False') != 'True': return True
        safe_name = section_name.replace("AI_", "").replace("_CONTROLS", "").replace("BINANCE", "BINANCE").upper()
        logo_path = os.path.join(self.assets_dir, f"logo_{safe_name}.png")
        if not os.path.exists(logo_path): return True
        try:
            return pyautogui.locateOnScreen(logo_path, confidence=0.8, grayscale=True) is not None
        except: return True

    def click_element(self, section, key_prefix, verify=True):
        try:
            x = self.cfg.get(section, f"{key_prefix}_x")
            y = self.cfg.get(section, f"{key_prefix}_y")
            if not x or not y: return False
            if verify and "_tab" in key_prefix:
                if not self.verify_page_active(section):
                    self.log.log(f"Zatrzymano kliknięcie w {section}", "WARN")
                    return False
            
            # Dynamic Mouse Speed
            spd = 0.0
            try:
                s = self.cfg.get('TIMING', 'mouse_speed')
                if s: spd = float(s)
            except: pass
            
            pyautogui.click(int(x), int(y), duration=spd)
            time.sleep(self._get_timing('click_post_wait', 0.5))
            return True
        except: return False

    def find_and_click_image(self, image_name, confidence=0.8, retries=3):
        path = os.path.join(self.assets_dir, image_name)
        if not os.path.exists(path): return False
        for i in range(retries):
            try:
                loc = pyautogui.locateCenterOnScreen(path, confidence=confidence)
                if loc:
                    pyautogui.click(loc)
                    time.sleep(self._get_timing('click_post_wait', 0.5))
                    return True
                time.sleep(self._get_timing('click_post_wait', 0.5)) # Wait before retry
            except: pass
        return False

    def extract_text_from_page(self, section, focus_key="focus"):
        """Pobiera tekst ze strony z czyszczeniem schowka (TABULA RASA)"""
        try:
            # 1. WYCZYŚĆ SCHOWEK (Kluczowe!)
            pyperclip.copy("") 
            
            # 2. Kliknij Focus
            if not self.click_element(section, focus_key, verify=False):
                pyautogui.click(pyautogui.size().width/2, pyautogui.size().height/2)
            time.sleep(self._get_timing('click_post_wait', 0.5))
            
            # 3. Kopiuj (Ctrl+A -> Ctrl+C)
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(self._get_timing('key_hotkey_wait', 0.3))
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(self._get_timing('clipboard_copy_wait', 0.8)) # Czas dla systemu
            pyautogui.click() # Odznacz
            
            # 4. Pobierz
            content = pyperclip.paste()
            
            # Jeśli schowek pusty -> zwróć znacznik braku danych
            if not content or len(content.strip()) == 0:
                return "NO DATA FOUND"
                
            return content
        except Exception as e:
            self.log.log(f"Extract Error: {e}", "ERROR")
            return "ERROR"

    def copy_image_to_clipboard(self, image_path):
        if not os.path.exists(image_path): return False
        try:
            cmd = f"powershell -command \"Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.Clipboard]::SetImage([System.Drawing.Image]::FromFile('{image_path}'))\""
            
            # Zmiana: capture_output=True, text=True aby złapać błędy
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if res.returncode != 0:
                self.log.log(f"Clipboard Error: {res.stderr}", "ERROR")
                return False

            # Pobranie czasu z configu (domyślnie 2.5s dla bezpieczeństwa)
            wait_time = self._get_timing('clipboard_lag', 2.5)
            time.sleep(wait_time)
            
            self.log.log(f"Image to clipboard: OK ({os.path.basename(image_path)})")
            return True
        except Exception as e:
            self.log.log(f"Clipboard Exception: {e}", "ERROR")
            return False

    def paste_content(self):
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(self._get_timing('clipboard_paste_wait', 1.5))

    def paste_text(self, text):
        pyperclip.copy(text)
        time.sleep(0.1)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(self._get_timing('click_post_wait', 0.5))

    def scroll_to_bottom(self, section, scroll_point_key):
        if self.click_element(section, scroll_point_key, verify=False):
            step_wait = self._get_timing('scroll_step_wait', 0.05)
            for _ in range(12): 
                pyautogui.scroll(-800)
                time.sleep(step_wait)
