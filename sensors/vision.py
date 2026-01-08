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
import os
from utils.logger import AgentLogger

class VisionSensor:
    def __init__(self, config_manager):
        self.cfg = config_manager
        self.log = AgentLogger("VISION")
        self.temp_dir = "temp_vision"
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)

    def capture_heatmap(self):
        return self._capture_region("COINGLASS", "cg_tab_main", "cg_focus", "cg_ss_1", "cg_ss_2", "heatmap.png")

    def capture_orderbook(self):
        return self._capture_region("BITMEX", "bm_tab", "bm_focus", "bm_ss_1", "bm_ss_2", "orderbook.png")

    def _capture_region(self, section, tab_key, focus_key, tl_key, br_key, filename):
        try:
            # 1. Pobierz czas z configu (Dostrajanie)
            load_wait = self.cfg.get_float('TIMING', 'vision_load', fallback=3.0)
            
            # 2. Kliknij zakładkę
            if not self._safe_click(section, tab_key): return None
            
            # 3. Czekaj na render (Dynamicznie)
            time.sleep(load_wait)
            
            # 4. Focus (Reset popupów)
            self._safe_click(section, focus_key)
            time.sleep(0.5)
            
            # 5. Pobierz koordynaty
            x1 = int(self.cfg.get(section, f"{tl_key}_x"))
            y1 = int(self.cfg.get(section, f"{tl_key}_y"))
            x2 = int(self.cfg.get(section, f"{br_key}_x"))
            y2 = int(self.cfg.get(section, f"{br_key}_y"))
            
            width = abs(x2 - x1)
            height = abs(y2 - y1)
            
            # 6. Screenshot
            path = os.path.join(self.temp_dir, filename)
            pyautogui.screenshot(region=(min(x1,x2), min(y1,y2), width, height)).save(path)
            self.log.log(f"Zapisano: {filename}")
            return path
            
        except Exception as e:
            self.log.log(f"Błąd Vision ({section}): {e}", "ERROR")
            return None

    def _safe_click(self, section, key):
        x = self.cfg.get(section, f"{key}_x")
        y = self.cfg.get(section, f"{key}_y")
        if x and y:
            pyautogui.click(int(x), int(y))
            return True
        return False